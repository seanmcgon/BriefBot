from src.summarizer import get_daily_summary
from src.fetcher import RSS_FEEDS, fetch_articles, deduplicate_articles_by_title, fetch_full_article
from src.classifier import categorize_article
from src.grouper import cluster_articles, select_top_articles_by_category
import json
import os
from collections import defaultdict

def main():
    USE_CACHE = True

    all_articles = []

    if USE_CACHE and os.path.exists("cached_articles.json"):
        with open("cached_articles.json", "r", encoding="utf-8") as f:
            all_articles = json.load(f)
    else:
        for feed in RSS_FEEDS:
            all_articles.extend(fetch_articles(feed))
        all_articles = deduplicate_articles_by_title(all_articles)
        all_articles = [categorize_article(article) for article in all_articles]
        with open("cached_articles.json", "w", encoding="utf-8") as f:
            json.dump(all_articles, f, indent=2, ensure_ascii=False)

    grouped = defaultdict(list)

    if USE_CACHE and os.path.exists("clustered_articles.json"):
        with open("clustered_articles.json", "r", encoding="utf-8") as f:
            grouped = json.load(f)
    else:
        for article in all_articles:
            grouped[article["category"]].append(article)

        for category, articles in grouped.items():
            print(f"Clustering {len(articles)} articles in category: {category}")
            clustered = cluster_articles(articles)
        with open("clustered_articles.json", "w", encoding="utf-8") as f:
            json.dump(grouped, f, indent=2, ensure_ascii=False)

    top_articles = []

    if USE_CACHE and os.path.exists("top_full_texts.json"):
        with open("top_full_texts.json", "r", encoding="utf-8") as f:
            top_articles = json.load(f)
    else:
        top_articles = select_top_articles_by_category(grouped)
        for category, articles in top_articles.items():
            for article in articles:
                full_text = fetch_full_article(article["link"])
                article["full_text"] = full_text or "[Unable to extract content]"
        with open("top_full_texts.json", "w", encoding="utf-8") as f:
            json.dump(top_articles, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
