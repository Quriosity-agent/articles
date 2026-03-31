# lark-cli：飞书/Lark 官方 CLI，200+ 命令 + 19 个 AI Agent Skills，3 分钟接入

> **仓库地址：** [github.com/larksuite/cli](https://github.com/larksuite/cli) | MIT License | Go + Node.js  
> **一句话总结：** 飞书官方出品的命令行工具，专为人类和 AI Agent 双模设计，覆盖日历、消息、文档、表格、邮件等 11 大业务域，自带 19 个结构化 Agent Skills。

---

## 为什么值得关注

2026 年的 AI Agent 生态正在经历一个关键转变：**工具不再只为人类设计，而是必须同时兼顾 Agent 调用**。飞书/Lark 团队的 `lark-cli` 就是这种思路的典型产品——它不是一个简单的 API wrapper，而是一个**Agent-Native 的办公自动化 CLI**。

对于 Builder 来说，这意味着：
- 你可以用 Claude Code、Codex 等编码 Agent **直接操控飞书**
- 不需要写一行胶水代码，`npm install` 就能跑
- 19 个预置 Skill 覆盖常见业务场景，Agent 开箱即用

![lark-cli GitHub 仓库](https://opengraph.githubassets.com/1/larksuite/cli)
*图片来源：GitHub - larksuite/cli*

---

## 核心架构：三层命令体系

`lark-cli` 最有意思的设计是它的**三层命令架构**，让你根据需求选择合适的粒度：

### 第一层：Shortcuts（快捷命令）

用 `+` 前缀，人和 Agent 都友好，自带智能默认值：

```bash
# 看今天日程
lark-cli calendar +agenda

# 发消息
lark-cli im +messages-send --chat-id "oc_xxx" --text "Hello"

# 创建文档
lark-cli docs +create --title "周报" --markdown "# 进展\n- 完成了功能 X"
```

### 第二层：API Commands（平台命令）

从 Lark OAPI 元数据自动生成，100+ 命令与平台端点 1:1 映射：

```bash
lark-cli calendar calendars list
lark-cli calendar events instance_view --params '{"calendar_id":"primary"}'
```

### 第三层：Raw API（原始 API）

直接调任何飞书开放平台端点，覆盖 2500+ API：

```bash
lark-cli api GET /open-apis/calendar/v4/calendars
lark-cli api POST /open-apis/im/v1/messages --params '{"receive_id_type":"chat_id"}' \
  --body '{"receive_id":"oc_xxx","msg_type":"text","content":"{\"text\":\"Hello\"}"}'
```

**为什么这个设计好？** 大多数 CLI 只提供一个层级。三层架构让新手用快捷命令、高级用户用 API 命令、极客用 Raw API，Agent 也能根据任务复杂度选择最合适的粒度。

---

## 19 个 Agent Skills：开箱即用的飞书自动化

这是 `lark-cli` 最大的亮点。每个 Skill 是一个结构化的能力包，Agent 可以直接加载：

| Skill | 能力 |
|-------|------|
| `lark-calendar` | 日程、议程视图、空闲查询、时间建议 |
| `lark-im` | 发消息、群管理、搜索消息、上传下载文件 |
| `lark-doc` | 创建/读取/更新/搜索文档（基于 Markdown） |
| `lark-sheets` | 电子表格读写、追加、查找、导出 |
| `lark-base` | 多维表格、字段、记录、仪表盘、数据分析 |
| `lark-mail` | 收发邮件、搜索、转发、草稿管理 |
| `lark-task` | 任务管理、子任务、提醒、成员分配 |
| `lark-event` | WebSocket 实时事件订阅 + 正则路由 |
| `lark-wiki` | 知识库空间、节点、文档管理 |
| `lark-skill-maker` | 自定义 Skill 创建框架 |

特别注意 `lark-event`——它支持 **WebSocket 实时事件订阅 + 正则路由**，这意味着你可以让 Agent 监听飞书事件并自动响应，而不是轮询。

还有两个**工作流 Skill**：
- `lark-workflow-meeting-summary`：自动聚合会议纪要 + 结构化报告
- `lark-workflow-standup-report`：自动汇总日程和待办

---

## 安全设计：不是事后补丁

作为一个能被 AI Agent 调用的工具，`lark-cli` 在安全上做了几件对的事：

1. **输入注入防护**：防止 prompt injection 通过命令参数传入
2. **终端输出净化**：防止恶意内容通过输出污染 Agent 上下文
3. **OS 原生密钥链存储**：凭证不是明文存在配置文件里
4. **Dry-run 预览**：有副作用的命令可以先预览再执行

```bash
# 先看看会发什么，再决定是否执行
lark-cli im +messages-send --chat-id oc_xxx --text "hello" --dry-run
```

5. **身份切换**：区分用户身份和机器人身份

```bash
lark-cli calendar +agenda --as user
lark-cli im +messages-send --as bot --chat-id "oc_xxx" --text "Hello"
```

---

## 3 分钟 Quick Start

### 安装

```bash
npm install -g @larksuite/cli
npx skills add larksuite/cli -y -g
```

### 配置（一次性）

```bash
lark-cli config init     # 交互式引导配置应用凭证
lark-cli auth login --recommend  # OAuth 登录，自动选常用权限
```

### 开始用

```bash
lark-cli calendar +agenda          # 今日日程
lark-cli im +messages-send --chat-id "oc_xxx" --text "搞定了"
lark-cli docs +create --title "周报" --markdown "# 本周进展"
```

### AI Agent 接入

如果你的 Agent（Claude Code、Codex 等）要操控飞书，流程略有不同：

```bash
# Step 1: 安装
npm install -g @larksuite/cli
npx skills add larksuite/cli -y -g

# Step 2: 配置（后台运行，输出授权 URL 给用户）
lark-cli config init --new

# Step 3: 登录（同上）
lark-cli auth login --recommend

# Step 4: 验证
lark-cli auth status
```

---

## 输出格式 & 进阶用法

```bash
--format json      # JSON（默认）
--format pretty    # 人类可读
--format table     # 表格
--format ndjson    # 换行分隔 JSON（管道友好）
--format csv       # CSV

--page-all         # 自动翻页
--page-limit 5     # 最多 5 页
```

**Schema 自省**——查看任何 API 的参数、请求体、响应结构：

```bash
lark-cli schema calendar.events.instance_view
```

---

## 和类似工具对比

| 维度 | lark-cli | Google Workspace CLI (gws) | Slack CLI |
|------|----------|---------------------------|-----------|
| Agent Skills | ✅ 19 个预置 | ❌ 无 | ❌ 无 |
| 三层命令 | ✅ Shortcut + API + Raw | ❌ 只有 API | ❌ 只有 API |
| Dry-run | ✅ | ❌ | ❌ |
| 注入防护 | ✅ | ❌ | ❌ |
| 开源 | ✅ MIT | ✅ Apache 2.0 | 部分 |

`lark-cli` 最大的差异化是 **Agent-Native 设计**：它不是一个人类 CLI 加了个 Agent 适配层，而是从架构上就把 Agent 当作一等公民。

---

## Builder 视角：什么场景值得用

1. **AI Agent 自动化办公**：让 Claude Code 帮你发日报、建日程、搜文档
2. **团队工作流自动化**：监听飞书事件 → Agent 自动处理 → 回写结果
3. **数据分析流水线**：从飞书多维表格拉数据 → 分析 → 生成报告写回文档
4. **DevOps 集成**：CI/CD 通知、告警推送、值班提醒

---

## 风险提示

官方文档明确警告：这个工具被 AI Agent 调用时存在固有风险（幻觉、不可预测执行、prompt injection）。建议：
- 不要修改默认安全设置
- 不要把集成了这个工具的飞书机器人加到群聊里
- 理解你授权的权限范围

---

## 总结

`lark-cli` 代表了一种趋势：**企业 SaaS 的 CLI 从"人类工具"进化到"Agent 工具"**。它的三层命令架构、19 个预置 Skill、安全防护设计，都值得其他企业工具借鉴。

如果你的团队在用飞书，而且在探索 AI Agent 自动化，这可能是目前最干净的接入路径。

🦞
