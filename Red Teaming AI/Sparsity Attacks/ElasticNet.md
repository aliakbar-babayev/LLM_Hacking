# ElasticNet (EAD) Attack

EAD = ElasticNet Attack to DNNs. It fools a model by changing **as few pixels as possible** (sparsity).

## Core Idea

Instead of changing every pixel a tiny bit (like FGSM), EAD picks a **small number of pixels** and changes them significantly.

## The Objective

```
min  c·f(x') + ‖x' - x‖₂² + β·‖x' - x‖₁
```

Three goals balanced together:
- **c·f(x')** → make the model misclassify (adversarial loss)
- **‖x' - x‖₂²** → keep total change small (L2 penalty)
- **β·‖x' - x‖₁** → push most changes to zero (L1 creates sparsity)

**β** controls sparsity: higher β = fewer pixels changed.
**c** controls attack strength: found via binary search.

## Why "ElasticNet"?

Same idea as ElasticNet regression — combines L1 (Lasso) + L2 (Ridge). L1 forces most values to exactly zero. L2 keeps the non-zero changes smooth.

## Result

A small set of large edits instead of many tiny ones. Most of the image stays untouched → harder for defenses that look for global noise.
