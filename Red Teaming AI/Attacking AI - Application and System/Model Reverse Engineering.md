
Model reverse engineering is an attack on an AI application in which an adversary attempts to reconstruct or approximate the deployed model. By systematically sending inputs to the model through an exposed API and observing the outputs, the adversary collects enough input-output data points to train a `surrogate model` that mimics the original model's behavior. This process can be executed as a black-box attack, i.e., it does not require access to the internal model architecture or training data, making it particularly dangerous for publicly accessible AI applications.

This type of attack poses multiple risks. For commercial ML providers, model reverse engineering can result in intellectual property theft, potentially undermining years of research and development investment. For security-sensitive applications, such as spam detection, facial recognition, or fraud detection systems, an extracted model can be used to probe for vulnerabilities or generate adversarial examples that bypass defenses. Moreover, if the original model is trained on sensitive data, a sufficiently accurate clone could be used for `model inversion attacks`, where the adversary attempts to reconstruct sensitive information about the training data.

## Reverse Engineering an ML Model

Let us explore a basic example of a model reverse engineering attack. Although the following implementation is not feasible for larger and more complex models, the underlying concept remains the same.

#### The Classifier

In this section, we will explore a classifier that classifies two species of penguins, `Adélie` and `Gentoo`, based on their flipper length in Millimeters and body mass in Grams. This classifier is based on a well-known [public dataset](https://allisonhorst.github.io/palmerpenguins/). Furthermore, the classification task does not require a complex classifier. As such, we could easily train a similar classifier ourselves based on the public dataset. However, for this section, we will assume that the training data is not publicly available, such that we need to execute a model reverse engineering attack to obtain our own classifier.

#### Sampling Datapoints

To reverse engineer the model, we first need to sample data points on which to train the surrogate model. For this, we need to generate pairs of flipper length and body mass. We can then run the model on these input pairs to obtain the corresponding output. In the final step, we can use these input-output data points to train our classifier.

In our code, we will use random generation to obtain a large number of input data points. To improve the data quality, we should consider prior information in our random sampling process. For instance, we could research a realistic range of penguin flipper lengths and body masses to obtain lower and upper boundaries. This ensures that we only obtain high-quality data points in our random sampling, thereby improving training performance by reducing the number of data points required for the training process. Depending on the type of classification problem, we may be unable to define meaningful boundaries for our input data points. In these cases, we need a significantly larger number of data points to successfully reverse-engineer the model, due to the lower quality of the data.

#### Replicating the Model

The final step in reverse engineering the original model is to train the surrogate model on the data obtained in the previous step. One of the main factors deciding the model's quality is the model architecture we choose. While different model architectures are known to perform well for specific tasks, such as CNN architectures for image classification or LLM architectures for text generation, we often do not know the exact architecture used by the original model. As such, it is often impossible to re-create the original model exactly. However, choosing an identical architecture is often not required, as long as we select one that suits the specific task we want the model to accomplish.



