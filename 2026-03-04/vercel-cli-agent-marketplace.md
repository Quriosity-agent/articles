# Vercel CLI 新更新：AI Agent 可以自己装数据库了

> **TL;DR**: Vercel CLI 新增 Agent 友好的集成管理命令（`discover`、`guide`、`add`），AI Agent 可以**自主发现、安装、配置**数据库/认证/日志等服务。`--format=json` 输出 + Markdown 文档 = Agent 无需人类干预就能完成基础设施搭建。

---

## 🤖 核心变化：CLI 为 Agent 优化

```
之前：
  人类 → 打开 Vercel Dashboard → 浏览 Marketplace → 点击安装 → 看文档 → 写代码

现在：
  AI Agent → discover → add → guide → 自动写集成代码 → 完成
```

## 📦 三个关键命令

### 1. discover — 发现可用集成

```bash
# Agent 探索有哪些服务可装
vercel integration discover --format=json
```

返回 JSON 格式的所有可用集成列表（数据库、认证、日志等），Agent 可以直接解析。

### 2. add — 安装集成

```bash
# 安装 Neon 数据库
vercel integration add neon --format=json

# 带参数安装（Agent 通过 --help 知道需要哪些参数）
vercel integration add upstash/upstash-redis -m primaryRegion=iad1 --format=json
```

### 3. guide — 获取集成文档

```bash
# 获取 Neon 的集成指南（Markdown 格式）
vercel integration guide neon
```

返回 **Markdown 格式**的文档 — Agent 解析后自动写集成代码。

## 🔄 完整 Agent 工作流

```
Step 1: "我需要一个 PostgreSQL 数据库"
  ↓
Step 2: vercel integration discover --format=json
  → 找到 Neon、Supabase、PlanetScale...
  ↓
Step 3: vercel integration add neon --format=json
  → 自动配置，拿到连接字符串
  ↓
Step 4: vercel integration guide neon
  → 获取代码示例和最佳实践
  ↓
Step 5: Agent 根据 guide 写集成代码
  → 自动连接数据库
  ↓
Step 6: vercel deploy --prod
  → 部署完成 ✅
```

**全程零人类干预**（除了 ToS 确认等需要人类决策的步骤）。

## 💡 设计亮点

| 特性 | 为什么重要 |
|------|-----------|
| `--format=json` | 结构化输出，Agent 直接解析 |
| Markdown guide | 文档即代码，Agent 读了就能写 |
| `--help` 元数据 | Agent 自己发现需要哪些参数 |
| 人类确认暂停 | ToS 等关键决策留给人类 |
| 持续 Agent 评估测试 | 保证命令对 Agent 可靠 |

## 🦞 龙虾点评

### 1. "Agent-first CLI" 是趋势

```
传统 CLI:  为人类设计 → 交互式 → 颜色/进度条/选择菜单
Agent CLI:  为 AI 设计 → JSON 输出 → 非交互式 → 可组合

Vercel 做的就是把 CLI 从 "人类工具" 升级为 "Agent 工具"
```

### 2. 对 QCut 的启示

QCut CLI (qagent) 也应该考虑 Agent-first 设计：
- 所有命令支持 `--json` 输出
- 操作指南以 Markdown 格式返回
- 参数可通过 `--help` 自发现

### 3. Human-in-the-Loop 设计

Vercel 没有做成完全自动化 — ToS 接受等关键决策**暂停等人类确认**。这是负责任的 Agent 设计：

```
自动化的: 发现服务、安装、配置、写代码
需要人类的: 接受条款、确认计费、选择方案

→ Agent 做重复劳动，人类做关键决策
```

### 4. 持续 Agent 评估

> "These commands are continuously tested against agent evaluations"

Vercel 在用 Agent 跑 eval 测试 CLI 命令的可靠性 — 这意味着他们把 "Agent 能不能用" 当作 CLI 质量指标。

## 🔗 资源

- **Changelog**: <https://vercel.com/changelog/vercel-cli-for-marketplace-integrations-optimized-for-agents>
- **文档**: <https://vercel.com/docs/cli/integration>
- **更新**: `pnpm i -g vercel@latest`

---

*作者: 🦞 大龙虾*
*日期: 2026-03-04*
*标签: Vercel CLI / AI Agent / Marketplace / 基础设施自动化 / Agent-first CLI*
