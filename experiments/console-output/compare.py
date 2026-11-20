"""Compare the workflow demo output rendered with plain print, Rich, and Click."""

import argparse
import unicodedata
from collections.abc import Callable

import click
from rich.cells import set_cell_size
from rich.console import Console
from rich.text import Text

Part = tuple[str, str]
Writer = Callable[..., None]

# Terminal cells reserved for the node name column. Hangul takes 2 cells per character.
NODE_WIDTH = 10


def cell_width(text: str) -> int:
    """Count terminal cells by hand, since plain print and Click have no width helper."""
    return sum(2 if unicodedata.east_asian_width(char) in "WF" else 1 for char in text)


def pad_cells(text: str, width: int) -> str:
    return text + " " * max(width - cell_width(text), 0)


RUNS = (
    (
        1,
        "환불 정책",
        [
            ("질의 준비", "검색 질의 생성: 환불 정책"),
            ("경로 선택", "문서 검색 경로"),
            ("RAG 검색", "질의: 환불 정책 | 문서: 환불 안내, 결제 취소 안내"),
            ("문서 처리", "검색 결과 처리 1건: 환불 안내 | 다음 문서로 반복"),
            ("문서 처리", "검색 결과 처리 2건: 결제 취소 안내 | 반복 종료"),
        ],
        "성공 | 문서 2건 처리",
    ),
    (
        2,
        "",
        [
            ("질의 준비", "빈 질의 전달"),
            ("경로 선택", "입력 검증 경로"),
            ("입력 검증", "실패: 질의가 비어 있음 | 엔진 처리: 이 실행을 실패로 종료"),
        ],
        "실패 | 입력 검증",
    ),
)


def plain_writer() -> Writer:
    def write(*parts: Part) -> None:
        print(
            "".join(pad_cells(text, NODE_WIDTH) if role == "node" else text for role, text in parts),
            flush=True,
        )

    return write


def rich_writer() -> Writer:
    console = Console(highlight=False)
    styles = {"title": "bold", "node": "bold cyan", "success": "bold green", "failure": "bold red", "": ""}

    def write(*parts: Part) -> None:
        # Rich ships its own cell width logic; set_cell_size pads to the given cell count.
        console.print(Text.assemble(*[
            (set_cell_size(text, NODE_WIDTH) if role == "node" else text, styles[role])
            for role, text in parts
        ]))

    return write


def click_writer() -> Writer:
    styles = {
        "title": {"bold": True},
        "node": {"fg": "cyan", "bold": True},
        "success": {"fg": "green", "bold": True},
        "failure": {"fg": "red", "bold": True},
        "": {},
    }

    def write(*parts: Part) -> None:
        click.echo("".join(
            click.style(pad_cells(text, NODE_WIDTH) if role == "node" else text, **styles[role])
            for role, text in parts
        ))

    return write


def show_demo(write: Writer) -> None:
    for number, query, steps, result in RUNS:
        write(("title", f"[실행 {number}] 입력: {query or '(빈 입력)'}"))
        for index, (node, summary) in enumerate(steps, start=1):
            status, separator, detail = summary.partition(": ")
            value = (
                (("failure", status), ("", separator + detail))
                if status == "실패" and separator
                else (("", summary),)
            )
            write(("", f"  {index:02d}  "), ("node", node), ("", " | "), *value)

        status, separator, detail = result.partition(" | ")
        role = "success" if status == "성공" else "failure"
        write(("", "  결과  "), (role, status), ("", separator + detail))
        write()

    write(("title", "[시연 완료]"), ("", " 2건 실행 | 성공 1건 | 예상된 실패 1건"))


def main() -> None:
    renderers = {"plain": plain_writer, "rich": rich_writer, "click": click_writer}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library", nargs="?", choices=("all", *renderers), default="all")
    args = parser.parse_args()

    selected = renderers if args.library == "all" else (args.library,)
    for index, name in enumerate(selected):
        if args.library == "all":
            if index:
                print()
            print(f"=== {name} ===", flush=True)
        show_demo(renderers[name]())


if __name__ == "__main__":
    main()
