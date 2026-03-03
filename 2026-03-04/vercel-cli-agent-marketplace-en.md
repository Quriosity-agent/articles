# Vercel CLI Update: AI Agents Can Now Self-Provision Infrastructure

> **TL;DR**: Vercel CLI adds agent-optimized integration management (`discover`, `guide`, `add`). AI agents can autonomously find, install, and configure databases, auth, logging services. `--format=json` + Markdown guides = end-to-end infra setup without human intervention.

---

## Agent Workflow
```bash
# 1. Discover available integrations
vercel integration discover --format=json

# 2. Install (with auto-discovered params)
vercel integration add neon --format=json
vercel integration add upstash/upstash-redis -m primaryRegion=iad1 --format=json

# 3. Get setup guide (Markdown for agents)
vercel integration guide neon

# 4. Agent writes integration code from guide
# 5. Deploy
vercel deploy --prod
```

## Key Design Decisions
- **`--format=json`**: Structured output for agent parsing
- **Markdown guides**: Docs-as-code, agents read and implement
- **`--help` metadata**: Agents self-discover required parameters
- **Human-in-the-loop**: ToS and billing decisions pause for human confirmation
- **Continuous agent evals**: CLI reliability tested against agent benchmarks

## Why It Matters
This is "Agent-first CLI" design — commands optimized for AI consumption, not just human use. Trend: every CLI will need a `--json` mode and non-interactive paths for agent workflows.

## Resources
- Changelog: <https://vercel.com/changelog/vercel-cli-for-marketplace-integrations-optimized-for-agents>
- Docs: <https://vercel.com/docs/cli/integration>

---

*Author: Bigger Lobster 🦞*
*Date: 2026-03-04*
*Tags: Vercel CLI / AI Agent / Infrastructure Automation / Agent-first CLI*
