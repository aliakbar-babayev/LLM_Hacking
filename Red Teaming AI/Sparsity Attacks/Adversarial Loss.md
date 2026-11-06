# Adversarial Loss

The **f(x')** part of EAD's objective — this is what makes the model misclassify.

## CW Loss (Carlini & Wagner)

The most common adversarial loss for targeted attacks:

```
f(x') = max(Z(x')_true - Z(x')_target, -κ)
```

- **Z(x')** = logits (raw model output before softmax)
- **Z(x')_true** = logit for the correct class
- **Z(x')_target** = logit for the class we WANT the model to predict
- **κ** (kappa) = confidence margin — how much we want to overshoot

## What It Does

- When `Z_true > Z_target` → loss is positive → model still predicts correctly → keep pushing
- When `Z_target > Z_true` → loss is negative → misclassification achieved
- **κ** makes the attack aim for `Z_target > Z_true + κ` → more confident wrong prediction

## Why Not Cross-Entropy?

Cross-entropy loss saturates (gradient vanishes) when the model is very confident. CW loss gives useful gradients throughout the attack, making optimization more stable.

## Untargeted Version

For untargeted (just make it wrong, don't care which class):

```
f(x') = max(Z(x')_runner_up - Z(x')_true, -κ)
```

Push any other class above the true class.
