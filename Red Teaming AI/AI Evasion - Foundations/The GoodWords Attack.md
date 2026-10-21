
The GoodWords attack, first introduced by Lowd and Meek in their 2005 paper "[Good Word Attacks on Statistical Spam Filters](https://www.ceas.cc/papers-2005/125.pdf)," is an adversarial technique designed to exploit fundamental probabilistic assumptions within `Naive Bayes` classifiers, particularly those deployed for spam detection. This attack methodology manipulates the classifier's decision-making process by strategically appending carefully selected legitimate words to malicious messages, disguising spam content with legitimate-looking terms.


At its core, the attack leverages the mathematical foundation of `Naive Bayes` classification, specifically targeting the classifier's reliance on word frequency distributions and conditional probabilities. The technique demonstrates how probabilistic models can be deceived through simple manipulations that exploit their inherent assumptions about feature independence and probability calculations.

The GoodWords attack is simple and effective. Rather than attempting to obfuscate or modify the malicious content itself, the attack preserves the original spam message intact while augmenting it with additional tokens that shift the overall probability distribution. This approach maintains the semantic meaning and intent of the spam message while simultaneously convincing the classifier that the message belongs to the legitimate class.


## Good Word Selection Strategy

The effectiveness of the GoodWords attack depends on selecting appropriate words to append. The optimal selection strategy identifies words with strong discriminative power in favor of the legitimate class. We define a "goodness score" for each word w as:

S(w)=P(w|ham)P(w|spam)+ϵ

where ϵ is a small constant to prevent division by zero. Words with high goodness scores appear frequently in legitimate messages while being rare or absent in spam messages. Consider an example: if the word "meeting" appears in 45

![The Goodness Prism: A triangle with arrows showing words 'thanks,' 'the,' and 'free' scoring high, low, and bad.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/318/good_word_selection_strategy_panel2_prism.png)

We employ a systematic approach to word selection in our attack implementation. First, we analyze the training corpus to compute conditional probabilities for all vocabulary terms. We then rank words by their goodness scores, creating a prioritized list of candidates. This ranking considers not only the raw probability ratios but also the absolute frequencies to ensure selected words are representative of legitimate communication patterns.

![The Two Vocabulary Worlds: Venn diagram with 'Legitimate (Ham)' words like 'thanks' and 'meeting,' 'Spam' words like 'free' and 'prize,' and shared words 'the' and 'is' with low discriminative power.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/318/good_word_selection_strategy_panel1_worlds.png)

When selecting words, we must avoid those that might trigger other spam detection heuristics. While a word might have a high goodness score, its inclusion could activate rule-based filters or appear suspicious to human reviewers. The selection process often incorporates additional constraints to ensure the augmented message maintains linguistic coherence and plausibility.

The number of words to add represents an important parameter balancing attack effectiveness against message length constraints. Adding too few words may fail to shift the probability sufficiently, while adding too many could make the message appear unnatural or exceed transmission limits. Analysis shows that most spam messages can be successfully misclassified by adding between 15 and 30 carefully selected good words, achieving evasion rates over 90%.