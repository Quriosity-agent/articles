# Polymarket CLI: Prediction Markets from Your Terminal — and an AI Agent Trading Interface

**Source: GitHub - Polymarket/polymarket-cli**

---

## TL;DR

Polymarket released an official Rust CLI for browsing markets, placing orders, managing positions, and interacting with on-chain contracts — all with `--output json` support, making it a natural fit for scripts and AI agents.

---

## What Is Polymarket?

Polymarket is the largest decentralized prediction market, running on Polygon. Users bet USDC on real-world outcomes ("Will BTC hit $100k?", "Who wins the election?"), with prices reflecting consensus probabilities. During the 2024 US election, a single market exceeded $145M in volume.

---

## What Can the CLI Do?

### No Wallet Needed (Read-Only)

- **Browse markets** — `polymarket markets list --active true`
- **View events** — `polymarket events list --tag ai`
- **Order books** — `polymarket clob book <condition_id>`
- **Price history** — `polymarket clob price-history <id> --interval 1d`
- **On-chain data** — Positions, leaderboards, contract state

### Wallet Required (Trading)

- **Limit orders** — `polymarket clob create-order <id> buy yes 0.55 100`
- **Market orders** — `polymarket clob market-order <id> buy yes 50`
- **Cancel** — Single, by market, or cancel all
- **CTF operations** — Split, merge, redeem conditional tokens
- **Bridge** — Deposit from other chains

### Order Types

| Type | Description |
|------|-------------|
| **GTC** | Good Till Cancelled (default) |
| **FOK** | Fill or Kill |
| **GTD** | Good Till Date |
| **FAK** | Fill and Kill (partial fill, cancel rest) |

---

## Why This Is an AI Agent's Best Friend

The killer feature: **every command supports `--output json`**.

```bash
polymarket markets list --active true -o json
polymarket clob book <condition_id> -o json
polymarket clob trades -o json
```

This means an AI agent can:
1. Parse market data as structured JSON
2. Analyze probability mispricing
3. Place orders automatically
4. Monitor positions and rebalance
5. All scriptable, zero human intervention

Error handling is structured too — JSON mode outputs `{"error": "..."}` to stdout with non-zero exit codes. Automation-friendly by design.

---

## Using OpenClaw + Polymarket to Track AI News

Here's where it gets interesting. With OpenClaw as your orchestration layer, you can set up an **AI news monitoring system** powered by prediction market data:

### Setup: OpenClaw Polymarket Skill

Create a skill at `~/clawd/skills/polymarket/SKILL.md` that wraps the CLI commands. Then your OpenClaw agent can:

```
# Ask your agent naturally:
"What are the current odds on Claude 5 release?"
"Show me all active AI prediction markets"
"What does Polymarket think about GPT-6 timeline?"
```

### Automated AI News Monitoring with Heartbeats

Add to your `HEARTBEAT.md`:

```markdown
## Polymarket AI Watch
- Check active AI prediction markets every 4 hours
- Alert if any AI market price moves >10% in 24h
- Track: Claude 5, GPT-6, AGI timeline, AI company valuations
```

Your OpenClaw agent will periodically scan markets and notify you of significant moves — like a Bloomberg terminal for AI predictions, running on autopilot.

### Real Example: What We Found Today

Running `polymarket events list --tag ai --active true` right now shows:

| Market | Volume | Signal |
|--------|--------|--------|
| Claude 5 released by…? | $2.4M | High interest in Anthropic's next move |
| Best AI model end of June? | $954.8K | Market consensus on model rankings |
| Anthropic IPO market cap | $476.4K | Valuation expectations |
| GPT-6 released by…? | $289.3K | OpenAI timeline bets |
| Chinese AI model #1 by June? | $47.7K | Geopolitical AI race |

**Prediction markets are leading indicators.** When Claude 5 odds spike, it often means insiders or well-informed traders are moving first. Polymarket + OpenClaw gives you that signal before the news breaks.

### Cron Job Setup

```yaml
# In OpenClaw cron config
- name: polymarket-ai-scan
  schedule: "0 */4 * * *"  # Every 4 hours
  task: "Check Polymarket AI markets. Compare prices to yesterday. Alert me if any market moved >10%."
```

---

## Technical Details

- **Language**: Rust (performance + safety)
- **Chain**: Polygon (low gas fees)
- **Tokens**: USDC (stablecoin) + ERC-1155 conditional tokens
- **Wallet**: Private key, env var, or config file
- **Signature types**: Proxy (default), EOA, Gnosis Safe
- **Interactive shell**: `polymarket shell` for REPL mode

### Installation

```bash
# macOS / Linux (Homebrew)
brew install polymarket/tap/polymarket

# Shell script
curl -fsSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh

# From source (Rust required)
cargo install --git https://github.com/Polymarket/polymarket-cli

# WSL on Windows (what we did)
wsl -- bash -c 'source "$HOME/.cargo/env" && cargo install --path .'
```

---

## Why This Matters

1. **Prediction markets as AI radar** — Market prices aggregate information faster than news. A spike in "Claude 5 by Q2" tells you something before the blog post drops.
2. **Agent-native trading** — JSON output + structured errors = built for automation. Imagine an agent that reads Hacker News, cross-references with Polymarket odds, and flags mispriced bets.
3. **DeFi CLI benchmark** — Clean Rust architecture, logical command grouping, consistent output formatting. A design template for DeFi tools.
4. **⚠️ Experimental** — Official warning: early-stage software, don't bet the farm.

---

*Repository: <https://github.com/Polymarket/polymarket-cli>*
*License: MIT*
*Article compiled from the open-source repository.*
