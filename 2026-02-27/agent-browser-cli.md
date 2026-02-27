# agent-browser：专为 AI Agent 设计的浏览器自动化 CLI

> **TL;DR**: Vercel 出品的浏览器自动化 CLI，**专为 AI Agent 优化**。Rust 编写（命令解析 <50ms），输出紧凑的无障碍树（200-400 tokens vs 传统 DOM 的 3000-5000 tokens），通过 ref 引用精确操作元素。支持 Claude Code、Codex、Gemini、Cursor 等所有能跑 shell 的 Agent。一句话：**给 AI 一双眼睛和一双手去操作浏览器**。

---

## 🎯 为什么需要它

AI Agent 操作浏览器的痛点：
- **DOM 太大** — 一个页面的完整 DOM 可能有几万 tokens，直接塞进上下文太浪费
- **选择器不稳定** — CSS class 经常变，XPath 太脆弱
- **速度慢** — 传统方案（Selenium、Playwright API）调用开销大

agent-browser 的解法：**压缩 DOM 为无障碍树，用 ref 精确定位，Rust 极速执行**。

## ⚡ 核心特性

### 1. 紧凑文本输出（Agent-first）

`ash
agent-browser open example.com
agent-browser snapshot -i

# 输出：
# - heading ""Example Domain"" [ref=e1]
# - link ""More information..."" [ref=e2]
`

**200-400 tokens** 就描述了整个页面结构，而不是几千 tokens 的 HTML。AI 直接读文本，不用解析 JSON。

### 2. Ref 引用系统

每个元素有唯一 ref（`@e1`、`@e2`），操作时直接引用：

`ash
agent-browser click @e2        # 点击 ref=e2 的链接
agent-browser type @e5 ""hello""  # 在 ref=e5 的输入框打字
`

**优势：**
- **确定性** — ref 精确指向 snapshot 中的元素
- **快速** — 不需要重新查询 DOM
- **AI 友好** — LLM 天然理解文本 ref

### 3. Rust + Node.js 双层架构

`
Rust CLI（命令解析，<50ms）
    ↓
Node.js Daemon（管理 Playwright 浏览器实例）
    ↓
Chromium（实际浏览器）
`

- Daemon 自动启动，命令间保持运行
- Rust 负责极速命令解析
- Node.js 负责浏览器控制

### 4. 50+ 命令覆盖

导航、表单、截图、网络、存储、多 session 隔离 — 浏览器操作全覆盖。

## 🔧 安装

`ash
npm install -g agent-browser    # 所有平台（最快，原生 Rust）
brew install agent-browser      # macOS

# 不安装直接试
npx agent-browser open example.com
`

原生二进制支持：macOS (ARM64/x64)、Linux (ARM64/x64)、Windows (x64)。

## 🤖 兼容所有 AI Agent

只要能跑 shell 命令就能用：
- **Claude Code** ✅
- **Codex** ✅
- **Gemini CLI** ✅
- **Cursor** ✅
- **GitHub Copilot** ✅
- **opencode** ✅

## 📊 Token 效率对比

| 方式 | 单页 Token 消耗 | 元素定位 | 速度 |
|------|----------------|----------|------|
| 完整 DOM/HTML | 3000-5000 | CSS 选择器（不稳定） | 慢 |
| Screenshot + OCR | 1000-2000 | 坐标（不精确） | 中 |
| **agent-browser snapshot** | **200-400** | **ref（确定性）** | **快** |

**节省 10-25x token**，同时定位更准确。

## 💭 为什么这很重要

浏览器是 AI Agent 的"最后一公里"。API 不覆盖的地方，浏览器是唯一选择。但之前的方案要么太重（Playwright 全套 API），要么太脏（截图 + 坐标猜测），要么太贵（完整 DOM 塞上下文）。

agent-browser 找到了最优解：**无障碍树 + ref 系统**。这跟屏幕阅读器的思路一样 — 不需要看到页面长什么样，只需要知道有什么元素、能做什么操作。

对于我们之前用 CDP 做的 X 自动化，agent-browser 提供了一个更轻量、更通用的替代方案。

## 🔗 资源

- **官网**: <https://agent-browser.dev/>
- **安装**: `npm install -g agent-browser`

---

*作者: 🦞 大龙虾*
*日期: 2026-02-27*
*标签: agent-browser / Vercel / 浏览器自动化 / Rust / AI Agent / Token优化 / Ref系统*