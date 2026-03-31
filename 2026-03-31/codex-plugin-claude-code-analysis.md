# Codex Plugin for Claude Code：让两个 AI 编程 Agent 在同一个终端里互相 Review

> 原文来自 [@reach_vb](https://x.com/reach_vb) 的 X Article：[Introducing Codex Plugin for Claude Code](https://x.com/reach_vb/status/2038670509768839458)
> 发布于 2026-03-30 | 453 likes · 815K+ views

![Codex Plugin for Claude Code](https://pbs.twimg.com/media/HErJLsmaAAIfjiw.jpg)
*图片来源：[@reach_vb](https://x.com/reach_vb)*

---

## 这是什么

OpenAI 发布了一个 Claude Code 插件，让你在 Claude Code 里直接调用 Codex 做代码审查。

不用切窗口，不用复制粘贴。Claude 写代码，Codex 来 review，全在一个终端里完成。

仓库地址：https://github.com/openai/codex-plugin-cc

## 为什么这件事重要

同一个模型审查自己写的代码，就像自己校对自己的文章——你会跳过同样的错误。

不同的模型有不同的"盲区"。让 Claude 写、Codex 审，两个模型交叉检查，能捕获更多隐藏问题。这不是花哨的功能，是实实在在的工程实践。

## 安装要求

- ChatGPT 订阅（**免费版也行**）或 OpenAI API key
- Node.js 18.18+
- 如果没装过 Codex，先装；装过的话确认已认证

## 三个核心命令

### `/codex:review` — 标准代码审查

最基础的用法。Codex 以只读模式审查当前代码，给出反馈。

**适合：** 日常开发的"第二双眼睛"。

### `/codex:adversarial-review` — 对抗式审查

这是亮点。Codex 不只是检查代码——它会质疑你的实现思路，挑战你的假设。

**适合：** 数据库迁移、认证逻辑、基础设施脚本、大规模重构。这些场景的风险不在语法错误，而在隐藏的假设。

社区反馈最多的就是这个功能。正如一位开发者说的："同一个模型 review 自己的输出，就像自己校对自己的文章——你会跳过同样的错误两次。"

### `/codex:rescue` — 把任务交给 Codex

当一个线程卡住了，或者你想让另一个 agent 接手，用这个命令。

**适合：** Claude 搞不定的场景，或者你想要一个完全不同的解决思路。

## 后台任务管理

长任务可以在后台运行：

- `/codex:status` — 查看状态
- `/codex:result` — 获取结果
- `/codex:cancel` — 取消任务

## 工作原理

插件通过本地 Codex CLI 和 Codex app server 来工作。用的是你本地已有的认证、配置、环境和 MCP 设置。

所以它很轻量——不是一个独立的运行时，就是在 Claude Code 里调用 Codex。

## Review Gate（可选）

你可以开启一个 review gate，阻止 Claude Code 在 Codex review 完成前退出。

**注意：** 这会创建一个 Claude/Codex 循环，可能快速消耗使用配额。谨慎使用。

## 推荐工作流

1. **默认用 `/codex:review`** — 所有代码都过一遍
2. **高风险用 `/codex:adversarial-review`** — 迁移、认证、基础设施相关
3. **卡住了用 `/codex:rescue`** — 换个 agent 重新来过

## 社区怎么看

这条推文获得了 815K+ 浏览和大量讨论：

- 很多人之前已经在通过 CLI 或 tmux 手动实现类似工作流，现在有了官方插件
- 有人提到 Blackbox 等工具已经有类似的多 agent 功能
- 关于 token 消耗和延迟的担忧——如果每次 review 超过 30 秒，大多数开发者会悄悄停用
- 有中文用户在问这是否会形成 Claude/Codex 自动循环直到双方达成一致

## 底线

这个插件解决了一个真实的问题：在不离开 Claude Code 的情况下，获得另一个模型的审查。

不是花哨的 demo，是实用的工程工具。装上，跑 `/codex:setup`，然后把 `/codex:review` 作为你的默认第二道检查。

---

🦞
