# LLM Hacking — AI / LLM Security Notes

Personal notes and write-ups from learning **LLM / AI security** through
[Hack The Box Academy](https://academy.hackthebox.com/). Maintained as an
[Obsidian](https://obsidian.md) vault, so internal `[[wiki-links]]` resolve inside
Obsidian and render as plain text elsewhere.

> ⚠️ **Educational / authorized use only.** All techniques here were practiced in
> authorized lab environments. Do not use them against models, applications, or systems
> you do not own or lack **explicit written permission** to test. You are responsible for
> how you use this material.

---

## 📂 Contents

### Introduction — ML & AI Fundamentals
Background needed to understand what you're attacking: how ML/LLM systems are built,
trained, and evaluated. Start here. See [ML Vault Index](Introduction/ML_Vault_Index.md)
for the structured module map.

| Note | Topic |
|------|-------|
| [ML Vault Index](Introduction/ML_Vault_Index.md) | Module map, red-team attack map, quick-reference glossary |
| [Introduction to Machine Learning](Introduction/Introduction_to_Machine_Learning.md) | ML pipeline, terminology, attack surfaces |
| [Supervised Learning Algorithms](Introduction/Supervised_Learning_Algorithms.md) | Linear models, SVM, trees, XGBoost |
| [Unsupervised Learning Algorithms](Introduction/Unsupervised_Learning_Algorithms.md) | Clustering, anomaly detection |
| [Reinforcement Learning Algorithms](Introduction/Reinforcement_Learning_Algorithms.md) | MDP, DQN, PPO, automated attacks |
| [Introduction to Deep Learning](Introduction/Introduction_to_Deep_Learning.md) | Neural nets, adversarial examples |
| [Introduction to Generative AI](Introduction/Introduction_to_Generative_AI.md) | LLMs, diffusion, prompt injection |
| [Metrics](Introduction/Metrics.md) | How models are evaluated |
| [Datasets](Introduction/Datasets.md) | Training data and its role |

### Red Teaming AI
Offensive techniques against ML- and LLM-powered applications.

**Prompt Injection**

| Note | Technique |
|------|-----------|
| [Reconnaissance](Red%20Teaming%20AI/Prompt%20Injection/Reconnaissance.md) | Probing and fingerprinting an LLM app |
| [Direct Prompt Injection](Red%20Teaming%20AI/Prompt%20Injection/Direct%20Prompt%20Injection.md) | Overriding instructions via user input |
| [Indirect Prompt Injection](Red%20Teaming%20AI/Prompt%20Injection/Indirect%20Prompt%20Injection.md) | Payloads delivered through external/retrieved content |
| [Jailbreaking](Red%20Teaming%20AI/Prompt%20Injection/Jailbreaking.md) | Bypassing alignment / safety guardrails |
| [Abuse Attacks](Red%20Teaming%20AI/Prompt%20Injection/Abuse%20Attaks.md) | Misusing intended model capabilities |
| [LLM Hallucinations](Red%20Teaming%20AI/Prompt%20Injection/LLM%20Hallucinations.md) | Exploiting and assessing fabricated output |
| [Safeguard](Red%20Teaming%20AI/Prompt%20Injection/Safeguard.md) | Defenses and mitigations |

**Attacking AI — Application & System**

| Note | Topic |
|------|-------|
| [Overview of Application & System Components](Red%20Teaming%20AI/Attacking%20AI%20-%20Application%20and%20System/Overview%20of%20Application%20%26%20System%20Components.md) | The LLM app attack surface |
| [Insecure Integrated Components](Red%20Teaming%20AI/Attacking%20AI%20-%20Application%20and%20System/Insecure%20Integrated%20Components.md) | Plugins, tools, and downstream handling |
| [Rogue Actions](Red%20Teaming%20AI/Attacking%20AI%20-%20Application%20and%20System/Rogue%20Actions.md) | Excessive agency and tool abuse |
| [Model Reverse Engineering](Red%20Teaming%20AI/Attacking%20AI%20-%20Application%20and%20System/Model%20Reverse%20Engineering.md) | Extracting model behavior / parameters |
| [Denial of ML Service](Red%20Teaming%20AI/Attacking%20AI%20-%20Application%20and%20System/Denial%20of%20ML%20Service.md) | Resource-exhaustion attacks on ML services |

**Data Attacks**

| Note | Topic |
|------|-------|
| [Introduction to AI Data](Red%20Teaming%20AI/Data%20Attacks/Introduction%20to%20AI%20Data.md) | Role of data in the ML lifecycle |
| [AI Data Attacks](Red%20Teaming%20AI/Data%20Attacks/AI%20Data%20Attacks.md) | Poisoning and data-centric attacks overview |
| [Label Flipping](Red%20Teaming%20AI/Data%20Attacks/Label%20Flipping.md) | Corrupting labels to degrade a model |
| [Targeted Label Attacks](Red%20Teaming%20AI/Data%20Attacks/Targeted%20Label%20Attacks.md) | Precision poisoning for chosen outcomes |

**Reference**

| Note | Topic |
|------|-------|
| [LLM OWASP Top 10](Red%20Teaming%20AI/LLM%20OWASP%20Top%2010.md) | OWASP Top 10 for LLM Applications |
| [ML OWASP Top 10](Red%20Teaming%20AI/ML%20OWASP%20Top%2010.md) | OWASP Top 10 for Machine Learning |

---

## 🎯 Topics Covered

- ML/LLM fundamentals (tokens, context windows, system prompts, training pipeline)
- Prompt injection — direct and indirect
- Jailbreaking and guardrail bypass
- Data leakage and system-prompt extraction
- Insecure output handling and insecure integrated components
- Excessive agency and tool abuse (rogue actions)
- Data poisoning and label attacks
- Model extraction / reverse engineering and denial of ML service
- OWASP Top 10 for LLM Applications and for ML
- Mitigations and defensive considerations

## 🚀 Getting Started

1. Open this folder as a vault in **Obsidian** for working links and graph view.
2. Or read any `.md` file directly in a text editor / on GitHub.
3. Begin with the **[ML Vault Index](Introduction/ML_Vault_Index.md)**, work through *Introduction*, then move into *Red Teaming AI*.

## 🗺️ Suggested Learning Path

```
Introduction (how ML/LLMs work)
  └─ ML → Supervised → Unsupervised → RL → Deep Learning → Generative AI
        │
        ▼
Red Teaming AI (offense)
  ├─ Prompt Injection:  Recon → Direct → Indirect → Jailbreaking → Abuse → Safeguard
  ├─ App & System:      Components → Insecure Integrations → Rogue Actions → Reverse Eng → DoS
  └─ Data Attacks:      AI Data → Data Attacks → Label Flipping → Targeted Labels
        │
        ▼
Reference:  LLM OWASP Top 10 · ML OWASP Top 10
```

## 📚 Resources

- [Hack The Box Academy](https://academy.hackthebox.com/)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP Machine Learning Security Top 10](https://owasp.org/www-project-machine-learning-security-top-10/)
- [MITRE ATLAS](https://atlas.mitre.org/)

## 🚧 Progress

- [x] Introduction
- [ ] Red Teaming AI *(in progress)*

## 👤 Author

**Ali Akbar Babayev**
GitHub: [@aliakbar-babayev](https://github.com/aliakbar-babayev)

---
*Notes are updated as I progress. Feedback and corrections are welcome!*
