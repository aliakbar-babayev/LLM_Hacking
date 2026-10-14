
`AI data attacks` corrupt systems by going after the data the model learns from or the stored model artifact itself. That makes them fundamentally different from two other attack families covered in other topics. `Evasion attacks` manipulate inputs at inference time to fool a deployed model. `Privacy attacks` extract sensitive information the model has memorized.

The attacks here work earlier.

They corrupt the data the model learns from or the format it is stored in. By the time the model serves a prediction, the damage is already inside it.

![Diagram showing Attack Surface with objectives: Data Poisoning, Storage Tampering, Processing Manipulation, Model Poisoning, Deployment Injection, Retraining Exploitation, targeting AI Data Pipeline Stages: Data Collection, Storage, Data Processing, Analysis & Modeling, Deployment, Monitoring & Maintenance.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/302/pipeline_attacks.png)

Every pipeline stage has a corresponding attack type. The sections below walk through each one using the two concrete examples from the previous section (the e-commerce recommendation system and the healthcare diagnostic tool) so the attack descriptions stay grounded in systems we have already mapped.

![Diagram showing Adversary injecting malicious data into Data Collection Stage, leading to Data Poisoning, resulting in Corrupted Training Set and Compromised AI Model.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/302/data_collection_attacks.png)

Collection is exactly where `data poisoning` enters the pipeline. The attacker injects malicious data at the source, not by breaking in, but by simply using the same input channels the system already trusts. The injected data is crafted for a specific downstream effect, typically `label flipping` (changing what the model thinks a sample means) or `feature attacks` (perturbing the input values a sample carries).

But if enough poisoned samples reach the training set, the CNN learns a version of the diagnostic task that inherently includes the attacker's distortions: wrong classifications, systemic biases, or triggered behaviors that only activate under specific input conditions.

![Diagram showing Adversary gaining unauthorized access to Storage System, leading to theft/tampering of datasets and models, and model replacement with Trojan, affecting AWS S3/Secure FS.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/302/stor_age_attacks.png)

The effect is not wrong predictions. It is code execution. A compromised `.pkl` loaded by the `Flask` API server gives the attacker a solid foothold on the serving infrastructure, while a compromised `.pt` loaded by the clinical system gives access to the entire healthcare network.

![Diagram showing Adversary manipulating processing logic in Data Processing Stage, leading to corrupted processed data and indirect downstream model impact.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/302/processing_attacks.png)

Processing-stage attacks do not directly target data. They target the code that transforms data.

The distinction matters immensely. If an attacker compromises the cleaning, transformation, or feature engineering logic, they can corrupt data that was perfectly clean when it arrived. The raw data upstream still passes any audit. The corruption happens inside the pipeline's own processing step, which makes it significantly harder to detect.

Consider the e-commerce platform. Compromising the `Spark` job that runs sentiment analysis on reviews could easily flip sentiment labels: positive reviews get tagged negative, and negative reviews get tagged positive.

That is a textbook `label flipping` attack, but it did not require touching a single raw review. It required modifying a job configuration or injecting code into a processing script.