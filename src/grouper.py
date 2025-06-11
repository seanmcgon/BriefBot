from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
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
        # Group articles by story_cluster
        clusters = defaultdict(list)
        for article in articles:
            clusters[article["story_cluster"]].append(article)

        # Find the two largest clusters
        top_two = sorted(clusters.items(), key=lambda item: len(item[1]), reverse=True)[:2]
        top_two_clusters = [cluster for _, cluster in top_two]

        top_articles[category] = top_two_clusters

    return top_articles