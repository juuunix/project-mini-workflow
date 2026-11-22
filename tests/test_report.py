from langchain_core.messages import AIMessage

from mini_workflow.report import format_output, table_rows
from mini_workflow.result import (
    ExecutionRecord,
    RecordKind,
    RunResult,
    StopKind,
    StopReason,
)


def test_message_text_is_shown_as_output() -> None:
    assert format_output({"messages": [AIMessage("요약: 끝")]}) == "요약: 끝"


def test_tool_request_is_shown_with_name_and_arguments() -> None:
    request = AIMessage(
        content="",
        tool_calls=[{"name": "send_email", "args": {"to": "hr", "n": 2}, "id": "c"}],
    )

    assert format_output({"messages": [request]}) == 'send_email(to="hr", n=2)'


def test_non_message_values_are_shown_as_key_and_value() -> None:
    output = {"score": 0.82, "detail": {"label": "positive"}}

    assert format_output(output) == "score=0.82, detail={label: positive}"


def test_stopped_run_ends_with_stop_row() -> None:
    record = ExecutionRecord(kind=RecordKind.NODE, node="search", output={})
    stop = StopReason(
        kind=StopKind.NODE_LIMIT_EXCEEDED, node="search", detail="상한 4회"
    )
    result = RunResult(history=[record], state={}, stop_reason=stop)

    rows = table_rows(result)

    assert rows[-1] == (
        "2",
        "search → 중단",
        "중단",
        "",
        "",
        "노드별 실행 횟수 상한 초과 (search, 상한 4회)",
    )
