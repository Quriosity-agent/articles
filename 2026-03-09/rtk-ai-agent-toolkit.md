# RTK：让 AI 编程助手省下 80% Token 的 CLI 神器

> 当 AI 编程助手每次执行 `git status` 都要消耗 2000 个 token，而实际有用信息只有 200 个——RTK 就是来解决这个问题的。

## 这是什么？

[RTK](https://github.com/rtk-ai/rtk)（Rust Token Killer）是一个用 Rust 编写的高性能 CLI 代理，它拦截 AI 编程助手（如 Claude Code）执行的终端命令，对输出进行智能过滤和压缩，将 LLM 的 token 消耗降低 60-90%。

- **单一 Rust 二进制文件**，零依赖
- **<10ms 额外开销**，几乎无感
- **支持 40+ 命令**，涵盖 Git、测试、构建、容器等
- **MIT 开源协议**

## 为什么需要 RTK？

AI 编程助手（Claude Code、Cursor、Copilot 等）在工作时会频繁执行终端命令。问题是：这些命令的输出大部分是噪音。

举个例子：

- `git push` 输出 15 行、~200 token → 实际有用信息只有 `ok main`（~10 token）
- `cargo test` 输出 200+ 行 → 有用的只是失败的 2 个测试（~20 行）
- `ls -la` 输出 45 行权限信息 → 有用的只是目录结构（~12 行）

一个典型的开发 session 中，这些命令加起来消耗约 118,000 token。用 RTK？降到约 23,900——**省了 80%**。

## 核心架构

RTK 的设计非常优雅，分为六个阶段：

- **PARSE** — Clap 解析器提取命令、参数和全局标志
- **ROUTE** — 根据命令类型分发到专用模块（git.rs、grep_cmd.rs 等）
- **EXECUTE** — 执行原始命令，捕获 stdout/stderr/exit code
- **FILTER** — 应用智能过滤策略压缩输出
- **PRINT** — 输出彩色格式化结果
- **TRACK** — SQLite 记录 token 节省统计

### 四大过滤策略

- **Smart Filtering** — 去除噪音（注释、空白、样板代码）
- **Grouping** — 聚合同类项（按目录分组文件，按类型分组错误）
- **Truncation** — 保留关键上下文，裁剪冗余
- **Deduplication** — 折叠重复日志行，附带计数

## 安装与使用

```bash
# Homebrew（推荐）
brew install rtk

# 或 curl 一键安装
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh

# 或从源码
cargo install --git https://github.com/rtk-ai/rtk
```

### 与 Claude Code 集成（核心用法）

```bash
# 安装全局 hook
rtk init --global

# 重启 Claude Code，完成！
```

Hook 的工作原理：透明地将命令重写。当 Claude Code 执行 `git status` 时，hook 自动将其改写为 `rtk git status`，Claude 完全无感知，只会收到压缩后的输出。

### 常用命令示例

```bash
# 文件操作
rtk ls .                    # 精简目录树
rtk read file.rs            # 智能文件读取
rtk read file.rs -l aggressive  # 仅展示函数签名

# Git 操作
rtk git status              # 精简状态
rtk git log -n 10           # 单行提交记录
rtk git diff                # 压缩 diff
rtk git push                # 输出: "ok main"

# 测试（只显示失败）
rtk test cargo test         # -90% token
rtk pytest                  # -90% token
rtk vitest run              # -99.5% token！

# 构建和 Lint
rtk tsc                     # TypeScript 错误按文件分组
rtk lint                    # ESLint 按规则/文件分组
rtk cargo clippy            # -80%

# Token 节省统计
rtk gain                    # 查看总节省
rtk gain --graph            # ASCII 图表（最近 30 天）
rtk discover                # 发现更多节省机会
```

## 支持的命令覆盖范围

RTK 模块化设计覆盖了几乎所有常见开发场景：

- **Git 全家桶** — status、diff、log、add、commit、push、pull、branch、checkout（85-99% 节省）
- **GitHub CLI** — pr list/view、issue list、run list（26-87% 节省）
- **JS/TS 生态** — ESLint、TSC、Next.js、Prettier、Playwright、Vitest、Prisma、pnpm（70-99% 节省）
- **Rust 生态** — cargo test/build/clippy（80-90% 节省）
- **Python 生态** — pytest、ruff、pip（70-90% 节省）
- **Go 生态** — go test/build/vet、golangci-lint（75-90% 节省）
- **容器** — Docker、Podman、kubectl（60-80% 节省）
- **通用** — grep、find、curl、wget、JSON、日志（50-95% 节省）

## 与同类工具的对比

RTK 在 AI token 优化这个领域几乎是独占地位，但我们可以和相关方案比较：

- **直接使用 AI 编程助手（无优化）** — 所有命令输出原样发送给 LLM，token 消耗高，成本高。RTK 解决的就是这个痛点。
- **手动 `.claud` 配置 / prompt 工程** — 可以告诉 AI "输出简洁一点"，但无法控制命令输出本身。RTK 在命令层面拦截，效果更彻底。
- **Context window 管理工具**（如 repomix、aider 的 repo map）— 侧重代码上下文压缩，而 RTK 侧重命令输出压缩，二者互补。
- **自定义 shell wrapper** — 可以手写脚本做类似的事，但 RTK 提供了 40+ 命令的开箱即用支持，且用 Rust 实现几乎零开销。

## 设计亮点

- **Fail-Safe 设计** — 如果过滤失败，回退到原始输出，绝不丢信息
- **Exit Code 透传** — 正确传递退出码，CI/CD 环境完全兼容
- **Tee 模式** — 命令失败时保存完整原始输出到日志文件，LLM 可以按需查看
- **可配置** — 支持排除特定命令、自定义数据库路径、控制 tee 行为
- **双 Hook 策略** — Auto-Rewrite（100% 覆盖）和 Suggest（Claude 自主决定，适合审计）

## 总结

RTK 解决了一个真实且重要的问题：AI 编程助手的 token 浪费。在 Claude Code 等工具日益成为开发主力的今天，一个能省下 80% token 的 CLI 代理不是锦上添花——是刚需。

用 Rust 写、零依赖、<10ms 开销、40+ 命令开箱即用。如果你在用 AI 编程助手，RTK 值得一试。

- GitHub: https://github.com/rtk-ai/rtk
- 官网: https://www.rtk-ai.app
- Discord: https://discord.gg/gFwRPEKq4p

🦞
