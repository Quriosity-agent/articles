# Claude Code Agent View：把多 Agent 并行从 tmux 网格升级成控制台

> Source: [Claude on X](https://x.com/claudeai/status/2053940938666279028) / [Anthropic blog: Agent view in Claude Code](https://claude.com/blog/agent-view-in-claude-code) / [Claude Code docs: Agent view](https://code.claude.com/docs/en/agent-view)  
> Date: 2026-05-11  
> Tags: Claude Code / Agent View / Coding Agents / Multi-Agent / Worktrees / Agent Orchestration

![Claude Code Agent View hero](imgs/claude-code-agent-view-control-plane/claude-agent-view-hero.svg)

Anthropic 这次给 Claude Code 加的 **Agent view**，表面看只是一个 CLI 里的会话列表：按左箭头，或者运行 `claude agents`，就能看到所有后台 Claude Code session 的状态。

但如果放到更大的 agent 工程趋势里看，它真正补上的不是“UI”，而是 **多 agent 并行工作的控制面**。

过去我们跑多个编码 agent，常见做法是：开一堆 terminal tab、tmux pane、不同目录、不同 worktree，然后靠脑子记：哪个在跑测试？哪个卡在权限确认？哪个已经开了 PR？哪个失败了？

这套方法能撑住 2 个任务，勉强撑住 4 个任务；一旦变成 8 个、12 个、再加上循环任务和 PR babysitter，人就变成了人工 scheduler。

Agent view 的价值就在这里：它把“多 Claude Code session”从一组散落的终端，收敛成一个可扫描、可切换、可回复、可恢复的任务面板。

---

## Agent View 解决的不是启动问题，而是管理问题

Anthropic 官方博客的第一句话很直接：

> one place to manage all your Claude Code sessions.

这句话比功能列表更重要。因为现在 coding agent 的瓶颈已经不只是“能不能写代码”，而是：

1. **能不能同时启动多个独立任务**；
2. **能不能知道每个任务现在在干什么**；
3. **能不能只在需要人类判断时打断你**；
4. **能不能把结果、PR、失败状态稳定收回来**。

Agent view 不是让 Claude Code 第一次支持并行。Claude Code 之前也可以靠多个终端、多个 worktree、多个 session 并行跑。它真正改变的是管理成本：从“用户手动维护 mental ledger”，变成“CLI 里有一个明确的 roster”。

官方文档把这个面板定义为：

> Dispatch and manage many Claude Code sessions from one screen. Agent view shows what every session is doing and which ones need your input.

这其实已经接近一个本地版 agent control plane。

---

## 核心入口：`claude agents`、左箭头、`/bg`、`claude --bg`

Agent view 有四个关键入口：

| 场景 | 命令 / 操作 | 含义 |
|---|---|---|
| 打开总览 | `claude agents` | 进入所有后台 session 的列表 |
| 从当前 session 回到总览 | 空 prompt 按 `←` | 把当前 session 放到后台并打开 Agent view |
| 把当前会话后台化 | `/bg` 或 `/background` | 继续运行，但不占用当前 terminal |
| 直接启动后台任务 | `claude --bg "<prompt>"` | 从 shell 发起一个后台 Claude Code session |

这四个入口组成了一个很完整的工作流：

```bash
claude agents
# 在底部输入任务，Enter 派发

claude --bg "investigate the flaky SettingsChangeDetector test"
# 从 shell 直接发起后台任务

/bg run the test suite and fix any failures
# 在已有交互 session 内追加指令并后台化
```

也就是说，Claude Code 不再只有“我和一个 agent 一对一聊天”的模式；它开始支持“我派发、巡视、接管、再回到总览”的操作模式。

这对真实工程很关键。因为工程问题经常天然可并行：一个 agent 查 flaky test，一个 agent 改 UI，一个 agent 写迁移脚本，一个 agent 做 PR review。真正难的不是让它们同时开始，而是让人类能在不被淹没的情况下管理它们。

---

## 状态面板：把 agent 从黑盒变成可扫描队列

Agent view 的列表按状态组织：需要你输入的、正在工作的、已完成的、失败的、停止的，以及循环任务下一次运行时间。

官方文档里给出的状态大致是：

| 状态 | 含义 |
|---|---|
| Working | Claude 正在运行工具或生成回复 |
| Needs input | Claude 等待用户输入，通常是权限确认或决策问题 |
| Idle | 会话在等待输入，但没有被具体问题阻塞 |
| Completed | 任务成功结束 |
| Failed | 任务以错误结束 |
| Stopped | 会话被停止 |
| Loop sleeping | `/loop` 类任务在两次运行之间休眠，并显示下一次运行时间 |

每一行还会显示 session 名称、最近活动、最后回复摘要、上次交互时间。如果 session 开了 PR，列表里还能直接显示 PR link 和 CI 状态。

这里有一个细节很值得注意：文档说每行摘要由配置的 Haiku-class model 生成，活跃任务最多约 15 秒刷新一次，并在每一轮结束时刷新一次。

这说明 Anthropic 在把 agent orchestration 产品化时，已经不只是在跑“主 agent”，还在用小模型做元层面的状态压缩。换句话说：未来 coding agent 的界面，不会只是 transcript，而会是不断被压缩、归纳、排序后的 operations dashboard。

---

## Peek and reply：不进入完整 transcript，也能处理阻塞点

Agent view 里最实用的设计可能不是列表，而是 **peek panel**。

选中一行按 Space，可以看到该 session 最近输出、它需要你做什么、以及它创建的 PR。很多时候，人类不需要 attach 进去读完整上下文，只需要回答一个问题：

- 是否允许执行某个命令；
- 在 A/B 两种方案里选一个；
- 给它一个缺失的环境变量；
- 看一眼 PR 是否已经产出。

文档里还提到，如果 session 正在问多选题，可以直接按数字选择；对普通阻塞问题，可以按 Tab 填入建议回复；甚至可以用 `!` 前缀从 peek panel 发送 Bash 命令。

这相当于把人类从“全程陪跑者”变成“异常处理器”。

对 agent 产品来说，这是很大的角色变化。早期 coding agent 的交互模型是 pairing：人类在旁边看、随时纠正。Agent view 指向的是 dispatching：人类负责派工、看状态、处理少数需要判断的节点。

---

## Attach / detach：需要深挖时，仍然回到完整 Claude Code

Agent view 没有试图替代完整的 Claude Code 交互。它的设计是：

- 平时在列表里扫描；
- 小问题用 peek 处理；
- 真正需要上下文时 attach；
- 完事按左箭头 detach 回列表。

快捷键也很像一个 terminal-native 的任务切换器：

| 快捷键 | 行为 |
|---|---|
| `↑ / ↓` | 在 session 间移动 |
| `Space` | 打开 / 关闭 peek panel |
| `Enter` 或 `→` | attach 到选中的 session |
| `←` | 从 attached session detach 回 Agent view |
| `Ctrl+T` | pin / unpin session |
| `Ctrl+S` | 按状态 / 目录切换分组 |
| `Ctrl+R` | 重命名 session |
| `Ctrl+X` | 停止；短时间内再按一次删除 |
| `?` | 显示所有快捷键 |

这套交互非常“终端原生”。它不是另开一个 Web dashboard，而是在 CLI 里长出一个多任务面板。对 Claude Code 的目标用户来说，这可能比一个浏览器控制台更自然。

---

## 最关键的工程点：后台 session 由 supervisor 托管

Agent view 真正变成基础设施，而不是 UI 小功能，靠的是后台 session 的托管模型。

官方文档说，后台 session 由一个 per-user supervisor process 托管。这个 supervisor 和终端、Agent view 本身是分开的：

- 你关闭 Agent view，session 继续跑；
- 你关闭 shell，session 继续跑；
- 已完成且无人 attach 的 session 约一小时后进程会被停止以释放资源，但 transcript 和状态留在磁盘上；
- 下次 attach、peek 或 reply 时，supervisor 会从保存状态恢复；
- Claude Code 自动更新后，supervisor 会跟着新 binary 重启并重新连接后台 session。

状态文件大致存在：

| 路径 | 内容 |
|---|---|
| `~/.claude/daemon.log` | supervisor log |
| `~/.claude/daemon/roster.json` | 运行中后台 session 列表 |
| `~/.claude/jobs/<id>/state.json` | Agent view 显示的每个 session 状态 |

这部分说明 Anthropic 已经在把 Claude Code 从“一个 CLI 进程”扩展成“一个本地 daemon + 多 worker process 的系统”。

这也是它和 tmux 的本质区别：tmux 保持的是终端窗口；Agent view 保持的是 agent 任务状态。

---

## Worktree 隔离：并行不是乱写同一个目录

多 agent 并行最危险的问题是文件冲突。Anthropic 的做法是：后台 session 默认从你的工作目录开始，但如果需要写文件，会自动进入 `.claude/worktrees/` 下的隔离 git worktree。

这样每个后台 session 可以读同一个 checkout，但写入自己的 worktree。删除 session 时，对应 worktree 会被清理；如果想保留改动，需要先 merge 或 push。

这对真实团队很重要，因为“多 agent 并行”不是多开几个进程那么简单。它至少需要三层隔离：

1. **上下文隔离**：每个 session 有自己的 conversation state；
2. **文件隔离**：每个 session 不要互相覆盖代码；
3. **权限隔离**：后台任务不能在用户没看见时无限制执行危险操作。

Agent view 这次把前两层都做进了默认工作流，第三层则通过 permission mode 和设置来控制。

---

## 这意味着什么：Coding Agent 正在从“助手”变成“队列”

这次更新最值得关注的，不是 Claude Code 多了几个命令，而是产品范式变化：

过去：

> 一个开发者 + 一个 AI 助手，在一个终端里结对。

现在：

> 一个开发者 + 一组后台 agent，在一个控制面里派发、监控、接管和回收结果。

这会改变很多工程习惯：

- 小 bug 不再排队等你一个个处理，而是可以批量派发；
- PR review、dashboard update、日志调查这类“长时间但低交互”的任务会更适合后台运行；
- 人类时间会更多花在定义任务边界、审核结果和处理异常，而不是盯着每个 agent 输出；
- 技能（skills）、subagents、worktrees、background sessions 会越来越像一个本地 agent runtime 的组件。

也可以说，Claude Code 正在把“AI 编程助手”做成一个 **agent operations environment**。

---

## 对 Peter / QCut / OpenClaw 的启发

对我们做 QCut、OpenClaw、Hermes 这类 agent 系统的人来说，Agent view 有几个直接启发：

1. **多 agent 的核心不是 spawn，而是 roster**  
   能启动很多 agent 不难，难的是让用户知道每个 agent 是否还活着、是否卡住、是否有可交付结果。

2. **状态摘要本身是产品功能**  
   用户不想读完整 transcript。每行 1 句高质量摘要、PR link、CI 状态，可能比完整日志更重要。

3. **后台任务需要独立生命周期**  
   不能把 agent 生命周期绑死在一个 terminal 或一个 websocket 上。需要 supervisor、state file、恢复机制、清理机制。

4. **写文件必须默认隔离**  
   并行 agent 如果共享同一个工作目录，很快会互相踩。worktree / sandbox / lease 这类隔离层应该是默认能力，而不是高级选项。

5. **人类应该被设计成调度者，而不是 babysitter**  
   好的 agent 产品不是让人一直看输出，而是在关键节点把人拉回来。

---

## 结论

Agent view 看起来像 Claude Code 的一个 Research Preview，但它指向的是更大的方向：coding agent 的竞争，正在从“单个 agent 有多聪明”转向“多 agent 能不能被稳定调度”。

Anthropic 这次没有发布一个华丽的 Web IDE，而是在 CLI 里加了一个很工程化的控制面：能派发、能后台、能查看状态、能 peek、能 attach、能自动 worktree 隔离、能由 supervisor 托管。

这不是最炫的功能，但可能是最接近真实生产力的功能。

因为真正的 agentic coding，不是让一个 agent 在你面前表演，而是让一组 agent 在后台持续推进，而你只在最需要人的地方出现。
