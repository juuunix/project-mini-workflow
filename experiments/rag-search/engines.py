"""BM25 engines under comparison.

Every engine receives already tokenized documents and queries, so the tokenizer
is the only thing that decides how Korean text is split.
Scores are returned so that a larger value means a better match.
"""

import sqlite3
from collections.abc import Callable
from typing import Protocol

import bm25s
from rank_bm25 import BM25Okapi


class Engine(Protocol):
    def scores(self, query: list[str]) -> list[float]:
        """Score every document, in the order the documents were given."""
        ...


class RankBM25:
    def __init__(self, docs: list[list[str]]) -> None:
        self._bm25 = BM25Okapi(docs)

    def scores(self, query: list[str]) -> list[float]:
        return [float(score) for score in self._bm25.get_scores(query)]


class BM25S:
    def __init__(self, docs: list[list[str]]) -> None:
        self._count = len(docs)
        self._bm25 = bm25s.BM25()
        self._bm25.index(docs, show_progress=False)

    def scores(self, query: list[str]) -> list[float]:
        if not query:  # bm25s raises IndexError on an empty query.
            return [0.0] * self._count
        return [float(score) for score in self._bm25.get_scores(query)]


class SQLiteFTS5:
    """Stores pre-tokenized text joined by spaces, so FTS5 only splits on spaces."""

    def __init__(self, docs: list[list[str]]) -> None:
        self._count = len(docs)
        self._db = sqlite3.connect(":memory:")
        self._db.execute(
            "CREATE VIRTUAL TABLE docs USING fts5(body, "
            "tokenize = 'unicode61 remove_diacritics 0')"
        )
        self._db.executemany(
            "INSERT INTO docs (rowid, body) VALUES (?, ?)",
            [(i, " ".join(tokens)) for i, tokens in enumerate(docs)],
        )

    def scores(self, query: list[str]) -> list[float]:
        result = [0.0] * self._count
        if not query:
            return result
        match = " OR ".join('"' + token.replace('"', '""') + '"' for token in query)
        rows = self._db.execute(
            "SELECT rowid, bm25(docs) FROM docs WHERE docs MATCH ?", (match,)
        )
        for rowid, score in rows:
            result[rowid] = -score  # FTS5 bm25() is negative; smaller is better.
        return result


ENGINES: dict[str, Callable[[list[list[str]]], Engine]] = {
    "rank-bm25": RankBM25,
    "bm25s": BM25S,
    "sqlite-fts5": SQLiteFTS5,
}
