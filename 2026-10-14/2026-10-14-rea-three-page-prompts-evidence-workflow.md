---
title: "REA 三页逆向提示词拆解：复制给 Codex 不是直接会逆向，而是启动一套证据工作流"
date: 2026-10-14
source: "https://x.com/qwerty__cs/status/2110345831635452411"
canonical: "https://github.com/morluto/rea"
tags:
  - REA
  - Reverse Engineering
  - Codex
  - Claude Code
  - MCP
  - Agent Skill
  - Evidence Ledger
  - Ghidra
  - Hopper
---

# REA 三页逆向提示词拆解：复制给 Codex 不是直接会逆向，而是启动一套证据工作流

> **TL;DR：** 这组在 X 上传播的三页提示词不是反编译器，也不会让一个普通 Codex 会话凭空获得读取 APK、IPA、EXE 或固件的能力。它真正做的是把 REA 的调查方法压缩成一套可复制的任务入口：先定位功能，再审计未知项，必要时做受限运行观察，然后独立实现并逐条验证。能力仍来自已经连接的 REA MCP、目标文件、Hopper/Ghidra/IDA/JADX 等 provider，以及可追溯的 Evidence。只复制文字而没有这些工具，Agent 最多能给出计划；连接完整栈后，这些提示词才会变成可执行的逆向工作流。

![REA prompt workflow page 1](imgs/rea-three-page-prompts-evidence-workflow/rea-prompt-workflow-page-1.jpg)

- **来源帖：** [拓跋鼠在 X 上发布的三页整理](https://x.com/qwerty__cs/status/2110345831635452411)
- **后续两页：** [同一线程中的提示词图片](https://x.com/qwerty__cs/status/2110346010593837566)
- **引用文章：** [0xCodila 的第三方教程](https://x.com/0xCodila/status/2109623431763292649)
- **官方项目：** [morluto/rea](https://github.com/morluto/rea)
- **官方 MCP Prompts 文档：** [Guided MCP prompts and completion](https://github.com/morluto/rea/blob/cf0a38ad9774ee9acff3164052688f7a58a1c72c/docs/mcp-prompts.md)
- **发布时间：** 2026-10-14
- **查阅时间：** 2026-10-15

## 一句话判断

**这不是“把逆向知识塞进一段 Prompt”，而是给已经接好逆向工具的 Agent 一张作业单。**

如果把 REA 比作一间实验室，三页提示词只是实验步骤。Codex 或 Claude Code 是研究员，MCP 是仪器接口，Hopper/Ghidra/IDA/JADX 是分析设备，Evidence ledger 是实验记录，最终的行为测试才是验收。

少了任意关键层，宣传语里的“复制粘贴，直接让 AI 帮你逆向”都会失真。

## 先纠正一个来源问题

来源帖写的是“REA 作者把逆向提示词公开了”，图片顶部也写着 REA 作者的账号，但这三张带大标题、产品 Logo 和分步排版的长图，并不是 REA 官方仓库里的发布海报。

可确认的关系是：

1. 提示词主体来自 REA 官方仓库的工作流与 MCP prompt；
2. X 来源帖由 `@qwerty__cs` 发布；
3. 帖子引用的是 `@0xCodila` 写的第三方教程；
4. 图片是对官方文本的二次整理与传播包装。

因此，本文把三页图当作 **REA 工作流的第三方速查卡**，把 GitHub 当前代码与文档当作能力边界的主要证据。

## 三页提示词到底包含什么

### 第一页：先调查，再承认不知道

第一页给出两个动作：

- **Map & Understand：** 围绕一个具体功能，从入口、相关函数、数据流和静态证据开始调查；
- **Find the Gap：** 审计仍然开放、互相矛盾、被工具阻塞或已经有证据解决的未知项。

其中最有价值的不是工具名，而是它反复要求 Agent 区分：

| 状态 | 含义 |
|---|---|
| Observation | 工具实际读到、运行时实际看到的事实 |
| Inference | 根据多个事实推导出的解释，必须标注置信度 |
| Unknown | 当前证据无法回答、覆盖不完整或彼此冲突的问题 |

这能抑制普通代码 Agent 最常见的错误：搜到几个字符串或函数名，就把可能路径写成已经确认的产品行为。REA 官方 Skill 同样明确要求，静态分析不能被描述成运行时观察，也不能在证据不完整时声称恢复了原始源码。

### 第二页：运行观察、独立实现、逐项验收

![REA prompt workflow page 2](imgs/rea-three-page-prompts-evidence-workflow/rea-prompt-workflow-page-2.jpg)

第二页把工作从“理解”推进到“重建”：

- **Watch It Run：** 只在静态证据不足时，设计范围明确、可清理的运行实验；
- **Build Your Version：** 根据已经确认的行为规范实现自己的版本；
- **Verify Against Original：** 把有限的验收项逐条标成 pass、fail 或 unknown。

这个顺序很关键。普通的“克隆这个 App”提示词常把观察和实现混在一起，Agent 一边猜产品行为，一边写 UI，最后用“看起来相似”替代等价性验证。REA 的流程要求先形成证据支持的行为规格，再实现，最后回到原目标做相容的比较。

但图片中的“Build Your Version”不是自动授权。目标是否属于自己、是否允许研究、能否执行、哪些数据可以读取，仍由用户、系统权限、许可证和当地法律决定。提示词不会替用户取得许可。

### 第三页：把版本差异和崩溃也变成证据问题

![REA prompt workflow page 3](imgs/rea-three-page-prompts-evidence-workflow/rea-prompt-workflow-page-3.jpg)

第三页增加两个常见任务：

- **Compare Two Versions：** 比较两个已发布制品的文件、函数、资源和运行行为差异；
- **Trace a Crash：** 把已观察到的崩溃、静态可达路径、推测原因和没有覆盖的路径分开。

这说明 REA 的重点不是“一键反编译”，而是让 Agent 在长调查里维持证据状态。版本 A 有某个字符串、版本 B 没有，不等于功能已被删除；某个函数能到达崩溃点，也不等于它就是实际原因。提示词强迫 Agent 把这种距离写出来。

## 它比直接对 Codex 说“帮我逆向”多了什么

| 普通请求容易发生的事 | REA 提示词增加的约束 |
|---|---|
| 目标和版本含糊 | 先绑定明确制品、路径和调查问题 |
| 一开始就全盘扫描 | 从最小可用 inventory 开始，围绕假设扩展 |
| 字符串命中被写成事实 | 区分 observation、inference 和 unknown |
| 静态结果冒充运行行为 | 只有受限 runtime capture 才能支持运行时结论 |
| 找不到就说不存在 | 保留搜索边界和 residual unknown |
| 做出相似 UI 就宣布完成 | 使用有限规格逐项 pass/fail/unknown |
| 每次重新分析 | 复用 session、Evidence ID 和既有发现 |

它提升的主要不是模型智力，而是 **调查纪律、上下文复用和结束条件**。这正是它对 Codex、Claude Code、Cursor 等 Agent 最实际的增益。

## 但 Prompt 只占整套系统的一层

REA 官方当前文档明确说，MCP prompts 只是对工具目录的补充，它们不会自行新增、删除或调用工具。完整栈至少包含：

| 层 | 负责什么 |
|---|---|
| 三页速查 Prompt | 给用户一个自然语言任务模板 |
| REA Skill | 规定如何选目标、使用证据、处理未知项和结束调查 |
| REA MCP / CLI | 暴露结构化工具、会话和 Evidence |
| Provider | 真正读取目标，如 Hopper、Ghidra、IDA、JADX 或 JavaScript analyzer |
| Agent | 选择下一步、解释结果、维护调查叙事 |
| 验证环境 | 对重建版本进行行为、输出或运行时比较 |

所以只有三页文字时，Codex 可能会知道“应该调用某个工具”，却根本没有这个工具。只有 Skill 时也一样：官方当前 Skill 特别说明，安装 Skill 不会自动注册 MCP、安装分析引擎，或给正在运行的 Agent 增加工具。

## 官方实现其实比图片更谨慎

截至本文查阅时，REA 官方 MCP 暴露六个 provider-neutral guided prompts：

| Prompt | 作用 |
|---|---|
| `investigate_feature` | 从功能入口追到相关函数证据 |
| `compare_application_versions` | 比较两个发布制品 |
| `verify_reconstruction` | 对有限重建规格逐项验收 |
| `trace_crash` | 关联崩溃症状、静态路径和可选运行证据 |
| `audit_residual_unknowns` | 审计尚未解决的未知项 |
| `prepare_bounded_process_capture` | 在执行前设计受限进程实验 |

官方实现还有三处值得注意：

1. 用户给 prompt 的参数和选择被视为不可信的 selection data，而不是额外指令或授权；
2. 工具结果把 Evidence 内联返回，Evidence ID 只是会话中的可追溯引用；
3. 自动补全只给候选项，不会读取目标、启动分析或扩大操作范围。

这三点共同构成了一个很实用的 Agent 安全边界：**建议不等于动作，参数不等于授权，引用不等于证据内容。**

## 不同目标仍然需要不同工具

“安卓 APK、iPhone App、Windows EXE、固件和闭源软件都没问题”只能理解为 REA 设计了多种路由，不能理解为任何电脑安装一次就能无条件处理所有目标。

| 目标 | 仍然需要的现实条件 |
|---|---|
| Electron / JavaScript | 可直接使用 REA 的 JavaScript 静态分析路径，不一定需要原生反编译器 |
| Android APK | Java/JADX 等 bring-your-own 前置条件，具体能力取决于当前 provider |
| macOS / iOS / Windows 原生二进制 | Hopper、Ghidra 或 IDA 等可用引擎与对应格式支持 |
| 固件 | 可识别的镜像格式、提取工具和架构支持 |
| 运行时观察 | 当前主机能执行目标，且用户明确允许该范围 |
| 加壳、混淆、完整性校验 | 仍可能显著降低静态可读性或阻止实验 |

换句话说，Prompt 负责选择和编排能力，不负责创造能力。

## 一个更准确的使用方式

对合法、获授权的兼容性研究、故障诊断、安全分析或独立实现，较稳妥的流程是：

1. 明确目标文件、版本、哈希和一个具体问题；
2. 检查 REA 工具是否已经出现在当前 Agent 会话，而不是仅确认 Skill 文件存在；
3. 确认该目标所需 provider 可用；
4. 从最小静态概览开始，记录 Evidence 与搜索边界；
5. 把未确认的行为保留为 unknown，不用猜测填空；
6. 只有静态证据回答不了问题时，才设计范围明确的运行观察；
7. 根据确认行为写独立规格，而不是假装恢复原始源码；
8. 对每条规格做可重复比较，允许结果为 unknown；
9. 保存工具版本、目标身份、限制和剩余问题，供下一次调查复用。

这套流程不会让逆向变得毫无门槛，但会让 Agent 的输出从“听起来像答案”更接近“能够追问、复查和复现的调查记录”。

## 和此前 REA 源码审计的关系

此前的[《REA 源码审计：它不是 AI 自动克隆 App，而是给逆向工程加上证据账本的 Agent 运行时》](../2026-10-09/2026-10-09-rea-evidence-ledger-agentic-reverse-engineering-runtime.md)回答的是“REA 整个系统是什么”。

这次三页图回答的是另一个问题：**普通用户怎样用几段自然语言进入这套系统。**

它们不是两套方案。三页 Prompt 是入口，Skill 是操作规程，MCP 与 provider 是执行层，Evidence ledger 和验证则负责阻止 Agent 把猜测写成完成。

## 结论

这组提示词值得保存，但不应神化。

它最先进的地方不是写出了几句神奇命令，而是把逆向任务组织成一个闭环：**调查目标、管理未知、受限观察、独立实现、逐条验证。** 对 Codex 来说，这确实比一句“分析并克隆这个 App”好很多，因为模型终于有了明确的证据格式和停止条件。

但复制三张图不会安装工具、不会连接 MCP、不会获得目标权限，也不会把相似实现变成等价实现。真正的门槛只是从“人手工操作每个逆向工具”，移动到了“人和 Agent 共同定义问题、审查证据、控制运行范围并验收结果”。

**它是 REA 的操作界面，不是 REA 本身；是逆向 Agent 的方法论，不是万能反编译能力。**

## 参考资料

- [来源帖 - X](https://x.com/qwerty__cs/status/2110345831635452411)
- [提示词后续图片 - X](https://x.com/qwerty__cs/status/2110346010593837566)
- [第三方引用文章 - X](https://x.com/0xCodila/status/2109623431763292649)
- [REA official repository](https://github.com/morluto/rea)
- [REA guided MCP prompts](https://github.com/morluto/rea/blob/cf0a38ad9774ee9acff3164052688f7a58a1c72c/docs/mcp-prompts.md)
- [REA Skill at the inspected commit](https://github.com/morluto/rea/blob/cf0a38ad9774ee9acff3164052688f7a58a1c72c/.agents/skills/reverse-engineer-anything/SKILL.md)
- [REA website](https://rea.tools/)

*本文核对的官方仓库提交为 `cf0a38ad9774ee9acff3164052688f7a58a1c72c`，查阅时间为 2026-10-15。REA 更新很快，工具名、客户端支持和 provider 前置条件可能继续变化。三张图片来自用户提供的 X 线程并在仓库中本地保存；其版式属于第三方整理，不作为 REA 官方视觉物料。本文仅讨论合法、获授权的研究、兼容性、调试与安全分析。*
