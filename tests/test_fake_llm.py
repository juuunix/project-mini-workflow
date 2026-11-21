import pytest
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage

from mini_agent import messages
from mini_agent.fake_llm import FakeLLM
from mini_agent.search import SEARCH_TOOL_NAME, Collection, SearchArtifact

LEAVE_QUESTION = "연차휴가 이월은 최대 며칠까지 가능한지 찾아줘"


def search_request(collection: Collection, call_id: str = "call_1") -> AIMessage:
    return AIMessage(
        content="",
        tool_calls=[
            {
                "name": SEARCH_TOOL_NAME,
                "args": {"query": LEAVE_QUESTION, "collection": collection},
                "id": call_id,
            }
        ],
    )


def search_result(
    collection: Collection, titles: list[str], call_id: str = "call_1"
) -> ToolMessage:
    artifact: SearchArtifact = {
        "collection": collection,
        "documents": [
            {"doc_id": f"doc-{i}", "title": title} for i, title in enumerate(titles)
        ],
    }
    return ToolMessage(content="", tool_call_id=call_id, artifact=artifact)


def conversation(*rest: BaseMessage) -> list[BaseMessage]:
    return [HumanMessage(LEAVE_QUESTION), *rest]


def requested_collection(response: AIMessage) -> str:
    assert len(response.tool_calls) == 1
    return response.tool_calls[0]["args"]["collection"]


def test_question_with_search_keyword_requests_current_search() -> None:
    response = FakeLLM().invoke([HumanMessage("웰니스 포인트 검색해줘")])

    assert requested_collection(response) == Collection.CURRENT
    assert response.tool_calls[0]["args"]["query"] == "웰니스 포인트 검색해줘"


def test_question_without_search_keyword_is_answered_directly() -> None:
    response = FakeLLM().invoke([HumanMessage("안녕하세요")])

    assert response.tool_calls == []
    assert response.content


def test_documents_found_in_current_are_answered_with_titles() -> None:
    response = FakeLLM().invoke(
        conversation(
            search_request(Collection.CURRENT),
            search_result(Collection.CURRENT, ["연차휴가 및 경조휴가 규정"]),
        )
    )

    assert response.tool_calls == []
    assert "연차휴가 및 경조휴가 규정" in response.text
    assert messages.ARCHIVE_NOTICE not in response.text


def test_documents_found_in_archive_are_answered_with_notice() -> None:
    response = FakeLLM().invoke(
        conversation(
            search_request(Collection.CURRENT),
            search_result(Collection.CURRENT, []),
            search_request(Collection.ARCHIVE, "call_2"),
            search_result(Collection.ARCHIVE, ["웰니스 포인트 운영 규정"], "call_2"),
        )
    )

    assert "웰니스 포인트 운영 규정" in response.text
    assert messages.ARCHIVE_NOTICE in response.text


def test_nothing_found_in_current_requests_archive_search() -> None:
    response = FakeLLM().invoke(
        conversation(
            search_request(Collection.CURRENT),
            search_result(Collection.CURRENT, []),
        )
    )

    assert requested_collection(response) == Collection.ARCHIVE


def test_nothing_found_in_archive_is_answered_as_not_found() -> None:
    response = FakeLLM().invoke(
        conversation(
            search_request(Collection.CURRENT),
            search_result(Collection.CURRENT, []),
            search_request(Collection.ARCHIVE, "call_2"),
            search_result(Collection.ARCHIVE, [], "call_2"),
        )
    )

    assert response.tool_calls == []
    assert response.text == messages.NOT_FOUND_ANSWER


def test_failed_search_is_answered_with_reason_without_searching_again() -> None:
    failure = ToolMessage(
        content="ValueError: index missing", tool_call_id="call_1", status="error"
    )

    response = FakeLLM().invoke(
        conversation(search_request(Collection.CURRENT), failure)
    )

    assert response.tool_calls == []
    assert SEARCH_TOOL_NAME in response.text
    assert "ValueError: index missing" in response.text


def test_result_of_unknown_tool_is_rejected() -> None:
    request = AIMessage(
        content="",
        tool_calls=[{"name": "send_email", "args": {}, "id": "call_1"}],
    )
    result = ToolMessage(content="sent", tool_call_id="call_1")

    with pytest.raises(ValueError, match="send_email"):
        FakeLLM().invoke(conversation(request, result))


def test_timeout_question_fails_when_answering_search_result() -> None:
    llm = FakeLLM(timeout_questions=frozenset({LEAVE_QUESTION}))
    found = conversation(
        search_request(Collection.CURRENT),
        search_result(Collection.CURRENT, ["연차휴가 및 경조휴가 규정"]),
    )

    assert requested_collection(llm.invoke(conversation())) == Collection.CURRENT
    with pytest.raises(TimeoutError):
        llm.invoke(found)


def test_same_messages_always_give_same_response() -> None:
    history = conversation(
        search_request(Collection.CURRENT), search_result(Collection.CURRENT, [])
    )

    first, second = FakeLLM().invoke(history), FakeLLM().invoke(history)

    assert (first.content, first.tool_calls) == (second.content, second.tool_calls)
