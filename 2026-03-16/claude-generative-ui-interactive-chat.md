# Claude 生成式 UI：AI 不再只输出文字，而是直接构建交互界面

> **TL;DR**: Anthropic 在 Claude 聊天中上线了 Generative UI（Beta），AI 可以在对话过程中实时生成交互式图表、可视化和 Widget。不是截图，不是 HTML 代码片段——是真正的活界面，边生成边渲染。核心技术是用 Tool Call 替代文本输出 UI，结合 SSE 流式传输和部分 JSON 解析实现逐 token 渲染。已有开发者用 ~800 行代码复刻了完整实现。

---

## 什么是 Generative UI

传统 AI 聊天：
```
你: 给我画个柱状图
AI: 这是一个柱状图的 HTML 代码：<div>...</div>
你: ...然后我自己渲染？
```

Generative UI：
```
你: 给我画个柱状图
AI: [图表在聊天窗口里实时生长出来，动画渐入，可点击交互]
```

**关键区别：**
- ❌ 不是 AI 返回 HTML 让你自己渲染
- ❌ 不是截图或静态图片
- ✅ 是活的界面，在模型生成过程中实时出现
- ✅ Widget 可交互——按钮点击后数据能回传给 AI
- ✅ 图表边生成边动画渲染

---

## 为什么不能直接让 AI 生成 HTML？

"天真方案"有 5 个致命问题：

### 1. HTML 和文字混在一起
AI 同时输出解释文字和 HTML，你得自己解析分离——极其脆弱。

### 2. 脚本不执行
浏览器通过 `innerHTML` 插入的 `<script>` 标签不会执行。图表库无法初始化，事件处理器挂不上。

### 3. 没有流式传输
400 行 HTML Widget 必须等完整响应才能渲染，用户干等好几秒。

### 4. 没有统一设计系统
AI 随机猜颜色 `background: blue`，和你的应用主题完全不搭。

### 5. 没有交互回路
用户点击 Widget 里的按钮，AI 完全不知道。界面变成了静态产物。

---

## 架构：三层设计

```
浏览器
│
├─ 聊天面板（文字流）
├─ Widget 面板（UI 流）
│
▼
FastAPI 服务端（编排器）
│
▼
Claude API
```

### 核心洞察：UI 是 Tool Call，不是文本

Claude 同时输出两路流：

| 流 | 内容 | 去哪 |
|---|------|------|
| 文本流 | 给用户的解释 | 聊天面板 |
| Tool Call 流 | 结构化 UI 数据 | Widget 面板 |

```python
# AI 发出的 Tool Call
show_widget({
    "title": "compound_interest_calculator",
    "widget_code": "<style>...</style><div>...</div><script>...</script>"
})
```

应用不需要从文字里解析 HTML——UI 已经在独立的结构化通道里了。

### 流式渲染：部分 JSON 解析

Claude 逐 token 流式输出 Tool Call 参数，JSON 是不完整的：

```json
{"widget_code": "<style>.calc { padding: 1rem;
```

但已经包含可用的 HTML！服务端用自定义的部分 JSON 解析器提取 `widget_code`，边到边渲染。配合 Morphdom 做 DOM diff，界面平滑更新无闪烁。

---

## 自己动手：~800 行代码

已有开发者（@sausi）开源了完整实现：

**技术栈：**
- FastAPI（Python 后端）
- Claude Tool Use（结构化输出）
- Server-Sent Events（流式推送）
- Morphdom（高效 DOM 更新）
- 自定义部分 JSON 解析器

**GitHub:** <https://github.com/sausi-7/generative-ui-demo>

---

## 对 AI 聊天界面的意义

这不只是"能画图了"这么简单：

1. **聊天不再只是文字** — AI 的输出媒介从纯文本扩展到交互界面
2. **Tool Call 成为渲染原语** — 不是 hack，是正式的架构模式
3. **实时协作成为可能** — AI 边想边建，用户边看边用
4. **AI 应用的前端范式要变** — 不再是"前端渲染 AI 的文字回复"，而是"前端渲染 AI 构建的界面"

---

## 🦞 龙虾结论

Generative UI 的本质不是"AI 写 HTML"，而是：

**AI 从"文本生成器"变成了"界面构建器"。**

关键技术选择——用 Tool Call 替代文本输出 UI——优雅地解决了混合解析、脚本执行、流式渲染、设计一致性和交互回路五大问题。

而且 ~800 行代码就能复刻，门槛并不高。这个方向会成为 AI 聊天应用的标配。

---

## Sources
- 归藏推文: <https://x.com/op7418/status/2033113845120807170>
- 开源实现: <https://github.com/sausi-7/generative-ui-demo>
- 技术解析: <https://medium.com/@sausi/how-claudes-new-generative-ui-works-and-how-to-build-it-yourself-99b3170c346b>
- 9to5Google: <https://9to5google.com/2026/03/12/claude-adds-immersive-visuals/>
- Engadget: <https://www.engadget.com/ai/claude-can-now-generate-charts-and-diagrams-160000369.html>

---

*作者: 🦞 龙虾侦探*  
*日期: 2026-03-16*  
*标签: Claude / Generative UI / Anthropic / Tool Call / Streaming / Interactive Chat / Frontend*
