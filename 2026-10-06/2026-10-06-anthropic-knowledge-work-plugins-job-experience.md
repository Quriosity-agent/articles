---
title: "岗位经验被写进 Markdown：Anthropic Knowledge Work Plugins 开源了什么，又没有开源什么"
date: 2026-10-06
source: "https://x.com/denziideng/status/2107252757698908360"
canonical: "https://x.com/denziideng/status/2107252757698908360"
related_project: "https://github.com/anthropics/knowledge-work-plugins"
tags:
  - Anthropic
  - Claude Cowork
  - Knowledge Work Plugins
  - Agent Skills
  - MCP
  - Future of Work
  - Open Source
  - Source Audit
---

# 岗位经验被写进 Markdown：Anthropic Knowledge Work Plugins 开源了什么，又没有开源什么

> **一句话结论：** Denzii 的 X 帖抓住了一个真实变化：过去藏在个人笔记、师徒传授和团队习惯里的显性流程，正在被写成 Agent 可执行的 Skill。但“岗位经验被完整开源”仍然说得太满。Anthropic 开源的是通用工作流、检查表、输出模板和连接器声明，不是公司的私有数据、权限、例外处理、专业判断与责任承担。更准确地说，岗位知识没有被一次性下载，岗位里的 **可程序化部分** 开始变成公共基础设施。

- **原帖：** [Denzii：2026 年，“岗位经验”首次被官方开源了](https://x.com/denziideng/status/2107252757698908360)
- **发布时间：** 2026-10-06
- **官方仓库：** [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
- **审计快照：** [`8444efc`](https://github.com/anthropics/knowledge-work-plugins/tree/8444efcd48f7012f09797778a36a33e73d0861f4)，即原帖发布前仓库最新 commit
- **检查时间：** 2026-10-09

![原帖使用的 GitHub 仓库截图](imgs/anthropic-knowledge-work-plugins-job-experience/source-post.jpg)

## 01｜这条帖子的直觉是对的，结论却需要拆开

原帖把冲突讲得很直接：有人看到销售、法务、财务、产品、市场、客服与数据插件，会觉得终于可以少踩坑；也有人担心自己最值钱的 know-how 已经变成 Claude 可以随时读取的 Markdown。

这种不安并非空穴来风。以往一项岗位经验想跨团队传播，往往要经过培训、旁听、模板积累和多轮复盘。现在，一份 `SKILL.md` 可以同时写下触发条件、步骤、工具选择、输出格式、异常分支与验收标准。模型不必亲历某家公司过去十年的错误，也能先继承一套经过整理的起步方法。

但“会按步骤做”与“已经成为这个岗位的专家”之间仍有很长距离。前者可以进入仓库，后者还依赖组织上下文、实时数据、对模糊局面的判断，以及对结果承担责任的人。

## 02｜先校准数字：11、17 和 123 说的是三件事

原帖引用了“11 个岗位插件”。这个数字有官方依据：Anthropic 回顾 2026 年 1 月 Cowork 发布时，明确称其包含 11 个开源插件；仓库 README 至今也列出 productivity、sales、customer-support、product-management、marketing、legal、finance、data、enterprise-search、bio-research 与 cowork-plugin-management 这 11 个首发项目。

不过，原帖截图与发帖当天的仓库已经比这更大。我们固定到当时最新的 `8444efc` 后得到：

| 口径 | 数量 | 它代表什么 |
|---|---:|---|
| 官方首发清单 | 11 | README 明确介绍的首批 Anthropic 插件 |
| 仓库本地一方插件目录 | 17 | 在首发清单外还包括 design、engineering、human-resources、operations、pdf-viewer 与 small-business |
| 一方插件中的 `SKILL.md` | 181 | 各岗位拆出的具体流程，其中 sales 有 36 个，small-business 有 44 个 |
| Marketplace manifest 条目 | 123 | 一方、合作方与远程 Git 子目录的市场清单，不等于 123 个 Anthropic 岗位插件 |

所以“11 个”是首发口径，不是发帖时仓库全部内容；“123 个”又是市场条目数，不能反过来写成 123 个官方岗位。数字只有连同统计边界才有意义。

原帖截图中的 26.1k stars 与正文“26k+”相符。到本文检查时仓库已超过 27k stars，但 star 只能说明关注度，不能证明插件覆盖了某个岗位的全部经验。

## 03｜一个岗位插件到底由什么组成

README 给出的基础结构很简单：

```text
plugin-name/
├── .claude-plugin/plugin.json   # 插件身份与元数据
├── .mcp.json                    # 外部工具连接声明
├── commands/                    # 用户显式调用的命令
└── skills/                      # 按任务触发的岗位工作流
```

这四层分别回答“它是谁”“能访问什么”“用户怎样点名调用”以及“真正应该怎样做”。对大多数通用岗位插件而言，核心知识确实主要写在 Markdown 与 JSON 中。仓库也包含少量 Python、HTML 等辅助文件，尤其是生物研究和数据打包流程，因此“全部只是 Markdown”是一个有用的概括，但不是对整个仓库文件类型的字面描述。

![岗位插件不是下载来的员工，而是公开流程、组织配置与受控执行组成的工作栈](imgs/anthropic-knowledge-work-plugins-job-experience/plugin-stack.svg)

插件也不是一个新模型。它不会重新训练 Claude，而是在合适任务出现时加载特定流程，并声明可能需要的连接器。模型仍负责理解与生成，Skill 约束做事顺序，MCP 把它接到真实系统。

## 04｜这些 Markdown 不是空泛提示词，而是可执行 SOP

真正值得重视的是文件的细度。

销售插件的 `call-prep` 不只写“帮我准备客户会议”。它要求先确认日历与 CRM 的可用范围，再查账户、机会阶段、联系人、通话转录、邮件和内部聊天；每个值要引用来源，空字段要区分“确实为空”与“没有查询”，最后生成会议目标、发现问题、可能异议和承诺事项。

法务插件的 `review-contract` 要先确认用户代表哪一方、截止时间和关注点，再加载公司谈判 playbook；若没有公司标准，必须明确告诉用户只能按通用商业标准分析。它逐项检查责任限制、赔偿、知识产权、数据保护、终止、争议解决等条款，并把偏差分为绿色、黄色与红色。文件还明确声明，结果不能替代合格法律专业人士复核。

财务插件把 reconciliation、journal entry、close management、SOX testing 与 variance analysis 分开；数据插件则把 SQL、探索、统计分析、可视化与数据验证拆开，并专门提醒平均数的平均数、时区错位、选择偏差、辛普森悖论和把相关性写成因果等常见陷阱。

这些内容已经超出“一段万能 Prompt”。它更像一本可以被机器执行、被团队 fork、被代码审查的岗位手册。

## 05｜连接器清单不等于数据已经接通

原帖说插件“附赠全套工具连接器”，这句话需要加限定。

在固定快照的 17 个一方插件中，`.mcp.json` 一共声明 174 个连接器引用，去重后涉及 86 个名称。但这些引用大量重复于不同岗位，且有 31 项 URL 为空，例如部分 Google Calendar、Gmail、Google Drive、Snowflake 与 Databricks 配置。其余连接器即使写有 MCP 地址，也仍然需要相应服务账号、OAuth、组织授权、管理员策略与数据权限。

换句话说，仓库开放的是 **工具地图**，不是你公司的工具访问权。安装 sales 插件不会自动获得 Salesforce 里的客户数据；安装 legal 插件也不会自动拥有 Box 合同库或 DocuSign 的签署权限。

官方产品文档还说明，插件功能目前面向 Claude 付费方案。仓库代码采用 Apache-2.0 许可证，不等于 Claude 运行环境、第三方 SaaS 账户和外部数据都是免费的。

## 06｜真正没有被开源的，是这四层

![岗位知识中哪些部分容易复制，哪些仍然必须留在组织与责任人手中](imgs/anthropic-knowledge-work-plugins-job-experience/knowledge-boundary.svg)

**第一，公司自己的标准。** 通用合同审查可以列出条款类别，却不知道你公司的责任上限、可接受回退位置和必须升级给总法律顾问的红线。通用 PRD 模板也不知道产品真实战略与技术债。

**第二，实时上下文。** 客户最近说了什么、这个季度预算还剩多少、数据仓库表结构怎样、某个候选人处于什么阶段，都不在公开仓库里。没有这些信息，插件只能给出结构正确但业务上空心的结果。

**第三，例外判断。** SOP 擅长覆盖常见路径，真正昂贵的经验经常发生在条件冲突时：该不该为战略客户放宽条款、异常数据是错误还是新信号、什么时候应该停止自动化并升级给人。

**第四，责任。** 模型可以起草分录、合同红线或客户回复，但不能替组织承担审计、监管、声誉与关系后果。权力、签字和责任并不会因为流程文件开源而自动转移。

## 07｜被压缩的不是“岗位”，而是岗位中的显性流程溢价

以前，一个人可能因为记得所有步骤、模板位置和系统入口而形成信息壁垒。插件把这些显性程序写进公共文件后，这部分价值会快速下降。团队不必再反复解释怎样准备销售电话、怎样写 PRD、怎样组织月结证据包。

但这不等于所有人的价值同时归零。岗位价值会向另外几件事迁移：

- 把通用 Skill 改造成公司真实流程；
- 判断输出是否遗漏关键风险；
- 设计权限、审计与人工审批边界；
- 处理文档没有覆盖的例外；
- 对最终决策和关系结果负责；
- 把新经验持续回写成团队可复用的资产。

初级岗位最机械的整理与首稿工作会先被压缩；中层专业人员会从“亲手完成每一步”转向“配置、复核与处理例外”；资深人员的隐性判断不会自动消失，但如果始终不把它变成可传承的制度，也更容易成为组织瓶颈。

## 08｜这次开源真正改变的是组织知识的载体

过去的 SOP 通常是静态文档。人要读完、记住，再进入多个系统执行。Knowledge Work Plugins 把说明书变成了运行时的一部分：任务触发后，Agent 可以按步骤读数据、生成中间产物、发现缺口，并在权限允许时执行动作。

这使组织知识第一次更接近“可执行配置”：

| 旧载体 | 插件化之后 |
|---|---|
| Wiki 里的操作说明 | 会在相关任务中自动加载的 Skill |
| 文档里的工具链接 | `.mcp.json` 中声明的连接器 |
| 老员工口头提醒 | 写进流程的缺失值、引用与升级规则 |
| 靠主管抽查质量 | 输出模板、证据要求与人工审批点 |
| 培训后各自发挥 | 可版本控制、fork、diff 和回滚的团队标准 |

这比“多了 11 个提示词包”重要得多。它把一部分管理制度从培训材料变成了 Agent 的执行接口。

## 09｜团队怎样正确采用，而不是直接安装后许愿

一个稳妥的落地顺序可以分成五步：

1. **选一个高频、低风险、输出容易验收的流程。** 比如会议准备、周报或初步数据检查，不要先从自动签合同和自动过账开始。
2. **把公开 Skill 当基线。** 标记其中哪些字段、阶段名称、阈值和输出格式与公司实际不符。
3. **补组织层。** 加入自己的术语、模板、playbook、升级规则和允许使用的数据源。
4. **按最小权限连接工具。** 先读后写，区分草稿、建议动作与真正执行，并保留日志。
5. **用真实历史案例做回归。** 不只看一次演示是否漂亮，还要检查遗漏、幻觉、权限错误与边界案例，然后把修订写回 Skill。

插件最适合成为“团队标准的可执行版本”，而不是绕过团队标准的捷径。

## 10｜四个不能被热度掩盖的限制

**其一，仓库热度不是岗位覆盖率。** 26k 或 27k stars 不能证明某个插件掌握了完整专业知识，也不能替代独立效果评估。

**其二，高风险工作仍需合格复核。** 法务文件自己写明不构成法律意见；财务、HR、合规和生物研究同样需要专业人员、组织政策与适用法规共同约束。

**其三，连接外部系统会扩大攻击面。** 邮件、聊天、转录与外部文档都可能包含恶意指令。值得肯定的是，新版 sales Skill 已明确把这些内容视为不可信数据，但每家公司仍要验证权限、提示注入防护与写操作审批。

**其四，开源模板会老化。** SaaS API、内部流程、法规和市场阶段都会变化。一个半年不维护的岗位插件，可能比没有插件更危险，因为它会以一致而自信的方式重复过时步骤。

## 结论

Denzii 的帖子之所以引起共鸣，不是因为 11 这个数字，而是因为它点破了知识工作的一个新事实：只要经验能被明确写成步骤、工具调用、检查表和输出契约，它就很可能被打包、共享并由 Agent 执行。

但 Anthropic 没有把一个销售、律师、财务或产品经理完整上传到 GitHub。它开放的是这些岗位的公共骨架。血肉仍来自公司的数据、制度、关系、专业判断和责任体系。

所以真正值得担心的不是“我的经验还能撑几年”，而是另一个问题：**我的价值有多少只是记住流程，又有多少来自配置流程、判断例外和承担结果？** 前一部分正在快速商品化；后一部分会成为人与组织新的竞争力。

## 主要来源

1. [Denzii 的原始 X 帖](https://x.com/denziideng/status/2107252757698908360)
2. [Anthropic Knowledge Work Plugins 仓库](https://github.com/anthropics/knowledge-work-plugins)
3. [原帖发布时的仓库快照 8444efc](https://github.com/anthropics/knowledge-work-plugins/tree/8444efcd48f7012f09797778a36a33e73d0861f4)
4. [官方 README：首发 11 个插件与目录结构](https://github.com/anthropics/knowledge-work-plugins/blob/8444efcd48f7012f09797778a36a33e73d0861f4/README.md)
5. [Sales call-prep Skill](https://github.com/anthropics/knowledge-work-plugins/blob/8444efcd48f7012f09797778a36a33e73d0861f4/sales/skills/call-prep/SKILL.md)
6. [Legal contract-review Skill](https://github.com/anthropics/knowledge-work-plugins/blob/8444efcd48f7012f09797778a36a33e73d0861f4/legal/skills/review-contract/SKILL.md)
7. [Claude Cowork 插件官方指南](https://claude.com/resources/guides/claude-cowork-product-guide/extending-claude-cowork-with-plugins)
8. [Anthropic 官方插件定制教程](https://academy.claude.com/tutorials/how-to-customize-plugins-in-cowork)
9. [Claude 插件方案与安全说明](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
10. [Anthropic 对 Cowork 首发 11 个开源插件的官方回顾](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation)

*说明：仓库 star、Marketplace 数量与插件内容会持续变化。本文所有数量审计均固定到原帖发布前的 `8444efc`；产品可用范围与方案信息则以 2026-10-09 的官方文档为准。*
