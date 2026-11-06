#!/usr/bin/env python3
"""LLM Hacking Quiz 3: Data Attacks, Application/System Attacks & OWASP Top 10"""

import random

QUESTIONS = [
    {
        "q": "LLM OWASP LLM05: Improper Output Handling.\nAn LLM generates a response containing: <script>alert('xss')</script>\nThe web app renders it without sanitization. What happened?",
        "options": [
            "The LLM was hacked",
            "The app trusts LLM output and renders it as HTML — the attacker used prompt injection to make the LLM generate XSS payloads",
            "The LLM has a JavaScript vulnerability",
            "The browser failed to block the script"
        ],
        "answer": 1,
        "explain": "LLM05: The LLM is just text generation. If the app renders output as HTML/SQL/commands without sanitization, an attacker can inject payloads via the LLM. The LLM becomes a proxy for XSS, SQLi, command injection."
    },
    {
        "q": "What is a 'Sponge Example' attack (Denial of ML Service)?",
        "options": [
            "Sending millions of requests to overwhelm the API",
            "Crafted inputs that maximize energy consumption and latency WITHOUT increasing input size — can drain battery on edge devices",
            "Corrupting the training data so the model becomes useless",
            "Encrypting the model weights with ransomware"
        ],
        "answer": 1,
        "explain": "Sponge Examples increase computational work per input. On battery-powered/edge devices, this can drain the battery entirely. It's DoS at the model inference level, not the network level."
    },
    {
        "q": "MCP (Model Context Protocol) has three capability types. What are they?",
        "options": [
            "Read, Write, Execute",
            "Prompts (user-controlled), Resources (application-controlled, read-only), Tools (model-controlled, state-changing)",
            "Input, Processing, Output",
            "Authentication, Authorization, Accounting"
        ],
        "answer": 1,
        "explain": "MCP capabilities: Prompts = user initiates, Resources = app provides read-only data, Tools = model can trigger actions that change state. Tools are the most dangerous — model-controlled state changes."
    },
    {
        "q": "What is a 'Rug Pull' attack on MCP servers?",
        "options": [
            "Stealing crypto through a malicious MCP server",
            "Initially benign tool description that gets changed to malicious AFTER the user approves the server",
            "Pulling the server offline during a critical operation",
            "Revoking user access to the MCP server"
        ],
        "answer": 1,
        "explain": "Rug Pull: MCP server starts with innocent tool descriptions. User approves. Later, the descriptions change to include malicious instructions. The user already trusted it."
    },
    {
        "q": "What is 'Tool Shadowing' in MCP?",
        "options": [
            "Hiding malicious code inside a legitimate tool",
            "A malicious MCP server provides a tool with the SAME NAME as a legitimate tool to intercept calls meant for it",
            "Monitoring which tools the user accesses",
            "Creating a backup copy of a tool"
        ],
        "answer": 1,
        "explain": "Tool Shadowing: if two MCP servers offer 'read_file', the malicious one can intercept calls. The LLM might route to the wrong server, leaking data or executing malicious actions."
    },
    {
        "q": "Label Flipping attack: you change 5% of 'spam' labels to 'not-spam' in the training data.\nWhat happens to the model?",
        "options": [
            "Nothing — 5% is too small to matter",
            "The model's performance degrades — it becomes confused, lowering accuracy, precision, and recall for spam detection",
            "The model crashes during training",
            "The model becomes 5% less accurate, proportionally"
        ],
        "answer": 1,
        "explain": "Label flipping is the simplest data poisoning. Even small percentages degrade performance because the model learns contradictory patterns. It doesn't crash — it silently becomes worse."
    },
    {
        "q": "How is a Targeted Label Attack different from random Label Flipping?",
        "options": [
            "It targets more labels",
            "It flips labels for SPECIFIC inputs/classes to cause predictable misclassification, not just general degradation",
            "It's faster to execute",
            "It requires more training data"
        ],
        "answer": 1,
        "explain": "Random flipping = degrade overall accuracy. Targeted = make the model misclassify specific things (e.g., always classify a specific malware variant as benign). More surgical, harder to detect."
    },
    {
        "q": "ML OWASP ML03: Model Inversion Attack. What does the attacker achieve?",
        "options": [
            "They reverse the model's training process",
            "They reconstruct training INPUTS from the model's OUTPUTS — e.g., reconstruct faces from a facial recognition model",
            "They flip the model's predictions to the opposite",
            "They convert the model from one framework to another"
        ],
        "answer": 1,
        "explain": "Model Inversion: given a model's output (e.g., 'this is person X'), reconstruct what the input looked like. Privacy nightmare for models trained on faces, medical data, etc."
    },
    {
        "q": "ML OWASP ML04: Membership Inference Attack. What question does it answer?",
        "options": [
            "What members have access to the model?",
            "Was THIS specific data point used in the model's training set?",
            "How many members are in each cluster?",
            "Which team member trained the model?"
        ],
        "answer": 1,
        "explain": "Membership Inference: 'Was my photo/medical record/text used to train this model?' Models behave slightly differently on data they've seen during training vs new data. Privacy violation."
    },
    {
        "q": "An LLM-powered app uses this endpoint: /query/5 where 5 is the conversation ID.\nYou change it to /query/6 and get another user's conversation.\nWhat vulnerability is this?",
        "options": [
            "SQL Injection",
            "IDOR (Insecure Direct Object Reference) — the app doesn't verify you own conversation 6",
            "Broken Authentication",
            "Prompt Injection"
        ],
        "answer": 1,
        "explain": "IDOR in LLM context: the app uses sequential IDs without authorization checks. Classic web vuln, but now exposes AI conversation history, potentially containing sensitive data."
    },
    {
        "q": "LLM OWASP LLM06: Excessive Agency. What does this mean?",
        "options": [
            "The LLM charges too much per API call",
            "The LLM has too many plugins/tools with too much autonomy and not enough oversight — it can take actions the user didn't intend",
            "The LLM generates too much text",
            "The LLM accesses too many knowledge bases"
        ],
        "answer": 1,
        "explain": "Excessive Agency: LLM with database write access, email sending, file deletion — and no confirmation step. Prompt injection + excessive agency = attacker controls real-world actions."
    },
    {
        "q": "Model Reverse Engineering (black-box): How does an attacker steal a model they can only query?",
        "options": [
            "Hack the server and download the weights",
            "Send inputs → observe outputs → train a surrogate model that mimics the original",
            "Record the API responses and replay them",
            "Decompile the API endpoint code"
        ],
        "answer": 1,
        "explain": "Black-box model theft: systematically query the model, collect input-output pairs, train your own model on them. The surrogate approximates the original. Defense: rate limiting, output perturbation."
    },
    {
        "q": "What communication format does MCP use, and what are the two transport options?",
        "options": [
            "REST API; HTTP and gRPC",
            "JSON-RPC; stdio (local) and Streamable HTTP with SSE (remote)",
            "GraphQL; WebSocket and HTTP",
            "Protobuf; TCP and UDP"
        ],
        "answer": 1,
        "explain": "MCP uses JSON-RPC (Request, Response, Notification message types). Transport: stdio for local processes, Streamable HTTP with Server-Sent Events for remote connections."
    },
    {
        "q": "LLM OWASP LLM08: Vector and Embedding Weaknesses.\nA RAG system retrieves poisoned documents. Why is this dangerous?",
        "options": [
            "The embeddings will crash",
            "The poisoned content enters the LLM's context and can contain hidden instructions — the LLM treats them as legitimate context",
            "The vector database will be corrupted permanently",
            "The embeddings will expose the model's weights"
        ],
        "answer": 1,
        "explain": "RAG retrieves documents and stuffs them into the LLM's context. If those documents contain prompt injection payloads, the LLM follows them. The LLM can't distinguish 'real context' from 'injected instructions'."
    },
    {
        "q": "What is Homomorphic Encryption (HE) and why isn't it widely adopted for ML?",
        "options": [
            "It encrypts the model architecture; too complex to implement",
            "It allows computation on ENCRYPTED data without decrypting — but has significant performance overhead",
            "It's a special hash for ML models; too easy to reverse",
            "It encrypts only the training data; doesn't protect inference"
        ],
        "answer": 1,
        "explain": "HE lets you run ML inference on encrypted data — the server never sees plaintext. Dream for privacy. Reality: 10-100x slower. Active research area."
    },
    {
        "q": "LLM OWASP LLM01 vs LLM07: What's the difference between Prompt Injection and System Prompt Leakage?",
        "options": [
            "They're the same vulnerability",
            "Prompt Injection (LLM01) overrides behavior. System Prompt Leakage (LLM07) extracts the hidden system prompt itself. Injection is the method, leakage is one possible goal",
            "LLM01 is input-side, LLM07 is output-side",
            "LLM07 is a subset of LLM01"
        ],
        "answer": 1,
        "explain": "LLM01: hijack what the LLM does. LLM07: reveal what instructions the LLM was given. You might use prompt injection (LLM01) to achieve system prompt leakage (LLM07), but they're separate risks."
    },
    {
        "q": "The ML pipeline has 6 stages: Collection → Storage → Processing → Modeling → Deployment → Monitoring.\nWhere does a 'processing attack' target, and how?",
        "options": [
            "The data collection API — inject false data",
            "The transformation/preprocessing code itself (e.g., compromise a Spark job), not the data directly",
            "The model training loop — inject backdoors",
            "The monitoring dashboard — hide anomalies"
        ],
        "answer": 1,
        "explain": "Processing attacks target the code that transforms data (ETL pipelines, Spark jobs, preprocessing scripts). Compromising the transformation logic is stealthier than poisoning raw data."
    },
    {
        "q": "What tool scans MCP servers for vulnerabilities?",
        "options": [
            "nmap with MCP scripts",
            "mcp-scan",
            "burpsuite MCP extension",
            "wireshark MCP protocol filter"
        ],
        "answer": 1,
        "explain": "mcp-scan checks for tool poisoning, rug pulls, prompt injection in tool descriptions, and other MCP-specific vulnerabilities."
    },
    {
        "q": "LLM OWASP LLM10: Unbounded Consumption. How is this different from a traditional DoS?",
        "options": [
            "It's the same thing — just flood the API",
            "LLMs have variable cost per request. Crafted prompts can trigger enormous token generation, recursive tool calls, or expensive operations — amplifying cost beyond network-level DoS",
            "It targets the model's memory, not the network",
            "It only works against open-source models"
        ],
        "answer": 1,
        "explain": "Unbounded Consumption: one prompt generating 100K tokens, recursive agent loops, massive RAG retrievals. The cost amplification is specific to LLMs — a single request can cost dollars, not cents."
    },
    {
        "q": "An attacker modifies a deployed model's weight file on the server.\nWhat OWASP categories does this fall under (both ML and LLM)?",
        "options": [
            "Only ML05 (Model Theft)",
            "ML10 (Model Poisoning — manipulate weights) and relates to LLM03 (Supply Chain) and LLM04 (Data and Model Poisoning)",
            "Only LLM04 (Data Poisoning)",
            "ML01 (Input Manipulation) and LLM01 (Prompt Injection)"
        ],
        "answer": 1,
        "explain": "ML10 = direct weight manipulation. LLM03 = supply chain (compromised model serving). LLM04 = model poisoning. These overlap because the attack compromises the model itself at deployment."
    },
]


def run_quiz():
    print("=" * 65)
    print("  LLM HACKING QUIZ 3: Data Attacks, Systems & OWASP Top 10")
    print("=" * 65)
    print(f"\n  {len(QUESTIONS)} scenario-based questions.")
    print("  Think about real attack chains, not just definitions.\n")

    questions = QUESTIONS[:]
    random.shuffle(questions)
    score = 0
    wrong = []

    for i, q in enumerate(questions, 1):
        print(f"\n{'─' * 60}")
        print(f"  [{i}/{len(questions)}] {q['q']}\n")

        indices = list(range(len(q["options"])))
        random.shuffle(indices)
        correct_letter = None
        for j, idx in enumerate(indices):
            letter = chr(65 + j)
            if idx == q["answer"]:
                correct_letter = letter
            print(f"    {letter}) {q['options'][idx]}")

        while True:
            ans = input(f"\n  Your answer (A-{chr(64 + len(q['options']))}): ").strip().upper()
            if ans in [chr(65 + j) for j in range(len(q["options"]))]:
                break
            print("  Invalid input. Try again.")

        if ans == correct_letter:
            score += 1
            print(f"\n  ✓ Correct!")
        else:
            print(f"\n  ✗ Wrong. Correct answer: {correct_letter}")
            wrong.append(q)

        print(f"  → {q['explain']}")

    print(f"\n{'=' * 65}")
    print(f"  FINAL SCORE: {score}/{len(questions)} ({score * 100 // len(questions)}%)")
    print(f"{'=' * 65}")

    if wrong:
        print(f"\n  Review these {len(wrong)} topics:")
        for q in wrong:
            print(f"    • {q['q'][:80]}")
    elif score == len(questions):
        print("\n  Perfect score! You understand the full AI attack surface.")
    print()


if __name__ == "__main__":
    run_quiz()
