# 🎯 Supervised Learning Algorithms

> **Red Team Mindset:** Know the algorithm, know its blind spots. Every model has decision boundaries — your job is to find the cracks.

---

## 📂 Two Problem Types

| Type | Output | Example |
|------|--------|---------|
| **Classification** | Discrete class label | Malware vs. benign |
| **Regression** | Continuous number | Predict attack likelihood score |

---

## 📈 Regression Algorithms

### Linear Regression
The simplest model — fits a straight line through data.

```
ŷ = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ
```

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

**When to use:** Continuous output, roughly linear relationship.
**Weakness:** Fails on non-linear patterns.

### Ridge (L2) vs. Lasso (L1) Regression

| Method | Penalty | Effect |
|--------|---------|--------|
| Ridge | Sum of squared weights | Shrinks all weights |
| Lasso | Sum of absolute weights | Drives some weights to **zero** (feature selection) |

---

## 🏷️ Classification Algorithms

### Logistic Regression
Despite the name — it's a **classifier**. Uses the sigmoid function to output a probability.

```
σ(z) = 1 / (1 + e⁻ᶻ)   →   output ∈ (0, 1)
```

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
```

**Strength:** Fast, interpretable, good baseline.
**Weakness:** Linear decision boundary only.

---

### Decision Trees
Learns a tree of if/else rules by splitting data on features.

```
         [Packet size > 1500?]
            /           \
          Yes             No
  [Port == 443?]    [Predict: Normal]
    /        \
  Yes         No
[HTTPS]   [Suspicious]
```

```python
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(max_depth=5)
model.fit(X_train, y_train)
```

**Strength:** Interpretable, handles non-linear data.
**Weakness:** Overfits easily without depth limits.

---

### Random Forest
An **ensemble** of decision trees — each tree sees a random subset of data and features. Final prediction = majority vote.

```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Check what features matter most
importances = model.feature_importances_
```

**Strength:** Robust, handles noise, gives feature importance.
**Red Team use:** Feature importance reveals what the defender's model cares about → evade those features.

---

### Support Vector Machine (SVM)
Finds the **maximum-margin hyperplane** that best separates classes. The **kernel trick** projects data into higher dimensions for non-linear separation.

```python
from sklearn.svm import SVC
model = SVC(kernel='rbf', C=1.0, gamma='scale')
model.fit(X_train, y_train)
```

| Kernel | Use Case |
|--------|----------|
| `linear` | Linearly separable data |
| `rbf` | General non-linear (default) |
| `poly` | Polynomial boundaries |

---

### K-Nearest Neighbors (KNN)
No training — classifies based on the **K most similar examples** in training data.

```python
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
```

**Strength:** Simple, intuitive.
**Weakness:** Slow at inference, sensitive to irrelevant features.

---

### Naive Bayes
Based on **Bayes' Theorem** — assumes features are independent.

```
P(class | features) ∝ P(class) × ∏ P(featureᵢ | class)
```

```python
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(X_train, y_train)
```

**Best for:** Text classification, spam detection, fast inference.

---

### Gradient Boosting (XGBoost / LightGBM)
Builds trees **sequentially** — each tree corrects errors of the previous one.

```python
import xgboost as xgb
model = xgb.XGBClassifier(n_estimators=200, learning_rate=0.05, max_depth=6)
model.fit(X_train, y_train)
```

**Strength:** Often top performer on tabular data, wins competitions.
**Weakness:** Many hyperparameters to tune, slower to train.

---

## 🔧 Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, None]
}
gs = GridSearchCV(RandomForestClassifier(), param_grid, cv=5, scoring='f1')
gs.fit(X_train, y_train)
print("Best params:", gs.best_params_)
```

---

## 📊 Algorithm Comparison

| Algorithm | Interpretable | Speed | Handles Non-linear | Large Datasets |
|-----------|:-----------:|:-----:|:-----------------:|:--------------:|
| Linear/Logistic | ✅ | ⚡ Fast | ❌ | ✅ |
| Decision Tree | ✅ | ⚡ Fast | ✅ | ⚠️ |
| Random Forest | ⚠️ | 🔶 Medium | ✅ | ✅ |
| SVM | ❌ | 🔴 Slow | ✅ | ❌ |
| KNN | ✅ | 🔴 Slow | ✅ | ❌ |
| XGBoost | ❌ | ⚡ Fast | ✅ | ✅ |

---

## 🔴 Red Team Angle

| Algorithm | Attack Strategy |
|-----------|----------------|
| **Logistic Regression** | Feature space is linear — small perturbations near decision boundary flip predictions |
| **Decision Tree** | Fully interpretable — reverse-engineer exact rules, craft inputs that fall in desired leaf |
| **Random Forest** | Query feature importances → deliberately suppress high-importance features in your payload |
| **SVM** | Attacks near the support vectors are most effective |
| **KNN** | Inject poisoned points near target class boundaries to shift neighbor votes |
| **XGBoost** | Hard to interpret but vulnerable to adversarial tabular attacks |

---

## 🔗 Linked Notes
- [[Introduction_to_Machine_Learning]]
- [[Unsupervised_Learning_Algorithms]]
- [[Introduction_to_Deep_Learning]]

---
*Tags: #SupervisedLearning #Classification #Regression #DecisionTree #RandomForest #SVM #RedTeam*
