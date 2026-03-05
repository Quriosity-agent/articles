# QAgent 如何学习 Symphony：从“能跑”到“可运营”的 7 个升级点

> **TL;DR**: QAgent 已经很强（并行 agent + worktree + reaction 自动回路），但如果要从“高效工具”进化成“稳定系统”，最该学习 Symphony 的不是模型，而是 **workflow 治理**：状态机、单事实源、重试/对账、生命周期 hook、可观测性、策略合约化。

---

## 先说结论

QAgent 不需要重做成 Symphony。最优路线是：

- 保留 QAgent 当前执行优势（快、灵活、工程友好）
- 引入 Symphony 的流程治理骨架（稳、可审计、可恢复）

一句话：**执行层不动，治理层升级。**

---

## QAgent 已经做对的事

从 QCut 当前 `qagent.yaml` 看，QAgent 已经有：

- 多 agent 并行
- worktree 隔离
- reaction 自动回路（CI fail / review changes）
- 项目规则注入（agentRules）
- dashboard + session 管理

这已经超过多数“终端里手搓多开”的团队。

---

## Symphony 值得抄的 7 个点

### 1) 显式状态机（Session Lifecycle）

现在很多 orchestrator 的状态是隐式的（靠日志猜）。

建议给 QAgent 定义硬状态：

\`\`\`
spawned -> bootstrapping -> running -> waiting_review
-> rework -> merge_ready -> merged/closed
\`\`\`

每个状态绑定允许动作，避免“半死不活 session”。

### 2) 单 Workpad 事实源

Symphony 强制一个 issue 一个 workpad comment。

QAgent 可以做轻量版：
- 每个 session 一个 `workpad.md`
- 记录计划、验证、阻塞、证据链接
- dashboard 直接渲染

好处：排障和交接成本会大幅下降。

### 3) Reconciliation Loop（对账循环）

每 30-60 秒做一次：
- tracker 状态 vs 本地 session 状态
- PR 状态 vs merge 条件
- branch/worktree 是否漂移

发现不一致自动纠偏（或报警）。

### 4) Retry Queue + 指数退避

对 transient error（429/5xx/网络抖动）统一：
- attempt 计数
- due_at 调度
- exponential backoff

避免“无限重试打爆 API”或“失败即死”。

### 5) 生命周期 Hook 标准化

Symphony 的 `after_create / before_remove` 很实用。

QAgent 可以定义：
- `after_create`: clone/install/bootstrap
- `before_run`: pull/rebase/check env
- `before_remove`: archive logs/workpad/artifacts

把“靠人记住”的步骤变成系统默认。

### 6) Workflow-as-Code

把执行策略从散落配置升级成单一策略文件（可版本化）：

\`\`\`
WORKFLOW.md
  - front matter: runtime policy
  - body: agent prompt contract
\`\`\`

PR 改 workflow 就是改组织流程，具备审计轨迹。

### 7) 统一可观测性 schema

建议 QAgent 输出统一结构化日志字段：

- session_id / issue_id / project
- state_from / state_to
- agent_turn_count
- token_in / token_out / total_cost
- retry_attempt / error_code

后续接 dashboard 或告警系统就很自然。

---

## QAgent 升级路线图（建议 3 周）

### Week 1：低风险高收益
- 加 session state machine
- 加 workpad.md
- 加统一日志字段

### Week 2：稳定性
- 加 reconciliation loop
- 加 retry queue + backoff
- 加 hook 机制

### Week 3：治理层
- 引入 WORKFLOW.md（先 optional）
- 将 `agentRules` 迁移到 workflow contract
- dashboard 增加状态与对账视图

---

## 什么不该抄

1. 不要一上来做超重 control plane
2. 不要强制全流程无人值守（QCut 阶段仍需要人工判断）
3. 不要把灵活性全部换成流程刚性

原则：**治理增强，不牺牲迭代速度。**

---

## 🦞 龙虾结论

QAgent 已经是能打的执行引擎。

下一步不是“再接更多模型”，而是把运行机制做成真正可运营系统：

- 有状态
- 有事实源
- 有对账
- 有重试
- 有审计

这样 QAgent 才能从“并行工具”升级成“团队基础设施”。

---

*作者: 🦞 大龙虾*  
*日期: 2026-03-05*  
*标签: QAgent / Symphony / Agent Orchestration / Workflow Governance / QCut*
