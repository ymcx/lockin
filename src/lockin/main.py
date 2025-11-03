from collections import defaultdict
from lockin import io, logic
from lockin.logic import Timer


def main() -> None:
    amount_to_list, poll_interval, subreddits, reddit = io.read_config()
    scores = defaultdict(defaultdict)

    Timer(poll_interval, logic.thread, reddit, scores, subreddits, amount_to_list)
