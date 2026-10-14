
So far, we have explored `Label Flipping`. The primary goal there was general `performance degradation` - making the model less accurate overall. Now let's explore a more focused variant of a data poisoning attack: the `Targeted Label Attack`.

Unlike the broad impact caused by random label flipping, a `Targeted Label Attack` has a more specific objective: an adversary aims to cause the trained model to `misclassify specific, chosen target instances` or, more commonly, instances belonging to a particular `target class`. Instead of just reducing overall accuracy, the adversary wants to manipulate the model's behavior in a predictable way for certain inputs.

