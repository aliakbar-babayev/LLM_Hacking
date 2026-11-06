# Loss Gradients and Optimization

## What Gets Optimized

EAD solves: `min c·f(x') + ‖x'-x‖₂² + β·‖x'-x‖₁`

The gradient only applies to the **smooth** parts:
- **c·f(x')** — adversarial loss (differentiable)
- **‖x'-x‖₂²** — L2 distance (differentiable)

The **L1 term** is NOT differentiable at zero → handled by the proximal/shrinkage step, not gradient.

## Gradient Flow

```
Input pixels → Model layers → Logits → CW Loss
                                         ↓
                                    Backprop
                                         ↓
                              Gradient w.r.t. pixels
```

The gradient tells us: "which direction should each pixel move to maximize misclassification while staying close to the original?"

## Step Size

- Too large → overshoots, unstable
- Too small → too slow to converge
- FISTA handles this with momentum — converges faster without needing aggressive step sizes

## Key Insight

We're doing gradient descent on the **input** (pixels), not the weights. The model is frozen. Same math as training, different target.
