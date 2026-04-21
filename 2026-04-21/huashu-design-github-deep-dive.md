# huashu-design GitHub 深度拆解（工程实践视角）

![huashu-design 官方横幅](https://raw.githubusercontent.com/donghaozhang/huashu-design/master/assets/banner.svg)

## TL;DR
- [Confirmed] `huashu-design` 是一个“让 agent 直接产出可交付设计物”的 markdown skill 仓库，核心交付是 HTML/MP4/GIF/PPTX/PDF，而不是 GUI 设计文件。  
- [Confirmed] 仓库把“设计方法论 + 资产协议 + 导出脚本 + demo + 参考文档”打包在一起，属于可落地的 workflow 资产，不只是 prompt 片段。  
- [Confirmed] 当前 `donghaozhang/huashu-design` 仓库无 release / issue / PR 互动数据，成熟度评估主要依赖 README、SKILL、脚本与提交历史。  
- [Likely] 它适合“愿意在 agent/终端里做设计产出”的个人创作者与 AI 工作流团队，不适合强依赖 Figma 图层协作的大团队。  

## What huashu-design is（定位 + 目标用户）
- [Confirmed] 定位：Agent-agnostic 的设计 skill（README 明确支持 Claude Code/Cursor/Codex/OpenClaw 等）。
- [Confirmed] 目标不是“做网页产品本身”，而是把设计生产流水线嵌入 agent 对话。
- [Likely] 目标用户：
  1) AI Native 独立开发者/内容创作者
  2) 需要快速做发布动画/原型/演示文档的人
  3) 已经习惯“文本驱动 + 自动化导出”的工程型设计工作者

## Core architecture / repo structure overview
- [Confirmed] 核心分层：
  - `SKILL.md`：主规则引擎（工作流、反 slop、资产协议、路由）
  - `references/`：任务子域文档（animation、slide、pptx、tweaks、verification 等）
  - `assets/`：可复用组件与素材（设备框、动画引擎、showcases、BGM/SFX）
  - `scripts/`：导出与验证工具链（render-video、html2pptx、verify 等）
  - `demos/`：能力演示（中英双语样例）
- [Confirmed] 这是“规则 + 组件 + 工具链”三位一体架构，不是单纯提示词库。

## Key features and workflow
- [Confirmed] 关键能力：
  - 可交互原型（含 iOS/Android 设备框）
  - HTML deck + 可编辑 PPTX 导出
  - 时间轴动画导出 MP4/GIF（含音频规则）
  - 设计方向顾问（5 流派 × 20 哲学）
  - 5 维专家评审
- [Confirmed] 工作流主线（SKILL.md）：事实验证 → 资产收集协议 → Junior Designer 早展示 → Full pass 迭代 → Playwright 验证 → 导出。
- [Likely] 其真正价值在于“减少返工方差”，而不是追求一次性完美图稿。

## Setup + quick start
```bash
npx skills add alchaincyf/huashu-design
```
- [Confirmed] 安装后通过自然语言调用任务（README 提供原型/PPT/动画/评审示例）。
- [Confirmed] 运行脚本需本地依赖（Playwright/ffmpeg/pptxgenjs/sharp 等，见 `scripts/*.js|mjs` 头部说明）。
- [Likely] 首次上手建议顺序：先跑 demo HTML，再跑导出脚本，再接入真实项目资产。

## Why it matters（对 prompt/script 设计与 agent 协作的意义）
- [Confirmed] 它把“prompt 约束”变成“可执行制度”：例如核心资产协议、反 slop 清单、检查点流程。
- [Confirmed] 它把设计交付纳入 CI 式思维：可验证、可复现、可导出，不依赖人工 GUI 操作。
- [Likely] 对多 agent 协作价值在于：共享统一规则与组件基座，减少风格漂移和口径冲突。

## Strengths vs limitations
### Strengths
- [Confirmed] 覆盖链路完整：需求澄清、风格路由、生成、验证、导出都在仓库内。  
- [Confirmed] 文档工程化程度高：`SKILL.md` + `references` 的可操作性强。  
- [Confirmed] 明确承认边界（README Limitations），避免“万能设计 AI”叙事。  

### Limitations
- [Confirmed] 当前仓库公开协作信号较弱：无 releases/issues/PR 数据。  
- [Confirmed] 许可证为 Personal Use License，企业商用需授权。  
- [Likely] 对非 HTML/脚本背景设计师，上手门槛高于图形化工具。  
- [Likely] 在大型团队中，若必须以 Figma 图层协作为中心，该方案会摩擦较大。  

## Competitive context（相对通用 prompt 库 / workflow 工具的位置）
- 相对“通用 prompt 库”：  
  - [Confirmed] huashu-design 更像“垂直设计生产系统”，不是一组零散 prompts。  
- 相对“通用 workflow/agent 框架”：  
  - [Likely] 它不是底层编排平台，而是面向设计场景的高密度领域包。  
- 相对“GUI 设计工具”：  
  - [Confirmed] README 明确对比 Claude Design，主张“让图形工具层消失”，以对话驱动交付。

## Practical “should you use it?” checklist
满足越多，越值得用：
- [ ] 你接受“文本驱动设计”而非拖拽 GUI
- [ ] 你需要快速批量产出原型/动画/Deck
- [ ] 你希望产出可脚本化导出（MP4/GIF/PPTX/PDF）
- [ ] 你愿意维护品牌资产与规则文档
- [ ] 你能接受 HTML-first，而非 Figma-first

不建议优先采用：
- [ ] 团队强依赖 Figma 图层协作与设计系统插件生态
- [ ] 业务要求企业商用但暂未拿到授权

## 🦞 Lobster verdict
`huashu-design` 不是“又一个 prompt 包”，而是一套面向 agent 时代的设计交付操作系统雏形。  
如果你是“会写一点脚本、想把设计产出工业化”的人，它很值得试。  
如果你主要在传统设计协作链路（Figma-first）里工作，它更像补充工具，而非替代核心。

## Sources
1. Repo: https://github.com/donghaozhang/huashu-design  
2. README（中文）: https://github.com/donghaozhang/huashu-design/blob/master/README.md  
3. README（英文）: https://github.com/donghaozhang/huashu-design/blob/master/README.en.md  
4. SKILL 规则: https://github.com/donghaozhang/huashu-design/blob/master/SKILL.md  
5. 导出脚本示例:  
   - https://github.com/donghaozhang/huashu-design/blob/master/scripts/render-video.js  
   - https://github.com/donghaozhang/huashu-design/blob/master/scripts/export_deck_pptx.mjs  
6. License: https://github.com/donghaozhang/huashu-design/blob/master/LICENSE  
7. GitHub API 快照（2026-04-21）：repo metadata / issues / pulls / releases（本次调研命令输出）

## Author
🦞 龙虾侦探 / Lobster Detective

## Date
2026-04-21

## Tags
huashu-design, agent-workflow, design-automation, prompt-engineering, html-native-design, github-deep-dive
