from typing import Any
from praw import Reddit
from lockin import score
from lockin.score import Scores
import tomllib
import sys
import os


def _get_reddit(credentials: dict[str, Any]) -> Reddit:
    return Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        password=credentials["password"],
        username=credentials["username"],
        user_agent="Mozarella Firecat",
    )


def _clear_screen() -> None:
    if sys.platform in ("win32", "cygwin"):
        os.system("cls")
    else:
        os.system("clear")


def read_config() -> tuple[int, int, str, Reddit]:
    file = open("config.toml", "rb")
    config = tomllib.load(file)
    file.close()

    settings = config["settings"]
    amount_to_list = settings["amount_to_list"]
    poll_interval = settings["poll_interval"]
    subreddits = "+".join(settings["subreddits"])

    credentials = config["credentials"]
    reddit = _get_reddit(credentials)

    return amount_to_list, poll_interval, subreddits, reddit


def list_scores(scores: Scores, amount_to_list: int) -> None:
    string = score.format(scores, amount_to_list)

    _clear_screen()
    print(string)
