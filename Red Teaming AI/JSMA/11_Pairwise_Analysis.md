# Pairwise Analysis

> Back to [[00_JSMA_Index]] | Previous: [[10_Pairwise_Batch_Evaluation]]

## Analyzing Attack Results

After running both single-pixel and pairwise attacks, this section covers how to interpret and present the findings.

## Statistical Comparison

### 1. Success Rate Significance

Don't just compare raw percentages — check if the difference is statistically meaningful:

```python
from scipy import stats

# Example data
single_successes = 73  # out of 100
pairwise_successes = 82  # out of 100
n = 100

# Chi-squared test or proportion test
z_stat, p_value = stats.proportions_ztest(
    [single_successes, pairwise_successes], [n, n]
)

if p_value < 0.05:
    print("Pairwise is significantly better")
else:
    print("Difference might be due to chance")
```

### 2. Pixel Efficiency Distribution

```
Single-Pixel pixel counts (per successful attack):
  Min: 3, Q1: 8, Median: 14, Q3: 22, Max: 65

Pairwise pixel counts (per successful attack):
  Min: 2, Q1: 5, Median: 10, Q3: 16, Max: 48

→ Pairwise modifies ~30% fewer pixels on average
```

### 3. Per-Pair Difficulty Ranking

```python
def rank_class_pairs(results):
    """Rank source→target pairs by attack difficulty."""
    pair_stats = {}
    
    for detail in results['attack_details']:
        pair = (detail['original_class'], target_class)
        if pair not in pair_stats:
            pair_stats[pair] = {'success': 0, 'total': 0, 'pixels': []}
        pair_stats[pair]['total'] += 1
        if detail['success']:
            pair_stats[pair]['success'] += 1
            pair_stats[pair]['pixels'].append(detail['pixels_modified'])
    
    # Sort by success rate (ascending = hardest first)
    ranked = sorted(pair_stats.items(), 
                   key=lambda x: x[1]['success']/x[1]['total'])
    
    return ranked
```

Output:
```
Hardest attacks (lowest success rate):
  1. "0" → "3": 45% ASR, avg 28 pixels
  2. "6" → "3": 52% ASR, avg 24 pixels
  
Easiest attacks (highest success rate):
  1. "7" → "3": 95% ASR, avg 8 pixels
  2. "1" → "3": 91% ASR, avg 10 pixels
```

## What the Analysis Reveals

### Feature Space Relationships

Easy attacks tell you which classes are **close in feature space**:
- "7" → "3" is easy because they share structural features (top horizontal, vertical stroke)
- "0" → "3" is hard because "0" is closed/rounded while "3" is open

### Model Weaknesses

If a model is easily fooled on many pairs → it hasn't learned robust features.

```
High ASR across all pairs:
  → Model relies on superficial pixel patterns
  → Not robust to adversarial perturbation
  → Would need adversarial training to fix

Low ASR on most pairs:
  → Model has learned more robust features
  → Harder to attack with L0 perturbations
```

### Perturbation Patterns

Analyze WHERE pixels are modified:

```python
def analyze_perturbation_locations(original, adversarial):
    """Find which pixels were changed and their positions."""
    diff = (adversarial - original).abs()
    modified_mask = diff > 0
    
    # For 28x28 images
    positions = modified_mask.view(28, 28).nonzero()
    
    # Are modifications clustered or spread out?
    center = positions.float().mean(dim=0)
    spread = positions.float().std(dim=0)
    
    return {
        'num_modified': modified_mask.sum().item(),
        'center': center.tolist(),
        'spread': spread.tolist(),
        'positions': positions.tolist()
    }
```

Typical findings:
- **Clustered** modifications → attack targets a specific structural feature
- **Spread out** modifications → attack disrupts the overall pattern
- **Edge** modifications → model relies heavily on contour features

## Summary Table Template

```
┌─────────────────────────────────────────────────────┐
│           JSMA Attack Analysis Summary               │
├─────────────────────┬──────────────┬────────────────┤
│ Metric              │ Single-Pixel │ Pairwise       │
├─────────────────────┼──────────────┼────────────────┤
│ ASR                 │ 73%          │ 82%            │
│ Avg pixels modified │ 15.3         │ 11.7           │
│ Median pixels       │ 14           │ 10             │
│ Avg iterations      │ 15.3         │ 5.9            │
│ Easiest pair        │ 7→3 (92%)    │ 7→3 (95%)      │
│ Hardest pair        │ 0→3 (45%)    │ 0→3 (58%)      │
│ Compute time        │ 45 min       │ 38 min         │
└─────────────────────┴──────────────┴────────────────┘
```

## Key Takeaways

- **Statistical testing** confirms whether pairwise is truly better or just luck
- **Per-class breakdown** reveals which class transitions expose model weaknesses
- **Perturbation location analysis** shows what features the model relies on
- Easy attack pairs → classes are close in the model's learned feature space
- High overall ASR → model needs adversarial training for robustness
