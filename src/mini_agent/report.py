from mini_agent import messages
from mini_agent.result import ExecutionRecord, RecordKind, RunResult


def format_result(result: RunResult) -> list[str]:
    lines = [format_record(record) for record in result.history]
    lines.append(messages.result_line(result.status))
    return lines


def format_record(record: ExecutionRecord) -> str:
    if record.kind is RecordKind.ERROR_HANDLER:
        label = messages.ERROR_HANDLER_LABEL
    else:
        label = messages.record_label(record.succeeded)
    return f"[{label}] {record.node}"
