# gstack 深度拆解：Office Hours + CEO Review — YC 掌门人的 AI 产品思维工具链

> **TL;DR:** Garry Tan（YC CEO）开源了 gstack，一套把 Claude Code 变成虚拟工程团队的 Skill 系统。本文聚焦其中两个最核心的"思考型" Skill：`/office-hours`（产品诊断）和 `/plan-ceo-review`（CEO 级方案审查）。它们不写一行代码，但决定了你接下来写的每一行代码是否值得写。

**源码：** [donghaozhang/gstack](https://github.com/donghaozhang/gstack) (fork of garrytan/gstack)

---

## 背景：一个人日产 10,000-20,000 行代码

Garry Tan 在 README 里写了一个让人瞠目的数字：过去 60 天，他写了**超过 60 万行生产代码**，其中 35% 是测试。他一边当 YC CEO，一边每天产出 10K-20K 行可用代码。

秘密不是他更努力了，而是他把 Claude Code 变成了一个**18 人虚拟团队**——CEO、工程经理、设计师、QA、发布工程师……全部用 Markdown Skill 文件定义，全部免费开源。

gstack 的核心理念叫 **"Boil the Lake"**（把湖水煮沸）：AI 让完整实现的边际成本趋近于零，所以永远选完整方案，别走捷径。

---

## `/office-hours`：写代码之前的六个致命问题

这个 Skill 模拟 YC Office Hours，核心目标是：**确保你理解了问题，再谈方案**。

### 两种模式

| 模式 | 适用场景 | 风格 |
|------|---------|------|
| **Startup Mode** | 创业 / 内部创业 | 硬核诊断，不留情面 |
| **Builder Mode** | Hackathon / 开源 / 学习 / Side Project | 热情协作，设计思维 |

### Startup Mode 的六个逼问（Forcing Questions）

根据产品阶段智能路由——不是每次都问全部六个：

- **Pre-product（纯想法）→** Q1 需求真实性、Q2 现状竞品、Q3 极致具体性
- **有用户 →** Q2 现状竞品、Q4 最窄楔子、Q5 观察洞见
- **有付费客户 →** Q4 最窄楔子、Q5 观察洞见、Q6 未来适配

**Q1 — 需求真实性（Demand Reality）**

> "你有什么最强的证据证明有人真的想要这个——不是'感兴趣'，不是'注册了候补名单'，而是如果它明天消失，会真的不高兴？"

红旗 🚩：
- "大家都说很有意思" — 感兴趣是免费的
- "候补名单有 500 人" — 注册不是需求
- "VC 都看好这个赛道" — 那每个竞品都能说

**Q2 — 现状是你的真正竞争对手**

不是别的创业公司，不是大公司，而是用户目前用 Excel + Slack 消息拼凑出来的那套破烂方案。如果"什么都不做"就是现状，通常说明问题还不够痛。

**Q3 — 极致具体性**

"企业客户"不是客户。你需要：一个名字、一个角色、一家公司、一个原因。

**Q4 — 最窄楔子**

> "这周有人愿意付钱买的最小版本是什么？"

如果没人能从更小的版本中获得价值，通常说明价值主张本身还不清晰——不是产品需要更大。

### 反谄媚规则

这是我见过的**最严格的 anti-sycophancy 指令**：

❌ 永远不要说：
- "That's an interesting approach" — 给出你的立场
- "You might want to consider..." — 直接说"这是错的，因为..."
- "That could work" — 说它"会"还是"不会"work，以及缺什么证据

✅ 必须做：
- 对每个回答**表明立场**
- 说明什么证据会改变你的立场
- 挑战创始人主张的**最强版本**，不要打稻草人

### 输出

不写代码。只输出一份**设计文档**，自动保存到 `~/.gstack/projects/` 下，供后续 `/plan-ceo-review` 读取。

---

## `/plan-ceo-review`：CEO 级方案审查

拿到设计文档后，这个 Skill 进入 **Mega Plan Review Mode**——用 CEO 思维审视整个方案。

### 四种审查模式

| 模式 | 姿态 | 关键词 |
|------|------|--------|
| **SCOPE EXPANSION** | 造教堂。想象柏拉图理想型。 | "10x better for 2x effort" |
| **SELECTIVE EXPANSION** | 守住范围，逐个评估扩展机会 | Cherry-pick |
| **HOLD SCOPE** | 纯防御。找每个失败模式 | Bulletproof |
| **SCOPE REDUCTION** | 外科手术。砍到最小可行 | Ruthless |

关键规则：**用户 100% 控制权**。每个范围变更都是显式的 opt-in，不能偷偷加减。

### 九条 Prime Directives

1. **零静默失败** — 每个失败模式必须可见
2. **每个错误有名字** — 不能说"处理错误"，要说具体的异常类、触发条件、捕获方式、用户看到什么
3. **数据流有暗影路径** — 每个数据流有 4 条路：正常、nil 输入、空输入、上游错误
4. **交互有边缘情况** — 双击、中途导航、慢连接、过期状态、返回按钮
5. **可观测性是范围** — Dashboard、告警、Runbook 是一等交付物
6. **图表是强制的** — 每个非平凡流程都要 ASCII 图
7. **延期的事必须写下来** — 模糊意图是谎言，TODOS.md 或不存在
8. **为 6 个月后优化** — 如果今天的方案是下季度的噩梦，直说
9. **允许说"全部推翻"** — 有根本更好的方案就说

### 18 条 CEO 认知模式

这是整个 gstack 里**信息密度最高的部分**。摘几条核心的：

- **Bezos 双向门** — 大多数决策可逆，快速行动。不可逆 + 重大的才慢下来
- **Munger 逆向思维** — 问完"怎么赢"，再问"什么会让我们失败"
- **Jobs 聚焦减法** — 从 350 个产品砍到 10 个。默认：做更少的事，做更好
- **70% 信息就够决策** — 等到 90% 你已经慢了
- **Ben Horowitz 战时意识** — 正确诊断和平期 vs 战争期，和平期的习惯会杀死战争期的公司
- **Altman 杠杆执念** — 找到小投入大产出的杠杆点。技术是终极杠杆

### 完整性原则（Completeness Principle）

| 任务类型 | 人类团队 | CC+gstack | 压缩比 |
|---------|---------|-----------|--------|
| 脚手架/样板 | 2 天 | 15 分钟 | ~100x |
| 写测试 | 1 天 | 15 分钟 | ~50x |
| 功能实现 | 1 周 | 30 分钟 | ~30x |
| Bug 修复 + 回归测试 | 4 小时 | 15 分钟 | ~20x |
| 架构设计 | 2 天 | 4 小时 | ~5x |
| 调研探索 | 1 天 | 3 小时 | ~3x |

核心论点：**"够好了"在 AI 时代是错误直觉**。当"完整"只多花几分钟时，永远选完整。

---

## 整个冲刺流程

```
/office-hours → 设计文档
      ↓
/plan-ceo-review → CEO 审查（范围、野心、认知偏差）
      ↓
/plan-eng-review → 工程审查（架构图、测试矩阵、失败模式）
      ↓
实现代码（AI 写，你审）
      ↓
/review → 自动修 + 人工确认
      ↓
/qa → 真实浏览器点击测试
      ↓
/ship → 测试 + PR
```

一个人，一个功能冲刺，约 30 分钟。但关键是：**你可以并行跑 10-15 个冲刺**。不同功能、不同分支、不同 Agent。

---

## 对 Builder 的启示

1. **先诊断，再开刀。** `/office-hours` 的六个逼问可以直接拿来用——不需要 gstack，不需要 Claude Code。下次有人跟你说"我有个 idea"，试试用这六个问题问他。

2. **反谄媚是可以工程化的。** gstack 用 Markdown 指令禁止了特定的谄媚短语，并要求 AI 对每个回答表明立场。这个模式可以复制到任何 AI 工作流。

3. **"Boil the Lake" 改变了决策框架。** 当 AI 让完整实现只多花 5 分钟时，"先做 MVP 再迭代"的老思路需要重新校准。不是说 MVP 不对，而是 MVP 的粒度变了。

4. **CEO 认知模式是通用的。** 那 18 条认知模式不只适用于代码审查——产品决策、招聘、融资、战略规划，全部适用。

---

## 相关链接

- **gstack 源码：** <https://github.com/donghaozhang/gstack>
- **office-hours SKILL.md：** <https://github.com/donghaozhang/gstack/blob/main/office-hours/SKILL.md>
- **plan-ceo-review SKILL.md：** <https://github.com/donghaozhang/gstack/blob/main/plan-ceo-review/SKILL.md>
- **Garry Tan "Boil the Ocean" 文章：** <https://garryslist.org/posts/boil-the-ocean>

---

*写于 2026-03-23 | 源自 gstack office-hours + plan-ceo-review 两个 Skill 的完整拆解*

🦞
