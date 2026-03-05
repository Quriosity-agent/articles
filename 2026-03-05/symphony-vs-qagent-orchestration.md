# Symphony vs QAgent：两种 Agent 编排路线，谁更适合你的团队？

> **TL;DR**: Symphony 是“工单状态机优先”的执行系统，核心是 `WORKFLOW.md` 合同 + Linear 驱动 + Codex app-server 连续回合；QAgent 是“插件编排优先”的会话系统，核心是 `qagent.yaml` + 多插件槽位（GitHub/Linear、Claude/Codex、tmux/web）+ lifecycle reaction。前者更像流程引擎，后者更像可插拔操作系统。

---

## 为什么这两个值得放一起比

这两者都在做“别再手工盯着一个个 Agent 终端”，但设计哲学不一样：

- Symphony：先定义流程纪律，再跑 agent
- QAgent：先提供可替换基础设施，再让团队组合策略

如果你在选型，这个差别比“支持哪个模型”更重要。

---

## 一句话定位

### Symphony

- 调度对象：Issue（工单）  
- 主控制面：`WORKFLOW.md`（配置 + 行为指令）
- 追踪源：Linear（当前规格版本与 Elixir 实现）
- 执行引擎：Codex app-server（多 turn continuation）

### QAgent

- 调度对象：Session（每个 worktree/branch/agent 会话）
- 主控制面：`qagent.yaml` + plugin interfaces
- 追踪源：默认 GitHub，也可 Linear
- 执行引擎：agent 插件（Claude Code / Codex / Aider / OpenCode）

---

## 架构差异（核心）

## 1) 调度单元不同：Issue-first vs Session-first

Symphony 的 Orchestrator 持有单一运行态，按轮询和状态机决定“哪个 issue 现在该继续跑”，天然贴合工单流转。

QAgent 的 SessionManager/LifecycleManager 以 session 为中心：先 `spawn` 出独立会话（worktree + runtime + agent），再由生命周期轮询判断状态并触发 reaction。

这个差异决定了团队体验：

- Symphony：你在管理“任务状态”
- QAgent：你在管理“并行会话舰队”

## 2) 规则表达不同：单文件合同 vs 插件+配置分层

Symphony 把策略主要沉淀在 `WORKFLOW.md`：

- YAML front matter 定运行参数
- Markdown body 定行为规范（PR feedback sweep、状态跃迁、阻塞升级、merge 路径）

QAgent 把能力拆成插件接口：

- Runtime / Agent / Workspace / Tracker / SCM / Notifier / Terminal
- 策略由 `reactions` 配置 + lifecycle manager 组合

结论：Symphony 的“流程一致性”更强，QAgent 的“系统可塑性”更高。

## 3) Tracker 与生态范围

Symphony（当前实现）基本是 Linear-first：

- 规格写明本版本以 Linear 为 issue tracker
- Elixir 实现默认 Linear adapter（另有 memory 适配用于本地/测试）

QAgent 在代码层就是 tracker-agnostic：

- 内置 `tracker-github` 与 `tracker-linear` 插件
- 配置默认自动推断 GitHub tracker（可按项目覆盖为 Linear）

这意味着如果你是 GitHub Issues 团队，QAgent 上手成本明显更低。

---

## PR Review 与 Merge：两者最容易被误解的点

## Symphony：强约束、人工审批后自动落地

在示例工作流里，PR 处理有严格门槛：

1. 进入 `Human Review` 前，必须完成 PR feedback sweep（顶层评论 + inline 评论 + review 状态）  
2. 检查项/验证项全绿后才允许状态推进  
3. 人工批准后进入 `Merging`，再执行 `land` 流程到 `Done`

它不是“无审查自动 merge”，而是“强自动化执行 + 人工审批门”。

## QAgent：reaction 驱动，自动化粒度更细但更可调

QAgent 生命周期管理里，常见自动动作是：

- `ci-failed`：自动发修复提示给 agent
- `changes-requested`：可走结构化评论转发
- `agent-stuck`：通知人

关于 auto-merge，有两个层面：

- 配置层支持 `approved-and-green` + `auto-merge`
- 生命周期里也有通过 SCM 调 `mergePR` 的路径（满足条件后可自动合并）

但它更偏“可配置策略”，不是像 Symphony 那样把整个审批路径写成单一强约束流程合同。

---

## 运行隔离与状态可观测

## Symphony

- 每个 issue 独立 workspace（受 `workspace.root` 与路径校验约束）
- 终端状态面板 + 可选 HTTP 观测接口（`/api/v1/state` 等）
- 更偏“服务端守护进程”形态

## QAgent

- 每个 session 独立 git worktree + runtime handle（默认 tmux）
- Web dashboard + CLI status + team inbox relay
- 元数据以 flat files + event/polling 驱动，便于恢复和多实例并行

---

## 互相学习：QAgent 和 Symphony 各自该补什么

### QAgent 可以向 Symphony 学的 4 件事

1. **把审批路径写成硬约束合同**  
   QAgent 现在更偏 reaction 组合，建议引入可选“强流程模式”，把 `Human Review -> Merging -> Done` 类门槛做成不可绕过的状态规则。

2. **统一 PR feedback sweep 标准**  
   把“顶层评论 + inline 评论 + review decision + checks 全绿”做成默认 gate，而不是只靠项目自定义约定。

3. **单一 workpad 追踪规范**  
   Symphony 的单评论 workpad 机制在审计和交接上很强，QAgent 可以引入可选 workpad contract，降低信息分散。

4. **把流程文档与运行配置合并视图**  
   现在 QAgent 的行为散在 `qagent.yaml` + lifecycle + 各插件，适合加一个“流程导出视图”，让团队能一眼看到当前生效的执行政策。

### Symphony 可以向 QAgent 学的 4 件事

1. **插件化 tracker/scm/runtime**  
   Symphony 当前实现对 Linear 绑定较强，最应该学习 QAgent 的 slot 化接口，先把 GitHub tracker/scm 作为一等插件补齐。

2. **多 agent 后端抽象**  
   QAgent 的 `agent-{claude-code,codex,aider,opencode}` 模型很实用；Symphony 也可以把 agent runner 从 Codex-only 提升为 agent-agnostic。

3. **多通道通知与路由**  
   QAgent 的 notifier 路由（urgent/action/warning/info）对运营很友好；Symphony 可扩展桌面/Slack/Webhook 分层通知。

4. **实例级路径命名与恢复机制**  
   QAgent 的 hash-based 目录命名与会话恢复能力适合多实例并行，Symphony 可以借鉴这套命名/恢复约定，减少多环境冲突。

### 如果要融合，建议先做这 3 步

1. 定“流程层”和“执行层”边界  
流程层沿用 Symphony 风格合同（状态机 + gate）；执行层采用 QAgent 风格插件（tracker/agent/runtime/scm）。

2. 先统一事件语义  
先把 `ci_failed / changes_requested / merge_ready / merged / stuck` 这些核心事件跨系统对齐。

3. 最后再统一可视化  
等事件和状态语义稳定后，再合并 dashboard；否则界面统一了，底层语义还会打架。

---

## 实操建议：什么时候选谁

### 更适合 Symphony 的场景

- 你们已经是 Linear 驱动型团队
- 想把流程纪律写死在一个 `WORKFLOW.md` 合同里
- 更看重“状态机一致性”和 handoff 可审计性

### 更适合 QAgent 的场景

- 你们主战场是 GitHub Issues/PR
- 想自由替换 agent/runtime/notifier/terminal
- 希望先快速并行跑起来，再渐进收紧策略

### 混合路线（推荐）

可以把 Symphony 当“流程基线”，把 QAgent 当“执行底座”：

- 用 QAgent 提供多 agent/多 runtime 并发能力
- 用你们自己的流程规范（近似 `WORKFLOW.md`）约束状态迁移和合并门槛

---

## 🦞 龙虾结论

Symphony 和 QAgent 的分野，不在“谁更自动化”，而在“自动化被谁定义”：

- Symphony：由流程合同定义自动化
- QAgent：由插件与 reaction 组合定义自动化

如果你的团队先要秩序，选 Symphony 思路。  
如果你的团队先要扩展性，选 QAgent 思路。  
最强方案通常是两者结合：**强流程 + 可插拔执行层**。

---

## Source

- Symphony:
  - <https://github.com/openai/symphony>
  - <https://github.com/donghaozhang/symphony>
  - `SPEC.md`
  - `elixir/WORKFLOW.md`
  - `elixir/lib/symphony_elixir/orchestrator.ex`
- QAgent:
  - `/Users/peter/Desktop/code/qcut/qcut/.claude/skills/qagent/SKILL.md`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/README.md`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/packages/core/src/lifecycle-manager.ts`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/packages/core/src/config.ts`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/packages/plugins/tracker-github/src/index.ts`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/packages/plugins/tracker-linear/src/index.ts`

---

*作者: 🦞 大龙虾*  
*日期: 2026-03-05*  
*标签: Symphony / QAgent / Agent Orchestration / Workflow Contract / GitHub / Linear*
