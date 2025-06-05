from src.summarizer import get_daily_summary
from src.fetcher import RSS_FEEDS, fetch_articles
from src.classifier import categorize_article
import json
import os

def main():
    USE_CACHE = True

    all_articles = []

    if USE_CACHE and os.path.exists("cached_articles.json"):
        with open("cached_articles.json", "r", encoding="utf-8") as f:
            all_articles = json.load(f)
    else:
        for feed in RSS_FEEDS:
            all_articles.extend(fetch_articles(feed))
        #TODO: Might want to drop the 'other' threshold next time, and maybe no entertainment category
        all_articles = [categorize_article(article) for article in all_articles]
        with open("cached_articles.json", "w", encoding="utf-8") as f:
            json.dump(all_articles, f, indent=2, ensure_ascii=False)

    print(f"Fetched {len(all_articles)} articles")


if __name__ == "__main__":
    main()
