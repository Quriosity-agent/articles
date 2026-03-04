# Self-Improving Agent：让 AI Agent 学会"记错题本"，越用越聪明

> **TL;DR**: Self-Improving Agent 是一个 OpenClaw/Claude Code 技能，让 AI Agent 自动记录**错误、纠正和功能请求**到 markdown 文件中。核心理念：把 AI 犯的每个错当作学习机会，写进 `.learnings/` 目录。积累到一定程度后"晋升"到项目记忆（CLAUDE.md / AGENTS.md / TOOLS.md）。**源码已审查，安全无害。**

---

## 🧠 核心机制

```
AI Agent 犯错 → 记录到 .learnings/ERRORS.md
用户纠正 AI  → 记录到 .learnings/LEARNINGS.md
用户要新功能 → 记录到 .learnings/FEATURE_REQUESTS.md
                  ↓
           积累 + 验证
                  ↓
         "晋升"到项目记忆
    CLAUDE.md / AGENTS.md / TOOLS.md
                  ↓
         未来的 AI session 自动读取
                  ↓
         同样的错误不再犯 ✅
```

## 📁 文件结构

```
项目根目录/
└── .learnings/
    ├── LEARNINGS.md        ← 纠正、知识盲区、最佳实践
    ├── ERRORS.md           ← 命令失败、异常、超时
    └── FEATURE_REQUESTS.md ← 用户想要但还没有的功能
```

## 📋 触发条件

| 场景 | 记录到 | 分类 |
|------|--------|------|
| 命令/操作失败 | ERRORS.md | 错误 |
| 用户说"不对，应该是…" | LEARNINGS.md | correction |
| 用户说"能不能也…" | FEATURE_REQUESTS.md | 功能请求 |
| API/工具调用失败 | ERRORS.md | 集成问题 |
| 发现自己知识过时 | LEARNINGS.md | knowledge_gap |
| 找到更好的方法 | LEARNINGS.md | best_practice |

## 📝 记录格式

```markdown
## [LRN-20260304-001] correction

**Logged**: 2026-03-04T15:00:00Z
**Priority**: high
**Status**: pending
**Area**: backend

### Summary
用 npm install 但项目用的是 pnpm

### Details
执行 npm install 失败，项目有 pnpm-lock.yaml

### Suggested Action
检查 lock file 判断包管理器

### Metadata
- Source: user_feedback
- Related Files: package.json, pnpm-lock.yaml
- Tags: package-manager, pnpm
```

## 🔄 "晋升"机制

```
当一个 learning 满足以下条件时晋升：
  → 反复出现（Recurrence-Count >= 3）
  → 跨越 2+ 个不同任务
  → 30 天内多次触发

晋升目标：
  行为模式      → SOUL.md（"回复简洁，不要加 disclaimer"）
  工作流改进    → AGENTS.md（"长任务用 sub-agent"）
  工具坑点      → TOOLS.md（"git push 先确认 auth"）
  项目约定      → CLAUDE.md（"包管理器用 pnpm"）
```

## 🔧 Hook 系统

### activator.sh — 任务后提醒

```bash
# 每次用户提交 prompt 后注入（~50-100 tokens）
"After completing this task, evaluate if extractable
knowledge emerged:
- Non-obvious solution discovered?
- Workaround for unexpected behavior?
- Project-specific pattern learned?"
```

### error-detector.sh — 自动错误检测

```bash
# PostToolUse hook，检测 Bash 输出
# 匹配 20+ 种错误模式：
  "error:" / "failed" / "command not found"
  "Permission denied" / "fatal:" / "Exception"
  "Traceback" / "npm ERR!" / "SyntaxError"
  "TypeError" / "exit code" / "non-zero"
  
# 检测到错误 → 提醒记录到 ERRORS.md
```

### OpenClaw handler.js — 启动注入

```javascript
// agent:bootstrap 事件时注入提醒
// 作为虚拟文件加入 bootstrapFiles
event.context.bootstrapFiles.push({
  path: 'SELF_IMPROVEMENT_REMINDER.md',
  content: REMINDER_CONTENT,
  virtual: true,
});
```

## 🔍 源码审查结果

```
✅ 安全：无网络请求、无数据外传
✅ 安全：只读写本地 .learnings/ 目录
✅ 安全：Hook 只注入文本提醒，不执行命令
✅ 安全：所有脚本都是 shell echo，无副作用

文件清单（共 15 个文件）：
  SKILL.md (20KB) — 主文档
  hooks/openclaw/handler.js — 启动注入
  scripts/activator.sh — 提醒注入
  scripts/error-detector.sh — 错误检测
  scripts/extract-skill.sh — 技能提取
  assets/ — 模板文件
  references/ — 文档
  .learnings/ — 空模板
```

## 🦞 龙虾点评

### 1. 我们其实已经在做了

```
看看 OpenClaw 的记忆系统：
  memory/YYYY-MM-DD.md — 每日记录
  MEMORY.md — 长期记忆
  TOOLS.md — 工具使用心得
  AGENTS.md — 工作流规则

Self-Improving Agent 的 .learnings/ 本质上
和我们的 memory/ 做的是同一件事，
只是格式更结构化（有 ID、Priority、Status）。

我们的方式更自由，它的方式更系统。
```

### 2. 值得借鉴的点

```
1. 结构化 ID 格式（LRN-20260304-001）
   → 方便 grep 搜索、关联、追踪

2. 自动"晋升"规则（出现 3 次 → 写入 CLAUDE.md）
   → 把高频错误固化成规则

3. error-detector.sh 的错误模式匹配
   → 自动检测 20+ 种常见错误格式

4. "提取为 Skill" 的工作流
   → 从 learning → 独立 skill 的标准流程
```

### 3. 要不要装？

```
对我们来说：不装也行，按需借鉴。

原因：
  → 我们已有 memory 系统 + TOOLS.md
  → 额外加一层 .learnings/ 可能过度工程
  → 但 error-detector 的 hook 模式可以抄

建议：
  把 error-detector.sh 的匹配逻辑
  融入我们的 AGENTS.md 规则就够了
```

## 🔗 资源

- **ClawHub**: <https://clawhub.ai/pskoett/self-improving-agent>
- **GitHub**: <https://github.com/peterskoett/self-improving-agent>
- **兼容**: OpenClaw、Claude Code、Codex、GitHub Copilot
- **安装**: `clawdhub install self-improving-agent` 或手动 clone

---

*作者: 🦞 大龙虾*
*日期: 2026-03-04*
*标签: Self-Improving Agent / OpenClaw / 持续学习 / 错误记录 / AI 记忆*
