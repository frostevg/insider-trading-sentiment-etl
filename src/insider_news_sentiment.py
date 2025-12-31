import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- Paths and config ---
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data" / "raw" / "insider_trades_sample.csv"
OUT_PATH = BASE_DIR / "data" / "processed" / "insider_with_sentiment.csv"

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news_headlines(ticker: str, trade_date: str) -> list[str]:
    """Get news headlines around the trade date for the given ticker."""
    if not NEWS_API_KEY:
        print("WARNING: NEWS_API_KEY not set, skipping news fetch.")
        return []

    base_url = "https://newsapi.org/v2/everything"

    # 1 day before and after trade date
    dt = datetime.fromisoformat(trade_date)
    from_date = (dt - timedelta(days=1)).date().isoformat()
    to_date = (dt + timedelta(days=1)).date().isoformat()

    params = {
        "q": ticker,
        "from": from_date,
        "to": to_date,
        "sortBy": "relevancy",
        "language": "en",
        "pageSize": 20,
        "apiKey": NEWS_API_KEY,
    }

    try:
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        headlines = [a.get("title", "") for a in articles if a.get("title")]
        return headlines
    except Exception as e:
        print(f"Error fetching news for {ticker} on {trade_date}: {e}")
        return []


def compute_sentiment(headlines: list[str]) -> float:
    """Compute average sentiment score for a list of headlines."""
    if not headlines:
        return 0.0

    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(h)["compound"] for h in headlines]
    return sum(scores) / len(scores)


def label_sentiment(score: float) -> str:
    """Turn numeric sentiment into label."""
    if score >= 0.2:
        return "positive"
    if score <= -0.2:
        return "negative"
    return "neutral"


def main():
    """Read insider trades, fetch news, compute sentiment, save CSV."""
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {RAW_PATH}")

    df = pd.read_csv(RAW_PATH)

    required_cols = {
        "ticker",
        "insider_name",
        "insider_role",
        "trade_date",
        "transaction_type",
        "shares",
        "price",
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    sentiments = []
    labels = []
    news_counts = []

    for _, row in df.iterrows():
        ticker = row["ticker"]
        trade_date = str(row["trade_date"])
        print(f"Processing {ticker} trade on {trade_date}...")

        headlines = fetch_news_headlines(ticker, trade_date)
        score = compute_sentiment(headlines)
        label = label_sentiment(score)

        sentiments.append(score)
        labels.append(label)
        news_counts.append(len(headlines))

    df["news_sentiment_score"] = sentiments
    df["news_sentiment_label"] = labels
    df["news_headlines_count"] = news_counts

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Saved enriched data with sentiment to: {OUT_PATH}")
    print(df[["ticker", "trade_date", "news_sentiment_score", "news_sentiment_label"]])


if __name__ == "__main__":
    main()
