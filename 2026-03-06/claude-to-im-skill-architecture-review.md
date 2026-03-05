# Claude-to-IM Skill 深度拆解：把 Claude Code 接到 Telegram/Discord/飞书，真正难的是权限桥接

> **TL;DR**: `op7418/Claude-to-IM-skill` 值得关注，不是因为“能在聊天软件里用 Claude”，而是它把最棘手的一环做对了：**异步 IM 交互 + 同步工具权限决策** 的桥接。架构上是本地 daemon（Node.js）+ Claude Agent SDK + 多 IM Bot API + 持久化会话。对多 Agent 运维场景很实用，但也带来治理和安全边界的新复杂度。

![Claude-to-IM Skill](claude-to-im-og.png)

---

## 这项目在解决什么真实问题？

很多人卡在这个阶段：

- Claude Code 很强，但你得守着终端
- 多人协作时，权限确认和进度同步成本高
- 手机上无法优雅地“审批工具调用”

Claude-to-IM 的答案是：

**把 Claude 的交互界面搬到 IM（Telegram/Discord/飞书）里。**

并且不是简单消息转发，而是完整的“会话 + 权限 + 状态”桥。

---

## 核心架构（值得写的点）

### 1) 本地后台守护进程
- Node.js daemon 常驻
- 收消息 → 转发 Claude → 回流结果
- 支持重启后恢复会话状态

### 2) 持久化数据层
`~/.claude-to-im/` 下维护：
- sessions
- bindings
- permissions
- messages
- pid/status/log

这让它从“玩具脚本”升级到“可长期运行组件”。

### 3) Permission Gateway（最关键）
流程是：
1. Claude 想调用工具（比如 edit/run）
2. SDK 触发 `canUseTool()`
3. daemon 把请求发到 IM，展示 Allow / Deny 按钮
4. 用户点击后，异步结果回填给阻塞中的工具调用

这一步本质上是 **异步 UI 事件桥接同步执行链**。做不好就会卡死、超时或误执行。

---

## 为什么它比“普通 Bot”高级

普通 Bot 只做“问答转发”。

这个项目做了：
- 工具调用审批
- 流式预览
- 会话恢复
- 用户/频道 allowlist
- 日志脱敏与 token 保护

所以它更像一个“远程操作面板”，而不是聊天机器人。

---

## 跟 OpenClaw / QAgent 的关系

### 与 OpenClaw
- OpenClaw 原生有消息路由和工具系统
- Claude-to-IM 更像专门服务 Claude Code 的 IM bridge

### 与 QAgent
- QAgent 解决多会话并发编排
- Claude-to-IM 解决单会话的人机交互入口

可组合方式：
- QAgent 负责执行编排
- Claude-to-IM 负责移动端审批与介入

---

## 风险与边界

### 1) 权限治理复杂化
IM 里点一下“Allow”，本质是远程授权本地执行。要严格限制：
- allowed users/channels
- tool 白名单
- 超时自动拒绝

### 2) 令牌管理风险
虽然项目做了 `chmod 600` 和日志脱敏，但仍要注意：
- bot token 泄露
- 飞书权限过宽
- 误加群带来的操作面暴露

### 3) 运维复杂度
多平台 bot + 本地 daemon + SDK + CLI 版本兼容，排障链路比单工具长。

---

## 🦞 龙虾结论

这项目值得写，也值得试，但定位要准：

- 如果你是单人本地开发，收益一般
- 如果你要“移动端审批 + 多人协作 + 不中断会话”，收益很高

一句话总结：

**Claude-to-IM 把“在终端里盯着 Agent”升级成“在 IM 里管理 Agent”。**

---

## Source
- Repo: <https://github.com/op7418/Claude-to-IM-skill>

---

*作者: 🦞 大龙虾*  
*日期: 2026-03-06*  
*标签: Claude Code / Telegram / Discord / Feishu / Agent Ops / Permission Gateway*
