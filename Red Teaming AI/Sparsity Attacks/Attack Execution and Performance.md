# Attack Execution and Performance

## Running the Full EAD Attack

```
1. Pick a target class (targeted) or just "anything wrong" (untargeted)
2. Binary search over c values (outer loop, ~10 steps)
3. For each c: run FISTA for N iterations (inner loop, ~1000 steps)
4. Track the best adversarial example found across all c values
5. Return the one with lowest distortion that still fools the model
```

## Performance Metrics

| Metric | What It Tells You |
|--------|------------------|
| **Attack Success Rate** | % of images successfully misclassified |
| **Mean L0** | Average number of pixels changed |
| **Mean L1** | Average total perturbation |
| **Mean L2** | Average Euclidean distance |
| **Iterations to Success** | How fast the attack converges |

## Typical Results (MNIST/CIFAR)

- **Success rate**: 99%+ on undefended models
- **L0**: often < 20 pixels changed (out of 784 for MNIST)
- Much sparser than FGSM or CW L2 attack
- Slower than FGSM (iterative optimization vs single step), but produces better quality adversarial examples

## Speed vs Quality Tradeoff

- **FGSM**: fast (one step), changes everything, easy to detect
- **EAD**: slow (many iterations + binary search), changes few pixels, hard to detect
