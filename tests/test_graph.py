import pytest
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END

from mini_agent.engine import run_graph
from mini_agent.fake_llm import FakeLLM
from mini_agent.graph import LLM_RETRY_POLICY, build_graph, route_after_llm
from mini_agent.nodes import (
    DATE_NODE,
    DATE_TOOL_NAME,
    ERROR_GUIDE_NODE,
    LLM_NODE,
    SEARCH_NODE,
    AgentState,
)
from mini_agent.report import result_text, table_rows
from mini_agent.result import RecordKind, RunStatus
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


def test_table_rows_show_moves_and_counts(search: DocumentSearch) -> None:
    graph = build_graph(FakeLLM(), search)
    result = run_graph(graph, {"messages": [HumanMessage(LEAVE_QUESTION)]})

    rows = table_rows(result)

    assert [row[:5] for row in rows] == [
        ("1", "START → llm", "성공", LLM_NODE, "1번째"),
        ("2", f"{LLM_NODE} → {SEARCH_NODE}", "성공", SEARCH_NODE, "1번째"),
        ("3", f"{SEARCH_NODE} → {LLM_NODE}", "성공", LLM_NODE, "2번째"),
        ("4", f"{LLM_NODE} → END", "종료", "", ""),
    ]


def test_table_rows_show_failure_and_handling(search: DocumentSearch) -> None:
    llm = FakeLLM(timeout_questions=frozenset({LEAVE_QUESTION}))
    no_wait = LLM_RETRY_POLICY._replace(initial_interval=0)
    graph = build_graph(llm, search, llm_retry=no_wait)
    result = run_graph(graph, {"messages": [HumanMessage(LEAVE_QUESTION)]})

    rows = table_rows(result)

    assert [row[:5] for row in rows] == [
        ("1", "START → llm", "성공", LLM_NODE, "1번째"),
        ("2", f"{LLM_NODE} → {SEARCH_NODE}", "성공", SEARCH_NODE, "1번째"),
        ("3", f"{SEARCH_NODE} → {LLM_NODE}", "실패", LLM_NODE, "2번째"),
        ("4", f"{LLM_NODE} → 오류 처리", "오류 처리", LLM_NODE, ""),
        ("5", f"오류 처리 → {ERROR_GUIDE_NODE}", "성공", ERROR_GUIDE_NODE, "1번째"),
        ("6", f"{ERROR_GUIDE_NODE} → END", "종료", "", ""),
    ]
    assert rows[2][5].startswith("TimeoutError")
    assert "attempts: 3" in rows[3][5]
    assert result_text(result) == (
        "성공 (오류 처리 1건) · llm 2회, search 1회, error_guide 1회"
    )


def test_result_text_has_no_error_note_without_failures(
    search: DocumentSearch,
) -> None:
    graph = build_graph(FakeLLM(), search)
    result = run_graph(graph, {"messages": [HumanMessage(LEAVE_QUESTION)]})

    assert result_text(result) == "성공 · llm 2회, search 1회"


def test_llm_timeout_is_retried_then_guided(search: DocumentSearch) -> None:
    llm = FakeLLM(timeout_questions=frozenset({LEAVE_QUESTION}))
    no_wait = LLM_RETRY_POLICY._replace(initial_interval=0)
    graph = build_graph(llm, search, llm_retry=no_wait)

    result = run_graph(graph, {"messages": [HumanMessage(LEAVE_QUESTION)]})

    assert [(record.kind, record.node) for record in result.history] == [
        (RecordKind.NODE, LLM_NODE),
        (RecordKind.NODE, SEARCH_NODE),
        (RecordKind.NODE, LLM_NODE),
        (RecordKind.ERROR_HANDLER, LLM_NODE),
        (RecordKind.NODE, ERROR_GUIDE_NODE),
    ]
    assert not result.history[2].succeeded
    assert result.status is RunStatus.SUCCESS
    assert result.state["failure"]["attempts"] == LLM_RETRY_POLICY.max_attempts


def test_llm_retry_policy_matches_architecture() -> None:
    assert LLM_RETRY_POLICY.max_attempts == 3
    assert LLM_RETRY_POLICY.initial_interval == 1.0
    assert LLM_RETRY_POLICY.backoff_factor == 2.0
    assert LLM_RETRY_POLICY.retry_on == (TimeoutError, ConnectionError)


ROUTES = {SEARCH_TOOL_NAME: SEARCH_NODE, DATE_TOOL_NAME: DATE_NODE}


def tool_request(tool_name: str) -> AIMessage:
    return AIMessage(
        content="", tool_calls=[{"name": tool_name, "args": {}, "id": "call_1"}]
    )


def test_route_sends_search_request_to_search_node() -> None:
    state: AgentState = {"messages": [tool_request(SEARCH_TOOL_NAME)]}

    assert route_after_llm(state, ROUTES) == SEARCH_NODE


def test_route_sends_date_request_to_date_node() -> None:
    state: AgentState = {"messages": [tool_request(DATE_TOOL_NAME)]}

    assert route_after_llm(state, ROUTES) == DATE_NODE


def test_route_ends_when_llm_answers_in_text() -> None:
    state: AgentState = {"messages": [AIMessage("안녕하세요")]}

    assert route_after_llm(state, ROUTES) == END


def test_route_rejects_tool_without_node() -> None:
    state: AgentState = {"messages": [tool_request("send_email")]}

    with pytest.raises(ValueError, match="send_email"):
        route_after_llm(state, ROUTES)
