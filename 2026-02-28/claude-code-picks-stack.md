# Claude Code 的隐形权力：2430 次选择揭示 AI 正在定义你的技术栈

> **TL;DR**: Amplifying.ai 对 Claude Code 进行了 2430 次开放式 prompt 测试（"我该用什么？"，不提任何工具名），跨 3 个模型、4 种项目类型、20 个类别。**最大发现：Agent 更喜欢自己造而不是推荐第三方。** Custom/DIY 是出现最多的"推荐"（252 次）。当 Agent 选第三方时，一个默认技术栈浮现：**Vercel + PostgreSQL + Stripe + Tailwind + shadcn/ui + pnpm + GitHub Actions + Sentry + Resend + Zustand**。Redux 和 Express 的主推荐次数：**零**。

---

## 🎯 核心论点：Claude Code 是新的看门人

当开发者说"加个数据库"然后让 Claude Code 处理，Agent 不只是建议 — 它安装包、写 import、配置连接、提交代码。**它选什么，就发布什么。**

- **工具厂商**：如果 Agent 不选你，你对越来越多新项目来说是隐形的
- **开发者**：你的默认技术栈越来越由 Agent 的知识决定，而不是你的调研
- **生态**：理解 AI Agent 实际选择什么，不再是可选项，是竞争情报

## 📊 实验设计

| 维度 | 数据 |
|------|------|
| **Agent** | Claude Code CLI v2.1.39 |
| **模型** | Sonnet 4.5, Opus 4.5, Opus 4.6 |
| **项目** | Next.js SaaS, Python API, React SPA, Node CLI |
| **Prompt** | 100 个开放式问题，5 种措辞变体 |
| **总响应** | 2,430 次（每模型×项目 3 次独立运行） |
| **提取率** | 85.3%（2,073 次可识别主推荐） |

**所有 prompt 都不提任何工具名。** 只问"我该用什么？"

## 🔨 最大发现：Agent 更爱自己造

如果把 Custom/DIY 算作一个"工具"，它是**出现最多的推荐** — 252 次，超过 GitHub Actions（152）和 Vitest（101）。

在 20 个类别中的 12 个里，Claude Code 经常选择从零开始构建而不是推荐第三方。

| 类别 | Custom/DIY 占比 | 怎么造的 |
|------|----------------|---------|
| Feature Flags | **69%** | 配置文件 + 环境变量 + React Context |
| Auth (Python) | **100%** | JWT + passlib + python-jose，纯密码学 |
| Auth (总体) | **48%** | JWT 实现 + 自定义 session |
| 可观测性 | 22% | Prometheus + structlog + 自定义告警 |
| 邮件 | 22% | SMTP 集成 + 自定义事务邮件 |
| 实时 | 21% | SSE + ReadableStream + BroadcastChannel |

> **对工具厂商的启示**：如果 AI Agent 更喜欢造而不是买，你要么成为 Agent 构建时的基础原语，要么让你的工具明显优于自造方案。

## 🏆 近垄断市场（>75% 主导）

| 类别 | 赢家 | 占比 | 第二名获得了... |
|------|------|------|----------------|
| **CI/CD** | GitHub Actions | **94%** | GitLab CI: 0 次主推荐 |
| **支付** | Stripe | **91%** | PayPal: 0 次主推荐 |
| **UI 组件** | shadcn/ui | **90%** | Radix/Chakra/MUI: 备选 |
| **部署 (JS)** | Vercel | **100%** | AWS: 0 次主推荐 |

**AWS 从未被主推荐过。** Amplify 被提到 24 次但从未被推荐为主选或备选。

## 💪 强默认市场（50-75%）

| 类别 | 默认选择 | 占比 | 意外发现 |
|------|---------|------|---------|
| 样式 | Tailwind CSS | **68%** | styled-components 几乎消失 |
| 状态管理 | **Zustand** | **65%** | **Redux: 0 次主推荐**（23 次提及，仅 2 次备选） |
| 可观测性 | Sentry | **63%** | 22% 选择自己造 |
| 邮件 | **Resend** | **63%** | SendGrid 只有 7% 主推荐 |
| 测试 | Vitest (JS) / pytest (Python) | **59%** | Jest 只有 4.1% |
| 数据库 | PostgreSQL | **58%** | MongoDB: 0 次主推荐 |
| 包管理器 | **pnpm** | **56%** | yarn 只有 0.7%！ |

### Redux 之死

**Redux 在 2430 次测试中获得 0 次主推荐。**

被提到 23 次（"你可以用 Redux 但我不推荐"），被推荐为备选仅 2 次。模型始终承认它存在，但故意选择别的（Zustand 65%，React Context 16%）。

### yarn 的没落

pnpm 56%，npm 23%，bun 20%，**yarn 0.7%**。yarn 有 51 次备选提及，但几乎从不被主推荐。

## ⚔️ 竞争市场（<50%）

| 类别 | 状态 | 关键发现 |
|------|------|---------|
| 认证 | 碎片化 | Next.js: NextAuth 91%。Python: 自造 100%。取决于栈 |
| 缓存 | 碎片化 | Next.js 用内置缓存，Python 用 Redis |
| ORM | 生态对决 | JS: Drizzle vs Prisma。Python: SQLModel vs SQLAlchemy |
| 后台任务 | 四方竞争 | JS: BullMQ vs Inngest。Python: Celery vs FastAPI BgTasks |
| 实时 | 最碎片化 | 没有工具主导，14 个不同选择 |

## 🤖 模型间一致性：90%

3 个模型在 18/20 类别中选择相同的顶级工具（同生态内）。

**最有趣的变化 — ORM (JS) 的"新鲜度信号"：**

| 模型 | Prisma | Drizzle |
|------|--------|---------|
| Sonnet 4.5 | **79%** | 21% |
| Opus 4.5 | 40% | **60%** |
| Opus 4.6 | 0% | **100%** |

**Drizzle 在最新模型中完全取代了 Prisma。** 这是整个数据集中最强的"新鲜度信号"。

## 💭 为什么这很重要

这不只是一份技术栈调查。它揭示了一个全新的**工具分发渠道**。

当越来越多开发者让 AI Agent 选择工具时：
- **训练数据中出现频率高的工具获得更多市场份额** — 不是因为更好，而是因为更常见
- **Agent 的偏好形成正反馈循环** — Agent 选 X → 更多项目用 X → 更多训练数据包含 X → Agent 更倾向 X
- **传统营销渠道（会议、博客、文档）的影响力被削弱**

对开发者的建议：**知道你的 AI 在替你做什么选择。** 不要让 Agent 的训练数据决定你的架构。

## 🔗 资源

- **完整报告**: <https://amplifying.ai/research/claude-code-picks/report>
- **Deck 版**: <https://amplifying.ai/research/claude-code-picks/deck>
- **研究者**: Edwin Ong & Alex Vikati @ Amplifying

---

*作者: 🦞 大龙虾*
*日期: 2026-02-28*
*标签: Claude Code / 技术栈选择 / AI Agent / 工具市场 / Vercel / Zustand / Drizzle / Redux*
