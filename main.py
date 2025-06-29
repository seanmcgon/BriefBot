from src.summarizer import mistral_summarize
from src.fetcher import RSS_FEEDS_POLITICS, RSS_FEEDS_TECH, fetch_articles, deduplicate_articles_by_title, fetch_full_article
from src.grouper import cluster_articles, select_top_articles_by_category
from src.emailer import build_html_email, send_email
import json, os, time, random
from collections import defaultdict
from dotenv import load_dotenv

def main():
    load_dotenv()
    USE_CACHE = False

    all_articles = []

    if USE_CACHE and os.path.exists("cached_articles.json"):
        with open("cached_articles.json", "r", encoding="utf-8") as f:
            all_articles = json.load(f)
    else:
        for feed in RSS_FEEDS_POLITICS:
            all_articles.extend(fetch_articles(feed, "politics"))
        for feed in RSS_FEEDS_TECH:
            all_articles.extend(fetch_articles(feed, "tech"))
        all_articles = deduplicate_articles_by_title(all_articles)
        with open("cached_articles.json", "w", encoding="utf-8") as f:
            json.dump(all_articles, f, indent=2, ensure_ascii=False)

    grouped = defaultdict(list)

    if USE_CACHE and os.path.exists("clustered_articles.json"):
        with open("clustered_articles.json", "r", encoding="utf-8") as f:
            grouped = json.load(f)
    else:
        random.shuffle(all_articles)
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
        for category, clusters in top_articles.items():
            for cluster in clusters:
                for article in cluster:
                    full_text = fetch_full_article(article["link"])
                    article["full_text"] = full_text or "[Unable to extract content]"
        with open("top_full_texts.json", "w", encoding="utf-8") as f:
            json.dump(top_articles, f, indent=2, ensure_ascii=False)

    # summaries = defaultdict(list)

    # if USE_CACHE and os.path.exists("summaries.json"):
    #     with open("summaries.json", "r", encoding="utf-8") as f:
    #         summaries = json.load(f)
    # else:
    #     for category, clusters in top_articles.items():
    #         for cluster in clusters:
    #             full_texts = [a.get("full_text") for a in cluster if a.get("full_text")]
    #             combined_text = "\n\n".join(full_texts)
    #             summary = mistral_summarize(combined_text)
    #             summaries[category].append(summary)
    #             time.sleep(1)
    #     with open("summaries.json", "w", encoding="utf-8") as f:
    #         json.dump(summaries, f, indent=2, ensure_ascii=False)
    
    # content = defaultdict(list)
    # for category, sums in summaries.items():
    #     for i in range(2):
    #         obj = {"text": sums[i]}
    #         obj["links"] = [a["link"] for a in top_articles[category][i]]
    #         content[category].append(obj)

    # html = build_html_email(content)

    # send_email(
    #     subject="📰 Your Daily BriefBot",
    #     html_body=html,
    #     from_email=os.getenv("SENDER"),
    #     to_email=os.getenv("RECIPIENT"),
    #     smtp_server="smtp.gmail.com",
    #     smtp_port=465,
    #     login=os.getenv("EMAIL"),
    #     password=os.getenv("EMAIL_PASSWORD")
    # )



if __name__ == "__main__":
    main()
