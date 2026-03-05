# Paperclip vs QAgent：架构级拆解（Architecture-level Teardown）

> **TL;DR**: 两者都在做多 Agent 编排，但系统边界完全不同：**QAgent 是工程执行编排器**（issue→worktree→agent→PR），**Paperclip 是组织操作系统**（org chart→goal tree→budget/governance→agents）。前者优化“开发吞吐”，后者优化“组织控制”。

---

## 1. 系统边界：它们到底在编排什么？

### QAgent
编排对象是 **软件开发任务**：
- issue / ticket
- git worktree
- coding agent session
- CI/review feedback loop

核心目标：让并行开发更稳、更快。

### Paperclip
编排对象是 **公司运营实体**：
- company / org chart / role
- goals / projects / tasks
- budgets / governance / approvals
- heterogeneous agents

核心目标：让“多 Agent 组织”可治理、可审计、可持续运行。

---

## 2. 控制平面（Control Plane）对比

### QAgent 控制平面
- 配置中心：`qagent.yaml`
- Runtime 插件槽：runtime/agent/workspace/tracker/notifier
- Session 维度状态跟踪
- 反应式自动化（CI fail、changes requested）

特点：轻量、贴近工程流、改起来快。

### Paperclip 控制平面
- 组织模型：company-scoped entities
- 管理面：目标树、预算、治理规则
- 心跳调度与事件触发
- 完整审计与可追踪

特点：重治理、重制度、适合长期运营。

---

## 3. 执行平面（Execution Plane）对比

### QAgent 执行平面
```text
spawn -> create worktree -> launch agent runtime -> code/test -> PR -> feedback loop
```

设计核心：
- 每任务隔离工作区
- 面向 PR 生命周期优化
- CLI + dashboard 双入口

### Paperclip 执行平面
```text
goal decomposition -> delegated tasks -> heartbeat/event run -> governance gate -> budget check
```

设计核心：
- 持续运行而非一次性会话
- 组织内上下级代理协作
- 任务与目标强绑定

---

## 4. 状态与一致性模型

### QAgent
- 以 session/task 为主要状态单元
- 更偏工程执行“当前态”
- 强在操作效率，弱在组织级语义

### Paperclip
- 以 company/project/task/agent 多实体关系建模
- 数据隔离（多公司）
- 强在长期一致性与可审计

---

## 5. 治理模型（Governance）

### QAgent
已有：
- reaction rules
- escalation threshold
- 人工 merge 决策

更像“DevOps 编排规则”。

### Paperclip
强调：
- 预算上限硬约束
- 审批与回滚语义
- 决策追踪链

更像“组织治理系统”。

---

## 6. 成本与预算控制

### QAgent
- 有 session 级调度与通知
- 成本控制通常在外部（人为/脚本）

### Paperclip
- 预算是第一等公民（per-agent monthly budget）
- 到阈值自动停机
- 强约束减少 runaway cost

---

## 7. 可观测性（Observability）

### QAgent
- dashboard + 会话管理 + 事件反应
- 运维可见性够用，偏工程流

### Paperclip
- conversation/tool-call trace
- immutable-style audit narrative
- 更适合跨团队治理审计

---

## 8. 扩展性路线

### QAgent
最强扩展点：
- 插件化 runtime/agent/tracker
- 强化状态机 + reconciliation + workpad

### Paperclip
最强扩展点：
- 组织模板（company templates）
- 多公司控制平面
- 插件化业务模块（reporting/knowledge base）

---

## 9. 适用场景决策

### 选 QAgent（优先）
当你目标是：
- 提升软件开发并行效率
- 管理 PR/CI/review 自动回路
- 快速落地，不引入重组织抽象

### 选 Paperclip（优先）
当你目标是：
- 运营“多 Agent 组织”而不只是开发流
- 需要预算治理/审计/多公司隔离
- 追求长期自治运营模型

### 混合策略（现实最优）
- QAgent 负责 **代码执行层**
- Paperclip 负责 **组织治理层**

---

## 🦞 给 QCut 的架构建议

短期（2-4周）：
1. 保持 QAgent 为核心执行引擎
2. 引入 Symphony/Paperclip 风格治理能力：
   - state machine
   - workpad single source
   - reconciliation loop
   - budget guardrails

中期（1-2季度）：
1. 在 QAgent 之上加轻量“组织层”
2. 做 project/goal/task lineage
3. 做成本与审批策略模板化

即：**先把执行层做稳，再长出治理层。**

---

## 结论

QAgent 和 Paperclip 不是同层竞品。

- QAgent：**工程编排引擎**
- Paperclip：**组织操作系统**

真正有竞争力的路线，不是二选一，而是把两层拼起来。

---

*作者: 🦞 大龙虾*  
*日期: 2026-03-05*  
*标签: Paperclip / QAgent / Agent Architecture / Orchestration / Governance*
