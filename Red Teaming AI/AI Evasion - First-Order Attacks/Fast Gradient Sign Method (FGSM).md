
Machine learning models (like image classifiers) can be fooled by **adversarial examples**: inputs with tiny, often invisible changes that make the model give a wrong answer. A panda image plus carefully crafted noise still looks like a panda to you, but the model says “gibbon.”

**FGSM (Fast Gradient Sign Method)** is the simplest attack for creating these. Think of it as the “hello world” of adversarial ML, like a basic payload before you move on to advanced exploits.

**Red team mapping:**

|ML concept|Security analogy|
|---|---|
|Model|The target system|
|Adversarial example|The crafted exploit input|
|Epsilon (ε)|Your “stealth budget”: how much you may change the input before it gets noticed|
|Gradient|Information leak that tells you which direction hurts the target most|
|White-box attack|You have the source code/internals (FGSM requires model access)|

---
### 1. FGSM

**Definition:** An attack that adds a tiny perturbation to an input, pushing it in the direction that makes the model’s error as large as possible, in a single step.

**How it works:**

1. Feed the image to the model and measure how wrong the prediction is (the **loss**).
2. Compute the **gradient**: for every pixel, which direction (brighter or darker) increases the loss the most?
3. Keep only the **sign** of that gradient (+1 or −1 per pixel). You don’t care how much, only which way.
4. Nudge every pixel by ε in that direction.


### 2.FGSM Setup

**Definition:** The preparation before attacking: everything you need in place.

Typically:

- **Load a pretrained model** (the victim), e.g., a classifier trained on MNIST or ImageNet.
- **Load a dataset** of test images with their correct labels.
- **Pick a loss function** (usually cross-entropy), since the gradient comes from it.
- **Choose ε** (the perturbation budget).
- **Put the model in eval mode** (disables training-only behavior like dropout).
- **Enable gradients on the input** (`x.requires_grad = True`), so the framework computes ∇ₓ.


### 3. Normalization

**Definition:** Models usually don’t take raw pixels (0–255). Inputs are scaled and standardized first, e.g., divided by 255, then `(pixel − mean) / std`.

**Why it matters for the attack:**

- Your ε is meant to be in **real image space** (e.g., 3% change in brightness), because that’s what determines whether a human would notice.
- If the model works in normalized space, applying ε there gives you a different, wrong effective perturbation size.
- You must handle the conversion correctly: **denormalize → perturb → clip to valid range → renormalize**.
- After perturbing, **clip** the result to [0, 1] so it’s still a valid image.



### 4. Core Implementation

**Definition:** The actual attack function in code. The logic is short:

```
def fgsm_attack(model, x, y, epsilon):
    x.requires_grad = True
    output = model(x)                  # forward pass
    loss = F.cross_entropy(output, y)  # how wrong is it?
    model.zero_grad()
    loss.backward()                    # compute gradients
    grad_sign = x.grad.sign()          # direction only
    x_adv = x + epsilon * grad_sign    # nudge the pixels
    x_adv = torch.clamp(x_adv, 0, 1)   # keep a valid image
    return x_adv
```

Steps: **forward pass → loss → backward pass → sign → perturb → clip**. That’s the whole attack.

### 5. Evaluation Metrics

**Definition:** Numbers that tell you how well the attack worked.

- **Clean accuracy:** model accuracy on normal images (the baseline).
- **Adversarial (robust) accuracy:** accuracy on attacked images. Lower means a more effective attack.
- **Attack success rate:** the percentage of images that were correctly classified before and misclassified after the attack.
- **Accuracy vs ε curve:** accuracy as ε grows. Larger ε gives a stronger attack but is more visible.
- **Perturbation size:** measured with norms (L∞, L2) to confirm you stayed within budget.
- **Confidence change:** how confident the model is in its wrong answer.

_Analogy:_ Like reporting exploit success rate and detection rate in a pentest.


### 6. Visualization

**Definition:** Plotting results so you can see what the attack did.

Common plots:

- **Side-by-side:** original image | perturbation (amplified so it’s visible) | adversarial image, with predicted labels and confidences.
- **Accuracy vs ε graph:** shows how quickly the model breaks down.
- **Grid of examples** at different ε values, showing where noise becomes visible to humans.

This helps you understand the trade-off between **attack success** and **stealthiness**.

---

### 7. Targeted FGSM

**Definition:** Standard FGSM is **untargeted**: you just want _any_ wrong answer. **Targeted FGSM** forces the model to predict a _specific_ wrong class you choose (e.g., make a “stop sign” be classified as “speed limit 45”).

**The change:** instead of _increasing_ the loss for the true label, you _decrease_ the loss for your target label

_Analogy:_ Untargeted is “crash the service.” Targeted is “get the service to do exactly what I want.”



### 8. I-FGSM (Iterative FGSM, also called BIM)

**Definition:** Instead of one big step, take **many small steps**, recomputing the gradient each time.

**Why it’s better:** FGSM assumes the loss surface is a straight line, which it isn’t. One big jump can overshoot. Small steps follow the curved surface more accurately, so I-FGSM finds stronger adversarial examples with less visible noise.

_Analogy:_ FGSM is a single exploit attempt. I-FGSM is iterative fuzzing: probe, adjust, probe again, getting closer to a working payload each round.


### 9. I-FGSM Implementation

**Definition:** The code version of the iterative attack, which wraps FGSM in a loop.

Key implementation details:

- **Number of steps and α:** a common choice is α = ε / steps, or a bit larger.
- **Two clips each iteration:** one for the ε budget, one for valid pixel range.
- **`.detach()`** so gradients don’t accumulate across iterations.
- Optionally, **early stopping** once the model is fooled.