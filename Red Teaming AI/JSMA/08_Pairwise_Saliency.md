# Pairwise Saliency

> Back to [[00_JSMA_Index]] | Previous: [[07_Single_Pixel_Configuration]]

## The Problem with Single-Pixel

Single-pixel JSMA is **greedy** — it picks the best individual pixel. But what if two pixels are mediocre alone but **powerful together**?

```
Single-pixel view:
  Pixel A saliency: 0.3  (mediocre)
  Pixel B saliency: 0.2  (weak)
  Pixel C saliency: 0.5  (best — pick this one)

Pairwise view:
  Pair (A, B) saliency: 0.9  ← These two TOGETHER are amazing!
  Pair (A, C) saliency: 0.6
  Pair (B, C) saliency: 0.5
```

Single-pixel would pick C. Pairwise picks (A, B) — a much better choice.

## Pairwise Saliency Formula

Instead of evaluating one pixel at a time, evaluate **pairs of pixels** (p, q):

```
For pixel pair (p, q):

  target_effect = ∂F_target/∂x_p + ∂F_target/∂x_q
  other_effect  = Σ(∂F_other/∂x_p) + Σ(∂F_other/∂x_q)

  If target_effect > 0 AND other_effect < 0:
      saliency(p, q) = target_effect × |other_effect|
  Else:
      saliency(p, q) = 0
```

### Comparison to Single-Pixel

| | Single-Pixel | Pairwise |
|---|---|---|
| **Evaluates** | Individual pixels | Pairs of pixels |
| **Saliency** | 1D vector (length n) | 2D matrix (n × n) |
| **Picks** | 1 pixel per iteration | 2 pixels per iteration |
| **Search space** | O(n) per iteration | O(n²) per iteration |
| **Quality** | Good | Better (captures synergies) |

## Building the Pairwise Saliency Map

```python
def compute_pairwise_saliency(jacobian, target_class, search_space):
    num_pixels = jacobian.shape[1]
    
    # Gradients for target class
    target_grad = jacobian[target_class]  # shape: (num_pixels,)
    
    # Sum of gradients for all other classes
    other_grad = jacobian.sum(dim=0) - target_grad  # shape: (num_pixels,)
    
    # Pairwise saliency matrix
    saliency = torch.zeros(num_pixels, num_pixels)
    
    # For each pair (p, q) where p < q:
    for p in range(num_pixels):
        if not search_space[p]:
            continue
        for q in range(p + 1, num_pixels):
            if not search_space[q]:
                continue
            
            # Combined effect of modifying BOTH pixels
            t_effect = target_grad[p] + target_grad[q]
            o_effect = other_grad[p] + other_grad[q]
            
            if t_effect > 0 and o_effect < 0:
                saliency[p, q] = t_effect * abs(o_effect)
    
    return saliency
```

## Why Pairwise is Better

### Synergy Example

Consider two pixels in a "7" → "3" attack:

```
Pixel at top of the "7" (position A):
  - Modifying it alone slightly opens the top → partial "3" shape
  - ∂F_target/∂x_A = 0.2 (weak alone)

Pixel at the middle of the "7" (position B):
  - Modifying it alone adds a tiny middle stroke
  - ∂F_target/∂x_B = 0.15 (weak alone)

Together (A + B):
  - Open top + middle stroke → looks much more like "3"
  - Combined effect > sum of individual effects due to nonlinear model behavior
```

### Computational Cost Trade-off

| | Single-Pixel | Pairwise |
|---|---|---|
| Candidates per iter | n | n(n-1)/2 |
| For 784 pixels | 784 | 306,936 |
| Pixels modified per iter | 1 | 2 |
| Total iterations needed | More | Fewer |

Pairwise does more work per iteration but needs fewer iterations — often a net win.

## Optimized Pairwise Computation

The naive nested loop is slow. Vectorized approach:

```python
def pairwise_saliency_fast(jacobian, target_class, search_space):
    target_grad = jacobian[target_class]
    other_grad = jacobian.sum(dim=0) - target_grad
    
    # Mask invalid pixels
    target_grad = target_grad * search_space.float()
    other_grad = other_grad * search_space.float()
    
    # Outer sums for all pairs
    # target_effect[p,q] = target_grad[p] + target_grad[q]
    target_effect = target_grad.unsqueeze(0) + target_grad.unsqueeze(1)
    other_effect = other_grad.unsqueeze(0) + other_grad.unsqueeze(1)
    
    # Apply conditions
    valid = (target_effect > 0) & (other_effect < 0)
    saliency = torch.where(valid, target_effect * other_effect.abs(), torch.zeros_like(target_effect))
    
    # Zero out diagonal (can't pick same pixel twice)
    saliency.fill_diagonal_(0)
    # Keep only upper triangle (avoid duplicate pairs)
    saliency = torch.triu(saliency, diagonal=1)
    
    return saliency
```

## Key Takeaways

- Pairwise JSMA evaluates **pairs of pixels** instead of individual ones
- Captures **synergies** between pixels that single-pixel misses
- Produces a **2D saliency matrix** instead of a 1D vector
- More compute per iteration but typically fewer total iterations
- Almost always produces **better attack results** than single-pixel
