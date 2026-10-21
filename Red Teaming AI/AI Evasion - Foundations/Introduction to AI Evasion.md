

Evasion attacks manipulate inference-time inputs to cause a trained model to produce incorrect outputs. Adversarial machine learning, the discipline that studies these hostile interactions with machine learning systems, treats this interference during the inference phase as a distinct threat because it bypasses safeguards built into the training pipeline.

Understanding evasion is therefore essential for anyone securing deployed AI models, such as AI Red Teamers.


## The AI Attack Landscape

To understand evasion, place it within the lifecycle of adversarial machine learning. AI systems can be attacked during training or at inference, and the distinction drives very different defenses.

Training‑time attacks change what the model learns. `Data poisoning` injects or alters training samples so the model internalizes biased patterns. `Label manipulation` tampers with annotations so ground truth no longer matches reality. `Trojan attacks` implant hidden triggers that activate specific behavior when an attacker’s pattern appears in the input.

These `training-time attacks` differ from `inference-time manipulation`, which changes only what the model sees when making a prediction. Data poisoning requires access to the dataset or pipeline and tends to shift behavior globally. Evasion, by contrast, leaves training and parameters untouched and succeeds by sending crafted inputs through the normal interface so a single example crosses the model’s learned decision boundary.

A property called transferability links these settings to real deployments. An adversarial example crafted against a surrogate model can often fool different production models, particularly when architectures or data are similar. This enables offline preparation and black-box attacks where the defender exposes only an API but not internals.


## Evasion Attacks in Traditional ML vs. LLMs

### 1. What an evasion attack is

An evasion attack happens at **inference time**. The model is already trained and frozen, and the attacker does not touch the training data or the weights. They craft an input that a human (or the system’s intended semantics) would classify one way, but the model classifies another way.

The attacker’s goal is usually one of two things:

- **Misclassification:** a malicious input is labeled benign (spam → ham, malware → clean).
- **Bypass of a control:** a prohibited request slips past a safety filter or policy.

The passage you quoted describes the traditional ML case. Below I unpack it, then contrast it with LLMs.

---

### 2. Traditional ML: why small edits work

#### Fixed feature representations

Classic models don’t see raw input. They see a **feature vector** produced by a deterministic pipeline: word counts, n-gram frequencies, byte histograms, import tables, section sizes, and so on. Training learns a function over that vector, and the learned function carves feature space into regions (classes).

The boundary between regions is the **decision boundary**. For a linear model it is a hyperplane (w·x + b = 0). For trees, SVMs, or neural nets it is more complex, but the idea is the same: there is a surface, and which side you land on determines the label.

Because the feature extraction is fixed and known (or discoverable), the attacker can reason about it directly. Their question becomes: _what is the cheapest change to the raw input that moves the feature vector across the boundary, while preserving the input’s true function?_

#### Example 1: Spam filter with bag-of-words

**How a Naive Bayes style filter works:**  
Each word has a learned likelihood under “spam” and under “ham.” A message’s score is the combined evidence across words:

> log P(spam | message) ∝ log P(spam) + Σ log P(word | spam)

(and the same for ham). Whichever is larger wins.

**The attack, often called “good word attack” or “word salad padding”:**

- The spam message contains strongly spammy tokens (“free,” “winner,” “claim”).
- The attacker appends a block of benign, ham-associated words (“meeting,” “agenda,” “quarterly,” “thanks”).
- Each added word contributes negative evidence for spam. Enough of them outweigh the spammy tokens.
- The **posterior shifts across the threshold**, and the message is classified as ham.

**The key insight:** the human reader still sees the same offer, perhaps with some harmless noise appended or hidden (white-on-white text, HTML comments). The _semantics for the human_ are unchanged, but the _statistics for the model_ are changed. This gap is the vulnerability.

A related technique is **obfuscation**: writing “fr33” or “v1agra” or inserting zero-width characters. Humans read the word normally, but the tokenizer produces a different, unseen token with no spam weight.

#### Example 2: Static malware detector

Static detectors analyze a file without running it, using features such as byte n-grams, PE header fields, section names and entropy, and imported API functions.

**Attack techniques:**

- **Section manipulation:** add or reorder sections, append unused overlay data, or pad with benign content. This shifts byte histograms and entropy statistics.
- **Import perturbation:** add imports of harmless APIs, or hide suspicious ones behind dynamic resolution (`GetProcAddress`), so the import table looks benign.
- **Packing/encryption:** wrap the payload so its on-disk bytes look unlike any known signature.
- **Semantics-preserving transformations:** change instruction encodings or insert no-ops without altering behavior.

**The constraint:** the attacker must keep the program **functional**. This is what makes malware evasion harder than image evasion. You can’t change arbitrary bytes, only ones that leave behavior intact.

#### The common thread

The passage identifies it precisely: **direct manipulation of the summarized features the model consumes**, aimed at moving a single prediction across its threshold. Three properties define this setting:

1. **Structured, low-level input space.** Features are numeric and well-defined, so you can compute gradients (white-box) or probe score changes (black-box).
2. **A measurable boundary.** The attacker can often quantify “distance to the boundary” and minimize the perturbation needed.
3. **A clear success criterion.** The label flips or it doesn’t.

#### The related image case

The same logic underlies **adversarial examples** in vision. Adding imperceptible pixel noise, computed via gradients (FGSM, PGD), pushes an image across the boundary: a panda becomes a “gibbon” with 99% confidence. Same mechanism, different feature space.

---

### 3. Why LLMs are different

LLMs break several assumptions that make traditional evasion clean.

|Dimension|Traditional ML|LLMs|
|---|---|---|
|**Input**|Fixed-length feature vector from a deterministic extractor|Free-form natural language (variable length, open-ended)|
|**Output**|One label or score|Open-ended generated text|
|**“Boundary”**|A geometric decision surface in feature space|No single boundary. Behavior emerges from billions of parameters plus context|
|**What’s attacked**|Feature values|Instructions, context, semantics, and the model’s own reasoning|
|**Success criterion**|Label flipped|Model produces content or takes actions it shouldn’t|
|**Perturbation**|Small numeric or token edits|Often large, fluent, human-readable rewrites|

#### The core shift: instructions and data share one channel

A traditional classifier has a rigid separation: the model’s logic is in the weights, and the input is only _data_. In an LLM, **instructions and data are both just text in the same context window**. The model can’t reliably tell “this is a command from my developer” from “this is text I was asked to process.” That structural fact opens up attack surface that doesn’t exist in classic ML.

#### Evasion categories for LLMs

**a) Jailbreaks (evading safety training)**  
The model has been trained to refuse certain requests. Attackers reframe the request so the refusal behavior doesn’t trigger:

- **Role-play / persona framing:** “You are an actor playing a character who has no restrictions…”
- **Hypothetical or fictional wrappers:** asking for prohibited content “for a novel.”
- **Instruction override:** “Ignore previous instructions…”
- **Multi-turn escalation:** building up gradually so no single message looks harmful.
- **Many-shot patterns:** filling context with examples of the model “complying,” exploiting in-context learning.

This is the analogue of crossing the decision boundary, but the “boundary” is a fuzzy learned behavior (refuse vs. comply), not a hyperplane.

**b) Obfuscation and encoding (the closest analogue to classic evasion)**  
These resemble “fr33” tricks in spam filters:

- Encoding a request in Base64, ROT13, leetspeak, or another language.
- Splitting a prohibited word across tokens or inserting odd characters.
- Using synonyms, euphemisms, or low-resource languages that safety training covered less.

Here the principle is identical to traditional evasion: **a mismatch between what the filter sees and what the underlying system understands.** The LLM can decode the obfuscated text, but the guardrail (or safety training) was weaker on that representation.

**c) Evading external guardrails and classifiers**  
Many deployments wrap the LLM with a separate moderation classifier. That classifier is a traditional ML model, so classic evasion applies to it directly: crafted tokens, suffixes, or paraphrases that keep the meaning for the LLM but lower the classifier’s harmfulness score.

**d) Adversarial suffixes (gradient-based, white-box)**  
Research (e.g., the GCG attack) showed that optimizing a string of seemingly nonsensical tokens, appended to a prompt, can reliably induce compliance. This is the literal descendant of classic adversarial examples, now applied to token sequences. Notably, such suffixes sometimes **transfer** across models.

**e) Prompt injection (indirect evasion)**  
Malicious instructions are hidden in content the LLM later processes, such as a web page, email, or document. The system’s guardrails focus on the _user’s_ message, so the attack slips in through a trusted-looking data channel. This has no clean counterpart in traditional ML and is especially dangerous in agentic systems with tool access.