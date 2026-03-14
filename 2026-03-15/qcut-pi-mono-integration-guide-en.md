# How to Build an Embedded AI Agent in QCut Using Pi Mono: Complete Implementation Guide

> Turn an 87+ CLI command video editor into a natural-language-driven AI workbench — no Claude Code installation required.

## Architecture Overview

```
User types "Cut this video to 15 seconds"
         │
         ▼
┌─────────────────────────┐
│   QCut Editor (Electron) │
│  ┌───────────────────┐  │
│  │  Chat Panel       │  │
│  │  (pi-web-ui)      │  │
│  └────────┬──────────┘  │
│           │              │
│  ┌────────▼──────────┐  │
│  │  pi-agent-core    │  │
│  │  Agent Runtime    │  │
│  │  - Tool registry  │  │
│  │  - State mgmt     │  │
│  │  - transformContext│  │
│  └────────┬──────────┘  │
│           │              │
│  ┌────────▼──────────┐  │
│  │  pi-ai            │  │
│  │  Unified LLM API  │  │
│  │  Claude/GPT/Gemini│  │
│  └────────┬──────────┘  │
│           │              │
│           ▼              │
│     LLM returns tool call│
│           │              │
│  ┌────────▼──────────┐  │
│  │  QCut CLI Bridge  │  │
│  │  qcut-pipeline    │  │
│  │  87+ commands     │  │
│  └────────┬──────────┘  │
│           │              │
│           ▼              │
│   Result → Chat UI      │
└─────────────────────────┘
```

The agent runs in Electron's main process, calling `qcut-pipeline` CLI via `child_process.exec`. Users type natural language in the editor's chat panel, Pi Mono handles LLM interaction and tool calling, and the CLI returns JSON results.

## Step 1: Install Pi Mono Packages

```bash
cd qcut/
npm install @mariozechner/pi-ai @mariozechner/pi-agent-core @mariozechner/pi-web-ui
```

| Package | Purpose | Role |
|---------|---------|------|
| `pi-ai` | Unified LLM API across OpenAI/Anthropic/Google | LLM layer |
| `pi-agent-core` | Agent runtime: tool calling, state, events, context compression | Core |
| `pi-web-ui` | React chat components for embedding in Electron | UI |

**Context:** Pi Mono is a monorepo ([github.com/badlogic/pi-mono](https://github.com/badlogic/pi-mono)) with 23.6k stars and 171 releases, maintained by Mario Zechner (creator of libGDX). OpenClaw already uses these packages in production.

## Step 2: Progressive Command Loading Design

QCut has 87+ CLI commands. Dumping all of them into the system prompt is **wrong** — it wastes tokens and degrades response quality.

The right approach: leverage QCut's existing 3-layer help system for progressive discovery.

### L0: System Prompt — Category Overview Only (~200 tokens)

```typescript
const SYSTEM_PROMPT = `You are a QCut video editing assistant. QCut is controlled via CLI commands.

Available command categories:
- timeline: Timeline operations (cut, split, move, delete clips)
- media: Media import and management
- transcribe: AI transcription and subtitles
- export: Export and rendering
- effects: Effects and transitions
- audio: Audio processing
- ai: AI-assisted features (smart cuts, content analysis)
- project: Project management

Use the qcut_help tool to list commands in a category.
Use the qcut_command_help tool to get detailed parameters for a specific command.
Always discover available commands before executing operations.`;
```

### L1: `qcut_help` Tool — Lists Commands per Category

```typescript
const qcutHelpTool = {
  name: 'qcut_help',
  description: 'List QCut commands. Pass a category name to get all commands in that category.',
  parameters: {
    type: 'object',
    properties: {
      category: {
        type: 'string',
        description: 'Command category: timeline, media, transcribe, export, etc.'
      }
    },
    required: ['category']
  },
  execute: async (params: { category: string }) => {
    const result = await execCli(`qcut-pipeline ${params.category} --help --json`);
    return JSON.parse(result);
    // Returns: { commands: ["split", "trim", "delete", "move", ...], descriptions: {...} }
  }
};
```

### L2: `qcut_command_help` Tool — Full Parameter Details

```typescript
const qcutCommandHelpTool = {
  name: 'qcut_command_help',
  description: 'Get full parameters and usage for a specific QCut command.',
  parameters: {
    type: 'object',
    properties: {
      command: {
        type: 'string',
        description: 'Full command name, e.g. timeline:split, media:import'
      }
    },
    required: ['command']
  },
  execute: async (params: { command: string }) => {
    const result = await execCli(
      `qcut-pipeline ${params.command} --help --json`
    );
    return JSON.parse(result);
    // Returns: { name, description, parameters: [{name, type, required, default, description}...] }
  }
};
```

**Result:** When the agent first needs to edit video, it calls L1 to discover timeline commands, then L2 to get `timeline:split` parameters. In subsequent turns, the LLM has already "learned" these commands — no repeat queries needed.

## Step 3: Register QCut CLI Commands as Tools

Core pattern: each CLI command maps to an agent tool.

### CLI Bridge Function

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

### Representative Tool Implementations

```typescript
// Timeline split
const timelineSplitTool = {
  name: 'timeline_split',
  description: 'Split a clip on the timeline at a specified time point',
  parameters: {
    type: 'object',
    properties: {
      track: { type: 'number', description: 'Track index' },
      time: { type: 'string', description: 'Split time point, e.g. "00:01:30.500"' },
      clip_id: { type: 'string', description: 'Clip ID to split (optional)' }
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

// Media import
const mediaImportTool = {
  name: 'media_import',
  description: 'Import a media file into the project',
  parameters: {
    type: 'object',
    properties: {
      path: { type: 'string', description: 'File path' },
      track: { type: 'number', description: 'Target track' },
      position: { type: 'string', description: 'Insert position timecode' }
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

// AI Transcription
const transcribeTool = {
  name: 'transcribe',
  description: 'Run AI transcription on video/audio to generate subtitles',
  parameters: {
    type: 'object',
    properties: {
      source: { type: 'string', description: 'Source file path or clip ID' },
      language: { type: 'string', description: 'Language code: zh, en, etc.' },
      model: { type: 'string', description: 'Transcription model: whisper-large-v3' }
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

// Export
const exportStartTool = {
  name: 'export_start',
  description: 'Start exporting/rendering the project',
  parameters: {
    type: 'object',
    properties: {
      output: { type: 'string', description: 'Output file path' },
      format: { type: 'string', description: 'Format: mp4, mov, webm' },
      resolution: { type: 'string', description: 'Resolution: 1080p, 4k' },
      quality: { type: 'string', description: 'Quality: draft, normal, high' }
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

### Auto-Generating Tool Registrations

With 87+ commands, writing each tool by hand is impractical. Use `--help --json` output to auto-generate:

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

**Recommendation:** For MVP, register only the 15-20 most-used commands as direct tools. Let the agent discover the rest via the L1/L2 help system on demand.

## Step 4: Agent Initialization with pi-agent-core

```typescript
import { Agent, type AgentConfig } from '@mariozechner/pi-agent-core';
import { createProvider } from '@mariozechner/pi-ai';

// Create LLM provider
const provider = createProvider({
  type: 'anthropic',  // or 'openai', 'google'
  apiKey: userSettings.apiKey,
  model: 'claude-sonnet-4-20250514'
});

// Agent configuration
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
    // ... other common tools
  ],

  // Context compression — critical for long sessions
  transformContext: (messages) => {
    return compressEditingContext(messages);
  },

  // Event handling
  onToolCall: (toolName, params) => {
    chatPanel.showToolExecution(toolName, params);
  },

  onToolResult: (toolName, result) => {
    editor.refreshTimeline();
    chatPanel.showToolResult(toolName, result);
  }
};

// Create agent instance
const agent = new Agent(agentConfig);

// Handle user messages
async function handleUserMessage(text: string) {
  const response = await agent.chat(text);
  chatPanel.appendMessage('assistant', response);
}
```

## Step 5: Embed Chat UI in QCut Editor

QCut already has an AI panel UI framework. Embed using `pi-web-ui` or a custom React component:

### Option A: Using pi-web-ui Components

```tsx
import { ChatPanel } from '@mariozechner/pi-web-ui';

function QCutAIPanel() {
  const agent = useQCutAgent();

  return (
    <div className="qcut-ai-panel">
      <ChatPanel
        agent={agent}
        placeholder="Describe the edit you want..."
        theme="dark"
        onToolExecution={(tool, params) => {
          editor.highlightAffectedRegion(tool, params);
        }}
      />
    </div>
  );
}
```

### Option B: Custom Component (More Flexible)

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
        toolCalls: response.toolCalls
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

## Step 6: Context Management (transformContext)

Video editing sessions run long — users may perform dozens of operations in a row. Without context compression, token costs explode.

```typescript
function compressEditingContext(messages: Message[]): Message[] {
  const MAX_MESSAGES = 30;

  if (messages.length <= MAX_MESSAGES) return messages;

  const systemMsg = messages[0];
  const recentMessages = messages.slice(-MAX_MESSAGES);

  // Compress old tool results to summaries
  const compressed = recentMessages.map(msg => {
    if (msg.role === 'tool' && msg.content.length > 500) {
      const parsed = JSON.parse(msg.content);
      return {
        ...msg,
        content: JSON.stringify({
          status: parsed.status,
          summary: parsed.summary || 'Operation completed',
        })
      };
    }
    return msg;
  });

  // Insert current project state at compression boundary
  const projectState = getCurrentProjectState();
  const stateSummary: Message = {
    role: 'system',
    content: `[Context compressed] Current project state:
- Timeline duration: ${projectState.duration}
- Track count: ${projectState.trackCount}
- Clip count: ${projectState.clipCount}
- Recent operations: ${projectState.recentOps.join(', ')}
Previous conversation has been compressed.`
  };

  return [systemMsg, stateSummary, ...compressed];
}

function getCurrentProjectState() {
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

**Key point:** `transformContext` is a built-in feature of `pi-agent-core`. It runs automatically before each LLM call — transparent to the user.

## Step 7: Multi-Model Support

The biggest advantage of `pi-ai`: unified API, user chooses the model.

```typescript
import { createProvider, type ProviderType } from '@mariozechner/pi-ai';

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

// Settings UI
function AISettingsPanel() {
  const models = {
    anthropic: ['claude-sonnet-4-20250514', 'claude-haiku-4-20250414'],
    openai: ['gpt-4o', 'gpt-4o-mini'],
    google: ['gemini-2.5-pro', 'gemini-2.5-flash']
  };

  return (
    <div className="ai-settings">
      <h3>AI Model Settings</h3>
      <Select label="Provider" options={Object.keys(models)} />
      <Select label="Model" options={models[selectedProvider]} />
      <Input label="API Key" type="password" />
      <p className="hint">
        Different models excel at different tasks.
        Claude handles complex editing intent well, GPT-4o is fast, Gemini supports ultra-long context.
      </p>
    </div>
  );
}
```

## Timeline Estimate

| Phase | Scope | Duration |
|-------|-------|----------|
| Week 1, first half | Install Pi Mono, build Agent + CLI bridge | 2-3 days |
| Week 1, second half | Register 15-20 core tools, implement L0-L2 help system | 2-3 days |
| Week 2, first half | Embed chat UI, implement transformContext | 2-3 days |
| Week 2, second half | Multi-model settings panel, testing & bug fixes | 2-3 days |

**MVP goal:** User types "split the video at 1 minute" in QCut's chat panel → Agent calls `timeline:split --time 00:01:00` → result displayed.

## Risk Mitigation

### Risk 1: Pi Mono is Single-Maintainer

Pi Mono is maintained solely by Mario Zechner. While he's an experienced developer (creator of libGDX), single-maintainer projects carry bus factor risk.

**Mitigation:**
- Pi Mono's core APIs (`pi-ai`, `pi-agent-core`) are lean — small codebase
- If maintenance stalls, fork and continue
- More aggressive fallback: abstract an interface layer, swap to Vercel AI SDK or direct LLM APIs

```typescript
// Abstract interface — swappable implementation
interface QCutAIProvider {
  chat(messages: Message[], tools: Tool[]): Promise<Response>;
}

class PiMonoProvider implements QCutAIProvider {
  private agent: Agent;
  async chat(messages, tools) { /* pi-agent-core */ }
}

class DirectAPIProvider implements QCutAIProvider {
  async chat(messages, tools) { /* direct Anthropic/OpenAI SDK */ }
}
```

### Risk 2: CLI Command Error Handling

LLMs may generate invalid parameters.

```typescript
function wrapToolExecute(execute: Function) {
  return async (params: any) => {
    try {
      return await execute(params);
    } catch (error: any) {
      return {
        status: 'error',
        message: error.message,
        hint: 'Check parameters. Use qcut_command_help to see parameter details.'
      };
    }
  };
}
```

### Risk 3: Long Session Token Costs

`transformContext` handles most of this. Additional measures:

- Set per-conversation token limits
- Show token usage stats in settings
- "New conversation" button to reset context

---

## Summary

The core ideas for embedding an AI agent in QCut with Pi Mono:

1. **Don't make users install CLI tools** — the agent lives inside the editor
2. **Don't stuff the system prompt** — use 3-layer progressive loading
3. **Use `pi-agent-core` to manage complexity** — tool registration, state management, context compression are built-in
4. **Let users choose their model** — `pi-ai` unified API, one line to switch

This isn't hypothetical. OpenClaw already runs agents with Pi Mono in production. QCut has a complete CLI command system (87+ commands, all supporting `--help --json`). The combination is natural.

1-2 weeks to MVP. Users edit video with natural language inside QCut.

🦞
