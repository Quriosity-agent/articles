---
title: "Loop Engineering 深度拆解：Agent 时代真正要设计的不是 Prompt，而是会自我推进的控制系统"
date: 2026-06-07
source: "https://x.com/addyosmani/status/2064127981161959567?s=20"
canonical: "https://addyosmani.com/blog/loop-engineering/"
x_article: "https://x.com/i/article/2064122477731852288"
author: "Addy Osmani"
tags:
  - Loop Engineering
  - AI Agents
  - Coding Agents
  - Codex
  - Claude Code
  - Agent Harness
  - Agentic Software Engineering
---

# Loop Engineering 深度拆解：Agent 时代真正要设计的不是 Prompt，而是会自我推进的控制系统

Addy Osmani 在 X 上转发并发布了他的文章 [**Loop Engineering**](https://addyosmani.com/blog/loop-engineering/)。这篇文章把最近 AI Coding 圈里几句很火的话放到了一套工程框架里：Peter Steinberger 说“你不应该再提示 coding agents，而应该设计提示 agents 的 loop”；Claude Code 负责人 Boris Cherny 也说，他现在不是直接 prompt Claude，而是在写会 prompt Claude、判断下一步怎么做的 loops。

这不是“Prompt Engineering 又换了一个新词”。它真正描述的是一个权力转移：**人类不再一轮一轮扮演调度器、上下文管理员、测试员和 reviewer，而是把这些动作放进一个可重复运行、可观测、可停止、可追责的控制系统里。**

对 QCut、OpenClaw、Hermes、Claude Code、Codex 这类工具来说，这个概念特别关键。因为一旦 Agent 能持续改代码、跑测试、开 PR、读 issue、查日志、发消息，瓶颈就不再是“单次回答够不够聪明”，而是：谁来发现任务？谁来隔离修改？谁来验证成功？失败后怎么重试？什么时候必须把控制权交回人？这些问题的答案，就是 loop engineering。

## 一句话概括

**Loop Engineering 是把“我下一句该怎么 prompt agent”升级成“我该设计什么系统，让 agent 能按目标、按节奏、带验证地持续工作”。**

Addy 的定义很直接：loop engineering 是“替代你自己作为 prompt agent 的那个人”，由系统来提示 agent。这里的 loop 可以理解成一个递归目标：你定义一个目的，AI 系统不断执行、观察、修正，直到目标完成或触发交接条件。

这跟传统 prompt engineering 的差别非常大：

| 层级 | 你设计的对象 | 典型问题 |
|---|---|---|
| Prompt Engineering | 单次指令 | “我该怎么说，模型才会给好答案？” |
| Context Engineering | 上下文窗口 | “我该给模型哪些文件、规范、历史和约束？” |
| Harness Engineering | 单个 Agent 的运行环境 | “Agent 有哪些工具、权限、沙箱、记忆和反馈？” |
| Loop Engineering | 会反复启动和验证 Agent 的系统 | “系统如何发现任务、分配任务、检查结果、记录状态并继续下一步？” |
| Orchestration | 多个 loop / 多个 agent 的组织方式 | “多个并行任务、PR、CI、review、部署如何形成生产线？” |

所以 loop engineering 不是抛弃 prompt，而是把 prompt 从“手工输入”变成“系统生成”。Prompt 仍然存在，只是它被放进了一个更大的运行机制里。

## Addy 提出的五个部件，加上一个外部记忆

Addy 把一个可工作的 loop 拆成五个 primitives，再加一个 state/memory 层：

1. **Automations**：按计划触发的发现、巡检和 triage；
2. **Worktrees**：让并行 agent 在隔离目录和分支里工作，避免互相覆盖；
3. **Skills**：把项目知识、约定、踩坑经验写成 agent 可复用的说明；
4. **Plugins / Connectors**：通过 MCP、API、Slack、Linear、GitHub、数据库等连接真实工具；
5. **Sub-agents**：让构思、实现、验证由不同 agent 承担；
6. **State / Memory**：用 Markdown、Linear、issue、run log 或数据库记录“做过什么、下一步是什么”。

最容易被低估的是第六项。Addy 的一句话很准：**“The agent forgets, the repo doesn't.”** 模型会忘，session 会断，context 会被压缩，但 repo、state file、issue board、run log 不会忘。长期 agent 系统如果没有外部状态，就会在每次启动时重新猜测世界；有了外部状态，loop 才能从“聪明的单次执行”变成“可延续的工程过程”。

## 为什么现在才变重要？因为工具终于把 primitives 做成产品了

一年前，如果你想做这样的 loop，大概率要自己维护一堆脚本：cron、shell、git worktree、CI hook、日志解析、API 调用、PR 创建、Slack 通知、状态文件更新。可用，但脆弱，而且只有写脚本的人懂。

Addy 观察到的变化是：这些能力正在从自制胶水变成 AI coding 产品的原生功能。文章里他把 Codex app 和 Claude Code 做了映射：

| Primitive | 在 loop 中的工作 | Codex app | Claude Code |
|---|---|---|---|
| Automations | 定时发现与 triage | Automations tab、Triage inbox、`/goal` | scheduled tasks、cron、`/loop`、`/goal`、hooks、GitHub Actions |
| Worktrees | 隔离并行修改 | 每个 thread 内建 worktree | `git worktree`、`--worktree`、subagent worktree isolation |
| Skills | 固化项目知识 | `SKILL.md` Agent Skills | `SKILL.md` Agent Skills |
| Connectors | 连接外部工具 | MCP connectors、plugins | MCP servers、plugins |
| Sub-agents | 分离 maker 和 checker | `.codex/agents/` TOML subagents | `.claude/agents/`、agent teams |
| State | 记录进度 | Markdown、Linear、Memory | Markdown、`AGENTS.md`、Linear/MCP、memory |

这说明 loop engineering 不是某个工具的私有能力，而是一种跨工具的架构形状。工具名会变，但这些 primitives 大概率会稳定下来：触发、隔离、技能、连接器、子代理、状态、验证、停止条件。

## `/loop` 和 `/goal` 的区别：一个是节拍器，一个是完成契约

文章里一个很实用的区分是：`/loop` 和 `/goal` 不是同一个东西。

- **`/loop` 更像节拍器**：每隔一段时间重新运行某个任务，比如每小时检查 CI、每天总结 issue、定时扫描最近改动。
- **`/goal` 更像完成契约**：给 agent 一个可验证目标，让它跨多轮持续工作，直到条件成立，例如“`test/auth` 全部通过且 lint clean”。

真正的工程价值在后者。因为 AI agent 最容易出问题的地方不是“不会开始”，而是“不会可靠地停”。如果没有明确 stopping condition，loop 会在两种坏状态之间摇摆：要么过早宣布完成，要么无限重试烧 token。

所以一个好的 `/goal` 不是“把 auth 修好”，而应该像这样：

```text
目标：修复 auth 模块中最近引入的 session refresh bug。
成功条件：
1. `pnpm test test/auth/session-refresh.test.ts` 通过；
2. `pnpm lint --filter auth` 通过；
3. 不修改 public API，除非在 PR 描述里解释原因；
4. 如果三次尝试后仍失败，把失败日志和假设写入 `loop-run-log.md` 并停止。
```

这才是 loop engineering 的味道：目标、验证、边界、停止、交接，全都写清楚。

## Worktree 是 Agent 并行的地基

只要多个 agent 同时改同一个 repo，最先坏掉的通常不是模型能力，而是文件冲突。两个 agent 同时改同一组文件，就像两个工程师同时在同一个 checkout 上 commit，没有任何协调。

`git worktree` 的意义在这里被放大了：它不是 Git 的高级技巧，而是 agent factory 的安全地基。每个 agent 得到一个独立 checkout、独立 branch、独立测试环境，失败也只污染自己的工作区。

但 worktree 只能解决机械冲突，不能解决产品判断。Addy 提到的 “orchestration tax” 在这里非常真实：你可以同时跑十个 agent，但你不一定能 review 十个 PR。**并行能力会把瓶颈从“生成代码”转移到“人类审核、集成和决策”。** 如果这个瓶颈不设计好，更多 agent 只会制造更多待审核垃圾。

## Skills 是把“项目意图”从人脑搬到系统里

在单次聊天里，项目约定可以靠人类临时补充：不要改这个目录、测试要这么跑、这个 API 有历史包袱、UI 风格要跟某个组件一致。但 loop 是无人值守的，不能指望每次运行时都有一个人补充上下文。

所以 skills 是 loop 的“长期意图层”。它把项目知识写进 `SKILL.md`、references、scripts、templates 里，让 agent 每次运行时读到同一套约束。比如：

- 代码风格和目录边界；
- 常用测试命令；
- 架构禁区；
- 发布流程；
- review checklist；
- 曾经踩过的坑。

这也是为什么 Peter 做 Hermes / QCut 时，skill 不是“提示词收藏夹”，而更像团队操作手册。没有 skill 的 loop 会每次重新推断项目；有 skill 的 loop 才能复利。

## Sub-agent 的价值：把写代码的人和判卷的人分开

Addy 强调 sub-agents，一个核心原因是：写代码的 agent 不应该独自判定自己是否完成。模型很容易对自己的输出过度友好，尤其是在已经花了很多轮尝试之后。

更合理的结构是：

1. 一个 explorer 读代码、定位问题、提出方案；
2. 一个 implementer 修改代码；
3. 一个 verifier 只看 spec、diff、测试和日志，负责挑错；
4. 必要时再由 human reviewer 处理 verifier 不能判断的产品取舍。

这就是 maker-checker split。它会多花 token，但在无人值守 loop 里很值得，因为它决定了“完成”这个词有没有可信度。

## 一个真实可落地的 loop 长什么样？

把这些部件拼起来，一个软件团队可以从很小的 loop 开始：

1. 每天早上 automation 启动；
2. 它读取昨天的 CI failure、open issues、最近 commits；
3. 调用 triage skill，把可处理项写入 `loop-state.md`；
4. 对每个小任务开一个 worktree；
5. implementer agent 尝试修复；
6. verifier agent 根据测试、lint、diff 和 skill checklist 审核；
7. 通过则开 PR 并更新 Linear/GitHub issue；
8. 不确定或失败则写入 triage inbox，等待人类处理；
9. 下一次运行从 state file 继续，而不是重新开始。

这不是科幻，也不需要一个“超级智能体”。它更像 CI/CD 的下一层：CI/CD 自动化构建、测试、部署；loop engineering 自动化发现、修复、验证和交接。

## 对 QCut / OpenClaw / Hermes 的启发

这篇文章对 Peter 现在做的几条线都很直接：

- **QCut**：视频生成 pipeline 本身就是 loop：脚本、素材、镜头、音频、字幕、预览、导出、失败重试。真正难的是把每一步的成功条件和可回滚状态设计出来，而不是写一个“生成视频”的大 prompt。
- **OpenClaw**：多 agent coding 的价值不只是同时开很多 Codex，而是给每个 agent 明确 worktree、budget、scope、reviewer 和 stop condition。
- **Hermes**：cronjob、skills、memory、toolsets、Discord delivery 本质上已经是一个 loop runtime。关键是让每个 job 有外部状态、验证和失败上报，而不是只“定时叫一次模型”。
- **文章自动化**：从 X 链接写文章也可以被 loop 化：解析源、找 canonical、保存媒体、写双语、更新 README/MOC、commit/push、验证 GitHub 链接。这就是一个非常具体的 content loop。

换句话说，loop engineering 不是只给 coding agent 用的。任何“AI 需要重复处理任务、检查结果、记录状态、继续下一步”的工作流，都可以用这个框架重新设计。

## 最危险的误解：loop 不是自动驾驶，而是可审计的半自动工程系统

Addy 最重要的警告不是“loop 很强”，而是“loop 会让错误更快发生”。他提到三个风险：

1. **Verification 仍然是你的责任**：无人值守 loop 也可能无人值守地犯错；
2. **Comprehension debt 会增长**：agent 写得越快，人理解系统的速度可能越跟不上；
3. **Cognitive surrender 很危险**：如果人类只是按下开始然后接受结果，loop 会变成逃避思考的工具。

这点非常关键。好的 loop 不是让工程师退出，而是让工程师从“每轮手工推动”升级成“设计控制系统、定义验收标准、处理例外、审核关键决策”。

如果一个团队没有测试、没有日志、没有权限边界、没有 state、没有 review，只是让 agent 每小时自动改代码，那不是 loop engineering，而是自动化事故生成器。

## 我的判断：Prompt 会继续存在，但 leverage 已经上移

Prompt engineering 不会消失。你仍然需要写清楚目标、约束、上下文和评价标准。但高杠杆的位置已经从“这一句 prompt 写得多漂亮”转移到“这个系统能不能持续产出可验证结果”。

未来真正有价值的 AI 工程能力，可能会更像下面这些问题：

- 哪些任务适合进入 loop，哪些必须人工处理？
- 每个 loop 的成功条件是什么？
- 失败几次后停止？
- 状态写在哪里？
- 谁有权限改什么？
- verifier 怎么独立于 maker？
- token budget 和时间 budget 怎么设？
- 结果如何进入 PR、issue、文档或用户可见产品？

Addy 的结尾很像一句原则：**Build the loop. Stay the engineer.**

这也是我觉得 loop engineering 最值得被认真对待的原因。它不是“让 AI 替你工作”的口号，而是提醒我们：当 Agent 可以持续行动时，工程师真正要设计的，是让行动可控、可查、可停、可恢复的系统。
