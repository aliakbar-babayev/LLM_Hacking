#!/usr/bin/env python3
"""LLM Hacking Quiz 1: ML/DL Foundations & Concepts"""

import random

QUESTIONS = [
    {
        "q": "A spam filter has 99% accuracy on a dataset where 98% of emails are legitimate.\nIs this filter good? Why or why not?",
        "options": [
            "Yes — 99% accuracy is excellent by any standard",
            "No — a model that always predicts 'legitimate' gets 98% accuracy, so 99% barely beats the naive baseline. Check precision/recall instead",
            "No — 99% means 1% of spam gets through which is too much",
            "Yes — but only if the dataset is balanced"
        ],
        "answer": 1,
        "explain": "Class imbalance makes accuracy misleading. Always predicting majority class = 98% accuracy. The real question: what's the precision and recall for the SPAM class?"
    },
    {
        "q": "As a red teamer, why should you care that a model has high precision but low recall?",
        "options": [
            "It means the model is overfit and will crash in production",
            "It means you can easily flood it with false positives",
            "It means the model catches what it flags accurately, but MISSES many attacks — easy to slip through undetected",
            "It means the model is too slow for real-time detection"
        ],
        "answer": 2,
        "explain": "High precision = few false positives. Low recall = many false negatives. For a red teamer: the model won't flag your attacks because it misses a lot."
    },
    {
        "q": "You want to classify images. Which algorithm family would you use and why?",
        "options": [
            "Random Forest — it handles any data type with majority voting",
            "CNN (Convolutional Neural Network) — Conv→ReLU→Pool layers learn spatial features from images",
            "KNN — it compares images pixel by pixel with neighbors",
            "Naive Bayes — it works well on all classification tasks"
        ],
        "answer": 1,
        "explain": "CNNs (AlexNet, VGG, ResNet) learn spatial hierarchies: edges → textures → parts → objects. Convolution detects local patterns regardless of position."
    },
    {
        "q": "What makes Transformers fundamentally different from RNNs for processing sequences?",
        "options": [
            "Transformers use more layers so they're more powerful",
            "Transformers process all tokens in parallel via self-attention, while RNNs process sequentially (one token at a time)",
            "Transformers don't need training data",
            "RNNs can only handle text while Transformers handle any data"
        ],
        "answer": 1,
        "explain": "Self-attention: Attention(Q,K,V) = softmax(QK^T/√d_k)·V. Every token attends to every other token simultaneously. RNNs must process left-to-right, creating bottlenecks."
    },
    {
        "q": "What does Temperature control in LLM generation?\nTemp=0 vs Temp=2?",
        "options": [
            "Temp=0 generates more tokens, Temp=2 generates fewer",
            "Temp=0 is deterministic (most likely token always), Temp=2 is highly random (more uniform probability distribution)",
            "Temp=0 means the model is frozen (no output), Temp=2 means it's creative",
            "Temperature controls the maximum output length"
        ],
        "answer": 1,
        "explain": "Temperature scales the logits before softmax. 0→deterministic (greedy), higher→flatter distribution→more randomness. This matters for attacks: low temp = predictable, high temp = harder to control."
    },
    {
        "q": "You find a .pkl model file on a target server. Why is this a security concern?",
        "options": [
            "PKL files are unencrypted so anyone can read the model weights",
            "Pickle deserialization executes arbitrary code — a compromised .pkl file = remote code execution",
            "PKL files contain training data which is a privacy violation",
            "PKL files are too large and will fill the server disk"
        ],
        "answer": 1,
        "explain": "Python pickle deserializes objects by executing code. A malicious .pkl can run arbitrary commands when loaded. This is a real supply chain attack vector."
    },
    {
        "q": "What is the difference between Supervised, Unsupervised, and Reinforcement Learning?",
        "options": [
            "Supervised uses labels, Unsupervised has no labels, RL uses rewards from environment interaction",
            "Supervised is automated, Unsupervised needs human oversight, RL is self-improving",
            "Supervised works on text, Unsupervised on images, RL on games",
            "They're different names for the same process with different datasets"
        ],
        "answer": 0,
        "explain": "Supervised: Data+Labels→Model. Unsupervised: Data only→find patterns. RL: Agent takes Actions→Environment returns States+Rewards. Each has different attack surfaces."
    },
    {
        "q": "DBSCAN labels a point as -1. What does that mean, and why is this relevant to security?",
        "options": [
            "The point belongs to cluster 1 in reverse order",
            "The point is noise/outlier — doesn't belong to any cluster. Anomaly detectors use this to flag attacks",
            "The point hasn't been processed yet",
            "The algorithm failed on that data point"
        ],
        "answer": 1,
        "explain": "DBSCAN label -1 = noise (not dense enough to belong to any cluster). Security tools use this for anomaly detection. As an attacker, you want your malicious traffic to NOT get labeled -1."
    },
    {
        "q": "An Isolation Forest scores a sample as anomalous. What's the underlying intuition?",
        "options": [
            "Anomalies are far from the forest's center of mass",
            "Anomalies are easier to isolate — they require fewer random splits to separate from the rest",
            "Anomalies have the highest feature values",
            "Anomalies appear in the smallest cluster"
        ],
        "answer": 1,
        "explain": "Isolation Forest randomly splits features. Anomalies are rare and different, so they get isolated in fewer splits. Short path length = more likely anomalous."
    },
    {
        "q": "What is RAG (Retrieval Augmented Generation) and why does it matter for security?",
        "options": [
            "A training technique that makes models larger",
            "A method where the LLM retrieves external documents before generating — the retrieved content becomes an attack surface for indirect prompt injection",
            "A way to encrypt LLM outputs",
            "A debugging tool for LLM applications"
        ],
        "answer": 1,
        "explain": "RAG feeds external data into the LLM's context. If an attacker poisons those external documents, the LLM processes malicious instructions. This is indirect prompt injection."
    },
    {
        "q": "What is the difference between fine-tuning and prompting an LLM?",
        "options": [
            "Prompting changes the model weights, fine-tuning changes the input",
            "Prompting crafts the input to guide output (no weight changes). Fine-tuning actually updates model weights on new data",
            "Fine-tuning is free, prompting costs money",
            "There's no practical difference"
        ],
        "answer": 1,
        "explain": "Cost ladder: Prompting (free) → RAG (low) → LoRA/QLoRA (medium, partial weight updates) → Full fine-tuning (expensive, all weights). Each level opens different attack surfaces."
    },
    {
        "q": "What does backpropagation compute, and why is it relevant to adversarial attacks?",
        "options": [
            "It computes the model's accuracy on test data",
            "It computes gradients (∂Loss/∂weights) via chain rule — attackers use the SAME gradients to craft adversarial inputs (e.g., FGSM)",
            "It propagates data backwards through the network for verification",
            "It's the process of removing bad training data"
        ],
        "answer": 1,
        "explain": "Backprop computes how much each parameter contributed to the loss. Training adjusts weights to DECREASE loss. FGSM adjusts INPUTS to INCREASE loss — same math, different target."
    },
    {
        "q": "GANs have a 'mode collapse' problem. What does that mean?",
        "options": [
            "The discriminator becomes too strong and blocks all generated output",
            "The generator learns to produce only one type of output that fools the discriminator, losing diversity",
            "The model crashes when given too many modes/classes",
            "Training fails because both networks improve at the same rate"
        ],
        "answer": 1,
        "explain": "Mode collapse: Generator finds one 'safe' output that reliably fools the Discriminator and stops exploring. Result: all generated images look the same."
    },
    {
        "q": "What is the ε-greedy policy in Reinforcement Learning?",
        "options": [
            "Always exploit the best known action",
            "With probability ε take a random action (explore), otherwise take the best known action (exploit)",
            "Gradually increase the learning rate by ε each episode",
            "Only explore if the reward drops below ε"
        ],
        "answer": 1,
        "explain": "Exploration vs Exploitation tradeoff. ε-greedy balances: explore ε% of the time (try new things), exploit (1-ε)% (use what works). ε usually decays over time."
    },
    {
        "q": "What is the key difference between PCA and t-SNE?",
        "options": [
            "PCA is for images, t-SNE is for text",
            "PCA finds directions of maximum variance (linear, usable for features). t-SNE is non-linear, visualization only, preserves local structure",
            "PCA reduces dimensions, t-SNE increases them",
            "t-SNE is faster and better in every way"
        ],
        "answer": 1,
        "explain": "PCA = linear dimensionality reduction, keeps global variance. t-SNE = non-linear, great for visualizing clusters but NOT for features. UMAP is a faster alternative to t-SNE."
    },
    {
        "q": "What RL attack could manipulate an AI agent's behavior without touching its code?",
        "options": [
            "SQL injection into the reward function",
            "Reward poisoning — manipulate the reward signal so the agent learns the wrong behavior",
            "Deleting the agent's memory buffer",
            "Overclocking the training GPU"
        ],
        "answer": 1,
        "explain": "RL attacks: reward poisoning (corrupt rewards), observation manipulation (alter what agent sees), policy extraction (steal the strategy), adversarial perturbations (confuse inputs)."
    },
    {
        "q": "Why is deep learning described as 'vulnerable' from a security perspective?",
        "options": [
            "It uses too much memory making it easy to DoS",
            "Non-interpretable (can't explain decisions), overconfident (high confidence on wrong predictions), brittle (small perturbations flip output), and adversarial examples transfer across models",
            "It requires internet access to run",
            "The training data is always publicly available"
        ],
        "answer": 1,
        "explain": "Four DL weaknesses: non-interpretable (black box), overconfident (99% sure but wrong), brittle (tiny pixel changes fool it), transferable (attack one model, fool another)."
    },
    {
        "q": "Diffusion models are now state-of-the-art for image generation. How do they work?",
        "options": [
            "They generate images pixel by pixel from left to right",
            "Forward process adds noise until pure noise; reverse process learns to denoise step by step to generate images",
            "They combine multiple GANs in a pipeline",
            "They memorize and retrieve training images"
        ],
        "answer": 1,
        "explain": "Forward: gradually add Gaussian noise to image → pure noise. Reverse: train a neural network to undo each noise step. Generation starts from random noise and denoises."
    },
    {
        "q": "What is the Silhouette Score and what does a value of -1 mean?",
        "options": [
            "It measures model accuracy; -1 = 100% wrong",
            "It evaluates clustering quality [-1,1]; -1 means points are assigned to the WRONG clusters (closer to other clusters than their own)",
            "It measures feature importance; -1 = feature is harmful",
            "It's a loss function; -1 = perfect convergence"
        ],
        "answer": 1,
        "explain": "Silhouette Score compares intra-cluster distance vs nearest-cluster distance. +1 = perfect clustering, 0 = overlapping, -1 = wrong cluster assignments."
    },
    {
        "q": "Traditional ML: Data + Output → Rules.\nWhat does this mean compared to traditional programming?",
        "options": [
            "ML writes its own code based on examples",
            "Instead of coding rules manually (Rules + Data → Output), ML learns rules from data and expected outputs",
            "ML doesn't need any rules at all",
            "ML outputs rules as text that programmers then implement"
        ],
        "answer": 1,
        "explain": "Traditional programming: you write the rules. ML: you provide examples (data + correct outputs), and the algorithm learns the rules. This is why the training data is such a critical attack surface."
    },
]


def run_quiz():
    print("=" * 65)
    print("  LLM HACKING QUIZ 1: ML/DL Foundations & Concepts")
    print("=" * 65)
    print(f"\n  {len(QUESTIONS)} scenario-based questions.")
    print("  Focus on WHY things work, not just what they are.\n")

    questions = QUESTIONS[:]
    random.shuffle(questions)
    score = 0
    wrong = []

    for i, q in enumerate(questions, 1):
        print(f"\n{'─' * 60}")
        print(f"  [{i}/{len(questions)}] {q['q']}\n")

        indices = list(range(len(q["options"])))
        random.shuffle(indices)
        correct_letter = None
        for j, idx in enumerate(indices):
            letter = chr(65 + j)
            if idx == q["answer"]:
                correct_letter = letter
            print(f"    {letter}) {q['options'][idx]}")

        while True:
            ans = input(f"\n  Your answer (A-{chr(64 + len(q['options']))}): ").strip().upper()
            if ans in [chr(65 + j) for j in range(len(q["options"]))]:
                break
            print("  Invalid input. Try again.")

        if ans == correct_letter:
            score += 1
            print(f"\n  ✓ Correct!")
        else:
            print(f"\n  ✗ Wrong. Correct answer: {correct_letter}")
            wrong.append(q)

        print(f"  → {q['explain']}")

    print(f"\n{'=' * 65}")
    print(f"  FINAL SCORE: {score}/{len(questions)} ({score * 100 // len(questions)}%)")
    print(f"{'=' * 65}")

    if wrong:
        print(f"\n  Review these {len(wrong)} topics:")
        for q in wrong:
            print(f"    • {q['q'][:80]}")
    elif score == len(questions):
        print("\n  Perfect score! Solid ML/DL foundation.")
    print()


if __name__ == "__main__":
    run_quiz()
