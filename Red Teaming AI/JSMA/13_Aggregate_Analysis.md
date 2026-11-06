# Aggregate Analysis

> Back to [[00_JSMA_Index]] | Previous: [[12_Visualizations]]

## The Big Picture

Aggregate analysis combines all results from single-pixel and pairwise attacks across all class pairs to draw **conclusions about the model's overall robustness**.

## Full Attack Matrix

Instead of attacking to just one target class, run attacks for **every source→target pair**:

```python
def full_attack_matrix(model, dataset, attack_fn, theta=1.0, gamma=0.1, samples_per_pair=20):
    """Run attacks for all source→target combinations."""
    num_classes = 10  # For MNIST
    
    # Result matrix: success_rate[source][target]
    asr_matrix = torch.zeros(num_classes, num_classes)
    pixel_matrix = torch.zeros(num_classes, num_classes)
    
    for target in range(num_classes):
        for source in range(num_classes):
            if source == target:
                continue
            
            # Get images of source class
            source_images = [img for img, lbl in dataset if lbl == source][:samples_per_pair]
            
            successes = 0
            total_pixels = 0
            
            for img in source_images:
                _, success, n_pixels = attack_fn(model, img, target, theta, gamma)
                if success:
                    successes += 1
                    total_pixels += n_pixels
            
            asr_matrix[source][target] = successes / len(source_images)
            if successes > 0:
                pixel_matrix[source][target] = total_pixels / successes
    
    return asr_matrix, pixel_matrix
```

### Reading the ASR Matrix

```
               TARGET CLASS
           0    1    2    3    4    5    6    7    8    9
S  0  [  —   .65  .40  .45  .55  .50  .60  .70  .48  .52 ]
O  1  [ .55   —   .42  .85  .30  .25  .20  .90  .35  .40 ]
U  2  [ .45  .50   —   .62  .48  .55  .52  .58  .60  .45 ]
R  3  [ .42  .70  .55   —   .38  .65  .40  .60  .72  .50 ]
C  4  [ .50  .60  .35  .40   —   .45  .55  .48  .42  .80 ]
E  5  [ .55  .30  .40  .65  .50   —   .70  .35  .55  .45 ]
   6  [ .62  .25  .45  .42  .48  .72   —   .30  .55  .40 ]
   7  [ .60  .88  .50  .92  .55  .35  .30   —   .42  .48 ]
   8  [ .45  .40  .55  .72  .50  .60  .55  .45   —   .52 ]
   9  [ .50  .80  .35  .48  .85  .55  .42  .70  .50   —  ]
```

**Hot spots** (high values): vulnerable class transitions
**Cold spots** (low values): robust class boundaries

## Key Aggregate Metrics

### 1. Overall ASR

```
overall_asr = asr_matrix.sum() / (num_classes * (num_classes - 1))

Interpretation:
  > 70%: Model is broadly vulnerable
  40-70%: Moderate robustness
  < 40%: Reasonably robust against JSMA
```

### 2. Per-Class Vulnerability (as Source)

"How easy is it to make the model stop predicting this class?"

```python
source_vulnerability = asr_matrix.mean(dim=1)  # Average across all targets

# High score → this class is easy to attack FROM
# The model is not confident about these features
```

### 3. Per-Class Attractiveness (as Target)

"How easy is it to make the model predict this class?"

```python
target_attractiveness = asr_matrix.mean(dim=0)  # Average across all sources

# High score → this class is easy to attack TO
# The model has broad "basins" for this class in feature space
```

### 4. Asymmetry

Is "7→3" equally easy as "3→7"?

```python
asymmetry = (asr_matrix - asr_matrix.T).abs()

# High asymmetry → the model treats the boundary differently
# in each direction — directional vulnerability
```

## Model Robustness Report

```
═══════════════════════════════════════════════
    JSMA ADVERSARIAL ROBUSTNESS REPORT
═══════════════════════════════════════════════

Model: MNIST Classifier (3-layer CNN)
Dataset: MNIST Test Set (1000 samples)
Attack: JSMA (θ=1.0, γ=0.1)

OVERALL METRICS
  Single-Pixel ASR:     58.2%
  Pairwise ASR:         67.5%
  Improvement:          +9.3pp

MOST VULNERABLE TRANSITIONS
  1. 7 → 3:  95% ASR,  avg 8 pixels
  2. 1 → 7:  90% ASR,  avg 6 pixels
  3. 9 → 4:  85% ASR,  avg 12 pixels

MOST ROBUST TRANSITIONS
  1. 0 → 1:  15% ASR,  avg 42 pixels
  2. 6 → 1:  20% ASR,  avg 38 pixels
  3. 8 → 1:  22% ASR,  avg 35 pixels

CLASS VULNERABILITY RANKING (easiest to attack FROM)
  Most vulnerable:  "1" (avg ASR 71%)
  Most robust:      "0" (avg ASR 42%)

CLASS ATTRACTIVENESS RANKING (easiest to attack TO)
  Most attractive:  "3" (avg ASR 68%)
  Least attractive: "1" (avg ASR 35%)

RECOMMENDATION
  Model shows significant vulnerability to JSMA attacks.
  Consider adversarial training with L0-bounded perturbations
  focusing on vulnerable class pairs.
═══════════════════════════════════════════════
```

## Connecting to LLM Red Teaming

These adversarial ML concepts map to LLM security:

| Adversarial ML (JSMA) | LLM Red Teaming |
|----------------------|------------------|
| Pixel perturbation | Token/prompt manipulation |
| Saliency map | Token importance / attention |
| Target class | Desired model output |
| Attack budget | Prompt length constraints |
| White-box (gradients) | Open-weight model access |
| Robustness evaluation | Jailbreak resistance testing |

## Key Takeaways

- **Full attack matrix** reveals all vulnerable source→target transitions
- **Asymmetry** analysis shows directional weaknesses
- Aggregate metrics give an **overall robustness score**
- The report template is how you'd communicate findings professionally
- These concepts directly parallel LLM red teaming techniques
