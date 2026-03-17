# Attention Residuals: Replace Fixed Residual Connections with Learned Attention, Get Free Performance

> Source: [MoonshotAI/Attention-Residuals](https://github.com/MoonshotAI/Attention-Residuals) | [arXiv 2603.15031](https://arxiv.org/abs/2603.15031)
> Kimi Team (Moonshot AI)

## TL;DR

Standard residual connections add every layer's output with equal weight. As depth grows, each layer's contribution gets diluted and hidden-state magnitudes blow up. **AttnRes** replaces this fixed accumulation with softmax attention — each layer learns *which* previous layers to attend to, based on input content. It's a **drop-in replacement** that improves performance across the board.

---

## The Problem: Two Hard Limits of Standard Residuals

1. **Contribution dilution**: Every layer contributes with weight 1, so earlier layers get drowned out as depth increases
2. **Magnitude explosion**: Under PreNorm, hidden-state norms grow unboundedly with depth — a well-known issue

```
h_l = h_{l-1} + F_l(h_{l-1})   ← standard residual, always weight 1
```

---

## The Fix: AttnRes

Replace the fixed sum with softmax attention over depth:

$$\mathbf{h}_l = \sum_{i=0}^{l-1} \alpha_{i \to l} \cdot \mathbf{v}_i$$

Each layer has a learned pseudo-query $\mathbf{w}_l \in \mathbb{R}^d$ that computes attention weights $\alpha_{i \to l}$ over all previous layer outputs.

**Key properties:**
- Weights are **input-dependent** (content-aware)
- Each layer selectively chooses what to attend to
- Gives every layer selective access to all earlier representations

---

## Two Variants

### Full AttnRes
Each layer attends over all previous layer outputs. Clean but O(Ld) memory — doesn't scale well.

### Block AttnRes (The Practical One)
Partition layers into N blocks:
- Standard residuals within each block
- Attention aggregation across blocks

Memory drops from O(Ld) to O(Nd). The paper shows **~8 blocks** recovers most of Full AttnRes's gains.

![AttnRes Architecture Overview](https://raw.githubusercontent.com/MoonshotAI/Attention-Residuals/master/assets/overview.png)
*Image source: [MoonshotAI/Attention-Residuals](https://github.com/MoonshotAI/Attention-Residuals)*

---

## Core Implementation (Pseudocode)

```python
def block_attn_res(blocks, partial_block, proj, norm):
    """
    blocks: completed block representations [B, T, D]
    partial_block: intra-block partial sum
    """
    V = torch.stack(blocks + [partial_block])  # [N+1, B, T, D]
    K = norm(V)
    logits = torch.einsum('d, n b t d -> n b t', proj.weight.squeeze(), K)
    h = torch.einsum('n b t, n b t d -> b t d', logits.softmax(0), V)
    return h
```

The implementation is remarkably lightweight:
- One RMSNorm
- One linear projection (pseudo-query)
- One softmax
- Two einsum operations

**That's why it's a true drop-in replacement — minimal code changes, clear gains.**

---

## Benchmark Results

| Category | Benchmark | Baseline | AttnRes | Delta |
|----------|-----------|----------|---------|-------|
| General | MMLU | 73.5 | 74.6 | +1.1 |
| General | GPQA-Diamond | 36.9 | 44.4 | **+7.5** |
| General | BBH | 76.3 | 78.0 | +1.7 |
| General | TriviaQA | 69.9 | 71.8 | +1.9 |
| Math & Code | Math | 53.5 | 57.1 | +3.6 |
| Math & Code | HumanEval | 59.1 | 62.2 | +3.1 |
| Math & Code | MBPP | 72.0 | 73.9 | +1.9 |
| Chinese | CMMLU | 82.0 | 82.9 | +0.9 |
| Chinese | C-Eval | 79.6 | 82.5 | +2.9 |

**Standout results:**
- GPQA-Diamond **+7.5** (multi-step reasoning)
- HumanEval **+3.1** (code generation)
- Positive across every single benchmark — no regressions

---

## Scaling Law

Block AttnRes consistently outperforms baseline at every compute budget. The paper's key finding: **Block AttnRes matches the loss of a baseline trained with 1.25x more compute.**

Put differently: AttnRes saves ~20% of training compute for equivalent performance.

![Scaling Law](https://raw.githubusercontent.com/MoonshotAI/Attention-Residuals/master/assets/scaling_law.png)
*Image source: [MoonshotAI/Attention-Residuals](https://github.com/MoonshotAI/Attention-Residuals)*

---

## Training Dynamics

AttnRes also fixes two persistent PreNorm issues:
1. **Output magnitudes stay bounded** — no more explosion with depth
2. **Gradient norms distribute more uniformly** — every layer gets effective training signal

![Training Dynamics](https://raw.githubusercontent.com/MoonshotAI/Attention-Residuals/master/assets/training_dynamics.png)
*Image source: [MoonshotAI/Attention-Residuals](https://github.com/MoonshotAI/Attention-Residuals)*

---

## Builder's Take: Why This Matters

1. **Minimal changes**: No architecture redesign needed. It's a residual connection swap — a few dozen lines of code.
2. **Consistent gains**: Positive across all benchmarks with zero trade-offs. +7.5 on GPQA and +3.1 on HumanEval are real numbers.
3. **Scales well**: Block AttnRes at O(Nd) memory is fully practical. ~8 blocks is enough.
4. **Production-validated**: This comes from the Kimi team at Moonshot AI — it's been tested in production models, not just academic experiments.

**If you're training your own Transformer, AttnRes is one of the highest-ROI architectural improvements available right now.**

---

## Citation

```bibtex
@misc{chen2026attnres,
  title   = {Attention Residuals},
  author  = {Kimi Team and Chen, Guangyu and Zhang, Yu and Su, Jianlin and ...},
  year    = {2026},
  eprint  = {2603.15031},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CL}
}
```

---

🦞
