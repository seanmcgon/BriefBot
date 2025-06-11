import feedparser
import trafilatura

RSS_FEEDS_POLITICS = [
    "https://www.pbs.org/newshour/feeds/rss/politics",
    "http://rss.cnn.com/rss/cnn_allpolitics.rss",
    "https://feeds.npr.org/1014/rss.xml",
    "http://feeds.foxnews.com/foxnews/politics",
]

RSS_FEEDS_TECH = [
    "https://thenextweb.com/feed/",
    "https://venturebeat.com/feed/",
    "https://www.zdnet.com/news/rss.xml",
]

def fetch_articles(rss_url, category, max_articles=10):
    print("Parsing ", rss_url)
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries:
        if entry.title.startswith("WATCH"): continue
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