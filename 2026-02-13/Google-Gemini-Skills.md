# Google Gemini API Skills — Official Skill Library

> Source: Logan Kilpatrick (Google) on X + GitHub
> Tweet: https://x.com/officiallogank/status/2022123808296251451
> Repo: https://github.com/google-gemini/gemini-skills

---

## What Is It?

Google released an official **skills library for the Gemini API**. Skills are reusable, versioned instruction bundles that agents can load on demand — aligned with the emerging **Agent Skills open standard** (same concept OpenAI just shipped).

The repo currently contains one skill: **gemini-api-dev** — best practices for building apps that use the Gemini API.

---

## Installation

```bash
# List available skills
npx skills add google-gemini/gemini-skills --list

# Install gemini-api-dev skill globally
npx skills add google-gemini/gemini-skills --skill gemini-api-dev --global

# Or via Context7 CLI
npx ctx7 skills install /google-gemini/gemini-skills gemini-api-dev
```

---

## Why It Matters

- **Agent Skills as a standard**: Both OpenAI and Google are now shipping skills — reusable procedure bundles that agents load when needed, instead of bloating system prompts
- **Convergence**: The industry is aligning on the same pattern — SKILL.md manifests, versioned bundles, on-demand loading
- **Practical**: `gemini-api-dev` gives agents up-to-date Gemini API best practices without manual prompt engineering
- **Early stage**: Only 1 skill so far (19 commits, 784 stars), but the infrastructure is there for community contributions

---

## Context

Logan Kilpatrick (Google's Gemini developer relations lead) announced this alongside OpenAI's own skills release — showing both major AI providers are betting on the same agentic primitive pattern: **Skills + Execution + Context Management**.

---

*Collected: 2026-02-13*
