import feedparser
import trafilatura
from urllib.parse import urlparse
# import cloudscraper
# import requests
# from time import sleep

RSS_FEEDS_POLITICS = [
    ("https://www.pbs.org/newshour/feeds/rss/politics", "pbs.org"),
    ("https://slate.com/feeds/news-and-politics.rss", "slate.com"),
    ("https://feeds.npr.org/1014/rss.xml", "npr.org"),
    ("http://feeds.foxnews.com/foxnews/politics", "foxnews.com"),
]

RSS_FEEDS_TECH = [
    # ("https://spectrum.ieee.org/feeds/feed.rss", "spectrum.ieee.org"),
    # ("https://venturebeat.com/feed/", "venturebeat.com"),
    ("https://www.technologyreview.com/feed/", "technologyreview.com"),
    ("https://techcrunch.com/feed/", "techcrunch.com")
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
        if entry.title.startswith(("WATCH", "The Download:", "Video Friday:", "Fox News Politics Newsletter:")): continue
        if any(x in entry.link for x in ["/podcasts/", "/video/", "up-first-newsletter", "/newshour/show/", "/week-in-politics", 
                                         "startups-from-disrupt-startup-battlefield"]): continue
        if not is_valid_domain(entry['link'], domain): continue

        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.get('summary')[:300] or entry.get('description')[:300] or '',
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

    # scraper = cloudscraper.create_scraper()
    # max_retries = 2

    # # Try with cloudscraper first (handles Cloudflare automatically)
    # for attempt in range(1, max_retries + 1):
    #     try:
    #         resp = scraper.get(url)
    #         if resp.status_code == 200:
    #             return trafilatura.extract(resp.text)
    #     except Exception as e:
    #         print(f"cloudscraper attempt {attempt} failed: {e}")
    #     sleep(2)

    # # Fallback to plain requests with browser-like User-Agent
    # try:
    #     headers = {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    #                       "AppleWebKit/537.36 (KHTML, like Gecko) "
    #                       "Chrome/114.0.0.0 Safari/537.36"
    #     }
    #     resp = requests.get(url, headers=headers, timeout=15)
    #     if resp.status_code == 200:
    #         return trafilatura.extract(resp.text)
    #     print(f"Plain requests fallback returned status {resp.status_code}")
    # except Exception as e:
    #     print(f"Plain requests fallback failed: {e}")

    # return None
