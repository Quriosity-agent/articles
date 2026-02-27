# AI Code Review Tools Ranked: Martian's Open Benchmark Reveals Who Actually Helps

> **TL;DR**: Martian released Code Review Bench — an open benchmark measuring AI code review tools on real GitHub PRs. Analyzed **1M+ pull requests** using Precision/Recall/F1 to determine which tools' suggestions actually get adopted by developers. Results: **CodeRabbit #1 (F1 51.3%)**, Copilot has the most PRs (643K+) but only 43.5% F1. Surprise: **Cursor has highest precision (67.9%) but lowest recall (36.4%).**

---

## Leaderboard (Last 2 Months)

| Rank | Tool | F1 Score | Precision | Recall | PR Count |
|------|------|---------|-----------|--------|----------|
| #1 | **CodeRabbit** | **51.3%** | 49.2% | 53.5% | 284,696 |
| #2 | **Greptile** | 50.6% | 65.3% | 41.3% | 40,054 |
| #3 | **Gemini Code Assist** | 49.3% | 59.5% | 42.1% | 145,450 |
| #4 | AugmentCode | 47.6% | 62.5% | 38.4% | 3,423 |
| #5 | Cursor | 47.4% | **67.9%** | 36.4% | 46,121 |
| #6 | Claude | 47.1% | 47.5% | 46.7% | 34,328 |
| #7 | KiloConnect | 46.1% | 60.0% | 37.5% | 4,210 |
| #8 | Copilot | 43.5% | 54.5% | 36.2% | **643,212** |
| #9 | Graphite | 40.2% | 64.7% | 29.2% | 5,354 |
| #10 | ChatGPT Codex | 39.8% | 58.3% | 30.2% | 154,584 |

## Key Findings

### CodeRabbit Wins Overall
- F1 51.3%, most balanced Precision/Recall ratio
- 284K PR sample — statistically robust
- **Only tool with Recall above 50%**

### Copilot: Volume != Quality
- Most PRs by far (643K) but only 43.5% F1
- 36.2% Recall means it misses most issues
- **Market share does not equal quality**

### Cursor: Precise but Conservative
- 67.9% Precision — highest in the field. When it flags something, it's usually right
- But 36.4% Recall — misses too many issues
- **Quality over quantity strategy**

### Claude: Most Balanced
- Precision 47.5% and Recall 46.7% nearly equal
- No standout weakness, consistent performer

### ChatGPT Codex: Last Place
- 39.8% F1 on 154K PRs — worst performer at scale
- 30.2% Recall — misses 70% of issues

## Methodology

Not synthetic benchmarks — **real-world PR analysis**:

1. Collect PRs where AI review bots participated on GitHub
2. Full timeline: every suggestion, developer response, code change, resolved thread
3. LLM-powered analysis: did the bot's suggestion lead to actual code changes?
4. Score each PR on Precision, Recall, F1

**Core question: Did the bot's suggestions cause real code changes?**

- **Precision** — What % of bot suggestions were adopted? Higher = less noise
- **Recall** — What % of needed changes did the bot find? Higher = fewer misses
- **F1** — Harmonic mean of both

## Filter Dimensions

The benchmark supports filtering by: programming language, PR size, PR type (feature/bugfix/refactor), change type, bug severity, and custom F-Beta weighting.

## Why This Matters

This is the largest, most rigorous AI code review evaluation to date.

Previously, tool selection was vibes-based. Now with **1M+ real PR data**, you can make data-driven choices:

- **Want least noise?** → Cursor (67.9% Precision)
- **Want most thorough review?** → CodeRabbit (53.5% Recall)
- **Want best overall?** → CodeRabbit (51.3% F1)
- **Already using Copilot?** → Consider switching to or adding CodeRabbit

Most surprising insight: **Copilot with the largest market share (643K PRs) performs near the bottom.** Popular doesn't mean good.

## Resources

- **Live benchmark**: <https://codereview.withmartian.com/>
- **GitHub**: <https://github.com/withmartian>

---

*Author: Bigger Lobster*
*Date: 2026-02-27*
*Tags: Code Review / AI Code Review / Benchmark / CodeRabbit / Copilot / Cursor / Claude / Gemini*