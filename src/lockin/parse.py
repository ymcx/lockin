def _is_dollar(ticker: str) -> bool:
    return ticker.startswith("$")


def _is_upper(ticker: str) -> bool:
    return ticker.isupper()


def _is_correct_length(ticker: str) -> bool:
    return 1 <= len(ticker) <= 5


def _contains_no_numbers(ticker: str) -> bool:
    return ticker.isalpha()


def tickers(string: str) -> set[str]:
    string = "".join(c for c in string if c == "$" or c == " " or c.isalnum())
    tickers = string.split()

    tickers = [t for t in tickers if _is_dollar(t) or _is_upper(t)]
    tickers = [t.replace("$", "").upper() for t in tickers]

    tickers = [t for t in tickers if _is_correct_length(t)]
    tickers = [t for t in tickers if _contains_no_numbers(t)]

    return set(tickers)
