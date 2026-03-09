# Apify Agent Skills: Web Scraping Superpowers for AI Coding Assistants

> When your AI coding assistant needs real-world data, Apify Agent Skills gives it 55+ production-grade scrapers out of the box.

## What Is It?

[Apify Agent Skills](https://github.com/apify/agent-skills) is Apify's official skill pack for AI coding assistants, focused on **web scraping, data extraction, and automation**. It works with Claude Code, Cursor, Codex, Gemini CLI, and other AI tools — giving them the ability to scrape Instagram, Google Maps, Amazon, TikTok, and dozens more platforms on command.

Tell your AI "scrape the top-rated coffee shops in Melbourne from Google Maps" and it knows which Actor to use, how to call it, and how to format the results.

## Architecture

The architecture is straightforward:

- **SKILL.md files** — Each skill is a Markdown file with YAML frontmatter (name, description) and detailed instructions
- **mcpc CLI** — Apify's MCP client tool for interacting with Actor APIs
- **Apify Actors** — Serverless scraping programs running on Apify's cloud
- **agents/AGENTS.md** — Auto-generated skill index for tools that don't have plugin systems

The flow:

```
AI Assistant → reads SKILL.md → understands task → calls mcpc CLI → Apify Actor runs → structured data returned
```

## The 12 Skills

- **apify-ultimate-scraper** — Universal scraper covering 55+ Actors, auto-selects the best one
- **apify-lead-generation** — B2B/B2C lead mining (Google Maps, LinkedIn, Instagram, etc.)
- **apify-ecommerce** — E-commerce data (Amazon, Walmart, eBay, IKEA, 50+ marketplaces)
- **apify-brand-reputation-monitoring** — Reviews, ratings, sentiment tracking
- **apify-competitor-intelligence** — Competitor strategy, pricing, ads analysis
- **apify-content-analytics** — Content performance across Instagram, YouTube, TikTok
- **apify-audience-analysis** — Audience demographics and behavior
- **apify-influencer-discovery** — Find and vet influencers
- **apify-trend-analysis** — Trend tracking (Google Trends + social platforms)
- **apify-market-research** — Market conditions and opportunity analysis
- **apify-actor-development** — Build and deploy custom Actors
- **apify-actorization** — Convert existing projects into Apify Actors

## Installation & Usage

### Via vercel-labs/skills CLI (recommended)

```bash
npx skills add apify/agent-skills
```

### Claude Code plugin

```bash
/plugin marketplace add https://github.com/apify/agent-skills
/plugin install apify-ultimate-scraper@apify-agent-skills
```

### Prerequisites

- Apify account + API token (set `APIFY_TOKEN` in `.env`)
- Node.js 20.6+
- mcpc CLI: `npm install -g @apify/mcpc`

### Real-World Example

With `apify-ultimate-scraper` installed, you can tell your AI assistant:

```
Scrape Google Maps for coffee shops in Melbourne rated 4.5+, export as CSV
```

The assistant will:
1. Read SKILL.md to understand available Actors
2. Select `compass/crawler-google-places`
3. Fetch the Actor's input schema via mcpc
4. Build parameters and execute the scrape
5. Format results as CSV

Under the hood:

```bash
export $(grep APIFY_TOKEN .env | xargs) && \
mcpc --json mcp.apify.com \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  tools-call search-actors keywords:="google maps" limit:=10
```

## Comparison with Other Skill Ecosystems

### vs vercel-labs/skills

[vercel-labs/skills](https://github.com/vercel-labs/skills) is Vercel's **universal skill distribution CLI**, not a skill pack itself:

- **vercel-labs/skills** is infrastructure — provides `npx skills add/list/remove/update`, supports 37+ AI coding tools
- **apify/agent-skills** is content — provides concrete scraping skills, distributed via the skills CLI
- They're **complementary**: Apify skills install through Vercel's CLI
- The CLI supports symlink and copy install modes, project-level and global scopes
- Discover skills at [skills.sh](https://skills.sh)

### vs OpenClaw Skills / ClawHub

OpenClaw's skill system takes a different approach:

- **OpenClaw Skills** — Designed for personal AI assistant scenarios; skills can include scripts, configs, and tool integrations (not just Markdown prompts)
- **ClawHub** — Skill marketplace with `clawhub search/install/publish`, npm-style publishing
- **Apify Skills** are more focused — Pure Markdown + external API calls, core capability lives on Apify's cloud
- **OpenClaw Skills** are more flexible — Can contain local scripts, binary tools, complex workflows

The fundamental difference: Apify skills are **instruction documents** (telling AI how to call external APIs), while OpenClaw skills are **capability packages** (potentially including executable code and toolchains).

### Converging Patterns

Across all ecosystems, the core Agent Skills pattern is converging:

- **SKILL.md as the standard format** — YAML frontmatter + Markdown instructions
- **Installation = placing files in convention directories** — Each tool has its own path (`.claude/skills/`, `skills/`, `.agents/skills/`)
- **Auto-discovery by AI** — Tools scan directories at startup and inject skills into context
- **Git repos as distribution units** — GitHub is the package manager

## Who Is This For?

- **Marketing teams** — Competitor analysis, influencer discovery, trend tracking without code
- **Sales teams** — Lead generation, contact extraction
- **Data analysts** — Quick access to social media, e-commerce, and review data
- **Developers** — Call scrapers directly from your AI coding assistant, skip writing scripts

## Caveats

- **Pay-per-use** — Apify Actors charge per result, it's not free
- **Cloud-dependent** — All scraping runs on Apify's infrastructure, no offline mode
- **Overlapping skills** — The 12 skills have significant overlap (ultimate-scraper covers most of what the others do)
- **Markdown instruction limitations** — Skills work by AI interpreting natural language instructions; complex scenarios may need iteration

## Bottom Line

Apify Agent Skills solves a real problem: **AI coding assistants need access to real-world data**. By packaging Apify's powerful scraping capabilities as SKILL.md files, any AI tool with skill support gets professional-grade data extraction.

It's not a silver bullet — you need an Apify account, it costs money, and it requires internet. But for the specific problem of "let my AI assistant scrape the web," it's one of the most mature solutions available today.

The Agent Skills ecosystem is still early, but the trend is clear: **SKILL.md + Git repos + CLI distribution** is becoming the standard pattern for extending AI tool capabilities.

---

🦞
