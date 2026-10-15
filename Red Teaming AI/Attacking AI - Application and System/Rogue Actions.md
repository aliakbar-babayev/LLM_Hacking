
In ML applications, `rogue actions` refer to unintended behaviors or operations carried out via system extensions, such as LLM plugins or agents. These actions may arise accidentally due to poor alignment between the model input and the system's constraints, or malicious adversaries may trigger them intentionally by exploiting vulnerabilities or using prompt injection. As such, it can be challenging to determine if a rogue action was caused by the inherent randomness of ML models or an adversary's malicious input. Due to the increasing modularity and extensibility of ML applications, agents are often granted access to plugins or extensions to enhance their functionality. These can include APIs, automation routines, or third-party integrations. While these extensions are intended to expand the agent's capabilities, they also significantly increase the attack surface. If an agent is not properly sandboxed or its actions are not adequately restricted, it might execute harmful commands that impact data integrity, privacy, or system operations.


## Directly Exploiting Rogue Actions

Excessive agency in ML applications refers to scenarios where a model is given too much autonomy to make decisions or perform actions without adequate human oversight, which can potentially lead to unintended consequences. For instance, when LLMs are empowered to execute actions based on natural language commands, such as sending emails, modifying codebases, or making purchases, there is a risk of overstepping user intent, misinterpreting ambiguous instructions, or being exploited by prompt injection or other adversarial inputs. Thus, excessive agency may directly result in rogue actions.

## Indirectly Exploiting Rogue Actions

Indirect malicious user inputs can also cause rogue actions. For instance, [this](https://embracethered.com/blog/posts/2023/chatgpt-plugin-vulns-chat-with-code/) blog post details an attack vector similar to the `exfiltration attacks` discussed in the [LLM Output Attacks](https://academy.hackthebox.com/module/details/307) module. By providing an indirect prompt injection payload that calls a plugin, the LLM can be coerced to take actions on behalf of other users.


## Mitigations

A layered security approach is required to mitigate rogue actions. A fundamental control is the implementation of strict `agent and plugin permission frameworks`. Similar to permission models used in traditional applications, each plugin should have a clearly defined set of capabilities, such as read-only access to files, limited network calls, or restrictions on executing certain commands. These permissions must be explicitly declared, reviewed, and granted in accordance with the `principle of least privilege`. Dynamic permission revocation and runtime auditing can further help restrict access abuse or privilege escalation.

Furthermore, we need to ensure `user control`, giving end-users or administrators ultimate authority over what actions are performed. Typical implementations include mechanisms for approving or denying sensitive actions, such as a confirmation prompt before an action is executed. This enables users to detect and prevent rogue actions.