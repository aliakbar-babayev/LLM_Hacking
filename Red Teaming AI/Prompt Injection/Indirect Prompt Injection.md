


---

After discussing direct prompt injection, we will discuss **indirect** prompt injection. Indirect prompt injection attacks occur when an attacker can place a payload in a resource, which is subsequently fed to an LLM. The critical difference to direct prompt injection is that the attacker does not **directly** interact with the LLM but rather through an indirection.

For example, consider an LLM that is tasked with summarizing incoming emails. If an attacker can send an email containing a prompt injection payload to the LLM, prompt injection vulnerabilities may occur. However, since the attacker does not feed the payload directly to the LLM but rather indirectly via an email, which is subsequently used in the LLM prompt, it is an **indirect** prompt injection attack.


## URL-based Indirect Prompt Injection

A common task for LLMs is creating summaries for large bodies of text, such as documents or websites. Search engines like Google or Bing may utilize LLMs to display a website summary before a user clicks on a search result.


## SMTP-based Indirect Prompt Injection

The last scenario in this section is based on an Email summary bot. If we send an email to `admin@llm.htb` using the SMTP server, an LLM will summarize the email contents. To test this, we can use the command line utility `swaks` to send emails, which can be installed using the package manager `apt`