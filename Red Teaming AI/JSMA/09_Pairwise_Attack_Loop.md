# Pairwise Attack Loop

> Back to [[00_JSMA_Index]] | Previous: [[08_Pairwise_Saliency]]

## How Pairwise Differs from Single-Pixel Loop

The structure is almost identical to [[05_Single_Pixel_Attack_Loop]], but each iteration modifies **two pixels** instead of one.

## The Pairwise Loop

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
          │ target_class?         │
          └───────────┬───────────┘
                      │ No
                      ▼
          ┌───────────────────────┐
          │ Check: pixels_modified│──── Yes ──→ FAILURE ✗
          │ ≥ max_pixels?         │
          └───────────┬───────────┘
                      │ No
                      ▼
          ┌───────────────────────┐
          │ Compute Jacobian      │
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Compute PAIRWISE      │  ← 2D matrix instead of 1D vector
          │ saliency map          │
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Any pair with         │──── No ──→ FAILURE ✗
          │ saliency > 0?         │
          └───────────┬───────────┘
                      │ Yes
                      ▼
          ┌───────────────────────┐
          │ Pick PAIR (p,q) with  │  ← Two pixels at once!
          │ highest saliency      │
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Modify BOTH p and q   │
          │ Clip to [min, max]    │
          │ Remove both from      │
          │   search space        │
          │ pixels_modified += 2  │
          └───────────┬───────────┘
                      │
                      └──────── Loop back to check
```

## Code Implementation

```python
def jsma_pairwise(model, image, target_class, theta=1.0, gamma=0.1):
    current_image = image.clone()
    num_pixels = image.numel()
    max_modifications = int(gamma * num_pixels)
    search_space = torch.ones(num_pixels, dtype=torch.bool)
    pixels_modified = 0
    
    while True:
        # Check success
        prediction = model(current_image).argmax(dim=1)
        if prediction == target_class:
            return current_image, True, pixels_modified
        
        # Check budget (need room for 2 more pixels)
        if pixels_modified + 1 >= max_modifications:
            return current_image, False, pixels_modified
        
        # Compute Jacobian and pairwise saliency
        jacobian = compute_jacobian(model, current_image)
        saliency = pairwise_saliency_fast(jacobian, target_class, search_space)
        
        # Check if any valid pair exists
        if saliency.max() == 0:
            return current_image, False, pixels_modified
        
        # Find best pair
        flat_idx = saliency.argmax()
        p = flat_idx // num_pixels
        q = flat_idx % num_pixels
        
        # Modify both pixels
        flat_image = current_image.view(-1)
        flat_image[p] += theta
        flat_image[q] += theta
        flat_image[p] = torch.clamp(flat_image[p], 0.0, 1.0)
        flat_image[q] = torch.clamp(flat_image[q], 0.0, 1.0)
        current_image = flat_image.view(image.shape)
        
        # Update search space
        search_space[p] = False
        search_space[q] = False
        pixels_modified += 2
```

## Key Differences from Single-Pixel

| Aspect | Single-Pixel | Pairwise |
|--------|-------------|----------|
| Pixels per iteration | 1 | 2 |
| Saliency computation | O(n) | O(n²) |
| Budget consumption | +1 per iter | +2 per iter |
| Total iterations | More | Fewer (~half) |
| Finding best candidate | argmax of vector | argmax of matrix → convert to (row, col) |
| Budget check | `pixels_modified >= max` | `pixels_modified + 1 >= max` (need room for 2) |

## Finding the Best Pair from the Matrix

The saliency matrix is 2D, so finding the best pair requires converting a flat index:

```python
# Saliency is an n×n matrix
# argmax gives a single flat index
flat_idx = saliency.argmax()

# Convert to row, col
p = flat_idx // n    # row = first pixel
q = flat_idx % n     # col = second pixel

# Now modify pixels p and q
```

## Convergence Comparison

```
Single-pixel attack on "7" → "3":
  Iter 1: modify 1 pixel   → still "7" (conf 0.89)
  Iter 2: modify 1 pixel   → still "7" (conf 0.81)
  ...
  Iter 12: modify 1 pixel  → "3" (conf 0.52)  ← 12 iterations, 12 pixels

Pairwise attack on "7" → "3":
  Iter 1: modify 2 pixels  → still "7" (conf 0.78)
  Iter 2: modify 2 pixels  → still "7" (conf 0.61)
  ...
  Iter 5: modify 2 pixels  → "3" (conf 0.58)   ← 5 iterations, 10 pixels
```

Fewer iterations AND fewer total pixels modified (because pairs are chosen better).

## Key Takeaways

- Pairwise loop modifies **2 pixels per iteration** instead of 1
- Uses **argmax on a 2D matrix** to find the best pair
- Typically converges in **fewer iterations** and **fewer total pixels**
- Budget check must ensure room for 2 more pixels
- Same three exit conditions as single-pixel: success, budget, stuck
