
# Introduction to Abuse Attacks

Malicious actors can utilize LLM capabilities to facilitate abuse attacks, resulting in the widespread distribution of propaganda, cyber threats, and manipulative narratives, which pose significant risks to individuals, organizations, and societies. Since LLMs can generate convincing human-like text quickly and at scale, they can be powerful tools for spreading misinformation, hate speech, and aiding in unethical activities. In contrast to the `LLM hallucinations` discussed previously, Abuse Attacks aim at `deliberately` generating misinformation.

---

## Propaganda and Psychological Manipulation

Adversaries may weaponize LLMs through the `mass generation of propaganda and manipulative content`. These LLM-generated narratives may influence public opinion or spread ideological extremism via biased news articles, fake testimonials, and persuasive arguments that align with specific agendas. These generated texts may make it difficult for the public to distinguish between legitimate information and deliberately generated disinformation. Additionally, LLMs can be utilized to create and operate social media bots that mimic real users. These bots are often particularly effective in amplifying propaganda and orchestrating large-scale influence campaigns because they can engage in back-and-forth conversations with real users and are thus particularly effective in achieving their purpose. As such, LLM-generated abuse attacks may play a significant role in election interference in democratic countries, as these attacks provide a powerful tool to influence voters for both domestic and international actors.


## Evading Hate Speech Detection

As a second case study, let us explore evading LLM-based hate speech detectors based on [this](https://arxiv.org/abs/2501.16750) paper. Before diving in, let us first establish a definition of hate speech. According to the [United Nations](https://www.un.org/en/hate-speech/understanding-hate-speech/what-is-hate-speech), hate speech is `any kind of communication in speech, writing or behavior, that attacks or uses pejorative or discriminatory language with reference to a person or a group on the basis of who they are, in other words, based on their religion, ethnicity, nationality, race, colour, descent, gender or other identity factor`.

As LLMs significantly lower the cost of misinformation and hate campaigns, they are quickly becoming more prevalent. In large-scale hate speech campaigns, the adversaries' goal is typically to generate and spread hate speech without detection by existing hate speech detection measures, including both algorithmic and human-based detection mechanisms.

There are many popular AI-based hate speech detectors, such as [HateXplain](https://github.com/hate-alert/HateXplain) or [Detoxify](https://github.com/unitaryai/detoxify). These models typically process a text input and assign a `toxicity score`. If the input score exceeds a predefined threshold, we can classify it as hate speech. These detectors work reasonably well on LLM-generated hate speech samples. When evaluating different hate speech detectors, it is essential to remember that different detectors may operate based on different definitions of hate speech, resulting in varying outcomes.

To evade hate speech detectors, adversaries may apply various adversarial attacks to the LLM-generated hate speech samples. These include:

- `Character-level modifications`: These adversarial attacks modify text input by scoring individual tokens and modifying the most important tokens. An example of this type of adversarial attack is [DeepWordBug](https://github.com/QData/deepWordBug). Character-level modifications can include the following operations:
    - `Swap`: Swapping two adjacent characters, e.g., `HackTheBox` becomes `HackhTeBox`
    - `Substitution`: Substituting a character with a different character, e.g., `HackTheBox` becomes `HackTueBox`
    - `Deletion`: Deleting a character, e.g., `HackTheBox` becomes `HackTeBox`
    - `Insertion`: Inserting a character, e.g., `HackTheBox` becomes `HackTheBoux`
- `Word-level modifications`: These adversarial attacks modify text input by replacing words with synonyms. An example would be [PWWS](https://github.com/JHL-HUST/PWWS), which greedily replaces words with synonyms until the classification changes.
- `Sentence-level modifications`: This adversarial attack modifies text input by paraphra