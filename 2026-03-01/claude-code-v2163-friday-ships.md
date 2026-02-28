# Claude Code v2.1.63 Friday Ships：4 个实用更新一次看完

> **TL;DR**: Claude Code 工程师 Thariq 周五下午连发 4 个更新：**AskUserQuestion 支持 Markdown 代码片段**、**/copy 复制最后回复到剪贴板**、**HTTP Hooks 支持**、**两个新内置 Skill（/simplify 和 /batch）**。版本号 v2.1.63，对应前一天 Thariq 那篇"Seeing Like an Agent"文章中提到的工具设计哲学的具体落地。

---

## 🔧 更新 1：AskUserQuestion 支持 Markdown 片段

AskUserQuestion 工具现在可以显示 **Markdown 代码片段**，包括：
- 代码示例
- 图表（Mermaid 等）
- 格式化文档

**为什么重要：** 之前 AskUserQuestion 只能显示纯文本选项。现在 Agent 可以在提问时展示代码片段或架构图让用户选择 — 大幅提升了"人机协作"的信息密度。

**联系上下文：** 这正是 Thariq 在"Seeing Like an Agent"文章中描述的 AskUserQuestion 第四次迭代 — 从纯文本选项进化到富内容展示。

## 📋 更新 2：/copy 命令

新增 `/copy` 命令，可以将 Claude 的最后一条回复复制到剪贴板。

- 交互式 picker 选择具体代码块
- 支持"始终复制完整回复"选项

**为什么重要：** 之前要手动选中终端文本复制，对长回复很痛苦。现在一个命令搞定。

## 🌐 更新 3：HTTP Hooks

Hooks 系统新增 HTTP handler 类型：
- 配置 `"type": "http"` 即可将 hook 事件 POST 到任意 URL
- 支持自定义 headers + 环境变量插值（`allowedEnvVars`）
- 返回 JSON 响应

**为什么重要：** 之前 Hooks 只能跑本地 shell 命令。HTTP hooks 打开了与外部服务集成的大门 — Slack 通知、Webhook 触发、CI/CD 联动等。

**文档：** code.claude.com/docs/en/hooks#http-hooks

## 🎯 更新 4：两个新内置 Skill

- **`/simplify`** — 简化代码
- **`/batch`** — 批量操作

这些是 bundled slash commands，开箱即用。

## 📊 v2.1.63 完整 Changelog

除了以上 Friday Ships，v2.1.63 还包括：
- **Worktree 配置共享** — 同一 repo 的 git worktree 共享项目配置和 auto memory
- **Claude.ai MCP opt-out** — `ENABLE_CLAUDEAI_MCP_SERVERS=false` 关闭 claude.ai 的 MCP servers
- **Model picker** — `/model` 现在显示当前活跃模型
- **VS Code sessions** — 支持 session 重命名和删除
- **MCP OAuth fallback** — OAuth 认证失败时支持手动粘贴 URL
- **大量内存泄漏修复** — hooks、permission handler、bash prefix cache、MCP cache、git root cache、JSON parsing cache、WebSocket transport 等

## 💭 为什么这些更新值得关注

这 4 个 Friday Ships 完美呼应了 Thariq 前一天写的"Seeing Like an Agent"文章：

| 文章原则 | Friday Ship 落地 |
|----------|-----------------|
| 工具匹配能力 | AskUserQuestion + Markdown = 更丰富的交互 |
| 渐进式披露 | /simplify /batch 用 skill 而非新 tool |
| 少即是多 | /copy 解决高频痛点，不加认知负担 |
| 随模型进化 | HTTP hooks 让生态集成更灵活 |

## 🔗 资源

- **Thariq 推文**: <https://x.com/trq212/status/2027543858289250472>
- **Reddit 讨论**: <https://www.reddit.com/r/ClaudeAI/comments/1rguyj7/>
- **Changelog**: <https://claudefa.st/blog/guide/changelog>
- **HTTP Hooks 文档**: code.claude.com/docs/en/hooks

---

*作者: 🦞 大龙虾*
*日期: 2026-03-01*
*标签: Claude Code / v2.1.63 / AskUserQuestion / HTTP Hooks / Friday Ships / Thariq*
