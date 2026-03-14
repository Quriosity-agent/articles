# QCut 内嵌 AI Agent：Anthropic Claude SDK vs Pi Mono 选型对比

> 给 QCut 视频编辑器内嵌一个 AI Agent，让用户用自然语言剪视频。该选哪个 SDK？

## 背景

QCut 是一个 Electron + React 视频编辑器，已有：
- **87+ CLI 命令**，全部 JSON 输出，支持 session 模式
- **19 个 Claude Code Skills**（`.agents/skills/`）
- 完整的 TypeScript 代码库

目标：让终端用户（不装 Claude Code / Codex）直接在 QCut 里用自然语言编辑视频。

## 候选方案

| 维度 | Anthropic Claude SDK | Pi Mono |
|------|---------------------|---------|
| **包名** | `@anthropic-ai/sdk` | `badlogic/pi-mono`（7 个子包） |
| **协议** | MIT | MIT |
| **Stars** | ~15K | ~23.6K |
| **维护** | Anthropic 官方团队 | Mario Zechner 一人维护 |
| **模型支持** | 仅 Claude | 全供应商（OpenAI、Google、Anthropic、本地等） |
| **提供什么** | API 客户端 + Tool Calling | 统一 LLM API + Agent Runtime + TUI + Web UI |
| **Agent 循环** | 需自己写 | 内置 |
| **TypeScript** | ✅ 原生 | ✅ 原生 |

## 1. 架构对比：各自提供什么 vs QCut 需要自建什么

### Anthropic Claude SDK
```
你得到的：API 调用 + Tool Calling 协议
你要自建的：Agent 循环、工具注册、上下文管理、错误重试、UI
```

Claude SDK 本质是个 HTTP 客户端。你调用 `messages.create()`，传入 tools 定义，拿回 `tool_use` block，自己执行，再把结果塞回去。循环要自己写。

### Pi Mono
```
你得到的：统一 LLM API + Agent Runtime + 工具系统 + TUI/Web UI
你要自建的：QCut 专属工具适配、嵌入到 Electron 的 UI
```

Pi Mono 的 `@anthropic-ai/sdk` 等价物是 `pi-llm`（统一 API），但它还给你 `pi-agent`（Agent 循环）、`pi-tools`（工具注册），甚至 `pi-tui` 和 `pi-web`。

### 结论
**Pi Mono 给的更多，QCut 自建量更少。** 但"更多"也意味着更多依赖和更多需要理解的抽象。

## 2. 模型灵活性

这是最大分歧。

- **Claude SDK**：锁死 Claude。Opus 贵（$15/M input），Haiku 便宜但能力有限。用户没得选。
- **Pi Mono**：同一套代码跑 Claude / GPT / Gemini / 本地模型。用户可以按需切换。

**对 QCut 的意义：** 视频编辑 Agent 需要强推理能力（理解用户意图 → 拆解成 CLI 命令序列），但也需要成本可控。多供应商支持让你可以：用便宜模型处理简单任务（"加个字幕"），用强模型处理复杂任务（"把这段剪成节奏感更强的版本"）。

## 3. Agent 循环实现难度

**Claude SDK 方案：**
```typescript
// 你得自己写这个循环
while (true) {
  const response = await client.messages.create({ tools, messages });
  if (response.stop_reason === 'end_turn') break;
  for (const block of response.content) {
    if (block.type === 'tool_use') {
      const result = await executeTool(block.name, block.input);
      messages.push({ role: 'assistant', content: [block] });
      messages.push({ role: 'user', content: [{ type: 'tool_result', tool_use_id: block.id, content: result }] });
    }
  }
}
```
看起来简单，但实际要处理：并行工具调用、错误恢复、上下文窗口截断、token 计费、流式输出等。大约 500-1000 行生产级代码。

**Pi Mono 方案：**
```typescript
const agent = createAgent({ model: 'claude-sonnet-4-20250514', tools: qcutTools });
const result = await agent.run('把第二个片段的音量降低 50%');
```
循环、重试、上下文管理都内置了。你专注写 QCut 工具定义就行。

## 4. 维护风险

这是 Pi Mono 的最大软肋。

| 风险 | Claude SDK | Pi Mono |
|------|-----------|---------|
| 维护人数 | Anthropic 团队（数十人） | Mario Zechner（1 人） |
| 公司支持 | Anthropic（估值 $600B+） | 无 |
| 弃坑风险 | 极低 | 中高 |
| API 变更响应 | 即时 | 取决于 Mario 的时间 |
| 安全补丁 | 有保障 | 不确定 |

**23.6K Stars 不等于稳定。** 个人项目火了之后弃坑的案例太多。QCut 是商业产品，要慎重考虑这个风险。

## 5. 与 QCut CLI 的集成

QCut 已有 87+ CLI 命令，JSON 输出。两种方案集成方式相同：

```typescript
// 两种方案都是这样注册工具
const tools = [
  {
    name: 'qcut_add_subtitle',
    description: '在指定时间点添加字幕',
    parameters: { text: 'string', startTime: 'number', duration: 'number' },
    execute: async (params) => {
      return await exec(`qcut subtitle add --text "${params.text}" --start ${params.startTime} --duration ${params.duration} --json`);
    }
  }
];
```

**集成难度基本相同。** 差异在上层（Agent 循环），不在工具层。

## 6. 成本

两种方案的 API 费用完全透传，取决于你用哪个模型：

| 模型 | Input $/M tokens | Output $/M tokens |
|------|------------------|-------------------|
| Claude Opus 4 | $15 | $75 |
| Claude Sonnet 4 | $3 | $15 |
| Claude Haiku 3.5 | $0.80 | $4 |
| GPT-4.1 | $2 | $8 |
| Gemini 2.5 Pro | $1.25 | $10 |
| Gemini 2.5 Flash | $0.15 | $0.60 |

**多供应商 = 成本优化空间更大。** 简单任务用 Flash/Haiku，复杂任务用 Sonnet/4.1。

## 7. 还有什么选择？

| 方案 | 优势 | 劣势 |
|------|------|------|
| **OpenRouter API** | 统一 API，50+ 模型 | 只是 API 转发，Agent 循环要自己写 |
| **Vercel AI SDK (`ai`)** | 成熟、多供应商、流式支持好 | 偏 Web 场景，Agent 循环支持一般 |
| **自己写** | 完全可控 | 工作量大，重复造轮子 |

**Vercel AI SDK** 值得认真考虑——比 Claude SDK 多供应商，比 Pi Mono 更稳定（Vercel 团队维护），而且 Next.js 生态对 Electron app 友好。

## 推荐

**对 QCut 的具体情况，推荐分两步走：**

### 短期（MVP）：Anthropic Claude SDK + 自建轻量 Agent 循环
- QCut 已有 19 个 Claude Code Skills，团队对 Claude 生态熟悉
- Agent 循环代码量可控（~500 行），且完全可控
- 先用 Sonnet 4 验证产品体验，不需要多模型

### 中期（产品化）：迁移到 Vercel AI SDK
- 当需要多模型支持、成本优化时，换到 `ai` 包
- API 层替换成本低（工具定义不变）
- Vercel 团队维护，稳定性有保障

### 不推荐 Pi Mono
- 尽管功能最全，但单人维护风险太高
- QCut 是商业产品，不能赌一个人的热情

---

*实际选型永远是 tradeoff。先跑起来再优化，比选"最佳方案"然后半年不动更重要。* 🦞
