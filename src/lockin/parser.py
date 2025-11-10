from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline


class TickerParser:
    def __init__(
        self: TickerParser, checkpoint: str = "Jean-Baptiste/roberta-ticker"
    ) -> None:
        model = AutoModelForTokenClassification.from_pretrained(checkpoint)
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        self.nlp = pipeline(
            "ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple"
        )

    def __call__(self: TickerParser, string: str) -> set[str]:
        tickers = {ticker["word"] for ticker in self.nlp(string)}

        tickers = {ticker.replace("$", "") for ticker in tickers}
        tickers = {ticker.strip() for ticker in tickers}
        tickers = {ticker.upper() for ticker in tickers}

        tickers = {ticker for ticker in tickers if ticker.isalpha()}
        tickers = {ticker for ticker in tickers if 0 < len(ticker) < 6}

        return tickers
