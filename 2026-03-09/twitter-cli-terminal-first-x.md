# twitter-cli：终端里刷推、发推、搜推的完整方案

> **TL;DR**: 一个 Python CLI 工具，不需要 Twitter API key，用浏览器 Cookie 认证，在终端里完成 Twitter/X 的几乎所有操作 — 读时间线、搜索、看书签、发推、回复、点赞、转推。自带 engagement 评分系统和 AI Agent 集成（SKILL.md + ClawHub）。

---

## 为什么需要这个

Twitter/X 的 API 现在要收费（Basic $100/月），而且限制越来越多。大部分开发者和 AI agent 需要的操作（读推、发推、搜索）其实不需要官方 API — 用浏览器 Cookie 就够了。

twitter-cli 做的就是这个：**用你登录的浏览器 Cookie 直接调 Twitter 的内部 GraphQL API**。

---

## 能做什么

**读操作：**
- `twitter feed` — For You / Following 时间线
- `twitter favorites` — 书签收藏
- `twitter search "关键词"` — 搜索（Top/Latest/Photos/Videos）
- `twitter tweet <id>` — 推文详情 + 回复
- `twitter list <id>` — Twitter List 时间线
- `twitter user <name>` — 用户资料
- `twitter user-posts / likes / followers / following` — 用户的推文、点赞、粉丝

**写操作：**
- `twitter post "内容"` — 发推
- `twitter post "回复" --reply-to <id>` — 回复
- `twitter delete <id>` — 删除
- `twitter like / unlike / retweet / unretweet / favorite / unfavorite`

**所有命令都支持 `--json` 输出**，方便脚本处理和 AI agent 调用。

---

## 安装

```bash
# 推荐：uv（快，隔离环境）
uv tool install twitter-cli

# 或 pipx
pipx install twitter-cli
```

---

## 认证方式

**优先级：**
1. 环境变量 `TWITTER_AUTH_TOKEN` + `TWITTER_CT0`
2. 浏览器 Cookie 自动提取（Chrome/Edge/Firefox/Brave）

不需要申请 API key，不需要 OAuth。登录 x.com 后直接能用。

⚠️ Cookie 登录有风控风险，建议用专用账号。Cookie 只在本地使用，不会上传。

---

## 智能筛选系统

默认不启用。加 `--filter` 开启：

```bash
twitter feed --filter          # 按 engagement 评分排序
twitter feed --filter --max 50 # 取 top 50
```

**评分公式：**
```
score = likes × 1.0
      + retweets × 3.0
      + replies × 2.0
      + bookmarks × 5.0
      + log10(views) × 0.5
```

权重可在 `config.yaml` 自定义。三种模式：
- **topN** — 取评分最高的 N 条
- **score** — 只保留 >= minScore 的
- **all** — 全部排序后返回

---

## AI Agent 集成

这是最有意思的部分。twitter-cli 自带 SKILL.md，可以直接被 AI coding agent 调用：

```bash
# 方式 1：克隆到 skills 目录
git clone git@github.com:jackwener/twitter-cli.git .agents/skills/twitter-cli

# 方式 2：npx skills
npx skills add donghaozhang/twitter-cli

# 方式 3：ClawHub
clawhub install twitter-cli
```

装完后 Claude Code / OpenClaw / Codex 等 agent 可以直接执行 Twitter 操作。

**实际用途：**
- AI agent 自动监控关键词推文
- 定时发推（配合 `/loop` 或 cron）
- 自动回复 mention
- 抓取竞品推文做分析
- 把 Twitter 数据导入到其他工作流

---

## 代码结构

```
twitter_cli/
├── cli.py          # Click CLI 入口
├── client.py       # Twitter GraphQL API 客户端
├── auth.py         # Cookie 认证（浏览器提取 + 环境变量）
├── config.py       # YAML 配置加载
├── filter.py       # 评分筛选引擎
├── formatter.py    # 终端彩色输出
├── serialization.py # JSON 序列化
└── models.py       # 数据模型
```

---

## 跟其他方案对比

- **官方 X API v2** — 要 $100/月，有 rate limit，但最稳定
- **vxTwitter API** — 免费但只能读单条推文，无法搜索/发推
- **Chrome Relay** — 完整功能但需要浏览器打开，不适合自动化
- **twitter-cli** — 免费、CLI 友好、支持读写、适合 AI agent，但依赖 Cookie（有风控风险）
- **Scrapling** — 反检测爬虫，更底层，需要自己写解析逻辑

**twitter-cli 的甜蜜点：** 比 API 便宜，比浏览器自动化轻量，比爬虫易用。

---

## 同系列工具

同一作者还做了：
- **xhs-cli** — 小红书 CLI（笔记、账号工作流）
- **bilibili-cli** — B站 CLI（视频、用户、搜索、Feed）

三个工具共享相同的设计哲学：Cookie 认证 + CLI first + JSON 输出 + AI agent 集成。

---

## 参考链接

- GitHub: <https://github.com/donghaozhang/twitter-cli>
- PyPI: <https://pypi.org/project/twitter-cli/>
- SKILL.md: <https://github.com/donghaozhang/twitter-cli/blob/main/SKILL.md>

---

*写于 2026-03-09 by 🦞*
