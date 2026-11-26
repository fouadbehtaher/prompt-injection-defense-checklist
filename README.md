# Prompt Injection Defense Checklist

A practical, defense-first checklist for testing LLM assistants and AI agents against prompt injection. Built for security engineers, bug bounty hunters, and teams shipping AI features.

This repo contains **no working jailbreak payloads**. It organizes the attack surface into test categories and verification items, because that is what actually helps you defend: payloads change weekly, categories do not.

## Why this exists

Prompt injection is OWASP LLM01, the top risk in the OWASP Top 10 for LLM applications. Most public material is either attack write-ups with payloads, or vendor marketing. Defenders need something else: a repeatable way to check whether their assistant treats untrusted text as data, keeps its tools scoped, and asks a human before doing anything irreversible.

## How to use it

1. Read [CHECKLIST.md](CHECKLIST.md) top to bottom once. It starts with authorization and scope, not attacks.
2. Run the categories that apply to your system. Skip what your architecture does not have (no tools = no tool-misuse section).
3. Run the safe planted-content checks in [CANARY-TESTS.md](CANARY-TESTS.md) if your assistant reads email, web pages, documents, or invites.
4. Record every result in [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md), even passes. A finding without evidence is a story.
5. Rerun after every model change, system-prompt change, or new tool integration. Injection defense decays quietly. `regression_runner.py` walks the cases from `cases.json` and writes a versioned Markdown report.

## Scope and ethics

Only test systems you own or are explicitly authorized to test: your own assistant, your own application, a public AI red-team program, or a target whose written scope includes the AI layer. Curiosity is not authorization. Real bypasses in someone else's product go to their security team or bug bounty program through coordinated disclosure, not to social media.

## Contents

| File | What it is |
| --- | --- |
| [CHECKLIST.md](CHECKLIST.md) | The full defensive testing checklist, organized by attack category |
| [CANARY-TESTS.md](CANARY-TESTS.md) | Safe planted-canary recipes for indirect injection and data leaks |
| [TEST-CASES.md](TEST-CASES.md) | 25 abstract test cases: category, description, expected result, severity |
| [cases.json](cases.json) + [regression_runner.py](regression_runner.py) | The same cases in JSON plus an interactive runner that writes a Markdown regression report |
| [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) | A fill-in template for documenting each test and finding |

## Companion article

The story behind this checklist, including what happened when I ran these categories against a defended assistant: on Medium at [@fouadbehtaher](https://medium.com/@fouadbehtaher) (link added on publication).

## License

MIT. Use it, extend it, and open issues with categories you think are missing.
