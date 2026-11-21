from pathlib import Path

import pytest

from mini_agent.search import Collection, DocumentSearch, best_passage, tokenize

LEAVE_QUERY = "연차휴가 이월은 최대 며칠까지 가능한가요?"
WELLNESS_QUERY = "웰니스 포인트는 어디에 쓸 수 있나요?"


def test_tokenize_splits_words_into_two_character_pieces() -> None:
    assert tokenize("연차휴가 이월은") == ["연차", "차휴", "휴가", "이월", "월은"]


def test_tokenize_keeps_one_character_words_and_lowercases() -> None:
    assert tokenize("API 키, v2") == ["ap", "pi", "키", "v2"]


def test_search_ranks_leave_policy_first_in_current(search: DocumentSearch) -> None:
    hits = search.search(LEAVE_QUERY, Collection.CURRENT)

    assert hits[0].document.doc_id == "policy-01-leave"
    assert hits[0].document.title == "연차휴가 및 경조휴가 규정"


def test_search_looks_only_in_the_given_collection(search: DocumentSearch) -> None:
    hits = search.search(LEAVE_QUERY, Collection.ARCHIVE)

    assert hits
    assert all(hit.document.collection is Collection.ARCHIVE for hit in hits)


def test_rank_returns_every_document_in_the_collection(search: DocumentSearch) -> None:
    hits = search.rank(WELLNESS_QUERY, Collection.CURRENT)

    assert len(hits) == 15
    assert [hit.score for hit in hits] == sorted(
        (hit.score for hit in hits), reverse=True
    )


def test_retired_topic_is_not_found_in_current(search: DocumentSearch) -> None:
    assert search.search(WELLNESS_QUERY, Collection.CURRENT) == []


def test_retired_topic_is_found_in_archive(search: DocumentSearch) -> None:
    hits = search.search(WELLNESS_QUERY, Collection.ARCHIVE)

    assert hits[0].document.doc_id == "policy-14-wellness-points"


def test_search_without_documents_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="current"):
        DocumentSearch.from_directory(tmp_path)


def test_best_passage_picks_line_sharing_most_query_tokens() -> None:
    text = "# 연차휴가 규정\n\n- 연차휴가는 15일이다.\n1. 남은 연차휴가는 최대 5일까지 이월할 수 있다.\n"

    assert best_passage(text, "연차휴가 이월은 최대 며칠") == (
        "남은 연차휴가는 최대 5일까지 이월할 수 있다."
    )


def test_best_passage_answers_leave_question_from_real_document(
    search: DocumentSearch,
) -> None:
    hit = search.search(LEAVE_QUERY, Collection.CURRENT)[0]

    assert "최대 5일" in best_passage(hit.document.text, LEAVE_QUERY)
