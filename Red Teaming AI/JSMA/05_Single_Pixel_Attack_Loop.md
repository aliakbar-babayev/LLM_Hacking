# Single-Pixel Attack Loop

> Back to [[00_JSMA_Index]] | Previous: [[04_Single_Pixel_Attack_Fundamentals]]

## The Full Attack Algorithm

Here's the complete loop from start to finish:

```
┌──────────────────────────────────────────────┐
│           INITIALIZE                          │
│  • Copy original image → current_image        │
│  • Set search_space = all pixels (all True)   │
│  • Set pixels_modified = 0                    │
│  • Set max_pixels = γ × total_pixels          │
└─────────────────────┬────────────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Check: model predicts │──── Yes ──→ SUCCESS ✓
          │ target_class?         │           (return modified image)
          └───────────┬───────────┘
                      │ No
                      ▼
          ┌───────────────────────┐
          │ Check: pixels_modified│──── Yes ──→ FAILURE ✗
          │ ≥ max_pixels?         │           (budget exhausted)
          └───────────┬───────────┘
                      │ No
                      ▼
          ┌───────────────────────┐
          │ Compute Jacobian      │
          │ at current_image      │
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Compute saliency map  │
          │ (only search_space)   │
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Check: any pixel with │──── No ──→ FAILURE ✗
          │ saliency > 0?         │         (no useful pixels left)
          └───────────┬───────────┘
                      │ Yes
                      ▼
          ┌───────────────────────┐
          │ Pick pixel with       │
          │ highest saliency      │
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Modify pixel by θ     │
          │ Clip to [min, max]    │
          │ Remove from search    │
          │ pixels_modified += 1  │
          └───────────┬───────────┘
                      │
                      └──────── Loop back to "Check: model predicts target?"
```

## Three Ways the Loop Ends

| Outcome | Condition | Meaning |
|---------|-----------|---------|
| **Success** | Model predicts target class | Attack worked! |
| **Failure (budget)** | Modified too many pixels | Couldn't fool the model within budget |
| **Failure (stuck)** | No pixels with saliency > 0 | No remaining pixel can help |

## Complete Code

```python
def jsma_single_pixel(model, image, target_class, theta=1.0, gamma=0.1):
    # Initialize
    current_image = image.clone()
    num_pixels = image.numel()
    max_modifications = int(gamma * num_pixels)
    search_space = torch.ones(num_pixels, dtype=torch.bool)
    pixels_modified = 0
    
    while True:
        # Check if attack succeeded
        prediction = model(current_image).argmax(dim=1)
        if prediction == target_class:
            return current_image, True, pixels_modified  # SUCCESS
        
        # Check budget
        if pixels_modified >= max_modifications:
            return current_image, False, pixels_modified  # FAILURE
        
        # Compute Jacobian
        jacobian = compute_jacobian(model, current_image)
        
        # Compute saliency map
        saliency = compute_saliency_map(jacobian, target_class, search_space)
        
        # Check if any valid pixels remain
        if saliency.max() == 0:
            return current_image, False, pixels_modified  # STUCK
        
        # Select best pixel
        best_pixel = saliency.argmax()
        
        # Modify pixel
        flat_image = current_image.view(-1)
        flat_image[best_pixel] += theta
        flat_image[best_pixel] = torch.clamp(flat_image[best_pixel], 0.0, 1.0)
        current_image = flat_image.view(image.shape)
        
        # Update search space
        search_space[best_pixel] = False
        pixels_modified += 1
```

## Why Recompute Every Iteration?

**Question**: Why not compute the Jacobian once and reuse it?

**Answer**: Because the Jacobian changes every time you modify a pixel!

```
Iteration 1: Image = [0.5, 0.3, 0.8, ...]
  Jacobian says pixel #2 is most important
  
Iteration 2: Image = [0.5, 0.3, 1.0, ...]  (pixel #2 changed!)
  The model's gradients are now DIFFERENT
  Maybe pixel #50 is now most important (not #2 anymore)
```

The model's internal activations change with the input, so the gradients (and thus the saliency map) must be recomputed.

## Computational Cost

Each iteration requires:
- 1 forward pass (check prediction)
- `num_classes` backward passes (compute Jacobian)
- 1 saliency map computation

For MNIST (10 classes, 784 pixels):
- Worst case: 78 iterations (γ=0.1) × 11 passes = 858 forward/backward passes
- Typical: ~10-30 iterations to succeed

## Key Takeaways

- The loop has three exit conditions: **success**, **budget exhausted**, **stuck**
- Jacobian is **recomputed every iteration** because the image changes
- The algorithm is greedy and iterative — no guaranteed optimal solution
- Cost grows with number of iterations needed
