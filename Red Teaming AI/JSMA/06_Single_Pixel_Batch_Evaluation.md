# Single-Pixel Batch Evaluation

> Back to [[00_JSMA_Index]] | Previous: [[05_Single_Pixel_Attack_Loop]]

## Why Batch Evaluation?

Running JSMA on a single image tells you one story. Running it on **hundreds or thousands of images** tells you how robust (or fragile) the model actually is.

Batch evaluation answers:
- **What % of images can be fooled?** (attack success rate)
- **How many pixels does it take on average?** (attack efficiency)
- **Which source→target class pairs are easiest to attack?**

## Setting Up Batch Evaluation

```python
def batch_evaluate(model, dataset, target_class, theta=1.0, gamma=0.1, max_samples=100):
    results = {
        'success': 0,
        'fail': 0,
        'total': 0,
        'pixels_modified': [],  # list of counts per successful attack
        'original_classes': [],
        'attack_details': []
    }
    
    for image, true_label in dataset:
        if true_label == target_class:
            continue  # skip if already the target class
        
        adv_image, success, num_modified = jsma_single_pixel(
            model, image, target_class, theta, gamma
        )
        
        results['total'] += 1
        if success:
            results['success'] += 1
            results['pixels_modified'].append(num_modified)
        else:
            results['fail'] += 1
        
        results['attack_details'].append({
            'original_class': true_label,
            'success': success,
            'pixels_modified': num_modified
        })
        
        if results['total'] >= max_samples:
            break
    
    return results
```

## Key Metrics

### 1. Attack Success Rate (ASR)
```
ASR = successful_attacks / total_attacks × 100%

Example: 73 out of 100 images fooled → ASR = 73%
```

### 2. Average Perturbation Size
```
avg_pixels = mean(pixels_modified for successful attacks)

Example: Average of 15.3 pixels modified per successful attack
         Out of 784 total → only 1.95% of pixels changed
```

### 3. Success Rate by Source Class
Some digit→target pairs are easier than others:

```
Attacking TO class "3":
  From "7": 92% success (7 and 3 look similar!)
  From "1": 85% success
  From "0": 45% success (0 and 3 look very different)
```

### 4. Confusion Matrix (Attack Version)
```
               Predicted After Attack
              0   1   2   3   4   5   6   7   8   9
Original  0 [ -  .02 .05 .45 .01 .10 .08 .03 .15 .11]
          1 [.03  -  .08 .85 .01 .02 .00 .01 .00 .00]
          ...
```

Each cell = success rate of attacking from row class to column class.

## Interpreting Results

| Metric | Good Attack | Weak Attack |
|--------|------------|-------------|
| ASR | > 80% | < 30% |
| Avg pixels modified | < 5% of total | > 15% of total |
| Consistency | Similar across source classes | Highly variable |

## What Batch Results Tell a Red Teamer

1. **High ASR** → Model is vulnerable to adversarial examples
2. **Low pixel count** → Attack is stealthy (hard to detect)
3. **Some classes easier** → Model has specific weak spots
4. **Consistent results** → Vulnerability is systematic, not random

## Key Takeaways

- Batch evaluation runs JSMA on many images to measure overall vulnerability
- Key metrics: **success rate**, **average pixels modified**, **per-class breakdown**
- Results reveal which class transitions are easiest to attack
- Essential for assessing a model's adversarial robustness systematically
