# 🎮 Reinforcement Learning Algorithms

> **Red Team Mindset:** RL is how AI learns to play games — and attack/defend networks. Understanding RL means understanding both automated defenders and how to build automated attackers.

---

## 🧩 The Core Loop

```
         ┌────────────────────────────────┐
         │          ENVIRONMENT           │
         │                                │
  State (sₜ) ───→  AGENT ───→  Action (aₜ)
         │            ↑                   │
         │   Reward (rₜ) + Next State sₜ₊₁│
         └────────────────────────────────┘
```

The agent's goal: **maximize cumulative reward over time**.

---

## 🧠 Core Components Defined

| Component | Description | Security Analogy |
|-----------|-------------|-----------------|
| **Agent** | The learner / decision-maker | Attacker or defender bot |
| **Environment** | The world agent interacts with | Target network |
| **State (s)** | Current situation snapshot | Network topology, alerts |
| **Action (a)** | Choice the agent makes | Launch exploit, pivot, patch |
| **Reward (r)** | Feedback signal (+/-) | Flag captured, detection avoided |
| **Policy (π)** | Strategy: state → action | Attack playbook |
| **Value Function V(s)** | Expected future reward from state s | How promising is this position? |
| **Q-Function Q(s,a)** | Expected reward for action a in state s | Which move is best right now? |

---

## 📐 Formal Framework — Markov Decision Process (MDP)

An MDP is defined by the tuple **(S, A, P, R, γ)**:

- **S** — State space
- **A** — Action space
- **P(s'|s,a)** — Transition probability (next state given current state + action)
- **R(s,a)** — Reward function
- **γ (gamma)** — Discount factor (0 ≤ γ ≤ 1)
  - γ close to 1 = values future rewards highly (long-term thinking)
  - γ close to 0 = greedy, only cares about immediate reward

**Bellman Equation:**
```
V*(s) = max_a [ R(s,a) + γ · Σ P(s'|s,a) · V*(s') ]
```

---

## ⚖️ Exploration vs. Exploitation

One of the core dilemmas in RL:

| Strategy | Meaning |
|----------|---------|
| **Exploration** | Try new actions to discover better rewards |
| **Exploitation** | Stick with what works based on current knowledge |

**ε-greedy policy:**
```python
import random
if random.random() < epsilon:
    action = env.action_space.sample()  # Explore
else:
    action = argmax(Q[state])           # Exploit
```

Epsilon typically decays over training: start high (explore), end low (exploit).

---

## 🗂️ Algorithm Families

### 1. Value-Based Methods
Learn a value/Q function → derive policy from it.

#### Q-Learning (Tabular)
Works for small, discrete state spaces. Stores Q-values in a table.

```python
# Q-table update (Bellman update)
Q[state][action] = Q[state][action] + alpha * (
    reward + gamma * max(Q[next_state]) - Q[state][action]
)
```

| Hyperparameter | Role |
|---------------|------|
| `alpha` (α) | Learning rate — how fast to update |
| `gamma` (γ) | Discount factor — weight future rewards |
| `epsilon` (ε) | Exploration rate |

---

#### Deep Q-Network (DQN)
Replaces the Q-table with a **neural network** — handles large/continuous state spaces.

```
State (s) → [Neural Network] → Q-values for each action
                                       ↓
                               Pick action with max Q
```

**Key innovations:**
- **Experience Replay Buffer:** Store past transitions, sample randomly for training (breaks correlation)
- **Target Network:** A slow-updating copy of the network for stable training targets

```python
# Pseudocode
for step in range(max_steps):
    action = epsilon_greedy(Q_network, state)
    next_state, reward, done = env.step(action)
    replay_buffer.add((state, action, reward, next_state, done))

    batch = replay_buffer.sample(batch_size)
    target = reward + gamma * max(Q_target(next_state))
    loss = MSE(Q_network(state, action), target)
    optimizer.step(loss)
```

---

### 2. Policy-Based Methods
Directly learn the policy π(a|s) without a value function.

#### REINFORCE (Policy Gradient)
```
∇J(θ) = E[ ∇log π(aₜ|sₜ, θ) · Gₜ ]
```
- Gₜ = cumulative return from timestep t
- Update policy to make high-reward actions more likely

**Strength:** Works in continuous action spaces.
**Weakness:** High variance — training can be unstable.

---

### 3. Actor-Critic Methods
Combine value-based and policy-based approaches:

```
Actor  → Learns π(a|s) — what to do
Critic → Learns V(s)   — how good the state is
           ↓
       Advantage = R + γV(s') - V(s)
       Actor updates toward high-advantage actions
```

---

### 4. Advanced Algorithms at a Glance

| Algorithm | Type | Key Feature | Best For |
|-----------|------|------------|----------|
| **PPO** | On-policy Actor-Critic | Clipped objective, very stable | General purpose |
| **A3C** | Async Actor-Critic | Parallel workers, no replay buffer | Speed |
| **SAC** | Off-policy Actor-Critic | Entropy bonus (encourages exploration) | Continuous control |
| **DDPG** | Off-policy | Deterministic policy for continuous actions | Robotics |
| **TD3** | Off-policy | Fixes DDPG instability | Continuous control |

---

## 🛠️ Getting Started with Gymnasium

```python
import gymnasium as gym

env = gym.make("CartPole-v1", render_mode="human")
obs, info = env.reset(seed=42)

for step in range(500):
    action = env.action_space.sample()                         # Random agent
    obs, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        obs, info = env.reset()

env.close()
```

**Common Environments:**
| Environment | Task | Complexity |
|------------|------|-----------|
| `CartPole-v1` | Balance a pole | Simple |
| `MountainCar-v0` | Drive up a hill | Medium |
| `LunarLander-v2` | Land a spacecraft | Medium |
| `Atari/Breakout` | Play Breakout | Hard |

---

## 🔴 Red Team Angle

### RL as an Attack Tool
```
Agent = Automated attacker
Environment = Target system/network
State = Current access level, alerts triggered
Action = Exploit to try, lateral move, exfil route
Reward = +10 reaching objective, -5 getting detected
```

Real research (e.g., **CyberBattleSim** by Microsoft, **NASimEmu**) uses RL for automated penetration testing.

### Attacking RL-Based Defenders
| Attack | Description |
|--------|-------------|
| **Reward poisoning** | Manipulate the reward signal to misdirect the agent |
| **Observation manipulation** | Feed false state to confuse the agent's policy |
| **Policy extraction** | Query an RL agent repeatedly to clone its policy |
| **Adversarial perturbations** | Small changes to state observations that cause policy failures |

> RL defenders are only as good as the environment they trained in — if your real attack falls outside the training distribution, the defender has no idea how to respond.

---

## 🔗 Linked Notes
- [[Introduction_to_Machine_Learning]]
- [[Introduction_to_Deep_Learning]]

---
*Tags: #ReinforcementLearning #RL #DQN #PPO #ActorCritic #RedTeam #AutomatedPentest*
