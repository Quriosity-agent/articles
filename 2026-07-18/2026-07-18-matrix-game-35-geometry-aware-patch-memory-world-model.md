---
title: "Matrix-Game 3.5 深度拆解：长期世界模型的记忆，正在从历史帧变成可重投影的 3D Patch"
date: 2026-07-18
source: "https://matrix-game-v3-5.github.io/"
canonical: "https://matrix-game-v3-5.github.io/"
related_sources:
  - "https://matrix-game-v3-5.github.io/paper/Matrix-Game-3.5.pdf"
  - "https://github.com/Riemann-Dynamics/Matrix-Game-3.5"
  - "https://huggingface.co/RiemannDynamics/Matrix-Game-3.5-Base"
tags:
  - Matrix-Game 3.5
  - World Model
  - Patch Memory
  - Warped PRoPE
  - Video Generation
  - Camera Control
  - Interactive World
---

# Matrix-Game 3.5 深度拆解：长期世界模型的记忆，正在从历史帧变成可重投影的 3D Patch

> **TL;DR:** Matrix-Game 3.5 最重要的变化，不是又把视频生成时间拉长了一点，而是重新定义了“记住一个世界”。它用深度、相机内外参把历史画面中的静态 patch 提升到 3D，再按当前视角重投影；动态人物则由多视图 reference tokens 单独维护。配合把相机投影写进位置编码的 Warped PRoPE，以及 Flow Matching + Self-Rollout DMD 蒸馏，论文报告 5B 模型可在单张 H200 上以 720p、最高 20 FPS 运行。需要特别注意：当前公开的是约 20GB 的双向基础模型权重，默认仍要 25 步去噪和预先计算的相机轨迹；README 明确写着实时自回归蒸馏模型“即将发布”。所以今天能下载验证的是几何记忆基础模型，不是论文里完整的实时交互系统。

- **项目页：** [Matrix-Game 3.5](https://matrix-game-v3-5.github.io/)
- **技术报告：** [Matrix-Game 3.5 PDF](https://matrix-game-v3-5.github.io/paper/Matrix-Game-3.5.pdf)
- **代码：** [Riemann-Dynamics/Matrix-Game-3.5](https://github.com/Riemann-Dynamics/Matrix-Game-3.5)
- **模型：** [Matrix-Game-3.5-Base](https://huggingface.co/RiemannDynamics/Matrix-Game-3.5-Base)
- **发布时间：** 2026-07-18
- **访问时间：** 2026-07-20

![Matrix-Game 3.5 official teaser montage](imgs/matrix-game-35-patch-memory/00-teaser.jpg)

*图：项目页官方 teaser 的一帧，同时展示第一人称、第三人称和多种环境。*

## 一句话判断

**Matrix-Game 3.5 把世界模型的长期记忆，从“让生成器回想以前见过的帧”，推进成“先计算旧画面在当前相机里应该出现在哪里，再让生成器补全看不见和不可靠的部分”。**

这是一条很实在的路线。纯视频模型可以学会空间常识，却很难在一分钟自回归生成中持续保存某扇窗、某个路口和某个角色的精确状态。因为历史越长，有限上下文越容易忘；每一轮生成误差还会成为下一轮输入，最后演变成结构漂移。

Matrix-Game 3.5 没有要求一个 Transformer 在隐藏状态里包办全部记忆。它把最适合几何计算的静态场景交给显式重投影，把难以固定在空间坐标里的动态主体交给语义参考 token。生成模型负责的，不再是从零回忆整个世界，而是融合可见记忆并生成缺失区域。

## 1. 3.0 到 3.5：重点从“长时记忆”转向“记忆放在哪里”

Matrix-Game 3.0 已经强调流式生成、长时记忆和相机控制。3.5 并不是把同一方案简单放大，而是进一步追问：当相机绕一圈回到原处，模型凭什么知道旧画面的哪个像素应该落在新画面的哪个位置？

只检索历史帧仍有三个问题：

1. **视角不同。** 正面看见的墙面，侧面重访时会发生透视变化，直接复制或跨帧注意力都需要模型自己推断对应关系。
2. **遮挡不同。** 旧视角可见的物体，在新视角可能被前景挡住；反过来，新视角也会暴露从未见过的区域。
3. **动态物体不能当背景。** 如果把走动的人连同街景一起存入静态记忆，再重投影时就容易产生残影、重复人物或“角色被贴在墙上”的错误。

3.5 的答案是一套不新增可学习参数的 geometry-aware memory：Warped PRoPE 负责让注意力理解相机几何，Patch Memory 负责将历史静态内容搬到当前视角，reference tokens 负责保持动态主体身份。

## 2. Warped PRoPE：把相机投影写进位置编码

普通时空 RoPE 主要编码时间和二维 token 坐标。相机控制通常还要增加额外分支、控制网络，或者把 pose 作为普通条件输入。问题在于，“时间上相邻”和“空间中看向同一位置”不是一回事。

Matrix-Game 3.5 使用 Warped PRoPE，把完整的世界到图像投影矩阵叠加到全部 attention head 通道，而不是只占用一部分通道。论文里的处理可以概括为：

- 用相机内参和外参构造投影矩阵；
- query 侧使用目标帧投影的转置变换；
- key/value 侧使用来源帧投影的逆变换；
- 在同一次 attention softmax 中，同时表达相对时间、图像位置和相机关系。

因此，模型不需要另起一条可学习 camera branch，也不必修改 Wan2.2-TI2V-5B 主干。相机条件成为 attention 本身的一部分。

![Warped PRoPE overlays camera projection across the full attention-head dimension](imgs/matrix-game-35-patch-memory/01-warped-prope.jpg)

*图：原生 PRoPE 与 Warped PRoPE 的差异。后者把投影矩阵覆盖到完整 head dimension，并直接参与 Q/K/V 的 attention 计算。来源：官方技术报告。*

这个设计真正解决的不是“让模型知道相机参数”，而是让不同帧的 token 在计算相关性时，自带一个几何坐标转换。对镜头前进、横移、旋转和旧场景回访来说，这比把 `camera_pose` 当成一串附加数字更贴近问题结构。

## 3. Patch Memory：先重投影，后生成

Patch Memory 是 3.5 的核心。它的工作流可以拆成五步：

1. 从历史生成帧估计深度；
2. 结合相机内参和位姿，把二维像素/patch 反投影到度量 3D 空间；
3. 将这些 3D 点投影到下一目标相机；
4. 用 z-buffer 保留当前视角中最近、应当可见的表面；
5. 将得到的 mosaic memory 作为 token 输入生成器，空洞、遮挡和不可靠区域由 diffusion 补全。

它不是维护一个完整、可编辑的 3D mesh，而是维护能随视角检索的历史外观 patch。这个差异很重要：Matrix-Game 3.5 仍然输出视频，不是从一个显式场景图渲染画面；但相比完全潜在的记忆，它至少把“过去的内容应该出现在哪里”交给了相机几何。

这也解释了为什么项目演示里的重访更稳定。当镜头返回旧地点时，模型不必只凭长期隐藏状态重新画一遍建筑，而是先拿到对齐当前视角的旧材质、轮廓和局部细节，然后生成未覆盖区域。

## 4. 为什么静态与动态必须分开记忆

把所有历史像素都塞进 Patch Memory 会立刻遇到一个问题：世界里的人、车和动物会动。

3.5 增加 motion-aware object filter，通过检测、分割和运动判断，把动态区域排除在静态 mosaic memory 之外。静态场景继续走“深度估计 -> 提升到 3D -> 重投影”的路线；人物和其他主体则由最多四张多视图参考裁剪编码成 sequence-level reference tokens，并配合 subject-region auxiliary loss 保持身份和外观。

![Static scene patches and dynamic subject references are routed through different memory paths](imgs/matrix-game-35-patch-memory/02-static-dynamic-memory.jpg)

*图：静态环境进入 Mosaic/Patch Memory，动态主体进入 reference tokens；运动过滤减少残影和身份泄漏。来源：官方技术报告。*

这不是实现细节，而是世界模型的一条关键原则：

- 静态场景适合绑定到世界坐标；
- 动态主体需要身份一致性，但不能固定在旧坐标；
- 不可见的新区域应该生成，而不是伪装成“已经记住”。

不过当前方法也没有真正维护动态实体的持久状态。论文把“让动态实体在离开视野后继续演化，并在重新出现时保持状态”列为未来方向。现在的 reference tokens 更接近身份与外观锚点，不是完整的角色状态机。

## 5. 从 25 步基础模型到 3 步实时生成器

项目以 Wan2.2-TI2V-5B 为主干，先训练双向 diffusion 基础模型，再把它蒸馏成因果、自回归、少步数生成器。蒸馏分两段：

### 第一段：感知空间里的 Flow Matching

团队没有只在像素或 latent 空间约束输出，而是在冻结的 InternVideo2-1B 特征空间进行感知式因果适配。目标是同时学习自回归延续和少步去噪，为后续蒸馏提供稳定起点。

### 第二段：Self-Rollout DMD

普通 teacher forcing 只让模型看真实历史，部署时却要面对自己生成的历史，训练和推理分布会逐步分叉。Self-Rollout DMD 让 student 在自己的自回归轨迹上训练，并通过 curriculum 逐步加入 CFG、相机控制和 memory conditioning。

最终论文中的因果模型每个 chunk 只需 3 个 denoising steps。再加上 INT8 DiT、`torch.compile`、优化后的 memory retrieval，以及剪枝 75% 的 MG-LightVAE，技术报告给出的运行上限是：

| 项目 | 论文报告配置 |
|---|---|
| 模型 | 5B |
| 输出 | 1280 x 704，通常概括为 720p |
| 因果去噪 | 3 steps / chunk |
| 硬件 | 单张 NVIDIA H200 |
| 速度 | 最高 20 FPS |

这里的限定词必须保留：这是论文系统的性能，不是当前公开基础 checkpoint 的默认性能。

## 6. 数据引擎：先给视频补几何，再训练世界模型

项目页只概括说数据来自 Unreal 模拟、开放世界游戏和互联网视频，没有在正式技术报告中给出可核验的总小时数或总片段数。比规模更值得注意的是它如何把普通视频变成几何训练数据：

- 用 VGGT-Omega 和 Depth Anything 3 的 metric branch 估计位姿、深度和相机内参；
- 对长视频分块，并通过 Sim(3) 对齐统一尺度；
- 用视觉语言模型生成窗口级语义描述；
- 用检测、跟踪、mask 和 DINO 特征挑选动态主体的多视图参考；
- 按重建质量、相机质量、图像/深度质量和任务适配度过滤数据。

这条管线的意义是：互联网视频本来没有干净的 6-DoF 相机轨迹、度量深度和角色 reference，它们需要先被“几何化”和“结构化”，才能进入 Patch Memory 训练。

## 7. 基准真正说明了什么

论文在一分钟 Simple/Hard camera trajectories 上比较相机姿态精度、VBench、效率、回访一致性和前后段画质退化。

![Matrix-Game 3.5 quantitative benchmark](imgs/matrix-game-35-patch-memory/03-benchmark.png)

*图：Matrix-Game 3.5 定量结果。蓝色并不意味着每一列都由 3.5 领先，阅读时要区分姿态、画质、效率和回访指标。来源：官方技术报告。*

最有说服力的是相机控制：

| Split | Rotation error R ↓ | Translation error T ↓ | CMC ↓ | Revisit SSIM ↑ |
|---|---:|---:|---:|---:|
| Simple | 1.63 | 1.10 | 1.11 | 0.439 |
| Hard | 2.70 | 1.25 | 1.33 | 0.414 |

在表中，3.5 的相机姿态指标明显领先；例如 Simple split 的 rotation error 从 SANA-WM + refiner 的 4.50 降到 1.63，Hard split 从 8.34 降到 2.70。回访 SSIM 也最高，这和几何记忆的目标一致。

但它不是所有指标都第一：

- Simple split 的 VBench 80.14，低于 LingBot-World 的 81.82；
- Hard split 的 VBench 80.85，低于 81.89；
- 回访 LPIPS 并非最佳；
- 表中 8 张 H100 的离线吞吐为 10.9 videos/hour，低于 SANA-WM 的 24.1；
- 峰值显存 77GB，也不是最低。

论文还提醒，同一相机位姿下的像素指标会惩罚合理的动态变化。也就是说，角色换了动作可能让 PSNR/LPIPS 变差，却不一定代表世界几何崩坏。因此这张表最能支持的是“相机遵循和静态场景回访更稳”，不能被扩写成“综合画质和效率全面领先”。

## 8. 当前开源了什么，没开源什么

这是目前最容易被项目页演示混淆的部分。

### 已公开

- Apache-2.0 代码仓库；
- 两个 5B 双向基础模型：`first-person.safetensors` 和 `third-person.safetensors`；
- Hugging Face 仓库合计约 20GB；
- 基于 DiffSynth 的推理管线；
- Mosaic Memory 重投影代码；
- vendored Depth Anything 3；
- 第一人称和第三人称样例。

基础模型的输入是 anchor image、文本 prompt 和预先生成的相机轨迹 `.npz`；第三人称还可以提供 0 至 4 张主角参考图。默认每个 block 生成 80 帧、消耗 84 个相机 pose，使用 25 个 denoising steps。官方要求 Linux、至少 64GB 系统内存，以及一张至少 40GB VRAM 的 NVIDIA GPU；704 x 1280 推理峰值约 40GB。

### 尚未公开

- 论文中的蒸馏实时自回归 checkpoint；
- 可直接用键盘即时驱动的完整实时 runtime；
- 项目演示所对应的 H200、INT8、3-step 端到端复现配置。

README 原文明确写着：`The distilled real-time autoregressive models will be released soon.`

所以现在最准确的说法是：**Matrix-Game 3.5 已经开放了几何记忆基础模型、权重和离线轨迹推理；实时蒸馏版仍是论文结果与项目演示，等待后续发布。**

## 9. 它还不是一个游戏引擎，也没有学会碰撞

项目页有 collision avoidance 演示，但技术报告附录说明，模型控制信号本身并不进行碰撞推理。演示使用外部的渐进式 3D occupancy map：通过累计深度和相机位姿构建占用体素，再修改计划中的相机路径。

这是一种有用的组合系统，但不能解读为生成模型已经学会物理碰撞。

Matrix-Game 3.5 当前也不提供：

- 可编辑 mesh、材质和场景层级；
- navmesh、刚体、碰撞体或游戏逻辑；
- 可靠的对象 permanence 和动态实体状态；
- 任意玩家动作到环境状态变化的通用 action model；
- 可验证、可查询的 3D world state。

它输出的是受相机轨迹、文本和记忆条件控制的连续视频。把它称为 interactive world model 是合理的，但把它等同于 Unity、Unreal 或可直接发布的游戏系统，就跨过了当前证据。

## 10. 对创作者和开发者意味着什么

Matrix-Game 3.5 当前最适合三类探索：

1. **长镜头预演。** 用 anchor image 和 camera trajectory 测试第一/第三人称运镜、空间回访和场景连续性。
2. **世界模型研究。** 研究显式几何记忆如何与 diffusion transformer 融合，尤其是动态/静态分治和自回归蒸馏。
3. **混合式交互原型。** 用传统 3D 占用、路径规划和控制系统提供约束，用生成模型负责视觉展开。

它暂时不适合低显存个人设备、要求确定性物理的仿真、需要对象级编辑的游戏制作，或者把“20 FPS”直接当作当前下载版部署指标的产品规划。

## 结论：世界模型开始承认，记忆也需要坐标系

Matrix-Game 3.5 最有价值的思想并不复杂：一个长期存在的世界，不能只是一串越来越长的历史帧。静态环境需要知道旧内容在 3D 空间里属于哪里，动态主体需要独立身份记忆，新暴露区域则需要明确交还给生成器。

Warped PRoPE 把相机几何放进 attention；Patch Memory 把历史外观搬到当前视角；reference tokens 避免动态角色污染静态地图；Self-Rollout DMD 则尝试让这套系统在自己的生成历史上跑得足够快。

但 3.5 也提醒我们区分三个层次：论文方法、项目演示和当前可下载产品。方法已经公开，基础模型可以测试，实时蒸馏版还没有交付。等后者真正发布后，最值得验证的不是 teaser 能不能动，而是普通开发者能否在一分钟以上的连续交互中稳定复现相机遵循、场景回访、角色身份和 20 FPS。

在那之前，Matrix-Game 3.5 已经给出一个清晰方向：**世界模型的记忆，不只要记得发生过什么，还要知道它发生在哪里。**
