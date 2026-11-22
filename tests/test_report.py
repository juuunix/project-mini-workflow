from langchain_core.messages import AIMessage

from mini_workflow.report import final_answer, format_output, input_of, table_rows
from mini_workflow.result import (
    ExecutionRecord,
    RecordKind,
    RunResult,
    StopKind,
    StopReason,
)
from mini_workflow.search import Collection, Document


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


def test_failed_error_handler_is_shown_as_failure() -> None:
    failed = ExecutionRecord(
        kind=RecordKind.NODE, node="llm", output={}, error="TimeoutError: 시간 초과"
    )
    handler = ExecutionRecord(
        kind=RecordKind.ERROR_HANDLER, node="llm", output={}, error="KeyError: 'x'"
    )
    result = RunResult(history=[failed, handler], state={})

    rows = table_rows(result)

    assert rows[1] == ("2", "llm → 오류 처리", "실패", "llm", "", "KeyError: 'x'")


def test_input_without_question_is_shown_as_keys_and_values() -> None:
    assert input_of({"topic": "배포"}) == ("입력", "topic: 배포")


def test_report_is_the_answer_when_there_is_no_llm_answer() -> None:
    assert final_answer({"topic": "배포", "report": "정리 결과"}) == "정리 결과"


def test_document_is_shown_by_title_and_id() -> None:
    document = Document(
        doc_id="tech-02-deploy",
        title="서비스 배포 절차",
        collection=Collection.CURRENT,
        text="# 서비스 배포 절차\n\n긴 본문",
    )

    assert format_output({"documents": [document]}) == (
        "documents=[서비스 배포 절차 (tech-02-deploy)]"
    )


def test_multiline_text_is_shown_by_first_line() -> None:
    assert format_output({"report": "첫 줄\n\n둘째 줄\n셋째 줄"}) == (
        "report=첫 줄 (외 3줄)"
    )
