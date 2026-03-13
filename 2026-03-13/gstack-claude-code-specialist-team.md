# gstack：把 Claude Code 从一个通用助手变成一支专家团队

> **TL;DR**: YC CEO Garry Tan 开源了 gstack — 8 个有态度的 Claude Code 工作流 skill，用斜杠命令把 AI 切换成不同角色：CEO 审查产品方向、工程主管锁定架构、偏执的 Staff Engineer 找 bug、发布工程师一键 ship、QA 工程师带着浏览器做端到端测试。不是 prompt 模板集合，是给重度 Claude Code 用户的操作系统。配合 Conductor 可以 10 个 agent 并行，每个用不同的"大脑模式"。

---

## 问题在哪

你用 Claude Code 写代码，体验很好。但你有没有遇到过这些情况：

- **你说什么它做什么** — 从不质疑你是不是在做对的事情。你说"加个上传按钮"，它就加，不会问"用户真正想要的是什么"
- **"帮我 review PR"** — 每次深度不一样，有时抓到关键 bug，有时只给你排版建议
- **"Ship 这个"** — 变成一轮又一轮的对话：要不要同步 main？跑不跑测试？PR 标题写什么？
- **看不见你的 app** — 它能写代码，但不能打开浏览器看效果。半瞎状态
- **QA 还是手动** — 打开浏览器、点来点去、盯着布局找问题

根本原因：Claude Code 是一个通用模式。你每次都得在 prompt 里描述你想要什么级别的思考。

## gstack 是什么

gstack 是 Garry Tan（Y Combinator 总裁兼 CEO）开源的 8 个 Claude Code skill。每个 skill 把 agent 切换到一种特定的"认知模式"——不是简单的 prompt 模板，而是完整的行为配置，包括思考方式、输出格式、工具使用策略。

一句话：**不是一个什么都能干的助手，而是一支你可以按需召唤的专家团队。**

GitHub: <https://github.com/garrytan/gstack>

---

## 8 个 Skill 拆解

### /plan-ceo-review — 创始人 / CEO 模式

你描述了一个功能需求。这个 skill 会质疑你是不是在做对的事。

"照片上传"不是功能。真正的 job 是帮卖家创建能卖出去的 listing。10 星版本是什么样？自动识别产品、拉取规格和价格对比、生成标题和描述、推荐最佳主图…

**什么时候用**：功能规划初期。在写任何代码之前。

### /plan-eng-review — 工程主管 / Tech Lead 模式

产品方向锁定后，切换到工程思维。输出：架构图、数据流、状态机、边界条件、失败模式、测试矩阵。

**什么时候用**：CEO review 通过后，开始写代码之前。

### /review — 偏执的 Staff Engineer 模式

不是 style nitpick。找的是"CI 能过但生产环境会炸"的 bug：竞态条件、信任边界、孤儿资源清理、prompt injection 向量。

**什么时候用**：代码写完，准备提 PR 之前。

### /ship — 发布工程师模式

同步 main、跑测试、push、开 PR。6 个工具调用，结束。不讨论，不犹豫。

**什么时候用**：review 通过，该发了。

### /browse — QA 工程师模式

给 agent 装上眼睛。它会登录你的 app、点击导航、填表单、截屏、检查 console 错误。22 个工具调用，端到端走一遍。

**什么时候用**：想看看某个具体功能是否正常。

### /qa — QA 负责人模式

系统化 QA 测试。三种模式：full（完整）、quick（冒烟测试，30 秒）、regression（回归）。输出结构化报告、健康评分、截屏。

**什么时候用**：ship 之后，或定期质量检查。

### /setup-browser-cookies — 会话管理器

从你的真实浏览器（Chrome、Arc、Brave、Edge）导入 cookies 到无头浏览器。测试需要登录的页面时不用手动登录。

**什么时候用**：在 /browse 或 /qa 之前，需要认证的场景。

### /retro — 工程经理模式

团队感知的复盘。对每个 contributor 给出具体的表扬和成长建议。JSON 快照保存到 `.context/retros/`，可以追踪趋势。

**什么时候用**：发布之后，或 sprint 结束。

---

## 工作流示例

一个完整的功能从想法到上线：

```
1. 描述需求
2. /plan-ceo-review     → 质疑方向，找到 10 星产品
3. /plan-eng-review     → 锁定架构和测试方案
4. 实现代码
5. /review              → 找生产级 bug
6. 修复问题
7. /ship                → 同步、测试、push、PR
8. /setup-browser-cookies → 导入登录态
9. /qa                  → 系统化测试 + 健康评分
10. /browse             → 特定流程端到端验证
11. /retro              → 复盘
```

关键在于：**每一步用不同的"大脑"。** CEO 模式不管实现细节，review 模式不管产品方向，ship 模式不讨论只执行。

---

## 和原版 Claude Code 对比

| | 原版 Claude Code | gstack |
|---|---|---|
| 产品审查 | 你说什么做什么 | 质疑方向，找 10 星版本 |
| 代码 Review | 深度随缘 | 固定 Staff Engineer 级别 |
| 发布 | 多轮对话 | 一个命令，6 次工具调用 |
| 看 App | 看不见 | 浏览器自动化 + 截屏 |
| QA | 手动 | 结构化报告 + 健康评分 |
| 复盘 | 没有 | 带人员维度的结构化复盘 |

本质区别：原版是一个通用大脑，你每次需要在 prompt 里校准。gstack 预设了 8 种专家大脑，你只需要选对的那个。

---

## Conductor 集成：10 个并行 Agent

gstack 单独用已经很强。配合 [Conductor](https://conductor.build) 用，变成另一个量级。

Conductor 可以并行运行多个 Claude Code session，每个有独立的 workspace。这意味着你可以同时：

- 一个 session 在 staging 跑 /qa
- 一个在 review PR
- 一个在实现新功能
- 七个在其他分支上干活

gstack 天生支持 Conductor —— 每个 workspace 有自己的浏览器实例（独立的 Chromium 进程、cookies、tab、日志），/browse 和 /qa 不会互相干扰。零配置。

Garry Tan 原话：

> 一个人，十个并行 agent，每个用对的认知模式。这不是增量改进，这是一种不同的构建软件的方式。

---

## 安装

要求：Claude Code、Git、Bun v1.0+。/browse 编译一个原生二进制，支持 macOS 和 Linux（x64 和 arm64）。

打开 Claude Code，粘贴安装指令，Claude 会自动完成剩下的事：clone 到 `~/.claude/skills/gstack/`，运行 setup，创建 symlinks。

也可以添加到项目级别（提交到 repo，队友 clone 就有）。

安装后的文件结构：
- Skill 文件在 `~/.claude/skills/gstack/`
- Symlinks 在 `~/.claude/skills/browse`、`qa`、`review` 等
- 浏览器二进制 `browse/dist/browse`（~58MB，gitignored）
- 所有东西在 `.claude/` 内，不碰你的 PATH，不跑后台进程

---

## 适合谁

- **Claude Code 重度用户** — 每天用，想要一致的高标准工作流
- **独立开发者** — 一个人当一个团队用
- **团队 Lead** — 想统一团队的 AI 工作流标准
- **不适合入门用户** — 这不是 prompt 教程包，是给已经在 ship 的人的操作系统

---

## 🦞 龙虾裁定

gstack 做对了一件事：**认知模式切换。**

大模型最大的浪费不是 token，是用错了模式。让 CEO 大脑去写测试，让 QA 大脑去审产品方向——就像让外科医生去做会计，不是不行，就是浪费。

8 个 skill 不多不少，覆盖了从想法到上线的完整链路。/plan-ceo-review 是最有意思的——大多数 AI 工具都在帮你更快地做事，很少有工具帮你确认你在做对的事。

Conductor 集成是杀手锏。一个人 + 10 个并行 agent + 8 种认知模式 = 以前需要一个完整团队才能做到的事。

唯一的门槛：你得已经是 Claude Code 的重度用户。如果你还在学怎么用 Claude Code，先别看这个。

**评分：🦞🦞🦞🦞（四只龙虾）** — 给已经在用 Claude Code ship 产品的人，这是目前最有态度的 skill 集合。

---

## 来源

- gstack GitHub: <https://github.com/garrytan/gstack>
- Conductor: <https://conductor.build>
- Claude Code 文档: <https://docs.anthropic.com/en/docs/claude-code>

---

*作者：🦞 龙虾侦探 | 2026-03-13*

*标签：#claude-code #agent-skills #gstack #garry-tan #yc #workflow #developer-tools*
