# Single-Pixel Configuration

> Back to [[00_JSMA_Index]] | Previous: [[06_Single_Pixel_Batch_Evaluation]]

## Tuning the Attack

JSMA has several parameters that dramatically affect its performance. Understanding how to configure them is key to running effective attacks.

## Parameter Deep Dive

### 1. Theta (θ) — Perturbation Step Size

Controls how much each selected pixel changes per iteration.

```
θ = +1.0  → Set pixel to maximum (most aggressive, increases brightness)
θ = -1.0  → Set pixel to minimum (most aggressive, decreases brightness)
θ = +0.5  → Increase pixel by 0.5 (moderate)
θ = -0.5  → Decrease pixel by 0.5 (moderate)
```

**Impact**:
| θ value | Effect |
|---------|--------|
| Large (+1 or -1) | Fewer iterations needed, but more visible changes |
| Small (±0.1) | More iterations, subtler changes, may not converge |

**Best practice**: Start with ±1.0. If attack is too visible, try ±0.5.

### 2. Gamma (γ) — Pixel Budget

Maximum fraction of pixels that can be modified.

```
γ = 0.05 → Only 5% of pixels (very stealthy, may fail)
γ = 0.10 → 10% of pixels (balanced — common default)
γ = 0.20 → 20% of pixels (more room, less stealthy)
γ = 1.00 → All pixels allowed (no budget constraint)
```

**Impact**:
| γ value | Success rate | Stealth |
|---------|-------------|---------|
| Small (0.05) | Lower | Higher |
| Medium (0.10) | Moderate | Moderate |
| Large (0.20+) | Higher | Lower |

### 3. Clip Bounds — Valid Pixel Range

Keeps pixel values in valid range after modification.

```
clip_min = 0.0  → Pixels can't go below 0 (black)
clip_max = 1.0  → Pixels can't go above 1 (white)
```

For images normalized to [-1, 1]:
```
clip_min = -1.0
clip_max = 1.0
```

### 4. Target Class Selection Strategy

Which class to target affects success rate:

```python
# Strategy 1: Fixed target (attack all images to one class)
target = 3  # Everything becomes "3"

# Strategy 2: Next class (simple rotation)
target = (true_label + 1) % num_classes

# Strategy 3: Most likely misclassification (easiest attack)
probs = model(image).softmax(dim=1)
probs[0, true_label] = 0  # exclude true class
target = probs.argmax(dim=1)  # pick class with highest prob after true

# Strategy 4: Least likely class (hardest attack — stress test)
target = probs.argmin(dim=1)
```

## Configuration Experiments

### Experiment: θ direction matters

```
Image of "7", target class "1":
  θ = +1.0 → Success in 8 pixels  (adding white strokes)
  θ = -1.0 → Success in 22 pixels (removing strokes is harder here)

Image of "8", target class "0":
  θ = +1.0 → Failed (adding white doesn't help)
  θ = -1.0 → Success in 6 pixels  (erasing the middle of 8 → 0!)
```

**Lesson**: The best θ depends on what visual transformation is needed.

### Experiment: γ vs Success Rate

```
γ = 0.01 → ASR: 12%  (too restrictive)
γ = 0.05 → ASR: 45%
γ = 0.10 → ASR: 73%
γ = 0.15 → ASR: 81%
γ = 0.20 → ASR: 86%  (diminishing returns beyond this)
```

## Recommended Starting Configuration

```python
config = {
    'theta': 1.0,         # Start with maximum perturbation
    'gamma': 0.1,         # 10% pixel budget
    'clip_min': 0.0,      # Standard image range
    'clip_max': 1.0,
    'target': 'next',     # Or pick based on your goal
}
```

Then iterate:
1. Run batch evaluation with defaults
2. If ASR is low → increase γ or try both θ directions
3. If attack is too visible → decrease θ magnitude
4. If targeting specific class → try "most likely" strategy

## Key Takeaways

- **θ (theta)** controls perturbation magnitude and direction
- **γ (gamma)** controls the pixel budget (stealth vs success tradeoff)
- The **best θ direction** depends on the specific source→target class pair
- Target class strategy affects difficulty: "most likely" is easiest, "least likely" is hardest
- Start with aggressive settings, then dial back for stealth
