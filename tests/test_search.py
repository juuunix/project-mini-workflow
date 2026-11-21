from pathlib import Path

import pytest

from mini_agent.search import Collection, DocumentSearch, tokenize

DOCS_DIR = Path(__file__).parents[1] / "data" / "docs"
LEAVE_QUERY = "연차휴가 이월은 최대 며칠까지 가능한가요?"


@pytest.fixture(scope="module")
def search() -> DocumentSearch:
    return DocumentSearch.from_directory(DOCS_DIR)


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
