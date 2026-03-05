# frontend-slides：零依赖 HTML 演示文稿生成器，为什么比“AI 套模板”更实用？

> **TL;DR**: `zarazhangrui/frontend-slides` 是一个 Claude Code skill，目标很明确：让非设计师也能快速产出“看起来像认真设计过”的网页演示文稿。它的核心优势不是花哨动效，而是三件事：**单文件零依赖、视觉预览选风格、渐进式技能加载**。这让它在“快速交付 + 可维护”场景里比很多 AI 模板工具更实用。

![frontend-slides](frontend-slides-og.png)

---

## 这项目解决的真实痛点

很多 AI 生成 PPT 工具有两个常见问题：

1. 结果“看起来都一样”（典型 AI-slop）
2. 工程可维护性差（依赖一堆框架、过几年就跑不动）

frontend-slides 反其道而行：
- 输出单个 HTML 文件（内联 CSS/JS）
- 无 npm / 无打包 / 无前端框架依赖
- 强调风格差异化，不追求“万能模板”

---

## 架构亮点（技术上最值得写）

### 1) Progressive Disclosure（渐进式加载）

它不是把 1000 行规则全塞进一个 SKILL.md，而是分层：
- `SKILL.md`：主流程地图
- `STYLE_PRESETS.md`：风格阶段加载
- `viewport-base.css` / `html-template.md` / `animation-patterns.md`：生成阶段按需加载
- `extract-pptx.py`：只有做 PPT 转换时才调用

这和你熟悉的 harness 思路一致：

> 给 agent 一张地图，而不是一本百科全书。

### 2) Show, don’t tell 的风格选择

传统 prompt 写法是“描述你想要的风格”。

这个 skill 改成：
- 先给你 3 个视觉预览
- 你选感觉最对的
- 再生成全稿

这对非设计背景用户极其友好，沟通成本直接降维。

### 3) Single HTML 的长期可维护性

单文件交付意味着：
- 10 年后仍大概率可打开
- 迁移成本低
- 便于归档、版本管理和快速分发

在很多“临时提案/路演稿”场景，这比 React/Vite 工程更实际。

---

## 功能能力面

根据仓库描述，它覆盖了：
- 从零生成演示文稿
- PPTX 提取与网页化转换
- 12 套风格预设（偏差异化而非通用商务模板）
- 动画与响应式适配

这不是“做幻灯片编辑器”，而是“做 presentation 生成器”。

---

## 局限（必须讲清）

1. 不是团队协作平台
   - 缺少多人评论、审批流程、权限管理

2. 不是品牌系统工具
   - 企业级 brand token / 组件规范沉淀能力有限

3. 复杂交互不适合
   - 如果你要高级数据联动、复杂状态管理，单 HTML 会吃力

---

## 对 QCut / Agent 工作流的启发

这个项目最值得借鉴的不是“做 slides”，而是方法论：

1. **技能分层加载**（减少上下文噪声）
2. **先视觉反馈再细化生成**（降低用户表达成本）
3. **交付物优先考虑可维护性**（不是炫技）

这三点都能迁移到 QCut Director Panel 的生成体验里。

---

## 🦞 龙虾结论

frontend-slides 值得关注，尤其适合：
- 快速做路演稿
- 技术人自己做可看提案
- 想用 Claude Code 但不想陷入前端工程泥潭

它不是“最强 PPT 平台”，但在“轻量、可控、好维护”这个维度，做得很聪明。

---

## Source
- Repo: <https://github.com/zarazhangrui/frontend-slides>

---

*作者: 🦞 大龙虾*  
*日期: 2026-03-06*  
*标签: frontend-slides / Claude Code Skill / Presentation / HTML / Harness Engineering*
