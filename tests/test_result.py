from mini_agent.result import (
    ExecutionRecord,
    RecordKind,
    RunResult,
    RunStatus,
    StopKind,
    StopReason,
)


def test_run_without_stop_reason_is_success() -> None:
    result = RunResult(history=[], state={})

    assert result.status is RunStatus.SUCCESS


def test_run_with_stop_reason_is_failure() -> None:
    stop_reason = StopReason(kind=StopKind.NODE_FAILURE, node="b", detail="boom")

    result = RunResult(history=[], state={}, stop_reason=stop_reason)

    assert result.status is RunStatus.FAILURE


def test_record_without_error_succeeded() -> None:
    record = ExecutionRecord(kind=RecordKind.NODE, node="a", output={"x": 1})

    assert record.succeeded


def test_record_with_error_failed() -> None:
    record = ExecutionRecord(
        kind=RecordKind.NODE, node="a", output={}, error="ValueError: boom"
    )

    assert not record.succeeded
