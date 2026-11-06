# Sparsity Analysis

## What We're Analyzing

After running EAD, we examine HOW sparse the perturbation actually is and what it reveals about the model.

## β (Beta) vs Sparsity

| β Value | Effect |
|---------|--------|
| β = 0 | No L1 penalty → behaves like CW L2 attack (not sparse) |
| β = 0.001 | Light sparsity → many pixels still change |
| β = 0.01 | Moderate → noticeable sparsity |
| β = 0.1 | Aggressive → very few pixels change |
| β = 1.0 | Extreme → almost no pixels change, attack may fail |

There's a sweet spot: enough sparsity to be stealthy, but enough freedom to succeed.

## What Sparse Attacks Reveal

The pixels EAD chooses to modify are the **most important features** for the model's decision. This is useful for:
- **Understanding the model**: which pixels actually matter?
- **Finding weaknesses**: models that rely on few pixels are fragile
- **Defense design**: protect the features the model depends on most

## Sparsity vs Success Rate

As you increase β (force more sparsity):
- L0 decreases (fewer pixels changed) ✓
- Success rate eventually drops ✗
- The crossover point tells you the model's minimum vulnerable feature set

## Comparison Across Attacks

```
FGSM   → L0 ≈ ALL pixels  | Success: high  | Stealth: low
CW L2  → L0 ≈ most pixels | Success: high  | Stealth: medium
EAD    → L0 ≈ few pixels  | Success: high  | Stealth: high
```
