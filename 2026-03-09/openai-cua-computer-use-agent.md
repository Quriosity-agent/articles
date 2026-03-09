# OpenAI CUA：让 AI 像人一样操控电脑

> 深入解析 OpenAI Computer-Using Agent（CUA）及其 GPT-5.4 示例应用

## 什么是 CUA？

CUA（Computer-Using Agent）是 OpenAI 推出的计算机使用代理模型。它的核心理念非常直觉：**让 AI 像人类一样看屏幕、动鼠标、敲键盘**，而不是通过 API 去调用软件。

传统的 AI Agent 需要为每个应用编写专门的 API 集成。CUA 的做法完全不同——它直接处理屏幕像素数据，理解 GUI 界面上的按钮、菜单和文本框，然后通过虚拟鼠标和键盘执行操作。这意味着理论上，**任何人能用的软件，CUA 都能用**。

CUA 最初驱动了 OpenAI 的 [Operator](https://operator.chatgpt.com/) 产品，现在通过 Responses API 开放给开发者。

## CUA 的工作循环

CUA 的核心是一个感知-推理-行动的迭代循环：

- **感知（Perception）**：对当前屏幕截图，模型获得计算机当前状态的视觉快照
- **推理（Reasoning）**：利用 chain-of-thought 推理下一步操作，综合考虑当前和历史截图及动作
- **行动（Action）**：执行点击、滚动、输入等操作，直到任务完成或需要用户介入

这个循环不断重复，直到模型判断任务已完成。遇到敏感操作（如登录、CAPTCHA），CUA 会主动请求用户确认。

## GPT-5.4 CUA 示例应用

[openai-cua-sample-app](https://github.com/donghaozhang/openai-cua-sample-app) 是一个 TypeScript 实现的 CUA 示例项目，展示了如何用 GPT-5.4 构建浏览器自动化工作流。

### 项目架构

项目采用 monorepo 结构，由 pnpm 管理：

- **apps/demo-web** — Next.js 操作控制台，用于启动任务、查看截图和回放
- **apps/runner** — Fastify HTTP 服务，管理工作空间、浏览器会话、SSE 推送和回放数据
- **packages/runner-core** — 核心编排逻辑，包含 Responses 循环、场景执行器和验证
- **packages/browser-runtime** — Playwright 浏览器会话抽象
- **packages/scenario-kit** — 场景清单和 prompt 默认值
- **packages/replay-schema** — 请求/响应/回放/错误的共享契约
- **labs/** — 静态实验模板，运行时复制到独立工作空间

### 两种执行模式

项目支持两种与浏览器交互的模式：

- **native 模式**：直接暴露 Responses API 的 computer tool。模型发出点击、拖拽、输入、等待和截图等原始指令，由 runner 在真实浏览器上执行
- **code 模式**：暴露一个持久的 Playwright JavaScript REPL（`exec_js`）。模型编写 JS 代码来操控浏览器，而不是发出原始鼠标/键盘动作

两种模式共用相同的场景清单和回放管线。

### 核心代码：Responses Loop

整个 CUA 的灵魂在 `packages/runner-core/src/responses-loop.ts` 中。这是一个简化的调用流程：

```typescript
// 1. 创建 OpenAI 客户端
const client = new OpenAI({ apiKey });

// 2. 构建工具定义
// native 模式
const tools = [{ type: "computer" }];
// 或 code 模式
const tools = [{
  type: "function",
  name: "exec_js",
  description: "Execute JavaScript in a persistent Playwright REPL.",
  parameters: {
    properties: {
      code: { type: "string", description: "JS to execute..." }
    },
    required: ["code"]
  }
}];

// 3. 迭代循环
for (let turn = 0; turn < maxResponseTurns; turn++) {
  // 调用 Responses API
  const response = await client.responses.create({
    model: "gpt-5.4",
    instructions: systemPrompt,
    input: conversationHistory,
    tools,
  });

  // 处理 computer_call（native 模式）
  if (hasComputerCall(response)) {
    // 执行鼠标点击、键盘输入等
    await executeActions(response.actions);
    // 截图作为反馈
    const screenshot = await page.screenshot();
    conversationHistory.push(screenshotAsInput(screenshot));
  }

  // 处理 function_call（code 模式）
  if (hasFunctionCall(response, "exec_js")) {
    const result = await executeInRepl(response.arguments.code);
    conversationHistory.push(functionResult(result));
  }

  // 如果模型返回消息而非工具调用，任务完成
  if (isMessageOnly(response)) break;
}
```

关键设计：
- 每个 turn 后截图反馈，让模型看到操作结果
- `computer_call` 包含一批 actions（点击、输入、按键等），批量执行后统一截图
- action 之间有 120ms 默认延迟，模拟人类操作节奏
- 工具执行有 20 秒超时保护
- 支持 abort signal，可随时中止运行

### 内置场景

项目附带三个演示场景：

- **kanban-reprioritize-sprint**：看板拖拽排序——测试有状态的 drag-and-drop 操作
- **paint-draw-poster**：画布绘图——测试精确的光标控制和绘图能力
- **booking-complete-reservation**：预订表单——测试多步骤浏览和表单填写

每个场景都有确定性验证，不是开放式的"随便浏览网页"。

### 快速上手

```bash
git clone https://github.com/donghaozhang/openai-cua-sample-app
cd openai-cua-sample-app
corepack enable
pnpm install
cp .env.example .env
# 编辑 .env 设置 OPENAI_API_KEY

pnpm playwright:install    # 安装 Chromium
pnpm dev                   # 启动开发服务器
# 访问 http://127.0.0.1:3000
```

环境要求：
- Node.js 22.20.0
- pnpm 10.26.0
- Playwright Chromium

关键环境变量：
- `OPENAI_API_KEY` — 必需
- `CUA_DEFAULT_MODEL` — 默认 `gpt-5.4`
- `CUA_RESPONSES_MODE` — `auto`、`fallback` 或 `live`
- `NEXT_PUBLIC_CUA_DEFAULT_MAX_RESPONSE_TURNS` — 默认 24 轮

## CUA vs Anthropic Computer Use：两种路线

OpenAI CUA 和 Anthropic 的 Computer Use 是目前最主要的两个"AI 操控电脑"方案。它们的核心理念相同（看屏幕 → 推理 → 操作），但实现路线有明显差异：

**模型与产品形态**
- OpenAI CUA：基于 GPT-4o 视觉 + 强化学习，通过 Operator 产品和 Responses API 提供
- Anthropic：基于 Claude 3.5 Sonnet，通过 Messages API 的 `computer_20241022` tool 提供

**API 设计**
- OpenAI：`computer` tool type 是一等公民，actions 批量返回（一个 turn 可以包含多个动作）
- Anthropic：每个 tool_use 块返回单个动作（`mouse_move`、`click`、`type` 等），需要更多轮次

**执行环境**
- 这个示例应用用 Playwright 管理浏览器，支持 headless 和 headful
- Anthropic 的官方示例用 Docker 容器跑完整桌面环境（包含 VNC）

**Benchmark 表现**
- CUA 在 OSWorld 上达到 38.1%（Anthropic 之前是 22.0%）
- CUA 在 WebArena 上达到 58.1%
- CUA 在 WebVoyager 上达到 87.0%

**安全机制**
- 两者都强调"不要在高风险环境中使用"
- CUA 有 `pending_safety_checks` 机制，可在敏感操作前暂停
- Anthropic 依赖系统 prompt 中的安全指引

**开发者体验**
- OpenAI 的示例是 TypeScript monorepo，架构清晰，有场景系统和回放功能
- Anthropic 的示例是 Python，相对简单直接，用 Docker 一键启动

## 这意味着什么？

CUA 代表了一种新的 AI 交互范式：不再需要为每个应用写 API 集成，AI 直接使用人类的界面。这对自动化测试、RPA、无障碍辅助等领域有巨大潜力。

但目前的局限也很明显：
- 速度慢——每一步都要截图、传图、推理
- 成本高——大量 token 消耗在图片处理上
- 可靠性有限——复杂任务成功率仍远低于人类（OSWorld 38% vs 人类 72%）
- 安全风险——给 AI 控制电脑本身就是高风险操作

这个示例应用的价值在于：它展示了一个**完整的、生产级架构**来构建 CUA 工作流——从 API 调用、浏览器管理、事件流到回放验证，所有关键环节都有了参考实现。

对于想要探索 AI 计算机操控能力的开发者来说，这是目前最好的起点之一。

---

*2026-03-09*

🦞
