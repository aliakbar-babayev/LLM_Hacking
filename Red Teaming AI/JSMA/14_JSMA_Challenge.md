# JSMA Challenge

> Back to [[00_JSMA_Index]] | Previous: [[13_Aggregate_Analysis]]

## Putting It All Together

The JSMA Challenge is the interactive/practical exercise from the HTB module. Here's a framework for approaching it.

## General Approach for JSMA Challenges

### Step 1: Understand the Setup

```python
# Typical challenge setup:
# - A pre-trained model (PyTorch)
# - A dataset (usually MNIST or similar)
# - A specific attack goal (e.g., "make all 7s classify as 3")
# - Constraints (max pixels, specific theta, etc.)

import torch
import torch.nn as nn

# Load model
model = load_model('model.pth')
model.eval()

# Load dataset
dataset = load_dataset()
```

### Step 2: Implement Core Functions

You need these four functions:

```python
# 1. Jacobian computation
def compute_jacobian(model, input_tensor):
    """Returns (num_classes, num_pixels) matrix."""
    ...

# 2. Saliency map (single or pairwise)
def compute_saliency(jacobian, target_class, search_space):
    """Returns saliency scores for candidate pixels/pairs."""
    ...

# 3. Attack loop
def jsma_attack(model, image, target, theta, gamma):
    """Returns (adversarial_image, success, pixels_modified)."""
    ...

# 4. Evaluation
def evaluate(model, dataset, attack_fn, target):
    """Returns metrics dict."""
    ...
```

### Step 3: Run and Validate

```python
# Run attack on a single image first
test_image, test_label = dataset[0]
adv_image, success, n_pixels = jsma_attack(model, test_image, target_class=3)

print(f"Success: {success}")
print(f"Pixels modified: {n_pixels}")
print(f"Original prediction: {model(test_image).argmax()}")
print(f"Adversarial prediction: {model(adv_image).argmax()}")

# Verify visually
plot_comparison(test_image, adv_image)
```

### Step 4: Scale Up

```python
# Run batch evaluation
results = evaluate(model, dataset, jsma_attack, target_class=3)
print(f"ASR: {results['success']/results['total']:.1%}")
print(f"Avg pixels: {sum(results['pixels_modified'])/len(results['pixels_modified']):.1f}")
```

## Common Pitfalls

### 1. Forgetting to set model to eval mode
```python
model.eval()  # CRITICAL — batch norm and dropout behave differently in train mode
```

### 2. Not cloning the input
```python
current_image = image.clone()  # Don't modify the original!
```

### 3. Wrong gradient computation
```python
# Must zero gradients between backward passes
input_tensor.grad.data.zero_()
```

### 4. Forgetting retain_graph
```python
output[0, i].backward(retain_graph=True)  # Need this for multiple backward passes
```

### 5. Not handling the search space correctly
```python
# Remove pixels that hit boundaries too
if flat_image[best_pixel] >= clip_max or flat_image[best_pixel] <= clip_min:
    search_space[best_pixel] = False
```

## Challenge Strategy

1. **Start simple**: Get single-pixel working on one image
2. **Verify correctness**: Check that Jacobian values make sense (gradients should be small, not NaN or inf)
3. **Test both θ directions**: Try +1 and -1, see which works better
4. **Scale to batch**: Once single image works, run on many
5. **Try pairwise**: If single-pixel ASR is low, pairwise will improve it
6. **Analyze results**: Build the attack matrix, find patterns

## Debugging Checklist

- [ ] Model in eval mode?
- [ ] Input requires_grad set?
- [ ] Gradients zeroed between backward passes?
- [ ] retain_graph=True used?
- [ ] Pixel values clipped to valid range?
- [ ] Search space updated correctly?
- [ ] Not attacking images already in target class?
- [ ] Budget (gamma) not too restrictive?

## Key Takeaways

- Approach the challenge **incrementally** — single image first, then batch
- The four core functions (Jacobian, saliency, attack loop, evaluation) are your building blocks
- Most debugging issues are gradient-related — watch for NaN, zeroing, and retain_graph
- Always verify with a visual comparison before trusting metrics
- Try both θ=+1 and θ=-1 — the right direction depends on the class pair
