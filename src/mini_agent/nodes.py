from typing import NotRequired, TypedDict

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, ToolCall, ToolMessage
from langgraph.errors import NodeError
from langgraph.graph import MessagesState
from langgraph.runtime import Runtime
from langgraph.types import Command

from mini_agent import messages
from mini_agent.engine import describe_error
from mini_agent.search import (
    SEARCH_TOOL_NAME,
    Collection,
    DocumentSearch,
    SearchArtifact,
)

LLM_NODE = "llm"
SEARCH_NODE = "search"
ERROR_GUIDE_NODE = "error_guide"

type MessagesUpdate = dict[str, list[BaseMessage]]


# 실패한 노드가 상태에 쓴 값은 버려지므로, 시도 횟수는 예외의 속성으로 오류 처리기에 전한다.
ATTEMPT_ATTRIBUTE = "node_attempt"


class Failure(TypedDict):
    node: str
    reason: str
    attempts: int


class AgentState(MessagesState):
    failure: NotRequired[Failure]


class LLMNode:
    def __init__(self, model: BaseChatModel) -> None:
        self._model = model

    def __call__(self, state: AgentState, runtime: Runtime) -> MessagesUpdate:
        try:
            response = self._model.invoke(state["messages"])
        except Exception as error:
            info = runtime.execution_info
            record_attempt(error, info.node_attempt if info else 1)
            raise
        return {"messages": [response]}


class RagSearchNode:
    """LLM의 검색 요청마다 문서를 찾아 검색 결과 메시지로 돌려준다.

    요청의 인자가 잘못되면(처리하지 않는 도구, 없는 묶음) 예외를 던지고, 검색 노드의
    오류 처리기가 그 실패를 결과 메시지로 바꿔 LLM에게 돌려준다.
    """

    def __init__(self, search: DocumentSearch) -> None:
        self._search = search

    def __call__(self, state: AgentState) -> MessagesUpdate:
        return {"messages": [self._run(call) for call in tool_calls_of(state)]}

    def _run(self, call: ToolCall) -> ToolMessage:
        if call["name"] != SEARCH_TOOL_NAME:
            raise ValueError(messages.unsupported_tool(SEARCH_NODE, call["name"]))
        collection = Collection(call["args"]["collection"])
        hits = self._search.search(call["args"]["query"], collection)
        artifact: SearchArtifact = {
            "collection": collection,
            "documents": [
                {"doc_id": hit.document.doc_id, "title": hit.document.title}
                for hit in hits
            ],
        }
        titles = [hit.document.title for hit in hits]
        return ToolMessage(
            content=messages.search_result_text(collection, titles),
            tool_call_id=call["id"],
            artifact=artifact,
        )


def error_guide(state: AgentState) -> MessagesUpdate:
    failure = state["failure"]
    guide = messages.error_guide(
        failure["node"], failure["reason"], failure["attempts"]
    )
    return {"messages": [AIMessage(guide)]}


def search_error_handler(state: AgentState, error: NodeError) -> Command:
    """검색 요청마다 실패 결과를 돌려준다. 도구 호출 요청에는 결과가 짝으로 있어야 한다."""
    reason = describe_error(error.error)
    failures = [
        ToolMessage(content=reason, tool_call_id=call["id"], status="error")
        for call in tool_calls_of(state)
    ]
    return Command(update={"messages": failures}, goto=LLM_NODE)


def llm_error_handler(state: AgentState, error: NodeError) -> Command:
    failure: Failure = {
        "node": error.node,
        "reason": describe_error(error.error),
        "attempts": attempts_of(error.error),
    }
    return Command(update={"failure": failure}, goto=ERROR_GUIDE_NODE)


def record_attempt(error: BaseException, attempt: int) -> None:
    setattr(error, ATTEMPT_ATTRIBUTE, attempt)


def attempts_of(error: BaseException) -> int:
    return getattr(error, ATTEMPT_ATTRIBUTE, 1)


def tool_calls_of(state: AgentState) -> list[ToolCall]:
    last = state["messages"][-1]
    if not isinstance(last, AIMessage):
        return []
    return last.tool_calls
