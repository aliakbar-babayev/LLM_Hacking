# Pairwise Batch Evaluation

> Back to [[00_JSMA_Index]] | Previous: [[09_Pairwise_Attack_Loop]]

## Running Pairwise at Scale

Same concept as [[06_Single_Pixel_Batch_Evaluation]] but using the pairwise attack loop. The goal is to compare pairwise vs single-pixel performance across many images.

## Batch Evaluation Code

```python
def batch_evaluate_pairwise(model, dataset, target_class, theta=1.0, gamma=0.1, max_samples=100):
    results = {
        'success': 0,
        'fail': 0,
        'total': 0,
        'pixels_modified': [],
        'iterations': [],
        'original_classes': [],
    }
    
    for image, true_label in dataset:
        if true_label == target_class:
            continue
        
        adv_image, success, num_modified = jsma_pairwise(
            model, image, target_class, theta, gamma
        )
        
        results['total'] += 1
        if success:
            results['success'] += 1
            results['pixels_modified'].append(num_modified)
            results['iterations'].append(num_modified // 2)  # 2 pixels per iter
        else:
            results['fail'] += 1
        
        results['original_classes'].append(true_label)
        
        if results['total'] >= max_samples:
            break
    
    return results
```

## Metrics to Compare

### Side-by-Side: Single vs Pairwise

```
Metric                    Single-Pixel    Pairwise
─────────────────────────────────────────────────
Attack Success Rate (ASR)    73%            82%
Avg pixels modified          15.3           11.7
Avg iterations               15.3            5.9
Total compute time           45min          38min
```

### Per-Class Success Rates

```
Source → Target "3"     Single    Pairwise
──────────────────────────────────────────
"0" → "3"               45%        58%
"1" → "3"               85%        91%
"2" → "3"               62%        74%
"4" → "3"               55%        67%
"7" → "3"               92%        95%
"9" → "3"               78%        85%
```

Pairwise consistently outperforms single-pixel across all class pairs.

## Why Pairwise Wins

1. **Synergy capture**: Pairs can create visual features that single pixels can't
2. **Better gradient utilization**: Two complementary gradient directions combined
3. **Fewer wasted modifications**: Each iteration is more impactful
4. **Escapes local optima**: Single-pixel can get stuck; pair selection has more options

## When Single-Pixel Might Be Preferred

| Scenario | Use Single-Pixel |
|----------|------------------|
| Memory constrained | O(n) vs O(n²) saliency map |
| Very small budget (γ < 0.03) | Need fine-grained control |
| Interpretability | Easier to explain one pixel at a time |
| Speed per iteration | When n is very large |

## Recording Results for Analysis

```python
import json

def save_results(single_results, pairwise_results, filename):
    comparison = {
        'single_pixel': {
            'asr': single_results['success'] / single_results['total'],
            'avg_pixels': sum(single_results['pixels_modified']) / len(single_results['pixels_modified']),
        },
        'pairwise': {
            'asr': pairwise_results['success'] / pairwise_results['total'],
            'avg_pixels': sum(pairwise_results['pixels_modified']) / len(pairwise_results['pixels_modified']),
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(comparison, f, indent=2)
```

## Key Takeaways

- Pairwise typically achieves **higher success rates** with **fewer pixels modified**
- The improvement comes from **capturing pixel synergies**
- Both methods should be compared on the same dataset for fair evaluation
- Single-pixel may be preferred when memory or interpretability is critical
- Track **per-class breakdowns** to understand model-specific vulnerabilities
