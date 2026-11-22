import pytest
from langchain_core.messages import HumanMessage

from mini_agent.engine import run_graph
from mini_agent.fake_llm import FakeLLM
from mini_agent.graph import LLM_RETRY_POLICY, build_agent_graph
from mini_agent.nodes import DATE_NODE, ERROR_GUIDE_NODE, LLM_NODE, SEARCH_NODE
from mini_agent.result import RecordKind, RunStatus
from mini_agent.scenarios import (
    DEMO_NODE_LIMITS,
    DEMO_QUESTIONS,
    TIMEOUT_QUESTION,
)
from mini_agent.search import DocumentSearch

ERROR_HANDLING = f"오류 처리:{LLM_NODE}"
SEARCH_TWICE = [LLM_NODE, SEARCH_NODE, LLM_NODE, SEARCH_NODE, LLM_NODE]

# 시나리오 이름: (질문, 예상 경로). 이름은 테스트 결과에 표시된다.
SCENARIOS = {
    "greeting": ("안녕하세요", [LLM_NODE]),
    "today": ("오늘 날짜 알려줘", [LLM_NODE, DATE_NODE, LLM_NODE]),
    "current": (
        "연차휴가 이월은 최대 며칠까지 가능한지 찾아줘",
        [LLM_NODE, SEARCH_NODE, LLM_NODE],
    ),
    "archive": ("웰니스 포인트는 언제 폐지됐는지 찾아줘", SEARCH_TWICE),
    "not_found": ("사내 동호회 가입 방법 찾아줘", SEARCH_TWICE),
    "llm_timeout": (
        TIMEOUT_QUESTION,
        [LLM_NODE, SEARCH_NODE, LLM_NODE, ERROR_HANDLING, ERROR_GUIDE_NODE],
    ),
}


def test_every_demo_question_has_scenario() -> None:
    assert set(DEMO_QUESTIONS) == {question for question, _ in SCENARIOS.values()}


@pytest.mark.parametrize("name", SCENARIOS)
def test_demo_question_follows_expected_path(name: str, search: DocumentSearch) -> None:
    question, expected_path = SCENARIOS[name]
    llm = FakeLLM(timeout_questions=frozenset({TIMEOUT_QUESTION}))
    no_wait = LLM_RETRY_POLICY._replace(initial_interval=0)
    graph = build_agent_graph(llm, search, llm_retry=no_wait)

    result = run_graph(
        graph, {"messages": [HumanMessage(question)]}, node_limits=DEMO_NODE_LIMITS
    )

    path = [
        f"오류 처리:{record.node}"
        if record.kind is RecordKind.ERROR_HANDLER
        else record.node
        for record in result.history
    ]
    assert path == expected_path
    assert result.status is RunStatus.SUCCESS
