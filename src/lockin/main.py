from praw import Reddit
from collections import defaultdict
import os
from lockin import format, parse, graph
import time
import sys

POLL_INTERVAL = 5
AMOUNT_TO_LIST = 20
SUBREDDITS = [
    "DIVIDENDINVESTING",
    "FINANCE",
    "INVESTING",
    "OPTIONS",
    "PENNYSTOCKS",
    "ROBINHOOD",
    "STOCKMARKET",
    "STOCKS",
    "TRADING",
    "VALUEINVESTING",
    "WALLSTREETBETS",
]


def read_credentials(path: str) -> dict[str, str]:
    file = open(path)
    credentials = [line.strip().split("=") for line in file]
    file.close()

    return dict(credentials)


def get_reddit(credentials: dict[str, str]) -> Reddit:
    return Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        password=credentials["password"],
        username=credentials["username"],
        user_agent="Mozarella Firecat",
    )


def read_arguments() -> tuple[str, bool]:
    match len(sys.argv):
        case 1:
            print("Please pass the credentials.txt file")
            sys.exit()
        case 2:
            print("Please specify if you want to print the scores or show the graph")
            sys.exit()
        case _:
            if sys.argv[2] != "graph" and sys.argv[2] != "text":
                print("Invalid mode given, please select either 'graph' or 'text'")
                sys.exit()

    return sys.argv[1], sys.argv[2] == "graph"


def main() -> None:
    arguments = read_arguments()
    credentials = read_credentials(arguments[0])
    create_graph = arguments[1]

    reddit = get_reddit(credentials)
    scores = defaultdict(defaultdict)
    subreddits = "+".join(SUBREDDITS)
    iteration = 0

    if create_graph:
        figure, axes, lines = graph.create()

    while True:
        submissions = reddit.subreddit(subreddits).new()
        parse.scores(scores, submissions)

        if create_graph:
            scores_data = format.scores_data(scores, AMOUNT_TO_LIST)
            graph.update(iteration, scores_data, figure, axes, lines)
        else:
            scores_str = format.scores_str(scores, AMOUNT_TO_LIST)
            os.system("clear")
            print(scores_str)

        iteration += 1
        time.sleep(60 * POLL_INTERVAL)


if __name__ == "__main__":
    main()
