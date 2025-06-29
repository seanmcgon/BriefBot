from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from collections import defaultdict, deque
import os, json

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
        sorted_clusters = sorted(clusters.items(), key=lambda item: len(item[1]), reverse=True)
        clusters_by_size = [cluster for _, cluster in sorted_clusters]
        chosen_clusters = []
        recent_clusters = deque([], 20)
        if os.path.exists(f"cache/{category}_cache.json"):
            with open(f"cache/{category}_cache.json", "r", encoding="utf-8") as f:
                loaded = json.load(f)
                recent_clusters = deque([set(item) for item in loaded], 20)
            print(f"Recent {category} clusters:", recent_clusters)
            for cur_cluster in clusters_by_size:
                # Skip if we've seen these same articles in last ten days
                links = set([a["link"] for a in cur_cluster])
                is_subset = any(links.issubset(cluster) for cluster in recent_clusters)
                if is_subset: continue

                chosen_clusters.append(cur_cluster)
                recent_clusters.append(links)
                if len(chosen_clusters) == 2: break
        else:
            chosen_clusters = clusters_by_size[:2]
            for cur_cluster in chosen_clusters:
                links = set([a["link"] for a in cur_cluster])
                recent_clusters.append(links)
        
        serializable_data = [list(s) for s in recent_clusters]
        with open(f"cache/{category}_cache.json", "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)


        top_articles[category] = chosen_clusters

    return top_articles