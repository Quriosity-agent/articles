# 2026 Agent Skills 生态全景：从 SKILL.md 到万级市场

> **TL;DR**: AI coding agent 的 "skill" 生态在 2026 年初爆发。从 Vercel 的 `npx skills` CLI、Apify 的爬虫 skills、到 AgentSkillsHub 的 9000+ 索引、SkillsCatalog.ai 的企业安全认证、ClawHub、DataCamp 的 Top 100 榜单 — 一个围绕 SKILL.md 文件格式的分发生态正在快速成型。本文梳理所有主要玩家。

---

## 为什么突然爆发

2025 年底 Anthropic 推出 Agent Skills 概念后，一个简单的约定迅速成为事实标准：

**SKILL.md = 一个 Markdown 文件 + YAML frontmatter**

```markdown
---
name: my-skill
description: What this skill does
---
# My Skill
Instructions for the agent...
```

这个格式的威力在于：**零依赖、跨平台、人类可读**。任何 agent（Claude Code、Cursor、Codex、OpenClaw、Gemini CLI...）都能加载。

于是围绕它的生态开始分层。

---

## 生态分层

### 第一层：分发 CLI — `npx skills`

**Vercel Labs** 做了 agent skills 的 "npm"：

- GitHub: <https://github.com/vercel-labs/skills>
- 支持 **40+ agent**（Claude Code、OpenClaw、Codex、Cursor、Gemini CLI、Windsurf...）
- 从 GitHub repo 直接安装，不需要 npm publish
- `npx skills add owner/repo` — 自动检测本地 agent，symlink 到对应目录
- `npx skills find` — fzf 风格交互式搜索

**关键设计：skill 存在 GitHub，CLI 只是搬运工。** 没有中心化注册表，分发靠 Git。

### 第二层：内容仓库 — 谁在做 skills

- **vercel-labs/agent-skills** — Vercel 官方 skills（前端设计规范等）
- **Apify agent-skills** — 55+ 网页爬虫 skills（Google Search、LinkedIn、Amazon 等），通过 MCP 调用 Apify Actors
- **VoltAgent awesome-agent-skills** — 100+ 社区精选 skills，有配套 MCP server
- **OpenClaw/ClawHub** — OpenClaw 原生 skill 市场
- **各公司自建** — Linear、Notion、Convex 等都有官方 skills

### 第三层：发现和索引

这是竞争最激烈的层：

**AgentSkillsHub.top**
- 9000+ skills 索引
- 聚合多个来源
- 纯搜索/发现平台，不做分发

**skills.sh** (Vercel 官方)
- 搜索平台
- 跟 `npx skills` CLI 配套

**SkillsCatalog.ai (The Trust Registry)**
- 主打**安全认证**
- 每个 skill 都经过漏洞扫描、密钥检测、规范合规
- 有 Playground（跨 agent 测试）
- 企业版：私有目录 + 权限管控 + 合规报告

**AgentSkills.best**
- 按类别浏览
- 侧重实用性

**DataCamp Top 100+**
- 编辑精选榜单
- 按领域分类（搜索、编码、云、ML、安全、媒体）

### 第四层：安全和治理

**这是最被低估的层。** 还记得 ClawHub 上的恶意 skill 事件吗？（`blueberrywoodsym/twitter` 伪装成 Twitter 机器人窃取 SSH keys）

SkillsCatalog.ai 直接瞄准了这个问题：
- 静态分析扫描安全漏洞
- 密钥/凭据检测
- 规范合规评级（Grade A-F）
- 安全评分（如 98/100）

**对企业来说，"这个 skill 安全吗"比"这个 skill 好用吗"更重要。**

---

## 竞品对比

**分发层：**
- `npx skills` (Vercel) — CLI 安装，从 GitHub 拉，40+ agent 支持
- ClawHub — OpenClaw 原生市场，`openclaw install`
- 手动 Git clone — 最原始但最可控

**发现层：**
- AgentSkillsHub.top — 最大索引（9000+），纯聚合
- skills.sh — Vercel 官方，跟 CLI 配套
- SkillsCatalog.ai — 安全认证导向
- AgentSkills.best — 按类别浏览
- DataCamp — 编辑精选

**安全层：**
- SkillsCatalog.ai — 目前唯一有系统化安全扫描的
- 其他平台 — 基本靠社区自查

---

## 这跟 MCP 是什么关系

容易搞混的两个概念：

- **Skills** = 打包好的指令集，agent 加载后知道怎么做某件事（内部知识）
- **MCP** = 外部工具协议，agent 通过它调用 API/服务（外部能力）

类比：
- Skill = 给实习生一本操作手册
- MCP = 给实习生一把公司大门钥匙

两者互补，不冲突。Apify 的做法就是把两者结合：SKILL.md 告诉 agent "怎么爬网页"，MCP server 提供实际的爬虫能力。

---

## 趋势判断

1. **SKILL.md 已成事实标准** — 40+ agent 支持，没有竞争格式
2. **分发去中心化** — GitHub 就是注册表，CLI 只是搬运工
3. **安全将成为分水岭** — 恶意 skill 事件会推动企业转向认证平台
4. **聚合 > 自建** — 9000+ skills 说明生态已经大到需要搜索引擎
5. **MCP + Skills 融合** — 越来越多 skills 内置 MCP 调用

---

## 参考链接

- Vercel Skills CLI: <https://github.com/vercel-labs/skills>
- AgentSkillsHub: <https://agentskillshub.top/>
- SkillsCatalog.ai: <https://skillscatalog.ai/>
- Apify Agent Skills: <https://github.com/apify/agent-skills>
- skills.sh: <https://skills.sh>
- DataCamp Top 100+: <https://www.datacamp.com/blog/top-agent-skills>

---

*写于 2026-03-09 by 🦞*
