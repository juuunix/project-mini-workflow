def step_limit_detail(limit: int) -> str:
    return f"상한 {limit}단계"


def node_limit_detail(limit: int) -> str:
    return f"상한 {limit}회"


DIRECT_ANSWER = (
    "안녕하세요. 문서를 찾으려면 질문 끝에 '찾아줘'나 '검색해줘'를 붙여 주세요."
)
ARCHIVE_NOTICE = "보관 처리된 문서에서 찾은 내용이라 현재와 다를 수 있습니다."
NOT_FOUND_ANSWER = "현행 문서와 보관 문서에서 관련 문서를 찾지 못했습니다."


def found_answer(titles: list[str]) -> str:
    return f"관련 문서를 찾았습니다: {', '.join(titles)}"


def tool_failed_answer(tool_name: str, reason: str) -> str:
    return f"도구 {tool_name} 실행에 실패해 답변하지 못했습니다. ({reason})"


def unknown_tool(tool_name: str) -> str:
    return f"FakeLLM이 결과를 읽는 규칙이 없는 도구입니다: {tool_name}"


def unmatched_tool_result(tool_call_id: str) -> str:
    return f"도구 결과에 해당하는 요청이 없습니다: {tool_call_id}"


def llm_timeout(question: str) -> str:
    return f"LLM 응답 시간 초과: {question}"


COLLECTION_LABELS = {"current": "현행", "archive": "보관"}


def search_result_text(collection: str, titles: list[str]) -> str:
    label = COLLECTION_LABELS[collection]
    if not titles:
        return f"{label} 문서에서 관련 문서를 찾지 못했습니다."
    return f"{label} 문서에서 {len(titles)}건을 찾았습니다: {', '.join(titles)}"


def unsupported_tool(node: str, tool_name: str) -> str:
    return f"{node} 노드가 처리하지 않는 도구입니다: {tool_name}"


def no_node_for_tool(tool_name: str) -> str:
    return f"그래프에 실행할 노드가 없는 도구입니다: {tool_name}"


def no_documents(collection: str) -> str:
    return f"{COLLECTION_LABELS[collection]}({collection}) 문서가 하나도 없습니다."


def error_guide(node: str, reason: str) -> str:
    return f"{node} 노드가 실패해 답변하지 못했습니다. ({reason})"


ERROR_HANDLER_LABEL = "오류 처리"


def record_label(succeeded: bool) -> str:
    return "성공" if succeeded else "실패"


def result_line(status: str) -> str:
    return f"결과: {'성공' if status == 'success' else '실패'}"
