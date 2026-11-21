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
