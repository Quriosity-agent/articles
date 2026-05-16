# Suna / Kortix 深度拆解：把 Agent 从聊天框搬进一台会长期工作的公司电脑

> Repo: [kortix-ai/suna](https://github.com/kortix-ai/suna)  
> Inspect commit: `c1aa270` (`Stabilize OpenCode sandbox runtime`)  
> Date: 2026-05-15  
> Tags: Kortix, Suna, AI Agent, Agent OS, OpenCode, Sandbox, Company OS, Agent Infrastructure

![kortix-ai/suna GitHub repository](imgs/kortix-suna-autonomous-company-os/github-repo.png)

很多 Agent 产品的问题，不是模型不会推理，而是它们没有一台真正属于自己的电脑。它们每次从聊天框里醒来，拿到一段上下文，调用几个工具，然后在会话结束时失去大部分工作现场。`kortix-ai/suna`（当前 README 中的产品名已经转向 Kortix）有趣的地方正在这里：它不是把 Agent 做成另一个 SaaS 面板，而是在尝试把“公司运营”放进一台持久运行的 Linux 机器。

项目自己的描述很直接：**The Autonomous Company Operating System**。截至检查时，GitHub API 显示仓库有约 **19.8k stars、3.4k forks**，主语言为 TypeScript，默认分支为 `main`，不是 fork；仓库创建于 2024-10-05，最近 push 在 2026-05-13。这个量级说明它已经不只是一个概念 demo，而是一个正在快速迭代的 Agent OS / 云电脑 / 公司工作台混合体。

## 一句话判断

Suna / Kortix 的核心不是“让 Agent 能聊天”，而是给 Agent 一个可持续运行的工作场：Ubuntu/KDE 桌面、bash、文件系统、Docker、OpenCode runtime、持久卷、API、前端、移动端、权限、计费、隧道、测试和部署脚本。它押注的是：未来的 Agent 产品，不会只竞争 prompt，而会竞争谁能把上下文、工具、凭据、文件、历史和后台触发器组织成一个长期复利的操作系统。

## 这个仓库实际有多重

从文件结构看，`suna` 是一个 pnpm monorepo，而不是单页面 demo。一次本地统计得到：

- 总文件约 **3,248** 个，其中文本文件约 **2,901** 个，二进制/媒体文件约 **347** 个；
- 代码与文本总行数主要集中在 TypeScript / TSX：`.tsx` 约 **285k** 行，`.ts` 约 **212k** 行；
- `apps/` 约 **2,334** 个文件、约 **447k** 文本行；
- `apps/api/` 约 **52k** 行，是 Hono + Bun 的后端单体；
- `apps/web/` 约 **230k** 行，是 Next.js 前端；
- `apps/mobile/` 约 **158k** 行，说明它不只面向桌面浏览器；
- `core/` 约 **120k** 行，承载 sandbox runtime、Docker image、OpenCode 状态和桌面服务；
- `packages/agent-tunnel/` 约 **8.3k** 行，负责隧道、远程访问和权限边界；
- `supabase/migrations/` 有 31 个迁移文件，覆盖 billing、tunnel、sandbox members、invites、access control 等表结构；
- `tests/` 下有 Playwright E2E、shell E2E、security-audit 测试，说明团队在补生产化护栏。

这些数字本身不是价值，但它们揭示了一个事实：Kortix 想解决的不是“如何发一个 prompt”，而是“如何让 Agent 在真实系统里持续做事”。

## 架构层：不是一个 Agent，而是一台 Agent 电脑

我会把这个仓库拆成六层。

第一层是 **产品入口层**。`apps/web` 是主要 Web UI，依赖 Next.js、OpenCode SDK、Supabase、TipTap、CodeMirror、xterm、Pipedream、Stripe、Sentry 等一长串库。它不是简单 chat UI，而是把 session、files、terminal、integrations、billing、admin、sandbox、scheduled tasks 等功能放进同一个控制台。`apps/mobile` 和 `apps/desktop` 说明它还在尝试多端入口。

第二层是 **后端控制平面**。`apps/api/src/index.ts` 把很多子服务挂在一个 Hono 应用下：router、billing、platform、sandbox-proxy、setup、providers、secrets、integrations、queue、servers、tunnel、teams、admin、oauth、access-control 等。文件里的注释把它称为 “Unified monolith combining router, billing, platform, cron, and daytona-proxy”。这很像早期平台公司常见的选择：先用一个可理解的单体把产品闭环跑通，再逐步拆边界。

第三层是 **Agent runtime 层**。README 明确说 agent runtime 是 [OpenCode](https://github.com/anomalyco/opencode)。这很关键：Kortix 没有重新发明 coding agent 内核，而是把 OpenCode 放进一台持久 Linux 机器，再围绕它补状态、权限、通道、触发器、前端和云服务。

第四层是 **sandbox / 云电脑层**。`core/docker/docker-compose.yml` 写得很清楚：这是一个 privileged Docker sandbox，暴露 Kortix Master、noVNC、Presentation Viewer、Agent Browser Stream、SSH、Static Web Server 等端口。更重要的是它定义了三类状态区：`/workspace/` 是持久用户工作区，`/persistent/` 是 OpenCode DB、secrets、auth、browser profile 等系统状态，`/ephemeral/` 是随镜像更新替换的 runtime。这个分层是 Agent OS 的核心，因为长期工作必须先回答“哪些东西会活过下一次更新”。

第五层是 **连接与隧道层**。`packages/agent-tunnel`、`apps/api/src/tunnel`、`sandbox-proxy`、`local-preview`、`preview-ownership` 等文件说明，Kortix 不只是本地容器，还要处理远程 sandbox、预览代理、设备认证、权限请求和审计。Agent 要真的替公司做事，就必须能安全穿过浏览器、API、文件和远程服务之间的边界。

第六层是 **公司操作资产层**。`MANIFESTO.md` 提到 agent、skills、tools、commands、memory、integrations 都应该是文件；`core/docker/general_skill_inventory.json` 列出了大量业务技能，例如 account research、audit support、brand voice、campaign planning、contract review、compliance 等。这里最有意思的不是某个技能写得多完美，而是它说明 Kortix 想把“公司能力”变成可安装、可检查、可积累的文本/脚本资产。

## 最值得借鉴的设计：状态分层

很多 Agent sandbox 的失败点不是不能运行命令，而是状态混乱：用户项目、agent 记忆、工具缓存、系统包、凭据、运行时文件全混在一起，一更新就丢东西，一备份又拖走一堆无关镜像层。

Kortix 的 Docker Compose 对这个问题有明确答案：

- `/workspace/`：用户代码、项目文件、用户安装包，是持久用户空间；
- `/persistent/`：OpenCode DB、shadow backup、secrets、auth、browser profile，是持久系统状态；
- `/ephemeral/`：Kortix server、OpenCode config、services、metadata，是每次镜像更新可替换的运行时；
- `/var/lib/docker` 用单独 `sandbox_docker` 卷保存 Docker-in-Docker 数据，避免把镜像层和用户工作区备份混在一起。

这类细节比 marketing slogan 更说明项目已经摸到生产问题。Agent 想 24/7 工作，第一件事不是多加工具，而是让它的文件、凭据、历史和运行时在更新、重启、迁移时有清晰归属。

## 后台工作不是“异步按钮”，而是队列与触发器

`apps/api/src/queue/drainer.ts` 是一个小但重要的文件。它每 2 秒检查有排队消息的 session，确认 OpenCode session idle 后，再调用 `prompt_async` 把下一条消息送进去。如果发送失败，就重新入队。

这个实现很朴素，但方向正确：Agent 产品如果只依赖浏览器 tab，就永远是交互工具；一旦有后台队列、cron/webhook、session 状态检查和失败重试，它才开始接近“雇员”。`docs/kortix-agent-os-framework-cloud-spec.md` 也把 wedge 讲得很具体：不是抽象“公司大脑”，而是把自定义 agent 部署成 Slack / schedule / webhook 触发、带持久上下文的后台 worker。

## 为什么 OpenCode 是一个好选择

Kortix 把 OpenCode 放在中心，不只是为了“写代码”。README 的论点是：coding agent 的 harness —— bash、文件系统、脚本、API、数据库、浏览器、包管理器 —— 其实适合大部分知识工作。财务、运营、研究、客服、销售、法务和内容，本质上也经常是读文件、查 API、改表格、写报告、发消息、跑脚本。

这也是为什么 Kortix 的架构比普通 no-code automation 更激进。Zapier 式系统通常把动作封装成固定 block；Kortix 更接近把一台 Linux 机器交给 agent，让它按需写工具、装依赖、调用 API、生成新脚本，再把这些东西沉淀成 skill。风险更高，但上限也更高。

## 安全与治理：还在路上，但仓库已经暴露出意识

这种系统天然危险：README 甚至强调“every secret, every integration, every piece of institutional knowledge”。如果真的把公司上下文和凭据交给一个长期运行的 agent，权限、审计、隔离、撤销、最小授权就不是可选项。

仓库里已经有一些迹象：`tests/security-audit/` 下有 JWT、OAuth2、API key、CORS、tunnel、preview proxy、cloud access、webhook HMAC 等测试；`packages/agent-tunnel/src/agent/security/` 有 path validator、command validator、permission guard；后端有 access-control、roles、members、sandbox invite、member spend caps 等迁移和服务。

但从产品视角看，这也会是 Kortix 最大的挑战。越强调“完整公司上下文”，越需要默认安全模型足够清楚：谁能看到什么、谁能执行什么、哪些命令需要人类确认、credential 如何分域、agent 之间如何隔离、审计日志如何不可篡改。Agent OS 的护城河不会只是能力，也会是可控性。

## 与 Suna 早期定位的变化

仓库名还是 `suna`，但 README 标题已经是 `Kortix`，描述也从一般 AI assistant 转向 “Open-Source Operating System for Running Autonomous Companies”。这通常意味着项目正在从工具型产品转向平台型产品。

这个转向很合理。单个 general assistant 很容易被大模型厂商吞掉；但一套能部署、管理、连接、审计、持久化、触发、协作的 Agent OS，不是一个模型 API 能直接替代的。它的价值在 harness、状态、集成和组织流程。

## 谁应该研究这个仓库

如果你在做以下几类产品，Kortix 值得认真读：

1. **Agent 平台 / Agent OS**：重点看 `core/docker`、`apps/api`、`packages/agent-tunnel` 和 Supabase migrations；
2. **AI IDE / coding agent 控制台**：重点看 `apps/web` 如何围绕 OpenCode 做 session、files、terminal、preview；
3. **企业自动化 / ops agent**：重点看 integrations、queue、scheduled tasks、skill inventory；
4. **远程 sandbox / 云电脑**：重点看 persistent volume、noVNC、SSH、browser stream、proxy、tunnel；
5. **Agent 安全治理**：重点看 security-audit tests、permission guard、access-control、preview ownership。

## 局限与风险

第一，仓库体量已经很大，且存在大量 WIP 痕迹。对外部开发者来说，理解成本不低。

第二，当前很多能力看起来处于“平台骨架已经在、体验仍在收敛”的阶段。例如 docs 中还在写 framework + cloud spec，README 也更像愿景宣言加 quick start，而不是稳定 API 手册。

第三，privileged sandbox、完整凭据、root access、长期运行 agent 这条路线强大但危险。它必须依赖非常扎实的权限、隔离和审计设计，否则越自动化越可能放大事故。

第四，Agent OS 的商业落地需要比“公司电脑”更窄的 wedge。好消息是 docs 已经意识到这一点：先从 Slack support triage、GitHub maintainer、daily sales research、failed-payment follow-up、Linear triage、ops brief 这类可度量后台 worker 切入。

## 结论：真正的竞争在 Agent 的“工作场”

Suna / Kortix 最值得关注的地方，是它把 Agent 产品的重心从“对话能力”挪到了“工作场设计”。一台持久 Linux 电脑、一个可运行的 OpenCode runtime、一个保存状态的文件系统、一个能连接 SaaS 的后端、一个能看见桌面/终端/文件/任务的前端、再加上后台队列和触发器——这些东西组合起来，才像一个能长期工作的数字雇员。

从 builder 角度看，Kortix 给出的启发很明确：如果你想做下一代 Agent 产品，不要只问“模型能不能回答”。要问：它住在哪里？它如何记住？它如何拿到工具？它如何被触发？它失败后如何恢复？它的凭据如何隔离？它的工作如何被人类检查？

聊天框是入口，不是操作系统。Kortix 正在尝试证明：真正的 Agent OS，应该是一台会工作的公司电脑。
