# Linear CLI：不离开终端管理 Linear Issues 的命令行工具

> **TL;DR**: `linear-cli` 是一个开源 CLI 工具，让你在终端里直接管理 Linear issues——列表、创建、启动、评论、生成 PR，全部不用打开浏览器。支持 git 和 jj 版本控制，还内置 AI Agent skill，让 AI 编程助手也能操作 Linear 工作流。对命令行重度用户和 AI coding agent 来说，这是 `gh` 之于 GitHub 的 Linear 版本。

---

## 一句话定义

**linear-cli = 终端里的 Linear 操作面板。**

类似 `gh`（GitHub CLI）的定位，但目标是 [Linear](https://linear.app/) issue tracker：

> List, start, and create PRs for Linear issues. Agent friendly.

---

## 核心能力

### 🎯 Issue 全流程管理

```bash
linear issue list              # 列出分配给你的未开始 issues
linear issue start ABC-123     # 启动某个 issue，自动建分支
linear issue view              # 查看当前分支关联的 issue
linear issue pr                # 用 gh cli 创建 PR，标题/描述自动填充
linear issue create            # 交互式创建新 issue
linear issue comment add       # 添加评论
linear issue update            # 更新 issue 状态/属性
```

### 🌿 Git / jj 深度集成

- **Git**：从分支名自动识别 issue ID（如 `eng-123-my-feature`）
- **jj**：从 commit description 的 `Linear-issue` trailer 识别
- `linear issue start` 自动创建关联分支或添加 trailer

### 📋 项目 & 里程碑

```bash
linear project list                    # 列出项目
linear milestone create --project <id> # 创建里程碑
linear milestone list --project <id>   # 查看里程碑
```

### 📄 文档管理

```bash
linear document create --title "Spec" --content-file ./spec.md
linear document view --raw             # 输出原始 markdown
linear document update --edit          # 用 $EDITOR 编辑
```

### 🤖 AI Agent 友好

这是亮点：CLI 内置了 **skill 文件**，可以直接给 AI coding agent（Claude Code、Cursor 等）使用。Agent 可以：

- 创建/更新 issues
- 管理状态流转
- 在代码工作流中同步 Linear

---

## 安装

```bash
# Homebrew（推荐）
brew install schpet/tap/linear

# Deno
deno install -A --reload -f -g -n linear jsr:@schpet/linear-cli

# 或直接下载 binary
# https://github.com/schpet/linear-cli/releases/latest
```

设置三步：
1. 在 Linear 设置里创建 API key
2. `linear auth login`
3. `cd your-repo && linear config`

---

## 和同类工具对比

| 维度 | linear-cli | Linear Web/Desktop | gh (GitHub CLI) |
|------|-----------|-------------------|-----------------|
| 操作环境 | 终端 | 浏览器/桌面 | 终端 |
| Issue 管理 | ✅ | ✅ | ❌ (GitHub Issues) |
| PR 创建 | ✅ (调用 gh) | ❌ | ✅ |
| AI Agent 集成 | ✅ 内置 skill | ❌ | 部分 |
| VCS 感知 | git + jj | N/A | git |
| 离线 | ❌ | ❌ | ❌ |

---

## 适合谁

### 非常适合
- 终端重度用户（vim/neovim + tmux 工作流）
- 用 Linear 做项目管理的开发团队
- AI coding agent 需要操作 issue tracker
- 同时用 git 和 Linear 的团队（分支名自动关联）

### 不太适合
- 不用 Linear 的团队（专为 Linear 设计）
- 偏好 GUI 操作的非技术人员
- 需要看板/时间线等可视化视图的场景

---

## 对 Agent 工作流的启发

linear-cli 的 AI skill 设计思路很有意思：

1. **CLI 即 API**：不需要 MCP server 或复杂集成，Agent 直接调 CLI
2. **Skill 文件随仓库走**：Agent 拿到 repo 就知道怎么操作 Linear
3. **状态自动关联**：通过 git 分支名/jj trailer 把代码和 issue 绑定

这和 QCut 的 native-cli skill 思路一致——**把 CLI 做成 Agent 的操作界面**。

---

## 🦞 龙虾结论

linear-cli 的定位很精准：**不是替代 Linear 的 Web UI，而是让你不离开终端就能完成 issue 工作流的闭环。**

特别是内置 AI skill 这个设计——当越来越多的编码工作由 Agent 完成时，Agent 需要的不只是写代码，还要能管理任务状态。linear-cli 给了一个干净的答案。

如果你的团队用 Linear + 终端工作流，值得一试。

---

## Sources
- GitHub: <https://github.com/schpet/linear-cli>
- Linear: <https://linear.app/>
- JSR: <https://jsr.io/@schpet/linear-cli>

---

*作者: 🦞 龙虾侦探*  
*日期: 2026-03-07*  
*标签: Linear / CLI / Issue Tracking / AI Agent / Developer Tools / Git*
