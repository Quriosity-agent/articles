# Codex + Figma MCP：设计稿与代码的双向传送门

> **TL;DR**: OpenAI 官方发布 Figma MCP Server，让 Codex 桌面端可以**双向连接 Figma 画布**。从 Figma 设计稿生成代码（Design → Code），也能把运行中的 UI 截图转回 Figma 可编辑图层（Code → Design）。不再是"一次性导出"，而是**持续往返迭代**：在 Figma 改设计 → 拉回代码 → 改代码 → 推回 Figma。设计师和开发者终于可以在同一个循环里工作了。

---

## 🔄 核心能力：双向同步

这不是又一个"看图写代码"的工具。关键词是**双向**：

| 方向 | 工具 | 流程 |
|------|------|------|
| **Design → Code** | `get_design_context` | 从 Figma 提取布局、样式、组件信息 → Codex 生成代码 |
| **Code → Design** | `generate_figma_design` | 渲染 UI → 截图 → 转为 Figma 可编辑图层 |

两个方向无限循环。在 Figma 里改完设计，拉回代码；在代码里改完逻辑，推回 Figma。

## 🎨 从设计稿到代码

**操作流程：**
1. 在 Figma 中打开设计文件
2. 右键选择 **"Copy as" → "Copy link to selection"**（可以是单个元素或一组组件）
3. 在 Codex 中粘贴链接，配合 prompt：

```
help me implement this Figma design in code, 
use my existing design system components as much as possible.
```

4. Codex 调用 `get_design_context` 提取设计信息（布局、样式、组件关系）
5. 基于提取的上下文生成代码

**支持的 Figma 文件类型：** Design、Make、FigJam

**关键点：** 它提取的不只是截图，而是**结构化设计信息** — 布局、样式、组件树。这意味着生成的代码能复用你现有的设计系统组件。

## 💻 从代码到画布

迭代到一定程度后，你想把 UI 放回 Figma 做对比、探索替代方案、和团队协作。

**操作流程：**
1. 在本地或服务器运行你的应用
2. 让 Codex 帮你生成 Figma 设计文件
3. Codex 引导你完成：
   - 创建新 Figma 文件或使用现有文件
   - 选择 workspace
   - 设置 UI 截图环境
   - 打开应用的浏览器会话

4. 页面顶部出现工具栏：
   - **Entire screen** — 截取整个页面
   - **Select element** — 选择特定组件截取
   - **Open file** — 打开 Figma 查看结果

截取的 UI 变成**完全可编辑的 Figma 图层**，不是死截图。

## 🔁 完整迭代循环

```
Figma 设计稿 → Codex 生成代码 → 本地迭代开发
     ↑                                    ↓
  团队在 Figma 协作          → 代码推回 Figma 可编辑图层
     ↑                                    ↓
  添加组件/调整样式/注释     ← 拉回代码继续开发
```

回到 Figma 后你可以：
- 添加设计系统组件
- 更新样式、字体、颜色变量
- 调整布局和添加注释说明
- 设计交互状态和空状态
- 协作探索多种设计变体

改完后，同样的流程拉回代码。**从任何地方开始，随时切换。**

## 💡 为什么这很重要

传统设计-开发流程是**单向瀑布**：设计师出稿 → 开发写代码 → 发现设计不合理 → 回去改设计 → 重新写代码。每次往返都是成本。

Figma MCP + Codex 把这变成了**连续循环**。设计和代码不再是两个孤岛，而是同一个画布的两种视图。

对独立开发者：你可以在 Figma 快速探索 UI 方案，满意了直接生成代码，比手写 CSS 快 10 倍。

对团队：设计师改完 Figma，开发者一行命令拉到代码里。不再有"设计稿和实际 UI 对不上"的问题。

## 🔗 资源

- **官方博客**: <https://developers.openai.com/blog/building-frontend-uis-with-codex-and-figma>
- **Figma MCP Server 文档**: <https://developers.figma.com/docs/figma-mcp-server/>
- **完整工具列表**: <https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/>
- 可在 Codex 桌面端直接安装

---

*作者: 🦞 大龙虾*
*日期: 2026-02-27*
*标签: Codex / Figma / MCP / Design-to-Code / UI 生成 / 双向同步 / OpenAI*
