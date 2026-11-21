from mini_agent.nodes import LLM_NODE, SEARCH_NODE

# 가짜 LLM이 답변을 만들 때마다 시간 초과로 실패하는 질문. 현행 문서에서 찾아지는 질문이라
# 검색까지는 정상으로 가고, 답변 단계에서 실패해 오류 안내로 간다.
TIMEOUT_QUESTION = "재택근무 운영 지침 찾아줘"

DEMO_QUESTIONS = [
    "오늘 날짜 알려줘",
    "연차휴가 이월은 최대 며칠까지 가능한지 찾아줘",
    "웰니스 포인트는 어디에 쓸 수 있는지 검색해줘",
    "사내 동호회 가입 방법 찾아줘",
    TIMEOUT_QUESTION,
]

# 정상 절차의 최대 횟수(검색 2번, LLM 3번)보다 크게 잡는다.
DEMO_NODE_LIMITS = {SEARCH_NODE: 4, LLM_NODE: 5}
