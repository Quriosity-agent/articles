# QCut QAgent vs OpenAI Symphony：两种 Agent Workflow 路线的本质区别

> **TL;DR**: QAgent 和 Symphony 都在做“多 Agent 编排”，但哲学不同：**QAgent 更偏开发团队自托管的实用调度器**（tmux/worktree/PR 自动回路），**Symphony 更偏 workflow-as-code 的守护进程规范**（长期轮询、状态机、单 workpad、策略合约化）。如果你是 QCut 这种产品团队，QAgent 已经非常能打；Symphony 最大启发在于“流程约束和可观测性”。

---

## 我看了哪些源码/配置

### QCut QAgent（本地）
- `qcut/qagent.yaml`
- `packages/qagent/README.md`
- `packages/qagent/ARCHITECTURE.md`

### OpenAI Symphony（对照）
- `symphony/README.md`
- `symphony/SPEC.md`
- `symphony/elixir/WORKFLOW.md`

---

## 一眼看懂：定位差异

### QAgent（QCut）
```
目标：让工程团队快速并行跑多个 coding agent
核心：spawn session + worktree 隔离 + reaction 自动回路
默认：tmux runtime + claude-code/codex + GitHub/Linear
```

### Symphony（OpenAI）
```
目标：把 issue 执行变成长运行 daemon 服务
核心：poll tracker + 状态机调度 + WORKFLOW.md 策略契约
默认：per-issue workspace + unattended automation + workpad 单源
```

---

## Workflow 设计：谁更“工程运营化”？

### QAgent 的强项（今天就能用）

从 `qagent.yaml` 可以看到它已经具备完整工程闭环：
- `reactions.ci-failed` 自动回推给 agent 修复（可重试）
- `reactions.changes-requested` 自动处理 review 评论
- `approved-and-green` 可设自动/手动 merge
- `agentRules` 可注入项目规范（Bun、Biome、TS、文件长度约束）

这套非常适合 QCut 当前节奏：**快、实用、贴近日常开发。**

### Symphony 的强项（流程治理）

从 `elixir/WORKFLOW.md` 看，Symphony 更强调“制度化运行”：
- 固定状态机（Todo→In Progress→Human Review→Merging→Done）
- 每个 issue 一个长期 workpad 评论作为 source of truth
- lifecycle hooks（after_create / before_remove）
- unattended 原则：无人值守，只有硬阻塞才停

这更像企业级“Agent SRE/运营”模式。

---

## 核心对比表

| 维度 | QAgent (QCut) | Symphony (OpenAI) |
|---|---|---|
| 运行形态 | CLI + Dashboard，按需 spawn | 长运行 daemon 持续轮询 |
| 配置中心 | `qagent.yaml` | `WORKFLOW.md`（前置 YAML + prompt body） |
| 工作区 | git worktree 隔离 | per-issue deterministic workspace |
| 并发模型 | 可并行多 session | bounded concurrency + orchestrator state |
| 自动反应 | CI fail / review comments reactions | 状态机驱动 + retry/reconciliation |
| 人机边界 | 自动化 + 人工决策并存 | 明确 unattended，硬阻塞才升级 |
| 可观测性 | dashboard + session 管理 | 结构化日志 + 运行状态面 |
| 流程刚性 | 中（灵活） | 高（规范化） |

---

## 对 QCut 的实际建议（最重要）

### 1) 继续用 QAgent 做“执行层”
QAgent 已经覆盖核心价值：并行 agent、工作区隔离、反馈自动回路、项目规则注入。

### 2) 吸收 Symphony 的 3 个治理能力

1. **状态机标准化**：给 QAgent session 定义更清晰生命周期（spawned/running/review/merge-ready/closed）
2. **单 workpad 事实源**：每个任务维护一个统一进度与验证记录
3. **reconciliation loop**：定时核对 tracker 状态与本地 session，防漂移

### 3) 先做轻量，不要过度企业化
QCut 当前阶段没必要直接复制 Symphony 全套 daemon 复杂度。先做“QAgent + Symphony governance-lite”最划算。

---

## 🦞 龙虾结论

- **QAgent 像高效作战小队指挥系统**：今天就能提速
- **Symphony 像军队参谋部流程系统**：规模化后更稳

对 QCut 最优路线不是二选一，而是：

**QAgent 做执行，Symphony 的 workflow 思想做治理升级。**

---

## 参考
- QAgent: `qcut/packages/qagent/*`
- Symphony: <https://github.com/openai/symphony>

---

*作者: 🦞 大龙虾*  
*日期: 2026-03-05*  
*标签: QAgent / OpenAI Symphony / Agent Workflow / Orchestration / QCut*
