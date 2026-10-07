
# Metrics for Evaluating a Model

---

When assessing a trained machine learning model, one examines a set of numerical metrics to gauge how well the model performs on a given task. These metrics often quantify the relationship between predictions and known ground-truth labels.

In the [Fundamentals of AI](https://academy.hackthebox.com/module/details/290) module, we briefly covered metrics such as `accuracy`, `precision`, `recall`, and `F1-score`, and we know that these metrics provide different perspectives on model behavior.

## Accuracy

`Accuracy` is the proportion of correct predictions out of all predictions made. It measures how often the model classifies instances correctly. A model with `accuracy: 0.9950` indicates that it makes correct predictions 99.50% of the time.

Key points about `accuracy`:

- Measures overall correctness.
- Computed as `(true positives + true negatives) / (all instances)`.
- May be misleading in cases of class imbalance.

While `accuracy` appears intuitive, relying on it alone can hide important details. Consider a spam classification scenario where only 1% of incoming emails are spam and 99% are legitimate. A model that always predicts every email as legitimate will achieve `accuracy: 0.99`, but it will never catch any spam.

In this case, accuracy fails to highlight the model’s inability to correctly identify the minority class. This underscores the importance of complementary metrics, such as `precision`, `recall`, or `F1-score`, which provide a more nuanced understanding of performance when dealing with imbalanced datasets.

## Precision

`Precision` measures how often the model’s predicted positives are truly positive. For `precision: 0.9949`, when the model labels an instance as positive, it is correct 99.49% of the time.

Key points about `precision`:

- Reflects quality of positive predictions.
- Computed as `true positives / (true positives + false positives)`.
- High `precision` reduces wasted effort caused by false alarms.

With the spam classification example, if the model labels 100 emails as spam, and 99 of them are actually spam, then its `precision` is high. This reduces the inconvenience of losing important, legitimate emails to the spam folder. However, if the model rarely identifies spam in the first place, it may fail to catch a large portion of malicious emails. High `precision` alone does not guarantee that the model is finding all the spam it should.

## Recall

`Recall` measures the model’s ability to identify all positive instances. For `recall: 0.9950`, the model detects 99.50% of all positives.

Key points about `recall`:

- Reflects completeness of positive detection.
- Computed as `true positives / (true positives + false negatives)`.
- High `recall` reduces the risk of missing critical cases.

In the spam classification scenario, a model with high `recall` correctly flags most spam emails. This helps ensure that suspicious content does not slip through unnoticed. However, a model with very high `recall` but low `precision` might flood the spam folder with benign emails. Although it rarely misses spam, it inconveniences the user by misclassifying too many legitimate emails as spam.

## F1-Score

`F1-score` is the harmonic mean of `precision` and `recall`. For `F1-score: 0.9949`, the metric indicates a near-perfect balance between these two aspects.

Key points about `F1-score`:

- Balances `precision` and `recall`.
- Computed as `2 * (precision * recall) / (precision + recall)`.
- Useful for tasks involving class imbalance.

Continuing with the spam classification scenario, the `F1-score` ensures that the model not only minimizes the misclassification of legitimate emails (high `precision`) but also effectively identifies the majority of spam messages (high `recall`). By focusing on the balance rather than just one metric, the `F1-score` provides a more complete picture of the model’s performance in identifying and correctly handling both spam and non-spam emails.