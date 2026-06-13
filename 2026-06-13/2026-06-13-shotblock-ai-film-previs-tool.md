# Shotblock 深度拆解：AI 视频真正缺的不是 Prompt 模板，而是可验证的镜头预演层

> **TL;DR:** Shotblock 是一个免费、免登录、运行在浏览器里的 3D 分镜与镜头规划工具。它的重点不是把视频模型的 prompt 写得更华丽，而是把角色站位、道具、机位、镜头运动、180° 轴线、景别、时长和导出格式先变成可视化、可检查、可复用的 shot plan。对 AI 视频创作来说，这类工具的价值在于：把“导演脑中的空间关系”前置成机器可读的 storyboard、prompt、reference pack 和 JSON，而不是等视频模型生成失败后再靠文字反复补救。

- **Source:** [Shotblock live app](https://shotblock.vercel.app/) / [GitHub repo](https://github.com/shanghaicellcenter/shotblock)
- **Release:** `v0.1.0`（GitHub release published 2026-06-11）
- **Topic:** AI video / 3D previs / storyboard / shot planning / lens math / prompt export
- **Tags:** AI 视频 / 3D 分镜 / 预演 / 镜头调度 / 180° 规则 / Storyboard / Veo / Runway / Kling / Luma / Sora

![Shotblock browser UI: 3D storyboard and shot-planning workspace](imgs/shotblock-ai-film-previs-tool/shotblock-sample-ui-2.webp)

## 1. Shotblock 解决的不是“生成视频”，而是生成前的导演控制问题

今天的 AI 视频工具已经可以把一句 prompt 变成几秒画面，但创作链路里最不稳定的部分仍然是：**镜头之前的决策没有被结构化**。

导演真正关心的不是“一个人在厨房里争吵”这种语义，而是更细的空间和镜头问题：

- Maya 和 Dan 分别站在哪里？
- 摄影机在轴线的哪一侧？
- 这一镜是 master、OTS、medium shot，还是 close-up？
- 镜头是否 push in？移动距离是多少？
- 下一镜是否违反 180° 规则或造成 jump cut？
- 输出给 Veo、Runway、Kling、Luma、Sora 的 prompt 是否携带同一套空间事实？

Shotblock 的产品定位很明确：它不是又一个视频生成模型，而是一个 **AI filmmaker 的 browser-based previs 工具**。用户先在 3D 空间里搭场景、摆人物、放机位、捕捉 shot，再导出 storyboard、PDF、prompt、shot-list JSON 或 consistency reference pack。

这让它更像 AI 视频时代的“轻量导演台”：把 prompt 之前那些本来留在脑子里、草图里、口头沟通里的导演决策，变成可视化对象和可验证数据。

## 2. 浏览器里的 3D blocking：把空间关系从文字里拿出来

从 live app 和 README 看，Shotblock 的核心入口是一个 3D 工作区。左侧是对象库和 scene outliner，中央是 3D 视口与 camera preview，右侧是 Object / Camera / Shot 属性面板，底部是 Shots / Board / Animatic / Scene Chat。

对象库不是为了做最终画质，而是为了快速建立空间结构：

- character；
- camera；
- cube、table、chair、sofa、bed、counter、sink、desk、shelf；
- practical lamp、real point light；
- wall、door、window、tree、car、ground marker 等常见 set 元素。

README 还提到更深入的 blocking 能力：角色是 15-DOF articulated mannequin，支持 stand、sit、walk、run、point、fight、crouch、fallen、talk 等 pose preset；也支持 joint-level sliders。换句话说，角色不是一张参考图，而是一个可以在三维空间里被摆放、旋转、调整姿势的“动作起点”。

对 AI 视频来说，这一点很关键。很多失败不是因为模型不会生成“争吵”，而是它不知道两个人之间的距离、朝向、前后关系和身体姿势应该如何稳定延续。Shotblock 把这些信息从自然语言里抽离出来，让它们先成为几何事实。

## 3. 机位规划：Shotblock 把“镜头语言”做成 UI 和数据

Shotblock 不只是摆小人。它最有价值的部分在 camera / lens / coverage 层。

README 里列出的镜头能力包括：

- sensor format：Full Frame、Super 35、Alexa 65、IMAX；
- focal length → true field of view；
- hyperfocal 和 depth-of-field readouts；
- 16:9、2.39:1、9:16 等 delivery aspect extraction；
- sensor-true、letterboxed camera preview；
- EWS、ECU、OTS、2-shot、POV、insert 等 framing presets；
- classic 5-camera dialogue coverage generator：master、两个 OTS、两个 CU；
- A/B marks 和 camera movement scrub；
- captured shots 自动带上 movement note，例如 “Push in 1.5m”。

这说明 Shotblock 的重点不是“看起来有 3D 场景”，而是把真实片场里的镜头决策映射到软件对象上：镜头焦段、画幅、机位、运动、景别、时长、shot code 都进入同一套 shot plan。

这对 AI 视频模型特别重要。视频模型可以生成画面，但它不一定理解导演想要的 coverage plan。Shotblock 的价值在于：先把 coverage plan 明确下来，再把它翻译成 prompt、storyboard 和 reference pack。

## 4. 180° 规则和 30° 规则：AI 视频也需要 continuity checker

Shotblock 另一个值得注意的方向是 film grammar checker。

它支持：

- live HUD 里的 180° rule warning；
- storyboard-level flags，提示切换镜头时是否 cross the line；
- cutaway、neutral shot、subject movement 等例外；
- side lock 和 re-establish side workflow；
- 30° rule 检测，提示连续镜头之间的 jump-cut risk；
- 自动 shot-size classification，从 EWS 到 ECU。

这不是传统意义上的“AI 功能”，但对 AI 视频工作流反而非常重要。因为 AI 生成常见的问题不仅是画面瑕疵，还包括剪辑连续性：下一镜方向突然反了、人物视线不接、景别变化太小导致像跳切、同一段对话 coverage 没有建立清楚的轴线。

如果创作者只在 prompt 里写“cinematic dialogue scene”，这些规则很难被稳定执行。Shotblock 的思路是：在生成之前先检查 shot plan 是否合格，把 continuity bug 尽量前移。

## 5. 导出层：真正有价值的是 storyboard + prompts + JSON

Shotblock 的导出菜单和 README 都显示，它并不把成果限制在一张截图里。

当前 app 里可见的导出项包括：

- Storyboard PNG contact sheet；
- Storyboard PDF；
- Storyboard PDF with prompts；
- ZIP：panels + clean frames + prompts。

README 进一步说明输出能力包括：

- 6-up printable storyboard sheet；
- per-shot lens data、movement、action、timing；
- per-shot AI-ready prompts；
- 针对 Veo 3、Runway Gen-4、Kling 2.x、Luma Ray2、Sora 2 的 prompt variants；
- agent-friendly shot list JSON；
- consistency reference pack：character turnarounds、shot frames、per-shot prompts、shot-list JSON。

这里的关键词是 **machine-readable**。如果未来的 AI 视频生产由多个模型、多个 agent、多个渲染/剪辑步骤组成，单纯的自然语言 prompt 不够。你需要一个可以被 pipeline 读取的 shot list：每一镜的机位、焦段、构图、角色、动作、时长、运动和 prompt 都有结构化字段。

这也是 Shotblock 比普通“分镜草图工具”更贴近 AI 视频的地方：它默认把输出对象设计给视频模型和自动化流水线消费。

## 6. Scene Chat：有用，但更像 local scaffold，而不是黑箱生成

Shotblock 有一个 “✨ Scene Chat” 标签。README 描述它可以从一句话生成本地场景，例如 “two friends argue in a kitchen at night”，并生成 characters、furniture kit、blocking、lighting；同时强调 fully local、no API calls。

这点值得单独看。很多 AI 产品把 chat 当成主界面，但 Shotblock 更像把 chat 用作 **scaffolding**：快速铺出一个可编辑的 3D 场景，然后仍然回到导演台里调整对象、机位和镜头。

这比“聊天框直接生成最终视频”更稳。因为 chat 的结果不是终点，而是一个可编辑初稿。创作者仍然可以检查 180° 轴线、调整人物站位、改变焦段、补充 coverage、捕捉 shot、导出 storyboard。

## 7. 和传统 previs 工具的区别：Shotblock 把目标用户指向 AI filmmaker

传统影视行业早就有 previs、storyboard、animatic、Unreal 虚拟制片、摄像机规划软件。Shotblock 的新意不在“3D 预演”本身，而在它把这些能力重新压缩到 AI 视频创作者需要的轻量形态：

| 维度 | 传统 previs / DCC | Shotblock 的取向 |
|---|---|---|
| 学习成本 | 专业软件、复杂资产和渲染流程 | 浏览器里快速摆场景、摆机位 |
| 输出对象 | 给导演、摄影、美术、后期团队看 | 同时给人和视频模型/agent pipeline 用 |
| 镜头信息 | 可能存在于项目文件或人工 notes | 直接进入 storyboard、prompt、JSON |
| 一致性 | 靠导演、分镜师和剪辑流程维护 | 通过 180°/30° 检查和 reference pack 前置维护 |
| AI 适配 | 需要额外整理 prompt/reference | 内置多模型 prompt variants 和 consistency pack |

所以 Shotblock 的产品判断是：AI filmmaker 不一定需要完整的虚拟制片系统，但需要一个足够快的空间 planning layer。

## 8. 对 QCut / AI 视频工具链的启发

如果把 Shotblock 放到 AI 视频生产工具链里看，它给出的信号很清楚：未来的视频创作工具不会只围绕“生成按钮”竞争，而会围绕 **生成前的可控状态** 竞争。

对类似 QCut 的视频工作流，这里有几个可借鉴点：

1. **Shot plan 应该是一等对象**  
   不只是字幕、素材、时间线，也不只是 prompt，而是镜头级别的结构化计划。

2. **空间约束和 prompt 应该分离**  
   prompt 写情绪、动作、风格；3D blocking 或 reference frame 负责站位、机位和构图。

3. **导出给模型的不是一句话，而是一包上下文**  
   storyboard frame、clean frame、角色 turnarounds、镜头 JSON、模型专用 prompt variant 应该一起进入生成流程。

4. **continuity check 可以前置成产品功能**  
   180° 规则、30° 规则、视线、景别变化、镜头方向，都可以在生成前被检查，而不是生成后才发现剪不起来。

5. **AI chat 更适合作为场景 scaffolder**  
   让 chat 生成初始场景，然后进入可编辑空间，而不是把 chat 当作唯一控制面。

## 9. 风险和限制：浏览器轻量化不等于完整制作系统

Shotblock 现在仍然是早期项目。GitHub repo 在 2026-06-11 创建，公开 metadata 显示 star / fork 规模还很小，release 是 v0.1.0。实际生产里还需要关注几个问题：

- WebGL / 浏览器性能对复杂场景的限制；
- 自定义 GLB 资产质量与管理；
- 3D blocking 到视频模型结果之间的 fidelity gap；
- prompt variant 是否能跟上各家视频模型 API 的快速变化；
- 多人协作、版本控制、shot review、时间线整合还没有在当前页面里体现得很完整；
- 轻量 UI 如何避免变成“半个 Blender + 半个分镜软件”的复杂度陷阱。

但这些限制不影响它展示一个重要方向：AI 视频越强，前置规划层反而越重要。因为模型越能生成，创作者越需要回答“到底要生成哪一镜”。

## 10. 结论：AI 视频的下一层工具不是更长 prompt，而是可检查的镜头状态

Shotblock 的核心价值可以总结成一句话：**把 AI 视频的 prompt 之前，补上一层导演可编辑、模型可读取、规则可检查的 shot-planning state。**

它把 3D blocking、真实 lens math、coverage、film grammar、storyboard、animatic、prompt export 和 JSON 打包到一个浏览器工具里。对个人 AI filmmaker 来说，这降低了把“脑内镜头”变成可执行生成计划的门槛；对更大的 agentic video pipeline 来说，它提示了一个更长期的产品方向：

未来的视频生成系统不应该只保存 prompt history，而应该保存完整的 **scene graph + camera plan + continuity checks + per-shot generation context**。

当这层状态存在后，视频模型才不只是“按一句话出片”，而是真正进入可导演、可复盘、可迭代的制作流程。
