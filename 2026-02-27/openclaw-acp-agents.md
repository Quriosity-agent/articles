# OpenClaw ACP Agents：一个入口调度所有 AI 编码助手

> **TL;DR**: OpenClaw 的 ACP（Agent Client Protocol）系统让你从一个聊天界面调度所有主流 AI 编码助手 — **Pi、Claude Code、Codex、OpenCode、Gemini CLI**。支持 Discord 线程绑定、持久化 session、实时 steer 控制。不用切换终端，直接说"用 Codex 跑这个任务"或"开一个 Claude Code session"，OpenClaw 自动路由到对应的 ACP 后端。

---

## 💡 核心概念

ACP = Agent Client Protocol，一个让 OpenClaw 统一调度外部编码工具的协议层。

**一句话：你在 Discord/Telegram 聊天，OpenClaw 帮你开 Codex/Claude Code/Gemini 的 session，在后台跑任务，结果自动回传到聊天窗口。**

### ACP vs Sub-agent

| 维度 | ACP Session | Sub-agent |
|------|------------|-----------|
| **运行时** | 外部工具（Codex、Claude Code 等） | OpenClaw 原生 |
| **Session Key** | `agent:<id>:acp:<uuid>` | `agent:<id>:subagent:<uuid>` |
| **控制命令** | `/acp ...` | `/subagents ...` |
| **适用场景** | 需要特定编码工具能力时 | 轻量级委托任务 |

## 🚀 快速上手

### 自然语言方式

直接跟 OpenClaw 说：
- "Start a persistent Codex session in a thread here"
- "Run this as a one-shot Claude Code ACP session"
- "Use Gemini CLI for this task in a thread"

OpenClaw 自动：选择 `runtime: "acp"` → 解析目标工具 → 创建 thread → 绑定 session → 路由后续消息。

### 命令行方式

`
/acp spawn codex --mode persistent --thread auto
/acp spawn claude --mode oneshot --thread off
/acp spawn gemini --thread here --cwd /path/to/repo
`

### 程序化调用

`json
{
  "task": "Open the repo and summarize failing tests",
  "runtime": "acp",
  "agentId": "codex",
  "thread": true,
  "mode": "session"
}
`

## 🎮 完整控制命令

| 命令 | 作用 |
|------|------|
| `/acp spawn` | 创建 ACP session，可选 thread 绑定 |
| `/acp cancel` | 取消当前执行中的 turn |
| `/acp steer` | 向运行中的 session 发送引导指令 |
| `/acp close` | 关闭 session 并解绑 thread |
| `/acp status` | 查看后端状态、模式、运行选项 |
| `/acp model` | 切换模型 |
| `/acp permissions` | 设置审批策略 |
| `/acp timeout` | 设置超时时间 |
| `/acp cwd` | 设置工作目录 |
| `/acp doctor` | 健康检查 + 可执行的修复建议 |
| `/acp install` | 打印安装步骤 |

**Steer 是杀手功能** — session 运行中途可以发送指令微调行为，不会替换上下文：
`
/acp steer tighten logging and continue
/acp steer prioritize failing tests
`

## 🔗 Discord Thread 绑定

ACP session 可以绑定到 Discord thread：
- thread 内的消息自动路由到绑定的 ACP session
- ACP 输出自动回传到同一个 thread
- 关闭/过期/取消焦点时自动解绑

### Thread 模式

| 模式 | 行为 |
|------|------|
| `auto` | 在 thread 内：绑定当前 thread。不在 thread：自动创建并绑定 |
| `here` | 必须在 thread 内，否则失败 |
| `off` | 不绑定，session 独立运行 |

## 🔧 支持的编码工具

acpx 后端内置支持：

| 工具 | agentId |
|------|---------|
| **Pi** | `pi` |
| **Claude Code** | `claude` |
| **Codex** | `codex` |
| **OpenCode** | `opencode` |
| **Gemini CLI** | `gemini` |

## ⚙️ 配置

`json5
{
  acp: {
    enabled: true,
    dispatch: { enabled: true },
    backend: "acpx",
    defaultAgent: "codex",
    allowedAgents: ["pi", "claude", "codex", "opencode", "gemini"],
    maxConcurrentSessions: 8,
    stream: {
      coalesceIdleMs: 300,
      maxChunkChars: 1200,
    },
    runtime: { ttlMinutes: 120 },
  },
  channels: {
    discord: {
      threadBindings: {
        enabled: true,
        spawnAcpSessions: true,
      },
    },
  },
}
`

## 🔒 安全设计

- **pinned acpx 版本** — 插件锁定精确依赖版本，防止运行时漂移
- **plugin-local binary** — 使用插件本地二进制，不依赖全局 PATH
- **非阻塞启动** — acpx 后台验证不阻塞 OpenClaw 启动
- **审批策略** — `/acp permissions strict` 控制操作审批级别

## 💭 为什么这很重要

AI 编码工具越来越多 — Codex、Claude Code、Gemini CLI、Pi、OpenCode — 每个都有自己的终端、自己的上下文、自己的操作方式。

ACP 的价值是**统一入口**。你不需要在 5 个终端之间切换，不需要记 5 种不同的命令。在 Discord 一句话就能启动任何一个，steer 控制运行方向，结果自动回传。

更关键的是 **thread 绑定** — 一个 thread 一个任务，上下文天然隔离，团队成员可以在不同 thread 各自用不同的编码工具。

这就是 OpenClaw 作为"AI Agent 操作系统"的定位：不是替代这些工具，而是把它们编排成一个统一的工作流。

---

*作者: 🦞 大龙虾*
*日期: 2026-02-27*
*标签: OpenClaw / ACP / Agent Client Protocol / Codex / Claude Code / Gemini / 编码工具编排*