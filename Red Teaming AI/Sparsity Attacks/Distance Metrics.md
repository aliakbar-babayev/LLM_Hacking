# Distance Metrics

How we measure "how much did we change the input?"

## The Three Norms Used in EAD

| Norm | What It Measures | Formula | Intuition |
|------|-----------------|---------|-----------|
| **L0** | Count of changed pixels | \|{i : xᵢ ≠ x'ᵢ}\| | "How many pixels did I touch?" |
| **L1** | Sum of absolute changes | Σ\|x'ᵢ - xᵢ\| | "Total amount of change" |
| **L2** | Euclidean distance | √(Σ(x'ᵢ - xᵢ)²) | "Straight-line distance in pixel space" |

## Why EAD Reports All Three

- **L0** = the sparsity goal (fewer = better)
- **L1** = what the optimization directly penalizes
- **L2** = overall perturbation magnitude
- Lower numbers across all three = better, stealthier attack

## Comparison

An attack that changes 5 pixels by a lot:
- L0 = 5 (very sparse ✓)
- L1 = moderate
- L2 = moderate

FGSM changing 10,000 pixels by 0.01 each:
- L0 = 10,000 (not sparse ✗)
- L1 = 100
- L2 = 1.0
