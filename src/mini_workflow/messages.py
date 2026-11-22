from pathlib import Path


def error_reason(error: BaseException) -> str:
    return f"{type(error).__name__}: {error}"


def step_limit_detail(limit: int) -> str:
    return f"상한 {limit}단계"


def node_limit_detail(limit: int) -> str:
    return f"상한 {limit}회"


DIRECT_ANSWER = (
    "안녕하세요. 오늘 날짜를 물어보시거나, "
    "문서를 찾으려면 질문 끝에 '찾아줘'나 '검색해줘'를 붙여 주세요."
)
ARCHIVE_NOTICE = "보관 처리된 문서에서 찾은 내용이라 현재와 다를 수 있습니다."
NOT_FOUND_ANSWER = "현행 문서와 보관 문서에서 관련 문서를 찾지 못했습니다."


def found_answer(passage: str, title: str, doc_id: str) -> str:
    return f"{passage}\n\n참고 문서: {title} ({doc_id})"


def tool_failed_answer(tool_name: str, reason: str) -> str:
    return f"도구 {tool_name} 실행에 실패해 답변하지 못했습니다. ({reason})"


def unknown_tool(tool_name: str) -> str:
    return f"FakeLLM이 결과를 읽는 규칙이 없는 도구입니다: {tool_name}"


def unmatched_tool_result(tool_call_id: str) -> str:
    return f"도구 결과에 해당하는 요청이 없습니다: {tool_call_id}"


def llm_timeout(question: str) -> str:
    return f"LLM 응답 시간 초과: {question}"


COLLECTION_LABELS = {"current": "현행", "archive": "보관"}
WORKFLOW_LABELS = {"agent": "에이전트", "document_history": "문서 이력"}


def scenario_heading(workflow: str, number: int, total: int) -> str:
    return f"{WORKFLOW_LABELS[workflow]} [{number}/{total}]"


def unsupported_tool(node: str, tool_name: str) -> str:
    return f"{node} 노드가 처리하지 않는 도구입니다: {tool_name}"


def no_node_for_tool(tool_name: str) -> str:
    return f"그래프에 실행할 노드가 없는 도구입니다: {tool_name}"


def no_documents(collection: str) -> str:
    return f"{COLLECTION_LABELS[collection]}({collection}) 문서가 하나도 없습니다."


def no_documents_found(topic: str) -> str:
    return f"현행 문서와 보관 문서에서 '{topic}' 주제의 문서를 찾지 못했습니다."


def missing_metadata(key: str) -> str:
    return f"'{key}' 항목이 없습니다."


def invalid_date(key: str, value: str) -> str:
    return f"'{key}'이 YYYY-MM-DD 형식이 아닙니다: {value}"


def missing_end_date(key: str) -> str:
    return f"보관 문서인데 '{key}' 항목이 없습니다."


def history_heading(topic: str, count: int) -> str:
    return f"'{topic}' 관련 문서 {count}건의 이력입니다."


def all_documents_skipped(topic: str, count: int) -> str:
    return f"'{topic}' 관련 문서 {count}건 모두 메타데이터를 읽지 못했습니다."


def skipped_section(entries: list[str]) -> str:
    return "\n".join(["메타데이터를 읽지 못해 제외한 문서", *entries])


def skipped_entry(doc_id: str, reason: str) -> str:
    return f"- {doc_id}: {reason}"


def history_section(number: str, title: str, entries: list[str]) -> str:
    return "\n".join([f"[{number}] {title}", *entries])


def history_entry(
    effective: str, ended: str | None, title: str, doc_id: str, status: str
) -> str:
    return f"- {effective} ~ {ended or '현재'}: {title} ({doc_id}) · {status}"


def documents_to_follow(documents: list[str]) -> str:
    return f"지금 따라야 할 문서: {', '.join(documents)}"


def no_document_in_force(last_document: str, ended: str) -> str:
    return (
        f"지금 유효한 문서가 없습니다. 마지막으로 유효했던 문서는 {last_document}이며 "
        f"{ended}에 효력이 끝났습니다."
    )


def document_label(title: str, doc_id: str) -> str:
    return f"{title} ({doc_id})"


def empty_document(path: Path) -> str:
    return f"빈 문서입니다: {path}"


def not_utf8_document(path: Path) -> str:
    return f"UTF-8로 읽을 수 없는 문서입니다: {path}"


def unreadable_document(path: Path, error: OSError) -> str:
    return f"열 수 없는 문서입니다: {path} ({error.strerror})"


def log_file_unavailable(error: OSError) -> str:
    return f"로그 파일을 열 수 없어 로그 없이 실행합니다: {error}"


def demo_not_started(reason: str) -> str:
    return f"문서를 읽지 못해 시연을 시작할 수 없습니다: {reason}"


def error_guide(node: str, reason: str, attempts: int) -> str:
    return (
        f"{node} 노드가 {attempts}번 시도 끝에 실패해 답변하지 못했습니다. ({reason})"
    )


def date_answer(today: str) -> str:
    year, month, day = today.split("-")
    return f"오늘은 {int(year)}년 {int(month)}월 {int(day)}일입니다."


SEARCH_CURRENT_NOTE = "현행 문서에서 찾아보겠습니다."
SEARCH_ARCHIVE_NOTE = "현행 문서에 없어 보관 문서에서 다시 찾아보겠습니다."
DATE_NOTE = "오늘 날짜를 확인하겠습니다."
