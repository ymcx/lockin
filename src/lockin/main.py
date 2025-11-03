from collections import defaultdict
from lockin import logic, io
import time


def main() -> None:
    amount_to_list, poll_interval, subreddits, reddit = io.read_config()
    scores = defaultdict(defaultdict)

    while True:
        logic.sync(reddit, scores, subreddits)
        io.list_scores(scores, amount_to_list)

        time.sleep(60 * poll_interval)
