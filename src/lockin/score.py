from operator import itemgetter
from collections import defaultdict
from itertools import islice
import time
import math

Submission = tuple[int, int, float]
Submissions = dict[int, Submission]
Scores = dict[str, Submissions]


def _take(input: dict[str, float], n: int) -> dict[str, float]:
    return dict(islice(input.items(), n))


def _sum(scores: Scores) -> dict[str, float]:
    scores_summed = defaultdict(float)

    for ticker, submissions in scores.items():
        for _, submission in submissions.items():
            comments, score, epoch = submission
            scores_summed[ticker] += _calculate(comments, score, epoch)

    return scores_summed


def _sort(scores: dict[str, float]) -> dict[str, float]:
    scores_sorted = sorted(scores.items(), key=itemgetter(1), reverse=True)

    return dict(scores_sorted)


def _join(scores: dict[str, float]) -> str:
    scores_formatted = []

    for ticker, score in scores.items():
        line = f"{ticker:<5} {score:>4.0f}"
        scores_formatted.append(line)

    return "\n".join(scores_formatted)


def _calculate(comments: int, score: int, epoch: float) -> float:
    epoch_current = time.time()
    epoch_diff = epoch_current - epoch

    # Exponential decay
    # Multiplier is 1.0 at 0 hours, 0.5 at ~4 hours
    k = 0.00005
    multiplier = math.exp(-k * epoch_diff)

    return multiplier * (comments + score)


def format(scores: Scores, n: int) -> str:
    scores_summed = _sum(scores)
    scores_sorted = _sort(scores_summed)

    if n > 0:
        scores_sorted = _take(scores_sorted, n)

    return _join(scores_sorted)
