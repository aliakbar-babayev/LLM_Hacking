# Single-Pixel Attack Fundamentals

> Back to [[00_JSMA_Index]] | Previous: [[03_Saliency_and_Search_Space]]

## What is Single-Pixel JSMA?

In single-pixel mode, JSMA modifies **one pixel per iteration**. This is the simplest variant — each step picks the single most impactful pixel and changes it.

## The Attack Parameters

| Parameter | Meaning | Typical Value |
|-----------|---------|---------------|
| `theta (θ)` | How much to change the pixel | +1.0 (maximize) or -1.0 (minimize) |
| `gamma (γ)` | Max fraction of pixels to modify | 0.1 (10% of pixels) |
| `target_class` | Which class to force | Any valid class |
| `clip_min` | Minimum pixel value | 0.0 |
| `clip_max` | Maximum pixel value | 1.0 |

### Theta (θ) — Perturbation Direction

Theta decides whether we **increase** or **decrease** pixel values:

```
θ = +1.0 → Push selected pixels toward maximum (make them brighter)
θ = -1.0 → Push selected pixels toward minimum (make them darker)
```

**Which to use?** It depends on the image. Usually:
- θ = +1 works when adding bright features helps (adding strokes to make a 1 look like 7)
- θ = -1 works when removing features helps (erasing strokes)

### Gamma (γ) — Attack Budget

Gamma limits how many pixels you can touch:

```
max_pixels_to_modify = γ × total_pixels

Example: 28×28 image (784 pixels), γ = 0.1
max_pixels = 0.1 × 784 = 78 pixels

If 78 pixels are modified without success → attack fails
```

## Single-Pixel Selection

Each iteration:

```python
# 1. Compute Jacobian at current (modified) image
jacobian = compute_jacobian(model, current_image)

# 2. Build saliency map (only over search space)
saliency = compute_saliency_map(jacobian, target_class, search_space)

# 3. Pick the ONE pixel with highest saliency
best_pixel = saliency.argmax()

# 4. Modify that pixel
current_image[best_pixel] += theta  # add theta
current_image[best_pixel] = clip(current_image[best_pixel], clip_min, clip_max)

# 5. Remove from search space
search_space[best_pixel] = False
```

## Why "Single-Pixel" is Simple but Limited

### Advantages
- Easy to understand and implement
- Each step is interpretable (you know exactly which pixel and why)
- Minimal computation per step

### Disadvantages
- **Greedy bias**: Picks the best pixel individually, but maybe two mediocre pixels together would be better
- **Slower convergence**: May need more total iterations
- **Misses synergies**: Two pixels might work powerfully together but neither is strong alone

This limitation is why **pairwise** attacks exist (covered in [[08_Pairwise_Saliency]]).

## Example Walkthrough

Attacking a digit "7" to be classified as "3":

```
Iteration 1:
  Jacobian computed → Saliency map built
  Pixel (12, 14) has highest saliency = 0.95
  Set pixel (12, 14) = 1.0 (was 0.3)
  Model still says "7" with 0.85 confidence
  
Iteration 2:
  Recompute Jacobian (image changed!)
  Pixel (15, 10) has highest saliency = 0.82
  Set pixel (15, 10) = 1.0 (was 0.0)
  Model still says "7" with 0.71 confidence (dropping!)
  
...

Iteration 12:
  Pixel (8, 20) modified
  Model now says "3" with 0.52 confidence → SUCCESS!
  Only 12 pixels changed out of 784 (1.5%)
```

## Key Takeaways

- Single-pixel JSMA modifies **one pixel per iteration**
- `θ` controls direction (brighten or darken), `γ` controls budget
- It's **greedy** — always picks the individually best pixel
- Simple and interpretable, but may miss pixel pair synergies
