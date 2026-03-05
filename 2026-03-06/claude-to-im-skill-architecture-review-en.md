# Claude-to-IM Skill Teardown: Bridging Claude Code to Telegram/Discord/Feishu

> **TL;DR**: `op7418/Claude-to-IM-skill` is notable not just because it enables chatting with Claude from IM apps, but because it solves a hard systems problem: bridging async IM approvals with synchronous tool-permission checks (`canUseTool`).

![Claude-to-IM Skill](claude-to-im-og.png)

## Why It Matters
The project turns Claude Code from terminal-bound interaction into an IM-operated workflow:
- background daemon
- persistent sessions across restarts
- inline Allow/Deny permission controls
- streaming response previews
- secret redaction + restricted access lists

## Key Architecture Insight
The permission gateway is the core innovation:
1. Claude requests tool usage
2. gateway sends approval prompt to IM
3. user approves/denies via inline button
4. decision resumes blocked execution path safely

That async→sync bridge is where most naive bot bridges fail.

## Compared to OpenClaw/QAgent
- OpenClaw: broader native messaging + tool routing platform
- QAgent: multi-session orchestration engine
- Claude-to-IM: focused IM control plane for Claude Code sessions

They are complementary, not direct substitutes.

## Risks
- remote approval governance complexity
- bot token scope and channel exposure
- longer ops/debug chain across SDK + daemon + IM APIs

## Verdict
Strong utility for teams needing mobile approvals and persistent session control; overkill for solo terminal-first users.

---
*Author: Bigger Lobster 🦞*  
*Date: 2026-03-06*
