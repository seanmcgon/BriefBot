import feedparser
import trafilatura
from urllib.parse import urlparse

RSS_FEEDS_POLITICS = [
    ("https://www.pbs.org/newshour/feeds/rss/politics", "pbs.org"),
    ("https://slate.com/feeds/news-and-politics.rss", "slate.com"),
    ("https://feeds.npr.org/1014/rss.xml", "npr.org"),
    ("http://feeds.foxnews.com/foxnews/politics", "foxnews.com"),
]

RSS_FEEDS_TECH = [
    ("https://thenextweb.com/feed/", "thenextweb.com"),
    ("https://venturebeat.com/feed/", "venturebeat.com"),
    ("https://www.technologyreview.com/feed/", "technologyreview.com"),
]

def is_valid_domain(entry_url, expected_domain):
    parsed = urlparse(entry_url)
    return expected_domain in parsed.netloc

def fetch_articles(source, category, max_articles=10):
    rss_url, domain = source
    print("Parsing ", rss_url)
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries:
        # Prevent certain types of articles and link hijacking
        if entry.title.startswith(("WATCH", "The Download:")): continue
        if "up-first-newsletter" in entry.link: continue
        if not is_valid_domain(entry['link'], domain): continue

        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.get('summary') or entry.get('description') or '',
            "source": rss_url,
            "category": category,
        })
        if len(articles) == 10: break
    return articles

def deduplicate_articles_by_title(articles):
    seen_titles = set()
    deduped = []

    for article in articles:
        title = article["title"].strip().lower()  # Normalize case + spacing
        if title not in seen_titles:
            seen_titles.add(title)
            deduped.append(article)

    return deduped

def fetch_full_article(url):
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return trafilatura.extract(downloaded)
    return None