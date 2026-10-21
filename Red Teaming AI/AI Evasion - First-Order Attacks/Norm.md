

When we talk about adversarial attacks on machine learning models, one of the most important questions is: "How much did we change the input?" This might seem simple - just look at the image and see if it looks different, but computers need precise mathematical ways to measure these changes, and that's where `norms` come in.

Think of a norm as a ruler for measuring changes. Just like you might measure distance in miles or kilometers, we use different norms to measure how much an adversarial attack has modified an input. The fascinating part is that different "rulers" (norms) measure changes in completely different ways, leading to very different types of attacks.

## What Exactly Is a Norm?

![City grid metaphor comparing L0 counting turns, L1 Manhattan distance, L2 diagonal distance, and L∞ longest single leg between start and goal.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/319/introduction_norm_city_metaphor.png)


Let's start with something familiar. Imagine you're in New York City and want to travel from Times Square to Central Park. How far is it? The answer depends on how you measure:

- If you count how many intersections you pass through (regardless of distance), that's one measure
- If you have to walk along the city streets (following the grid), that's a different distance
- If you can fly in a straight line (like a bird), that's another distance
- If you only care about the longest single stretch you have to travel, that's yet another way to measure

These different ways of measuring distance are exactly what norms do for adversarial perturbations. A `norm` is simply a mathematical tool that assigns a "size" or "length" to changes we make to an input.

## The Three Rules Every Norm Must Follow

### Rule 1: “Zero means zero” (Positive Definiteness)

**Formal statement:** ‖**v**‖ ≥ 0 for every **v**, and ‖**v**‖ = 0 **if and only if** **v** = **0**.

There are really two claims bundled together:

1. **Lengths are never negative.** (Your summary skips this part, but it’s included in the formal axiom.)
2. **Only the zero vector has length zero.** The “if and only if” runs both directions: the zero vector must have length zero, _and_ any nonzero vector must have strictly positive length.

**Why it matters:** A norm should be able to tell vectors apart. If a nonzero vector could have length 0, then the ruler would be blind to it.

**Example of a violation:** On ℝ², define f(x, y) = |x|. This measures only the horizontal part. The vector (0, 5) is clearly not the zero vector, yet f(0, 5) = 0. This function is called a **seminorm**: it satisfies the other two rules but fails this one. A seminorm can’t distinguish vectors that differ only in the direction it ignores, which means you can’t say “two vectors are close” and conclude they are nearly equal.

**Consequence of the rule:** The distance between **u** and **v** is defined as ‖**u** − **v**‖. Rule 1 guarantees that distance zero means the points are _identical_. Without it, distinct points could be “zero distance apart.”

---

### Rule 2: “Doubling means doubling” (Absolute Homogeneity)

**Formal statement:** ‖c·**v**‖ = |c| · ‖**v**‖ for every scalar c and every vector **v**.

**The intuition:** Scaling a vector by a factor c scales its length by the same factor. Stretch an arrow to three times its size, and its length triples.

**Two subtleties your summary glosses over:**

- **The absolute value |c|.** If c = −2, the vector flips direction and doubles in size. Its length is still 2·‖**v**‖, not −2·‖**v**‖. Length is never negative, and flipping direction doesn’t change length. So ‖−**v**‖ = ‖**v**‖.
- **Scaling by zero.** Taking c = 0 gives ‖0·**v**‖ = 0·‖**v**‖ = 0, which is consistent with Rule 1.

**Example:** In ℝ² with the usual Euclidean length, **v** = (3, 4) has ‖**v**‖ = 5. Then ‖(6, 8)‖ = 10 and ‖(−3, −4)‖ = 5. Everything scales as promised.

**Example of a violation:** Let f(x, y) = x² + y². This is the _squared_ length. Doubling the vector (3, 4) to (6, 8) gives f = 100, which is **four times** f(3, 4) = 25, not twice. Squared length scales quadratically, so it is not a norm, even though it’s closely related to one.

**Why it matters:** This rule ties the norm to the _linear structure_ of the space. It means units behave properly: if you measure in centimeters instead of meters (scaling by 100), all your lengths scale by 100 as well. It also means that if you know the length of one vector, you instantly know the length of every multiple of it.

---

### Rule 3: “Shortcuts don’t exist” (The Triangle Inequality)

**Formal statement:** ‖**u** + **v**‖ ≤ ‖**u**‖ + ‖**v**‖ for all vectors **u**, **v**.

**The geometric picture:** Place **u** and **v** head to tail. Then **u** + **v** is the straight arrow from the start of **u** to the end of **v**. The three vectors form a triangle with sides of length ‖**u**‖, ‖**v**‖ and ‖**u** + **v**‖. The rule says one side of a triangle is never longer than the sum of the other two, or equivalently, **the direct route is never longer than a detour**.

**Example:** Walk 3 km east, then 4 km north. The detour covers 3 + 4 = 7 km total, but you end up only √(3² + 4²) = 5 km from where you started. Indeed 5 ≤ 7. Equality holds only when the two vectors point in the same direction (no real detour, as when you walk 3 km east and then 4 km further east).

### How the Three Rules Work Together

|Rule|What it protects|What fails without it|
|---|---|---|
|Positive definiteness|The ruler can detect any nonzero vector|Distinct points could be “distance 0” apart|
|Homogeneity|Lengths respect scaling and units|Measurements change unpredictably with scale|
|Triangle inequality|Straight lines are the shortest paths|Detours could beat direct routes; geometry collapses|

---

### Familiar Norms That Satisfy All Three

For a vector **x** = (x₁, …, xₙ):

- **Euclidean norm (ℓ²):** ‖**x**‖₂ = √(x₁² + … + xₙ²). Ordinary “as the crow flies” distance.
- **Manhattan norm (ℓ¹):** ‖**x**‖₁ = |x₁| + … + |xₙ|. Distance if you can only travel along a city grid.
- **Maximum norm (ℓ^∞):** ‖**x**‖_∞ = max(|x₁|, …, |xₙ|). The largest single coordinate.

All three obey the rules, yet they measure “size” differently. In ℝ², the set of vectors with norm 1 is a circle for ℓ², a diamond for ℓ¹, and a square for ℓ^∞. This shows that the three rules are flexible enough to allow many different notions of length while still guaranteeing consistent, sensible behavior.

## The p-Norm Family: Different Rulers for Different Jobs

The most common norms we use are called `p-norms`, and they're like a family of related measuring tools. The "p" is just a number that determines which family member we're using. Here's the formula:

∥x∥p=(∑i=1n|xi|p)1/p

This formula is just saying: "Take each change, raise it to the power p, add them all up, then take the p-th root." Different values of p give us different measuring tools:

When p=1, we get the L1 norm (like walking in Manhattan). When p=2, we get the L2 norm (like flying in a straight line). When p=∞, we get the L∞ norm (just look at the biggest change).

As p increases, the norm increasingly focuses on larger values. With p=1, all changes contribute equally to the sum. With p=2, bigger changes matter more because of the squaring. And as p approaches infinity, only the single largest change matters at all.

But wait, what about L0? Here’s where things get interesting. The L0 "norm" is actually an imposter in the p-norm family. It doesn’t follow the formula above at all. You can’t set p=0 in that equation and get something that counts non-zero elements. Instead, L0 has its own completely different definition:

∥x∥0=∑i𝟙[xi≠0]

This just counts how many elements are non-zero, regardless of their magnitude. A pixel changed by 0.001 counts the same as one changed by 255. Despite not being a true p-norm (or even a proper norm, since it violates the scaling rule), we use L0 constantly in adversarial ML because it captures something the p-norms can’t: pure sparsity. It answers the question "how many things did we touch?" rather than "how much did we change them?"

### The Shape of Constraints

Here's where it gets interesting. When we limit perturbations to a maximum norm value, we're essentially drawing a boundary that says "you can change the input, but only within this shape."

![Four constraint diagrams showing L0 selecting sparse points, L1 forming a diamond, L2 forming a circle, and L∞ forming a square as the perturbation budget grows.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/319/introduction_norm_shapes.png)

Imagine you're standing at a point and can move a fixed "distance" in any direction:

With the L0 norm, you can move in directions that change at most k coordinates (you can change k pixels to any value within the valid range). In continuous spaces, this feasible set is a union of axis‑aligned subspaces and is unbounded unless magnitudes are also bounded. With the L1 norm, you can reach anywhere within a diamond shape. With the L2 norm, you can reach anywhere within a circle. With the L∞ norm, you can reach anywhere within a square.

These shapes matter because they determine which directions are "cheaper" to move in. With L0, you get complete freedom in how much you change the selected pixels, but strict limits on how many you can touch; in practice, we often pair an L0 limit with a per‑pixel magnitude bound (e.g., the valid image range) to make the set well‑behaved. With L1, moving diagonally costs more than moving along the axes. With L∞, you can move equally far in any direction as long as no single coordinate changes too much.