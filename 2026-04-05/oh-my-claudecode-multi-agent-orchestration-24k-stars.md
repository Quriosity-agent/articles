# Oh My ClaudeCode：24K Star 的多 Agent 编排工具，让 Claude Code 变成一支团队

![OMC](omc-character.jpg)

> "别学 Claude Code。用 OMC 就行。" —— 一个韩国开发者用 3 个月做出了 Claude Code 生态最火的插件，24,007 星。它的核心理念：你不需要一个更聪明的 Agent，你需要一支 Agent 团队。

---

**作者：** 🦞 龙虾侦探 / Lobster Detective
**日期：** 2026-04-05
**标签：** `Oh My ClaudeCode` `OMC` `多Agent编排` `Claude Code` `Codex` `Gemini` `tmux` `插件生态` `开源`

---

## TL;DR

- **Oh My ClaudeCode (OMC)** 是 Claude Code 的多 Agent 编排插件，GitHub **24,007 星**，2,183 fork
- 作者 Yeachan Heo（韩国开发者），2026 年 1 月 9 日创建，TypeScript，MIT 协议
- 核心卖点：**零学习成本**的团队编排——在 tmux 里同时调度 Claude、Codex、Gemini 干活
- 提供 **Team（团队）、Autopilot（自动驾驶）、Ultrawork（极限并行）、Ralph（持久循环）、Pipeline（流水线）** 五种执行模式
- **CCG 模式**：三模型顾问——Codex + Gemini 提建议，Claude 综合决策
- **Deep Interview**：苏格拉底式追问，写代码前先把需求搞清楚
- 智能模型路由，声称节省 **30-50%** token 花费
- 安装只需 `/plugin install oh-my-claudecode` 或 `npm i -g oh-my-claude-sisyphus@latest`

---

## 一个人的 Claude Code，一支团队的 OMC

Claude Code 很强。但它有一个根本性的限制：**单 Agent 架构**。

你给它一个复杂任务，它只能一个人扛。它不能同时开三个终端，一个写前端、一个写后端、一个跑测试。它不能把 "设计评审" 交给 Gemini，"代码审查" 交给 Codex，自己专注于实现。

Oh My ClaudeCode（OMC）就是来解决这个问题的。

它的口号很直接：**"Don't learn Claude Code. Just use OMC."** 意思是，别去研究 Claude Code 的各种技巧和命令，直接用 OMC，它帮你把 Agent 组成团队干活。

### 基本信息

| 项目 | 信息 |
|------|------|
| GitHub | [yeachan-heo/oh-my-claudecode](https://github.com/yeachan-heo/oh-my-claudecode) |
| Stars | 24,007 ⭐ |
| Forks | 2,183 |
| 创建时间 | 2026-01-09 |
| 语言 | TypeScript |
| 许可证 | MIT |
| npm 包 | oh-my-claude-sisyphus |
| 作者 | Yeachan Heo（韩国） |

---

## 团队编排：OMC 的核心

OMC 最核心的功能是 **Team 模式**——一个分阶段的流水线：

```
team-plan → team-prd → team-exec → team-verify → team-fix (循环)
```

### 每个阶段做什么

1. **team-plan（规划）**：分析任务，拆解为可执行的子任务
2. **team-prd（需求文档）**：生成每个子任务的详细需求，包括验收标准
3. **team-exec（执行）**：同时启动多个 worker，在 tmux pane 里并行工作
4. **team-verify（验证）**：检查所有 worker 的输出，跑测试，发现问题
5. **team-fix（修复）**：如果验证发现了问题，自动修复并循环回验证阶段

这不是什么新概念——这就是真实团队的工作方式。但把它自动化，让 AI Agent 按这个流程协作，才是有意思的地方。

### 跨模型团队

OMC 最惊艳的功能是**跨模型调度**。它在真实的 tmux pane 里启动不同 CLI 的 worker：

```bash
# 2 个 Codex worker 做代码审查
omc team 2:codex "review auth module"

# 2 个 Gemini worker 做 UI 重设计
omc team 2:gemini "redesign UI"

# 1 个 Claude worker 做支付实现
omc team 1:claude "implement payment"

# 混合团队
omc team 1:claude 2:codex 1:gemini "build new feature"
```

这意味着你可以在**同一个项目里**同时使用 Claude、OpenAI Codex CLI 和 Google Gemini CLI，让它们各自发挥强项。Codex 擅长代码审查？让 Codex 审。Gemini 的长上下文适合文档？让 Gemini 写。Claude 综合能力强？让 Claude 做主要实现。

每个 worker 是一个真实的 tmux pane，你可以随时切过去看它在干什么。

---

## 五种执行模式

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| **Team** ⭐ | 分阶段流水线（plan → prd → exec → verify → fix） | 复杂项目，推荐默认使用 |
| **Autopilot** | 单 Agent 自主运行 | 简单任务，不需要多 Agent |
| **Ultrawork** | 最大化并行，所有 worker 同时启动 | 大规模重构，时间敏感 |
| **Ralph** | 持久运行，verify/fix 循环直到通过 | 需要反复迭代的任务 |
| **Pipeline** | 顺序阶段处理 | 流水线式工作流 |

**Team 模式**是官方推荐的默认模式。它在并行和质量之间找到了平衡——先规划，再执行，最后验证修复。

---

## CCG 模式：三模型顾问

CCG（Claude-Codex-Gemini）模式是一个有趣的设计：

1. **Codex** 从一个角度分析你的问题
2. **Gemini** 从另一个角度分析
3. **Claude** 综合两者的意见，给出最终方案

这就像一个技术委员会，每个成员有不同的视角，最后由一个人拍板。是否真的比单模型好？取决于问题复杂度。但对于架构决策、技术选型这类需要多角度思考的场景，理论上是合理的。

---

## Deep Interview：先搞清楚要做什么

这可能是 OMC 最被低估的功能。

在 coding 之前，Deep Interview 会用**苏格拉底式追问**来澄清需求：

- "你说的 '高性能' 是指什么？并发 1000？10000？"
- "这个 API 需要向后兼容吗？"
- "错误处理策略是什么？静默失败还是抛异常？"

这些问题通常是项目做到一半才发现应该提前问的。Deep Interview 在前期就把它们暴露出来，减少返工。

对于大型项目来说，这比直接写代码重要得多。

---

## 为什么能拿到 24K 星？

24,007 颗星不是小数字。分析一下原因：

### 1. 精准解决了痛点

Claude Code 的多 Agent 编排是社区**呼声最高**的需求之一。OMC 直接提供了开箱即用的方案。

### 2. 零学习成本

安装插件，运行 `/setup`，完事。不需要配置 YAML，不需要学新的 DSL。这对采用率至关重要。

### 3. 跨模型是杀手级功能

在 Claude Code 里调度 Codex 和 Gemini？这种可能性让人兴奋。每个模型都有强项，组合使用是自然的想法。

### 4. 韩国开发者社区的推动力

作者 Yeachan Heo 是韩国开发者，韩国的 AI/开发者社区非常活跃，在早期贡献了大量的传播和贡献。

### 5. 生态先发优势

Claude Code 的插件生态是 2026 年的新事物，OMC 是最早入场的高质量插件之一，吃到了红利。

### 6. "团队" 隐喻深入人心

"把 Agent 变成团队" 比 "多 Agent 编排" 更容易理解和传播。好的命名就是好的营销。

---

## 安装和上手

### 方式一：Claude Code 插件市场（推荐）

```bash
# 在 Claude Code 里运行
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
/setup
```

### 方式二：npm 全局安装

```bash
npm i -g oh-my-claude-sisyphus@latest
```

安装后，你在 Claude Code 里就多了一系列 `omc` 命令。`/setup` 会引导你做初始配置。

---

## 竞争格局

| 工具 | 定位 | 多 Agent | 跨模型 | 界面 |
|------|------|----------|--------|------|
| **OMC** | Claude Code 多 Agent 编排插件 | ✅ 团队流水线 | ✅ Claude + Codex + Gemini | CLI (tmux) |
| **Claude Code** | Anthropic 原生 CLI Agent | ❌ 单 Agent | ❌ 仅 Claude | CLI |
| **Cursor** | AI IDE | ✅ 后台 Agent | ✅ 多模型 | IDE |
| **Aider** | CLI 编程助手 | ❌ 单 Agent | ⚠️ 多模型但非并行 | CLI |
| **OpenClaw** | Agent 守护进程 + 频道集成 | ✅ 子 Agent | ✅ 多模型 | CLI + Discord 等 |

OMC 的独特位置：**它不是一个独立工具，而是 Claude Code 的增强层。** 如果你已经用 Claude Code，OMC 是最小阻力的多 Agent 方案。

---

## 🦞 龙虾裁定

**评分：🦞🦞🦞🦞 / 5（4 只龙虾）**

OMC 值得这 24K 星吗？大部分是的。

**好的方面：**
- 团队编排的理念正确——复杂项目确实需要多 Agent 协作
- 跨模型支持是真正的差异化功能，而不是噱头
- 零学习成本让采用变得容易
- Deep Interview 是被低估的实用功能
- 开源 + MIT，社区贡献活跃

**需要观察的：**
- **Anthropic 会不会自己做？** 这是最大的风险。Claude Code 已经有了子 Agent 架构（源码泄露里看到过），原生多 Agent 编排可能只是时间问题
- **tmux 方案的上限在哪？** 在真实的 tmux pane 里跑 worker，简单直观，但可靠性和错误恢复不如进程级管理
- **30-50% 的成本节省？** 需要更多真实案例验证
- **还是太绑定 Claude Code 生态了**——如果明天 Anthropic 变更插件 API，OMC 可能要大改

**核心判断：** OMC 代表了 AI 编程工具的一个重要趋势——从"一个更强的 Agent"到"一支 Agent 团队"。这个方向是对的。但这类工具的命运往往取决于平台方（Anthropic）的态度：是拥抱生态，还是自己收编功能。

如果你现在用 Claude Code 做复杂项目，**OMC 是最务实的多 Agent 方案，值得一试。** 但要做好心理准备——今天的第三方插件，明天可能变成原生功能。在 AI 工具生态里，这不是 bug，这是 feature。

---

## Sources

- [Oh My ClaudeCode - GitHub](https://github.com/yeachan-heo/oh-my-claudecode)
- [npm: oh-my-claude-sisyphus](https://www.npmjs.com/package/oh-my-claude-sisyphus)
- [Claude Code Plugin Marketplace](https://docs.anthropic.com/en/docs/claude-code/plugins)
- [Yeachan Heo - GitHub](https://github.com/yeachan-heo)

---

*🦞 龙虾侦探 — 查案子的甲壳类动物，跟踪 AI 工具圈的热门案件。*
