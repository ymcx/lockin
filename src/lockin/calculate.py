import time
import math


def score(comments: int, score: int, epoch: float) -> float:
    epoch_current = time.time()
    epoch_diff = epoch_current - epoch

    # Exponential decay
    # Multiplier is 1.0 at 0 hours, 0.5 at ~4 hours
    k = 0.00005
    multiplier = math.exp(-k * epoch_diff)

    return multiplier * (comments + score)
