# Anthropic Releases Financial Services Plugin Suite: Turning Claude into a Wall Street Analyst

**Source: GitHub - anthropics/financial-services-plugins**

---

## TL;DR

Anthropic has open-sourced a suite of Claude plugins for financial services, covering investment banking, equity research, private equity, and wealth management. With 41 skills, 38 commands, and 11 data connectors, Claude can now directly output professional-grade financial models, research reports, and deal materials.

---

## What Is This?

A set of plugins designed for **Claude Cowork** (Anthropic's enterprise collaboration product) and **Claude Code**. These aren't generic chat enhancements — they're **industry-specific workflow engines** that transform Claude from "can talk about finance" to "can do finance work."

The core design principle: **Pure Markdown + JSON. Zero code, zero infrastructure, zero build steps.** All domain knowledge, workflows, and best practices are encoded in files that Claude automatically invokes at runtime.

---

## Five Plugin Modules

### 1. Financial Analysis (Core Plugin — Install First)

The shared foundation providing all data connectors and universal modeling capabilities:

- **Comparable Company Analysis** — `/comps AAPL` to generate instantly
- **DCF Valuation Model** — Includes Python validation scripts
- **LBO Model** — Leveraged buyout returns analysis
- **3-Statement Model** — Auto-populate from SEC filings (income statement, balance sheet, cash flow)
- **Presentation QC** — Check data consistency and formatting in slide decks
- **Competitive Analysis** — Porter's Five Forces, SWOT, and other frameworks

### 2. Investment Banking

Full coverage of day-to-day IB workflows:

| Command | Function |
|---------|----------|
| `/cim` | Generate Confidential Information Memorandum |
| `/teaser` | Draft project teaser |
| `/buyer-list` | Build potential buyer list |
| `/merger-model` | Merger model analysis |
| `/one-pager` | One-page company profile |
| `/deal-tracker` | Track deal milestones |
| `/process-letter` | Draft process letters |

Also includes a Pitch Deck skill with complete XML references, formatting standards, and slide templates.

### 3. Equity Research

A full toolkit for sell-side analysts:

- **Earnings Analysis** — Rapid post-earnings update reports
- **Initiating Coverage** — Five-step workflow from company research to valuation to chart generation
- **Morning Notes** — Automated daily briefings
- **Catalyst Calendar** — Track price-moving events
- **Thesis Tracker** — Maintain and update investment theses

### 4. Private Equity

- **Deal Screening** — `/screen-deal` for quick evaluation
- **Due Diligence Checklist** — `/dd-checklist` for systematic review
- **IC Memo** — `/ic-memo` for investment committee materials
- **Returns Analysis** — IRR/MOIC/DPI calculations
- **Portfolio Monitoring** — Track portfolio company KPIs

### 5. Wealth Management

- **Client Meeting Prep** — `/client-review`
- **Financial Planning** — `/financial-plan`
- **Portfolio Rebalancing** — `/rebalance`
- **Tax-Loss Harvesting** — `/tlh` to identify tax-saving opportunities
- **Client Reports** — `/client-report` auto-generation

---

## 11 Data Connectors (MCP)

All connectors are centralized in the core plugin via MCP (Model Context Protocol):

| Provider | Coverage |
|----------|----------|
| **Daloopa** | Automated financial data extraction |
| **Morningstar** | Fund and stock analytics |
| **S&P Global** | Capital IQ data |
| **FactSet** | Comprehensive financial data |
| **Moody's** | Credit ratings and risk |
| **MT Newswires** | Real-time news |
| **Aiera** | Earnings call analysis |
| **LSEG** | Fixed income, FX, macro |
| **PitchBook** | PE/VC deal data |
| **Chronograph** | Alternative investment management |
| **Egnyte** | Document management |

Two partner-built plugins are also available: **LSEG** (8 specialized commands for bonds, FX, options, macro) and **S&P Global** (tearsheets, earnings previews, funding digests).

---

## Architecture Highlights

### Pure File-Driven, Zero Code

```
plugin-name/
├── .claude-plugin/plugin.json   # Plugin manifest
├── .mcp.json                    # Data connector config
├── commands/                    # Slash commands (Markdown)
└── skills/                      # Domain knowledge (Markdown)
```

Each skill is a Markdown file defining trigger conditions and workflow steps. Claude automatically matches and executes them based on context. This means:
- **No deployment** — Edit a Markdown file and it takes effect immediately
- **Easy to customize** — Swap in your firm's terminology, templates, and processes
- **Version control friendly** — Managed via Git, reviewable through PRs

### End-to-End Workflows

Not a collection of point tools, but complete pipelines:
- **Research → Report**: Pull data → analyze earnings → generate research reports
- **Data → Excel**: Auto-generate Comps/DCF/LBO workbooks with live formulas
- **Analysis → PowerPoint**: From data to branded presentation decks

---

## Customization

Anthropic explicitly positions these plugins as **starting points, not endpoints**:

1. **Swap data sources** — Edit `.mcp.json` to point at your internal systems
2. **Add firm context** — Write your terminology and processes into skill files
3. **Import templates** — Use `/ppt-template` to teach Claude your branded PPT style
4. **Adjust workflows** — Modify instructions to match how your team actually works

---

## Why This Matters

The real significance isn't that "AI can calculate a DCF" — it demonstrates a pattern: **encoding industry expert knowledge into pure Markdown files to turn an LLM into a domain specialist.**

This pattern is entirely replicable across legal, healthcare, consulting, and any professional services domain. The 41 skill files are essentially 41 operations manuals on "how to work like a senior analyst" — except the reader is an AI.

---

*Repository: <https://github.com/anthropics/financial-services-plugins>*
*Article compiled from the open-source repository.*
