

## The Three Building Blocks

### 1. Gradient of the Smooth Part

```python
# Forward pass through model
logits = model(x_adv)
# Compute CW adversarial loss
adv_loss = c * cw_loss(logits, true_label, target_label)
# Add L2 penalty
l2_loss = torch.sum((x_adv - x_orig) ** 2)
# Total smooth loss
smooth_loss = adv_loss + l2_loss
# Backward pass → gradient
smooth_loss.backward()
grad = x_adv.grad
```

### 2. Gradient Step

```python
# Move in the negative gradient direction (minimize loss)
y = x_adv - step_size * grad
```

### 3. Shrinkage (Proximal Operator for L1)

```python
def shrink(z, x_orig, beta):
    delta = z - x_orig
    # Kill small changes, shrink large ones
    delta = torch.sign(delta) * torch.clamp(torch.abs(delta) - beta, min=0)
    return x_orig + delta
```

## Putting It Together

Each FISTA iteration:
1. Compute gradient → step → shrink → clip to [0,1]
2. Apply momentum (accelerated step using previous iterate)
3. Check if misclassification achieved
