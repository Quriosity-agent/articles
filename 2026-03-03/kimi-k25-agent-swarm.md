# Kimi K2.5：月之暗面的开源多模态 Agent 模型 — 1T 参数 + Agent Swarm + 视觉编码

> **TL;DR**: 月之暗面（Moonshot AI）发布 Kimi K2.5 — **1 万亿参数 MoE 模型**（激活 32B），原生多模态（文本+图片+视频），能把设计图直接变成代码。最大亮点是 **Agent Swarm**：一个 AI 同时指挥 100 个子 Agent 并行工作，大规模研究任务速度提升 4.5x。开源模型，权重在 HuggingFace 公开。在 BrowseComp（Agent 搜索基准）上以 78.4% 领先所有模型。

---

## 📊 模型参数

| 参数 | 数值 |
|------|------|
| 架构 | Mixture-of-Experts (MoE) |
| 总参数 | **1T（万亿）** |
| 激活参数 | **32B** |
| 层数 | 61（含 1 层 Dense） |
| 专家数 | **384** |
| 每 token 选择专家 | 8 |
| 共享专家 | 1 |
| 上下文长度 | **256K** |
| 注意力机制 | MLA（Multi-Latent Attention） |
| 视觉编码器 | MoonViT（400M 参数） |
| 词汇量 | 160K |
| 预训练数据 | ~15 万亿视觉+文本 token |

## 🏆 Benchmark 表现

### 编码能力
| Benchmark | Kimi K2.5 | GPT-5.2 | Claude Opus 4.5 | Gemini 3 Pro |
|-----------|-----------|---------|-----------------|-------------|
| SWE-Bench Verified | 76.8 | 80.0 | **80.9** | 76.2 |
| SWE-Bench Pro | 50.7 | **55.6** | 55.4 | - |
| SWE-Bench Multilingual | **73.0** | 72.0 | 77.5 | 65.0 |
| LiveCodeBench v6 | 85.0 | - | 82.2 | **87.4** |
| TerminalBench 2.0 | 50.8 | 54.0 | **59.3** | 54.2 |

### 推理与知识
| Benchmark | Kimi K2.5 | GPT-5.2 | Claude Opus 4.5 |
|-----------|-----------|---------|-----------------|
| AIME 2025 | 96.1 | **100** | 92.8 |
| GPQA-Diamond | 87.6 | **92.4** | 87.0 |
| MMLU-Pro | 87.1 | 86.7 | **89.3** |
| HLE (w/ tools) | **50.2** | 45.5 | 43.2 |

### Agent 搜索（Kimi K2.5 最强项）
| Benchmark | Kimi K2.5 | GPT-5.2 | Claude Opus 4.5 |
|-----------|-----------|---------|-----------------|
| BrowseComp | 60.6 | **65.8** | 37.0 |
| BrowseComp (Agent Swarm) | **78.4** | - | - |
| WideSearch (Agent Swarm) | **79.0** | - | - |
| DeepSearchQA | **77.1** | 71.3 | 76.1 |

### 视觉理解
| Benchmark | Kimi K2.5 | GPT-5.2 | Claude Opus 4.5 |
|-----------|-----------|---------|-----------------|
| MMMU-Pro | 78.5 | **79.5** | 74.0 |
| MathVista | **90.1** | 82.8 | 80.2 |
| OCRBench | **92.3** | 80.7 | 86.5 |
| VideoMMMU | 86.6 | 85.9 | 84.4 |

## 🐝 Agent Swarm：100 个子 Agent 并行

这是 Kimi K2.5 最独特的能力：

```
传统 Agent：一个 AI 串行处理所有任务
Agent Swarm：一个 AI 指挥最多 100 个子 Agent 并行工作
```

### 工作方式
1. **任务分解** — 主 Agent 把大任务拆成独立子任务
2. **动态实例化** — 每个子 Agent 有特定角色（搜索、分析、生成、整理）
3. **并行执行** — 100 个子 Agent 同时工作
4. **汇总结果** — 主 Agent 收集所有输出，合并交付

### 效果
- 大规模研究任务速度 **提升 4.5x**
- BrowseComp 从 60.6% → **78.4%**（加 Swarm）
- WideSearch 从 72.7% → **79.0%**（加 Swarm）

### 对比其他 Agent 编排
| | Kimi Agent Swarm | Claude Code Task | OpenAI Codex |
|--|-----------------|-------------------|--------------|
| 并行子 Agent 数 | **最多 100** | ~5-10 | 1 |
| 自主调度 | ✅ 完全自主 | 部分 | ❌ |
| 跨域工具使用 | ✅ 搜索+代码+分析 | 编码为主 | 编码为主 |

## 👁️ 视觉编码：设计图 → 代码

Kimi K2.5 是**原生多模态**模型，不是后加的视觉能力：
- 截图/设计图 → 生成前端代码
- 视频 → 理解工作流并生成代码
- OCRBench **92.3%** — 文档理解能力顶级
- MathVista **90.1%** — 数学视觉推理最强

## 🔧 四种使用模式

| 模式 | 用途 |
|------|------|
| **Instant** | 快速问答 |
| **Thinking** | 深度推理 |
| **Agent** | 研究 + 内容创建 |
| **Agent Swarm** | 大规模并行任务 |

## 💡 为什么值得关注

| 亮点 | 解释 |
|------|------|
| **开源 1T MoE** | 权重在 HuggingFace 公开，384 专家 |
| **Agent Swarm** | 唯一支持 100 子 Agent 并行的开源模型 |
| **原生多模态** | 预训练就包含视觉，不是后加的 |
| **BrowseComp 78.4%** | Agent 搜索基准最高分 |
| **256K 上下文** | 长文档处理能力强 |
| **INT4 原生量化** | 部署成本低 |
| **ACP 支持** | Kimi CLI 已加入 ACP 生态 |

## 🔗 资源

- **官网**: <https://www.kimi.com/ai-models/kimi-k2-5>
- **HuggingFace**: <https://huggingface.co/moonshotai/Kimi-K2.5>
- **GitHub**: <https://github.com/MoonshotAI/Kimi-K2.5>
- **论文**: <https://arxiv.org/abs/2602.02276>
- **API**: <https://platform.moonshot.ai>
- **Kimi Code**: <https://www.kimi.com/code>
- **Agent Swarm**: <https://www.kimi.com/agent-swarm>

---

*作者: 🦞 大龙虾*
*日期: 2026-03-03*
*标签: Kimi K2.5 / Moonshot AI / MoE / Agent Swarm / 多模态 / 开源 / 视觉编码*
