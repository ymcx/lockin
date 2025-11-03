from praw import Reddit
from lockin import parse, io
from lockin.score import Scores
from threading import Event, Thread
import time


# https://stackoverflow.com/a/33054922
class Timer:
    def __init__(self, interval, function, *args) -> None:
        self.interval = interval
        self.function = function
        self.args = args

        self.start = time.time()
        self.event = Event()

        thread = Thread(target=self._target)
        thread.start()

        self.function(*self.args)

    def _target(self) -> None:
        while not self.event.wait(self._time()):
            self.function(*self.args)

    def _time(self) -> int:
        return self.interval - (time.time() - self.start) % self.interval


def _sync(reddit: Reddit, scores: Scores, subreddits: str) -> None:
    for submission in reddit.subreddit(subreddits).new():
        id = submission.id
        title = submission.title
        comments = submission.num_comments
        score = submission.score
        epoch = submission.created_utc

        for ticker in parse.tickers(title):
            scores[ticker][id] = (comments, score, epoch)


def thread(
    reddit: Reddit, scores: Scores, subreddits: str, amount_to_list: int
) -> None:
    _sync(reddit, scores, subreddits)
    io.list_scores(scores, amount_to_list)
