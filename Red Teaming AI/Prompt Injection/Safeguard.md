


Finally, to conclude our discussion on abuse attacks, let us examine two case studies for safeguards: [Google's Model Armor](https://cloud.google.com/security-command-center/docs/model-armor-overview) and [Google's ShieldGemma](https://arxiv.org/pdf/2407.21772). These safeguards can be integrated into LLM deployments to mitigate abuse attacks, as they can detect hate speech in user inputs and model outputs. However, neither safeguard aids in the detection of misinformation.

Similar safeguards, such as [Meta's Prompt Guard](https://www.llama.com/docs/model-cards-and-prompt-formats/prompt-guard/), can provide similar functionality. However, since Prompt Guard only provides protection from prompt attacks such as `prompt injection` and `jailbreaking` and does not aid in preventing abuse attacks, we will not consider it in this section.

## Model Armor

Model Armor is a service that can be integrated into AI deployments to enhance security against both prompt attacks and abuse attacks. In order to benefit from Model Armor, the AI application interacts with it as a sanitization layer. A typical data flow could look like this:

1. The user sends a prompt to the AI application.
2. The AI application sends the user prompt to Model Armor for inspection. Model Armor checks for potential attack vectors, such as prompt injection payloads, and returns the sanitized prompt.
3. The sanitized prompt is sent to the LLM.
4. The LLM returns a generated response to the sanitized input prompt.
5. The LLM-generated response is sent to Model Armor for inspection. Model Armor checks for potentially dangerous content, such as hate speech, and returns the sanitized response.
6. The sanitized response is sent to the user.

![Diagram showing interaction flow: User sends prompt to Application Service, which inspects and sanitizes it. LLM processes sanitized prompt and returns a response. Model Armor inspects and sanitizes the response before returning it to the user.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/307/diag1.png)


## ShieldGemma

ShieldGemma is an LLM-based safeguard built on the `Gemma` model. It was fine-tuned to aid in detecting hate speech and harassment in user input and LLM-generated responses. While Model Armor is a fully operational service that can be integrated into AI deployments, ShieldGemma is an LLM that requires manual integration into a deployment by running and querying ShieldGemma directly. The data flow in such a setting could be similar to Model Armor, where ShieldGemma is queried on the user's input prompt before the actual LLM and queried again on the LLM's generated response before it is served to the user.

ShieldGemma operates on a similar definition of these terms compared to Model Armor:

- `Hate speech`: content targeting identity and/or protected attributes (e.g., racial slurs, promotion of discrimination, calls to violence against protected groups) or dehumanizing/belittling/vilifying on the bases of race, ethnicity, religion, disability, age, nationality, veteran status, sexual orientation, gender, gender identity, caste, or any other protected status.
- `Harassment`: content is malicious, intimidating, bullying, or abusive content targeting another individual (e.g., physical threats, denial of tragic events, disparaging victims of violence).