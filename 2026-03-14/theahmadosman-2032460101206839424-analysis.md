# 掌握 LLM 的 26 篇必读论文：Ahmad 的完整阅读路线图

> 原推文：[@TheAhmadOsman](https://x.com/theahmadosman/status/2032460101206839424) · 2026-03-13

![Ahmad 推荐的 26 篇 LLM 必读论文列表](https://pbs.twimg.com/media/HDS_qsSWUAA8jEL.jpg)
*图片来源：[@TheAhmadOsman](https://x.com/TheAhmadOsman) 推文配图*

---

## 为什么这份清单值得关注

Ahmad Osman 整理了一份 **26 篇论文的阅读清单**，覆盖从 Transformer 基础到推理、MoE、Agent 系统的完整脉络。他的说法很直接：**读透这些，你就掌握了现代 LLM 90% 的核心知识**。剩下的都是锦上添花。

这份清单的价值不仅在于"列了哪些论文"，更在于**阅读顺序的编排**——从基础架构到训练优化，再到对齐、推理和 MoE，形成了一条清晰的学习路径。

---

## 完整论文清单（按推荐阅读顺序）

### 第一阶段：Transformer 基础

| # | 论文 | 核心要点 |
|---|------|----------|
| 1 | **Attention Is All You Need** (Vaswani et al., 2017) | 原始 Transformer 论文，self-attention、multi-head attention、encoder-decoder 架构 |
| 2 | **The Illustrated Transformer** (Jay Alammar, 2018) | 可视化直觉构建，理解 attention 和 tensor 流动的最佳入门 |
| 3 | **BERT** (Devlin et al., 2018) | Encoder 端基础，masked language modeling，表征学习 |
| 4 | **GPT-3: Language Models are Few-Shot Learners** (Brown et al., 2020) | 确立 in-context learning 能力，改变 prompting 的理解方式 |

### 第二阶段：Scaling Laws 与训练效率

| # | 论文 | 核心要点 |
|---|------|----------|
| 5 | **Scaling Laws for Neural Language Models** (Kaplan et al., 2020) | 参数、数据、算力的 scaling 关系框架 |
| 6 | **Chinchilla** (Hoffmann et al., 2022) | 固定算力预算下，token 数量比参数量更重要 |
| 7 | **LLaMA** (Touvron et al., 2023) | 开源权重时代的起点，RMSNorm、SwiGLU、RoPE 成为标配 |
| 8 | **RoFormer: Rotary Position Embedding** (Su et al., 2021) | 长上下文 LLM 的默认位置编码方案 |
| 9 | **FlashAttention** (Dao et al., 2022) | 内存高效 attention，实现长上下文和高吞吐推理 |

### 第三阶段：RAG 与对齐

| # | 论文 | 核心要点 |
|---|------|----------|
| 10 | **RAG** (Lewis et al., 2020) | 参数模型 + 外部知识源，企业级系统的基础 |
| 11 | **InstructGPT** (Ouyang et al., 2022) | 现代 post-training 和对齐的蓝图 |
| 12 | **DPO** (Rafailov et al., 2023) | 比 PPO 更简单稳定的偏好对齐方案 |

### 第四阶段：推理与 Agent

| # | 论文 | 核心要点 |
|---|------|----------|
| 13 | **Chain-of-Thought Prompting** (Wei et al., 2022) | 仅通过 prompting 就能引出推理能力 |
| 14 | **ReAct** (Yao et al., 2022) | Agent 系统的基础——推理链 + 工具使用 + 环境交互 |
| 15 | **DeepSeek-R1** (Guo et al., 2025) | 大规模 RL 无需监督数据即可诱导自我验证和结构化推理 |
| 16 | **Qwen3 Technical Report** (Yang et al., 2025) | 统一 MoE + Thinking/Non-Thinking 模式动态切换 |

### 第五阶段：MoE（混合专家模型）

| # | 论文 | 核心要点 |
|---|------|----------|
| 17 | **Sparsely-Gated MoE** (Shazeer et al., 2017) | 现代 MoE 的起点，条件计算大规模化 |
| 18 | **Switch Transformers** (Fedus et al., 2021) | 单专家激活简化路由，稳定万亿参数训练 |
| 19 | **Mixtral of Experts** (Mistral AI, 2024) | 开源 MoE 证明稀疏模型能以小模型成本匹配稠密模型质量 |
| 20 | **Sparse Upcycling** (Komatsuzaki et al., 2022) | 把稠密模型 checkpoint 转换成 MoE，算力复用 |

### 第六阶段：理论与实践

| # | 论文 | 核心要点 |
|---|------|----------|
| 21 | **The Platonic Representation Hypothesis** (Huh et al., 2024) | 大规模模型跨模态收敛到共享内部表征 |
| 22 | **Textbooks Are All You Need** (Gunasekar et al., 2023) | 高质量合成数据让小模型超越大模型 |
| 23 | **Scaling Monosemanticity** (Templeton et al., 2024) | 机械可解释性的最大突破，分解数百万可解释特征 |
| 24 | **PaLM** (Chowdhery et al., 2022) | 数千加速器上的大规模训练编排 |
| 25 | **GLaM** (Du et al., 2022) | MoE 规模经济：总参数量大但活跃参数少 |
| 26 | **The Smol Training Playbook** (Hugging Face, 2025) | 高效训练语言模型的端到端实战手册 |

### Bonus

- T5 (Raffel et al., 2019)
- Toolformer (Schick et al., 2023)
- GShard (Lepikhin et al., 2020)
- Adaptive Mixtures of Local Experts (Jacobs et al., 1991)
- Hierarchical Mixtures of Experts (Jordan & Jacobs, 1994)

---

## 实战建议

**如果你时间有限**，按优先级抓这几条线：

1. **Transformer 核心**（#1-4）：地基不稳什么都白搭
2. **Scaling + 训练**（#5-9）：理解为什么模型是这样设计的
3. **对齐 + 推理**（#11-15）：理解现代 LLM "为什么能用"

**如果你在做工程**，重点看：
- FlashAttention (#9) — 你的推理速度取决于它
- RAG (#10) — 企业产品绑不开
- ReAct (#14) — 做 Agent 必读
- DeepSeek-R1 (#15) — 理解 reasoning model 的训练范式

**如果你在做研究**，别跳过：
- Scaling Monosemanticity (#23) — 可解释性前沿
- Platonic Representation (#21) — 多模态理论基础
- Sparse Upcycling (#20) — 实验成本优化

---

## 总结

这份清单的编排逻辑很清晰：**基础架构 → 规模法则 → 训练优化 → 对齐推理 → MoE → 前沿理论**。不是随便列的论文堆砌，而是一条有逻辑的学习路径。

Ahmad 说得对——深入理解 Transformer 核心、scaling laws、FlashAttention、指令微调、R1 式推理和 MoE upcycling，你对 LLM 的理解就已经超过大多数人了。

🦞
