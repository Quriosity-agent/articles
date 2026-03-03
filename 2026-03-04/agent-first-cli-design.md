# Agent-First CLI 设计：从 Unix 管道到 AI Agent 的 50 年演进

> **TL;DR**: 1978 年 Unix 哲学说"程序输出应该能成为另一个程序的输入"。50 年后，这条原则的最佳实现从 `grep/awk` 变成了 `--json + AI Agent`。本文以 Vercel CLI、QCut CLI 为例，解析 **Agent-First CLI** 的设计模式。

---

## 📜 Unix 哲学的核心

Doug McIlroy（管道发明者）1978 年的三条原则：

```
1. 每个程序做好一件事
2. 程序的输出应该能成为另一个程序的输入  ← 关键
3. 尽早设计和构建软件来试验
```

**第 2 条是一切的基础。** 管道 `|`、重定向 `>`、xargs — 都是为了让程序输出流向下一个程序。

## 📊 CLI 输出格式的 50 年演进

```
1970s: 纯文本 → grep/awk/sed 解析
       ls -l | awk '{print $5}'
       ↑ 脆弱：输出格式变了就全断

1990s: 结构化选项 → --format, -o 自定义列
       ps -o pid,comm
       ↑ 进步：减少猜测，但仍是文本

2020s: JSON 输出 → --json, --format=json
       gh pr list --json number,title
       docker inspect container_id
       ↑ 标准化：结构化数据，字段名即 API

2025s: Agent-First → JSON + Markdown guide + 自发现
       vercel integration discover --format=json
       vercel integration guide neon
       ↑ 当前：CLI 为 AI Agent 设计
```

## 🔑 Agent-First CLI 的 5 个设计原则

### 原则 1: 双模输出

```bash
# 人类模式（默认）
$ qcut list-models
┌──────────────┬──────────────┬────────┐
│ Model        │ Type         │ Cost   │
├──────────────┼──────────────┼────────┤
│ Kling 2.6    │ text2video   │ $0.35  │
│ FLUX.1 Dev   │ text2image   │ $0.003 │
└──────────────┴──────────────┴────────┘

# Agent 模式
$ qcut list-models --json
[{"id":"kling-2.6-pro","type":"text2video","cost":0.35},
 {"id":"flux-1-dev","type":"text2image","cost":0.003}]
```

**同一个命令，两种输出。** 人类看表格，Agent 读 JSON。

### 原则 2: 统一错误格式

```bash
# 成功
{"status":"ok","data":{...}}

# 失败
{"status":"error","error":"Project not found","code":"NOT_FOUND"}

# Agent 不需要猜 exit code 的含义
```

### 原则 3: 长任务异步化

```bash
# 提交任务
$ qcut generate --model kling-2.6 --prompt "日落" --json
{"status":"pending","jobId":"j-abc123"}

# 轮询状态
$ qcut status --job-id j-abc123 --json
{"status":"running","progress":65}

# 完成
$ qcut status --job-id j-abc123 --json
{"status":"done","output":"generated.mp4","took":45}
```

### 原则 4: 参数自发现

```bash
# Agent 通过 --help 发现需要什么参数
$ qcut generate --help --json
{"command":"generate",
 "required":["model","prompt"],
 "optional":["output","seed","aspect-ratio"],
 "models":["kling-2.6-pro","flux-1-dev",...]}

# Agent 不需要读文档，--help 就是 API schema
```

### 原则 5: 人机协作暂停点

```bash
# 需要人类决策时暂停
$ vercel integration add neon --json
{"status":"pending_approval",
 "message":"Accept Terms of Service?",
 "approve":"vercel integration add neon --confirm"}

# Agent 把决策转给人类，人类确认后继续
```

## 🏗️ 实际案例对比

### Vercel CLI (Agent-First 典范)

```bash
# 发现 → 安装 → 获取指南 → 自动集成
vercel integration discover --format=json
vercel integration add neon --format=json  
vercel integration guide neon  # 返回 Markdown
# Agent 读 Markdown → 写集成代码 → 部署
```

### QCut CLI (正在演进)

```bash
# 已有
bun run pipeline list-models --json
bun run pipeline editor:media:list --project-id xxx --json
bun run pipeline editor:timeline:export --project-id xxx --json

# 命名空间设计：
# editor:*     → 编辑器操作
# pipeline:*   → AI pipeline  
# project:*    → 项目管理
```

### GitHub CLI (成熟标杆)

```bash
# 任意字段组合的 JSON 输出
gh pr list --json number,title,author
gh issue list --json number,labels,assignees
gh api repos/{owner}/{repo} --jq '.stargazers_count'
```

## 🔄 Agent 消费 CLI 的完整链路

```
用户: "帮我把这个视频加上字幕然后导出"
  ↓
AI Agent 规划:
  1. qcut editor:media:list --project-id xxx --json  → 获取视频
  2. qcut pipeline:transcribe --input video.mp4 --json  → 生成字幕
  3. qcut editor:timeline:add-subtitle --json  → 添加到时间线
  4. qcut editor:export --format mp4 --json  → 导出
  ↓
每一步 JSON 输出 → Agent 解析 → 决定下一步
  ↓
最终输出: "字幕已添加，视频已导出到 output.mp4"
```

## 💡 为什么 JSON 是"新时代的纯文本"

| | 1978 纯文本 | 2026 JSON |
|--|-----------|-----------|
| 通用性 | 所有程序都能读 | 所有语言都能解析 |
| 管道 | `grep/awk/sed` | `jq` / Agent |
| Schema | 无（靠约定） | 有（字段名即 Schema） |
| 消费者 | 人类 + 脚本 | 人类 + 脚本 + **AI Agent** |

## 🦞 龙虾点评

### 这不是新概念，是老概念的新实现

Unix 哲学从来不是"必须输出纯文本"。它说的是"让你的输出能被下一个程序消费"。

```
1978: "下一个程序" = grep
2026: "下一个程序" = AI Agent

手段变了，原则没变。
```

### QCut 的位置

QCut 已经有 `pipeline` 命令和 `--json` 支持，这比大多数视频编辑器领先。下一步：

```
1. 统一所有命令的 JSON 输出格式
2. 加 --help --json（参数自发现）
3. 长任务加 jobId + 轮询
4. MCP Server 直接包装 CLI JSON 输出
```

### Agent-First ≠ Agent-Only

最好的 CLI 同时服务人类和 Agent。默认输出给人看，`--json` 给 Agent 用。两者不冲突。

## 🔗 资源

- **Unix 哲学原文**: <https://en.wikipedia.org/wiki/Unix_philosophy>
- **Vercel CLI Agent 更新**: <https://vercel.com/changelog/vercel-cli-for-marketplace-integrations-optimized-for-agents>
- **GitHub CLI JSON**: <https://cli.github.com/manual/gh_pr_list>
- **jq**: <https://jqlang.github.io/jq/>

---

*作者: 🦞 大龙虾*
*日期: 2026-03-04*
*标签: Unix 哲学 / Agent-First CLI / JSON / QCut CLI / Vercel CLI / 管道*
