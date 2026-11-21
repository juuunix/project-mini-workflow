import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TypedDict

from rank_bm25 import BM25Okapi

from mini_agent import messages

WORD_PATTERN = re.compile(r"[0-9A-Za-z가-힣]+")

SEARCH_TOOL_NAME = "search_documents"


class Collection(StrEnum):
    CURRENT = "current"
    ARCHIVE = "archive"


class FoundDocument(TypedDict):
    doc_id: str
    title: str
    passage: str


class SearchArtifact(TypedDict):
    """문서 검색 결과 메시지(ToolMessage)의 artifact. LLM에는 보내지 않고 코드만 읽는다."""

    collection: Collection
    documents: list[FoundDocument]


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    collection: Collection
    text: str


@dataclass(frozen=True)
class SearchHit:
    document: Document
    score: float


def tokenize(text: str) -> list[str]:
    """단어 안에서만 두 글자씩 자른다. 한 글자 단어는 그대로 둔다."""
    tokens: list[str] = []
    for word in WORD_PATTERN.findall(text.lower()):
        if len(word) == 1:
            tokens.append(word)
        else:
            tokens.extend(word[i : i + 2] for i in range(len(word) - 1))
    return tokens


# 줄 앞의 목록 기호(-, *), 제목 기호(#), 인용 기호(>), 번호("1.")를 떼어 낸다.
LINE_MARKER = re.compile(r"^\s*(?:[-*#>]+|\d+\.)\s*")


def best_passage(text: str, query: str) -> str:
    """문서에서 질의의 토큰과 가장 많이 겹치는 줄을 돌려준다. 첫 줄(제목)은 뺀다.

    겹치는 수가 같으면 앞의 줄을 고른다. LLM이 답의 근거로 읽을 본문이다.
    """
    query_tokens = set(tokenize(query))
    lines = [LINE_MARKER.sub("", line).strip() for line in text.splitlines()[1:]]
    candidates = [line for line in lines if line]
    if not candidates:
        return ""
    return max(candidates, key=lambda line: len(query_tokens & set(tokenize(line))))


# 점수 순으로 정렬된 검색 결과에서 관련 문서만 골라낸다. 순서는 바꾸지 않는다.
type Judge = Callable[[list[str], list[SearchHit]], list[SearchHit]]


def title_match(query_tokens: list[str], hits: list[SearchHit]) -> list[SearchHit]:
    """BM25 점수가 0보다 크고, 질의의 토큰이 제목에도 있는 문서만 남긴다."""
    query = set(query_tokens)
    return [
        hit
        for hit in hits
        if hit.score > 0 and query & set(tokenize(hit.document.title))
    ]


class DocumentSearch:
    def __init__(
        self, documents: Sequence[Document], judge: Judge = title_match
    ) -> None:
        self._documents = {
            collection: [doc for doc in documents if doc.collection is collection]
            for collection in Collection
        }
        for collection, docs in self._documents.items():
            if not docs:
                raise ValueError(messages.no_documents(collection))
        self._indexes = {
            collection: BM25Okapi([tokenize(doc.text) for doc in docs])
            for collection, docs in self._documents.items()
        }
        self._judge = judge

    @classmethod
    def from_directory(cls, root: Path) -> "DocumentSearch":
        """root 아래 묶음 이름의 폴더(current, archive)에서 .md 문서를 읽는다."""
        documents = [
            load_document(path, collection)
            for collection in Collection
            for path in sorted((root / collection).glob("*.md"))
        ]
        return cls(documents)

    def rank(self, query: str, collection: Collection) -> list[SearchHit]:
        """묶음의 모든 문서를 BM25 점수 순으로 돌려준다."""
        scores = self._indexes[collection].get_scores(tokenize(query))
        hits = [
            SearchHit(document=doc, score=float(score))
            for doc, score in zip(self._documents[collection], scores, strict=True)
        ]
        return sorted(hits, key=lambda hit: hit.score, reverse=True)

    def search(self, query: str, collection: Collection) -> list[SearchHit]:
        """판정 기준에 맞는 관련 문서만 점수 순으로 돌려준다. 없으면 빈 목록이다."""
        return self._judge(tokenize(query), self.rank(query, collection))


def load_document(path: Path, collection: Collection) -> Document:
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ")
    return Document(doc_id=path.stem, title=title, collection=collection, text=text)
