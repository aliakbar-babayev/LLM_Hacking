
### The big picture first

FGSM asks: “if I’m allowed to change every pixel by ε, what’s the worst I can do?” You pick the budget and hope it’s enough.

DeepFool asks the opposite: **“what’s the smallest change that flips the prediction?”** It finds the minimum, so you don’t guess ε.

**Red team mapping:**

|ML concept|Security analogy|
|---|---|
|Decision boundary|The line between “blocked” and “allowed” in the target’s logic|
|Minimal perturbation|The smallest payload that bypasses the filter|
|Distance to boundary|How close the input already is to a bypass|
|Overshoot|Pushing slightly _past_ the line so the flip is reliable|
|Robustness|How big a push the target tolerates before it breaks|

The core idea: a classifier divides the input space into regions, one per class. Your image sits inside the “7” region. Somewhere nearby there’s a border with another region. DeepFool finds the shortest route to that border and steps just over it.


### 1. DeepFool and the Quest for Minimality

**Definition:** The motivation. Why does the smallest perturbation matter?

- **Stealth:** the smaller the change, the less likely a human, a detector, or a defense notices it.
- **Measurement:** the minimal perturbation is a _robustness score_ for the model. A model where you need a huge change to fool it is more robust than one where a tiny change works.
- **Fair comparison:** with FGSM you choose ε, so results depend on your choice. DeepFool gives a model-driven number, which lets you compare models or defenses objectively.

_Analogy:_ FGSM is “try a 10 KB payload and see if it works.” DeepFool is “binary search for the shortest payload that still works.”

### 2. DeepFool Theory and Formulation

**Definition:** The math behind the attack.

**Step 1: the linear case.** Suppose the classifier is a flat boundary, a line (or plane) described by f(x) = wᵀx + b. The sign of f decides the class, and f(x) = 0 is the boundary. The shortest path to a plane is a straight line perpendicular to it:

_Analogy:_ standing in a field, with a fence that is straight. The shortest way across is perpendicular to it.

**Step 2: real neural networks aren’t flat.** Their boundaries are curved. So DeepFool **pretends the boundary is flat locally** (a linear approximation using the gradient), jumps to that estimated boundary, then re-checks. If the label hasn’t changed yet, repeat from the new position. Each step gets closer.

**Step 3: multiple classes.** For each other class k, linearize the gap between class k and the original class

**Step 4: finish.** Stop when the predicted class changes. The total perturbation is the sum of all steps. Then multiply by **(1 + overshoot)** (typically 0.02) so you land slightly _past_ the boundary rather than exactly on it.

### 3. Perturbation Analysis and Metrics

**Definition:** Quantifying how small and how effective the attacks were.

|Metric|Meaning|
|---|---|
|**L2 norm** ‖r‖₂|Euclidean size of the change. DeepFool’s native measure|
|**L∞ norm** ‖r‖∞|Largest change to any single pixel (what the FGSM-style budget limits)|
|**L0 norm**|How many pixels changed at all|
|**Fooling rate**|% of correctly classified images the attack flipped|
|**Avg iterations**|How quickly the boundary was reached|
|**Robustness ρ**|Average of ‖r‖₂ / ‖x‖₂. A relative measure: **lower = easier to fool**|
|**Confidence after attack**|How sure the model is of its wrong answer|

**How to read them:**

- A **small ρ** means the model is fragile: a tiny relative change defeats it.
- Plot a **histogram of perturbation sizes** to see the spread. A few hard images may need much more.
- **Compare to FGSM:** DeepFool typically hits the same fooling rate with a _smaller_ perturbation, because it doesn’t waste budget.