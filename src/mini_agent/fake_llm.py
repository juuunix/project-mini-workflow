from typing import cast

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from mini_agent import messages
from mini_agent.nodes import DATE_TOOL_NAME
from mini_agent.search import SEARCH_TOOL_NAME, Collection, SearchArtifact

SEARCH_KEYWORDS = ("검색해줘", "찾아줘")
DATE_KEYWORDS = ("날짜",)


class FakeLLM(BaseChatModel):
    """메시지 목록의 상태만 보고 정해진 규칙대로 응답하는 가짜 채팅 모델.

    판단은 마지막 메시지로 한다. 마지막이 도구 결과면 그 결과로, 아니면 첫 질문으로
    응답을 정한다. timeout_questions에 든 질문은 도구 결과를 받아 답할 때마다
    TimeoutError를 던진다.
    """

    timeout_questions: frozenset[str] = frozenset()

    @property
    def _llm_type(self) -> str:
        return "fake"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: object,
    ) -> ChatResult:
        return ChatResult(generations=[ChatGeneration(message=self._respond(messages))])

    def _respond(self, history: list[BaseMessage]) -> AIMessage:
        question = first_question(history)
        last = history[-1]

        if not isinstance(last, ToolMessage):
            if any(keyword in question for keyword in DATE_KEYWORDS):
                return tool_request(DATE_TOOL_NAME, {}, history)
            if any(keyword in question for keyword in SEARCH_KEYWORDS):
                return search_request(question, Collection.CURRENT, history)
            return AIMessage(messages.DIRECT_ANSWER)

        if question in self.timeout_questions:
            raise TimeoutError(messages.llm_timeout(question))
        tool_name = requested_tool(history, last.tool_call_id)
        if last.status == "error":
            return AIMessage(messages.tool_failed_answer(tool_name, last.text))
        # 도구가 늘면 그 도구의 결과를 읽는 갈래를 여기에 더한다.
        if tool_name == SEARCH_TOOL_NAME:
            return answer_search_result(question, last, history)
        if tool_name == DATE_TOOL_NAME:
            return AIMessage(messages.date_answer(last.artifact["date"]))
        raise ValueError(messages.unknown_tool(tool_name))


def answer_search_result(
    question: str, result: ToolMessage, history: list[BaseMessage]
) -> AIMessage:
    artifact = cast(SearchArtifact, result.artifact)
    titles = [doc["title"] for doc in artifact["documents"]]
    in_archive = artifact["collection"] == Collection.ARCHIVE
    if titles:
        answer = messages.found_answer(titles)
        if in_archive:
            answer = f"{answer}\n{messages.ARCHIVE_NOTICE}"
        return AIMessage(answer)
    if not in_archive:
        return search_request(question, Collection.ARCHIVE, history)
    return AIMessage(messages.NOT_FOUND_ANSWER)


def first_question(history: list[BaseMessage]) -> str:
    return next(m.text for m in history if isinstance(m, HumanMessage))


def requested_tool(history: list[BaseMessage], tool_call_id: str) -> str:
    """도구 결과가 답하는 요청을 tool_call_id로 찾아 그 도구 이름을 돌려준다."""
    for message in reversed(history):
        if isinstance(message, AIMessage):
            for call in message.tool_calls:
                if call["id"] == tool_call_id:
                    return call["name"]
    raise ValueError(messages.unmatched_tool_result(tool_call_id))


def search_request(
    question: str, collection: Collection, history: list[BaseMessage]
) -> AIMessage:
    args = {"query": question, "collection": collection}
    return tool_request(SEARCH_TOOL_NAME, args, history)


def tool_request(
    tool_name: str, args: dict[str, object], history: list[BaseMessage]
) -> AIMessage:
    # 같은 메시지 목록에는 같은 응답을 내도록, 호출 ID를 지금까지의 LLM 응답 수로 정한다.
    call_number = sum(isinstance(m, AIMessage) for m in history) + 1
    return AIMessage(
        content="",
        tool_calls=[{"name": tool_name, "args": args, "id": f"call_{call_number}"}],
    )
