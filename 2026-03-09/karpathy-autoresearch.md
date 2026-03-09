# Karpathy 的 autoresearch：让 AI Agent 自动做 AI 研究

> "有一天，前沿 AI 研究曾由肉体计算机完成……那个时代早已过去。" —— Andrej Karpathy, 2026年3月

## 这是什么？

[autoresearch](https://github.com/karpathy/autoresearch) 是 Andrej Karpathy 于 2026 年 3 月开源的一个项目，核心理念极其简单又极其大胆：**让 AI Agent 自主进行 AI 研究**。

具体来说：给一个 AI Agent（如 Claude Code 或 Codex）一个真实的小型 LLM 训练环境，让它自主修改代码、训练模型、评估结果、保留改进、丢弃退步，然后不断重复。你睡一觉起来，就能看到一整夜的实验日志和（希望是）一个更好的模型。

Karpathy 在推特上说，他让 Agent 自动跑了 12 小时，完成了 110 次修改，将验证损失从 0.862415 降到了 0.858039。他甚至感叹自己花在优化 "meta-setup"（Agent 工作流）上的时间比直接优化代码还多——这或许正是 AI 研究的未来缩影。

## 架构：极简三文件设计

autoresearch 的设计哲学是**极简**。整个项目只有三个核心文件：

- **`prepare.py`** — 固定不变的数据准备脚本。下载训练数据、训练 BPE tokenizer、提供 dataloader 和评估工具。Agent 不会修改这个文件。
- **`train.py`** — Agent 唯一修改的文件。包含完整的 GPT 模型定义、优化器（Muon + AdamW）和训练循环。架构、超参数、batch size、优化器——一切都可以改。
- **`program.md`** — 给 Agent 的指令文件。相当于一个超轻量的 "skill"，告诉 Agent 该怎么做实验。这个文件由人类编辑和迭代。

这种设计的精妙之处在于：**你不再直接写 Python 代码做研究，你在编写指导 AI 做研究的 Markdown 文件**。用 Karpathy 的话说："You are programming the program."

## 工作流程：5 分钟一个实验

整个研究循环是这样的：

- **Step 1：** Agent 阅读 `program.md`，理解当前目标和约束
- **Step 2：** Agent 分析当前的 `train.py`，提出一个改进假设
- **Step 3：** Agent 修改 `train.py`（可能改架构、调超参、换优化策略等）
- **Step 4：** 运行训练，固定 5 分钟墙钟时间
- **Step 5：** 检查 `val_bpb`（验证集 bits per byte），与之前的最佳结果比较
- **Step 6：** 如果改进了，保留修改；如果退步了，回滚
- **Step 7：** 记录实验结果，回到 Step 2

关键设计决策：

- **固定 5 分钟时间预算** — 不管你改了什么（模型大小、batch size、架构），训练时间都一样，所以实验之间可以公平比较。每小时约 12 个实验，一晚上约 100 个实验。
- **单一指标 val_bpb** — bits per byte 与词表大小无关，所以即使 Agent 改了 tokenizer 相关的东西，结果依然可比。
- **单 GPU 自包含** — 不需要分布式训练，不需要复杂配置。一张 GPU、一个文件、一个指标。

## 快速上手

```bash
# 安装 uv 包管理器
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
uv sync

# 下载数据和训练 tokenizer（一次性，约 2 分钟）
uv run prepare.py

# 手动跑一次训练测试（约 5 分钟）
uv run train.py

# 然后启动你的 AI Agent（如 Claude Code），提示它：
# "Hi have a look at program.md and let's kick off a new experiment!"
```

硬件要求：单张 NVIDIA GPU（在 H100 上测试过），Python 3.10+，uv。

社区也有 macOS 适配的 fork：
- [miolini/autoresearch-macos](https://github.com/miolini/autoresearch-macos)
- [trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx)

## 与其他自动化研究工具的对比

autoresearch 并不是第一个尝试自动化 AI 研究的项目，但它的定位非常独特：

**ChatGPT Deep Research / Gemini Deep Research / Perplexity**
- 这些工具侧重于**信息检索和综合**——帮你搜集资料、整理文献、写综述
- 本质上是高级搜索引擎 + 摘要工具
- **不会**修改代码、运行实验、迭代模型

**Sakana AI 的 AI Scientist**
- 自动生成研究想法、写代码、运行实验、撰写论文
- 范围更广（从 idea 到 paper），但每个实验的质量控制较弱
- autoresearch 更聚焦：只做一件事（优化训练代码），但做得更深

**FARS (Fully Autonomous Research System)**
- 类似的自主实验理念
- 但通常更复杂，涉及多 Agent 协作、论文撰写等
- autoresearch 刻意保持简单——三个文件，一个 Agent

**autoresearch 的独特之处：**
- **真正的闭环实验** — 不只是分析和建议，而是真的改代码、跑训练、看结果
- **极简设计** — 三个文件，零配置，即插即用
- **人类可审计** — 所有修改都在一个文件里，diff 一目了然
- **"编程编程"的范式** — 你不写研究代码，你写指导 AI 写研究代码的指令

## 为什么这很重要？

Karpathy 在 README 里写了一段充满科幻感的话：未来 AI 研究将完全由自主 Agent 群体完成，代码将变成自修改的二进制文件，超越人类理解。而 autoresearch 就是这一切的起点。

但抛开科幻叙事，这个项目真正展示的是一种**新的研究范式**：

- 研究者的角色从"写代码跑实验"变成"设计 Agent 的工作流程"
- 实验的规模不再受限于人类的精力和时间
- 小型团队甚至个人可以让 AI 24/7 不间断地探索假设空间

这或许是 2026 年最值得关注的 AI 趋势之一：**AI 研究本身正在被 AI 自动化**。

---

*写于 2026 年 3 月 9 日*

🦞
