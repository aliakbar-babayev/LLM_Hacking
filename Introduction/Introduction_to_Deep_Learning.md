# 🧠 Introduction to Deep Learning

> **Red Team Mindset:** Deep Learning models are powerful but fragile. They excel at pattern recognition — but they don't *understand* anything. That gap is your playground.

---

## 🔬 Why "Deep"?

"Deep" refers to the **multiple layers** in a neural network. Each layer learns increasingly abstract representations:

```
Input (raw pixels)
   → Layer 1: edges and colors
   → Layer 2: shapes and textures
   → Layer 3: object parts
   → Layer 4: full objects
   → Output: "This is a cat"
```

Traditional ML requires hand-crafted features. Deep Learning **learns the features automatically**.

---

## 🧬 The Artificial Neuron

Inspired by biology but much simpler:

```
Inputs:   x₁, x₂, x₃
Weights:  w₁, w₂, w₃
Bias:     b

z = (w₁·x₁) + (w₂·x₂) + (w₃·x₃) + b   ← weighted sum
a = f(z)                                   ← apply activation function
```

The **activation function** f decides whether (and how strongly) the neuron "fires."

---

## ⚡ Activation Functions

| Function | Formula | Used In |
|----------|---------|---------|
| **ReLU** | max(0, x) | Hidden layers (default choice) |
| **Leaky ReLU** | max(0.01x, x) | Avoids "dead neurons" |
| **Sigmoid** | 1 / (1 + e⁻ˣ) | Binary output layer |
| **Softmax** | eˣⁱ / Σeˣʲ | Multi-class output layer |
| **Tanh** | (eˣ - e⁻ˣ) / (eˣ + e⁻ˣ) | RNNs, some hidden layers |

> **Why ReLU?** It's fast to compute, doesn't saturate for positive values, and works surprisingly well in practice.

---

## 🏗️ Neural Network Architecture

```
Input Layer    →   Hidden Layers   →   Output Layer
  [x₁]              [h₁] [h₂]            [ŷ]
  [x₂]    →→→→     [h₃] [h₄]   →→→→    [ŷ]
  [x₃]              [h₅] [h₆]
```

**Layer Types:**

| Layer | What It Does |
|-------|-------------|
| **Dense / Fully Connected** | Every neuron connects to every neuron in next layer |
| **Convolutional (Conv2D)** | Slides a filter over input to detect local patterns |
| **Pooling** | Downsamples spatial dimensions |
| **Recurrent (LSTM/GRU)** | Maintains memory across time steps |
| **Dropout** | Randomly zeros activations → prevents overfitting |
| **Batch Normalization** | Normalizes layer inputs → speeds up training |
| **Attention** | Learns which parts of input to focus on |

---

## 🔄 How Training Works

### Step 1: Forward Pass
```
Input → Layer 1 → Layer 2 → ... → Output (ŷ)
```

### Step 2: Compute Loss
Measure how wrong the prediction is:

| Task | Loss Function |
|------|--------------|
| Binary Classification | Binary Cross-Entropy |
| Multi-class Classification | Categorical Cross-Entropy |
| Regression | Mean Squared Error (MSE) |

### Step 3: Backpropagation
Compute gradients of loss with respect to every weight using the **chain rule**:

```
∂L/∂w = ∂L/∂ŷ · ∂ŷ/∂z · ∂z/∂w
```

Gradients flow **backward** through the network.

### Step 4: Update Weights

```
w ← w - α · ∂L/∂w     (α = learning rate)
```

---

## 🛠️ Optimizers

| Optimizer | Notes |
|-----------|-------|
| **SGD** | Simple, but slow and sensitive to learning rate |
| **Adam** | Adaptive learning rate, most popular default |
| **AdamW** | Adam + weight decay (better generalization) |
| **RMSprop** | Good for RNNs |

```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
```

---

## 🔧 PyTorch — Building a Neural Network

```python
import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.net(x)

model = MLP(input_dim=784, hidden_dim=256, output_dim=10)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

# Training loop
for epoch in range(20):
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        logits = model(X_batch)
        loss = criterion(logits, y_batch)
        loss.backward()
        optimizer.step()
```

---

## 🏛️ Specialized Architectures

### Convolutional Neural Networks (CNN) — Images
```
Image → [Conv → ReLU → Pool] × N → Flatten → Dense → Output
```
- Learns spatial features (edges, shapes, objects)
- Architectures: AlexNet, VGG, ResNet, EfficientNet

### Recurrent Neural Networks (RNN/LSTM) — Sequences
```
x₁ → [LSTM] → h₁
x₂ → [LSTM] → h₂   (h₁ feeds into next step)
x₃ → [LSTM] → h₃
```
- Maintains state across time steps
- Used for: logs analysis, network traffic sequences, NLP

### Transformers — Attention is All You Need
```
Input tokens → Embeddings → [Self-Attention + FFN] × N → Output
```
- Processes all tokens in parallel (unlike RNN)
- Powers all modern LLMs (GPT, BERT, Claude)

---

## 🛡️ Regularization Techniques

| Technique | How It Works | When to Use |
|-----------|-------------|------------|
| **Dropout** | Randomly zero activations during training | Overfitting |
| **Weight Decay (L2)** | Penalize large weights in loss function | Overfitting |
| **Early Stopping** | Stop training when val loss stops improving | Always |
| **Data Augmentation** | Artificially expand training set | Small datasets |
| **Batch Normalization** | Normalize layer inputs | Almost always |

---

## 🏆 Landmark Architectures Timeline

| Year | Model | Contribution |
|------|-------|-------------|
| 1998 | LeNet | First practical CNN (digit recognition) |
| 2012 | AlexNet | Deep CNN wins ImageNet — start of DL era |
| 2014 | GAN | Generate realistic images |
| 2015 | ResNet | Skip connections — train 100+ layer networks |
| 2017 | Transformer | Attention mechanism — revolutionizes NLP |
| 2018 | BERT | Pre-trained language understanding |
| 2020 | GPT-3 | 175B parameter language model |
| 2020 | ViT | Transformers for vision |
| 2022+ | Diffusion Models | State-of-the-art image generation |

---

## 🔴 Red Team Angle

### Adversarial Examples
Small, **imperceptible perturbations** to inputs that cause the model to misclassify.

```python
# FGSM — Fast Gradient Sign Method (Goodfellow et al., 2014)
loss = criterion(model(x), y_true)
loss.backward()
x_adversarial = x + epsilon * x.grad.sign()
# The model now misclassifies x_adversarial with high confidence
```

### Attack Taxonomy

| Attack | Description | Phase |
|--------|-------------|-------|
| **FGSM** | One-step gradient attack | Evasion |
| **PGD** | Iterative gradient attack (stronger) | Evasion |
| **C&W Attack** | Optimization-based, minimal perturbation | Evasion |
| **Neural Backdoor** | Inject hidden trigger during training | Poisoning |
| **Model Inversion** | Reconstruct training data from model | Privacy |
| **Membership Inference** | Was this sample in training set? | Privacy |
| **Model Stealing** | Clone model via query access | Theft |

### Why DL is Especially Vulnerable
1. **Non-interpretable** — no one fully understands what they learned
2. **Overconfident** — high-confidence predictions on garbage inputs
3. **Brittle** — small distribution shifts break performance
4. **Transferability** — adversarial examples often transfer across models

---

## 🔗 Linked Notes
- [[Introduction_to_Machine_Learning]]
- [[Supervised_Learning_Algorithms]]
- [[Introduction_to_Generative_AI]]

---
*Tags: #DeepLearning #NeuralNetworks #CNN #LSTM #Transformer #PyTorch #AdversarialML #RedTeam*
