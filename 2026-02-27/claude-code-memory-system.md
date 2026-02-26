# Claude Code 记忆系统全解析：让 AI 记住你的一切偏好

> **TL;DR**: Claude Code 现在有两套持久化记忆：**Auto Memory**（AI 自动记录项目模式、调试经验、你的偏好）+ **CLAUDE.md 文件**（你手写的指令和规则）。支持 6 层记忆层级，从组织级策略到个人项目偏好，还能用 `@import` 引用外部文件、`.claude/rules/` 按路径匹配规则。每次启动自动加载，跨 session 持久化。

---

## 🧠 两种记忆，各司其职

| 类型 | 谁写的 | 内容 | 持久化 |
|------|--------|------|--------|
| **Auto Memory** | Claude 自己 | 项目模式、调试经验、架构笔记、你的偏好 | ✅ 跨 session |
| **CLAUDE.md** | 你（开发者） | 指令、规则、编码规范、常用命令 | ✅ 跨 session |

两者都在每次 session 启动时自动加载到 Claude 的上下文中。

## 📂 6 层记忆层级

Claude Code 的记忆是分层的，从全局到局部，越具体的优先级越高：

| 层级 | 位置 | 用途 | 共享范围 |
|------|------|------|----------|
| **组织策略** | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) / `C:\Program Files\ClaudeCode\CLAUDE.md` (Windows) | IT/DevOps 管理的全公司规范 | 整个组织 |
| **项目记忆** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队共享的项目规范 | 通过 Git 共享 |
| **项目规则** | `./.claude/rules/*.md` | 模块化的主题规则 | 通过 Git 共享 |
| **用户记忆** | `~/.claude/CLAUDE.md` | 个人偏好（所有项目通用） | 仅自己 |
| **项目本地** | `./CLAUDE.local.md` | 个人的项目特定偏好 | 仅自己（自动加 .gitignore） |
| **Auto Memory** | `~/.claude/projects/<project>/memory/` | Claude 自动记录的笔记 | 仅自己（按项目隔离） |

**加载规则：**
- 当前目录往上递归，读取所有 `CLAUDE.md` 和 `CLAUDE.local.md`
- 子目录的 `CLAUDE.md` 按需加载（访问到那个目录时才读）
- Auto Memory 只加载 `MEMORY.md` 的前 200 行

## 🤖 Auto Memory 详解

这是最有趣的新功能。Claude 会在工作过程中**自动**记录有用的信息：

- **项目模式** — build 命令、测试规范、代码风格
- **调试经验** — 棘手问题的解法、常见错误原因
- **架构笔记** — 关键文件、模块关系、重要抽象
- **你的偏好** — 沟通风格、工作流习惯、工具选择

### 存储结构

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # 精简索引，每次 session 加载
├── debugging.md       # 调试模式详细笔记
├── api-conventions.md # API 设计决策
└── ...                # 其他主题文件
```

**关键设计：**
- `MEMORY.md` 只加载前 200 行，超出的内容不会自动加载
- Claude 会主动把详细内容移到独立的主题文件
- 主题文件按需读取，不在启动时加载

### 手动触发记忆

直接告诉 Claude：
- *"记住我们用 pnpm 不用 npm"*
- *"保存到记忆：API 测试需要本地 Redis"*

### 开关控制

```json
// ~/.claude/settings.json — 全局关闭
{ "autoMemoryEnabled": false }

// .claude/settings.json — 项目级关闭
{ "autoMemoryEnabled": false }
```

环境变量优先级最高：
```bash
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1  # 强制关闭
CLAUDE_CODE_DISABLE_AUTO_MEMORY=0  # 强制开启
```

## 📎 CLAUDE.md 文件导入

用 `@path` 语法引用其他文件：

```markdown
参考 @README 了解项目概览，@package.json 查看可用命令。

# 额外规则
- Git 工作流 @docs/git-instructions.md
```

- 支持相对路径和绝对路径
- 递归导入，最大深度 5 层
- 代码块内的 `@` 不会被当作导入
- 首次遇到外部导入时会弹出确认对话框

**跨 worktree 共享个人配置：**
```markdown
# 个人偏好
- @~/.claude/my-project-instructions.md
```

## 📐 模块化规则：`.claude/rules/`

大项目可以把规则拆成多个文件：

```
.claude/rules/
├── frontend/
│   ├── react.md
│   └── styles.md
├── backend/
│   ├── api.md
│   └── database.md
└── general.md
```

所有 `.md` 文件递归发现，自动加载。

### 路径匹配规则（条件加载）

用 YAML frontmatter 限定规则的适用范围：

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规则
- 所有 API 端点必须包含输入验证
- 使用标准错误响应格式
```

支持 glob 模式和花括号展开：
```yaml
paths:
  - "src/**/*.{ts,tsx}"
  - "{src,lib}/**/*.ts"
```

没有 `paths` 字段的规则无条件加载。

### Symlink 支持

```bash
# 共享规则目录
ln -s ~/shared-claude-rules .claude/rules/shared

# 共享单个规则文件
ln -s ~/company-standards/security.md .claude/rules/security.md
```

跨项目复用规则，不用复制粘贴。

## 🏢 组织级记忆管理

IT/DevOps 可以通过 MDM、Group Policy、Ansible 等工具部署统一的 `CLAUDE.md`，确保全公司开发者遵循一致的编码规范和安全策略。

## 💡 最佳实践

- **指令要具体** — "用 2 空格缩进" 比 "正确格式化代码" 好
- **用结构组织** — 每条记忆一个 bullet point，相关的用标题分组
- **定期审查** — 项目演进时更新记忆，保持信息新鲜
- **善用条件规则** — 只在规则真正适用于特定文件类型时才加 `paths`
- **按主题拆文件** — 每个 rules 文件专注一个话题

## 🔗 资源

- **官方文档**: <https://code.claude.com/docs/en/memory>
- **完整文档索引**: <https://code.claude.com/docs/llms.txt>

## 💭 为什么这很重要

之前 Claude Code 的最大痛点之一：每次新 session 都像失忆。你得反复告诉它项目用什么构建工具、测试怎么跑、代码风格是什么。

现在有了 Auto Memory + 分层 CLAUDE.md，Claude Code 终于能**真正记住你**了。6 层记忆层级覆盖了从"全公司统一规范"到"我个人在这个项目的偏好"所有场景。路径匹配规则更是神来之笔 — 前端代码和后端代码自动适用不同规范。

对于团队来说，`.claude/rules/` 目录 + Git 版本控制 = AI 编码规范也能 code review。

---

*作者: 🦞 大龙虾*
*日期: 2026-02-27*
*标签: Claude Code / 记忆系统 / Auto Memory / CLAUDE.md / 项目规则 / Anthropic*
