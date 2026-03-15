# ArgusBot：让 Codex CLI 不再"干到一半就停"的 Python 监督插件

> **Repo:** [waltstephen/ArgusBot](https://github.com/waltstephen/ArgusBot)
> **语言:** Python · **协议:** MIT（推测）· **依赖:** Codex CLI

## 一句话总结

ArgusBot 是一个给 Codex CLI 套上"监工循环"的 Python 插件——主 Agent 干活，Reviewer 子 Agent 判断完没完，Planner 子 Agent 维护全局视图。循环只有在 Reviewer 说 `done` 且验收检查全过了才会停。

## 它解决什么问题？

用过 Codex CLI 的人都知道一个痛点：**Agent 干到一半就停了，然后问你"接下来干嘛？"**

这不是 Agent 不行，而是它没有一个"闭环判断"的机制。ArgusBot 的做法很直接：加一层监督循环。

```
┌──────────────────────────────────────┐
│            ArgusBot Loop             │
│                                      │
│  ┌─────────┐   ┌──────────┐         │
│  │  Main    │──▶│ Reviewer  │        │
│  │  Agent   │   │ Sub-Agent │        │
│  │(codex    │   │           │        │
│  │ exec)    │   │ done?     │        │
│  └─────────┘   │ continue? │        │
│       ▲        │ blocked?  │        │
│       │        └─────┬─────┘        │
│       │              │               │
│       └──────────────┘               │
│              ▲                       │
│   ┌──────────┴──────────┐           │
│   │   Planner Agent     │           │
│   │ (全局视图 + 下一步)   │           │
│   └─────────────────────┘           │
└──────────────────────────────────────┘
```

## 架构深挖

读完源码，ArgusBot 的核心设计分三层：

### 1. 三角色子 Agent 系统

| 角色 | 职责 | 输出 |
|------|------|------|
| **Main Agent** | 执行具体任务（调 `codex exec`） | 代码改动、终端输出 |
| **Reviewer** | 评判任务是否完成 | `done` / `continue` / `blocked` + 置信度 |
| **Planner** | 维护全局计划、工作流表、TODO board | plan_report.md、plan_todo.md |

从 `reviewer.py` 可以看到，Reviewer 的 prompt 设计很严谨：
- 只有目标**完全满足**、无 blocker、验收检查全过才能给 `done`
- 不确定就给 `continue`
- 只有**必须用户介入**才给 `blocked`
- 每轮必须产出 `round_summary_markdown`

Planner 有三个模式：
- `auto`：主动提出下一步目标
- `record`：只记录不提议
- `off`：关掉

### 2. 防停滞看门狗（Stall Watchdog）

这个设计很实用：
- **1 小时无输出** → 启动诊断子 Agent，分析是不是卡住了
- **3 小时无输出** → 强制重启，不商量

源码里还有对 `invalid_encrypted_content` 的处理——如果恢复 session 遇到加密问题，直接开新 session 而不是在 Reviewer 的 `continue` 循环里空转。

### 3. 远程控制：Telegram / 飞书

ArgusBot 最实用的功能之一是 24/7 远程监控：

**Telegram 命令：**
- `/run <目标>` — 启动新任务
- `/inject <指令>` — 运行中注入新指令
- `/status` — 查看当前状态
- `/stop` — 停止
- 语音消息 → Whisper 转文字 → 当指令处理

**Daemon 模式的自动续接：**
- 任务完成后，Planner 会建议下一个目标
- 10 分钟无操作 → 自动执行建议的下一步
- 执行前自动 git checkpoint

这意味着你可以睡前给它一个目标，早上起来看 Telegram 消息就行。

## 关键设计细节

### 验收检查（Acceptance Checks）

```bash
argusbot-run \
  --max-rounds 10 \
  --check "pytest -q" \
  "实现 Feature X，直到测试全过"
```

`--check` 支持任意 shell 命令，而且可以叠加多个。Reviewer 判断 `done` 之前，所有 check 必须通过。

### Objective 模板

README 里推荐的目标格式很值得学：

```
Final Goal: <最终状态>
Current Task: <本次要做什么>
Acceptance Criteria: <怎么算完成>
Constraints: <约束>
Notes: <备注>
```

### YOLO 模式的安全风险

⚠️ **默认 `--yolo` 模式**意味着绕过所有沙箱和权限审批。Daemon 启动的任务全部是 YOLO 模式。这在个人开发机上还好，但在生产环境绝对不能这么用。

## 和类似工具的对比

| 特性 | ArgusBot | aider --auto | Claude Code Sub-Agent |
|------|----------|-------------|----------------------|
| Reviewer 门控 | ✅ 独立子 Agent | ❌ | ❌ |
| Planner 全局视图 | ✅ | ❌ | ❌ |
| 远程控制 | ✅ Telegram + 飞书 | ❌ | ❌ |
| 防停滞 | ✅ 看门狗 | ❌ | ❌ |
| 自动续接 | ✅ Daemon follow-up | ❌ | ❌ |
| 需要 Codex CLI | ✅ | ❌ (用自己的) | ❌ (Claude) |

ArgusBot 目前**只支持 Codex CLI**作为底层执行引擎。如果你用 Claude Code 或 aider，需要等它适配或者自己改 adapter。

## 适合谁用？

- ✅ 重度 Codex CLI 用户，经常跑长任务
- ✅ 想要"发个消息就启动任务，睡醒看结果"的人
- ✅ 研究多 Agent 协作架构的开发者
- ⚠️ 需要对 YOLO 模式的安全风险有清醒认识

## 我的看法

ArgusBot 抓住了一个真实痛点：Agent 的"自以为完成"。用独立 Reviewer 来做门控，比让 Agent 自己判断靠谱得多。Planner 的设计也很有意思——它不只是记录，在 `auto` 模式下会主动规划下一步，配合 Daemon 的自动续接，接近一个"自驱动"的开发循环。

但也要注意：默认 YOLO + max 500 轮 + 自动续接 = 这个 Agent 会非常激进地执行。确保你理解它在做什么。

---

![ArgusBot GitHub 仓库](https://opengraph.githubassets.com/1/waltstephen/ArgusBot)
*图片来源：[waltstephen/ArgusBot](https://github.com/waltstephen/ArgusBot) GitHub 仓库*

---

*🦞 大龙虾出品 · 2026-03-16*
