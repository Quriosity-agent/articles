# 如何用 Pi Mono 在 QCut 中构建嵌入式 AI Agent：完整实现指南

> 把 87+ CLI 命令的视频编辑器变成自然语言驱动的 AI 工作台，不需要用户安装 Claude Code。

## 架构总览

```
用户输入 "把这段视频剪成15秒"
         │
         ▼
┌─────────────────────────┐
│   QCut 编辑器 (Electron) │
│  ┌───────────────────┐  │
│  │  Chat Panel       │  │
│  │  (pi-web-ui)      │  │
│  └────────┬──────────┘  │
│           │              │
│  ┌────────▼──────────┐  │
│  │  pi-agent-core    │  │
│  │  Agent Runtime    │  │
│  │  - 工具注册        │  │
│  │  - 状态管理        │  │
│  │  - transformContext│  │
│  └────────┬──────────┘  │
│           │              │
│  ┌────────▼──────────┐  │
│  │  pi-ai            │  │
│  │  统一 LLM API     │  │
│  │  Claude/GPT/Gemini│  │
│  └────────┬──────────┘  │
│           │              │
│           ▼              │
│     LLM 返回 tool call  │
│           │              │
│  ┌────────▼──────────┐  │
│  │  QCut CLI Bridge  │  │
│  │  qcut-pipeline    │  │
│  │  87+ 命令         │  │
│  └────────┬──────────┘  │
│           │              │
│           ▼              │
│     执行结果 → Chat UI   │
└─────────────────────────┘
```

关键设计：Agent 运行在 Electron 主进程中，通过 `child_process.exec` 调用 `qcut-pipeline` CLI。用户在编辑器内的聊天面板输入自然语言，Pi Mono 处理 LLM 交互和工具调用，CLI 返回 JSON 结果。

## Step 1: 安装 Pi Mono 包

```bash
cd qcut/
npm install @mariozechner/pi-ai @mariozechner/pi-agent-core @mariozechner/pi-web-ui
```

三个包各司其职：

| 包 | 作用 | 大小 |
|---|---|---|
| `pi-ai` | 统一 LLM API，支持 OpenAI/Anthropic/Google | ~轻量 |
| `pi-agent-core` | Agent 运行时：工具调用、状态管理、事件、上下文压缩 | ~核心 |
| `pi-web-ui` | React 聊天组件，可直接嵌入 Electron | ~UI |

**注意：** Pi Mono 是 monorepo 结构（[github.com/badlogic/pi-mono](https://github.com/badlogic/pi-mono)），23.6k stars，171 个 release，由 Mario Zechner（libGDX 作者）维护。OpenClaw 已在生产环境中使用这些包。

## Step 2: 渐进式命令加载设计

QCut 有 87+ CLI 命令。把所有命令塞进 system prompt 是**错误做法**——会浪费 token、降低响应质量。

正确做法：利用 QCut 现有的 3 层帮助系统，设计渐进式加载：

### L0: System Prompt — 只放类别概览（~200 tokens）

```typescript
const SYSTEM_PROMPT = `你是 QCut 视频编辑助手。QCut 通过 CLI 命令控制编辑器。

可用命令类别：
- timeline: 时间线操作（剪切、分割、移动、删除片段）
- media: 媒体导入和管理
- transcribe: AI 转录和字幕
- export: 导出和渲染
- effects: 特效和转场
- audio: 音频处理
- ai: AI 辅助功能（智能剪辑、内容分析）
- project: 项目管理

使用 qcut_help 工具获取具体类别下的命令列表。
使用 qcut_command_help 工具获取具体命令的参数详情。
先了解可用命令，再执行操作。`;
```

### L1: `qcut_help` 工具 — 返回类别下的命令列表

```typescript
const qcutHelpTool = {
  name: 'qcut_help',
  description: '获取 QCut 命令列表。传入类别名获取该类别下所有命令。',
  parameters: {
    type: 'object',
    properties: {
      category: {
        type: 'string',
        description: '命令类别，如 timeline, media, transcribe, export'
      }
    },
    required: ['category']
  },
  execute: async (params: { category: string }) => {
    const result = await execCli(`qcut-pipeline ${params.category} --help --json`);
    return JSON.parse(result);
    // 返回类似: { commands: ["split", "trim", "delete", "move", ...], descriptions: {...} }
  }
};
```

### L2: `qcut_command_help` 工具 — 返回具体命令的完整参数

```typescript
const qcutCommandHelpTool = {
  name: 'qcut_command_help',
  description: '获取 QCut 具体命令的完整参数和用法。',
  parameters: {
    type: 'object',
    properties: {
      command: {
        type: 'string',
        description: '完整命令名，如 timeline:split, media:import'
      }
    },
    required: ['command']
  },
  execute: async (params: { command: string }) => {
    const result = await execCli(
      `qcut-pipeline ${params.command} --help --json`
    );
    return JSON.parse(result);
    // 返回: { name, description, parameters: [{name, type, required, default, description}...] }
  }
};
```

**效果：** Agent 第一次需要剪辑视频时，先调 L1 拿到 timeline 类别的命令列表，再调 L2 拿到 `timeline:split` 的具体参数。后续对话中 LLM 已经"学会"了这些命令，不需要重复查询。

## Step 3: 注册 QCut CLI 命令为工具

核心模式：每个 CLI 命令对应一个 Agent 工具。

### CLI 桥接函数

```typescript
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function execCli(command: string): Promise<string> {
  const { stdout, stderr } = await execAsync(
    `qcut-pipeline ${command} --json`,
    {
      cwd: projectDir,
      timeout: 60000,
      env: { ...process.env, QCUT_SESSION: sessionId }
    }
  );
  if (stderr) console.warn('[QCut CLI stderr]', stderr);
  return stdout;
}
```

### 代表性工具实现

```typescript
// 时间线分割
const timelineSplitTool = {
  name: 'timeline_split',
  description: '在指定时间点分割时间线上的片段',
  parameters: {
    type: 'object',
    properties: {
      track: { type: 'number', description: '轨道索引' },
      time: { type: 'string', description: '分割时间点，如 "00:01:30.500"' },
      clip_id: { type: 'string', description: '要分割的片段 ID（可选）' }
    },
    required: ['time']
  },
  execute: async (params: { track?: number; time: string; clip_id?: string }) => {
    const args = [`--time "${params.time}"`];
    if (params.track !== undefined) args.push(`--track ${params.track}`);
    if (params.clip_id) args.push(`--clip-id "${params.clip_id}"`);
    return JSON.parse(await execCli(`timeline:split ${args.join(' ')}`));
  }
};

// 媒体导入
const mediaImportTool = {
  name: 'media_import',
  description: '导入媒体文件到项目',
  parameters: {
    type: 'object',
    properties: {
      path: { type: 'string', description: '文件路径' },
      track: { type: 'number', description: '目标轨道' },
      position: { type: 'string', description: '插入位置时间码' }
    },
    required: ['path']
  },
  execute: async (params) => {
    const args = [`--path "${params.path}"`];
    if (params.track !== undefined) args.push(`--track ${params.track}`);
    if (params.position) args.push(`--position "${params.position}"`);
    return JSON.parse(await execCli(`media:import ${args.join(' ')}`));
  }
};

// AI 转录
const transcribeTool = {
  name: 'transcribe',
  description: '对视频/音频进行 AI 转录，生成字幕',
  parameters: {
    type: 'object',
    properties: {
      source: { type: 'string', description: '源文件路径或片段 ID' },
      language: { type: 'string', description: '语言代码，如 zh, en' },
      model: { type: 'string', description: '转录模型，如 whisper-large-v3' }
    },
    required: ['source']
  },
  execute: async (params) => {
    const args = [`--source "${params.source}"`];
    if (params.language) args.push(`--language ${params.language}`);
    if (params.model) args.push(`--model ${params.model}`);
    return JSON.parse(await execCli(`transcribe ${args.join(' ')}`));
  }
};

// 导出
const exportStartTool = {
  name: 'export_start',
  description: '开始导出/渲染项目',
  parameters: {
    type: 'object',
    properties: {
      output: { type: 'string', description: '输出文件路径' },
      format: { type: 'string', description: '格式: mp4, mov, webm' },
      resolution: { type: 'string', description: '分辨率: 1080p, 4k' },
      quality: { type: 'string', description: '质量: draft, normal, high' }
    },
    required: ['output']
  },
  execute: async (params) => {
    const args = [`--output "${params.output}"`];
    if (params.format) args.push(`--format ${params.format}`);
    if (params.resolution) args.push(`--resolution ${params.resolution}`);
    if (params.quality) args.push(`--quality ${params.quality}`);
    return JSON.parse(await execCli(`export:start ${args.join(' ')}`));
  }
};
```

### 自动生成工具注册

对于 87+ 命令，手动写每个工具不现实。用命令的 `--help --json` 输出自动生成：

```typescript
async function autoRegisterTools(agent: Agent, categories: string[]) {
  for (const category of categories) {
    const helpJson = await execCli(`${category} --help --json`);
    const { commands } = JSON.parse(helpJson);

    for (const cmd of commands) {
      const cmdHelp = await execCli(`${category}:${cmd.name} --help --json`);
      const cmdInfo = JSON.parse(cmdHelp);

      agent.registerTool({
        name: `${category}_${cmd.name}`,
        description: cmdInfo.description,
        parameters: buildParameterSchema(cmdInfo.parameters),
        execute: async (params) => {
          const args = buildCliArgs(params, cmdInfo.parameters);
          return JSON.parse(await execCli(`${category}:${cmd.name} ${args}`));
        }
      });
    }
  }
}
```

**建议：** MVP 阶段只注册最常用的 15-20 个命令作为直接工具，其余通过 L1/L2 帮助系统让 Agent 按需发现。

## Step 4: Agent 初始化（pi-agent-core）

```typescript
import { Agent, type AgentConfig } from '@mariozechner/pi-agent-core';
import { createProvider } from '@mariozechner/pi-ai';

// 创建 LLM provider
const provider = createProvider({
  type: 'anthropic',  // 或 'openai', 'google'
  apiKey: userSettings.apiKey,
  model: 'claude-sonnet-4-20250514'
});

// Agent 配置
const agentConfig: AgentConfig = {
  provider,
  systemPrompt: SYSTEM_PROMPT,

  tools: [
    qcutHelpTool,
    qcutCommandHelpTool,
    timelineSplitTool,
    mediaImportTool,
    transcribeTool,
    exportStartTool,
    // ... 其他常用工具
  ],

  // 上下文压缩 — 长会话的关键
  transformContext: (messages) => {
    return compressEditingContext(messages);
  },

  // 事件处理
  onToolCall: (toolName, params) => {
    // 在 UI 中显示正在执行的操作
    chatPanel.showToolExecution(toolName, params);
  },

  onToolResult: (toolName, result) => {
    // 更新编辑器状态（如时间线刷新）
    editor.refreshTimeline();
    chatPanel.showToolResult(toolName, result);
  }
};

// 创建 Agent 实例
const agent = new Agent(agentConfig);

// 处理用户消息
async function handleUserMessage(text: string) {
  const response = await agent.chat(text);
  chatPanel.appendMessage('assistant', response);
}
```

## Step 5: 在 QCut 编辑器中嵌入聊天 UI

QCut 已有 AI 面板的 UI 框架。用 `pi-web-ui` 或自定义 React 组件嵌入：

### 方案 A: 使用 pi-web-ui 组件

```tsx
import { ChatPanel } from '@mariozechner/pi-web-ui';

function QCutAIPanel() {
  const agent = useQCutAgent(); // 上面创建的 agent 实例

  return (
    <div className="qcut-ai-panel">
      <ChatPanel
        agent={agent}
        placeholder="描述你想要的编辑操作..."
        theme="dark"
        onToolExecution={(tool, params) => {
          // 高亮编辑器中受影响的区域
          editor.highlightAffectedRegion(tool, params);
        }}
      />
    </div>
  );
}
```

### 方案 B: 自定义组件（更灵活）

```tsx
function QCutChatPanel() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const agent = useQCutAgent();

  const handleSend = async (text: string) => {
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setIsProcessing(true);

    try {
      const response = await agent.chat(text);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.text,
        toolCalls: response.toolCalls // 显示执行了哪些操作
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="qcut-chat">
      <MessageList messages={messages} />
      {isProcessing && <ToolExecutionIndicator />}
      <ChatInput onSend={handleSend} disabled={isProcessing} />
    </div>
  );
}
```

在 QCut 的 Electron 窗口中，这个面板放在编辑器右侧或底部，和现有的 AI 面板位置一致。

## Step 6: 上下文管理（transformContext）

视频编辑会话通常很长——用户可能连续操作几十次。不做上下文压缩，token 成本会爆炸。

```typescript
function compressEditingContext(messages: Message[]): Message[] {
  const MAX_MESSAGES = 30;
  const MAX_TOOL_RESULTS = 10;

  if (messages.length <= MAX_MESSAGES) return messages;

  // 策略1: 保留 system prompt + 最近 N 条消息
  const systemMsg = messages[0]; // system prompt
  const recentMessages = messages.slice(-MAX_MESSAGES);

  // 策略2: 压缩旧的 tool result（只保留摘要）
  const compressed = recentMessages.map(msg => {
    if (msg.role === 'tool' && msg.content.length > 500) {
      const parsed = JSON.parse(msg.content);
      return {
        ...msg,
        content: JSON.stringify({
          status: parsed.status,
          summary: parsed.summary || `操作完成`,
          // 丢弃详细数据
        })
      };
    }
    return msg;
  });

  // 策略3: 在压缩点插入当前项目状态摘要
  const projectState = getCurrentProjectState();
  const stateSummary: Message = {
    role: 'system',
    content: `[上下文压缩] 当前项目状态：
- 时间线长度: ${projectState.duration}
- 轨道数: ${projectState.trackCount}
- 片段数: ${projectState.clipCount}
- 最近操作: ${projectState.recentOps.join(', ')}
之前的对话已被压缩。`
  };

  return [systemMsg, stateSummary, ...compressed];
}

function getCurrentProjectState() {
  // 通过 CLI 获取当前项目状态
  const state = JSON.parse(
    execSync('qcut-pipeline project:status --json').toString()
  );
  return {
    duration: state.duration,
    trackCount: state.tracks.length,
    clipCount: state.totalClips,
    recentOps: state.undoStack.slice(-5).map((op: any) => op.name)
  };
}
```

**关键点：** `transformContext` 是 `pi-agent-core` 的内置功能。每次 LLM 调用前自动执行，用户无感知。

## Step 7: 多模型支持

`pi-ai` 最大的优势：统一 API，用户自由选择模型。

```typescript
import { createProvider, type ProviderType } from '@mariozechner/pi-ai';

// 在 QCut 设置中让用户选择
interface AISettings {
  provider: ProviderType; // 'anthropic' | 'openai' | 'google'
  model: string;
  apiKey: string;
}

function createAgentWithUserSettings(settings: AISettings) {
  const provider = createProvider({
    type: settings.provider,
    apiKey: settings.apiKey,
    model: settings.model
  });

  return new Agent({
    provider,
    systemPrompt: SYSTEM_PROMPT,
    tools: qcutTools,
    transformContext: compressEditingContext
  });
}

// 设置 UI
function AISettingsPanel() {
  const models = {
    anthropic: ['claude-sonnet-4-20250514', 'claude-haiku-4-20250414'],
    openai: ['gpt-4o', 'gpt-4o-mini'],
    google: ['gemini-2.5-pro', 'gemini-2.5-flash']
  };

  return (
    <div className="ai-settings">
      <h3>AI 模型设置</h3>
      <Select label="Provider" options={Object.keys(models)} />
      <Select label="Model" options={models[selectedProvider]} />
      <Input label="API Key" type="password" />
      <p className="hint">
        不同模型在不同任务上各有优势。
        Claude 擅长理解复杂编辑意图，GPT-4o 响应快，Gemini 支持超长上下文。
      </p>
    </div>
  );
}
```

## 时间线估算

| 阶段 | 内容 | 时间 |
|------|------|------|
| Week 1 前半 | 安装 Pi Mono，搭建 Agent + CLI 桥接 | 2-3 天 |
| Week 1 后半 | 注册 15-20 个核心工具，实现 L0-L2 帮助系统 | 2-3 天 |
| Week 2 前半 | 嵌入聊天 UI，实现 transformContext | 2-3 天 |
| Week 2 后半 | 多模型设置面板，测试和修 bug | 2-3 天 |

**MVP 目标：** 用户在 QCut 聊天面板输入"把视频从1分钟处分割"，Agent 自动调用 `timeline:split --time 00:01:00` 并返回结果。

## 风险缓解

### 风险 1: Pi Mono 是单人维护

Pi Mono 由 Mario Zechner 一人维护。虽然他是 libGDX 的作者（经验丰富），但单人项目存在 bus factor 风险。

**缓解策略：**
- Pi Mono 的核心 API（`pi-ai`、`pi-agent-core`）设计精简，代码量不大
- 如果维护停滞，可以 fork 继续维护
- 更激进的备选：抽象出接口层，底层可换成 Vercel AI SDK 或直接调 LLM API

```typescript
// 抽象接口 — 未来可替换底层实现
interface QCutAIProvider {
  chat(messages: Message[], tools: Tool[]): Promise<Response>;
}

// 当前实现: Pi Mono
class PiMonoProvider implements QCutAIProvider {
  private agent: Agent;
  async chat(messages, tools) { /* pi-agent-core */ }
}

// 备选实现: 直接 API
class DirectAPIProvider implements QCutAIProvider {
  async chat(messages, tools) { /* 直接调 Anthropic/OpenAI SDK */ }
}
```

### 风险 2: CLI 命令的错误处理

LLM 可能生成无效参数。

```typescript
// 包装每个工具调用，统一错误处理
function wrapToolExecute(execute: Function) {
  return async (params: any) => {
    try {
      const result = await execute(params);
      return result;
    } catch (error: any) {
      // 返回友好错误，让 LLM 可以自我修正
      return {
        status: 'error',
        message: error.message,
        hint: '请检查参数是否正确，可以用 qcut_command_help 查看参数说明'
      };
    }
  };
}
```

### 风险 3: 长会话 token 成本

`transformContext` 已经解决了大部分问题。额外措施：

- 设置每次对话的 token 上限
- 在设置中显示 token 使用统计
- 支持"新对话"按钮重置上下文

---

## 总结

用 Pi Mono 在 QCut 中嵌入 AI Agent 的核心思路：

1. **不要让用户装 CLI 工具** — Agent 内嵌在编辑器中
2. **不要塞满 system prompt** — 用 3 层渐进式加载
3. **用 `pi-agent-core` 管理复杂性** — 工具注册、状态管理、上下文压缩都是现成的
4. **让用户选模型** — `pi-ai` 统一 API，一行代码切换

这不是假想方案。OpenClaw 已经用 Pi Mono 在生产环境中运行 Agent。QCut 有完整的 CLI 命令体系（87+ 命令，全部支持 `--help --json`）。两者的结合是自然的。

1-2 周 MVP，用户就能在 QCut 里用自然语言剪视频。

🦞
