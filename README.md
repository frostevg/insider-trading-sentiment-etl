# Insider Trading News Sentiment ETL

This project combines **insider trading activity** with **news sentiment analysis** to assess the context around insider stock purchases.

Given a file of insider trades, the pipeline:
1. Reads insider trade records (ticker, insider, date, transaction details)
2. Fetches news headlines around the trade date for each ticker (via NewsAPI.org)
3. Calculates a sentiment score for the headlines (using VADER sentiment analysis)
4. Outputs an enriched dataset with sentiment score and label (positive / neutral / negative)

This is a portfolio project to demonstrate real-world **data engineering + analytics** skills:
- API integration
- ETL with Python and pandas
- Text sentiment analysis
- Config management with `.env`
- Clean project & GitHub structure

---

## Project Structure

```text
insider_news_sentiment/
├── src/
│   └── insider_news_sentiment.py   # Main ETL script: insider trades + news + sentiment
├── data/
│   ├── raw/                        # Input CSV with insider trades (ignored in git)
│   └── processed/                  # Output CSV with sentiment (ignored in git)
├── .env                            # Stores NEWS_API_KEY (not committed)
├── .gitignore
├── requirements.txt
└── README.md
