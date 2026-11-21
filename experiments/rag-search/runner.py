"""Shared runner: run every tokenizer x engine x judge combination over the questions.

Search order follows the architecture: search `current` first, and search
`archive` only when nothing in `current` is judged as found.
Each version folder (v1, v2, ...) passes its own judges and results folder.
"""

import argparse
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from engines import ENGINES
from queries import QUERIES, Collection, Query
from tokenizers import TOKENIZERS, Tokenizer, bigrams

ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT / "data" / "docs"
COLLECTIONS: tuple[Collection, ...] = ("current", "archive")
KINDS = ("A", "B", "C", "D", "E")


@dataclass(frozen=True)
class Scored:
    doc_id: str
    score: float


@dataclass(frozen=True)
class Corpus:
    """What judges may know about all 30 documents, under one tokenizer."""

    doc_tokens: dict[str, frozenset[str]]
    doc_bigrams: dict[str, frozenset[str]]
    title_tokens: dict[str, frozenset[str]]
    doc_freq: dict[str, int]  # Number of documents (of 30) that contain a token.


@dataclass(frozen=True)
class JudgeInput:
    """One query against one collection."""

    scored: list[Scored]
    query_tokens: list[str]
    corpus: Corpus


# A judge keeps the scored documents it accepts as found. A judge registered
# with a sweep function is tried with every threshold that function returns.
Judge = Callable[[JudgeInput, float], list[Scored]]
Sweep = Callable[[list[JudgeInput]], list[float]]
Judges = dict[str, tuple[Judge, Sweep | None]]
Scores = dict[tuple[str, Collection], JudgeInput]


@dataclass(frozen=True)
class Outcome:
    query: Query
    collection: Collection | None
    ranking: list[Scored]

    @property
    def top1(self) -> bool:
        """Correct collection, and the expected document ranks first."""
        if self.collection != self.query.expected_collection:
            return False
        return self.query.expected_doc is None or (
            self.ranking[0].doc_id == self.query.expected_doc
        )

    @property
    def top3(self) -> bool:
        """Correct collection, and the expected document is within the top three."""
        if self.collection != self.query.expected_collection:
            return False
        return self.query.expected_doc is None or any(
            s.doc_id == self.query.expected_doc for s in self.ranking[:3]
        )


def load_docs() -> dict[Collection, dict[str, str]]:
    return {
        collection: {
            path.stem: path.read_text(encoding="utf-8")
            for path in sorted((DOCS_DIR / collection).glob("*.md"))
        }
        for collection in COLLECTIONS
    }


def score_all(
    docs: dict[Collection, dict[str, str]], tokenizer: Tokenizer, engine_name: str
) -> tuple[Scores, float]:
    """Score every query against both collections. Returns scores and index time."""
    started = time.perf_counter()
    engines = {}
    for collection, texts in docs.items():
        engines[collection] = ENGINES[engine_name](
            [tokenizer(text) for text in texts.values()]
        )
    index_seconds = time.perf_counter() - started

    corpus = build_corpus(docs, tokenizer)
    scores: Scores = {}
    for query in QUERIES:
        tokens = tokenizer(query.text)
        for collection, engine in engines.items():
            values = engine.scores(tokens)
            scored = [
                Scored(doc_id, value)
                for doc_id, value in zip(docs[collection], values, strict=True)
            ]
            scores[query.text, collection] = JudgeInput(scored, tokens, corpus)
    return scores, index_seconds


def build_corpus(docs: dict[Collection, dict[str, str]], tokenizer: Tokenizer) -> Corpus:
    texts = {doc_id: text for by_id in docs.values() for doc_id, text in by_id.items()}
    doc_tokens = {doc_id: frozenset(tokenizer(text)) for doc_id, text in texts.items()}
    doc_freq: dict[str, int] = {}
    for tokens in doc_tokens.values():
        for token in tokens:
            doc_freq[token] = doc_freq.get(token, 0) + 1
    return Corpus(
        doc_tokens=doc_tokens,
        doc_bigrams={doc_id: frozenset(bigrams(text)) for doc_id, text in texts.items()},
        title_tokens={
            doc_id: frozenset(tokenizer(text.splitlines()[0].lstrip("# ")))
            for doc_id, text in texts.items()
        },
        doc_freq=doc_freq,
    )


def search(query: Query, scores: Scores, judge: Judge, threshold: float) -> Outcome:
    for collection in COLLECTIONS:
        found = [s for s in judge(scores[query.text, collection], threshold) if s.score > 0]
        if found:
            ranking = sorted(found, key=lambda s: s.score, reverse=True)
            return Outcome(query, collection, ranking)
    return Outcome(query, None, [])


def evaluate(scores: Scores, judge: Judge, threshold: float) -> list[Outcome]:
    return [search(query, scores, judge, threshold) for query in QUERIES]


def best_threshold(
    scores: Scores, judge: Judge, sweep: Sweep
) -> tuple[float, list[Outcome], tuple[float, float]]:
    """Try every threshold from `sweep`. Returns the best one, its outcomes,
    and the range of thresholds that reach the same top-1 count."""
    candidates = sorted(set(sweep(list(scores.values()))))
    results = [(t, evaluate(scores, judge, t)) for t in candidates]
    counts = [sum(o.top1 for o in outcomes) for _, outcomes in results]
    best = max(counts)
    winners = [
        t for (t, _), count in zip(results, counts, strict=True) if count == best
    ]
    middle = winners[len(winners) // 2]
    outcomes = next(o for t, o in results if t == middle)
    return middle, outcomes, (winners[0], winners[-1])


def routes(outcomes: list[Outcome]) -> str:
    """Where searches ended, regardless of rank.

    C·D 보관 도달: archive-only questions whose search reached the archive.
    A·B 현행 놓침: current questions whose search did not end in current
    (it ended in the archive or found nothing).
    """
    archive_kinds = [o for o in outcomes if o.query.kind in ("C", "D")]
    current_kinds = [o for o in outcomes if o.query.kind in ("A", "B")]
    reached = sum(o.collection == "archive" for o in archive_kinds)
    missed = sum(o.collection != "current" for o in current_kinds)
    return f"{reached}/{len(archive_kinds)} | {missed}/{len(current_kinds)}"


def describe(outcome: Outcome) -> str:
    if outcome.collection is None:
        return "없음"
    top = ", ".join(f"{s.doc_id} ({s.score:.2f})" for s in outcome.ranking[:3])
    return f"{outcome.collection}: {top}"


def write_detail(results_dir: Path, name: str, outcomes: list[Outcome]) -> None:
    lines = [
        f"# {name}",
        "",
        "| # | 유형 | 말투 | 질문 | 정답 | Hit@1 | Hit@3 | 결과 (상위 3건) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for o in outcomes:
        q = o.query
        expected = (
            f"{q.expected_collection}: {q.expected_doc}" if q.expected_doc else "없음"
        )
        lines.append(
            f"| {q.topic} | {q.kind} | {q.style} | {q.text} | {expected} | "
            f"{'O' if o.top1 else 'X'} | {'O' if o.top3 else 'X'} | {describe(o)} |"
        )
    details = results_dir / "details"
    details.mkdir(parents=True, exist_ok=True)
    (details / f"{name}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(judges: Judges, results_dir: Path) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", choices=TOKENIZERS)
    parser.add_argument("--engine", choices=ENGINES)
    args = parser.parse_args()

    docs = load_docs()
    tokenizers = [args.tokenizer] if args.tokenizer else list(TOKENIZERS)
    engines = [args.engine] if args.engine else list(ENGINES)

    rows = []
    for tokenizer_name in tokenizers:
        tokenizer = TOKENIZERS[tokenizer_name]
        tokenizer("준비")  # Load models such as Kiwi before timing the index.
        for engine_name in engines:
            scores, index_seconds = score_all(docs, tokenizer, engine_name)
            for judge_name, (judge, sweep) in judges.items():
                name = f"{tokenizer_name}__{engine_name}__{judge_name}"
                if sweep:
                    threshold, outcomes, (low, high) = best_threshold(
                        scores, judge, sweep
                    )
                    threshold_text = f"{threshold:.2f} ({low:.2f}~{high:.2f})"
                else:
                    outcomes = evaluate(scores, judge, 0.0)
                    threshold_text = "-"
                write_detail(results_dir, name, outcomes)
                by_kind = " / ".join(
                    f"{sum(o.top1 for o in outcomes if o.query.kind == k)}"
                    f"/{sum(o.query.kind == k for o in outcomes)}"
                    for k in KINDS
                )
                rows.append(
                    f"| {tokenizer_name} | {engine_name} | {judge_name} | "
                    f"{threshold_text} | "
                    f"{sum(o.top1 for o in outcomes)}/{len(outcomes)} | "
                    f"{sum(o.top3 for o in outcomes)}/{len(outcomes)} | "
                    f"{routes(outcomes)} | {by_kind} | "
                    f"{index_seconds:.3f} |"
                )

    summary = [
        "# 결과 요약",
        "",
        "| 토크나이저 | 엔진 | 판정 | 기준값 (같은 결과 범위) | Hit@1 | Hit@3 "
        "| C·D 보관 도달 | A·B 현행 놓침 "
        "| 유형별 Hit@1 (A / B / C / D / E) | 색인(초) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        *rows,
    ]
    results_dir.mkdir(parents=True, exist_ok=True)
    text = "\n".join(summary) + "\n"
    (results_dir / "summary.md").write_text(text, encoding="utf-8")
    print(text)
