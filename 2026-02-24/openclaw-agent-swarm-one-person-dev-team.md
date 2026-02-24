# OpenClaw + Codex/Claude Code Agent Swarm：一个人的开发团队实战指南

**作者：Elvis (@elvissun) | 2026年2月23日**

---

## 一句话总结

Elvis 用 OpenClaw 作为编排层，让 AI orchestrator（Zoe）自动管理一群 Codex 和 Claude Code Agent，实现了一个人日均 50 次 commit、单日最高 94 次 commit、30 分钟 7 个 PR 的开发效率——而他甚至没打开编辑器。

---

## 核心理念：为什么需要编排层？

**上下文窗口是零和博弈。**

填满代码 → 没空间放业务上下文。填满客户历史 → 没空间放代码。所以需要两层系统：

- **OpenClaw（编排层）** — 持有所有业务上下文：客户数据、会议记录、历史决策、成败经验
- **Codex / Claude Code（执行层）** — 专注写代码，接收精确的 prompt

两层各自加载最需要的上下文，通过专注实现专业化。

---

## 完整 8 步工作流

### Step 1：客户需求 → 与 Zoe 讨论

客户通话后，会议记录自动同步到 Obsidian vault。Zoe 直接读取，零解释成本。一起 scope 功能，然后 Zoe 做三件事：
- 充值客户额度（有 admin API 权限）
- 从生产数据库拉客户配置（只读权限，Codex 永远没有）
- Spawn Codex Agent，带完整上下文的 prompt

### Step 2：Spawn Agent

每个 Agent 独立 worktree + tmux session：

```bash
git worktree add ../feat-custom-templates -b feat/custom-templates origin/main
tmux new-session -d -s "codex-templates" \
  "$HOME/.codex-agent/run-agent.sh templates gpt-5.3-codex high"
```

关键发现：**tmux 比 `codex exec` 更好**——可以中途重定向 Agent：

```bash
# Agent 方向错了？
tmux send-keys -t codex-templates "Stop. Focus on the API layer first." Enter
# 需要更多上下文？
tmux send-keys -t codex-templates "The schema is in src/types/template.ts." Enter
```

### Step 3：自动监控循环

Cron 每 10 分钟运行，**不直接 poll Agent**（太贵），而是读 JSON 注册表检查：
- tmux session 是否存活
- 是否有 open PR
- CI 状态（通过 gh CLI）
- 失败自动重生（最多 3 次）

### Step 4：Agent 创建 PR

Agent commit → push → `gh pr create --fill`。但 **PR 创建 ≠ 完成**。

**完成的定义：**
- PR 已创建
- 分支与 main 同步（无冲突）
- CI 通过（lint、类型、单测、E2E）
- Codex review 通过
- Claude Code review 通过
- Gemini review 通过
- UI 变更含截图

### Step 5：三重 AI Code Review

| 模型 | 特点 |
|------|------|
| **Codex** | 最彻底。擅长边界情况、逻辑错误、竞态条件。误报率极低 |
| **Gemini Code Assist** | 免费且好用。擅长安全问题、可扩展性。会建议具体修复方案 |
| **Claude Code** | 基本没用——过度谨慎，建议通常是过度设计。只看 critical 级别 |

### Step 6-7：自动测试 → 人工 Review

CI 跑完所有测试后，Telegram 通知："PR #341 ready for review。"

此时三个 AI 已审核、CI 已通过、截图已包含。人工 review 只需 **5-10 分钟**，很多 PR 甚至不看代码——截图就够了。

### Step 8：Merge + 清理

日常 cron 清理孤立 worktree 和 task JSON。

---

## 进化版 Ralph Loop

与标准 Ralph Loop（拉上下文→生成→评估→保存）不同，这个系统的 retry 更智能：

- Agent 上下文不够？"只关注这三个文件"
- Agent 方向错误？"客户要的是 X 不是 Y，这是会议原话"
- Agent 需要澄清？"这是客户邮件和公司介绍"

**Zoe 还主动找活干：**
- 早上扫 Sentry → 4 个新错误 → spawn 4 个 Agent 修复
- 会后扫会议记录 → 3 个功能请求 → spawn 3 个 Codex Agent
- 晚上扫 git log → spawn Claude Code 更新 changelog

成功模式会被记录："这种 prompt 结构适合计费功能"、"Codex 需要先给类型定义"、"永远包含测试文件路径"。

---

## Agent 选型

| Agent | 最佳场景 | 占比 |
|-------|---------|------|
| **Codex** | 后端逻辑、复杂 bug、跨文件重构 | 90% |
| **Claude Code** | 前端、速度快、git 操作 | — |
| **Gemini** | UI 设计感 → 生成 HTML/CSS spec → 交给 Claude Code 实现 | — |

---

## 成本与瓶颈

- **成本**：Claude ~$100/月 + Codex ~$90/月（可从 $20 起步）
- **瓶颈：内存！** 每个 Agent 需要独立 worktree + node_modules + 编译器。16GB Mac Mini 最多跑 4-5 个 Agent。Elvis 买了 128GB Mac Studio M4 Max（$3,500）来解决。

---

## 为什么值得关注

这不是 demo，是**真实运营的 B2B SaaS**（Agentic PR——帮初创公司获取媒体报道）。Elvis 用这套系统把功能请求当天交付，速度直接转化为付费客户。

核心洞察：**2026 年的竞争力不是写代码快，而是管 Agent 好。** 从"自己写代码"到"管 Claude Code"到"管一个管 Claude Code 的 AI"——每一层抽象都是效率倍增。

---

*原文：Elvis (@elvissun) X Article，2026年2月23日*
