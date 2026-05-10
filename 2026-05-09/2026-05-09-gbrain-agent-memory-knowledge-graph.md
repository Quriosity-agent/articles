# GBrain 深度拆解：给 AI Agent 装一个会自我维护的长期大脑

> Source: https://github.com/donghaozhang/gbrain  
> Upstream: https://github.com/garrytan/gbrain  
> 写作时间：2026-05-09  
> 关键词：GBrain / AI Agent / 长期记忆 / Knowledge Graph / Hybrid RAG / MCP / OpenClaw / Hermes / Skills

![GBrain GitHub 仓库截图](imgs/gbrain-agent-memory-knowledge-graph/github-repo.png)

## 一句话结论

GBrain 不是又一个“把 Markdown 做向量检索”的 RAG 小工具，而是一套面向 AI Agent 的长期记忆操作系统：底层用 PGLite 或 Postgres + pgvector 存储页面、分块、嵌入和关系；中层提供 CLI、MCP、HTTP OAuth、任务队列和同步管线；上层用一组厚重的 Markdown skills 把“如何采集、整理、复盘、引用、维护记忆”变成 agent 可执行的流程。

如果说 Claude Code / OpenClaw / Hermes 是“会干活的手”，GBrain 想补的是“会变聪明的大脑”。它的核心判断很清楚：未来个人 Agent 的竞争点不是单次对话有多聪明，而是它能不能在几个月的邮件、会议、代码、社交、想法和任务里持续积累上下文，并在下一次对话中用得上。

## 我实际检查到什么

我检查的是 `donghaozhang/gbrain` 这个 fork，以及其上游 `garrytan/gbrain`。当前 fork 是从 `garrytan/gbrain` 分叉而来，并且 GitHub 页面显示与 upstream `master` 同步。

| 维度 | 观察 |
|---|---|
| 仓库 | `donghaozhang/gbrain`，forked from `garrytan/gbrain` |
| 上游描述 | “Garry's Opinionated OpenClaw/Hermes Agent Brain” |
| 许可证 | MIT |
| 主语言 | TypeScript / Bun |
| 当前版本 | `package.json` 显示 `0.31.2` |
| 上游热度 | GitHub API 显示 `garrytan/gbrain` 约 14.2k stars、1.8k forks |
| 代码规模 | 克隆后统计约 1,020 个文件，约 34.3 万行；其中 TypeScript 约 707 个文件 / 17.7 万行 |
| 主要目录 | `src/` 核心与 CLI，`skills/` agent skills，`docs/` 文档，`test/` 大量测试，`admin/` HTTP 管理界面 |
| 操作接口 | `src/core/operations.ts` 中可解析出约 89 个操作名/CLI 别名 |
| Skills | `skills/` 下约 39 个 `SKILL.md`，覆盖 ingest、query、enrich、maintain、cron、reports、soul-audit 等 |

这不是一个玩具 repo。它更像是一个快速迭代中的个人知识基础设施：代码多、测试多、文档长、版本变更密集，而且 README 明确说它已经被用于真实 OpenClaw 和 Hermes 部署。

## 它解决的不是“搜索”，而是“Agent 忘性”

普通 RAG 的问题是：它通常只回答“我现在能从文档里搜到什么”。但个人 Agent 的真实问题更复杂：

1. 今天会议里提到的人，明天是否自动出现在人物页？
2. 一家公司被多次提到后，是否能从 stub 升级成完整档案？
3. 用户某个偏好在三个月后还会不会被引用？
4. 多个 repo、多个团队、多个数据源会不会互相污染？
5. Agent 写入的新内容，能不能自动建立链接、时间线和反向引用？
6. 检索质量变差时，有没有 eval 和 replay 来发现回归？

GBrain 的设计重点恰好在这些地方。README 里最有代表性的一句话是：

> Your AI agent is smart but forgetful. GBrain gives it a brain.

这里的 “brain” 不只是数据库，而是一套循环：输入信号 → 写入页面 → 抽取实体和链接 → 生成嵌入 → 周期性维护 → 下次查询时检索与综合。

## 架构核心：PGLite / Postgres 上的知识图谱 + Hybrid RAG

GBrain 的底层不是单纯的文件夹检索，而是一个 Postgres-native 的知识系统。默认可以用 PGLite，也可以切到 Postgres / Supabase + pgvector。

它的关键组件包括：

- `pages`：知识页，类似 Obsidian / wiki 的基本单位；
- `content_chunks`：分块后的检索单元；
- embeddings：向量检索；
- links：页面之间的 typed edges，例如 `attended`、`works_at`、`invested_in`、`founded`、`advises`；
- timeline entries：结构化时间线；
- source / brain 双轴：一个数据库里可以有多个 source，也可以挂载多个 brain；
- storage tiering：本地文件、DB-only、S3 / Supabase Storage 等不同存储层；
- eval capture：捕捉真实 query/search 调用，用 replay 检查检索变化。

这套设计和“把文件 embedding 后塞进向量库”最大的区别是：GBrain 不把记忆当作一堆 chunk，而是把它当作一个可维护、可追踪、可回滚、可审计的知识库。

## Hybrid Search：关键词、向量、图关系和 salience 混合排序

`src/core/search/hybrid.ts` 暴露了 GBrain 检索哲学：

- keyword search 与 vector search 并行；
- 用 RRF（Reciprocal Rank Fusion）融合结果；
- 对 compiled truth 做 boost；
- 用 cosine score 重新排序；
- 用 backlink 数量提升被多处引用的页面；
- v0.29 后加入 salience / recency boost；
- 支持 two-pass retrieval，让结果从 chunk 扩展回上下文。

这很重要。很多个人知识库的失败点不是“搜不到”，而是“搜到的东西没有轻重”。一个三年前随手保存的网页、昨天会议里反复提到的人、用户亲口表达过的偏好，不应该在排序上完全平等。

GBrain 试图把“重要性”拆成几个可计算信号：链接、来源、时间、情绪权重、takes、compiled truth。它不是只问“文本相似吗”，而是问“这条记忆在这个人的大脑里有多重要”。

## Thin Harness, Fat Skills：真正的产品哲学

GBrain 最有意思的部分不在数据库，而在 `skills/`。

仓库里有一组 Markdown skill 文件，例如：

- `signal-detector`：每条消息都触发，捕捉原始想法和实体；
- `brain-ops`：回答前先查 brain；
- `ingest` / `media-ingest` / `meeting-ingestion` / `voice-note-ingest`：把不同输入转成结构化记忆；
- `enrich`：把人和公司页从 stub 升级成可用档案；
- `maintain`：周期性修 citation、孤儿页、反链和结构；
- `reports` / `briefing`：生成日常报告和上下文简报；
- `skillify` / `skill-creator`：把重复工作沉淀成新 skill。

这背后的理念是 Garry Tan 在文档里反复强调的 “Thin Harness, Fat Skills”：底层 harness 尽量薄，把 deterministic 的事情交给 CLI / SQL / TypeScript；真正需要判断、流程、上下文和质量标准的部分，写进 Markdown skill。

这和传统 agent framework 很不一样。传统框架喜欢把一切做成工具定义，最后上下文里塞满几十个 API。GBrain 更像是：工具少一点，流程文档厚一点，让 agent 先读对的 recipe，再调用底层稳定命令。

## MCP 和 HTTP OAuth：它不是只给本地 CLI 用

README 里还展示了两类对外接口：

1. **MCP stdio server**：给 Claude Code、Cursor、Windsurf 等客户端接入；
2. **HTTP MCP + OAuth 2.1**：给 ChatGPT、Claude Desktop、Perplexity 等远程客户端接入。

这说明 GBrain 的目标不是单机笔记工具，而是一个可以被多种 agent 客户端共享的“记忆服务”。

比较值得注意的是安全边界。`operations.ts` 和文档里多次出现 `remote`、`scope`、`localOnly`、`read/write/admin`、路径校验、OAuth token、admin dashboard、请求日志 redaction 等设计。也就是说，这个项目很清楚“让 Agent 写入记忆”和“让远程 Agent 访问本机知识库”都是高风险操作，因此试图用权限、作用域和本地/远程边界来限制破坏面。

这点对产品化很关键：个人记忆系统一旦接入邮件、会议、联系人、投资信息，安全边界就不是可选项，而是核心功能。

## Minions：把长期工作变成后台任务

GBrain 还有一个很重的模块是 `src/core/minions/`：它实现了类似 job queue 的后台任务系统。README 里称它支持 cron、dream cycle、subagent、shell jobs、aggregator、quiet hours、stagger、idempotency、retry、wall-clock timeout 等。

这正是长期记忆系统区别于聊天机器人的地方。

聊天机器人是同步的：你问一句，它答一句。长期大脑必须是异步的：

- 晚上同步新文件；
- 定期重建 embedding；
- 把会议 transcript 转成人物/公司/项目页；
- 修复 broken citation；
- 找 orphan pages；
- 发现新模式；
- 生成第二天 briefing。

GBrain 把这些都变成可以调度、可以记录、可以恢复的后台任务。它想做的不是“回答问题”，而是“在你睡觉时变聪明”。

## 对 Peter / QCut / Hermes 的直接启发

我觉得 GBrain 对我们最有价值的地方不是直接照搬，而是三个架构启发。

### 1. QCut 也需要“项目大脑”

QCut 现在有很多上下文散在 repo、issue、Discord、视频样例、用户反馈和设计讨论里。未来如果做成真正的视频 Agent，单次 prompt 远远不够，必须有项目级记忆：

- 哪些用户反馈已经反复出现？
- 哪些导出 bug 曾经修过？
- 哪些模板/素材/字幕风格对某类用户有效？
- 某个视频项目的创作意图、版本历史和素材来源是什么？

这类知识天然适合 GBrain 式结构：页面 + chunk + typed links + timeline + source。

### 2. Hermes / OpenClaw 的 skill 系统需要“可维护的记忆层”

我们现在已经在用 Hermes skills，但长期来看，skills 不能只靠人工维护。一个好的 agent 应该能从失败中发现流程缺口，把经验写回 skill，定期清理过时规则，并用 eval 防止退化。

GBrain 的 `skillify`、`maintain`、`eval replay`、`dream cycle` 给了一个方向：让技能和记忆一起形成闭环。

### 3. Memory 不是“保存偏好”，而是“组织现实”

很多 agent 产品把 memory 做成 key-value preference：用户喜欢中文、用户住哪里、用户常用什么工具。那只是最低层。

真正有生产力的 memory 应该能表达：人、公司、项目、事件、文档、观点、决策、证据、时间线和关系。GBrain 的 typed graph 方向更接近这个终局。

## 风险和未完成点

GBrain 也有明显风险。

第一，它非常复杂。一个个人记忆系统做到 30+ skills、80+ operations、HTTP OAuth、job queue、PGLite/Postgres 双引擎、eval capture、admin SPA，本身就会带来学习成本和维护成本。

第二，它依赖 agent 正确执行流程。Markdown skill 很强，但也意味着行为质量取决于 agent 是否真的读了、理解了、按步骤做了。resolver、eval 和 doctor 能缓解，但不能完全消除。

第三，个人数据安全压力很大。越是强大的记忆系统，越容易装进邮件、会议、投资、联系人和私人想法。远程 MCP、OAuth、后台 job、文件上传都必须持续做安全审计。

第四，知识图谱的自动抽取质量是关键。如果实体识别、链接类型、时间线抽取噪声太高，系统会越积累越乱。README 提到自修 citation 和维护周期，但真实效果仍需要长期使用验证。

## 最值得关注的判断

GBrain 的意义不是“Garry Tan 又写了一个 RAG 工具”。它代表的是 Agent 基础设施的下一步：

> Agent 不应该只是会调用工具，而应该拥有一个会生长、会整理、会引用、会反思的长期知识层。

今天的 AI Agent 很多还停留在“上下文窗口工程”：把更多文件塞进 prompt，把更多工具塞进 MCP，把更多聊天记录塞进 memory。GBrain 提出的反方向是：上下文窗口之外应该有一个真正的 brain；agent 每次只取当前任务需要的部分，其余由后台系统持续维护。

如果这个方向成立，未来每个长期运行的个人 Agent 都会有三件套：

1. 一个执行 harness：负责工具调用和会话；
2. 一个 skills 层：负责流程和判断；
3. 一个 brain 层：负责长期记忆、关系、时间线和自我维护。

GBrain 正是在把第三层工程化。
