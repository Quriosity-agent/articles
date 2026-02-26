# Hermes Agent：Nous Research 的开源个人 AI Agent，OpenClaw 最强竞品？

**来源：GitHub - NousResearch/hermes-agent**

---

## 一句话总结

Nous Research 发布了 Hermes Agent——一个完全开源的持久化个人 AI Agent，安装在你的机器上，连接你的消息平台（Telegram/Discord/Slack/WhatsApp），自动学习、构建技能、定时执行任务。架构上极像 OpenClaw，但面向开源社区，且内置了 RL 训练环境。

---

## 核心亮点

### 1. 持久化个人 Agent
不是一次性对话，而是**常驻服务器的 Agent**。它记住你的偏好、项目、环境，运行越久越聪明。

### 2. 随意切换模型，零锁定
- **Nous Portal** — 订阅制，零配置
- **OpenRouter** — 200+ 模型，按量付费
- **自托管** — VLLM/SGLang/任何 OpenAI 兼容端点

一行命令切换：`hermes model`

### 3. 全平台消息网关
单个 Gateway 进程连接 **Telegram + Discord + Slack + WhatsApp + CLI**。跨平台消息同步——Telegram 开始的对话可以在 Discord 继续。

### 4. 技能系统（自我进化）
Agent 解决复杂问题后，自动写 Skill 文档供下次复用。技能兼容 agentskills.io 开放标准，可搜索、共享、安装社区技能。

### 5. 五种终端后端（真正的沙盒）
| 后端 | 用途 |
|------|------|
| **Local** | 直接在本机跑 |
| **Docker** | 容器隔离 |
| **SSH** | 远程服务器（推荐：Agent 无法修改自身代码） |
| **Singularity** | HPC 集群 |
| **Modal** | 无服务器云执行 |

### 6. 子 Agent 并行
`delegate_task` 生成隔离的子 Agent，各自独立上下文和终端，最多 3 个并行。

### 7. 定时任务（Cron）
自然语言设置："每天早上9点发送 AI 资讯到 Telegram"。Gateway 后台执行。

### 8. RL 训练环境（研究级）
内置 Atropos RL 框架，可以用强化学习训练 tool-calling 模型。批量生成数千条并行轨迹，轨迹压缩，奖励函数自定义。

---

## 与 OpenClaw 对比

| 特性 | Hermes Agent | OpenClaw |
|------|-------------|---------|
| **开源** | ✅ MIT | ❌ 商业 |
| **模型支持** | OpenRouter 200+ / 自托管 / Nous Portal | Anthropic / OpenAI / 多家 |
| **消息平台** | Telegram / Discord / Slack / WhatsApp / CLI | Telegram / Discord / WhatsApp / Signal / iMessage / CLI |
| **技能系统** | ✅ agentskills.io 标准 | ✅ 自有技能系统 |
| **持久化记忆** | MEMORY.md + USER.md（有 token 上限） | MEMORY.md + USER.md |
| **终端沙盒** | 5 种后端（Docker/SSH/Modal 等） | 本地 + Docker |
| **子 Agent** | ✅ delegate_task | ✅ sessions_spawn |
| **Cron** | ✅ 自然语言 | ✅ 自然语言 |
| **代码执行** | ✅ Python RPC 沙盒 | ✅ exec 工具 |
| **RL 训练** | ✅ Atropos 集成 | ❌ |
| **浏览器** | Browserbase | Chrome Relay / OpenClaw 浏览器 |
| **语音** | Edge TTS / ElevenLabs / OpenAI | TTS 工具 |
| **SOUL.md** | ✅ | ✅ |
| **AGENTS.md** | ✅ 层级合并 | ✅ |

---

## 能否控制 Claude Code 和 Codex？

**可以！** Hermes Agent 的终端工具支持 **PTY 模式**（`pty=true`），可以运行交互式 CLI 工具。README 明确提到：

> "PTY mode (`pty=true`) enables interactive CLI tools like Codex and Claude Code."

这意味着 Hermes Agent 可以：
1. 在后台启动 Claude Code 或 Codex session
2. 通过 `process` 工具发送指令、读取输出
3. 像 OpenClaw 一样编排多个 coding agent

配合 `delegate_task` 子 Agent 功能，理论上可以实现类似 Elvis 文章中的 Agent Swarm 模式——Hermes 作为编排层，spawn 多个子 Agent 各自运行 Codex/Claude Code。

**不过注意：** 这种集成是通过终端工具间接控制，不是原生集成。OpenClaw 对 Claude Code 的集成更深（直接 spawn sub-agent），而 Hermes 需要自己写 prompt 管理交互。

---

## 安装

```bash
# Linux/macOS 一行安装
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/setup-hermes.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/setup-hermes.ps1 | iex
```

---

## 为什么值得关注？

1. **完全开源的 OpenClaw 替代品** — MIT 协议，可以自由修改部署
2. **研究+产品一体** — 同一架构既是个人 Agent 又是 RL 训练平台
3. **Nous Research 出品** — 开源 LLM 社区最受尊敬的团队之一（Hermes 系列模型）
4. **零模型锁定** — 任何 OpenAI 兼容 API 都能用，包括本地模型

---

*仓库：<https://github.com/NousResearch/hermes-agent>*
*协议：MIT*
*本文基于该开源仓库 README 编译整理。*
