# Deprecated as of June 2025 — replaced with curated RSS feeds

from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

CATEGORIES = ["tech", "politics", "business", "sports", "health", "science", "world"]

def categorize_article(article):
    text = f"{article['title']} {article.get('summary', '')}"
    result = classifier(text, CATEGORIES)
    # result['labels'] is sorted by confidence
    article["category"] = result["labels"][0]
    article["confidence"] = result["scores"][0]
    if article["confidence"] < 0.375:
        article["category"] = "other"
    
    print(article['category'])
    return article
