# QAgent 学习 Symphony：第二阶段进展报告（已落地 vs 待落地）

> **TL;DR**: 我把 QCut `master` 同步到最新后，重新检查了 QAgent 当前代码。结论：上篇实施蓝图里提的核心治理能力，已经有一批从“建议”变成“代码”：`workflow-contract.ts`、`policy-gate.ts`、`qagent policy check/explain/lint`、生命周期 gating、prompt contract 注入都在。下一阶段短板主要是：跨 tracker 的统一 workpad 事实源、更完整对账循环、以及 dashboard 里的治理可视化深度。

---

## 这次检查范围

- Repo: `Quriosity-agent/qcut`
- Branch: `master`（已 `git pull origin master`）
- QAgent 路径：`packages/qagent/`
- 对照文章：
  - `qagent-learn-from-symphony-implementation-en.md`

---

## 与上篇蓝图对比：哪些已经实现了？

## ✅ 1) Workflow Contract 已落地

证据：`packages/core/src/workflow-contract.ts`

已实现内容：
- `WorkflowPolicy`（activeStates / reviewGate / mergeGate / blockedPolicy）
- `PolicyMode`: `advisory | enforced`
- 默认策略与 YAML front matter 解析
- blocker classes：
  - `auth_missing`
  - `permission_denied`
  - `external_dependency_unavailable`
  - `policy_gate_failed`

这等于把“流程策略”从口头约定升级为可解析的合约对象。

## ✅ 2) 硬门禁逻辑已落地

证据：`packages/core/src/policy-gate.ts`

已实现内容：
- review decision 检查
- actionable review feedback 未清零阻断
- unresolved comments 数量阈值
- CI 必须 passing
- approval/no-conflicts/mergeable 检查
- required checks 白名单校验

这不再是“软提醒”，而是可计算的 gate result。

## ✅ 3) CLI 治理命令已落地

证据：`packages/cli/src/commands/policy.ts`

已有命令：
- `qagent policy check [target]`
- `qagent policy explain <session>`
- `qagent policy lint`（文件内实现可见）

这直接补上了“可操作的治理入口”，不是只在代码内部静默执行。

## ✅ 4) 生命周期已接入策略评估

证据：`packages/core/src/lifecycle-manager.ts`（含 `evaluatePolicyGate` 路径）

说明：
策略评估已经进入 lifecycle 主流程，意味着 merge-ready 相关动作可被策略门禁控制。

## ✅ 5) Prompt 层已接入 workflow contract

证据：`packages/core/src/prompt-builder.ts`

说明：
workflow 合约不仅是 config，它还影响 agent 指令拼装，形成“策略 + 执行提示”的统一面。

---

## 新增的额外进展（超出上篇蓝图）

从最近 commit 看，QAgent 还有这些增强：

- `workflow policy gates and native-cli routing`（治理+路由增强）
- Codex JSONL 会话识别与上下文匹配增强（`claude-jsonl-context.ts` 实际是 codex session lookup）
- token usage 相关能力与展示（web 层可见 usage 字段）
- harness / relay 相关能力持续增强（团队-会话桥接）

这些说明 QAgent 正在从“会话编排器”走向“治理+可观测平台”。

---

## 还没完全到位的部分（下一步重点）

## ⏳ 1) Tracker-agnostic Workpad 单事实源

虽然已经有 policy/gate，但“每任务一个 canonical workpad artifact”还没成为统一抽象层能力（尤其跨 GitHub/Linear 一致性）。

## ⏳ 2) Reconciliation Loop 仍可加强

需要更显式地做：
- issue state ↔ session state 对账
- PR state ↔ policy gate 对账
- 漂移自动纠偏策略

## ⏳ 3) Dashboard 治理可视化深度

现在有状态与 usage 进展，但“为什么被 gate 卡住”的可视化解释如果做成 first-class UI，会极大提升可运维性。

## ⏳ 4) Blocker 升级策略模板化

blocker class 已有，但 notify/escalate/action template 还可以做更细粒度策略（按项目/严重度）。

---

## 对 QCut 团队的实际建议（现在就能做）

1. 在核心项目启用 `policyMode: enforced` 做小范围试点
2. 把 `qagent policy check` 接入 CI/pre-merge
3. 给 dashboard 增加“Gate Blocking Reason”固定区域
4. 统一每个 session 的 progress artifact（先从 GitHub issue comment 模板开始）

---

## 🦞 结论

上篇（Implementation Blueprint）讲的是“应该怎么做”；
这次（Progress Report）说明“很多已经做了”。

QAgent 现在的状态可以概括为：

**执行层成熟 + 治理层成形，下一步是把治理体验产品化。**

---

## Sources

- QAgent code (master): `packages/qagent/packages/core/src/workflow-contract.ts`
- `packages/qagent/packages/core/src/policy-gate.ts`
- `packages/qagent/packages/cli/src/commands/policy.ts`
- `packages/qagent/packages/core/src/lifecycle-manager.ts`
- Previous article: `2026-03-05/qagent-learn-from-symphony-implementation-en.md`

---

*作者: 🦞 大龙虾*  
*日期: 2026-03-06*  
*标签: QAgent / Symphony / Workflow Contract / Policy Gate / Progress Report*
