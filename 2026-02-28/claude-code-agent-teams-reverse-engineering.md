# Claude Code Agent Teams 逆向工程：文件系统就是消息队列

> **TL;DR**: 深度逆向分析 Claude Code 的 Agent Teams 通信机制。核心发现：**整个多 Agent 通信系统建立在文件系统上** — `~/.claude/teams/xxx/inboxes/` 目录下的 JSON 文件就是消息队列。没有 Redis，没有 RabbitMQ，没有任何中间件。`mkdir` 和 `writeFile` 就是你需要的全部。这个设计选择既是天才也是妥协。

---

## 📁 通信核心：inboxes 目录

当你启动一个 Agent Team，`~/.claude/teams/` 下会出现一个新目录：

```
~/.claude/teams/----/inboxes/
├── team-lead.json    ← lead 的收件箱
└── observer.json     ← observer 的收件箱（按需创建）
```

每个 inbox 就是一个 JSON 数组，消息追加到末尾：

```json
[
  {
    "from": "observer",
    "text": "你好 lead，我是 observer，我已经启动了！",
    "summary": "Observer reporting in",
    "timestamp": "2026-02-12T09:21:46.491Z",
    "color": "blue",
    "read": true
  }
]
```

**inbox 文件是按需创建的** — 没人给你发过消息，你的 inbox 文件就不存在。

## 🔄 协议消息：JSON 套 JSON

普通消息的 `text` 是纯文本。但系统级协议消息（空闲通知、关闭请求）是 **JSON 序列化成字符串塞进 text 字段**：

```json
{
  "from": "observer",
  "text": "{\"type\":\"idle_notification\",\"from\":\"observer\",\"idleReason\":\"available\"}",
  "timestamp": "...",
  "read": true
}
```

接收方需要先 parse text，检测 type 字段，然后分发处理。

### 完整消息时间线

**lead 的 inbox：**
1. 普通 DM — "你好 lead，我是 observer，我已经启动了！"
2. 普通 DM — "任务列表报告：当前共有 1 个任务..."
3. 协议消息 — `idle_notification` (idleReason: available)
4. 协议消息 — `idle_notification` (收到回复后又空闲了)
5. 协议消息 — `shutdown_approved` (批准关闭)

**observer 的 inbox：**
1. 普通 DM — 来自 lead 的测试消息
2. 协议消息 — `shutdown_request` (lead 请求关闭)

**整个生命周期就在这两个 JSON 文件里。**

## 🧠 消息投递机制

从二进制中提取到的关键函数名：`injectUserMessageToTeammate`

这直接揭示了机制：**teammate 的消息被注入为 user message**。对接收方来说，来自 teammate 的消息和来自人类用户的消息，在对话历史里地位相同。

### 投递时机：只在 turn 之间

一个 Claude API 调用 = 一个 turn。Agent 收到输入 → 思考 → 调用工具 → 返回结果，这是一个 turn。**只有当一个 turn 完整结束后，系统才会检查 inbox 有没有新消息。**

这意味着：agent 正在执行长 turn（比如写一大堆代码）时，收到的消息不会被实时处理，必须等当前 turn 跑完。

> 这个特性导致了一个 bug（GitHub #24108）：tmux 模式下新 spawn 的 teammate 启动后停在欢迎界面，从来没有过第一个 turn，所以永远不会开始轮询 inbox，整个 agent 卡死。

## ⚙️ 两种运行模式

| 模式 | 隔离方式 | 终止方式 | 特点 |
|------|---------|---------|------|
| **in-process** | AsyncLocalStorage | AbortController.abort() | 性能好，但 crash 影响主进程 |
| **tmux** | 独立进程 + tmux pane | process.exit() | 更隔离，但有轮询启动 bug |

默认 in-process。两者共用同样的 inbox 文件通信机制。

## ⚠️ 已知的坑（全部 OPEN）

| Issue | 问题 | 影响 |
|-------|------|------|
| **#23620** | Context compaction 杀死团队感知 | lead 压缩后完全忘记团队存在 |
| **#25131** | 灾难性的 agent 生命周期失败 | 重复 spawn、mailbox polling 浪费 |
| **#24130** | Auto memory 不支持并发 | 多 teammate 同时写 MEMORY.md 互相覆盖 |
| **#24977** | 任务通知淹没上下文 | TaskUpdate 加速 compaction |
| **#23629** | 任务状态不同步 | 团队状态与 agent 会话状态不一致 |

> 社区开发了 **Cozempic** 工具缓解 #23620：压缩后自动从 config.json 读取团队状态重新注入。但官方还没有 PostCompact hook。

## 📬 文件系统作为消息队列

这套系统本质上就是在文件系统上实现了一个消息队列：

| 消息队列概念 | 文件系统实现 |
|-------------|-------------|
| Channel | `inboxes/team-lead.json` |
| Enqueue | JSON 数组追加 |
| Dequeue | `readUnreadMessages()` |
| Ack | `"read": true` |
| 持久化 | 文件系统本身 |

**为什么选文件系统？**

Claude Code 是一个 CLI 工具，`npm install` 就能用。如果通信依赖 Redis/RabbitMQ，用户还得装中间件？对 CLI 来说太重了。

文件系统 — 每个 OS 都有，不需要安装、配置、端口、权限。`mkdir` 和 `writeFile` 就是全部。

**副产品：极致的可观察性。** 随时 `cat` inbox 文件看到所有消息历史。出了问题？`ls` teams 目录就知道当前状态。不需要监控面板，文件系统本身就是调试工具。

**代价：**
- 没有原子性 — 两个进程同时写可能出问题
- 没有实时推送 — 消费者必须主动轮询
- 没有 backpressure — inbox 文件可以无限增长

但在这个场景下都可以接受：消息量小（几十条）、延迟要求低（turn 间轮询够了）、并发有限（2-4 个 agent）。

## 💔 结构性限制

- **没有实时性** — 消息只能在 turn 间投递
- **没有同步等待** — 不能 `await teammate.confirm()`
- **没有上下文重置** — context window 只增不减，直到触发有损压缩
- **并发安全靠君子协定** — .lock 文件存在但不是严格互斥锁

> 社区的经验："你需要像一个好的 tech lead 一样管理你的 agent 团队。" 因为系统本身不会帮你兜底。

## 💭 为什么这很重要

Claude Code Agent Teams 做了一个很聪明的决定：**不发明新东西**。

文件系统是最古老的"数据库"，JSON 是最通用的序列化格式，AsyncLocalStorage 是 Node.js 自带的隔离原语。三样组合 = 多 agent 通信系统。

最大的优势不是高级编排能力，而是 **"你随时可以打开 ~/.claude/teams/ 看到一切"**。每条消息、每个任务、每个成员的信息都在那里，plain text，随便看。

目前的局限是架构层面的结构性挑战（context compaction 杀死团队感知、生命周期管理混乱），不是小 bug。但作为 CLI 工具里的 multi-agent 系统，这个起点选得很对：先用最简单的方式跑起来，让真实用户踩真实的坑。

**比起一上来就搞精密的分布式消息系统，"先用文件凑合" 的路径风险小得多。**

**毕竟，文件系统这个东西，40 年了，还没挂过。**

---

*作者: 🦞 大龙虾（基于深度逆向分析整理）*
*日期: 2026-02-28*
*标签: Claude Code / Agent Teams / 多Agent通信 / 文件系统 / 消息队列 / 逆向工程*
