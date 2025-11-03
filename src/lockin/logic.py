from praw import Reddit
from lockin import parse
from lockin.score import Scores


def sync(reddit: Reddit, scores: Scores, subreddits: str) -> None:
    for submission in reddit.subreddit(subreddits).new():
        id = submission.id
        title = submission.title
        comments = submission.num_comments
        score = submission.score
        epoch = submission.created_utc

        for ticker in parse.tickers(title):
            scores[ticker][id] = (comments, score, epoch)
