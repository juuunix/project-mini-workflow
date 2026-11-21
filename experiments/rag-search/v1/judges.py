"""v1 judges: decide found documents by score alone."""

from runner import JudgeInput, Judges, Scored


def any_overlap(given: JudgeInput, threshold: float) -> list[Scored]:
    """Baseline: any document with a positive score is found."""
    return [s for s in given.scored if s.score > 0]


def score_threshold(given: JudgeInput, threshold: float) -> list[Scored]:
    return [s for s in given.scored if s.score >= threshold]


def observed_scores(inputs: list[JudgeInput]) -> list[float]:
    return [s.score for given in inputs for s in given.scored if s.score > 0]


JUDGES: Judges = {
    "any-overlap": (any_overlap, None),
    "score-threshold": (score_threshold, observed_scores),
}
