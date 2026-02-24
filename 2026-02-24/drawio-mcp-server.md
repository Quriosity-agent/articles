# Draw.io 官方 MCP Server：让 AI 直接画架构图

**来源：GitHub - jgraph/drawio-mcp**

---

## 一句话总结

Draw.io 官方发布了 MCP Server，让 Claude 等 LLM 能直接创建和打开 draw.io 图表——在聊天中内嵌交互式图表、在浏览器中打开编辑器、或生成本地文件，四种方式任选。

---

## 为什么值得关注？

Draw.io 是全球最流行的免费图表工具之一（架构图、流程图、UML 等），现在它通过 MCP 协议直接接入了 AI 工作流。这意味着你可以对 Claude 说"画一个微服务架构图"，它直接出图，不用你手动拖拽。

---

## 四种集成方式

| 方式 | 工作原理 | 适合场景 |
|------|---------|---------|
| **MCP App Server** | 图表直接嵌入聊天界面 | Claude.ai 在线对话 |
| **MCP Tool Server** | 在浏览器中打开 draw.io 编辑器 | 本地桌面工作流 |
| **Skill + CLI** | 生成 `.drawio` 文件，可导出 PNG/SVG/PDF | Claude Code 本地开发 |
| **Project Instructions** | 零安装，Claude 通过 Python 生成 draw.io 链接 | 快速上手，无需配置 |

---

## MCP App Server（推荐）

最简单的方式——零安装，直接添加远程 MCP 服务器：

```
https://mcp.draw.io/mcp
```

在 Claude.ai 或任何支持 MCP Apps 的客户端中添加这个 URL，图表就会**直接渲染在对话中**，作为可交互的 iframe。点击"Open in draw.io"按钮还能跳转到编辑器继续修改。

---

## MCP Tool Server

npm 包 `@drawio/mcp`，一行命令启动：

```bash
npx @drawio/mcp
```

支持三种输入格式：
- **XML** — draw.io 原生格式
- **CSV** — 表格数据自动转图表
- **Mermaid.js** — 用文本语法描述图表

图表会在浏览器中直接打开 draw.io 编辑器，支持亮色/暗色模式。

---

## Skill + CLI（Claude Code 用户）

无需 MCP 配置，复制一个 Skill 文件即可。Claude Code 会生成原生 `.drawio` 文件，还能通过 draw.io Desktop CLI 导出：

- `.drawio.png` — PNG 图片（内嵌 XML，可重新编辑）
- `.drawio.svg` — SVG 矢量图
- `.drawio.pdf` — PDF 文档

用法：`/drawio png 画一个用户登录流程图`

---

## Project Instructions（零安装方案）

最轻量的方式：把一段指令粘贴到 Claude Project 中，Claude 就会用 Python 代码执行来生成 draw.io 链接。不需要安装任何东西，支持 XML、CSV 和 Mermaid 格式。

---

## 实际意义

这个项目解决了 AI 辅助开发中的一个痛点：**AI 能写代码但画不了图**。现在：

- 需求评审时："帮我画个系统架构图" → 直接出图
- 代码审查时："把这个模块的调用关系画出来" → 自动分析并生成
- 文档编写时："给这个 API 画个序列图" → 嵌入文档

结合 draw.io 的生态（免费、开源、支持 Confluence/Notion/VS Code），这让 AI 生成的图表能无缝融入现有工作流。

---

**仓库**：<https://github.com/jgraph/drawio-mcp>
**npm**：`@drawio/mcp`
**托管端点**：`https://mcp.draw.io/mcp`
**Star 数**：567 ⭐

---

*本文基于 jgraph/drawio-mcp 开源仓库内容编译整理。*
