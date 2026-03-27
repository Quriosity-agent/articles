# 🎯 Lenny Skills: 86 Product Management Skills That Turn Claude Code Into Your Product Mentor

> 100+ episodes of Lenny's Podcast distilled into 86 structured Markdown skill files for Claude Code. A plug-and-play arsenal for PMs, founders, and product teams.

## Repo Info

- **GitHub:** [donghaozhang/lenny-skills](https://github.com/donghaozhang/lenny-skills) (forked from [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills))
- **License:** MIT
- **Skill Count:** 86
- **Source:** 100+ [Lenny's Podcast](https://www.lennyspodcast.com/) episodes

![Lenny Skills GitHub Repository](https://opengraph.githubassets.com/1/donghaozhang/lenny-skills)
*Image source: GitHub OpenGraph — donghaozhang/lenny-skills*

---

## What Is This?

Someone took the practical wisdom from 90+ world-class product leaders — Shreyas Doshi, Marty Cagan, Elena Verna, Christina Wodtke, and more — interviewed on Lenny Rachitsky's podcast, and structured it into 86 Markdown skill files.

These aren't just notes. They're **Claude Code Skills** — a mechanism that gives AI agents specialized knowledge for specific tasks. Once installed, when you say "help me write a PRD," Claude automatically invokes the `writing-prds` skill and guides you using frameworks from Maggie Crowley, Bill Carr, and others.

## Skill Coverage

86 skills organized into 8 categories spanning the entire product management lifecycle:

### 📋 Hiring & Team Building
`evaluating-candidates` · `conducting-interviews` · `writing-job-descriptions` · `onboarding-new-hires` · `building-team-culture` · `coaching-pms`

### 🔍 User Research & Discovery
`conducting-user-interviews` · `analyzing-user-feedback` · `usability-testing` · `designing-surveys` · `measuring-product-market-fit`

### 🧭 Strategy & Planning
`defining-product-vision` · `prioritizing-roadmap` · `setting-okrs-goals` · `writing-prds` · `working-backwards` · `problem-definition`

### 🚀 Shipping & Execution
`shipping-products` · `managing-timelines` · `scoping-cutting` · `managing-tech-debt` · `post-mortems-retrospectives`

### 🤝 Leadership & Alignment
`stakeholder-alignment` · `managing-up` · `having-difficult-conversations` · `running-effective-meetings` · `giving-presentations`

### 📈 Growth & Monetization
`designing-growth-loops` · `retention-engagement` · `pricing-strategy` · `user-onboarding`

### 💼 Sales & Go-to-Market
`founder-sales` · `enterprise-sales` · `launch-marketing` · `positioning-messaging`

### 🧠 AI-Specific
`ai-product-strategy` · `ai-evals` · `building-with-llms` · `vibe-coding`

## Inside a Skill File

Each skill is a standardized Markdown file with a consistent structure:

```markdown
---
name: writing-prds
description: Help users write effective PRDs...
---

# Writing PRDs

## How to Help        ← Behavioral guide for the AI
## Core Principles    ← Frameworks with guest attribution
## Questions to Help  ← Discovery questions for the user
## Common Mistakes    ← Anti-patterns to flag
```

The key design choice: every principle is **attributed to a specific guest**. For example, the PRD skill cites Maggie Crowley ("the most important section is background and context"), Bill Carr (Amazon's PR/FAQ methodology), and Aparna Chennapragada ("prototypes over memos in the AI age").

This isn't AI-generated fluff — it's traceable, sourced advice from real practitioners.

## Installation

Four options, from easiest to most customizable:

```bash
# 1. CLI install (recommended)
npx skills add RefoundAI/lenny-skills

# 2. Install specific skills only
npx skills add RefoundAI/lenny-skills --skill evaluating-candidates writing-prds

# 3. Clone + Copy
git clone https://github.com/RefoundAI/lenny-skills.git
cp -r lenny-skills/skills/* .claude/skills/

# 4. Git Submodule (easy updates)
git submodule add https://github.com/RefoundAI/lenny-skills.git .claude/lenny-skills
```

Skills land in `.claude/skills/` and Claude Code automatically discovers them.

## Usage

Just talk naturally:

| What You Say | Skill Triggered |
|-------------|-----------------|
| "Help me evaluate this PM candidate" | `evaluating-candidates` |
| "I need to write a PRD for our new feature" | `writing-prds` |
| "How do I get stakeholder buy-in?" | `stakeholder-alignment` |
| "We're not shipping fast enough" | `shipping-products` |

You can also invoke skills directly with `/skill-name`.

## Why This Repo Matters

1. **Skills are the knowledge-layer infrastructure for AI agents.** This repo demonstrates a replicable pattern: structure domain expertise into Markdown files and inject them into AI agents. The same approach works for design, engineering, marketing, legal — any domain.

2. **The bridge from "general AI" to "expert AI."** Claude's general knowledge is strong, but with these skill files, its product advice goes from generic platitudes to "as Marty Cagan says..." with real frameworks and attribution.

3. **Open source and extensible.** MIT license. Fork it, add your company's product playbook, contribute improvements back. The repo actively welcomes PRs.

4. **A new paradigm for product knowledge.** Product wisdom used to live in books, courses, and podcast episodes you'd never re-listen to. Now it's a set of Markdown files in `.claude/skills/` that actively participate in your workflow.

## Who Should Use This

- **PMs / Product Leads:** Upgrade your daily AI assistant with expert-level product guidance
- **Founders:** When you don't have a product team, let AI play product advisor
- **Product Teams:** Align everyone on shared product methodology
- **AI Builders:** Study how the Skills mechanism is designed — it's a good reference implementation

## One-Liner

86 skills distilled from top product leaders' podcast interviews, turning Claude Code from a generic assistant into a product management expert. This isn't just a repo — it's a compelling example of the "AI agent + domain knowledge" paradigm.

---

🦞
