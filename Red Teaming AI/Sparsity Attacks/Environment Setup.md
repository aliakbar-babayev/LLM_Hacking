# Environment Setup

## What You Need

- **PyTorch** — for building/loading the model and computing gradients
- **Torchvision** — for datasets (MNIST, CIFAR-10) and pretrained models
- **NumPy** — for array operations
- **Matplotlib** — for visualizing adversarial examples

## Typical Setup

```python
import torch
import torch.nn as nn
import torchvision
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## Key Points

- Load a **pretrained classifier** (the model you're attacking)
- Set model to **eval mode** (`model.eval()`) — we're not training, we're attacking
- Images should be normalized to **[0, 1]** range — this is the "box constraint"
- If the model uses normalization (mean/std), gradients still propagate through it via chain rule
