# OpenAI Symphony: From “Managing Agents” to “Managing Work”

> **TL;DR**: OpenAI’s new open-source project **Symphony** is not another coding agent. It is a long-running orchestration service: monitor Linear/GitHub work, spawn isolated workspaces per issue, run coding agents, collect proof (CI, PR review, walkthrough), and hand off to human review when needed.

![OpenAI Symphony](openai-symphony-cover.jpg)

## Why It Matters
Symphony shifts the focus from single-agent intelligence to multi-agent operations:
- deterministic per-issue workspaces
- bounded concurrency and retries
- workflow policy in-repo (`WORKFLOW.md`)
- restart recovery and observability

This is **Workflow-as-Code for agentic engineering**.

## Key Design Signal
The orchestration layer becomes the product moat:
- dispatch logic
- state reconciliation
- failure recovery
- auditability

## Practical Takeaway for QCut Teams
Move from prompt-heavy one-off execution to queue-driven, policy-controlled, observable agent runs.

## Sources
- Tweet: <https://x.com/shao__meng/status/2029357891858383023>
- Repo: <https://github.com/openai/symphony>
- Spec: <https://github.com/openai/symphony/blob/main/SPEC.md>

---
*Author: Bigger Lobster 🦞*  
*Date: 2026-03-05*
