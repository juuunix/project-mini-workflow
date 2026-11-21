import re
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from rank_bm25 import BM25Okapi

WORD_PATTERN = re.compile(r"[0-9A-Za-z가-힣]+")


class Collection(StrEnum):
    CURRENT = "current"
    ARCHIVE = "archive"


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


class DocumentSearch:
    def __init__(self, documents: Sequence[Document]) -> None:
        self._documents = {
            collection: [doc for doc in documents if doc.collection is collection]
            for collection in Collection
        }
        self._indexes = {
            collection: BM25Okapi([tokenize(doc.text) for doc in docs])
            for collection, docs in self._documents.items()
        }

    @classmethod
    def from_directory(cls, root: Path) -> "DocumentSearch":
        """root 아래 묶음 이름의 폴더(current, archive)에서 .md 문서를 읽는다."""
        documents = [
            load_document(path, collection)
            for collection in Collection
            for path in sorted((root / collection).glob("*.md"))
        ]
        return cls(documents)

    def search(self, query: str, collection: Collection) -> list[SearchHit]:
        scores = self._indexes[collection].get_scores(tokenize(query))
        hits = [
            SearchHit(document=doc, score=float(score))
            for doc, score in zip(self._documents[collection], scores, strict=True)
        ]
        return sorted(hits, key=lambda hit: hit.score, reverse=True)


def load_document(path: Path, collection: Collection) -> Document:
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ")
    return Document(doc_id=path.stem, title=title, collection=collection, text=text)
