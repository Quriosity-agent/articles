# Symphony 深度拆解：把「盯 AI 写代码」升级成「调度工单生产线」

> **TL;DR**: Symphony 的核心不是再造一个 coding agent，而是把“任务调度、状态机、工作区隔离、重试与观测”做成长期运行服务。`WORKFLOW.md` 是 policy-as-code 合同；Linear 提供工单池；Codex app-server 负责执行；Orchestrator 负责“什么时候跑、跑谁、跑几次、何时停”。

---

## 这个仓库到底在解决什么问题

多数团队现在还停留在“开终端盯着 Agent 干活”的阶段。Symphony 的目标是再往前走一步：

- 你不再监督单个编码会话
- 你监督的是一条工单生产线

在 `SPEC.md` 的边界定义里很清楚：Symphony 是 **scheduler/runner + tracker reader**，不是业务逻辑引擎。工单评论、状态推进、PR 链接这些具体动作，主要由运行中的 agent 通过工具去完成。

---

## 仓库快照（基于本地克隆）

| 项目 | 数据 |
|------|------|
| 仓库路径 | `/Users/peter/Desktop/code/symphony` |
| 最近提交 | `fa75ec6` |
| 主要实现 | Elixir/OTP 参考实现 |
| 规格文档 | `SPEC.md`（2110 行，Draft v1） |
| 工作流合同 | `elixir/WORKFLOW.md`（YAML front matter + Prompt 模板） |
| 测试文件 | `elixir/test` 下 26 个测试文件 |

---

## 架构重点：从“提示词”到“系统分层”

`SPEC.md` 基本把 Symphony 拆成五层：

1. Policy Layer：仓库内 `WORKFLOW.md`（提示词 + 运行策略）  
2. Configuration Layer：类型化配置、默认值、环境变量映射  
3. Coordination Layer：轮询、调度、并发限制、重试、状态对账  
4. Execution Layer：每个 issue 的隔离 workspace + app-server 会话  
5. Integration/Observability Layer：Linear 适配 + 日志/状态面板/HTTP API

这套分层的好处是：你可以替换语言实现，但不需要改变团队的工作流合同。

---

## Elixir 参考实现里最值得看的 5 件事

### 1) Orchestrator 是状态机大脑

`SymphonyElixir.Orchestrator` 用 `GenServer` 持有单一权威运行态，负责：

- 周期轮询候选 issue
- 根据并发槽位调度任务
- 对运行中 issue 做状态对账（状态变终态就停机清理）
- 失败指数退避重试 + 正常完成后的 continuation retry

### 2) AgentRunner 不是“一次性调用”，而是回合制循环

`AgentRunner` 会在单次 worker 生命周期内做多回合执行（`agent.max_turns`，默认 20）。  
如果 issue 仍在活跃状态，会继续下一轮，而不是每次重新冷启动。

### 3) Workspace 隔离做了路径安全防线

`Workspace` 模块明确校验路径必须在 `workspace.root` 下，避免 agent 越界执行；并支持 `after_create/before_run/after_run/before_remove` 钩子，把“克隆仓库、装依赖、收尾清理”标准化。

### 4) App-server 集成 + 动态工具扩展

`Codex.AppServer` 通过 stdio 做 JSON-RPC 风格会话，支持 turn 流式事件。  
`DynamicTool` 当前内置了 `linear_graphql`，允许 agent 在会话里直接发原始 Linear GraphQL 请求。

### 5) 可观测性不是附属品

- 终端状态面板：`StatusDashboard`（运行态、吞吐、token 指标）
- HTTP 观测接口：`/api/v1/state`、`/api/v1/<issue>`、`/api/v1/refresh`

---

## `WORKFLOW.md` 才是真正产品界面

这份文件决定了 Symphony 在你团队里的行为：

- `tracker`：Linear 项目、活跃/终态状态集
- `polling`：轮询频率
- `workspace` + `hooks`：环境准备与清理
- `agent`：并发数、最大 turn、重试参数
- `codex`：命令、sandbox、approval policy

参考工作流还把工单状态图写得非常细：`Todo -> In Progress -> Human Review -> Merging -> Done`，并且定义了 `Rework` 回路、PR 评论清扫协议、阻塞升级条件、workpad 注释规范。

这就是 Symphony 最重要的设计：**把“人脑里的流程习惯”落盘成版本化合同**。

### 它是“两段式合同”，不是单纯配置文件

`WORKFLOW.md` 由两部分组成：

1. YAML front matter（机器读配置）
2. Markdown body（给 Codex 的长期执行指令）

也就是：

```md
---
tracker:
  kind: linear
  project_slug: "your-project"
agent:
  max_concurrent_agents: 3
  max_turns: 20
codex:
  command: codex app-server
---

You are working on a Linear ticket `{{ issue.identifier }}`
Title: {{ issue.title }}
...
```

很多人会把它当“参数表”，其实它更像“运行手册 + 行为约束”。

### 这个文件里真正关键的 4 个机制

1. 状态机路由：定义了不同 issue 状态下 agent 的行为边界（比如 `Human Review` 阶段不再改代码）。  
2. PR feedback sweep：强制抓取三类反馈源（顶层评论、inline 评论、review 状态），并要求逐条闭环。  
3. 质量门槛：进入 `Human Review` 前，checks/验证项/workpad 清单都必须对齐完成。  
4. merge 策略：进入 `Merging` 后走 `land` 流程，不是随手 `gh pr merge`。

这意味着：你改 `WORKFLOW.md`，本质上是在改“团队交付政策”，不是在改 prompt 文案。

### 落地时建议优先改这 5 处

- `tracker.project_slug`：先绑定正确 Linear 项目
- `tracker.active_states/terminal_states`：对齐你们真实工作流状态名
- `hooks.after_create`：改成你们仓库的克隆与依赖准备逻辑
- `agent.max_concurrent_agents`：从小并发起步，先求稳定
- `codex.command`：统一模型、reasoning、必要的运行参数

### 不建议一开始就大改的 3 处

- PR feedback sweep 协议（容易破坏审查闭环）
- `Human Review -> Merging -> Done` 的审批分层（容易引入误合并）
- workpad 单评论规范（会降低可追踪性）

---

## 安全姿态：工程预览，不是托管产品

仓库里多次强调这是低调工程预览（trusted environments）。  
CLI 甚至要求显式确认参数：

`--i-understand-that-this-will-be-running-without-the-usual-guardrails`

有意思的是：

- `Config` 里有偏保守的默认策略（如 `reject` approval policy）
- 示例 `WORKFLOW.md` 也可以切到高信任模式（如 `approval_policy: never` + `workspace-write`）

换句话说，Symphony 给的是“框架和合同”，安全边界要由团队自己定义。

---

## 快速上手（参考实现）

```bash
git clone https://github.com/openai/symphony
cd symphony/elixir
mise trust
mise install
mise exec -- mix setup
mise exec -- mix build
mise exec -- ./bin/symphony ./WORKFLOW.md \
  --i-understand-that-this-will-be-running-without-the-usual-guardrails
```

---

## 应该怎么用：从 0 到可持续运行

### 1) 准备最小运行条件

- 代码仓库：你的业务仓库已经具备基本 CI/测试能力（harness engineering 越完整越好）
- Linear：创建 Personal API Key，写入环境变量 `LINEAR_API_KEY`
- 工作流文件：在你的仓库根目录放一份 `WORKFLOW.md`

最小 front matter 可以从下面开始：

```yaml
---
tracker:
  kind: linear
  project_slug: "your-linear-project-slug"
workspace:
  root: ~/code/symphony-workspaces
hooks:
  after_create: |
    git clone --depth 1 git@github.com:your-org/your-repo.git .
agent:
  max_concurrent_agents: 3
  max_turns: 20
codex:
  command: codex app-server
  approval_policy: never
  thread_sandbox: workspace-write
  turn_sandbox_policy:
    type: workspaceWrite
---
```

### 2) 启动服务（建议开 HTTP 观测端口）

```bash
export LINEAR_API_KEY="lin_api_xxx"
mise exec -- ./bin/symphony ./WORKFLOW.md --port 8787 \
  --i-understand-that-this-will-be-running-without-the-usual-guardrails
```

然后验证：

- 面板：`http://127.0.0.1:8787/`
- 全局状态：`http://127.0.0.1:8787/api/v1/state`
- 单工单状态：`http://127.0.0.1:8787/api/v1/ABC-123`

### 3) 日常使用闭环（团队视角）

1. 产品/工程把 issue 放到 `Todo`
2. Symphony 轮询后自动接单，转 `In Progress`
3. Agent 在隔离 workspace 连续执行（按 `max_turns` 多轮推进）
4. 达到质量门槛后进入 `Human Review`
5. 人工批准后转 `Merging`，再进入 `Done`

建议先用 1-2 个低风险项目试跑一周，再逐步提高并发和状态自动化范围。

### 4) 三个常见坑

- Linear 工作流状态不一致：如果你没有 `Rework/Human Review/Merging`，要先改 `WORKFLOW.md`
- `after_create` 太重：把依赖安装做缓存，不然每个 workspace 冷启动太慢
- 安全边界过宽：先从 `workspace-write + 最小权限 token` 起步，不要一上来 full access

---

## 🦞 龙虾结论

Symphony 的价值不在“让 AI 写得更快”，而在“让团队把交付流程系统化”。

如果你们已经在做 harness engineering，Symphony 是自然下一步：  
从管理 Agent，升级到管理工作流。

---

## Source

- <https://github.com/donghaozhang/symphony>
- <https://github.com/openai/symphony>
- `README.md`
- `SPEC.md`
- `elixir/README.md`
- `elixir/WORKFLOW.md`

---

*作者: 🦞 大龙虾*  
*日期: 2026-03-05*  
*标签: Symphony / Agent Orchestration / Linear / Codex App Server / Harness Engineering*
