import logging
from collections.abc import Callable
from datetime import date
from typing import NotRequired, Protocol, TypedDict, cast

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, ToolCall, ToolMessage
from langgraph.errors import NodeError
from langgraph.graph import MessagesState
from langgraph.runtime import Runtime
from langgraph.types import Command

from mini_agent import messages
from mini_agent.log import Event, log_event
from mini_agent.search import Collection, DocumentSearch, best_passage
from mini_agent.tools import (
    DATE_TOOL_NAME,
    SEARCH_TOOL_NAME,
    DateArtifact,
    SearchArgs,
    SearchArtifact,
)

LLM_NODE = "llm"
SEARCH_NODE = "search"
DATE_NODE = "date"
ERROR_GUIDE_NODE = "error_guide"

logger = logging.getLogger(__name__)

type MessagesUpdate = dict[str, list[BaseMessage]]


# 실패한 노드가 상태에 쓴 값은 버려지므로, 시도 횟수는 예외의 속성으로 오류 처리기에 전한다.
ATTEMPT_ATTRIBUTE = "node_attempt"


class Failure(TypedDict):
    node: str
    reason: str
    attempts: int


class AgentState(MessagesState):
    failure: NotRequired[Failure]


class ToolRunner(Protocol):
    """도구 요청을 실행하는 노드의 모양. 마지막 메시지의 도구 요청에 결과 메시지로 답한다."""

    def __call__(self, state: AgentState) -> MessagesUpdate: ...


class LLMNode:
    def __init__(self, model: BaseChatModel) -> None:
        self._model = model

    def __call__(self, state: AgentState, runtime: Runtime) -> MessagesUpdate:
        try:
            response = self._model.invoke(state["messages"])
        except Exception as error:
            info = runtime.execution_info
            attempt = info.node_attempt if info else 1
            record_attempt(error, attempt)
            # 재시도는 노드 안에서 일어나 엔진이 보지 못하므로, 시도마다 여기서 남긴다.
            log_event(
                logger,
                logging.WARNING,
                Event.LLM_ATTEMPT_FAILED,
                attempt=attempt,
                error=messages.error_reason(error),
            )
            raise
        return {"messages": [response]}


class RagSearchNode:
    """LLM의 검색 요청마다 문서를 찾아 검색 결과 메시지로 돌려준다.

    요청의 인자가 잘못되면(처리하지 않는 도구, 없는 컬렉션) 예외를 던지고, 검색 노드의
    오류 처리기가 그 실패를 결과 메시지로 바꿔 LLM에게 돌려준다.
    """

    def __init__(self, search: DocumentSearch) -> None:
        self._search = search

    def __call__(self, state: AgentState) -> MessagesUpdate:
        return {"messages": [self._run(call) for call in tool_calls_of(state)]}

    def _run(self, call: ToolCall) -> ToolMessage:
        if call["name"] != SEARCH_TOOL_NAME:
            raise ValueError(messages.unsupported_tool(SEARCH_NODE, call["name"]))
        args = cast(SearchArgs, call["args"])
        collection = Collection(args["collection"])
        query = args["query"]
        hits = self._search.search(query, collection)
        artifact: SearchArtifact = {
            "collection": collection,
            "documents": [
                {
                    "doc_id": hit.document.doc_id,
                    "title": hit.document.title,
                    "passage": best_passage(hit.document.text, query),
                }
                for hit in hits
            ],
        }
        # 도구는 문장을 만들지 않고 데이터만 돌려준다. 문장으로 답하는 것은 LLM의 일이다.
        # 답의 근거가 될 본문은 가장 관련 있는 문서의 것을 함께 넘긴다.
        documents = artifact["documents"]
        titles = ", ".join(doc["title"] for doc in documents)
        content = f"collection={collection}, count={len(documents)}, titles=[{titles}]"
        if documents:
            content = f'{content}, passage="{documents[0]["passage"]}"'
        return ToolMessage(
            content=content,
            tool_call_id=call["id"],
            artifact=artifact,
        )


class DateNode:
    """LLM의 날짜 요청에 오늘 날짜를 결과 메시지로 돌려준다.

    오늘 날짜는 바깥에서 받은 함수로 얻는다. 테스트는 고정된 날짜를 돌려주는 함수를 넣는다.
    """

    def __init__(self, today: Callable[[], date]) -> None:
        self._today = today

    def __call__(self, state: AgentState) -> MessagesUpdate:
        return {"messages": [self._run(call) for call in tool_calls_of(state)]}

    def _run(self, call: ToolCall) -> ToolMessage:
        if call["name"] != DATE_TOOL_NAME:
            raise ValueError(messages.unsupported_tool(DATE_NODE, call["name"]))
        today = self._today().isoformat()
        artifact: DateArtifact = {"date": today}
        return ToolMessage(content=today, tool_call_id=call["id"], artifact=artifact)


def error_guide(state: AgentState) -> MessagesUpdate:
    failure = state["failure"]
    guide = messages.error_guide(
        failure["node"], failure["reason"], failure["attempts"]
    )
    return {"messages": [AIMessage(guide)]}


def tool_error_handler(state: AgentState, error: NodeError) -> Command:
    """도구 노드가 실패하면 도구 요청마다 실패 결과를 돌려주고 LLM 노드로 보낸다.

    도구 호출 요청에는 결과가 짝으로 있어야 한다. 어느 도구 노드든 같은 처리기를 쓴다.
    """
    reason = messages.error_reason(error.error)
    failures = [
        ToolMessage(content=reason, tool_call_id=call["id"], status="error")
        for call in tool_calls_of(state)
    ]
    return Command(update={"messages": failures}, goto=LLM_NODE)


def llm_error_handler(state: AgentState, error: NodeError) -> Command:
    failure: Failure = {
        "node": error.node,
        "reason": messages.error_reason(error.error),
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
