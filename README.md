This project collects insider trading data from a public API, retrieves company news headlines, performs sentiment analysis using VADER, and outputs a combined dataset showing insider buy activity alongside sentiment scores. The pipeline is written in Python and uses Pandas, Requests, and NLTK for data processing. Environment variables are managed with python-dotenv, and results are stored locally as CSV for future analysis, reporting, or dashboard development. This repository demonstrates API integration, ETL design, and basic NLP sentiment processing.

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
