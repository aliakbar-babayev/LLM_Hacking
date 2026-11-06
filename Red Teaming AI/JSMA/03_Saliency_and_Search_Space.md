# Saliency and Search Space

> Back to [[00_JSMA_Index]] | Previous: [[02_Jacobian_and_Gradients]]

## What is Saliency?

Saliency means **importance**. In JSMA, a pixel's saliency score answers:

> "How useful is modifying this pixel for making the model predict the target class?"

A high saliency pixel is one where changing it:
1. **Increases** the probability of the **target class** (the class we want)
2. **Decreases** the probability of **all other classes**

## The Saliency Map Formula

For each pixel `p`, the saliency score is:

```
Step 1: Get from the Jacobian:
  ∂F_target / ∂x_p  →  How much the TARGET class increases when pixel p changes
  Σ(∂F_other / ∂x_p) →  How much ALL OTHER classes change (summed)

Step 2: Apply the saliency rule:

  If ∂F_target/∂x_p > 0  AND  Σ(∂F_other/∂x_p) < 0:
      saliency(p) = ∂F_target/∂x_p × |Σ(∂F_other/∂x_p)|
  Else:
      saliency(p) = 0
```

### Breaking This Down

| Condition | What it means |
|-----------|--------------|
| `∂F_target/∂x_p > 0` | Changing this pixel increases the target class probability |
| `Σ(∂F_other/∂x_p) < 0` | Changing this pixel decreases all other classes combined |
| Both true | This pixel is **useful** — it pushes classification toward the target |
| Either false | This pixel is **not useful** — set saliency to 0 |

### Why Multiply?
The multiplication creates a score that rewards pixels that are good at **both** jobs simultaneously:
- Strongly increasing the target ✓
- Strongly decreasing others ✓

A pixel that only does one job (increases target but also increases another class) gets saliency = 0.

## Search Space

The search space is the **set of pixels JSMA is allowed to modify**. Not every pixel is a candidate.

### Pixels Excluded from the Search Space

```
A pixel is REMOVED from the search space if:
1. It has already been modified (don't touch the same pixel twice)
2. It has hit the boundary (pixel value is already at max/min)
3. It has saliency = 0 (not useful for the attack)
```

### Why Limit the Search Space?

- **Efficiency**: Fewer pixels to evaluate each iteration
- **Stealth**: Modified pixels are tracked; don't over-perturb
- **Convergence**: Removing zero-saliency pixels speeds up the search

### Search Space Shrinks Over Time

```
Iteration 1: Search space = all 784 pixels
  → Modify pixel #42 → Remove it
Iteration 2: Search space = 783 pixels
  → Modify pixel #199 → Remove it
Iteration 3: Search space = 782 pixels
  ...and so on
```

## Putting It Together

```
                    Input Image
                         │
                         ▼
               ┌─────────────────┐
               │  Compute Jacobian│
               └────────┬────────┘
                         │
                         ▼
               ┌─────────────────┐
               │ Build Saliency  │  ← For each pixel in search space
               │      Map        │
               └────────┬────────┘
                         │
                         ▼
               ┌─────────────────┐
               │ Pick pixel with │  ← Highest saliency score
               │ max saliency    │
               └────────┬────────┘
                         │
                         ▼
               ┌─────────────────┐
               │ Modify pixel &  │  ← Remove from search space
               │ update search   │
               │ space           │
               └─────────────────┘
```

## Code Intuition

```python
def compute_saliency_map(jacobian, target_class, search_space):
    # Gradient of target class w.r.t. all pixels
    target_grad = jacobian[target_class]  # shape: (num_pixels,)
    
    # Sum of gradients of ALL OTHER classes
    other_grad = jacobian.sum(dim=0) - target_grad  # shape: (num_pixels,)
    
    # Saliency conditions
    increasing_target = target_grad > 0
    decreasing_others = other_grad < 0
    in_search_space = search_space  # boolean mask
    
    # Saliency score (0 if conditions not met)
    valid = increasing_target & decreasing_others & in_search_space
    saliency = torch.zeros_like(target_grad)
    saliency[valid] = target_grad[valid] * torch.abs(other_grad[valid])
    
    return saliency
```

## Key Takeaways

- **Saliency** = how useful a pixel is for the attack (increase target + decrease others)
- Pixels that don't meet both criteria get **zero saliency** (filtered out)
- **Search space** starts as all pixels, shrinks as pixels are used or hit boundaries
- The attack is **greedy** — always picks the highest-saliency pixel each iteration
