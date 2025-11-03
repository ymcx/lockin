from operator import itemgetter
from collections import defaultdict
from itertools import islice
from lockin import calculate
from lockin.types import Scores


def _take(input: dict[str, float], n: int) -> dict[str, float]:
    return dict(islice(input.items(), n))


def _sum(scores: Scores) -> dict[str, float]:
    scores_summed = defaultdict(float)

    for ticker, submissions in scores.items():
        for _, submission in submissions.items():
            comments, score, epoch = submission
            scores_summed[ticker] += calculate.score(comments, score, epoch)

    return scores_summed


def _sort(scores: dict[str, float]) -> dict[str, float]:
    scores_sorted = sorted(scores.items(), key=itemgetter(1), reverse=True)

    return dict(scores_sorted)


def _format(scores: dict[str, float]) -> str:
    scores_formatted = []

    for ticker, score in scores.items():
        line = f"{ticker:<5} {score:>4.0f}"
        scores_formatted.append(line)

    return "\n".join(scores_formatted)


def scores_str(scores: Scores, n: int) -> str:
    scores_summed = _sum(scores)
    scores_sorted = _sort(scores_summed)
    scores_sorted = _take(scores_sorted, n)
    scores_formatted = _format(scores_sorted)

    return scores_formatted


def scores_data(scores: Scores, n: int) -> dict[str, float]:
    scores_summed = _sum(scores)
    scores_sorted = _sort(scores_summed)
    scores_sorted = _take(scores_sorted, n)

    return scores_sorted
