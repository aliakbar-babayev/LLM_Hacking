# Proximal Operators and FISTA Framework

## The Problem

EAD's objective has an L1 term (‖x' - x‖₁). L1 is **not smooth** — it has a sharp corner at zero. Standard gradient descent doesn't handle this well.

## Proximal Operator (Shrinkage)

The fix: after each gradient step, apply a **shrinkage function** that pushes small values to exactly zero.

```
shrink(z, λ) = sign(z) · max(|z| - λ, 0)
```

In plain English:
- If a change is **smaller than λ** → force it to **zero** (kill it)
- If a change is **larger than λ** → shrink it by λ but keep it alive

This is what actually creates sparsity — small perturbations get eliminated.

## FISTA (Fast Iterative Shrinkage-Thresholding Algorithm)

FISTA = a faster version of basic proximal gradient descent.

The loop:
1. Compute gradient of the smooth part (L2 + adversarial loss)
2. Take a gradient step
3. Apply shrinkage (proximal operator) → kills small changes
4. **Momentum step** — use history to accelerate convergence (like Nesterov momentum)
5. Clip to [0, 1] (valid pixel range)

FISTA converges at rate **O(1/k²)** vs O(1/k) for basic method — significantly faster.
