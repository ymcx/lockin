from typing import Any
from praw import Reddit
from collections import defaultdict
from lockin import format, parse, graph
import os
import time
import tomllib


def read_config() -> dict[str, Any]:
    file = open("config.toml", "rb")
    config = tomllib.load(file)
    file.close()

    return config


def get_reddit(credentials: dict[str, Any]) -> Reddit:
    return Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        password=credentials["password"],
        username=credentials["username"],
        user_agent="Mozarella Firecat",
    )


def main() -> None:
    config = read_config()

    credentials = config["credentials"]
    reddit = get_reddit(credentials)

    settings = config["settings"]
    amount_to_list = settings["amount_to_list"]
    poll_interval = settings["poll_interval"]
    create_graph = settings["create_graph"]
    subreddits = "+".join(settings["subreddits"])

    scores = defaultdict(defaultdict)
    iteration = 0

    if create_graph:
        figure, axes, lines = graph.create()

    while True:
        submissions = reddit.subreddit(subreddits).new()
        parse.scores(scores, submissions)

        if create_graph:
            scores_data = format.scores_data(scores, amount_to_list)
            graph.update(iteration, scores_data, figure, axes, lines)
        else:
            scores_str = format.scores_str(scores, amount_to_list)
            os.system("clear")
            print(scores_str)

        iteration += 1
        time.sleep(60 * poll_interval)
