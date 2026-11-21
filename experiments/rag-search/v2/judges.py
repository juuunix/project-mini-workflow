"""v2 judges: decide found documents by more than the score.

v1 judges stay as baselines. Every judge returns the documents it accepts;
the runner then drops documents whose score is not positive.
"""

from runner import JudgeInput, Judges, Scored
from tokenizers import bigrams
from v1.judges import JUDGES as V1_JUDGES


def rarest_tokens(given: JudgeInput) -> set[str]:
    """Query tokens that appear in the fewest documents (of all 30).

    Tokens that appear in no document are skipped; otherwise a word such as
    "얼마인가요" would always be the rarest and nothing would be found.
    """
    freq = given.corpus.doc_freq
    known = [token for token in given.query_tokens if freq.get(token, 0) > 0]
    if not known:
        return set()
    lowest = min(freq[token] for token in known)
    return {token for token in known if freq[token] == lowest}


def rare_word(given: JudgeInput, threshold: float) -> list[Scored]:
    """Found if the document contains one of the rarest query tokens."""
    rare = rarest_tokens(given)
    return [s for s in given.scored if rare & given.corpus.doc_tokens[s.doc_id]]


def rare_word_bigrams(given: JudgeInput, threshold: float) -> list[Scored]:
    """Found if the document contains every 2-character piece of a rarest token.

    Pieces match the token inside longer document words: "헤르메스" matches
    "헤르메스는". A particle on the query token stays in its pieces.
    """
    pieces = [set(bigrams(token)) for token in rarest_tokens(given)]
    return [
        s
        for s in given.scored
        if any(p <= given.corpus.doc_bigrams[s.doc_id] for p in pieces if p)
    ]


def title_match(given: JudgeInput, threshold: float) -> list[Scored]:
    """Found if any query token appears in the document title."""
    query = set(given.query_tokens)
    return [s for s in given.scored if query & given.corpus.title_tokens[s.doc_id]]


def _ratio(given: JudgeInput) -> float:
    top = sorted((s.score for s in given.scored if s.score > 0), reverse=True)
    if not top:
        return 0.0
    if len(top) == 1:
        return float("inf")
    return top[0] / top[1]


def score_ratio(given: JudgeInput, threshold: float) -> list[Scored]:
    """Found if the first score is at least `threshold` times the second."""
    if _ratio(given) < threshold:
        return []
    return given.scored


def observed_ratios(inputs: list[JudgeInput]) -> list[float]:
    return [r for r in map(_ratio, inputs) if 0 < r < float("inf")]


JUDGES: Judges = {
    **V1_JUDGES,
    "rare-word": (rare_word, None),
    "rare-word-bigrams": (rare_word_bigrams, None),
    "title-match": (title_match, None),
    "score-ratio": (score_ratio, observed_ratios),
}
