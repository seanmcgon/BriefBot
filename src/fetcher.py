import feedparser
import trafilatura

RSS_FEEDS = [
    "http://feeds.reuters.com/reuters/topNews",
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://feeds.npr.org/1001/rss.xml",
    "https://abcnews.go.com/abcnews/topstories",
    "https://www.cbsnews.com/latest/rss/main",
    "https://apnews.com/rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://feeds.npr.org/1014/rss.xml",
    "https://www.sciencedaily.com/rss/all.xml",
    "http://feeds.reuters.com/reuters/businessNews",
    "https://rss.dw.com/rdf/rss-en-all",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.wired.com/feed/rss",
    "https://hnrss.org/frontpage",
    "https://www.trackgit.com/github/rss/trending",
    "https://www.techmeme.com/feed.xml",
]

def fetch_articles(rss_url, max_articles=10):
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries[:max_articles]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "source": rss_url,
        })
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