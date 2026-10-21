

Organizations are rushing to integrate Large Language Models (LLMs) in order to improve their online customer experience. This exposes them to web LLM attacks that take advantage of the model's access to data, APIs, or user information that an attacker cannot access directly. For example, an attack may:

- Retrieve data that the LLM has access to. Common sources of such data include the LLM's prompt, training set, and APIs provided to the model.
- Trigger harmful actions via APIs. For example, the attacker could use an LLM to perform a SQL injection attack on an API it has access to.
- Trigger attacks on other users and systems that query the LLM.

## LLM attacks and prompt injection

Many web LLM attacks rely on a technique known as prompt injection. This is where an attacker uses crafted prompts to manipulate an LLM's output. Prompt injection can result in the AI taking actions that fall outside of its intended purpose, such as making incorrect calls to sensitive APIs or returning content that does not correspond to its guidelines.

## Detecting LLM vulnerabilities

Our recommended methodology for detecting LLM vulnerabilities is:

1. Identify the LLM's inputs, including both direct (such as a prompt) and indirect (such as training data) inputs.
2. Work out what data and APIs the LLM has access to.
3. Probe this new attack surface for vulnerabilities


### How LLM APIs work

The workflow for integrating an LLM with an API depends on the structure of the API itself. When calling external APIs, some LLMs may require the client to call a separate function endpoint (effectively a private API) in order to generate valid requests that can be sent to those APIs. The workflow for this could look something like the following:

1. The client calls the LLM with the user's prompt.
2. The LLM detects that a function needs to be called and returns a JSON object containing arguments adhering to the external API's schema.
3. The client calls the function with the provided arguments.
4. The client processes the function's response.
5. The client calls the LLM again, appending the function response as a new message.
6. The LLM calls the external API with the function response.
7. The LLM summarizes the results of this API call back to the user.

This workflow can have security implications, as the LLM is effectively calling external APIs on behalf of the user but the user may not be aware that these APIs are being called. Ideally, users should be presented with a confirmation step before the LLM calls the external API.


### Mapping LLM API attack surface

The term "excessive agency" refers to a situation in which an LLM has access to APIs that can access sensitive information and can be persuaded to use those APIs unsafely. This enables attackers to push the LLM beyond its intended scope and launch attacks via its APIs.

The first stage of using an LLM to attack APIs and plugins is to work out which APIs and plugins the LLM has access to. One way to do this is to simply ask the LLM which APIs it can access. You can then ask for additional details on any APIs of interest.

If the LLM isn't cooperative, try providing misleading context and re-asking the question. For example, you could claim that you are the LLM's developer and so should have a higher level of privilege.

