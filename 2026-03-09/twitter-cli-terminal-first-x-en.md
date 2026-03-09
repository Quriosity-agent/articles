# twitter-cli: A Terminal-First Client for Twitter/X — No API Key Required

> **TL;DR**: A Python CLI tool that uses browser cookies instead of Twitter API keys to do nearly everything on X/Twitter from the terminal — timelines, search, bookmarks, posting, replying, liking, retweeting. Includes an engagement scoring system and AI agent integration (SKILL.md + ClawHub).

---

## Why This Exists

Twitter/X's API now costs $100/month for Basic access, with increasing restrictions. Most developers and AI agents only need common operations (read feed, post, search) that don't require the official API — browser cookies are sufficient.

twitter-cli does exactly this: **uses your logged-in browser cookies to call Twitter's internal GraphQL API directly**.

---

## What It Can Do

**Read operations:**
- `twitter feed` — For You / Following timeline
- `twitter favorites` — bookmarks
- `twitter search "keyword"` — search (Top/Latest/Photos/Videos tabs)
- `twitter tweet <id>` — tweet detail + replies
- `twitter list <id>` — Twitter List timeline
- `twitter user <name>` — user profile
- `twitter user-posts / likes / followers / following` — user content

**Write operations:**
- `twitter post "content"` — post a tweet
- `twitter post "reply" --reply-to <id>` — reply
- `twitter delete <id>` — delete
- `twitter like / unlike / retweet / unretweet / favorite / unfavorite`

**All commands support `--json` output** for scripting and AI agent consumption.

---

## Installation

```bash
# Recommended: uv (fast, isolated)
uv tool install twitter-cli

# Or pipx
pipx install twitter-cli
```

---

## Authentication

**Priority order:**
1. Environment variables `TWITTER_AUTH_TOKEN` + `TWITTER_CT0`
2. Auto-extract from browser cookies (Chrome/Edge/Firefox/Brave)

No API key application needed. No OAuth flow. Just log into x.com and it works.

⚠️ Cookie-based auth carries platform risk. Use a dedicated account. Cookies stay local and are never uploaded.

---

## Smart Filtering System

Disabled by default. Enable with `--filter`:

```bash
twitter feed --filter          # sort by engagement score
twitter feed --filter --max 50 # top 50
```

**Scoring formula:**
```
score = likes × 1.0
      + retweets × 3.0
      + replies × 2.0
      + bookmarks × 5.0
      + log10(views) × 0.5
```

Weights are configurable in `config.yaml`. Three modes:
- **topN** — keep top N by score
- **score** — keep only those >= minScore
- **all** — sort all by score and return everything

---

## AI Agent Integration

The most interesting part. twitter-cli ships with SKILL.md for direct AI agent use:

```bash
# Option 1: Clone to skills directory
git clone git@github.com:jackwener/twitter-cli.git .agents/skills/twitter-cli

# Option 2: npx skills
npx skills add donghaozhang/twitter-cli

# Option 3: ClawHub
clawhub install twitter-cli
```

Once installed, Claude Code / OpenClaw / Codex can execute Twitter operations directly.

**Real-world use cases:**
- AI agent monitoring keyword mentions
- Scheduled posting (with `/loop` or cron)
- Auto-replying to mentions
- Scraping competitor tweets for analysis
- Piping Twitter data into other workflows

---

## Code Structure

```
twitter_cli/
├── cli.py          # Click CLI entry point
├── client.py       # Twitter GraphQL API client
├── auth.py         # Cookie auth (browser extraction + env vars)
├── config.py       # YAML config loading
├── filter.py       # Engagement scoring engine
├── formatter.py    # Terminal colored output
├── serialization.py # JSON serialization
└── models.py       # Data models
```

---

## Comparison With Alternatives

- **Official X API v2** — $100/month, rate-limited, but most stable
- **vxTwitter API** — free but read-only single tweets, no search/write
- **Chrome Relay** — full functionality but requires open browser, not great for automation
- **twitter-cli** — free, CLI-friendly, read+write, AI agent ready, but cookie-dependent (platform risk)
- **Scrapling** — anti-detection scraper, lower level, requires custom parsing

**twitter-cli's sweet spot:** cheaper than the API, lighter than browser automation, easier than raw scraping.

---

## Sibling Tools

Same author also built:
- **xhs-cli** — Xiaohongshu (小红书) CLI for notes and account workflows
- **bilibili-cli** — Bilibili CLI for videos, users, search, and feeds

All three share the same design philosophy: cookie auth + CLI first + JSON output + AI agent integration.

---

## Links

- GitHub: <https://github.com/donghaozhang/twitter-cli>
- PyPI: <https://pypi.org/project/twitter-cli/>
- SKILL.md: <https://github.com/donghaozhang/twitter-cli/blob/main/SKILL.md>

---

*Written 2026-03-09 by 🦞*
