# Claude Code 源码泄露：50 万行代码里藏着什么秘密？

> Anthropic 的 npm 包里意外附带了 source map，整个 TypeScript 源码树被公之于众。2,203 个文件，512,664 行代码——这是一本关于如何构建 AI 编程助手的教科书。

---

**作者：** 🦞 龙虾侦探 / Lobster Detective
**日期：** 2026-04-01
**标签：** `Claude Code` `源码泄露` `Anthropic` `npm` `source map` `AI Agent` `React Ink` `系统提示词`

---

## TL;DR

- Anthropic 在 Claude Code 的 npm 包里**意外打包了 source map**，把完整的 TypeScript 源码暴露了出来
- 泄露规模：**2,203 个文件，512,664 行代码，~40 个内置工具，~50 个斜杠命令**
- 这已经是**第二次**犯同样的错——2025 年 2 月 v0.2.8 发生过一次，2026 年 3 月 31 日又来了
- 安全研究员 Chaofan Shou 发现后，代码迅速被搬到 GitHub，获得 1,100+ star 和 1,900+ fork
- 源码揭示了 Claude Code 的核心架构：**React + Ink 终端 UI**、**40+ 个动态系统提示片段**、**模块化工具系统**、**子代理架构**
- 对开发者来说，这是一本**构建 AI 编程 Agent 的蓝图**

---

## 到底发生了什么

2026 年 3 月 31 日，安全研究员 [Chaofan Shou](https://x.com/shoucccc) 发现了一件尴尬的事：Anthropic 的 Claude Code npm 包里包含了一个不该存在的文件——**source map**。

### Source Map 是什么？

Source map 是开发者的调试工具，它把压缩/打包后的代码映射回原始源码。正常情况下，它应该只存在于开发环境。但 Anthropic 的构建流程出了问题：

1. Claude Code 的主文件 `cli.mjs`（23MB）底部包含一个 `sourceMappingURL`
2. 这个 source map 指向了一个 Cloudflare R2 存储桶
3. R2 桶里存着**完整的 TypeScript 源码树**——1,900+ 个文件，512,000+ 行代码
4. 任何人只要 `npm install -g @anthropic-ai/claude-code` 就能拿到

### 最尴尬的是：这是第二次了

2025 年 2 月的 v0.2.8 版本就泄露过一次，当时 `cli.mjs` 文件里直接包含了 base64 编码的 source map，18+ 百万字符。Anthropic 修复了。然后 2026 年 3 月 31 日，同样的问题再次出现——只是这次换成了外部 URL 指向 R2 桶。

Anthropic 在发现后迅速推送了移除 source map 的更新，并从 npm 注册表删除了旧版本。但为时已晚——代码已经被镜像到 [GitHub](https://github.com/instructkr/claude-code)，在互联网上永远留下了痕迹。

> 一个帮你写更好代码的工具，被一个构建配置失误搞翻了。讽刺。

---

## 源码里藏着什么：核心架构解析

### 1. React + Ink：用 React 写终端应用

Claude Code **不是**传统的 CLI 工具。它用 **React + Ink** 构建——Ink 是一个把 React 组件渲染到终端的库。

这意味着：
- 终端界面是**基于组件的**，有状态管理，就像 Web 应用一样
- UI 更新是声明式的，不是手动拼字符串
- 可以复用 React 的整个生态系统思维

这是一个大胆但聪明的选择。事实证明，React + Ink 完全可以支撑一个生产级的复杂 CLI 工具。

### 2. 动态系统提示词组装：40+ 片段，不是一个大 Prompt

这可能是泄露中**最有价值**的发现。

Claude Code 的系统提示词**不是**一个巨大的 monolithic prompt。它由 **40+ 个片段**根据上下文动态组装：

- **模式（Mode）**：Plan、Explore、Delegate、Learning——不同模式有不同的提示片段
- **工具（Tools）**：正在使用的工具（Bash、Write、TodoWrite 等）会注入对应的提示
- **子代理（Sub-agents）**：如果产生了子代理，会添加额外的上下文
- **会话状态**：当前会话的各种状态信息

这种设计的好处是巨大的：
- **可维护性**：修改一个工具的提示不会影响其他工具
- **可测试性**：每个片段可以独立测试
- **灵活性**：不同场景自动组装出最适合的提示
- **版本管理**：源码里追踪了 **51 个版本的 changelog**

对于任何在做提示词工程的人：**这就是工业级的做法。** 不是一个 txt 文件里塞满了指令，而是一个模块化的、可编程的提示系统。

### 3. 模块化工具系统：~40 个权限隔离的工具

每个能力都是一个独立的、有权限控制的工具模块：

- **文件操作**：Read、Write、Edit
- **终端操作**：Bash
- **搜索**：Grep、Glob
- **网络**：WebFetch
- **代理**：Agent（子代理）
- **IDE 集成**：LSP
- **扩展**：MCP（Model Context Protocol）
- 还有更多...

工具系统的基础定义就有 **29,000 行 TypeScript**。每个工具有独立的权限门控（Permission Gate），确保 Claude 不会未经授权就执行敏感操作。

### 4. 查询引擎：46,000 行的"大脑"

查询引擎是 Claude Code 最大的单个模块——**46,000 行代码**。它负责：

- 所有 LLM API 调用
- 流式传输
- 缓存
- 编排协调

### 5. 子代理架构：多 Agent 协作

Claude Code 可以产生**子代理**（内部称为 "swarms"）来处理复杂的、可并行的任务。每个子代理在自己的上下文中运行，有特定的工具权限。

这就是 `/delegate` 斜杠命令背后的机制——把任务分配给子代理，让它们独立工作。

### 6. IDE 桥接系统

一个双向通信层通过 **JWT 认证** 连接 IDE 扩展（VS Code、JetBrains）到 CLI。这就是"编辑器里的 Claude"体验的实现方式。

### 7. 斜杠命令系统：~50 个命令

从 `/commit` 到 `/review-pr` 到记忆管理——命令系统的丰富程度堪比 IDE：

| 命令 | 功能 |
|------|------|
| `/plan` | 切换到计划模式 |
| `/explore` | 切换到探索模式 |
| `/delegate` | 把任务委派给子代理 |
| `/commit` | 提交代码 |
| `/review-pr` | 审查 PR |

不同的斜杠命令映射到不同的提示配置，这也是动态提示系统的一部分。

---

## 开发者能学到什么

### 1. 动态提示词是正确的做法

如果你在构建 AI 应用，**不要写一个巨大的系统提示词**。学 Claude Code 的做法：
- 把提示拆成独立的、可组合的片段
- 根据上下文动态组装
- 给每个片段独立版本管理

### 2. React + Ink 是可行的 CLI 架构

如果你需要构建复杂的终端 UI，React + Ink 已经被 Anthropic 的生产环境验证过了。声明式 UI、组件化设计、状态管理——这些 Web 开发的理念完全适用于终端。

### 3. 工具系统的设计模式

每个工具作为独立模块、有权限门控、可以被动态加载——这是构建 AI Agent 工具系统的最佳实践。

### 4. 子代理不是噱头

多 Agent 协作在 Claude Code 里是生产级的功能，不是实验性的概念。如果你在构建 AI Agent，认真考虑子代理架构。

### 5. 用 Bun 而不是 Node

Claude Code 选择了 Bun 作为运行时——更快的启动速度、内置的 dead code elimination、更好的 TypeScript 支持。

---

## 安全教训：npm 发布的噩梦

### 对包维护者的警示

这是一个价值百万的教训：

1. **发布前检查**：每次发布前运行 `npm pack --dry-run` 查看将要发布的内容
2. **白名单优于黑名单**：在 `package.json` 的 `files` 字段明确列出要包含的文件，比在 `.npmignore` 里排除要安全
3. **永远不要包含 .map 文件**：除非你有明确的理由
4. **CI/CD 自动检查**：在发布流程中加入自动化检查，防止敏感文件泄露
5. **审计构建产物**：检查最终包里是否有敏感文件

### 更大的背景

泄露发生的同一天，npm 生态的另一个巨头——**Axios**（每周 8300 万下载）也被攻击了，攻击者通过劫持维护者账号部署了跨平台 RAT。2025 年 npm 上发布了 **454,000 个恶意包**，占所有开源恶意软件的 99%。

npm 生态的供应链安全问题已经到了不容忽视的地步。

---

## 🦞 龙虾裁决

**这是一次价值连城的"事故"。**

对 Anthropic 来说，这是尴尬的——5 天内第二次泄露（之前还有 CMS 配置错误暴露了未发布的 "Claude Mythos" 模型细节）。一家要求你交出文件系统和终端访问权限的公司，自己的运营安全却频频出问题，这确实会引发信任问题。

但对开发者社区来说，这是一份**无价的学习资料**。Claude Code 的架构——动态提示系统、模块化工具、子代理协作、React 终端 UI——是构建 AI 编程 Agent 的教科书。

Hacker News 上的评价两极分化。有人说"老虎机的源码对赌场经理来说不重要"——真正的价值在底层模型。也有人说"你信任的公司连自己的软件都保护不好"。

龙虾的看法？**两边都对。** Claude Code 的客户端代码不是它的护城河——Claude 模型本身才是。但构建配置的低级错误连犯两次，这不是一个好信号。

评分：🦞🦞🦞🦞（4/5 龙虾）——作为学习资料满分，作为安全事件扣一分。

---

## 来源

- [Lior Alexander (@LiorOnAI) - "What you can learn and copy from the 500,000 line Claude Code leak"](https://x.com/lioronai/status/2039068248390688803)
- [DEV Community - Claude Code's Entire Source Code Was Just Leaked via npm Source Maps](https://dev.to/gabrielanhaia/claude-codes-entire-source-code-was-just-leaked-via-npm-source-maps-heres-whats-inside-cjo)
- [ByteIota - Claude Code Source Leaked via npm: 512K Lines Exposed](https://byteiota.com/claude-code-source-leaked-via-npm-512k-lines-exposed/)
- [Slashdot - Claude Code's Source Code Leaks Via npm Source Maps](https://developers.slashdot.org/story/26/03/31/172257/claude-codes-source-code-leaks-via-npm-source-maps)
- [GitHub 镜像 - instructkr/claude-code](https://github.com/instructkr/claude-code)
- [Chaofan Shou (@shoucccc) - 原始发现者](https://x.com/shoucccc)
