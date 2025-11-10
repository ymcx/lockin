# LOCKIN

A tool that scrapes investing subreddits, extracts mentioned stock tickers, and visualizes their popularity over time based on frequency and recency.

# Usage

First, you'll need to fill config.toml with your Reddit account's username and password (please don't use your main account).

Next, navigate to https://www.reddit.com/prefs/apps to create a new application for PRAW to interact with the Reddit API. Select "script", fill the required fields, hit "create app", and finally fill both client_id and client_secret according to the values listed on the site.

Start the program by typing:

```
uv run lockin
```
