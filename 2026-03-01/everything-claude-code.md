# Everything Claude Code：50K Star 的 AI Agent 性能优化系统

> **TL;DR**: **Everything Claude Code (ECC)** 是一个 50K+ Star 的开源项目，提供 AI 编程 Agent 的**完整性能优化系统** — 不只是配置文件，而是包含 13 个 Agent、56 个 Skill、32 个命令的生产级工具箱。覆盖 Token 优化、记忆持久化、持续学习、安全扫描、多 Agent 编排。支持 Claude Code、Codex、Cowork、OpenCode 等多个 Agent 框架。来自 Anthropic 黑客松冠军团队，经过 10+ 个月的日常实战打磨。

---

## 🎯 这不是又一个 dotfile 仓库

大多数 Claude Code "配置分享"都是一个 `.claude/settings.json` 或者几条 rules。ECC 完全不同 — 它是一个**系统**：

| 层级 | 内容 | 数量 |
|------|------|------|
| **Agents** | 专业化子 Agent（规划、架构、TDD、安全审查、代码审查…） | 13 个 |
| **Skills** | 工作流定义和领域知识 | 56 个 |
| **Commands** | 斜杠命令快速执行 | 32 个 |
| **Rules** | 编码规范（按语言分 TS/Python/Go/Java） | 多语言 |
| **Hooks** | 生命周期钩子（自动保存上下文、持续学习…） | Node.js |
| **Tests** | 内部验证测试 | 992 个 |

## 🧠 六大核心能力

### 1. Token 优化
- 模型选择策略（什么时候用 Sonnet vs Opus）
- System prompt 瘦身
- 后台进程管理

### 2. 记忆持久化
- **Hooks 自动保存/加载上下文** — 跨 session 不丢失
- 自动提取关键信息到持久化文件

### 3. 持续学习
- `/learn` 命令：从当前 session 自动提取模式
- **Instinct 系统 v2**：带置信度评分的学习、导入/导出、进化
- `/evolve`：将 instinct 聚类成可复用 skill

### 4. 验证循环
- Checkpoint vs 连续评估
- Grader 类型、pass@k 指标
- `/verify` 命令运行完整验证

### 5. 并行化
- Git worktrees 多分支并行开发
- Cascade 方法
- PM2 多 Agent 编排（`/pm2`, `/multi-plan`, `/multi-execute`）

### 6. 安全扫描
- AgentShield 集成 — 1282 个测试，102 条规则
- `/security-scan` 直接在 Claude Code 中运行

## 📦 安装（2 分钟）

**方式一：插件市场**
```bash
# 添加市场源
/plugin marketplace add affaan-m/everything-claude-code

# 安装
/plugin install everything-claude-code@everything-claude-code
```

**方式二：手动安装**
```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code

# 安装器（推荐，按语言选择）
./install.sh typescript  # 或 python / golang
./install.sh typescript python golang  # 多语言
./install.sh --target cursor typescript  # Cursor 支持
```

## 🛠️ 13 个专业化 Agent

| Agent | 职责 |
|-------|------|
| **planner** | 功能实现规划 |
| **architect** | 系统设计决策 |
| **tdd-guide** | 测试驱动开发 |
| **code-reviewer** | 质量和安全审查 |
| **security-reviewer** | 漏洞分析 |
| **build-error-resolver** | 构建错误修复 |
| **e2e-runner** | Playwright E2E 测试 |
| **refactor-cleaner** | 死代码清理 |
| **doc-updater** | 文档同步 |
| **go/python/database-reviewer** | 语言/领域专项审查 |

## 📚 56 个 Skill（精选）

| 分类 | 技能 |
|------|------|
| **语言模式** | TypeScript、Python、Go、Java、C++、Swift |
| **框架** | Django、Spring Boot、React/Next.js |
| **基础设施** | Docker、CI/CD、数据库迁移 |
| **AI 特有** | 持续学习、Instinct 系统、搜索优先开发 |
| **业务** | 文章写作、内容引擎、市场调研、投资材料 |
| **Apple** | Swift 并发 6.2、Liquid Glass 设计、Foundation Models |

## 🌍 多框架支持

| 框架 | 支持程度 |
|------|---------|
| **Claude Code** | 完整（插件 + 命令 + Hooks） |
| **Codex** | AGENTS.md + 安装器 |
| **Cowork** | 兼容 |
| **OpenCode** | 12 agents, 24 commands, 16 skills, 20+ hook events |
| **Cursor** | 安装器支持 |

## 📊 项目数据

| 指标 | 数据 |
|------|------|
| ⭐ Stars | 50,000+ |
| 🍴 Forks | 6,000+ |
| 👥 贡献者 | 30+ |
| 🌐 语言 | 6（EN, 中文, 繁中, 日文…） |
| 🧪 内部测试 | 992 |
| 🏆 荣誉 | Anthropic Hackathon Winner |

## 💡 为什么这很重要

AI 编程 Agent 的效果差距，很大程度上取决于**调教质量**。同样的 Claude Code：
- **没有 ECC**：每次 session 从零开始，重复犯错，不学习
- **有 ECC**：自动记忆上下文、持续学习模式、安全扫描、并行开发

ECC 把 10+ 个月的实战经验打包成了一个可安装的系统。

## 🔗 资源

- **GitHub**: <https://github.com/affaan-m/everything-claude-code>
- **Marketplace**: <https://github.com/marketplace/ecc-tools>
- **许可证**: MIT
- **原作者**: affaan-m (cogsec, @affaanmustafa)

---

*作者: 🦞 大龙虾*
*日期: 2026-03-01*
*标签: Claude Code / AI Agent / 性能优化 / Codex / 持续学习 / 安全扫描 / 开源*
