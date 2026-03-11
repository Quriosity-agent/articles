# Ghost OS 技术分析：让 AI 代理真正“操作电脑”

> 项目仓库：<https://github.com/donghaozhang/ghost-os>

Ghost OS 是一个面向 **macOS 桌面自动化** 的开源 Agent 基础设施：它把“AI 能看见并操作 UI”这件事封装成 MCP Server（26 个工具），让 Claude Code、Cursor、VS Code 等任何 MCP 客户端都能调用。

核心不是“又一个截图点点点工具”，而是三层能力组合：

1. **AX 可访问性树优先**（结构化、可审计）
2. **CDP + 本地视觉模型兜底**（解决 Chrome/网页 AX 信息不足）
3. **Recipe 工作流沉淀**（把一次昂贵推理变成可复用脚本）

---

## 1. Ghost OS 是什么（定位）

从代码结构看（`Sources/GhostOS/*` + `vision-sidecar/server.py`），Ghost OS 不是通用“智能体框架”，而是一个 **Computer Use Runtime**：

- 对上：暴露 MCP 工具接口（`MCPServer.swift`, `MCPTools.swift`）
- 对下：调用 macOS AX、输入注入、窗口管理、屏幕截图
- 旁路：通过 Python sidecar 调 ShowUI-2B（本地 VLM grounding）
- 记忆层：Recipe JSON（`recipes/*.json`, `RecipeEngine.swift`）

一句话：**把“代理执行真实桌面任务”这层做成可组合、可诊断、可沉淀的系统能力。**

---

## 2. 核心架构（按模块拆解）

### 2.1 MCP 控制面：同步、可预测、强调稳定性

- `MCPServer.swift`：stdio JSON-RPC，兼容 `Content-Length` 与 NDJSON 两种 transport
- 初始化时设置全局 AX 超时 `AXTimeoutConfiguration.setGlobalTimeout(5.0)`，避免系统 API 卡死
- `MCPDispatch.swift`：统一路由工具，标准化 `ToolResult`

这意味着它优先追求 **可控失败**，而不是“无限等待直到成功”。

### 2.2 Perception：AX-first + 语义深度穿透

`Perception.swift` 的策略很工程化：

- `ghost_context/state/find/read/inspect/...` 全是先读 AX tree
- 对 web/electron 深层结构，用“semantic depth tunneling”：
  - 空布局容器不计深度成本
  - 真正有语义内容的节点才消耗 depth
- 针对 Chrome 额外做了：
  - DOM id 直查（`AXDOMIdentifier`）
  - CDP fallback（`CDPBridge.swift`）
  - 视觉 fallback（`VisionPerception`）

这个组合在实操里很关键：**先结构化，再补视觉，不盲目全靠像素。**

### 2.3 Action：AX 原生优先，合成输入兜底

`Actions.swift` 体现了“行动回路”：

1. 定位目标
2. 尝试 AX 原生动作（例如 `AXPress`, `AXValue`）
3. 失败后用坐标/合成事件 fallback
4. 做 readback/等待验证

新版本还增加了 `hover / long_press / drag / annotate`，把很多现实任务（菜单悬停、拖拽文件、滑条调整）纳入可用范围。

### 2.4 Vision Sidecar：本地 VLM grounding，而非云端 API

`vision-sidecar/server.py` 是独立 HTTP 服务：

- `/ground`：ShowUI-2B 定位单个元素坐标
- `/detect`、`/parse`：目前还是 placeholder（仓库中已明确）
- 懒加载模型，支持 idle timeout 自动退出

所以目前视觉层能力重点是 **“找一个目标”**，不是“完整检测全屏 UI 图谱”。

### 2.5 Recipe Engine：把一次“会做”变成“永远会做”

`RecipeEngine.swift` + `RecipeStore.swift` + `recipes/*.json` 形成可复用流程层：

- 参数化替换（`{{param}}`）
- preconditions
- step + wait_after
- 失败策略（stop/skip）
- 执行结果与时延回传

这就是 Ghost OS 与很多“纯在线决策 Agent”最大的差异：
**学习一次流程，然后以低成本稳定重放。**

---

## 3. 典型工作流（实际运行路径）

以“发 Gmail”为例：

1. Agent 先 `ghost_recipes` 看有没有现成流程
2. 找到 `gmail-send` 后 `ghost_run`
3. Recipe 执行 click/type/press/hotkey + wait
4. AX 找不到时可走 CDP/VLM fallback
5. 输出结构化 step result（成功/失败原因）

这条路径把模型推理开销从“每步都思考”转成“首次编排后稳定执行”。

---

## 4. 目标用户与适用场景

### 目标用户

- 做 AI agent 产品的开发者（尤其 MCP 生态）
- 需要跨浏览器 + 原生 App 自动化的个人/团队
- 对“本地运行、数据不出机”有要求的用户

### 适用场景

- 跨应用操作：Slack + Finder + Browser 串联
- 重复办公流程：邮件、资料整理、报表下载
- 低代码“操作脚本化”：把专家操作沉淀为 recipe

---

## 5. 与邻近项目/生态的实用对比

> 这里用“工程使用感”来比，不做营销式对比。

### vs Anthropic Computer Use / Operator 类纯视觉路线

Ghost OS 优势：
- AX tree 带来结构化对象（role/name/actionable），调试更可解释
- 本地运行可控，数据路径清晰
- Recipe 可复用，长期成本更低

纯视觉路线优势：
- 跨系统/跨环境更统一（不依赖特定 AX 语义）

结论：**Ghost OS 更像“macOS 专精、工程化可运维”的路径。**

### vs Playwright / Browser-only 自动化

Playwright 强在 Web，但不解决 Finder/Slack/系统弹窗。
Ghost OS 目标是 browser + native app 一起打通。

结论：如果你的代理任务边界只在网页，Playwright 很高效；
如果是真实桌面工作流，Ghost OS 的覆盖面更实用。

### vs OpenClaw（Browser DOM automation）

OpenClaw 在浏览器控制链路成熟；Ghost OS 强在 macOS 全局桌面。
两者并非互斥，更像分工：
- Web-heavy：DOM/CDP 优先
- Desktop-heavy：AX + recipe 优先

---

## 6. 当前优势（基于仓库实现）

1. **架构清晰**：MCP、Perception、Actions、Vision、Recipes 分层明确
2. **失败可诊断**：doctor/setup/health、step 级错误信息比较完整
3. **性能意识强**：AX 超时保护、语义深度、CDP 快速 fallback
4. **本地优先**：ShowUI-2B sidecar 本地运行，隐私与可控性更高
5. **可沉淀性**：recipe 让流程资产化，而不是一次性 prompt engineering

---

## 7. 当前限制与风险

1. **平台限制**：目前聚焦 macOS（Swift + AXorcist + ScreenCaptureKit）
2. **视觉能力未完全闭环**：`/detect`、`/parse` 仍是 placeholder
3. **网页复杂度仍高**：Chrome AX 退化为 AXGroup 时，仍需 CDP/VLM 兜底
4. **坐标映射与窗口状态**：多显示器、最小化窗口、Space 切换依旧是易错点
5. **Recipe 维护成本**：UI 改版后 recipe 可能失效，需要版本化治理

---

## 8. 给 Builder 的落地建议

1. **优先 recipe-first 编排**：先跑通一次，再沉淀成 JSON
2. **工具调用顺序固定化**：`ghost_context` → action → `ghost_wait`
3. **网页场景优先 DOM id/CDP**，再用 VLM（速度和稳定性更好）
4. **把失败当一等公民**：接入 `ghost_doctor` 思维，记录失败上下文
5. **建立 recipe 回归测试**：关键流程定时跑，监控成功率

---

## 结论

Ghost OS 的价值不在“炫技式 UI 自动化”，而在于它把 Agent 的 Computer Use 做成了一个可运维系统：

- 有结构化感知（AX）
- 有现实兜底（CDP + VLM）
- 有流程资产化（Recipe）

如果你在做“让代理真正完成跨应用任务”的产品，它提供的是一条非常实用的工程路线：
**把一次成功操作，变成团队可重复的能力。**

🦞
