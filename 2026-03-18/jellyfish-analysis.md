# Jellyfish：一站式 AI 短剧生产工厂，从剧本到成片的完整开源方案

> 仓库：[donghaozhang/Jellyfish](https://github.com/donghaozhang/Jellyfish) · 协议：Apache-2.0 · 技术栈：React 18 + TypeScript + Vite + 多模型 API

## 这是什么

Jellyfish 是一个**一站式 AI 短剧（竖屏短剧/微短剧）生产工具**。它解决的核心问题是：用 AI 生成视频时，角色和场景总是"漂移"——同一个角色在不同镜头里长得不一样。

它的完整流程是：

```
剧本输入 → 智能分镜 → 角色/场景/道具一致性管理 → AI 视频生成 → 后期剪辑 → 一键导出成片
```

![Jellyfish 项目概览](https://raw.githubusercontent.com/donghaozhang/Jellyfish/main/docs/img/project.png)
*图片来源：[donghaozhang/Jellyfish](https://github.com/donghaozhang/Jellyfish) 项目截图*

## 为什么值得关注

### 1. 一致性是核心卖点

AI 生成视频最大的痛点就是一致性。Jellyfish 用**全局种子 + 统一风格 + 资产复用**三板斧来解决：

- **全局种子防漂移**：项目级别锁定种子，所有分镜继承同一风格
- **资产双层体系**：项目资产库 + 全局资产库，角色/场景/道具/服装全生命周期管理
- **跨分镜引用**：参考图可以在分镜之间复用，ControlNet 骨骼/深度控制动作

### 2. 工业化生产流程

不是玩具，是想做成能落地的生产线：

| 模块 | 干什么 |
|------|--------|
| **章节拍摄工作台** | 剧本 → 智能精简 → 分镜提取 → 编辑 → 视频生成 → 预览 |
| **分镜精细控制** | 景别/角度/运镜/情绪/时长/氛围，首尾关键帧独立提示词 |
| **高级生成控制** | ControlNet 骨骼深度、智能对口型、多模型切换 |
| **视频后期剪辑** | 时间线编辑、多轨、素材库拖拽、最终导出 |
| **Agent 工作流** | 类似 Dify 的节点式编排，剧情提取/角色提取/分镜建议 |
| **模型管理** | OpenAI/Claude/通义/混元/Midjourney/Runway/Kling/Luma 多供应商 |

### 3. Agent 工作流编辑器

这是最有意思的部分。Jellyfish 内置了一个**类 Dify 的节点式工作流编辑器**（基于 React Flow），你可以自定义 Agent 来做：

- 剧情自动提取
- 角色自动识别和描述生成
- 分镜建议和提示词自动填充

这意味着你可以把整个短剧生产流程编排成自动化的 pipeline。

## 技术架构拆解

```
前端层：React 18 + TypeScript + Vite
├── UI：Ant Design + Tailwind CSS
├── 状态：Redux Toolkit / Zustand
├── 工作流：React Flow（节点式编排）
├── 播放器：Video.js / Plyr
└── 编辑器：Monaco Editor / React Quill

后端层（可选）：Node.js / NestJS / FastAPI / Spring Boot
├── OpenAPI 自动生成前端请求代码
└── pnpm run openapi:update 一键同步

AI 层：多模型 API 对接
├── 文本：OpenAI / Anthropic / 通义 / 混元
├── 图像：Midjourney / DALL-E
└── 视频：Runway / Kling / Luma
```

值得注意的是，前端请求函数和类型定义是从后端 OpenAPI 文档**自动生成**的（`front/src/services/generated/`）。这是个好实践，保证前后端接口不会漂移。

## 开发状态

项目处于活跃开发中。已完成的部分：

- ✅ 模型管理（多供应商、多类型、默认配置）
- ✅ 项目管理（CRUD、全局风格与种子）
- ✅ 项目工作台和章节拍摄工作台的交互层

进行中：

- 🚧 完整分镜编辑 + 视频生成 + 预览流程
- 🚧 高级提示词模板与智能填充

## Builder 视角：能拿来干什么

**如果你在做 AI 视频相关产品**，Jellyfish 的架构设计值得参考：

1. **资产一致性方案**：全局种子 + 资产库双层体系，这套方案解决了 AI 生成内容最核心的痛点
2. **Agent 工作流**：把视频生产流程拆成可编排的节点，这个思路可以复用到任何 AI 内容生产场景
3. **多模型切换架构**：同时对接 6+ 视频/图像/文本模型的管理层，对需要多模型协作的产品有参考价值
4. **OpenAPI 前后端同步**：自动生成前端类型和请求代码，避免接口漂移

**适合的场景**：
- 短剧/微短剧批量生产
- AI 影视工作室
- 教育培训视频制作
- 品牌/电商产品宣传短片

## 和同类项目的对比

和我们之前分析过的项目对比：

- **vs Omniclip**：Omniclip 是通用浏览器端视频编辑器，Jellyfish 专注 AI 短剧生产流程
- **vs LTX-Desktop**：LTX 是 AI 视频生成桌面端，Jellyfish 多了剧本→分镜→剪辑的完整链路
- **vs FunCineForge**：FunCineForge 做 AI 电影配音，Jellyfish 做 AI 短剧从头到尾的生产

Jellyfish 的差异化在于**垂直深耕短剧场景**，特别是一致性管理和工业化流程。

## 总结

Jellyfish 试图解决 AI 视频生成领域最难的问题——一致性，同时把短剧生产做成可工业化的流水线。虽然还在早期开发阶段，但架构设计思路清晰，资产管理 + Agent 工作流 + 多模型切换的组合很有想象空间。

对于做 AI 视频产品的 builder，这个项目的架构模式比代码本身更有参考价值。

🦞
