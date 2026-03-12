# OpenAI Codex Best Practices 深度拆解：给 Builder 的落地手册

> Source: OpenAI Developers — Codex Learn / Best Practices  
> URL: https://developers.openai.com/codex/learn/best-practices  
> Published analysis date: 2026-03-13

![OpenAI Codex Best Practices (Open Graph)](https://developers.openai.com/open-graph.png)

*图片来源：OpenAI Developers 页面 Open Graph 图（`https://developers.openai.com/open-graph.png`），版权归 OpenAI 所有。*

---

## 一句话结论

这篇官方 best practices 的核心不是“怎么写一条更花哨的 Prompt”，而是：**把 Codex 当成可配置、可迭代、可运营的工程搭档系统**。

如果你是 Builder，真正该做的是把“临时聊天习惯”升级成一套稳定流水线：

**上下文结构化 → 规则外置（AGENTS.md）→ 环境配置（config）→ 外部工具接入（MCP）→ 经验固化（Skills）→ 周期执行（Automations）**。

---

## 1) Prompt 的重点：不是华丽，而是可执行

官方建议的四段式 prompt 模板非常实用：

- **Goal**：你要改什么/做什么
- **Context**：相关文件、目录、报错、文档
- **Constraints**：架构、规范、安全要求
- **Done when**：完成判定（测试通过、bug 不复现等）

### Builder takeaway

把“Done when”写清楚，收益最大。因为这会把 Codex 从“写代码助手”变成“交付结果助手”。

推荐你在任务里加这句：

```text
Done when:
1) tests pass
2) lint/typecheck clean
3) behavior verified with repro steps
4) brief risk review included
```

---

## 2) 难任务先规划：Plan mode 比硬写快

文档强调：复杂、多步骤、需求模糊时，先计划再编码。

可用方式：
- `/plan`（Plan mode）
- 让 Codex 先“反向采访你”澄清需求
- 用 `PLANS.md` / execution plan 模板

### Builder takeaway

你可以把“先计划”变成默认工作流：

- 小任务（<30 分钟）直接做
- 中任务（30–120 分钟）先 5 分钟计划
- 大任务（跨天）强制落盘计划文档

这会显著减少返工和上下文漂移。

---

## 3) AGENTS.md 是长期收益最高的资产

官方把 AGENTS.md 定义为“agent 的 README”，会自动进入上下文。关键建议：

- 写 repo 结构、运行方法、测试命令
- 写工程规范和禁区
- 写“完成标准”和验证步骤
- 短小、准确、贴近真实流程

并且支持多层级：
- 全局（`~/.codex`）
- 仓库级
- 子目录级（越近优先级越高）

### Builder takeaway

当 Codex 同样错误出现第 2 次，就立刻把规则写进 AGENTS.md。别每次在 prompt 里重复吼一遍。

一个很实用的最小模板：

```md
## Commands
- test: ...
- lint: ...
- typecheck: ...

## Constraints
- 不允许改动 xxx 模块
- 数据库迁移必须包含回滚脚本

## Done When
- 单测/集成测试通过
- 关键路径手动验证完成
- 提交包含变更说明与风险点
```

---

## 4) 配置先于技巧：很多“模型问题”其实是“环境问题”

文档非常强调配置分层：

- 个人默认：`~/.codex/config.toml`
- 项目默认：`.codex/config.toml`
- 一次性覆盖：CLI flags

可配项包括：模型、reasoning effort、sandbox、approval、profiles、MCP、多 agent。

### Builder takeaway

如果你觉得 Codex “忽然变笨”，优先排查这四件事：

1. 工作目录是不是错了
2. 是否有写权限
3. 默认模型/推理级别是否匹配任务
4. MCP/依赖工具是否可用

这四项比“重写 prompt”更容易直接见效。

---

## 5) 交付闭环：让 Codex 不只写，还要测、查、审

官方建议不要停留在“让它改代码”，还要要求它：

- 补测试/改测试
- 跑对应 checks
- 验证行为
- 审查 diff 风险

并推荐 `/review` 做 PR 风格审查（基线分支、未提交变更、某次 commit、自定义规则）。

### Builder takeaway

把“生成代码”改为“生成 + 自验 + 自审”三件套，代码质量会明显稳定。

建议每次都要求它输出：

- 变更摘要
- 测试结果
- 未覆盖风险
- 回滚建议

---

## 6) MCP：把“粘贴上下文”升级为“实时上下文”

什么时候该上 MCP（Model Context Protocol）？

- 信息在仓库外
- 数据经常变
- 你想让 agent 真正调用工具
- 你要可复用的团队集成

官方建议：先接 1–2 个高价值工具，不要一开始全接。

### Builder takeaway

最优策略是先打掉一个高频手工环：

- 例：CI 失败诊断、日志排障、Issue triage、发布说明生成

单点打通后再扩展，否则“工具很多，效果很弱”。

---

## 7) Skills + Automations：方法和日程分离

官方给了很清晰的分工：

- **Skills 定义方法**（怎么做）
- **Automations 定义调度**（什么时候做）

适合 Skill 化的场景：
- Log triage
- PR checklist review
- Migration planning
- Incident summary

适合 Automation 的场景：
- 每日 commit 摘要
- 定时 bug 扫描
- CI 失败巡检
- standup 汇总

### Builder takeaway

先手工把流程跑稳定，再自动化。不要把“还不稳定的流程”直接 cron 化。

---

## 8) 线程管理是质量开关

官方强调：thread 是“工作线程”，不是普通聊天历史。

关键原则：
- 一个 thread 对应一个连贯任务
- 真正分叉再 fork
- 大上下文用 compact
- 用 multi-agent 把边界清晰的子任务外包

### Builder takeaway

“一个项目一个线程”通常会把上下文拖垮。应改成“一个任务一个线程”。

---

## 9) 新手常见坑（官方清单）

我把文档里的坑压缩成 Builder 版本：

1. 把长期规则写在每次 prompt，而不是 AGENTS.md/Skill
2. 不给测试命令，导致 agent 无法“看见自己的结果”
3. 复杂任务跳过 planning
4. 还没理解流程就开全权限
5. 同文件多线程同时改，且不用 worktree
6. 手工流程还不稳定就上自动化
7. 用“项目级超长线程”造成上下文污染

---

## 一套可直接抄的落地路径（7 天）

### Day 1
- 建 repo-level `AGENTS.md`
- 补齐 run/test/lint/typecheck 命令

### Day 2
- 固化四段式 prompt 模板（Goal/Context/Constraints/Done when）

### Day 3
- 给复杂任务默认启用 Plan mode

### Day 4
- 配好 `.codex/config.toml`（模型、reasoning、sandbox/approval）

### Day 5
- 接入 1 个 MCP（你最高频的外部数据源）

### Day 6
- 把一个重复流程做成 Skill（比如 PR review checklist）

### Day 7
- 把稳定 Skill 做成 Automation（低频开始）

---

## 最后总结

OpenAI 这篇 best practices 真正传达的是一个工程观：

- **Prompt 是入口，不是系统**
- **规则要沉淀到文件，而不是脑子里**
- **Agent 的上限由工作流设计决定，不由一句咒语决定**

对于 Builder 来说，最现实的目标不是“让 Codex 一次写对”，而是“让 Codex 在你的系统里持续写对”。

—— 完 🦞
