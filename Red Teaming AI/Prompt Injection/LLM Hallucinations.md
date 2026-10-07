
In addition to the injection vulnerabilities discussed so far, insecure handling of LLM-generated output can also lead to any other type of injection vulnerability, such as `LDAP injection` or `path traversal`, depending on the context in which the LLM response is used. However, additional types of security vulnerabilities may arise if LLM-generated output is mishandled. One of the most significant potential security issues is the lack of validation for the correctness of LLM-generated responses, including checks for potential LLM hallucinations.

---

## What are Hallucinations, and how are they caused?

LLM hallucinations are instances where LLMs generate nonsensical, misleading, fabricated, or factually incorrect responses. They are particularly challenging to detect as the response is often structured or phrased to suggest confidence.


In addition to providing misinformation, LLMs might also fabricate sources to support the hallucination. In particular, hallucinations may consist of easily detectable factual errors, as in the previous example, sophisticated misinformation, including fabricated sources, or even nonsensical or random sentences that lack logical coherence or meaningful content. This is what makes hallucinations challenging to detect.

Let us take a closer look at the different types of hallucinations:

- `Fact-conflicting hallucination` occurs when an LLM generates a response containing factually incorrect information. For instance, the previous example of a factually incorrect statement about the number of occurrences of a particular letter in a given sentence is a fact-conflicting hallucination.
- `Input-conflicting hallucination` occurs when an LLM generates a response that contradicts information provided in the input prompt. For instance, if the input prompt is `My shirt is red. What is the color of my shirt?` a case of input-conflicting hallucination would be an LLM response like `The color of your shirt is blue`.
- `Context-conflicting hallucination` occurs when an LLM generates a response that conflicts with previous LLM-generated information, i.e., the LLM response itself contains inconsistencies. This type of hallucination may occur in lengthy or multi-turn responses. For instance, if the input prompt is `My shirt is red. What is the color of my shirt?` a case of context-conflicting hallucination would be an LLM response like `Your shirt is red. This is a good looking hat` since the response confuses the words `shirt` and `hat` within the generated response.


Furthermore, some mitigations can be applied in LLM applications, including proper prompt engineering, ensuring clear and concise input prompts, and providing all relevant information to the LLM. It can help to enrich a user's query with relevant external knowledge by fetching applicable knowledge from an external knowledge base and leveraging it to guide the LLM response generation. We can also attempt to measure the LLM's level of certainty and disregard the response if it falls below a configured level of certainty. There are three approaches to measuring the level of certainty:

- `Logit-based`: This requires internal access to the LLM's state and evaluation of its logits to determine the token-level probability, rendering this approach typically impossible as most modern LLMs are closed-source.
- `Verbalize-based`: This estimation prompts the LLM to provide confidence scores directly by appending the prompt with a phrase like `Please also provide a confidence score from 0 to 100`. However, LLMs are not necessarily able to give an accurate estimate of their own confidence, making this approach unreliable.
- `Consistency-based`: This approach attempts to measure certainty by prompting the LLM multiple times and observing the consistency between all generated responses. The idea behind this approach is that an LLM response based on factual information is more likely to be generated consistently than hallucinated responses.