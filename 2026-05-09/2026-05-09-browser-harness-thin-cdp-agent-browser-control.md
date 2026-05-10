# Browser Harness 深度拆解：给 AI Agent 一根直连真实浏览器的细线

> Repo: <https://github.com/browser-use/browser-harness>  
> Inspected commit: `0e679e2`  
> Date: 2026-05-09  
> Tags: Browser Harness / Browser Use / CDP / Browser Agent / Chrome / Python / Skills

![Browser Harness banner](imgs/browser-harness-thin-cdp-agent-browser-control/banner-ink.svg)

## 1. 它解决的不是“浏览器自动化”，而是 Agent 如何接管真实浏览器

`browser-use/browser-harness` 这个仓库看起来很小，但它切中的问题很大：LLM/Agent 如果要完成真实网页任务，到底应该控制什么？

传统答案通常是 Playwright、Selenium、Puppeteer：给浏览器包一层自动化框架，提供 selector、locator、page object、等待机制。但 Browser Harness 选择了反方向：**尽量薄，直接连 Chrome DevTools Protocol（CDP），让 agent 用真实浏览器完成任务。**

README 的一句话很能概括它的路线：

> Connect an LLM directly to your real browser with a thin, editable CDP harness.

这里的关键词是 real browser。它不是开一个干净的测试浏览器跑脚本，而是尽量复用用户真实 Chrome/Chromium 环境：登录态、cookie、扩展、已有 profile、真实页面行为都在里面。对 Agent 来说，这比“无状态浏览器沙箱”更接近真实任务环境。

## 2. 仓库事实：小而热，重点在流程资产

本次检查的是 `browser-use/browser-harness`，HEAD 为 `0e679e2`。GitHub API 显示它约 **11.9k stars**、**1.1k forks**，主语言是 Python，许可证为 MIT，默认分支是 `main`。仓库创建时间是 2026-04-17，说明它增长非常快。

本地扫描得到的规模：

- 总文件约 **157** 个；
- Python 文件 **19** 个，约 **3,909** 行；
- Markdown 文件 **126** 个，约 **32K** 行；
- `src/browser_harness/` 只有 **6** 个 Python 文件，约 **2,005** 行；
- `agent-workspace/domain-skills/` 有约 **95** 个站点/任务技能目录；
- `interaction-skills/` 有 **17** 个浏览器交互技巧文档；
- 测试套件运行结果：**94 passed in 0.40s**。

这组数字说明：Browser Harness 的核心代码很薄，真正大的部分是文档、domain skills 和交互知识。换句话说，它不是在做一个复杂框架，而是在做一个 **agent 可学习、可扩展的浏览器操作底座**。

## 3. 架构：Chrome / Cloud → CDP → daemon → CLI

`install.md` 把架构写得很清楚：

```text
Chrome / Browser Use cloud -> CDP WS -> browser_harness.daemon -> IPC -> browser_harness.run
```

核心边界有四层：

1. **浏览器层**：本地 Chrome/Chromium，或者 Browser Use Cloud；
2. **CDP WebSocket**：连接真实页面和 DevTools Protocol；
3. **daemon**：长期持有 CDP 连接，处理事件、tab、页面状态；
4. **CLI runner**：每次 `browser-harness -c '...'` 只是发一段 Python 片段到 harness 环境里执行。

协议也很简单：IPC 里一来一回都是 JSON line。普通 CDP 请求是 `{method, params, session_id}`，daemon-control 请求是 `{meta: ...}`，响应是 `{result}`、`{error}`、`{events}` 或 `{session_id}`。

这个设计的好处是：Agent 不需要一直重启浏览器或重新建连接。daemon 保持长期 session，CLI 保持短命令模式，模型只要发一小段 Python，就能操控当前浏览器状态。

## 4. 核心文件：少抽象，但把真实边界处理得很细

`src/browser_harness/` 只有几个文件，但每个文件职责很明确：

- `run.py`：CLI 入口，支持 `--version`、`--doctor`、`--update`、`--reload`、`--debug-clicks` 和 `-c`。它会自动 `ensure_daemon()`，然后把 helpers/admin functions 预导入到执行环境。
- `daemon.py`：长期 CDP WebSocket holder。它会发现本地 Chrome profile、支持 `BU_CDP_WS` / `BU_CDP_URL`、探测 `9222/9223` 端口、attach 到真实 page、启用 `Page` / `DOM` / `Runtime` / `Network`，并维护最近 500 个事件。
- `helpers.py`：Agent 日常使用的浏览器 primitives，例如 `new_tab`、`page_info`、`click_at_xy`、`type_text`、`fill_input`、`press_key`、`scroll`、`capture_screenshot`、`wait_for_load`、`wait_for_network_idle`、`js`、`upload_file`。
- `admin.py`：daemon 生命周期、cloud browser、profile sync、doctor、update check。
- `_ipc.py`：POSIX 用 Unix socket，Windows 用 TCP loopback + token port file；还支持 `BH_RUNTIME_DIR` 和 `BH_TMP_DIR` 分离，避免 socket、pid、日志、截图混在一起。

值得注意的是，Browser Harness 的价值不在“封装了多少高级 API”，而在它处理了真实浏览器连接里的脏边界：remote debugging 开关、Chrome 新版弹窗、DevToolsActivePort、本地端口探测、stale socket、Windows IPC token、cloud browser shutdown 等。

## 5. 它为什么偏向截图和坐标，而不是 selector

`SKILL.md` 的日常用法很有意思：它鼓励 Agent 优先看截图、优先用坐标点击，必要时再用 JS/DOM。

这和传统自动化测试的习惯相反。测试工程师喜欢稳定 selector，因为测试要可重复。但 Agent 做真实任务时，经常面对的是：网站 DOM 很复杂；selector 不稳定；登录态/弹窗/AB test 会改变页面；目标是“一次性完成任务”，不是长期维护测试脚本；模型本身擅长从视觉布局理解按钮、输入框和表单。

所以 Browser Harness 更像是给 Agent 一双眼睛和一只手：先截图理解页面，再像用户一样点击、输入、滚动；如果视觉/坐标不够，再降级到 CDP/JS。这条路线更接近 Computer Use，而不是传统 E2E testing。

## 6. `agent-workspace`：让一次性探索沉淀成技能

仓库最值得借鉴的设计之一是 `agent-workspace/`。

- `agent-workspace/agent_helpers.py` 是 Agent 可以自己补充 helper 的地方；
- `agent-workspace/domain-skills/` 里有大量站点/任务技能，例如 Amazon、arXiv、Gmail、GitHub、LinkedIn、Shopify Admin、YouTube、Zillow 等；
- `interaction-skills/` 则沉淀了 browser mechanics，例如 cookies、iframes、dialogs、downloads、drag-and-drop、shadow DOM、tabs、uploads、viewport 等。

这说明 Browser Harness 把浏览器自动化看成一个 **可积累的技能系统**。第一次做某个网站任务，Agent 可能要探索、试错、写 helper；第二次再做同类任务，就可以复用 domain skill。

这和很多 browser agent 项目不同。很多项目把“浏览器操作能力”封装在框架里，Browser Harness 则把能力外置成 agent 可读、可编辑、可贡献的知识库。

## 7. 本地与云端：同一套 helper，换后端即可

Browser Harness 支持三种常见连接方式：

1. 连接用户正在使用的本地 Chrome profile；
2. 用 `--remote-debugging-port=9222` 和独立 `--user-data-dir` 启动一个隔离 Chrome；
3. 使用 Browser Use Cloud，通过 `BROWSER_USE_API_KEY` 启动远程 browser。

这三种模式背后尽量复用同一套 helper。Agent 不需要关心浏览器是在本地还是云端，它调用的仍然是 `new_tab()`、`page_info()`、`click_at_xy()`、`js()` 这些动作。

这个抽象很实用：本地模式适合复用真实登录态，云端模式适合可扩展、代理、captcha solving、多浏览器并发。对 builder 来说，这是一个很好的 pattern：**API 保持稳定，浏览器后端可替换。**

## 8. 限制与风险

Browser Harness 的“薄”也是它的风险来源：

1. **真实浏览器意味着真实权限。** 复用用户 profile 很强大，但也意味着 Agent 可能接触登录态、私密页面和真实账户操作。
2. **CDP/Chrome 行为会变。** Chrome 136/144/147 的 remote debugging 行为变化已经写进文档，未来还会继续变。
3. **坐标点击不一定稳定。** 对一次性任务很自然，但对长期可重复流程，仍需要更多结构化校验。
4. **domain skills 质量会参差。** 如果让 agent 不断生成站点技能，需要有 review、版本管理和安全边界。
5. **不是完整 browser agent。** 它更像 harness，不负责规划、记忆、任务分解、模型选择；这些要由上层 agent 系统提供。

## 9. Builder 应该学什么

Browser Harness 最值得学习的不是 CDP 调用本身，而是它的产品判断：

第一，给 Agent 的工具不一定越抽象越好。很多时候，薄接口 + 可编辑 helper + 原始 escape hatch，比厚框架更适合 LLM 自我修复。

第二，浏览器任务的知识应该沉淀成技能。`agent_helpers.py`、`domain-skills/`、`interaction-skills/` 让浏览器操作从“一次性脚本”变成可复用资产。

第三，真实环境比完美沙箱更重要。Agent 要完成真实任务，就需要登录态、cookie、文件上传、弹窗、跨域 iframe、下载、打印、标签页等真实边界。

第四，harness 和 agent brain 应该分层。Browser Harness 专注浏览器连接与操作，不试图包办规划与推理；这让它可以被 Claude Code、Codex、Hermes 或其他 agent runtime 复用。

如果说 Playwright 是给人类工程师写稳定测试脚本的浏览器自动化框架，那么 Browser Harness 更像是给 AI Agent 的“浏览器神经接口”：足够薄、足够真实、可修补、可积累。
