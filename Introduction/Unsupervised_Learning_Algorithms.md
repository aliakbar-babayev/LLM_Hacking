# 🔍 Unsupervised Learning Algorithms

> **Red Team Mindset:** Defenders use unsupervised learning to find anomalies *without* knowing what attacks look like. If you understand how clustering and anomaly detection work, you can blend in or overwhelm them.

---

## 🧭 Overview

Unsupervised learning finds **hidden structure in unlabeled data**. No ground truth, no labels — the algorithm figures out patterns on its own.

```
Labeled Data   →  Supervised   →  "This is spam"
Unlabeled Data →  Unsupervised →  "These 3 groups seem different"
```

---

## 📂 Main Categories

| Category | Goal | Security Use Case |
|----------|------|------------------|
| **Clustering** | Group similar points | Network traffic segmentation |
| **Dimensionality Reduction** | Compress features | Visualize high-dim attack data |
| **Anomaly Detection** | Find outliers | Intrusion detection |
| **Density Estimation** | Model data distribution | Baseline normal behavior |

---

## 🔵 Clustering

### K-Means
Partitions data into **K clusters** by minimizing distance to cluster centers (centroids).

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = model.fit_predict(X)
centroids = model.cluster_centers_
```

**Algorithm Steps:**
1. Initialize K centroids randomly
2. Assign each point to nearest centroid
3. Recompute centroids as cluster means
4. Repeat until centroids stop moving

**Choosing K — Elbow Method:**
```python
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, n_init=10)
    km.fit(X)
    inertias.append(km.inertia_)
# Plot inertias — pick the "elbow" where the drop flattens
```

**Weakness:** Assumes spherical clusters, sensitive to outliers.

---

### DBSCAN (Density-Based Spatial Clustering)
Groups points that are **densely packed** together. Points in sparse regions = **noise/outliers**.

```python
from sklearn.cluster import DBSCAN

model = DBSCAN(eps=0.5, min_samples=5)
labels = model.fit_predict(X)
# label == -1  →  outlier/noise point
```

| Parameter | Meaning |
|-----------|---------|
| `eps` | Max distance between two points to be considered neighbors |
| `min_samples` | Min points to form a dense region (core point) |

**Strengths:**
- No need to specify K
- Finds arbitrary shaped clusters
- Naturally identifies outliers

> 🔴 **Red Team:** DBSCAN is used in IDS for traffic clustering. Points labeled `-1` (noise) are the ones flying under the radar — model your traffic to fall there.

---

### Hierarchical Clustering
Builds a **dendrogram** (tree of merges). Cut it at any level to get N clusters.

```python
from sklearn.cluster import AgglomerativeClustering
model = AgglomerativeClustering(n_clusters=4, linkage='ward')
labels = model.fit_predict(X)
```

---

## 📉 Dimensionality Reduction

### PCA — Principal Component Analysis
Finds the directions of **maximum variance** and projects data onto them. Linear transformation.

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X_scaled)   # Always standardize first!

# How much variance each component explains
print(pca.explained_variance_ratio_)
# e.g., [0.72, 0.15] → first 2 PCs explain 87% of variance
```

**Use cases:**
- Visualize high-dimensional data in 2D/3D
- Remove noisy/redundant features before ML
- Speed up training

---

### t-SNE — for Visualization
Non-linear technique that preserves **local neighborhood structure**. Not for ML pipelines — only for visualization.

```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_vis = tsne.fit_transform(X)
```

> Ideal for visualizing clusters in malware embeddings, network flows, or log data.

---

### UMAP — Faster, Better t-SNE
Preserves both local and global structure. Faster and more consistent.

```python
import umap
reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1)
X_vis = reducer.fit_transform(X)
```

---

## 🚨 Anomaly Detection

### Isolation Forest
Randomly isolates points using decision trees. **Anomalies are easier to isolate** (fewer splits needed).

```python
from sklearn.ensemble import IsolationForest

model = IsolationForest(contamination=0.05, random_state=42)
preds = model.fit_predict(X)
# -1 = anomaly,  1 = normal
scores = model.decision_function(X)   # More negative = more anomalous
```

`contamination` = expected fraction of outliers in data.

---

### One-Class SVM
Learns a boundary around "normal" data. Anything outside = anomaly.

```python
from sklearn.svm import OneClassSVM
model = OneClassSVM(nu=0.05, kernel='rbf', gamma='auto')
model.fit(X_normal)
preds = model.predict(X_new)   # -1 = anomaly
```

---

### Local Outlier Factor (LOF)
Compares local density of a point to its neighbors. Low density relative to neighbors = outlier.

```python
from sklearn.neighbors import LocalOutlierFactor
model = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
preds = model.fit_predict(X)
```

---

## 📊 Evaluation Without Labels

| Metric | Measures | Range |
|--------|---------|-------|
| **Silhouette Score** | How well-separated clusters are | [-1, 1] → higher = better |
| **Davies-Bouldin Index** | Avg similarity of clusters | Lower = better |
| **Calinski-Harabasz** | Ratio of between/within cluster variance | Higher = better |

```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X, labels)
```

---

## 🔴 Red Team Angle

| Technique | Red Team Application |
|-----------|---------------------|
| **K-Means** | Identify how defenders segment traffic → craft payloads that mimic the "normal" cluster centroid |
| **DBSCAN** | Points labeled as noise (`-1`) evade cluster-based detection — operate at low density |
| **Isolation Forest** | Anomaly score reveals how "weird" your traffic looks — tune your TTPs to minimize isolation score |
| **PCA** | Reveals which feature combinations carry the most signal for the defender → suppress those |
| **Autoencoder anomaly detection** | High reconstruction error = detected. Craft inputs with low reconstruction error |

**Evasion Strategy:**
```
1. Query the anomaly detector on benign traffic → establish baseline scores
2. Gradually shift your malicious traffic toward that baseline distribution
3. Stay within the density cloud of normal behavior (low isolation, high silhouette fit)
```

---

## 🔗 Linked Notes
- [[Introduction_to_Machine_Learning]]
- [[Supervised_Learning_Algorithms]]
- [[Introduction_to_Deep_Learning]]

---
*Tags: #UnsupervisedLearning #Clustering #KMeans #DBSCAN #AnomalyDetection #PCA #RedTeam*
