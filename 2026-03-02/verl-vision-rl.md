# verl：重新定义大模型强化学习训练的开源框架

> **TL;DR:** verl（原名 Volcano Engine Reinforcement Learning）是由字节跳动 Seed 团队发起、社区共建的大模型强化学习训练框架。凭借创新的混合控制器架构和 3D-HybridEngine，它在 RLHF/RLAIF 吞吐量上实现了 1.5x~20x 的提升，已成为当前最活跃的 LLM 后训练基础设施之一。截至 2026 年 3 月，GitHub 星标 **19,500+**，Fork **3,330+**。

---

## 一、为什么我们需要 verl？

2024-2025 年，大语言模型（LLM）的训练范式发生了深刻转变：**后训练（Post-Training）**——尤其是基于强化学习的对齐和推理增强——从"锦上添花"变成了"必要环节"。DeepSeek-R1 的成功证明，GRPO 等 RL 算法可以让模型涌现出强大的推理能力。

但现实中的 RL 训练极其复杂：

- **多模型协同**：PPO 需要 Actor、Critic、Reference、Reward 四个模型同时运行
- **训练与推理交替**：生成（rollout）和训练不断切换，资源利用率低
- **分布式复杂度爆炸**：每个模型本身就是分布式程序，模型间通信是多对多广播
- **算法迭代快**：从 PPO 到 GRPO、DAPO、VAPO，研究者需要快速实验

现有框架要么灵活但低效（单控制器架构如 DeepSpeed-Chat），要么高效但僵化（多控制器架构如 OpenRLHF）。verl 的诞生正是为了解决这个两难困境。

---

## 二、核心架构：HybridFlow 混合控制器

verl 的学术论文名为 **HybridFlow**（发表于 EuroSys 2025），其核心创新是将单控制器和多控制器范式进行混合：

### 2.1 编程模型

```
┌─────────────────────────────────────────────┐
│           Single Controller (Python)         │
│  ┌───────┐  ┌───────┐  ┌───────┐  ┌──────┐ │
│  │ Actor │  │Critic │  │  Ref  │  │Reward│ │
│  │(Multi-│  │(Multi-│  │(Multi-│  │(Multi│ │
│  │ Ctrl) │  │ Ctrl) │  │ Ctrl) │  │Ctrl) │ │
│  └───────┘  └───────┘  └───────┘  └──────┘ │
└─────────────────────────────────────────────┘
```

- **层间（Inter-node）**：用单控制器编排 RL 数据流，用 Python 原生语法定义算法逻辑
- **层内（Intra-node）**：每个模型内部用多控制器高效执行分布式计算（FSDP/Megatron-LM）
- **效果**：用几行代码就能定义 PPO/GRPO 等复杂 RL 算法，同时保持接近手写优化的性能

### 2.2 3D-HybridEngine

这是 verl 最关键的性能优化。在 RL 训练中，Actor 模型需要在 **训练模式**（参数分片）和 **生成模式**（需要完整权重）之间反复切换。传统方法要么保留冗余副本（浪费显存），要么全量通信（带宽瓶颈）。

3D-HybridEngine 实现了：
- **零内存冗余**的模型重分片（resharding）
- 通信开销显著降低
- 支持 DP、TP、PP 三维并行的灵活映射

实验结果：相比 SOTA 基线，吞吐量提升 **1.53x ~ 20.57x**。

### 2.3 灵活的设备映射

verl 支持将不同模型放置在不同 GPU 集合上，从单机 8 卡到数百卡集群都能高效运行。这在其他框架中通常需要大量手动配置。

---

## 三、支持的算法与模型

### RL 算法（截至 2026 年 3 月）

| 算法 | 说明 |
|------|------|
| **PPO** | 经典策略优化 |
| **GRPO** | DeepSeek 提出的群组相对策略优化 |
| **DAPO** | 分布式对齐 PPO，AIME 2024 达到 50 分 |
| **VAPO** | 基于价值函数增强的 PPO，AIME 2024 达到 60.4 分 |
| **REINFORCE++** | 改进的 REINFORCE |
| **RLOO** | Leave-One-Out 策略梯度 |
| **ReMax** | 最大奖励强化学习 |
| **PF-PPO** | 过滤噪声奖励信号（ICML 2025） |
| **PRIME** | 过程奖励模型引导 |
| **DAPO** | 动态采样 + clip-higher |
| **SPPO** | 自博弈偏好优化 |
| **DrGRPO** | GRPO 的正则化变体 |

### 支持的模型

- **文本**：Qwen-3、Qwen-2.5、LLaMA 3.1、Gemma2、DeepSeek-LLM（含 671B MoE）
- **视觉语言**：Qwen2.5-VL、Kimi-VL、Qwen3-VL
- **规模**：从 1.5B 到 **671B**（万亿参数级别通过 Expert Parallelism 支持）

### 训练后端

- **训练**：FSDP、FSDP2、Megatron-LM
- **推理**：vLLM、SGLang、HuggingFace Transformers
- **硬件**：NVIDIA、AMD、华为昇腾

---

## 四、多模态与视觉 RL：新前沿

verl 不仅仅是一个文本 LLM 的 RL 框架——它正在成为**多模态 RL 训练的标准基础设施**。

### 4.1 原生 VLM 支持

verl 主仓库直接支持 Qwen2.5-VL 等视觉语言模型的 GRPO 训练，提供了开箱即用的示例脚本。这意味着你可以用 RL 来增强 VLM 的视觉推理能力——例如让模型学会在几何题中"看懂"图形。

### 4.2 VLA（Vision-Language-Action）实验

在 `verl/experimental/vla` 目录下，verl 正在探索视觉-语言-动作模型的 RL 训练，这直接对接具身智能（Embodied AI）的需求。

### 4.3 多轮工具调用

verl 支持基于 SGLang 的多轮对话 + 工具调用的 RL 训练，这是构建 Agent 系统的关键能力。

---

## 五、生态系统：谁在用 verl？

verl 最令人印象深刻的不仅是框架本身，还有围绕它生长出的庞大生态：

### 5.1 Easy-R1

- **仓库**：[hiyouga/EasyR1](https://github.com/hiyouga/EasyR1)
- **定位**：verl 的"友好 fork"，专注多模态 VLM 的 RL 训练
- **亮点**：极低的上手门槛，Docker 一键部署，支持 Qwen2.5-VL/Qwen3-VL
- **贡献者**：LLaMA-Factory 团队（hiyouga），中国 LLM 社区最活跃的开源力量之一
- **意义**：让 VLM+RL 从"实验室技术"变成"人人可用"

### 5.2 verl-agent

- **仓库**：[langfengQ/verl-agent](https://github.com/langfengQ/verl-agent)
- **定位**：verl 的 Agent 训练扩展
- **核心创新**：**逐步独立的多轮 rollout 机制**——不是简单拼接历史，而是每步可自定义输入结构、历史管理和记忆模块
- **算法**：GiGPO（Group-in-Group 策略优化，NeurIPS 2025）、HGPO（ICLR 2026）
- **环境**：ALFWorld、WebShop、Sokoban、Search 工具调用等
- **意义**：让 verl 从"模型训练"延伸到"Agent 训练"

### 5.3 VAGEN

- **仓库**：[mll-lab-nu/VAGEN](https://github.com/mll-lab-nu/VAGEN)
- **定位**：VLM Agent 的多轮 RL 训练框架
- **核心**：FreeThink——让 VLM agent 产生自然语言推理，视觉状态推理自然涌现
- **基础**：基于 verl 的 agent-loop

### 5.4 verl-recipe

- **仓库**：[verl-project/verl-recipe](https://github.com/verl-project/verl-recipe)
- **定位**：官方算法食谱仓库，包含 DAPO、PRIME、SPPO、DrGRPO 等的完整复现代码
- **意义**：将 verl 从框架变成可复现的研究平台

### 5.5 其他生态项目

- **ReTool**：多轮对话 + 代码沙箱，提升数学推理能力
- **OpenManus-RL**：支持 verl-agent 风格的训练流水线
- **ROLL（阿里巴巴）**：集成了 GiGPO 算法
- **Megatron-Bridge（NVIDIA）**：与 verl 联合训练万亿参数模型

---

## 六、里程碑式的研究成果

verl 不仅是基础设施——它直接推动了多项 SOTA 研究：

### DAPO（2025 年 3 月）
- 基于 Qwen2.5-32B 预训练模型
- **AIME 2024 达到 50 分**，超越 DeepSeek-R1-Zero
- 完全使用 verl 训练，代码开源

### VAPO（2025 年 4 月）
- 基于价值函数增强的 PPO
- **AIME 2024 达到 60.4 分**，超越 DAPO
- 论文：arXiv:2504.05118

### Seed-Thinking-v1.5（2025 年 4 月）
- 字节跳动 Seed 团队内部模型
- **AIME 2024: 86.7** | Codeforces: 55.0 | GPQA: 77.3
- 使用 verl 训练

### Doubao-1.5-pro（2025 年 1 月）
- 豆包大模型 1.5 版本
- RL scaling preview 达到 OpenAI O1 级别数学性能
- AIME pass@1: 70.0

### Mind Lab 万亿参数 RL（2025 年 12 月）
- 使用 verl + Megatron-Bridge
- 64 张 H800 训练 **万亿参数模型**的 GRPO LoRA

---

## 七、与其他框架的对比

| 维度 | verl | OpenRLHF | DeepSpeed-Chat | TRL |
|------|------|----------|----------------|-----|
| **架构** | 混合控制器 | 多控制器 | 单控制器 | 单控制器 |
| **灵活性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **吞吐量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **最大规模** | 671B (MoE) | 70B+ | 70B | 70B |
| **VLM 支持** | ✅ 原生 | ❌ | ❌ | 有限 |
| **多轮 Agent** | ✅ | ❌ | ❌ | ❌ |
| **Megatron 支持** | ✅ | ❌ | ❌ | ❌ |
| **社区活跃度** | 🔥🔥🔥 | 🔥🔥 | 🔥 | 🔥🔥 |

verl 的核心优势：
1. **兼顾灵活与高效**——混合控制器架构是独创的
2. **规模天花板最高**——支持 671B MoE + 数百卡集群
3. **多模态原生支持**——VLM、VLA、Agent 全覆盖
4. **生态最丰富**——从算法复现到 Agent 训练，下游项目最多

---

## 八、技术创新深度分析

### 8.1 为什么 HybridFlow 比纯单/多控制器更好？

**单控制器（如 DeepSpeed-Chat）的问题**：所有分布式操作都由一个 Python 进程调度，每次 GPU 操作都要经过控制器，形成巨大的调度开销。当模型分布在 64+ GPU 上时，控制器成为瓶颈。

**多控制器（如 Megatron-LM 原生）的问题**：每个模型作为独立的分布式程序运行，效率高但灵活性差。实现一个新的 RL 算法需要修改底层通信逻辑。

**HybridFlow 的解法**：
- 用单控制器定义 RL dataflow（高灵活性）
- 用多控制器执行每个模型的内部计算（高效率）
- 通过精心设计的分层 API 解耦计算和数据依赖

### 8.2 3D-HybridEngine 的实际影响

在 PPO 训练中，Actor 模型的 resharding（从训练分片到生成分片）是性能杀手。verl 的 3D-HybridEngine 支持 DP×TP×PP 三维并行组合下的零冗余切换，这在工程上极其困难，但带来的性能收益是量级级别的。

### 8.3 异步与离策略（Off-Policy）架构

verl 的实验目录中包含了 `fully_async_policy`、`one_step_off_policy` 和 `transfer_queue` 等模块，表明团队正在探索异步 RL 训练——这可以进一步提升 GPU 利用率，是下一代 RL 训练范式的方向。

---

## 九、谁在背后？

### 核心团队

verl 由**字节跳动 Seed 团队**发起。Seed 是字节跳动的 AI 基础研究团队，负责豆包大模型（Doubao）等核心产品的技术研发。

2026 年 1 月，verl 迁移到了独立的 [verl-project](https://github.com/verl-project) 组织，标志着从"公司项目"向"社区项目"的转变。

### 社区

- **首次线下聚会**：2026 年 1 月 10 日在上海举办，由火山引擎和 NVIDIA 联合主持
- **学术演讲**：EuroSys 2025、NeurIPS 2024、ICLR 2025、PyTorch Conference 2025、ICML 2025
- **国际化**：AWS AI Hours（新加坡）、GOSIM（巴黎）、Ray Summit、vLLM Meetup 等

### 数据表现

| 指标 | 数值 |
|------|------|
| GitHub Stars | 19,510 |
| Forks | 3,330 |
| Open Issues | 1,833 |
| 创建时间 | 2024 年 10 月 |
| 语言 | Python |
| 许可证 | Apache-2.0 |

从 2024 年 10 月创建到 2026 年 3 月达到近 2 万星，增长速度惊人，反映了社区对高质量 RL 训练基础设施的强烈需求。

---

## 十、verl 为什么重要？

### 10.1 它填补了关键的基础设施空白

在 verl 之前，做 LLM 的 RL 训练要么用学术实验室的玩具框架（能跑但性能差），要么用大厂内部系统（性能好但不开源）。verl 第一次提供了**生产级、开源、灵活**的三合一方案。

### 10.2 它加速了 RL for Reasoning 的研究

DAPO、VAPO、Seed-Thinking 等里程碑式成果都基于 verl，说明好的基础设施确实能加速研究。当研究者不需要花 80% 的时间搞工程，他们能更快地验证新想法。

### 10.3 它定义了多模态 RL 的方向

从文本到 VLM 到 VLA，verl 正在构建一个统一的多模态 RL 训练栈。在 Agent 和具身智能时代，这将是核心基础设施。

### 10.4 它代表了开源 AI 基础设施的新模式

字节跳动将内部系统开源、迁移到社区组织、在全球学术会议布道——这种模式正在被越来越多的中国 AI 公司采用。verl 是这种模式的标杆案例。

---

## 结语

verl 不仅仅是"又一个 RL 训练框架"。它是 LLM 后训练时代的**关键基础设施**，是连接研究创新与工程实践的桥梁，是多模态 RL 训练的事实标准正在形成的信号。

如果你在做 LLM 的 RL 训练，无论是学术研究还是工业应用，verl 都值得认真关注。

---

**相关链接：**
- GitHub：https://github.com/verl-project/verl
- 论文：https://arxiv.org/abs/2409.19256
- 文档：https://verl.readthedocs.io
- Slack：https://join.slack.com/t/verl-project
- Twitter：https://twitter.com/verl_project
