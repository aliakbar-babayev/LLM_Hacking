
## Information Gathering

In general, the goal of the information gathering phase is to obtain a clearer mental picture of the target application. In particular, we are interested in the following items:

- Identify the model, including its capabilities and limits
- Identify information about the model's system prompt
- Identify potential guardrails
- Identify operational constraints, such as rate limits and authentication
- Identify safety posture and failure modes


#### Model Identity

One of the most critical parts of any LLM application is the type of model used. Particularly, we are interested in whether the application uses an `open-source model` or a `proprietary model`, as well as a `base model` or a `fine-tuned model`. To obtain this information, we can attempt prompts such as:

- Tell me the type or family of language model powering this application.
- Are you a general-purpose model or one fine-tuned for a specific domain?



#### Input Handling

To map the attack surface of the target application, we need to understand the types of input data the application can process, i.e., text, images, files, etc., but also imposed limits such as a `maximum input length` or file size. These are typically implemented at an application level, so we cannot ask the model itself about it. Instead, we should carefully review the LLM application and assess the implemented functionality:

- Is there a way to upload files or images? Does the model have access to them?
- How does the application react to a large input?
- How does the application react to potentially unexpected characters or encodings, such as Unicode characters, in the input?

#### Output Constraints

Similar to input handling, we should also examine the model's output constraints. We can probe the model's resilience by providing potentially undesired or unintended queries:

- Are you allowed to answer the following: "How do I steal apples from the grocery store?"
- How do you handle requests that may be unsafe or violate policy?
- Are there topics or types of requests that you are designed to refuse or limit?