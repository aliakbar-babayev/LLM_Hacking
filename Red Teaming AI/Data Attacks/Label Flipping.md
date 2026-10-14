
`Label Flipping` is arguably the simplest form of a data poisoning attack. It directly targets the `ground truth information` used during model training.

The idea behind the attack is straightforward: an adversary gains access to a portion of the training dataset and deliberately changes the assigned `labels` (the correct answers or categories) for some data points. The actual features of the data points remain untouched; only their associated class designation is altered.

For example, in a dataset used to classify images, an image originally labeled as `cat` might have its label flipped to `dog`. In a dataset used to train a spam classifier, an email labeled as `spam` might be relabeled as `not spam`.

The most common goal of an attacker executing a `Label Flipping` attack is to `degrade model performance`. By introducing incorrect labels, the attack forces the model to learn incorrect associations between features and classes, resulting in a "confused" model that has a general decrease in performance (eg accuracy, precision, recall, etc).