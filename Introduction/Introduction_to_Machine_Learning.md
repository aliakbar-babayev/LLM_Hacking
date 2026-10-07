# 🤖 Introduction to Machine Learning

> **Red Team Mindset:** Understanding ML is understanding the target. Before you can attack a system, you need to know how it thinks.

---

## 🧠 What is Machine Learning?

Machine Learning is a subset of AI where systems **learn patterns from data** rather than following hand-coded rules. Instead of programming explicit logic, you feed the machine examples and let it figure out the rules itself.

```
Traditional Programming:  Rules + Data  → Output
Machine Learning:         Data + Output → Rules
```

---

## 📦 The Three Pillars of ML

### 1. Supervised Learning
- Learns from **labeled data** (input → known output)
- Goal: predict the output for unseen inputs
- Examples: spam detection, malware classification

### 2. Unsupervised Learning
- Learns from **unlabeled data** — no predefined answers
- Goal: find hidden structure or patterns
- Examples: anomaly detection, network traffic clustering

### 3. Reinforcement Learning
- An **agent** learns by interacting with an environment
- Gets rewards for good actions, penalties for bad ones
- Examples: game-playing AI, autonomous attack bots

---

## 🔄 The ML Pipeline

```
1. Data Collection
       ↓
2. Data Preprocessing (clean, normalize, encode)
       ↓
3. Feature Engineering (select/craft meaningful inputs)
       ↓
4. Model Training (fit algorithm to data)
       ↓
5. Evaluation (measure performance)
       ↓
6. Deployment (serve predictions in production)
```

Each step is an **attack surface**. Data poisoning hits step 1–2. Model evasion hits step 6.

---

## 🔑 Core Terminology

| Term | Meaning |
|------|---------|
| **Feature (X)** | Input variable fed to the model |
| **Label (y)** | Target output the model tries to predict |
| **Model** | Mathematical function mapping X → y |
| **Training** | Fitting the model on data |
| **Inference** | Using the trained model to predict |
| **Overfitting** | Model memorizes training data, fails on new data |
| **Underfitting** | Model too simple, misses patterns |
| **Hyperparameter** | Settings tuned before training (e.g., learning rate) |
| **Epoch** | One full pass through the training data |

---

## ✂️ Data Splitting

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

| Split | Size | Purpose |
|-------|------|---------|
| Training | ~70% | Fit the model |
| Validation | ~10–15% | Tune hyperparameters |
| Test | ~15–20% | Final unbiased evaluation |

---

## 📏 Evaluation Metrics

### Classification
- **Accuracy** = Correct / Total
- **Precision** = TP / (TP + FP) → "Of what I flagged, how many were real?"
- **Recall** = TP / (TP + FN) → "Of all real threats, how many did I catch?"
- **F1 Score** = Harmonic mean of Precision & Recall

> 🔴 **Red Team insight:** A model with high precision but low recall catches few real attacks — easy to slip through. Target recall weaknesses.

### Regression
- **MAE** — Average absolute error
- **RMSE** — Penalizes large errors more
- **R²** — How much variance the model explains (1.0 = perfect)

---

## 🛠️ Essential Python Libraries

```python
import numpy as np           # Arrays and math
import pandas as pd          # DataFrames and data wrangling
import matplotlib.pyplot as plt  # Plotting
import seaborn as sns        # Statistical visualization
from sklearn import *        # ML algorithms, metrics, preprocessing
```

---

## 🔴 Red Team Angle

| ML Phase | Attack Vector |
|----------|--------------|
| Data Collection | **Data poisoning** — corrupt training data |
| Feature Engineering | **Feature manipulation** — fool feature extractors |
| Model Training | **Backdoor/Trojan injection** |
| Inference | **Adversarial examples** — craft inputs that fool the model |
| Deployment | **Model stealing, API abuse, membership inference** |

---

## 🔗 Linked Notes
- [[Supervised_Learning_Algorithms]]
- [[Unsupervised_Learning_Algorithms]]
- [[Reinforcement_Learning_Algorithms]]
- [[Introduction_to_Deep_Learning]]
- [[Introduction_to_Generative_AI]]

---
*Tags: #ML #Fundamentals #RedTeam #MachineLearning*
