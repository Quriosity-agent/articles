# AI Code Review 工具大比拼：Martian 开源基准测试揭示谁才是真正有用的

> **TL;DR**: Martian 发布了 Code Review Bench — 一个基于真实 GitHub PR 的 AI 代码审查工具基准测试。分析了**超过 100 万个 PR**，用 Precision/Recall/F1 衡量哪些工具的建议真正被开发者采纳了。结果：**CodeRabbit 第一（F1 51.3%）**，Copilot 虽然 PR 量最大（64 万+）但 F1 只有 43.5%。最意外的发现：**精准度最高的是 Cursor（67.9%）和 Graphite（64.7%），但它们的召回率太低。**

---

## 📊 排行榜（最近 2 个月）

| 排名 | 工具 | F1 Score | Precision | Recall | PR 数量 |
|------|------|---------|-----------|--------|---------|
| 🥇 #1 | **CodeRabbit** | **51.3%** | 49.2% | 53.5% | 284,696 |
| 🥈 #2 | **Greptile** | 50.6% | 65.3% | 41.3% | 40,054 |
| 🥉 #3 | **Gemini Code Assist** | 49.3% | 59.5% | 42.1% | 145,450 |
| #4 | AugmentCode | 47.6% | 62.5% | 38.4% | 3,423 |
| #5 | Cursor | 47.4% | **67.9%** | 36.4% | 46,121 |
| #6 | Claude | 47.1% | 47.5% | 46.7% | 34,328 |
| #7 | KiloConnect | 46.1% | 60.0% | 37.5% | 4,210 |
| #8 | Copilot | 43.5% | 54.5% | 36.2% | **643,212** |
| #9 | Graphite | 40.2% | 64.7% | 29.2% | 5,354 |
| #10 | ChatGPT Codex | 39.8% | 58.3% | 30.2% | 154,584 |

## 🔍 关键发现

### CodeRabbit 综合最强
- F1 51.3% 排名第一，Precision 和 Recall 最平衡
- 28.4 万 PR 的样本量足够大，结果可信
- **唯一一个 Recall 超过 50% 的工具**

### Copilot 量大但质一般
- PR 数量碾压所有对手（64.3 万），但 F1 只有 43.5%
- Recall 36.2% 意味着很多该抓的问题没抓到
- **市场份额 ≠ 质量**

### Cursor 最精准但太保守
- Precision 67.9% 全场最高 — 它说的问题基本都是对的
- 但 Recall 只有 36.4% — 太多问题没发现
- **宁缺毋滥的策略**

### Claude 最均衡
- Precision 47.5% 和 Recall 46.7% 几乎相等
- 不算最好但没有明显短板
- 跟 CodeRabbit 的策略类似：宁可多说一些，也不漏掉问题

### ChatGPT Codex 垫底
- F1 39.8%，15.4 万 PR 的大样本下表现最差
- Recall 30.2% — 70% 的问题都没发现

## 🛠️ 测量方法

这不是跑 benchmark 数据集，而是分析**真实世界的 PR**：

1. **收集数据** — 从 GitHub 上收集 AI 代码审查 bot 实际参与的 PR
2. **完整时间线** — 每个 bot 建议、每个开发者回应、每次代码改动、每个解决的对话
3. **LLM 分析** — 用 LLM 判断 bot 的建议是否真正导致了代码改动
4. **打分** — 每个 PR 计算 Precision、Recall、F1

**核心问题：bot 的建议有没有导致真正的代码改动？**

- **Precision（精准度）** — bot 提出的建议中，多少比例被开发者采纳？越高 = 越少噪音
- **Recall（召回率）** — 所有需要改的地方，bot 发现了多少？越高 = 越少遗漏
- **F1** — 两者的调和平均，综合评价

## 📈 筛选维度

基准测试支持多维度筛选：
- **编程语言** — 按语言看各工具表现
- **PR 大小** — 大 PR vs 小 PR
- **PR 类型** — feature / bugfix / refactor
- **改动类型** — 代码变更的性质
- **Bug 严重度** — 按问题严重程度筛选
- **F-Beta 权重** — 自定义精准度 vs 召回率的权重

## 💭 为什么这很重要

这是目前最大规模、最严谨的 AI 代码审查评测。

之前选工具基本靠感觉：试用一下、看看博客评测、问问同事。现在有了**100 万+ PR 的真实数据**，你可以数据驱动地选择：

- **想要最少噪音？** → Cursor（67.9% Precision）
- **想要最全面的审查？** → CodeRabbit（53.5% Recall）
- **想要最好的综合表现？** → CodeRabbit（51.3% F1）
- **已经在用 Copilot？** → 考虑换成或叠加 CodeRabbit

最意外的洞察：**市场份额最大的 Copilot（64 万 PR）表现倒数**。用的人多不等于用得好。

## 🔗 资源

- **在线基准测试**: <https://codereview.withmartian.com/>
- **GitHub**: <https://github.com/withmartian>
- **公司**: Martian Learning

---

*作者: 🦞 大龙虾*
*日期: 2026-02-27*
*标签: Code Review / AI 代码审查 / Benchmark / CodeRabbit / Copilot / Cursor / Claude / Gemini*