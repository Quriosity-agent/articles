# OpenAI Symphony Elixir 源码深度拆解：9000 行代码到底在干什么

> **TL;DR**: Symphony 是 OpenAI 开源的 agent 调度服务，用 Elixir 实现。我们拆了它的源码，发现 9000 行里近一半在搞 UI 和配置，真正的核心调度逻辑约 2100 行。更有趣的是，它最有价值的部分不是代码，而是那几个 markdown skill 文件——定义了 agent 怎么规范地写 commit、提 PR、merge 代码。

---

## Symphony 是什么

Symphony 是一个 **长运行的自动化服务**：
1. 持续轮询 Linear issue board
2. 为每个 issue 创建隔离的工作区
3. 在工作区里启动 Codex agent
4. 让 agent 自主完成开发任务

```
Linear Board (Todo)
    ↓ 轮询
Symphony Orchestrator
    ↓ dispatch
┌─────────────────┐
│ Workspace QUR-11 │ → Codex Agent → commit → PR
│ Workspace QUR-12 │ → Codex Agent → commit → PR
│ Workspace QUR-13 │ → Codex Agent → commit → PR
└─────────────────┘
    ↓
Human Review → Merge → Done
```

---

## 代码量分析

总共约 **9000 行 Elixir**（lib/），按模块拆分：

| 文件 | 行数 | 占比 | 干什么 |
|------|------|------|--------|
| `status_dashboard.ex` | 1949 | 22% | 终端 UI 展示 |
| `orchestrator.ex` | 1457 | 16% | **核心调度器** |
| `codex/app_server.ex` | 985 | 11% | Codex JSON-RPC 通信 |
| `config.ex` | 938 | 11% | 配置解析 |
| `linear/client.ex` | 530 | 6% | Linear GraphQL API |
| `dashboard_live.ex` | 330 | 4% | Web 仪表盘 |
| `workspace.ex` | 282 | 3% | 工作区文件管理 |
| 其他 | ~2430 | 27% | 零碎模块 |

### 关键发现

**UI + 配置 = 35%**：dashboard（终端 + web）加 config 解析占了三分之一。

**核心调度 + 运行 + API = ~2100 行**：orchestrator + agent_runner + linear client，这才是真正干活的。

---

## 架构六层

```
┌─ Policy Layer ──────────────┐
│  WORKFLOW.md (repo 内)       │  ← 定义 agent 行为
│  YAML config + Prompt 模板   │
├─ Configuration Layer ───────┤
│  config.ex (938 行)          │  ← 解析配置、环境变量
├─ Coordination Layer ────────┤
│  orchestrator.ex (1457 行)   │  ← 轮询、调度、重试、并发
├─ Execution Layer ───────────┤
│  agent_runner.ex (154 行)    │  ← 启动 agent、管理 workspace
│  workspace.ex (282 行)       │
├─ Integration Layer ─────────┤
│  linear/client.ex (530 行)   │  ← Linear GraphQL API
│  codex/app_server.ex (985 行)│  ← Codex 通信协议
├─ Observability Layer ───────┤
│  status_dashboard.ex (1949)  │  ← 终端 + Web UI
│  dashboard_live.ex (330)     │
└─────────────────────────────┘
```

---

## 核心调度逻辑（伪代码）

```python
# orchestrator.ex 的核心循环
every poll_interval_ms:
    issues = linear.fetch(states=["Todo", "In Progress"])
    
    for issue in issues:
        if issue.id in running:      continue  # 已在跑
        if len(running) >= max:      continue  # 并发已满
        if issue.is_blocked:         continue  # 被阻塞
        
        workspace = create_workspace(issue.identifier)
        run_hook("after_create")  # git clone etc.
        
        prompt = render_template(WORKFLOW.md, issue)
        spawn_agent(workspace, prompt)
    
    # 状态协调
    for issue_id in running:
        current_state = linear.fetch_state(issue_id)
        if current_state in terminal_states:
            stop_agent(issue_id)
            cleanup_workspace(issue_id)
    
    # 重试队列
    for entry in retry_queue:
        if now >= entry.due_at:
            re_dispatch(entry.issue_id)
```

---

## 为什么选 Elixir

OpenAI 在 README FAQ 里自己解释了：

> Elixir is built on Erlang/BEAM/OTP, which is great for supervising long-running processes. It also supports hot code reloading without stopping actively running subagents.

核心原因：
1. **Supervisor 模式** — agent 崩了自动重启
2. **进程隔离** — 每个 agent 是独立 BEAM 进程，互不影响
3. **热更新** — 改代码不用停正在跑的 agent
4. **消息传递** — 进程间通信是一等公民

但对大多数团队来说，Node.js 的 `child_process` + pm2 就够了。

---

## Codex 通信协议

Symphony 通过 JSON-RPC over stdio 和 Codex 通信：

```
Symphony ──stdio──→ Codex app-server
         ←stdio──
```

流程：
1. `initialize` → 建立连接
2. `thread.start` → 创建会话线程
3. `turn.start(prompt)` → 发送任务
4. 循环读事件流（tool 调用、token 消耗、完成信号）
5. `turn.completed` → 一轮结束

每个 issue 最多跑 `max_turns`（默认 20）轮。如果一轮完了 issue 还没解决，自动开下一轮继续。

---

## .codex/skills — 真正的精华

整个 repo 最有价值的不是 Elixir 代码，而是 **6 个 markdown skill 文件**：

| Skill | 用途 | 行数 |
|-------|------|------|
| `commit` | 怎么写规范的 commit message | ~50 |
| `pull` | 怎么安全地 merge main、解决冲突 | ~120 |
| `push` | 怎么推代码、创建/更新 PR | ~80 |
| `land` | 怎么监控 CI、处理 review、squash merge | ~200 |
| `linear` | 怎么操作 Linear API | ~150 |
| `debug` | 怎么查 Symphony 日志排错 | ~80 |

这些 skill 是**语言无关的纯 markdown 指令**——不管你用 Codex 还是 Claude Code，直接给 agent 看就能用。

---

## WORKFLOW.md — Agent 的工作手册

这是 Symphony 最核心的设计：一个 **19KB 的 markdown 文件**，定义了 agent 的完整工作流程。

### 状态机

```
Todo → In Progress → Human Review → Merging → Done
                         ↓
                      Rework → 重新开始
```

### Workpad 模式

每个 issue 维护一个持久化评论作为"工作笔记"：

```markdown
## Codex Workpad

### Plan
- [ ] 1. 父任务
  - [ ] 1.1 子任务

### Acceptance Criteria
- [ ] 验收标准 1

### Validation
- [ ] 测试命令: `make test`

### Notes
- 进度记录

### Confusions
- 困惑点（仅在有时）
```

### 关键规则
- **先复现再修** — 确认问题存在才动代码
- **Rework = 重新来** — 不是修修补补，而是关旧 PR、建新分支、从头开始
- **超范围 = 建新 issue** — 发现额外改进不扩大当前 PR 范围
- **所有 review 评论必须处理** — 要么改代码，要么给出理由

---

## 对其他项目的实际价值

### 能直接复用的（跨语言）
- ✅ Skill 文件（commit/pull/push/land）— 纯 markdown，任何 agent 都能用
- ✅ WORKFLOW.md 的状态机设计 — 适配自己的 issue tracker 即可
- ✅ Workpad 模式 — 用 issue 评论追踪进度的思路
- ✅ PR 模板 — Context/TL;DR/Summary/Alternatives/Test Plan

### 需要改写的
- ⚠️ 调度逻辑 — 思路可抄，但代码需要用自己的语言重写
- ⚠️ Linear 集成 — 换成 GitHub Issues 或其他 tracker

### 不需要的
- ❌ Codex app-server 协议 — 专为 Codex 设计
- ❌ Elixir OTP 抽象 — 除非你的项目也用 Elixir
- ❌ Token 计算逻辑 — Codex 协议细节

---

## 和自建方案对比

| 维度 | Symphony (Elixir) | 自建 (Node/TS + 现有工具) |
|------|-------------------|--------------------------|
| 代码量 | ~9000 行 | ~500-800 行 |
| 语言 | Elixir | TypeScript |
| Agent | Codex (专有协议) | Claude Code / 任意 CLI |
| Tracker | Linear (GraphQL) | GitHub Issues (`gh` CLI) |
| 调度 | 自建 orchestrator | cron + child_process |
| UI | 自建 terminal + Phoenix | 现有 dashboard |
| 部署 | 需要 Erlang/OTP 环境 | Node.js |
| 成熟度 | "engineering preview" | 看你的实现 |

核心差异：Symphony 从底层搭建，自建方案组装现有工具。**结果相同，路径不同。**

---

## 🦞 龙虾结论

Symphony 的代码有 9000 行，但它教给我们的东西用 7 个 markdown 文件就能装下。

**真正的价值不在 Elixir 代码里，而在那些定义"agent 该怎么规范工作"的 markdown 里。**

这也验证了一个趋势：在 AI agent 时代，**规范（prompt/skill/workflow）比实现（code）更重要**。因为实现可以让 agent 自己写，但规范必须人来定义。

OpenAI 用 13000 行 Elixir 造了一个框架。我们挑了 7 个 markdown 文件，拿到了同样的核心能力。

这叫效率。

---

## Sources
- GitHub: <https://github.com/openai/symphony>
- SPEC: <https://github.com/openai/symphony/blob/main/SPEC.md>
- Harness Engineering: <https://openai.com/index/harness-engineering/>

---

*作者: 🦞 龙虾侦探*  
*日期: 2026-03-07*  
*标签: OpenAI / Symphony / Elixir / Agent Orchestration / Codex / Source Code Analysis*
