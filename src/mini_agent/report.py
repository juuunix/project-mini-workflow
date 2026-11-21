"""실행 결과를 시연 화면에 보여 줄 Rich 표로 바꾼다.

출력 열은 노드가 반환한 값의 공통 모양(메시지의 글, 도구 요청, 그 밖의 키와 값)만 보고
만든다. 특정 노드나 도구를 알지 않으므로, 새 노드를 추가해도 이 모듈을 고치지 않는다.
"""

from collections import Counter
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from rich import box
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mini_agent.result import ExecutionRecord, RecordKind, RunResult

START = "START"
END = "END"
ERROR_HANDLING = "오류 처리"
STOPPED = "중단"
FINISHED = "종료"
# 색은 상태 글자를 강조하는 데만 쓴다. 색이 없는 환경에서도 글자로 구분된다.
STATUS_STYLES = {
    "성공": "green",
    "실패": "bold red",
    ERROR_HANDLING: "yellow",
    STOPPED: "bold red",
    FINISHED: "dim",
}
# 표의 한 줄: 번호, 이동, 상태, 노드, 회차, 출력
type Row = tuple[str, str, str, str, str, str]
STOP_KIND_LABELS = {
    "node_failure": "노드 실패",
    "node_limit_exceeded": "노드별 실행 횟수 상한 초과",
    "step_limit_exceeded": "전체 단계 수 상한 초과",
}


def run_report(result: RunResult) -> RenderableType:
    """실행 하나를 질문 상자, 단계 표, 답변 상자로 만든다."""
    parts: list[RenderableType] = []
    question = first_question(result.state)
    if question is not None:
        parts.append(
            Panel(Text(question), title="질문", title_align="left", expand=False)
        )
    parts.append(step_table(result))
    parts.append(answer_panel(result))
    return Group(*parts)


def step_table(result: RunResult) -> Table:
    table = Table(box=box.SQUARE)
    for column in ["#", "이동", "상태", "노드", "회차"]:
        table.add_column(column, no_wrap=True)
    table.add_column("출력")
    for number, move, status, node, count, output in table_rows(result):
        styled = Text(status, style=STATUS_STYLES[status])
        table.add_row(number, move, styled, node, count, output)
    return table


def table_rows(result: RunResult) -> list[Row]:
    """표에 들어갈 줄. 실행 기록의 줄 뒤에 끝난 방식(END 또는 중단)을 한 줄 더한다."""
    rows, last = step_rows(result.history)
    number = str(len(rows) + 1)
    if result.stop_reason is None:
        rows.append((number, f"{last} → {END}", FINISHED, "", "", ""))
    else:
        stop = result.stop_reason
        reason = f"{STOP_KIND_LABELS[stop.kind]} ({stop.node}, {stop.detail})"
        rows.append((number, f"{last} → {STOPPED}", STOPPED, "", "", reason))
    return rows


def step_rows(history: list[ExecutionRecord]) -> tuple[list[Row], str]:
    """실행 기록을 표의 줄로 바꾸고, 마지막으로 머문 곳(다음 이동의 출발점)을 돌려준다."""
    rows: list[Row] = []
    counts: Counter[str] = Counter()
    previous = START
    for number, record in enumerate(history, start=1):
        if record.error is not None:
            output = record.error
        else:
            output = format_output(record.output)
        if record.kind is RecordKind.ERROR_HANDLER:
            move = f"{record.node} → {ERROR_HANDLING}"
            rows.append((str(number), move, ERROR_HANDLING, record.node, "", output))
            previous = ERROR_HANDLING
            continue
        counts[record.node] += 1
        status = "성공" if record.succeeded else "실패"
        move = f"{previous} → {record.node}"
        count = str(counts[record.node])
        rows.append((str(number), move, status, record.node, count, output))
        previous = record.node
    return rows, previous


def answer_panel(result: RunResult) -> Panel:
    """답변을 담고, 결과(성공·실패와 노드별 실행 횟수)는 상자 아래 테두리에 적는다.

    답변 없이 중단된 실행은 결과만 담은 상자로 보여 준다.
    """
    summary = result_text(result)
    answer = final_answer(result.state)
    if answer is None:
        return Panel(Text(summary), title="결과", title_align="left", expand=False)
    return Panel(
        Text(answer),
        title="답변",
        title_align="left",
        subtitle=Text(summary),
        subtitle_align="right",
        expand=False,
    )


def first_question(state: dict[str, Any]) -> str | None:
    for message in state.get("messages", []):
        if isinstance(message, HumanMessage):
            return message.text
    return None


def format_output(output: dict[str, Any]) -> str:
    """노드가 반환한 값을 한 줄로 바꾼다.

    메시지는 글과 도구 요청을, 그 밖의 값은 키와 값을 보여 준다.
    """
    parts: list[str] = []
    for key, value in output.items():
        if key == "messages":
            parts.extend(format_message(message) for message in value)
        else:
            parts.append(f"{key}={format_value(value)}")
    return ", ".join(part for part in parts if part)


def format_message(message: BaseMessage) -> str:
    parts = [" ".join(message.text.split())]
    if isinstance(message, AIMessage):
        for call in message.tool_calls:
            args = ", ".join(
                f"{name}={format_argument(value)}"
                for name, value in call["args"].items()
            )
            parts.append(f"{call['name']}({args})")
    return " ".join(part for part in parts if part)


def format_argument(value: object) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    return format_value(value)


def format_value(value: object) -> str:
    if isinstance(value, dict):
        items = ", ".join(f"{key}: {format_value(item)}" for key, item in value.items())
        return f"{{{items}}}"
    if isinstance(value, list):
        return f"[{', '.join(format_value(item) for item in value)}]"
    return str(value)


def final_answer(state: dict[str, Any]) -> str | None:
    """마지막 메시지가 도구 요청이 아닌 글로 된 LLM 응답이면 그 글을 답변으로 본다."""
    messages = state.get("messages", [])
    if messages and isinstance(messages[-1], AIMessage) and not messages[-1].tool_calls:
        return messages[-1].text
    return None


def result_text(result: RunResult) -> str:
    label = "성공" if result.stop_reason is None else "실패"
    counts = Counter(
        record.node for record in result.history if record.kind is RecordKind.NODE
    )
    runs = ", ".join(f"{node} {count}회" for node, count in counts.items())
    return f"{label} · {runs}" if runs else label
