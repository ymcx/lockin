from collections import defaultdict
from lockin import io, logic
from lockin.logic import Timer
from lockin.parser import TickerParser


def main() -> None:
    amount_to_list, poll_interval, subreddits, reddit = io.read_config()
    scores = defaultdict(defaultdict)
    parser = TickerParser()

    Timer(
        poll_interval, logic.thread, parser, reddit, scores, subreddits, amount_to_list
    )
