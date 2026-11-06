# Jacobian and Gradients

> Back to [[00_JSMA_Index]] | Previous: [[01_JSMA_Fundamentals]]

## Why Do We Need Gradients?

Gradients tell us: **"If I change this input pixel by a tiny amount, how much does each output change?"**

This is exactly what JSMA needs — it wants to find pixels where a small change causes a big shift toward the target class.

## Gradient — The Building Block

### What is a Gradient?
A gradient is just a **derivative** — it measures the rate of change.

For a model with one output and one input:
```
gradient = ∂output / ∂input

If gradient is +2.5:
  → Increasing this input by 1 increases the output by ~2.5
  
If gradient is -1.0:
  → Increasing this input by 1 decreases the output by ~1.0
```

### For Neural Networks
A neural network classifier has:
- **Many inputs** (e.g., 784 pixels for a 28×28 image)
- **Many outputs** (e.g., 10 class probabilities for digits 0-9)

So we need the gradient of *each output* with respect to *each input*.

## The Jacobian Matrix

The Jacobian is simply **all gradients organized into a matrix**.

### Structure
```
For a model F with:
  - n inputs (pixels): x₁, x₂, ..., xₙ
  - m outputs (classes): F₁, F₂, ..., Fₘ

The Jacobian J is an m × n matrix:

         x₁        x₂        x₃    ...   xₙ
F₁  [ ∂F₁/∂x₁  ∂F₁/∂x₂  ∂F₁/∂x₃  ...  ∂F₁/∂xₙ ]
F₂  [ ∂F₂/∂x₁  ∂F₂/∂x₂  ∂F₂/∂x₃  ...  ∂F₂/∂xₙ ]
...
Fₘ  [ ∂Fₘ/∂x₁  ∂Fₘ/∂x₂  ∂Fₘ/∂x₃  ...  ∂Fₘ/∂xₙ ]
```

### Reading the Jacobian

Each **row** = one output class. It tells you how sensitive that class is to each pixel.

Each **column** = one input pixel. It tells you how that pixel affects all classes.

### Example (Digit Classifier)

```
Pixel #42 column in the Jacobian:

  Class "0": -0.1   (increasing pixel 42 slightly decreases P("0"))
  Class "1": +0.0   (no effect on P("1"))
  Class "3": +0.8   (increasing pixel 42 strongly increases P("3"))  ← target!
  Class "7": -0.5   (increasing pixel 42 decreases P("7"))  ← source
  ...
```

This tells JSMA: "Pixel #42 is useful — it increases the target class and decreases the source class."

## Computing the Jacobian in PyTorch

```python
import torch

def compute_jacobian(model, input_tensor):
    input_tensor.requires_grad_(True)
    output = model(input_tensor)
    
    num_classes = output.shape[1]
    jacobian = []
    
    for i in range(num_classes):
        model.zero_grad()
        # Select the i-th output
        output[0, i].backward(retain_graph=True)
        # Gradient of class i w.r.t. all inputs
        jacobian.append(input_tensor.grad.data.clone())
        input_tensor.grad.data.zero_()
    
    # Stack into matrix: (num_classes, num_pixels)
    return torch.stack(jacobian)
```

**What this does step by step:**
1. Run the input through the model (forward pass)
2. For each output class, compute the gradient of that class w.r.t. all input pixels (backward pass)
3. Stack all those gradient vectors into the Jacobian matrix

## Key Takeaways

- **Gradient** = how much one output changes when one input changes
- **Jacobian** = the complete map of all gradients (all outputs × all inputs)
- JSMA reads the Jacobian to find pixels that **increase the target class** and **decrease other classes**
- Computing the Jacobian requires `num_classes` backward passes (one per class)
- This is why JSMA is a **white-box** attack — you need model internals for backpropagation

## Intuition Check

Think of the Jacobian as a **sensitivity report**:
> "Dear attacker, here's exactly how sensitive each of my predictions is to each pixel in the image. Sincerely, the model."

JSMA reads this report and picks the most impactful pixels to modify.
