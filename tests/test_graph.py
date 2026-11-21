import pytest
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END

from mini_agent.engine import run_graph
from mini_agent.fake_llm import FakeLLM
from mini_agent.graph import build_graph, route_after_llm
from mini_agent.nodes import LLM_NODE, SEARCH_NODE, AgentState
from mini_agent.report import format_result
from mini_agent.result import RunStatus
from mini_agent.search import SEARCH_TOOL_NAME, DocumentSearch

LEAVE_QUESTION = "연차휴가 이월은 최대 며칠까지 가능한지 찾아줘"


def test_current_document_question_goes_llm_search_llm(search: DocumentSearch) -> None:
    graph = build_graph(FakeLLM(), search)

    result = run_graph(graph, {"messages": [HumanMessage(LEAVE_QUESTION)]})

    assert [record.node for record in result.history] == [
        LLM_NODE,
        SEARCH_NODE,
        LLM_NODE,
    ]
    assert result.status is RunStatus.SUCCESS
    answer = result.state["messages"][-1]
    assert isinstance(answer, AIMessage)
    assert "연차휴가 및 경조휴가 규정" in answer.text


def test_report_shows_each_node_in_order(search: DocumentSearch) -> None:
    graph = build_graph(FakeLLM(), search)
    result = run_graph(graph, {"messages": [HumanMessage(LEAVE_QUESTION)]})

    lines = format_result(result)

    assert lines == [
        f"[성공] {LLM_NODE}",
        f"[성공] {SEARCH_NODE}",
        f"[성공] {LLM_NODE}",
        "결과: 성공",
    ]


def tool_request(tool_name: str) -> AIMessage:
    return AIMessage(
        content="", tool_calls=[{"name": tool_name, "args": {}, "id": "call_1"}]
    )


def test_route_sends_search_request_to_search_node() -> None:
    state: AgentState = {"messages": [tool_request(SEARCH_TOOL_NAME)]}

    assert route_after_llm(state) == SEARCH_NODE


def test_route_ends_when_llm_answers_in_text() -> None:
    state: AgentState = {"messages": [AIMessage("안녕하세요")]}

    assert route_after_llm(state) == END


def test_route_rejects_tool_without_node() -> None:
    state: AgentState = {"messages": [tool_request("send_email")]}

    with pytest.raises(ValueError, match="send_email"):
        route_after_llm(state)
