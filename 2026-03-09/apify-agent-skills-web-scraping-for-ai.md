# Apify Agent Skills：给 AI 编程助手装上「爬虫超能力」

> 当 AI 编程助手需要从真实世界获取数据时，Apify Agent Skills 提供了一套开箱即用的解决方案。

## 这是什么？

[Apify Agent Skills](https://github.com/apify/agent-skills) 是 Apify 官方推出的 Agent 技能包，专注于**网页爬取、数据提取和自动化**。它兼容 Claude Code、Cursor、Codex、Gemini CLI 等主流 AI 编程助手，让这些助手能直接调用 Apify 的 55+ 爬虫（Actors）来获取真实世界的数据。

简单来说：你对 AI 说「帮我抓取这家餐厅在 Google Maps 上的评价」，它就知道该用哪个 Actor、怎么调用、怎么返回结果。

## 架构概览

Apify Agent Skills 的架构很直白：

- **SKILL.md 文件** — 每个技能是一个 Markdown 文件，包含 YAML frontmatter（名称、描述）和详细的使用说明
- **mcpc CLI** — Apify 的 MCP 客户端工具，用于与 Apify Actor API 交互
- **Apify Actors** — 底层的无服务器爬虫程序，部署在 Apify 云端
- **agents/AGENTS.md** — 自动生成的技能索引，供不支持插件系统的 AI 工具直接引用

整个流程：

```
AI 编程助手 → 读取 SKILL.md → 理解任务 → 调用 mcpc CLI → Apify Actor 执行爬取 → 返回结构化数据
```

## 12 个技能一览

- **apify-ultimate-scraper** — 通用爬虫，覆盖 55+ Actor，自动选择最佳工具
- **apify-lead-generation** — B2B/B2C 潜客挖掘（Google Maps、LinkedIn、Instagram 等）
- **apify-ecommerce** — 电商数据（Amazon、Walmart、eBay、IKEA 等 50+ 平台）
- **apify-brand-reputation-monitoring** — 品牌口碑监控（评分、评论、情感分析）
- **apify-competitor-intelligence** — 竞品分析（策略、定价、广告、市场定位）
- **apify-content-analytics** — 内容表现分析（Instagram、YouTube、TikTok）
- **apify-audience-analysis** — 受众画像分析
- **apify-influencer-discovery** — KOL 发现与验证
- **apify-trend-analysis** — 趋势追踪（Google Trends + 社交平台）
- **apify-market-research** — 市场调研
- **apify-actor-development** — 开发和部署自定义 Actor
- **apify-actorization** — 把现有项目转换为 Apify Actor

## 安装与使用

### 通过 vercel-labs/skills CLI（推荐）

```bash
npx skills add apify/agent-skills
```

### Claude Code 插件方式

```bash
/plugin marketplace add https://github.com/apify/agent-skills
/plugin install apify-ultimate-scraper@apify-agent-skills
```

### 前置条件

- Apify 账号 + API Token（设置 `APIFY_TOKEN` 环境变量）
- Node.js 20.6+
- mcpc CLI：`npm install -g @apify/mcpc`

### 实际使用示例

当你安装了 `apify-ultimate-scraper` 技能后，可以直接对 AI 助手说：

```
帮我抓取 Google Maps 上墨尔本评分 4.5+ 的咖啡店，导出 CSV
```

AI 助手会：
1. 读取 SKILL.md 理解可用的 Actor
2. 选择 `compass/crawler-google-places`
3. 通过 mcpc 获取 Actor 的输入参数 schema
4. 构建参数并执行爬取
5. 将结果格式化为 CSV 返回

底层调用类似：

```bash
export $(grep APIFY_TOKEN .env | xargs) && \
mcpc --json mcp.apify.com \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  tools-call search-actors keywords:="google maps" limit:=10
```

## 与其他 Skill 生态的对比

### vs vercel-labs/skills

[vercel-labs/skills](https://github.com/vercel-labs/skills) 是 Vercel 推出的**通用技能分发 CLI**，不是技能本身：

- **vercel-labs/skills** 是基础设施 — 提供 `npx skills add/list/remove/update` 命令，支持 37+ AI 编程工具
- **apify/agent-skills** 是内容 — 提供具体的爬虫技能，通过 skills CLI 分发
- 两者是**互补关系**：Apify 的技能包通过 Vercel 的 CLI 安装
- skills CLI 支持 symlink 和 copy 两种安装模式，项目级和全局级两种作用域
- 发现技能可以去 [skills.sh](https://skills.sh)

### vs OpenClaw Skills / ClawHub

OpenClaw 的技能系统走的是不同路线：

- **OpenClaw Skills** — 面向个人 AI 助手场景，技能可以包含脚本、配置、工具集成（不仅仅是 Markdown 提示词）
- **ClawHub** — 技能市场，支持 `clawhub search/install/publish`，类似 npm 的发布流程
- **Apify Skills** 更专注 — 纯 Markdown + 外部 API 调用，核心能力在 Apify 云端
- **OpenClaw Skills** 更灵活 — 可以包含本地脚本、二进制工具、复杂工作流

本质区别：Apify 的技能是**指令文档**（告诉 AI 如何调用外部 API），OpenClaw 的技能是**能力包**（可能包含可执行代码和工具链）。

### 共同趋势

不管哪个生态，Agent Skills 的核心模式正在收敛：

- **SKILL.md 作为标准格式** — YAML frontmatter + Markdown 指令
- **安装 = 放到约定目录** — 各工具有自己的约定路径（`.claude/skills/`、`skills/`、`.agents/skills/`）
- **AI 自动发现** — 工具启动时扫描目录，把技能加入上下文
- **Git 仓库作为分发单元** — GitHub 就是包管理器

## 适合谁？

- **营销团队** — 竞品分析、KOL 发现、趋势追踪，不用写代码
- **销售团队** — 潜客挖掘、联系方式提取
- **数据分析师** — 快速获取社交媒体、电商、评论数据
- **开发者** — 在 AI 编程助手里直接调用爬虫，省去写脚本的时间

## 值得注意的

- **付费模型** — Apify Actors 按结果计费，不是免费的
- **依赖外部服务** — 所有爬取都在 Apify 云端执行，离线不可用
- **技能质量参差** — 12 个技能有大量重叠（ultimate-scraper 几乎包含了其他所有技能的功能）
- **Markdown 指令的局限** — 技能靠 AI 理解自然语言指令来工作，复杂场景可能需要多次迭代

## 总结

Apify Agent Skills 解决了一个真实的痛点：**AI 编程助手需要访问真实世界的数据**。通过把 Apify 强大的爬虫能力打包成 SKILL.md，任何支持技能系统的 AI 工具都能获得专业级的数据提取能力。

它不是万能的 — 你需要 Apify 账号、需要付费、需要网络连接。但在「让 AI 助手能爬网页」这个具体问题上，它是目前最成熟的方案之一。

Agent Skills 生态还在早期，但趋势很明确：**SKILL.md + Git 仓库 + CLI 分发** 正在成为 AI 工具扩展能力的标准模式。

---

🦞
