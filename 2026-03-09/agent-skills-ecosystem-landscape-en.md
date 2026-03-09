# The 2026 Agent Skills Ecosystem: From SKILL.md to a 9,000+ Marketplace

> **TL;DR**: The AI coding agent "skills" ecosystem exploded in early 2026. Vercel's `npx skills` CLI, Apify's scraper skills, AgentSkillsHub's 9,000+ index, SkillsCatalog.ai's enterprise security certification, ClawHub, DataCamp's Top 100 list — a distribution ecosystem built around the SKILL.md file format is rapidly taking shape. This article maps every major player.

---

## Why Now

After Anthropic introduced Agent Skills in late 2025, a simple convention became the de facto standard:

**SKILL.md = a Markdown file + YAML frontmatter**

```markdown
---
name: my-skill
description: What this skill does
---
# My Skill
Instructions for the agent...
```

The power of this format: **zero dependencies, cross-platform, human-readable**. Any agent (Claude Code, Cursor, Codex, OpenClaw, Gemini CLI...) can load it.

An ecosystem quickly formed in layers.

---

## The Ecosystem Layers

### Layer 1: Distribution CLI — `npx skills`

**Vercel Labs** built the "npm for agent skills":

- GitHub: <https://github.com/vercel-labs/skills>
- Supports **40+ agents** (Claude Code, OpenClaw, Codex, Cursor, Gemini CLI, Windsurf...)
- Installs directly from GitHub repos — no npm publish needed
- `npx skills add owner/repo` — auto-detects local agents, symlinks to correct directories
- `npx skills find` — fzf-style interactive search

**Key design: skills live on GitHub, the CLI is just a courier.** No centralized registry. Distribution via Git.

### Layer 2: Content Repositories — Who's Making Skills

- **vercel-labs/agent-skills** — Vercel's official skills (frontend design guidelines, etc.)
- **Apify agent-skills** — 55+ web scraper skills (Google Search, LinkedIn, Amazon, etc.), calling Apify Actors via MCP
- **VoltAgent awesome-agent-skills** — 100+ community-curated skills with companion MCP server
- **OpenClaw/ClawHub** — OpenClaw's native skill marketplace
- **Company-built** — Linear, Notion, Convex and others have official skills

### Layer 3: Discovery and Indexing

This is where competition is fiercest:

**AgentSkillsHub.top**
- 9,000+ skills indexed
- Aggregates multiple sources
- Pure search/discovery platform, no distribution

**skills.sh** (Vercel official)
- Search platform
- Pairs with `npx skills` CLI

**SkillsCatalog.ai (The Trust Registry)**
- Focus: **security certification**
- Every skill scanned for vulnerabilities, secrets, spec compliance
- Playground for cross-agent testing
- Enterprise tier: private catalogs + access control + compliance reporting

**AgentSkills.best**
- Browse by category
- Focused on practical utility

**DataCamp Top 100+**
- Editorially curated list
- Categorized by domain (search, coding, cloud, ML, security, media)

### Layer 4: Security and Governance

**The most underrated layer.** Remember the ClawHub malicious skill incident? (`blueberrywoodsym/twitter` disguised as a Twitter bot, actually stealing SSH keys.)

SkillsCatalog.ai targets this directly:
- Static analysis for security vulnerabilities
- Credential/secret detection
- Spec compliance grading (Grade A-F)
- Safety scores (e.g., 98/100)

**For enterprises, "is this skill safe?" matters more than "is this skill good?"**

---

## Comparison

**Distribution layer:**
- `npx skills` (Vercel) — CLI install from GitHub, 40+ agent support
- ClawHub — OpenClaw native marketplace, `openclaw install`
- Manual Git clone — most primitive but most controllable

**Discovery layer:**
- AgentSkillsHub.top — largest index (9,000+), pure aggregator
- skills.sh — Vercel official, pairs with CLI
- SkillsCatalog.ai — security certification focus
- AgentSkills.best — category browsing
- DataCamp — editorial picks

**Security layer:**
- SkillsCatalog.ai — currently the only systematic security scanner
- Others — rely on community self-review

---

## Skills vs MCP — What's the Difference

Two concepts easily confused:

- **Skills** = packaged instruction sets. Agent loads them and knows *how* to do something (internal knowledge)
- **MCP** = external tool protocol. Agent calls APIs/services through it (external capability)

Analogy:
- Skill = giving an intern an operations manual
- MCP = giving an intern the company door key

They're complementary, not competing. Apify's approach combines both: SKILL.md tells the agent *how to scrape*, the MCP server provides the actual scraping capability.

---

## Trend Analysis

1. **SKILL.md is the de facto standard** — 40+ agents support it, no competing format
2. **Distribution is decentralized** — GitHub is the registry, CLI is the courier
3. **Security will be the differentiator** — malicious skill incidents will push enterprises toward certified platforms
4. **Aggregation > self-hosting** — 9,000+ skills means the ecosystem needs search engines
5. **MCP + Skills convergence** — increasingly, skills embed MCP calls

---

## Links

- Vercel Skills CLI: <https://github.com/vercel-labs/skills>
- AgentSkillsHub: <https://agentskillshub.top/>
- SkillsCatalog.ai: <https://skillscatalog.ai/>
- Apify Agent Skills: <https://github.com/apify/agent-skills>
- skills.sh: <https://skills.sh>
- DataCamp Top 100+: <https://www.datacamp.com/blog/top-agent-skills>

---

*Written 2026-03-09 by 🦞*
