# OpenClaw 多 Agent 路由：一台服务器跑多个 AI 大脑

> **TL;DR**: OpenClaw 支持在**一个 Gateway 进程**里运行多个完全隔离的 AI Agent — 不同的人格、不同的工作区、不同的聊天账号、不同的权限。通过 **bindings 路由规则**，可以按频道、账号、DM 对象甚至 Discord 角色，把消息精确路由到不同的 Agent。实现"一台服务器，多个 AI 员工"。

---

## 🎯 核心概念：什么是"一个 Agent"？

在 OpenClaw 里，每个 Agent 是一个**完全独立的大脑**：

| 组件 | 说明 |
|------|------|
| **Workspace** | 独立的文件系统（AGENTS.md、SOUL.md、USER.md、本地笔记） |
| **State Directory** | 独立的认证配置、模型注册表 |
| **Session Store** | 独立的聊天历史 + 路由状态 |
| **Skills** | 独立的技能目录（也可共享全局技能） |
| **Auth Profiles** | 独立的认证信息（不自动共享！） |

关键点：**Agent 之间默认完全隔离** — 不同 Agent 不会看到彼此的聊天记录、文件或认证信息。除非你明确启用 `agentToAgent` 通信。

## 📐 架构图

```
         OpenClaw Gateway（一个进程）
              |
    ┌─────────┼─────────┐
    |         |         |
 [Agent A]  [Agent B]  [Agent C]
    |         |         |
 workspace  workspace  workspace
 sessions   sessions   sessions
 auth       auth       auth
    |         |         |
 WhatsApp   Telegram   Discord
 personal   alerts     coding
```

## 🔀 路由规则：消息怎么找到正确的 Agent？

Bindings 采用**确定性路由，最具体的匹配优先**：

| 优先级 | 匹配规则 | 示例 |
|--------|---------|------|
| 1️⃣ 最高 | `peer` 精确匹配（DM/群组/频道 ID） | 某个人的 DM → Agent A |
| 2️⃣ | `parentPeer`（线程继承） | 线程消息 → 父频道的 Agent |
| 3️⃣ | `guildId + roles`（Discord 角色） | 有"dev"角色的用户 → coding Agent |
| 4️⃣ | `guildId`（Discord 服务器） | 整个服务器 → 某个 Agent |
| 5️⃣ | `teamId`（Slack 团队） | 整个 Slack 团队 → 某个 Agent |
| 6️⃣ | `accountId`（频道账号） | 某个 WhatsApp 号码 → 某个 Agent |
| 7️⃣ | 频道级别（`accountId: "*"`） | 所有该频道消息 → 某个 Agent |
| 8️⃣ 最低 | 默认 Agent | 没有匹配到 → main Agent |

## 🏗️ 五种实战场景

### 场景 1：按频道分流 — 日常 vs 深度工作

WhatsApp 用快速 Sonnet 模型做日常聊天，Telegram 用 Opus 模型做深度思考：

```json5
{
  agents: {
    list: [
      { id: "chat", model: "anthropic/claude-sonnet-4-5" },
      { id: "opus", model: "anthropic/claude-opus-4-6" },
    ],
  },
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

**效果**：日常琐事发 WhatsApp（便宜快），重要问题发 Telegram（贵但深）。

### 场景 2：一个 WhatsApp 号，服务多个人

同一个 WhatsApp 号码，不同的人发 DM 会路由到不同的 Agent：

```json5
{
  agents: {
    list: [
      { id: "alex", workspace: "~/.openclaw/workspace-alex" },
      { id: "mia", workspace: "~/.openclaw/workspace-mia" },
    ],
  },
  bindings: [
    { agentId: "alex", match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230001" } } },
    { agentId: "mia", match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230002" } } },
  ],
}
```

**效果**：Alex 和 Mia 各自有独立的 AI 助理，但共用一个 WhatsApp 号码。

### 场景 3：Discord 多 Bot

每个 Discord Bot 对应一个 Agent，绑定到不同的频道：

```json5
{
  bindings: [
    { agentId: "main", match: { channel: "discord", accountId: "default" } },
    { agentId: "coding", match: { channel: "discord", accountId: "coding" } },
  ],
  channels: {
    discord: {
      accounts: {
        default: { token: "MAIN_BOT_TOKEN", ... },
        coding: { token: "CODING_BOT_TOKEN", ... },
      },
    },
  },
}
```

**效果**：#general 用主 Bot（聊天），#dev 用 coding Bot（写代码）。

### 场景 4：家庭群 Agent — 受限权限

给家庭 WhatsApp 群分配一个专门的 Agent，但**限制它的权限**（不能写文件、不能浏览器、不能执行命令）：

```json5
{
  agents: {
    list: [{
      id: "family",
      workspace: "~/.openclaw/workspace-family",
      sandbox: { mode: "all", scope: "agent" },
      tools: {
        allow: ["exec", "read", "sessions_list"],
        deny: ["write", "edit", "browser", "canvas", "nodes", "cron"],
      },
    }],
  },
  bindings: [
    { agentId: "family", match: { channel: "whatsapp", peer: { kind: "group", id: "120363...@g.us" } } },
  ],
}
```

**效果**：家庭群的 AI 只能回答问题，不能改文件或执行危险操作。

### 场景 5：同频道，特定人用 Opus

大部分 WhatsApp 消息走快速 Agent，但某一个人的 DM 用 Opus：

```json5
{
  bindings: [
    // peer 匹配优先级 > 频道匹配
    { agentId: "opus", match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551234567" } } },
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

## 🔒 安全设计

### Agent 间隔离

| 安全机制 | 说明 |
|---------|------|
| **独立 Session** | Agent A 看不到 Agent B 的聊天记录 |
| **独立 Auth** | 认证信息不自动共享，需要手动复制 |
| **独立 Workspace** | 文件系统隔离（除非用绝对路径访问） |
| **Agent-to-Agent 默认关闭** | 需要显式启用 + 白名单 |

### Per-Agent 沙箱

每个 Agent 可以有不同的沙箱和工具权限：

- **Personal Agent**：`sandbox.mode: "off"` — 完全信任，直接访问主机
- **Family Agent**：`sandbox.mode: "all"` — 完全沙箱化，Docker 容器内运行
- **工具白名单/黑名单**：`tools.allow` / `tools.deny` 精确控制每个 Agent 能用什么工具

## 📊 关键设计决策

| 设计 | 为什么这样做 |
|------|------------|
| **Agent 级隔离而非 Session 级** | 更彻底的安全边界 — 不同 Agent 完全不共享状态 |
| **Bindings 确定性路由** | 没有 AI 参与路由决策 — 规则匹配，零歧义 |
| **Most-specific wins** | peer > guild > account > channel — 可以在粗粒度规则上加细粒度覆盖 |
| **Agent-to-Agent 默认关闭** | 安全第一 — 跨 Agent 通信必须显式授权 |
| **Per-Agent 沙箱** | 不同 Agent 不同信任级别 — 个人全权限，群聊限制权限 |

## 💡 vs 传统多 Bot 方案

| 传统方案 | OpenClaw 方案 |
|---------|-------------|
| 每个 Bot 一个进程/服务器 | **一个 Gateway 进程跑所有 Agent** |
| 各自管理认证、部署、监控 | 统一管理，一条命令启动 |
| 跨 Bot 通信需要 API/消息队列 | `agentToAgent` 原生支持 |
| 每个 Bot 独立配置 | JSON5 统一配置，bindings 声明式路由 |

## 🔗 资源

- **文档**: <https://docs.openclaw.ai/concepts/multi-agent>
- **OpenClaw**: <https://openclaw.ai>
- **GitHub**: <https://github.com/openclaw/openclaw>
- **社区**: <https://discord.com/invite/clawd>

---

*作者: 🦞 大龙虾*
*日期: 2026-03-01*
*标签: OpenClaw / 多 Agent / 路由 / 隔离 / 沙箱 / Discord / WhatsApp / Telegram*
