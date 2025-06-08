from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_distances
import numpy as np
from collections import defaultdict

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_article_embedding(article):
    text = article['title'] + " " + article.get('summary', '')
    return model.encode(text, normalize_embeddings=True)  # normalize helps similarity comparisons

def cluster_articles(articles, threshold=0.4):
    if len(articles) < 2:
        for a in articles:
            a["story_cluster"] = 0
        return articles
    
    embeddings = np.array([get_article_embedding(a) for a in articles])

    clustering = AgglomerativeClustering(
        n_clusters=None,  # automatic
        metric='cosine',
        linkage='average',
        distance_threshold=threshold
    )
    labels = clustering.fit_predict(embeddings)

    for article, label in zip(articles, labels):
        article["story_cluster"] = int(label)

    return articles

def select_top_articles_by_category(grouped):
    top_articles = {}

    for category, articles in grouped.items():
        # Sports and other categories unnecessary
        if category == "sports" or category == "other": continue

        # Group articles by story_cluster
        clusters = defaultdict(list)
        for article in articles:
            clusters[article["story_cluster"]].append(article)

        # Find the largest cluster
        largest_cluster = max(clusters.values(), key=len)

        if len(largest_cluster) > 1:
            # If there's a clear top cluster, grab all articles
            chosen_articles = largest_cluster
        else:
            # Fall back to highest confidence
            chosen_articles = [max(articles, key=lambda a: a.get("confidence", 0))]

        top_articles[category] = chosen_articles

    return top_articles