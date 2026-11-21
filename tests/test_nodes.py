from pathlib import Path

import pytest
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from langgraph.errors import NodeError

from mini_agent.fake_llm import FakeLLM
from mini_agent.nodes import (
    ERROR_GUIDE_NODE,
    LLM_NODE,
    SEARCH_NODE,
    AgentState,
    LLMNode,
    RagSearchNode,
    error_guide,
    llm_error_handler,
    search_error_handler,
)
from mini_agent.search import SEARCH_TOOL_NAME, Collection, DocumentSearch, SearchHit

LEAVE_QUESTION = "연차휴가 이월은 최대 며칠까지 가능한지 찾아줘"


def state_with(*messages: AnyMessage) -> AgentState:
    return {"messages": [HumanMessage(LEAVE_QUESTION), *messages]}


def search_request(collection: str, query: str = LEAVE_QUESTION) -> AIMessage:
    return AIMessage(
        content="",
        tool_calls=[
            {
                "name": SEARCH_TOOL_NAME,
                "args": {"query": query, "collection": collection},
                "id": "call_1",
            }
        ],
    )


def only_message(update: dict[str, list[BaseMessage]]) -> BaseMessage:
    assert len(update["messages"]) == 1
    return update["messages"][0]


def run_search_node(search: DocumentSearch, request: AIMessage) -> BaseMessage:
    return only_message(RagSearchNode(search)(state_with(request)))


class BrokenSearch(DocumentSearch):
    def search(self, query: str, collection: Collection) -> list[SearchHit]:
        raise FileNotFoundError("data/docs")


def test_llm_node_appends_model_response() -> None:
    update = LLMNode(FakeLLM())(state_with())

    response = only_message(update)
    assert isinstance(response, AIMessage)
    assert response.tool_calls[0]["args"]["collection"] == Collection.CURRENT


def test_search_node_answers_request_with_found_documents(
    search: DocumentSearch,
) -> None:
    result = run_search_node(search, search_request("current"))

    assert isinstance(result, ToolMessage)
    assert result.tool_call_id == "call_1"
    assert result.artifact["collection"] == Collection.CURRENT
    assert result.artifact["documents"][0]["doc_id"] == "policy-01-leave"
    assert "연차휴가 및 경조휴가 규정" in result.text


def test_search_node_returns_empty_result_when_nothing_found(
    search: DocumentSearch,
) -> None:
    result = run_search_node(search, search_request("current", "웰니스 포인트 찾아줘"))

    assert isinstance(result, ToolMessage)
    assert result.status == "success"
    assert result.artifact["documents"] == []


def test_search_node_fails_on_unknown_collection(search: DocumentSearch) -> None:
    with pytest.raises(ValueError, match="nowhere"):
        run_search_node(search, search_request("nowhere"))


def test_search_failure_raises_out_of_node(docs_dir: Path) -> None:
    broken = BrokenSearch.from_directory(docs_dir)

    with pytest.raises(FileNotFoundError):
        run_search_node(broken, search_request("current"))


def test_search_error_handler_returns_failure_as_tool_result() -> None:
    failure = NodeError(node=SEARCH_NODE, error=FileNotFoundError("data/docs"))

    command = search_error_handler(state_with(search_request("current")), failure)

    assert command.goto == LLM_NODE
    assert isinstance(command.update, dict)
    result = command.update["messages"][0]
    assert isinstance(result, ToolMessage)
    assert result.status == "error"
    assert result.tool_call_id == "call_1"
    assert "FileNotFoundError" in result.text


def test_llm_error_handler_records_failure_and_goes_to_error_guide() -> None:
    failure = NodeError(node=LLM_NODE, error=TimeoutError("LLM 응답 시간 초과"))

    command = llm_error_handler(state_with(), failure)

    assert command.goto == ERROR_GUIDE_NODE
    assert command.update == {
        "failure": {"node": LLM_NODE, "reason": "TimeoutError: LLM 응답 시간 초과"}
    }


def test_error_guide_reports_failed_node_and_reason() -> None:
    state = state_with()
    state["failure"] = {"node": LLM_NODE, "reason": "TimeoutError: 시간 초과"}

    guide = only_message(error_guide(state))

    assert isinstance(guide, AIMessage)
    assert LLM_NODE in guide.text
    assert "TimeoutError: 시간 초과" in guide.text
