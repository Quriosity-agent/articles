# Mr. Mak Workspace 源码审计：它不是新的 Agent，而是把 CLI、项目证据与手机入口连成一间本地工作室

> **结论先行：** Mr. Mak Workspace 不训练模型，也不取代 Codex、Claude Code 或 OpenCode。它是一套 MIT 开源的本地 Agent 控制面：Tauri 打开彼此独立的 Chats 与 Workspace 两个窗口，Node 服务在 loopback 上管理真实 CLI 的 PTY、会话恢复、文件与报告，React 界面把项目卡片、Markdown、HTML、媒体、Skill 和 MCP 清单组织起来；0.5.0 又通过 Tailscale 把一组受限操作开放到手机。真正的产品价值不是“又一个聊天 UI”，而是让任务、运行中的终端和可复查交付物不再混在同一条对话里。

![Mr. Mak 的 Chats 与 Workspace 两个桌面窗口](imgs/mr-mak-workspace-local-agent-control-room-audit/desktop-chats-workspace.png)

[`witnesstodark/mr-mak-workspace`](https://github.com/witnesstodark/mr-mak-workspace) 创建于 2026 年 9 月 15 日。截至 10 月 9 日审计时，仓库约有 343 stars、97 forks，最新公开版本是 10 月 8 日发布的 [`v0.5.0`](https://github.com/witnesstodark/mr-mak-workspace/releases/tag/v0.5.0)；主分支已经进入 `0.5.1`，增加手机终端导航、关闭聊天以及直接修改 Workspace 状态和分类等功能。

本文固定审计主分支提交 [`c7c9fbf`](https://github.com/witnesstodark/mr-mak-workspace/tree/c7c9fbfd0d9c4f961536392fbd50b71ff0b0c528)，同时把 `v0.5.0` 作为已发布产品边界。这样可以避免把尚未发布的主分支功能当成所有下载用户已经拥有的能力。

---

## 01 | 它不是 Agent 模型，而是现有 CLI 的本地操作台

Mr. Mak 启动的是用户电脑上已经安装并登录的真实 CLI：

- Codex CLI；
- Claude Code CLI；
- OpenCode CLI；
- 以及用于普通命令行的 shell 会话。

每个聊天都是一个真实 PTY，界面使用 xterm.js 展示。创建、停止、恢复和重新连接会话时，系统尽量保留原生 CLI 的 conversation/session ID，而不是只保存一张终端截图。Codex、Claude Code 和 OpenCode 仍决定模型、账号、额度、原生历史与权限行为。

因此，Mr. Mak 没有提供“自己的 AI”。它提供的是三类基础设施：

1. **会话控制：** 多标签终端、状态、未读完成、固定、排序、历史恢复和附件路径；
2. **工作成果：** 将研究、图片、视频、Prompt、Markdown 和 HTML 报告注册成 Workspace 卡片；
3. **项目上下文：** 用 `context/`、`knowledge/`、`processes/`、`.agents/skills/` 与 `.claude/skills/` 把工作方式留在仓库里。

这与“套壳聊天客户端”的差别，在于成果不会只能留在聊天记录里。Agent 可以在真实文件系统中工作，交付物进入项目目录，再由 Workspace 作为审阅面展示。

---

## 02 | 两个窗口解决的是“执行”和“验收”不该挤在一起

桌面端不是单一页面里的左右栏，而是两个可以独立最小化和排列的 Tauri webview：

| 窗口 | 主要职责 | 持久化位置 |
|---|---|---|
| Chats | 运行 CLI、输入任务、看实时终端、管理会话 | CLI 原生历史与 `.mrmak` 本地状态 |
| Workspace | 审阅项目卡片、报告、图片、视频、文件、Skill 与 MCP 状态 | 仓库中的 `workspace/`、项目文件与 `workspace.json` |

这个划分看似简单，却击中了长任务 Agent 的真实摩擦：执行日志不是交付物，聊天完成也不代表成果已经被保存、组织、预览和验收。

仓库自带四个示例卡片：My Dream Game、Creative MCP Connections、Make Workspace Yours 和 Arachne Character Lab。模板检查实际验证了 **4 张卡片、16 个步骤、177 张图片、8 个视频与 20 个共享 Skill**。这些样例不是四个内置模型，而是展示文件型 Workspace 能承载哪些成果。

![Workspace 中的项目报告、素材与文件树](imgs/mr-mak-workspace-local-agent-control-room-audit/workspace-files.png)

---

## 03 | 源码里真正的架构中心是 loopback Node 服务

![依据源码绘制的 Mr. Mak 架构](imgs/mr-mak-workspace-local-agent-control-room-audit/mr-mak-architecture.svg)

Tauri 负责桌面生命周期、原生窗口、文件选择、拖放、回收站和平台集成，但大部分产品行为在本地 Node 服务中。启动流程大致是：

1. Tauri 打包并启动随应用分发的 Node runtime 与 service；
2. service 只绑定随机的 `127.0.0.1` 端口；
3. 它为桌面窗口生成 bearer credential，经私有启动管道交给 Tauri；
4. Chats 与 Workspace 通过经过鉴权的 HTTP/WebSocket 调用服务；
5. service 启动真实 CLI PTY，并读取仓库文件、原生历史与 `.mrmak` 运行状态。

`runtime.json` 只保留进程 ID 与本地 origin，不保存窗口 credential。文件预览则使用独立 origin 和作用域 grant，报告不能任意获得桌面控制 API。

这一结构比把 Tauri 直接做成一个拥有全部文件权限的大前端更清楚：UI、终端、文件内容和移动端各自有不同接口边界。但它仍运行在当前操作系统用户之下，不是用于隔离任意不可信代码的沙箱。

---

## 04 | Workspace 的“记忆”主要是仓库，不是隐藏的云数据库

`workspace/workspace.json` 是卡片注册表。每个实体记录标题、描述、类别、状态、日期、文件夹、默认步骤和报告路径；真正内容仍是普通 HTML、Markdown、图片、视频和项目文件。

这种设计有几个实际优点：

- 报告可以在浏览器或其他编辑器中打开，不锁死在 Mr. Mak；
- 交付物可以被 Git diff、备份、复制或发布；
- `knowledge/` 与 `processes/` 能成为项目级经验，而不是只存在于某个模型的全局记忆；
- Codex 与 Claude 的 Skill 由同一维护源同步，模板检查会发现副本漂移；
- 一个 Agent 可以生成成果，另一个 Agent 或人类可以在相同文件上复核。

但并非所有状态都适合进 Git。`.mrmak` 会话状态、原生聊天历史、`.env`、账号登录与 job receipt 都应保持本地并被忽略。仓库解决的是**可交付工作记忆**，不是把所有终端与模型状态完整迁移到另一台机器。

---

## 05 | 手机端不是云端 Agent，而是电脑上会话的受限遥控器

![Mr. Mak Mobile 的聊天列表、对话和语音输入](imgs/mr-mak-workspace-local-agent-control-room-audit/mobile-overview.png)

0.5.0 最显眼的变化是手机访问。它不把 Agent 搬到服务器：电脑必须保持开机，Mr. Mak 与对应 CLI 必须继续运行，手机和电脑还要接入同一个 Tailscale 网络。

配对流程包含二维码、手机请求、两端六位数比对和桌面确认。Tailscale Serve 只建立私有 HTTPS 路由，代码明确拒绝启用公开 Funnel。已配对设备获得 HttpOnly session cookie；电脑保存 credential hash，而不是把桌面 control token 或模型 API key 发给手机。

手机端当前可以：

- 阅读最近的 Codex/Claude 对话，并切换到实时终端视图；
- 发送完整 Prompt、图片与少量终端导航键；
- 恢复、关闭或新建已安装 Agent 的会话；
- 查看仓库内受限范围的 Workspace 报告；
- 录音、转写为草稿，经用户审阅后再发送。

它不能成为完整远程桌面或任意文件管理器。对话视图省略工具输出，只展示有限的最近记录；附件限图片；报告必须位于允许的仓库边界；桌面和手机的选中标签、滚动与终端尺寸彼此独立。

这是合理的安全与体验取舍：手机负责“跟进和下一个决定”，重型检查仍留在电脑。

---

## 06 | 消息投递做得比“远程敲回车”更认真

手机发送消息时，service 会在写入终端**之前**先持久化 request ID、内容 hash 与 receipt。相同 request ID 重试时，只有内容完全相同才复用结果；不同内容会被拒绝。每个会话的写入进入队列，整段 Prompt 通过 bracketed paste 写入，再单独发送 Enter。

如果连接恰好在终端写入附近断开，系统不会自动重复投递，而是把状态标记为 `uncertain`，要求用户查看真实终端后决定。这一点很重要：移动网络里的“HTTP 请求失败”不等于终端没有收到 Prompt。盲目重试可能让付费调用或文件修改执行两次。

测试也明确区分：`Delivered to terminal` 只证明文本进入 PTY，不证明 Agent 接受了任务、完成了任务，更不证明 Workspace 已产生可验收成果。

---

## 07 | Voice 有两条不同路径，付费与数据边界也不同

仓库里容易被混为一谈的 Voice 实际有两套：

| 功能 | 用途 | 依赖与计费 |
|---|---|---|
| Talk to Mak 桌面协调器 | 用自然语音操作聊天、Workspace 与本地工具 | OpenAI Live API + 已登录的 Codex CLI |
| 手机麦克风 | 把最长两分钟录音转成可编辑草稿 | OpenRouter 或 OpenAI 转写 API |

普通键盘聊天可以继续使用 Codex/Claude Code 的订阅登录，不要求新增 API key。语音 API 则单独计费，key 保存在电脑的 ignored `.env` 中。录音默认留在手机浏览器，电脑把音频提交给所选 provider；成功后返回文本，失败时可以重试或下载原录音。

所以“local-first”不等于“所有内容都不离开设备”。CLI 对话遵循各自模型供应商的政策，语音也会进入明确选择的转写或实时语音服务。

---

## 08 | 安全设计有实质内容，但权限最终仍属于本机用户

源码与测试覆盖了不少常被忽略的边界：

- Agent permission bypass 默认关闭，协调器不能自行把用户选择提升为 bypass；
- loopback API 校验 Host、Origin 与 bearer token；
- 跨站页面不能调用手机 API、WebSocket 或嵌入报告；
- 移动报告只能访问获得 grant 的文件夹，外部 symlink 和仓库外路径被拒绝；
- Tailscale 设置保留用户已有 route，并拒绝 Funnel；
- MCP 清单会隐藏 credential 和 URL secret，检查服务器时不调用实际工具；
- 图片、文件与转写请求有类型、大小、数量、频率和撤销边界；
- 设备撤销会关闭连接，并中止对应的付费转写请求。

真正的剩余风险也很清楚。Mr. Mak 以当前用户身份启动 CLI；开启 bypass 后，CLI 能力随之扩大。同一用户下的恶意进程不受它保护。配对手机虽然拿不到 API key，却能要求 Agent 使用已有权限执行操作，因此丢失设备需要同时从 Mr. Mak 与 Tailscale 撤销。

它是权限边界清楚的本地控制面，不是操作系统级安全容器。

---

## 09 | 工程成熟度：发布链路真实，macOS 状态仍有矛盾

审计快照包含约 530 个 Python、TypeScript/JavaScript、Rust 与 Shell 源文件，合计约 15.6 万行；其中包含桌面代码、测试、工具与项目 Skill。仓库有 33 个提交和 4 位 Git 作者，不能仅凭体量判断质量，但已经远超一份配置模板。

我在固定提交上进行了独立检查：

- `npm ci`：通过，两个 lockfile 的 audit 当时均报告 0 个已知漏洞；
- `npm run lint`：通过；
- `npm run build`：通过，React/Vite 生产构建成功；
- `npm run test:template`：通过，包含 9/9 资产清单测试与 375 个 Codex/Claude Skill 文件一致性检查；
- `MRMAK_TEST_BROWSER=chrome npm run test:preview`：通过，包括失败模块恢复测试；
- `npm test`：92 项中 86 通过、4 失败、2 跳过；失败集中在当前 macOS 环境的真实 PTY spawn/服务路径。

主分支对应的 GitHub Actions 在 Windows 和 Linux 都是绿色：Windows 还运行主题、语音、手机和 Workspace 编辑 UI 测试；Linux 会构建 AppImage。`v0.5.0` 发布流水线也成功生成 Windows、Linux 和 macOS 资产，并附带 SHA-256 清单。

这里存在一个需要保留的产品边界：仓库已经发布 macOS `.app.zip` 与 `.dmg`，但 README 和架构文档仍把 Windows x64 与 Linux 写为支持目标，并称 macOS 是未来工作。再加上本次 macOS PTY 测试失败，**有 macOS 安装包不能自动解释为 macOS 已正式支持并完成验收**。

本次没有登录真实 Codex、Claude Code 或 OpenCode，没有建立 Tailscale 手机配对，也没有发起语音或付费模型请求。因此，验证覆盖源码、构建、测试和发布设计，不覆盖真实账号、真实手机、长时间恢复或端到端创作接受度。

---

## 10 | 这套系统真正适合谁

Mr. Mak Workspace 最适合已经在本机使用多个 CLI Agent、并且交付物包含研究、图片、视频、3D 素材、Prompt 和报告的人。对于这类用户，瓶颈常常不是“如何再开一个聊天”，而是：哪个终端在做事、结果保存在哪里、不同版本如何比较、手机上如何继续跟进、哪些成果已经可审阅。

它不太适合以下场景：

- 只偶尔进行短代码问答，不需要项目报告和素材管理；
- 希望关掉电脑后仍由云端 Agent 继续运行；
- 需要多用户权限、组织审计或服务器级隔离；
- 期待安装后自带模型、额度、MCP 服务和创作账号；
- 把“CI 通过”当成真实手机、账号、语音和创作流程已经全部验收。

最准确的定位是：**Mr. Mak Workspace 是一套以仓库为长期成果层、以真实 CLI 为执行层、以 Tauri/Node 为本地控制层、以手机为受限跟进入口的个人 Agent 工作室。它没有发明新的 Agent，却把 Agent 工作从一次性对话变成了可以组织、复查、恢复和继续的项目。**

---

## 主要来源

- [Mr. Mak Workspace 仓库](https://github.com/witnesstodark/mr-mak-workspace)
- [固定审计提交 `c7c9fbf`](https://github.com/witnesstodark/mr-mak-workspace/tree/c7c9fbfd0d9c4f961536392fbd50b71ff0b0c528)
- [v0.5.0 发布页](https://github.com/witnesstodark/mr-mak-workspace/releases/tag/v0.5.0)
- [Desktop architecture](https://github.com/witnesstodark/mr-mak-workspace/blob/c7c9fbfd0d9c4f961536392fbd50b71ff0b0c528/desktop/README.md)
- [Mobile access](https://github.com/witnesstodark/mr-mak-workspace/blob/c7c9fbfd0d9c4f961536392fbd50b71ff0b0c528/docs/mobile-access.md)
- [Security policy](https://github.com/witnesstodark/mr-mak-workspace/blob/c7c9fbfd0d9c4f961536392fbd50b71ff0b0c528/SECURITY.md)
- [Agent working rules](https://github.com/witnesstodark/mr-mak-workspace/blob/c7c9fbfd0d9c4f961536392fbd50b71ff0b0c528/AGENTS.md)
- [Loopback service](https://github.com/witnesstodark/mr-mak-workspace/blob/c7c9fbfd0d9c4f961536392fbd50b71ff0b0c528/desktop/service/server.mjs)
- [Mobile gateway](https://github.com/witnesstodark/mr-mak-workspace/blob/c7c9fbfd0d9c4f961536392fbd50b71ff0b0c528/desktop/service/mobile.mjs)
- [Main-branch CI](https://github.com/witnesstodark/mr-mak-workspace/actions/runs/37900834185)

*审计日期：2026 年 10 月 9 日。stars、forks、主分支、release、依赖与 CI 会继续变化；技术结论固定到文中 commit。项目截图已随文章本地保存，架构图依据固定源码重绘。*
