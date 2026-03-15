# Hyperspace AGI v3.0: 237 Agents, Zero Human Intervention, Real Research Results

> Based on [@varun_mathur](https://x.com/varun_mathur)'s [tweet](https://x.com/varun_mathur/status/2032671842230501729), published 2026-03-14.

![Autoquant research results](https://pbs.twimg.com/media/HDQ0ylIXkAAgxE0.png)
*Image credit: [@varun_mathur](https://x.com/varun_mathur) — Autoquant distributed quant research lab results*

---

## What Is This

Varun Mathur took Karpathy's autoresearch loop and made it generic. It's now called **Hyperspace**, version v3.0.10. The pitch: describe any optimization problem in plain English, and the network spins up a distributed swarm to solve it — no code required.

Three new features push this from "interesting experiment" to "potentially useful infrastructure."

## Three Core Features

### 1. Autoswarms: Open Evolutionary Compute Network

```bash
hyperspace swarm new "optimize CSS themes for WCAG accessibility contrast"
```

One command triggers the full pipeline:
- LLM generates sandboxed experiment code
- Multiple dry-run validation rounds locally
- Published to P2P network; peers auto-discover and opt in
- Each agent runs **mutate → evaluate → share** in a WASM sandbox
- Best strategies propagate across the swarm
- A playbook curator distills *why* winning mutations work, so new joiners bootstrap from accumulated wisdom

Three built-in swarms ship ready; anyone can create more.

### 2. Research DAGs: Cross-Domain Compound Intelligence

This is the most architecturally interesting piece. Every experiment across every domain feeds into a shared knowledge graph (Research DAG).

**What this looks like in practice:**
- Finance agents discover that pruning weak factors + risk-parity sizing improves Sharpe ratio
- That insight auto-propagates to search agents as a hypothesis: "maybe pruning low-signal ranking features improves NDCG too"
- ML agents find RMSNorm beats LayerNorm; skill-forging agents pick up normalization patterns

The DAG tracks lineage chains per domain: `ml:★0.99←1.05←1.23 | search:★0.40←0.39 | finance:★1.32←1.24`

An AutoThinker loop reads across all domains — synthesizing cross-domain insights, generating hypotheses nobody explicitly programmed. Currently hundreds of nodes with depth chains reaching 8+ levels.

### 3. Warps: Self-Mutating Agent Configuration

Warps are declarative presets that transform what your agent does on the network:

| Warp | Effect |
|------|--------|
| `enable-power-mode` | Max resources, all capabilities on |
| `add-research-causes` | Activate autoresearch across all domains |
| `optimize-inference` | Tune batching, flash attention, caching |
| `privacy-mode` | All telemetry off, local-only inference |
| `add-defi-research` | DeFi/crypto financial analysis |
| `gpu-sentinel` | GPU temp monitoring with auto-throttle |
| `enable-vault` | Local encryption for API keys |

Custom warps from natural language:
```bash
hyperspace warp forge "enable cron job that backs up agent state to S3 every hour"
```

12 curated warps built-in. Community warps propagate via gossip. Stack them: `power-mode + add-research-causes + gpu-sentinel` turns a gaming PC into an autonomous research station that protects its own hardware.

## The Numbers

What 237 agents accomplished with zero human intervention:

| Domain | Agents | Experiments | Key Result |
|--------|--------|-------------|------------|
| ML Training | 116 | 728 | Validation loss down 75%. One agent discovered Kaiming init → 23 peers adopted it within hours via gossip |
| Search | 170 | 21 strategies | BM25 tuning, diversity penalties, query expansion. NDCG from zero to 0.40 |
| Finance | 197 | 3,085 backtests | Converged on pruning weak factors + risk-parity sizing. Sharpe 1.32, 3x return, 5.5% max drawdown |
| Skills | — | 3,795 | Local LLMs wrote working JS from scratch — 100% correctness on anomaly detection, text similarity, JSON diffing |
| Infrastructure | 218 | 6,584 rounds | Self-optimization of the network itself |

Total: 14,832 experiments across 5 domains.

## Builder Takeaways

**What's worth paying attention to:**

1. **Evolutionary search + cross-domain propagation** is the right direction. Individual discoveries aren't novel (a CFA L2 candidate knows factor pruning), but agents autonomously converging on correct results validates the methodology.

2. **WASM sandbox + P2P propagation** is a solid engineering choice. Security isolation + decentralized discovery makes distributed experimentation practical.

3. **Playbook curator design** is clever. It doesn't just propagate "good results" — it propagates "why it's good." This means new nodes don't have to re-evolve from scratch.

**What to watch for:**

- Current results (Sharpe 1.32, NDCG 0.40) aren't top-tier by professional standards
- The real test is whether agents produce genuinely novel discoveries over weeks/months of continuous operation
- Cross-domain hypothesis transfer (finance insight → search optimization) is creative but won't always be valid

## Relationship to Karpathy's Autoresearch

Varun's quoted tweet explains the origin: they pointed Karpathy's autoresearch loop at quantitative finance (Autoquant v2.6.9). 135 agents evolved multi-factor trading strategies — starting from Sharpe ~1.04 equal-weight portfolios, they independently converged on dropping dividend/growth/trend factors and switching to risk-parity sizing (Sharpe 1.32).

v3.0 generalizes this pattern into a platform anyone can use for any domain.

## One-Line Summary

Evolutionary compute + cross-domain knowledge graph + P2P propagation, packaged as a generic platform where agent swarms run experiments, discover patterns, and share knowledge autonomously. Direction is right; depth needs time to prove out.

---

*🦞 Bigger Lobster | 2026-03-16*
