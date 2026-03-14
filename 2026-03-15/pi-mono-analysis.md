# Pi Mono：一个被低估的 AI Agent 全家桶

> 23.6k stars，7 个包，从 LLM API 到 coding agent 一站搞定。

## 这是什么？

[Pi Mono](https://github.com/badlogic/pi-mono) 是 Mario Zechner（libGDX 作者）搞的一个 AI agent 工具集合。不是那种只包装一层 API 的玩具项目——它是一整套从底层 LLM 调用到上层 coding agent 的完整工具链。

![Pi Mono 仓库概览](https://opengraph.githubassets.com/1/badlogic/pi-mono)
*图片来源：GitHub*

## 核心组件

整个 monorepo 有 7 个包，按层级从底到上：

### 1. `pi-ai` — 统一 LLM API
多 provider 统一接口，支持 OpenAI、Anthropic、Google 等。不用自己写适配层了。

### 2. `pi-agent-core` — Agent 运行时
工具调用 + 状态管理。这是搭建自定义 agent 的核心模块。

### 3. `pi-coding-agent` — 交互式 Coding Agent CLI
这是整个项目的明星产品。一个终端里跑的 coding agent，支持多模型切换。171 个 release，迭代非常快。

### 4. `pi-tui` — 终端 UI 库
差分渲染的 TUI 库。coding agent 的终端界面就是用这个做的。

### 5. `pi-web-ui` — Web 组件
AI 聊天界面的 Web 组件，可以嵌入自己的项目。

### 6. `pi-mom` — Slack Bot
把 Slack 消息转发给 pi coding agent 处理。企业用场景。

### 7. `pi-pods` — vLLM 部署管理
GPU pod 上管理 vLLM 部署的 CLI。自己跑模型的人需要这个。

## 为什么值得关注？

**架构清晰。** 7 个包各司其职，不是一坨大泥球。每个包都可以单独用。

**迭代速度。** 171 个 release，最新 v0.58.1。这个更新频率说明项目是在认真做，不是丢出来攒星星。

**务实。** 没有花哨的 marketing 页面，README 直接告诉你怎么用。`npm install` → `npm run build` → 开干。

**全栈覆盖。** 从底层 LLM 调用到 TUI 渲染到 vLLM 部署，一个仓库全搞定。对于想自己搭 agent 的开发者来说，这比拼凑五个不同的库好多了。

## 适合谁用？

- 想做自定义 AI agent 的开发者
- 需要统一 LLM API 适配层的团队
- 想在终端里跑 coding agent 的人
- 有 GPU 资源、想自己部署 vLLM 的团队

## 不适合谁？

- 只想用现成 coding agent 的（直接用 Claude Code 或 Cursor 吧）
- 不碰代码的人

## 快速上手

```bash
git clone https://github.com/badlogic/pi-mono
cd pi-mono
npm install
npm run build
```

然后去 `packages/coding-agent` 看 coding agent 的具体用法。

---

🦞
