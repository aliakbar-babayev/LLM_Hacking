# JSMA Fundamentals

> Back to [[00_JSMA_Index]]

## The Big Picture

JSMA (Jacobian-based Saliency Map Approach) was introduced by Papernot et al. in 2016. It's a **targeted adversarial attack** — meaning you don't just want the model to be *wrong*, you want it to predict a *specific wrong class*.

## Key Concepts

### 1. Adversarial Examples
An adversarial example is an input intentionally modified to cause a model to make a mistake, while the modification is **imperceptible** to humans.

```
Original image → Model says "7"  ✓
Modified image → Model says "3"  ✗ (but image still looks like 7 to us)
```

### 2. White-Box vs Black-Box
| Type | What you know | Example |
|------|--------------|---------|
| **White-box** | Full model access (weights, gradients, architecture) | JSMA, FGSM, PGD |
| **Black-box** | Only inputs/outputs | Query-based attacks |

JSMA is a **white-box** attack — it needs to compute gradients through the model.

### 3. Targeted vs Untargeted
| Type | Goal |
|------|------|
| **Targeted** | Force model to predict a *specific* class (e.g., "classify this 7 as a 3") |
| **Untargeted** | Just make the model wrong (any wrong class works) |

JSMA is **targeted** — you pick the class you want the model to mispredict.

### 4. L0 Norm — The "How Many Pixels" Metric
Different attacks limit perturbations differently:
- **L∞ (infinity norm)**: limits the *maximum change* to any single pixel (FGSM, PGD)
- **L2 norm**: limits the *total magnitude* of all changes combined
- **L0 norm**: limits the *number of pixels changed* (JSMA)

JSMA minimizes L0 — it changes as **few pixels as possible**, but each changed pixel can be modified significantly.

### 5. How JSMA Works (High Level)

```
1. Compute the Jacobian matrix (how each output changes w.r.t. each input pixel)
2. Build a saliency map (which pixels matter most for the target class)
3. Pick the most "salient" pixel(s)
4. Modify those pixel(s)
5. Check: did the model change its prediction to target class?
   - Yes → Attack succeeded!
   - No → Go back to step 1 with the modified input
6. Repeat until success or budget (max pixels) exhausted
```

## Why JSMA Matters

- **Sparse attacks** are harder to detect (only a few pixels change)
- Shows that models rely on **specific features** that can be exploited
- Demonstrates that "confidence" doesn't equal robustness
- Foundation for understanding more complex adversarial techniques

## Key Terminology

| Term | Meaning |
|------|---------|
| **Perturbation** | The change applied to the input |
| **Saliency map** | A heatmap showing which pixels matter most |
| **Jacobian** | Matrix of all partial derivatives of outputs w.r.t. inputs |
| **Target class** | The class we want the model to predict |
| **Source class** | The original (correct) class |
| **Adversarial budget** | Maximum number of pixels we're allowed to change |
