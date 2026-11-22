from typing import TypedDict

from mini_workflow.search import Collection

SEARCH_TOOL_NAME = "search_documents"
DATE_TOOL_NAME = "get_today"


class SearchArgs(TypedDict):
    query: str
    collection: Collection


class FoundDocument(TypedDict):
    doc_id: str
    title: str
    passage: str


class SearchArtifact(TypedDict):
    """문서 검색 결과 메시지(ToolMessage)의 artifact. LLM에는 보내지 않고 코드만 읽는다."""

    collection: Collection
    documents: list[FoundDocument]


class DateArtifact(TypedDict):
    """날짜 조회 결과 메시지의 artifact. date는 ISO 형식(YYYY-MM-DD)이다."""

    date: str
