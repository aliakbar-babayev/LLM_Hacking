# Attack Visualizations

## What to Look For

When visualizing EAD adversarial examples, you typically see three images side by side:

```
[Original Image]  →  [Perturbation Map]  →  [Adversarial Image]
  "cat" (99%)         (amplified noise)       "dog" (97%)
```

## Perturbation Map

The perturbation (x_adv - x_orig) amplified for visibility:
- **EAD/Sparse**: a few bright dots on a black background — only a handful of pixels changed
- **FGSM**: uniform noise everywhere — every pixel touched
- **DeepFool**: faint pattern across the whole image

## Key Visual Difference

| Attack | Perturbation Looks Like |
|--------|------------------------|
| FGSM | TV static / uniform grain |
| CW L2 | Faint structured pattern |
| EAD | A few scattered bright spots on black |

## Heatmaps

Saliency heatmaps show WHERE the attack focused. EAD typically targets:
- Edge boundaries between objects
- High-contrast areas
- Features the model relies on most for classification

## Human Perception

Sparse attacks are often **harder for humans to notice** because our eyes are bad at spotting a few changed pixels but good at detecting global noise patterns.
