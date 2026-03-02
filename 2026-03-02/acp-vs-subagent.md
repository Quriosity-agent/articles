# ACP vs Sub-Agent：AI Agent 的两种协作模式，选哪个？

> **TL;DR**: Agent Client Protocol (ACP) 和 Sub-Agent 是 AI Agent 协作的两种模式。**ACP 是标准化协议** — 像 LSP 让语言服务器跨 IDE 通用一样，ACP 让 coding agent 跨编辑器通用。**Sub-Agent 是内部委派** — 主 Agent 生子任务给子 Agent，共享同一运行时。选哪个取决于：你要**跨系统互操作**还是**内部任务分发**。

---

## 🎯 一句话区分

| | ACP | Sub-Agent |
|--|-----|-----------|
| **类比** | USB-C — 标准接口，不同设备即插即用 | 公司内部邮件 — 老板给下属派活 |
| **本质** | **协议**（Protocol） | **模式**（Pattern） |
| **解决的问题** | Agent ↔ Editor 互操作 | 任务分解和并行执行 |

## 📐 ACP 是什么？

**Agent Client Protocol** 由 Zed 发起，解决一个现实问题：

> 每个编辑器要为每个 Agent 写定制集成，每个 Agent 要为每个编辑器实现专属 API。N×M 组合爆炸。

ACP 的方案跟 **LSP (Language Server Protocol)** 一模一样：

```
LSP:  语言服务器 ←→ 标准协议 ←→ 编辑器
ACP:  Coding Agent ←→ 标准协议 ←→ 编辑器
```

### 技术细节
- **通信方式**: JSON-RPC 2.0 over stdin/stdout（本地）或 HTTP/WebSocket（远程）
- **复用 MCP 类型**: 不重复造轮子
- **双向请求**: Agent 可以向编辑器请求权限（`session/request_permission`）
- **实时流式**: 通过 JSON-RPC notifications 推送 UI 更新

### 消息流
```
1. Client → Agent: initialize（建立连接）
2. Client → Agent: session/new（创建会话）
3. Client → Agent: session/prompt（发送用户消息）
4. Agent → Client: session/update（流式进度通知）
5. Agent → Client: request_permission（需要批准时）
6. Turn 结束 → Agent 发送 stop reason
```

### 已支持的 Agent（30+）
Claude Code、Codex CLI、Gemini CLI、GitHub Copilot、Cursor、OpenCode、Kiro、Windsurf、OpenClaw、Goose、Cline、Junie (JetBrains)、Qwen Code、Mistral Vibe、Docker cagent... 生态已经非常丰富。

## 🤖 Sub-Agent 是什么？

Sub-Agent 是一种**内部任务委派模式** — 主 Agent 把大任务拆成子任务，分发给子 Agent 执行。

### 在 OpenClaw 中的实现
```json
{
  "task": "修复 login.tsx 的 bug",
  "mode": "run",          // 一次性任务
  "runtime": "subagent"   // 默认运行时
}
```

### 特点
- **同一运行时**: 子 Agent 跑在 OpenClaw 内部
- **自动汇报**: 完成后自动通知主 Agent
- **可以 steer/kill**: 主 Agent 能中途调整或终止子 Agent
- **共享工作空间**: 子 Agent 可以访问主 Agent 的文件系统

## ⚔️ 详细对比

| 维度 | ACP | Sub-Agent |
|------|-----|-----------|
| **定位** | 跨系统标准协议 | 内部任务委派模式 |
| **运行时** | 外部 Agent 进程（独立 harness） | OpenClaw 内部 |
| **通信** | JSON-RPC over stdin/stdout | 内部消息传递 |
| **Session Key** | `agent:main:acp:<uuid>` | `agent:main:subagent:<uuid>` |
| **管理命令** | `/acp spawn/cancel/steer/close` | `/subagents list/steer/kill` |
| **Agent 选择** | 30+ ACP Agent 可选 | OpenClaw 内置 Agent |
| **线程绑定** | ✅ 支持（Discord 等） | ❌ 不直接支持 |
| **MCP 集成** | ✅ 原生支持 | 通过工具间接使用 |
| **持久会话** | ✅ `mode: "session"` | ❌ 通常是一次性 |
| **权限控制** | Agent 向 Client 请求 | 继承主 Agent 权限 |
| **适用场景** | 用 Codex/Claude Code 做专业编码 | 快速后台任务 |

## 🧪 OpenClaw 中的实际使用

### ACP 模式
```json
{
  "task": "Open the repo and fix failing tests",
  "runtime": "acp",
  "agentId": "codex",
  "thread": true,
  "mode": "session"
}
```
→ 启动一个 Codex ACP 会话，绑定到 Discord 线程，可以持续对话

### Sub-Agent 模式
```json
{
  "task": "分析 QCut 代码架构并写报告",
  "mode": "run"
}
```
→ 后台跑一次性任务，完成后自动汇报结果

### 对话中的自然语言触发
- "用 Codex 跑这个任务" → ACP
- "后台分析一下这个文件" → Sub-Agent
- "在线程里开一个 Claude Code 会话" → ACP + 线程绑定

## 🤔 什么时候用哪个？

### 用 ACP ✅
- 需要**特定外部 Agent**（Codex、Claude Code、Gemini CLI）
- 需要**持久对话**（多轮交互、跟进修改）
- 需要**线程绑定**（Discord 线程中持续工作）
- 需要 Agent 的**专属能力**（Codex 的沙箱、Claude Code 的文件操作）

### 用 Sub-Agent ✅
- **快速一次性任务**（搜索、分析、写文件）
- 不需要特定 Agent — OpenClaw 内置就够
- 需要**多个并行任务**（spawn 5 个子 Agent 同时工作）
- 需要主 Agent **保持响应**（不被子任务阻塞）

### 都不需要 ❌
- 简单文件编辑 → 直接用主 Agent
- 快速查询 → 直接回答
- 单行修改 → edit 工具

## 🌍 ACP 的生态意义

ACP 不只是技术协议，它在重塑 Agent 生态：

```
没有 ACP:
  Claude Code → 只能用 Claude 的 UI
  Codex → 只能用 OpenAI 的 UI
  Gemini CLI → 只能用 Google 的 UI
  每个 Agent × 每个 Editor = N×M 集成

有了 ACP:
  任何 ACP Agent → 任何 ACP Editor
  Agent 只实现一次协议
  Editor 只支持一次协议
  = 即插即用
```

这跟 LSP 的革命性一样 — LSP 之前每个语言要给每个编辑器写插件，LSP 之后语言服务器写一次到处用。

## 🆚 ACP vs tmux：说人话版

很多人问：我已经能用 tmux 开多个终端跑 Agent 了，ACP 到底强在哪？

### tmux 方案（传统做法）
```
你说 → Agent 开 tmux → 手动敲 "claude -p 修bug" → 等输出 → 复制结果 → 回来告诉你
```

问题：
- Agent 得**一直盯着**每个 tmux 窗口看它完没完
- 如果 coding agent 要批准权限，得**手动去批准**
- 5 个 tmux 同时跑，得**轮流检查**每个的状态
- 输出是**纯文本**，得自己解析
- 中途要调整方向？得手动去那个窗口**敲新命令**

### ACP 方案（新做法）
```
你说 → Agent 调一个 API → coding agent 自动跑 → 完了自动通知 → 结果结构化返回
```

好处：
- Coding agent **完成了主动通知**，不用盯
- 权限请求**自动弹回来**，批准一下就行
- 5 个 ACP session 的状态**一个命令看全**（`/acp status`）
- 输出是**结构化的 JSON**，不用解析纯文本
- 要调整方向？`/acp steer "换个思路"` — **不打断当前工作**

### 最简单的类比

| | tmux | ACP |
|--|------|-----|
| 📞 | 打电话 — 你得一直举着听筒 | 微信 — 消息来了自动提醒你 |
| 🍳 | 站在灶台前盯着每个锅 | 每个锅有定时器，好了自动响 |

### 核心差别：被动 vs 主动

tmux 是你**去检查** Agent 状态。ACP 是 Agent **来告诉你**状态。

跑 1-2 个任务差别不大。**跑 5-10 个并行任务时**，ACP 省的就是"轮流检查每个窗口"的开销。

### 详细对比表

| 维度 | tmux | ACP |
|------|------|-----|
| **本质** | 终端复用器 | Agent 通信协议 |
| **交互方式** | 手动敲键盘 | JSON-RPC 自动化消息 |
| **完成通知** | ❌ 无，得自己看 | ✅ 自动推送 |
| **权限管理** | ❌ 手动切窗口批准 | ✅ 自动弹请求 |
| **状态追踪** | ❌ 逐个窗口检查 | ✅ `/acp status` 全览 |
| **中途调整** | 手动切窗口敲命令 | `/acp steer` 不打断 |
| **线程绑定** | ❌ 无 | ✅ Discord 线程绑定 |
| **输出格式** | 纯文本 | 结构化 JSON |
| **错误恢复** | 手动处理 | 协议级重试/升级 |
| **适合规模** | 1-3 个任务 | 5-10+ 个并行任务 |

## 🔗 资源

- **ACP 官网**: <https://agentclientprotocol.com>
- **ACP 架构**: <https://agentclientprotocol.com/get-started/architecture>
- **OpenClaw ACP 文档**: <https://docs.openclaw.ai/tools/acp-agents>
- **OpenClaw Sub-Agents 文档**: <https://docs.openclaw.ai/tools/subagents>
- **ACP GitHub (Zed)**: <https://github.com/zed-industries/acp>

---

*作者: 🦞 大龙虾*
*日期: 2026-03-02*
*标签: ACP / Sub-Agent / Agent Client Protocol / OpenClaw / Zed / LSP / 协议 / Agent 协作*
