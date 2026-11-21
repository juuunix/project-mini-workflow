import argparse
from collections.abc import Sequence
from pathlib import Path

from langchain_core.messages import HumanMessage
from langgraph.types import RetryPolicy
from rich.console import Console
from rich.text import Text

from mini_agent.engine import run_graph
from mini_agent.fake_llm import FakeLLM
from mini_agent.graph import LLM_RETRY_POLICY, build_graph
from mini_agent.report import run_report
from mini_agent.scenarios import DEMO_NODE_LIMITS, DEMO_QUESTIONS, TIMEOUT_QUESTION
from mini_agent.search import DocumentSearch

DEFAULT_DOCS_DIR = Path("data") / "docs"


def run_demo(
    console: Console, docs_dir: Path, llm_retry: RetryPolicy = LLM_RETRY_POLICY
) -> None:
    """시연 질문마다 같은 그래프를 실행하고, 모든 실행이 끝난 뒤 결과를 한꺼번에 출력한다.

    실행하는 대로 출력하면 재시도로 기다리는 시나리오만 늦게 나타나 멈춘 것처럼 보인다.
    """
    llm = FakeLLM(timeout_questions=frozenset({TIMEOUT_QUESTION}))
    graph = build_graph(llm, DocumentSearch.from_directory(docs_dir), llm_retry)

    results = [
        run_graph(
            graph,
            {"messages": [HumanMessage(question)]},
            node_limits=DEMO_NODE_LIMITS,
        )
        for question in DEMO_QUESTIONS
    ]
    for number, result in enumerate(results, start=1):
        console.rule(Text(f"[{number}/{len(results)}]"))
        console.print(run_report(result))
        console.print()


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="미니 에이전트 시연")
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=DEFAULT_DOCS_DIR,
        help="current, archive 폴더가 있는 문서 디렉터리 (기본값: data/docs)",
    )
    args = parser.parse_args(argv)
    run_demo(Console(), args.docs_dir, LLM_RETRY_POLICY)


if __name__ == "__main__":
    main()
