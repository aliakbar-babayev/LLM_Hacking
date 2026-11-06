# Complete FISTA Iteration and Binary Search

## Full FISTA Loop

```
For each iteration k:
    1. Compute gradient of (c·f + L2) at current point
    2. Gradient step: y = x_k - step_size * gradient
    3. Shrinkage: x_{k+1} = shrink(y, x_orig, β·step_size)
    4. Clip: x_{k+1} = clamp(x_{k+1}, 0, 1)
    5. Momentum: update using acceleration term
    6. Track best result (lowest distortion that still misclassifies)
```

## Binary Search for c

**c** balances attack success vs perturbation size. Too small = attack fails. Too large = unnecessary distortion.

Finding the right c:
1. Start with a range: `c_low = 0`, `c_high = initial_c`
2. Try `c_mid = (c_low + c_high) / 2`
3. Run full FISTA with `c_mid`
4. If attack **succeeds** → `c_high = c_mid` (try smaller c)
5. If attack **fails** → `c_low = c_mid` (try larger c)
6. Repeat for ~10 steps

This finds the **minimum c** that achieves misclassification → smallest possible perturbation.

## Why Binary Search?

Setting c manually is guesswork. Binary search automatically finds the sweet spot where the attack barely succeeds with minimal distortion.
