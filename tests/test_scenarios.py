import pytest
from langgraph.graph.state import CompiledStateGraph

from mini_workflow.engine import run_graph
from mini_workflow.result import RecordKind, RunStatus
from mini_workflow.scenarios import (
    DEMO_NODE_LIMITS,
    DEMO_SCENARIOS,
    TIMEOUT_QUESTION,
    Workflow,
)
from mini_workflow.search import DocumentSearch
from mini_workflow.workflows.agent.fake_llm import FakeLLM
from mini_workflow.workflows.agent.graph import LLM_RETRY_POLICY, build_agent_graph
from mini_workflow.workflows.agent.nodes import (
    DATE_NODE,
    ERROR_GUIDE_NODE,
    LLM_NODE,
    SEARCH_NODE,
)
from mini_workflow.workflows.document_history.graph import build_document_graph
from mini_workflow.workflows.document_history.nodes import (
    FIND_DOCUMENTS_NODE,
    NO_DOCUMENTS_NODE,
    READ_METADATA_NODE,
    WRITE_REPORT_NODE,
)

ERROR_HANDLING = f"오류 처리:{LLM_NODE}"
SEARCH_TWICE = [LLM_NODE, SEARCH_NODE, LLM_NODE, SEARCH_NODE, LLM_NODE]

# 시나리오 이름: (시연 시나리오의 이름, 예상 경로). 이름은 테스트 결과에 표시된다.
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
    "document_history": (
        "배포",
        [FIND_DOCUMENTS_NODE, *[READ_METADATA_NODE] * 3, WRITE_REPORT_NODE],
    ),
    "no_documents": ("동호회", [FIND_DOCUMENTS_NODE, NO_DOCUMENTS_NODE]),
}


def demo_graphs(search: DocumentSearch) -> dict[Workflow, CompiledStateGraph]:
    llm = FakeLLM(timeout_questions=frozenset({TIMEOUT_QUESTION}))
    no_wait = LLM_RETRY_POLICY._replace(initial_interval=0)
    return {
        Workflow.AGENT: build_agent_graph(llm, search, llm_retry=no_wait),
        Workflow.DOCUMENT_HISTORY: build_document_graph(search),
    }


def test_every_demo_scenario_has_expected_path() -> None:
    assert {scenario.label for scenario in DEMO_SCENARIOS} == {
        label for label, _ in SCENARIOS.values()
    }


@pytest.mark.parametrize("name", SCENARIOS)
def test_demo_scenario_follows_expected_path(name: str, search: DocumentSearch) -> None:
    label, expected_path = SCENARIOS[name]
    [scenario] = [s for s in DEMO_SCENARIOS if s.label == label]
    graph = demo_graphs(search)[scenario.workflow]

    result = run_graph(graph, scenario.initial_state, node_limits=DEMO_NODE_LIMITS)

    path = [
        f"오류 처리:{record.node}"
        if record.kind is RecordKind.ERROR_HANDLER
        else record.node
        for record in result.history
    ]
    assert path == expected_path
    assert result.status is RunStatus.SUCCESS
