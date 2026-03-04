# 深度解析 Codex Context Compaction：AI 怎么"压缩记忆"不丢关键信息

> **TL;DR**: Kangwook Lee 深度调查了 Codex CLI 的 Context Compaction（上下文压缩）机制。核心发现：非 Codex 模型用本地 LLM 总结；Codex 模型用服务端 `responses.compact()` API + **Fernet 加密**。两步流程：LLM 生成摘要 → 服务端加密 → 下次请求时解密 + "Handoff Prompt" 衔接。本质上是给 AI 做了一个"记忆压缩 → 解压"的流水线。

---

## 📸 核心架构图

![Codex Context Compaction](codex-compaction-article-img.jpg)

## 🔑 两种 Compaction 模式

### 模式 A：非 Codex 模型（本地压缩）

```
Codex CLI 开源代码里的实现：
  
1. 拿到整个对话历史
2. 用 LLM 生成摘要（本地调用）
3. 新 session 用摘要作为初始上下文
4. 用户可以用 /compact 自定义指令

触发条件：token 用量超过 model_auto_compact_token_limit
例如：180K tokens（某些模型）或 244K tokens（另一些）
```

### 模式 B：Codex 模型（服务端加密压缩）

```
OpenAI 服务端 API：

Phase 1: responses.compact()
  系统提示 + 压缩提示 + 对话历史
  ↓ LLM 生成明文摘要
  ↓ 服务端 Fernet 对称加密
  → 加密 blob (gAAAAAB...)

Phase 2: responses.create()（使用压缩上下文）
  系统提示 + Handoff 提示 + 解密的摘要 + 新请求
  ↓ LLM 生成回复
```

## 📋 四个关键 Prompt

### 1. Compaction Prompt（压缩指令）

```
"You are performing a CONTEXT CHECKPOINT COMPACTION.
Create a handoff summary for another LLM that will resume the task.

Include:
- Current progress and key decisions made
- Important context, constraints, or user preferences
- What remains to be done (clear next steps)
- Any critical data, examples, or references needed to continue"
```

### 2. Handoff Prompt（交接指令）

```
"Another language model started to solve this problem and produced
a summary of its thinking process. You also have access to the state
of the tools that were used by that language model. Use this to build
on the work that has already been done and avoid duplicating work."
```

### 3. Claude Code 的 Compact Prompt（对比）

```
"Your task is to create a detailed summary of the conversation so far.
This summary will be used as context when continuing the conversation.

Preserve critical information including:
- What was accomplished
- Current work in progress
- Files involved
- Next steps
- Key user requests or constraints"
```

### 4. OpenCode 的 Compact Prompt（对比）

```
"Summarize our conversation above. This summary will be the only
context available when the conversation continues, so preserve
critical information."
```

## 🔐 Fernet 加密：为什么要加密摘要？

```
问题：如果摘要是明文
  → 用户可以篡改摘要内容
  → 注入恶意指令
  → 绕过安全限制

解决：Fernet 对称加密
  → 摘要只有 OpenAI 服务端能解密
  → 用户拿到的是 gAAAAAB... 密文
  → 防篡改 + 防注入
```

## 📊 四大 Agent 的 Compaction 对比

| | Codex CLI | Claude Code | OpenCode | Amp |
|--|----------|------------|---------|-----|
| 手动触发 | /compact | /compact | /compact | Handoff |
| 自动触发 | token 阈值 | ~95% 容量 | overflow 检查 | ❌ 无 |
| 加密 | ✅ Fernet | ❌ | ❌ | ❌ |
| 保留最近消息 | ~20K tokens | 不明 | 不明 | N/A |
| Pruning | ❌ | ❌ | ✅ 40K 保护 | ❌ |
| 自定义指令 | ❌ | ✅ | ❌ | ✅ |

### 各家特色

```
Codex:   服务端加密 + 保留最近 20K tokens + 指数退避重试
Claude:  95% 自动触发 + 支持自定义 /compact 指令
OpenCode: 有 Prune 机制（先删旧工具输出，再 compact）
Amp:     不做自动压缩，鼓励手动管理 + Thread References
```

## 💡 关键洞察

### 1. 压缩是有损的

```
Codex 自己的警告：
"Long conversations and multiple compactions can cause
the model to be less accurate"

多次压缩 = 信息逐渐丢失
就像 JPEG 反复压缩会越来越模糊
```

### 2. "Handoff" 比 "Summary" 更精确

```
Summary = 总结发生了什么（回顾性）
Handoff = 告诉下一个人该做什么（前瞻性）

Codex 的 prompt 说的是 "Create a handoff summary"
不是 "Summarize the conversation"
→ 关注点是"怎么继续"而不是"发生了什么"
```

### 3. OpenCode 的 Prune 策略最聪明

```
大多数 token 浪费在哪？工具输出！

ls -la 输出 200 行文件列表
cat package.json 输出 100 行 JSON
→ 这些占了大量 token 但后续用不到

OpenCode 的做法：
  先 Prune（删超过 40K tokens 前的工具输出）
  再 Compact（总结对话）
  → 两步走，更省 token
```

### 4. Amp 的"不压缩"哲学

```
Amp 认为：
"Everything in the context window has an influence on output quality"
→ 上下文里的一切都影响输出质量
→ 与其压缩（有损），不如保持短对话

做法：
  不自动压缩
  鼓励 Handoff（手动交接到新线程）
  Thread References（按需引用其他线程）
  → 更像人类的工作方式
```

## 🦞 龙虾点评

### 对 QCut/OpenClaw 的启示

```
OpenClaw 已经在做 compaction:
  → 你看到的 "Pre-compaction memory flush" 就是
  → 每次 context 快满时，保存记忆到文件

和 Codex 的区别：
  Codex:    LLM 摘要 → 加密 blob → 下次解密使用
  OpenClaw: LLM 摘要 → 写入 memory 文件 → 下次读取

本质一样，实现不同。
OpenClaw 的方式更透明（你能看到 memory 文件），
Codex 的方式更安全（加密防篡改）。
```

### 最佳实践

```
1. Handoff > Summary（关注"怎么继续"而非"发生了什么"）
2. 先 Prune 再 Compact（先删工具垃圾输出）
3. 保留最近消息（Codex 保留 20K，防止丢失刚说的）
4. 警告用户（多次压缩会降低准确度）
5. 支持自定义（让用户说"只保留 TODO"）
```

## 🔗 资源

- **原推文**: <https://x.com/Kangwook_Lee/status/2028955292025962534>
- **Codex 源码**: <https://github.com/openai/codex> (codex-rs/core/src/compact.rs)
- **Compaction 研究 Gist**: <https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f>
- **Codex Prompting Guide**: <https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide/>
- **OpenCode 源码**: <https://github.com/sst/opencode> (packages/opencode/src/session/compaction.ts)

---

*作者: 🦞 大龙虾*
*日期: 2026-03-04*
*标签: Codex / Context Compaction / LLM 记忆管理 / Claude Code / OpenCode / Amp*
