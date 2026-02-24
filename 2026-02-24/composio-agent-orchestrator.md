# Composio Agent Orchestrator：并行 AI 编码 Agent 的编排框架

**来源：GitHub - ComposioHQ/agent-orchestrator**

---

## 一句话总结

Composio 开源了 Agent Orchestrator，一个专门用来管理多个 AI 编码 Agent 并行工作的编排框架——自动创建工作区、启动 Agent、处理 CI 失败、响应 Code Review，你只需要 `ao spawn` 然后去喝咖啡。

---

## 为什么值得关注？

单个 AI Agent 写代码已经不新鲜了。但当你同时有 30 个 issue 要处理、30 个分支要管理、30 个 PR 要追踪时，这就变成了一个**编排问题**。

没有编排，你需要手动：创建分支、启动 Agent、检查是否卡住、阅读 CI 失败日志、转发 Review 评论、追踪哪些 PR 可以合并、清理完成的工作区。

Agent Orchestrator 把这些全自动化了。⭐ 616 stars，MIT 许可证。

---

## 核心设计：八个可插拔槽位

Agent Orchestrator 的架构核心是**插件系统**——8 个抽象槽位，每个都可以替换：

| 槽位 | 默认实现 | 可替换为 |
|------|---------|---------|
| **Runtime** | tmux | Docker, K8s, process |
| **Agent** | Claude Code | Codex, Aider, OpenCode |
| **Workspace** | git worktree | clone |
| **Tracker** | GitHub Issues | Linear |
| **SCM** | GitHub | — |
| **Notifier** | 桌面通知 | Slack, Composio, Webhook |
| **Terminal** | iTerm2 | Web |
| **Lifecycle** | core | — |

所有接口定义在 `packages/core/src/types.ts`，写一个插件只需要实现一个 TypeScript 接口并导出 `PluginModule`。

---

## 工作流程

```bash
ao spawn my-project 123   # 123 = GitHub Issue / Linear Ticket
```

执行后自动发生的事情：

1. **Workspace 插件** 创建独立的 git worktree + feature branch
2. **Runtime 插件** 启动一个 tmux session（或 Docker 容器）
3. **Agent 插件** 在隔离环境中启动 Claude Code，注入 issue 上下文
4. Agent 自主工作——读代码、写测试、创建 PR
5. **Reactions 系统** 自动处理 CI 失败和 Review 评论
6. **Notifier** 只在需要人类判断时才通知你

关键词：**自主闭环**。CI 挂了？Agent 自己看日志修。Reviewer 提了意见？Agent 自己改。PR 绿了且 approved？通知你点 merge。

---

## 自动化反应系统

配置文件 `agent-orchestrator.yaml` 中可以定义反应规则：

```yaml
reactions:
  ci-failed:
    auto: true
    action: send-to-agent
    retries: 2
  changes-requested:
    auto: true
    action: send-to-agent
    escalateAfter: 30m
  approved-and-green:
    auto: false        # 改为 true 可自动合并
    action: notify
```

这是真正的 **Agent-native CI/CD**——CI 失败不再是发个通知给人看，而是直接把失败日志喂给 Agent 让它修。

---

## CLI 一览

```bash
ao status                          # 查看所有 session 状态
ao spawn my-project 123            # 从 issue 启动 Agent
ao spawn my-project "Fix the tests" # 从自然语言描述启动
ao send <session> "try a different approach"  # 给 Agent 发指令
ao list                            # 列出所有 session
ao kill <session>                  # 终止 session
ao revive <session>                # 复活崩溃的 Agent
ao dashboard                       # 打开 Web 仪表盘
```

Web Dashboard 默认在 `http://localhost:3000`。

---

## 技术栈

- **语言：** TypeScript（89.1%）+ Shell（10%）
- **包管理：** pnpm monorepo
- **测试：** 3,288 个测试用例
- **前提：** Node.js 20+, Git 2.25+, tmux, gh CLI
- **许可证：** MIT

---

## 对比：为什么不自己写脚本？

你当然可以写个 bash 脚本来 `git worktree add && tmux new-session && claude`。但 Agent Orchestrator 解决的是规模化问题：

- **隔离性**：每个 Agent 有独立的 worktree，不会互相踩代码
- **反馈闭环**：CI 失败和 Review 评论自动路由回 Agent
- **状态追踪**：Dashboard 统一查看所有 Agent 的进度
- **容错**：Agent 崩溃可以 `ao revive` 复活
- **可扩展**：插件架构让你替换任何组件

---

## 我的看法

Agent Orchestrator 代表了一个趋势：**AI 编码从"单兵作战"走向"军团作战"**。

以前的工作流：你跟一个 AI Agent 对话，一次处理一个任务。
现在的工作流：你把 30 个 issue 分派给 30 个 Agent，它们并行工作，自己处理 CI 和 Review，你只负责最终的 merge 决策。

这本质上是把**软件工程的并行度**从"人的数量"提升到了"计算资源的数量"。Composio 做的事情和 OpenClaw 的 Agent Swarm、Claude Code 的 Agent Teams 方向一致——编排，才是 AI 编码的真正杀手锏。

---

## 链接

- **GitHub：** <https://github.com/ComposioHQ/agent-orchestrator>
- **官网：** <https://composio.dev>
- **文档：** [Setup Guide](https://github.com/ComposioHQ/agent-orchestrator/blob/main/SETUP.md) · [Architecture](https://github.com/ComposioHQ/agent-orchestrator/blob/main/CLAUDE.md) · [Troubleshooting](https://github.com/ComposioHQ/agent-orchestrator/blob/main/TROUBLESHOOTING.md)
