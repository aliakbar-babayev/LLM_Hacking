# JSMA — Jacobian-based Saliency Map Attack

> Module from HackTheBox Academy: Red Teaming LLMs

## What is JSMA?

JSMA is an **adversarial attack** technique that finds the **minimum number of input features (pixels)** to change in order to fool a machine learning model into misclassifying an input. It's a **white-box attack** — you need access to the model's internals (gradients).

**Real-world analogy**: Imagine you have a photo of a cat, and a classifier says "cat." JSMA figures out which *specific pixels* to tweak (and by how much) so the classifier now says "dog" — while the image still looks like a cat to humans.

## Why Learn JSMA for Red Teaming?

- Understand how ML models can be attacked at the **mathematical level**
- Learn adversarial robustness concepts transferable to LLM security
- Build intuition for **gradient-based attacks** used against AI systems
- The same principles (saliency, gradients, search space) apply to attacking text-based models

## Topics

1. [[01_JSMA_Fundamentals]] — What JSMA is and why it works
2. [[02_Jacobian_and_Gradients]] — The math engine behind JSMA
3. [[03_Saliency_and_Search_Space]] — How JSMA picks which pixels to attack
4. [[04_Single_Pixel_Attack_Fundamentals]] — Attacking one pixel at a time
5. [[05_Single_Pixel_Attack_Loop]] — The iterative attack process
6. [[06_Single_Pixel_Batch_Evaluation]] — Testing attacks across many images
7. [[07_Single_Pixel_Configuration]] — Tuning attack parameters
8. [[08_Pairwise_Saliency]] — Attacking two pixels at once (more powerful)
9. [[09_Pairwise_Attack_Loop]] — The pairwise iterative process
10. [[10_Pairwise_Batch_Evaluation]] — Testing pairwise attacks at scale
11. [[11_Pairwise_Analysis]] — Comparing single vs pairwise results
12. [[12_Visualizations]] — Seeing what the attack actually does
13. [[13_Aggregate_Analysis]] — Big-picture attack effectiveness
14. [[14_JSMA_Challenge]] — Putting it all together
