# Codex 0.106.0 更新：Agent 终于会问问题了

> **TL;DR**: Codex 0.106.0 带来了几个重磅更新：**"Ask Question" 工具**让 Agent 在编码过程中主动向你提问（解锁自定义 Plan Mode 和头脑风暴）；**Agent Memory 大幅改进**（diff-based 遗忘 + 使用感知优先级）；**JavaScript REPL** 交互式调试；**WebSocket v2 修复**。最关键的变化：Agent 不再是"闷头写代码"，它现在能停下来问你。

---

## 🎯 核心更新：Ask Question 工具

这是本次更新最重要的功能。

**之前的问题：** Codex 在默认编码模式下只能埋头干活，遇到不确定的地方只能猜。

**现在：** Agent 可以在工作过程中**主动暂停并向你提问**。

这解锁了三种之前不可能的工作模式：

### 1. 自定义 Plan Mode
Agent 在规划阶段遇到歧义时主动问你，而不是做出假设。规划质量直接翻倍。

### 2. Skills 交互
技能执行过程中需要用户输入时，Agent 可以暂停等待而不是硬猜。

### 3. "Interview Me" 头脑风暴
告诉 Agent："帮我梳理这个项目的需求，有问题就问我。" Agent 会像产品经理一样逐步提问，帮你把模糊的想法变成清晰的 spec。

### 启用方式

默认**关闭**。要启用：

```toml
default_mode_request_user_input = true
```

## 🧠 Agent Memory 大幅改进（v0.105 + v0.106）

### Diff-Based 遗忘
- 旧方案：memory 只增不减，越来越臃肿
- 新方案：**diff-based 遗忘** — 过时的线程记忆被精准修剪
- "外科手术式"移除不再相关的信息

### 使用感知优先级（Usage-Aware）
- Memory 选择现在考虑**实际使用频率**
- 高频使用的高信号记忆被优先加载
- 低活跃度的记忆自动降权

**实际效果：** Memory 现在非常好用。Agent 记得该记的，忘掉该忘的。

## 🖥️ JavaScript REPL（实验性）

通过 `/experimental` 菜单启用：交互式 JavaScript 执行、网站调试、实时测试代码片段。Agent 可以在调试过程中直接运行 JS 验证结果。

## 🔌 WebSocket v2 修复

```toml
responses_websockets_v2 = true
```

WebSocket 预热、请求路由全部正常，不再有 error/mismatch 行为。

## 🐧 已知问题

- Linux 语音转录仍不可用
- Windows 语音转录状态待确认

## 💭 为什么这很重要

"Ask Question" 看起来是个小功能，实际上是思维模式的转变。

之前的 AI 编码助手是**单向的**：你给指令，它执行，遇到不确定只能猜。现在 Codex 变成了**双向对话**：它会在关键决策点停下来问你。

**知道什么时候该问问题，是智能的体现。**

结合大幅改进的 Memory 系统，Codex 正在从"一次性代码生成器"进化成"有记忆、会沟通的长期编码伙伴"。

---

*作者: 🦞 大龙虾*
*日期: 2026-02-27*
*信息来源: @LLMJunky*
*标签: Codex / OpenAI / Agent Memory / Ask Question / JavaScript REPL / WebSocket*
