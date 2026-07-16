---
title: "NVIDIA ARDY 深度拆解：AI 角色动画正在从生成片段变成实时可重规划的运动控制层"
date: 2026-07-14
source: "https://x.com/Stefan_3D_AI/status/2077070556579696836"
canonical: "https://research.nvidia.com/labs/sil/projects/ardy/"
tags:
  - NVIDIA
  - ARDY
  - Human Motion Generation
  - 3D Animation
  - Humanoid Robotics
  - Diffusion
  - Physical AI
---

# NVIDIA ARDY 深度拆解：AI 角色动画正在从生成片段变成实时可重规划的运动控制层

> **TL;DR:** NVIDIA Spatial Intelligence Lab 的 ARDY 把文本生成动作从离线任务改造成了流式控制系统。角色正在走路时，用户仍可替换文本、点击新路径点、加入全身关键帧或手脚位置与旋转约束；模型会利用已经生成的历史运动重新规划后续动作。它能做到这一点，靠的是显式 root motion 与 latent body motion 组成的混合表示、先预测根节点再预测身体的两阶段 Transformer，以及用播放缓冲隐藏推理延迟的非阻塞重规划。论文在 RTX 4090 上报告，4 步扩散平均用 33ms 生成一个 2 秒、40 帧的窗口。但 ARDY 输出的是运动学骨骼序列，不是带碰撞、环境理解和物理稳定性的成品动画；机器人演示也需要 SONIC 物理跟踪策略执行。

- **Original post:** [Stefan 3D AI on X](https://x.com/Stefan_3D_AI/status/2077070556579696836)
- **Project:** [ARDY - NVIDIA Spatial Intelligence Lab](https://research.nvidia.com/labs/sil/projects/ardy/)
- **Paper:** [arXiv:2607.08741](https://arxiv.org/abs/2607.08741)
- **Code:** [nv-tlabs/ardy](https://github.com/nv-tlabs/ardy)
- **Models:** [NVIDIA ARDY collection on Hugging Face](https://huggingface.co/collections/nvidia/ardy)
- **Paper submitted:** 2026-07-09
- **Models released:** 2026-07-10
- **Post published:** 2026-07-14
- **Accessed:** 2026-07-16
- **Tags:** NVIDIA / ARDY / human motion generation / 3D animation / humanoid robotics / diffusion / Physical AI

## 一句话判断

**ARDY 的意义不是把 text-to-motion 再加速一点，而是让生成模型进入角色控制循环：动作不再一次生成完再修改，而是可以一边播放、一边接受新意图和空间约束、一边重规划。**

这改变了人与动画模型的交互单位。

过去，生成式动作工具更像渲染任务：输入 prompt 和约束，等待模型生成完整片段，再查看结果、修改条件、重新生成。ARDY 把这个循环缩短到角色仍在运动的过程中。用户可以随时改变动作语义，也可以给角色一个新去向、一条地面轨迹、未来某一帧的全身姿势，或只约束手脚的位置和朝向。

![ARDY source demo contact sheet showing text-to-motion, combined constraints, keyboard control, local UI, and Unreal Engine previews](imgs/nvidia-ardy-realtime-interactive-motion-control/x-demo-contact-sheet.jpg)

原帖把它形容成 “Kimodo × MotionBricks”。这个比喻抓住了产品轮廓：Kimodo 擅长文本与多种运动学约束下的高质量离线动作创作，MotionBricks 强调低延迟实时动作与运行时控制。ARDY 试图把前者的语义与约束能力，带进后者所在的交互式时间尺度。

但它不是两个系统的简单拼接。ARDY 的关键是重新设计运动表示和生成过程，使文本、历史动作与未来约束能够共同进入一个自回归扩散模型。

## “实时”到底是什么意思

原帖的 “No baking, no waiting” 很有传播力，但论文给出的定义更精确。

ARDY 的部署模型以 20 fps 工作，每次生成 40 帧，也就是未来 2 秒的运动。论文在 RTX 4090 上报告：

| 配置 | 单次生成窗口 | 平均延迟 | 用法 |
|---|---:|---:|---|
| 4-step diffusion | 40 帧 / 2 秒 | 33ms | 最低交互延迟，无需额外缓冲帧 |
| 10-step diffusion | 40 帧 / 2 秒 | 63ms | 控制精度略高，使用 1 帧重规划缓冲 |

所以 33ms 不是“每帧花 33ms”，而是模型平均用 33ms 生成一个 2 秒窗口。角色播放已生成动作时，后台继续准备下一个窗口。只要生成速度持续快于播放消耗速度，用户看到的就是连续运动。

当文本或约束突然变化，系统不会删除正在播放的一切并停住。它把接下来已经生成的少量帧作为 **replan buffer**：这些帧继续播放，同时也作为新一轮生成的历史上下文。新动作准备好后，再平滑接到缓冲末尾。

这套 latency-aware replanning 比单纯追求更高 FPS 更重要。交互系统真正需要的不是某次推理很快，而是输入变化时，角色不会停顿、跳帧或瞬移。

## 混合表示：路径要精确，身体要会表达

ARDY 面对的是一个结构性矛盾。

完整显式表示每个关节的位置和旋转，控制直观，却维度高、生成困难；把整个人体都压进 latent，学习效率更高，但角色根节点在世界坐标中的路径容易失真。对游戏和机器人来说，身体动作很自然却走不到目标点，仍然不可用。

ARDY 将运动拆成两部分：

- **显式 global root features**：负责角色在世界中的平移、朝向和地面轨迹；
- **latent body embedding**：通过运动 tokenizer 压缩身体关节运动，负责姿态、风格和动作细节。

tokenizer 默认把 4 帧压成一个 patch，编码器和解码器都是 8 层 causal Transformer。论文最终采用 FSQ 量化 latent，原因不是它在每项指标都绝对最好，而是训练稳定性优于容易发散的普通 autoencoder。

这种拆分很像动画生产中的两层控制：root motion 决定角色真正走到哪里，body motion 决定它如何走、如何挥手、如何弯腰。ARDY 不是让一个统一 latent 同时承担两个冲突目标，而是保留 root 的可解释性，再压缩身体的高维变化。

## 两阶段去噪：先决定去哪里，再决定怎么动

混合表示之后，ARDY 的去噪器也分成两阶段。

![ARDY official two-stage transformer denoiser architecture](imgs/nvidia-ardy-realtime-interactive-motion-control/ardy-two-stage-denoiser.png)

每个扩散步骤中：

1. `Root Transformer` 先根据文本、历史运动和空间约束预测干净的 global root motion；
2. `Body Transformer` 再以这个干净 root 为条件，预测 latent body tokens；
3. 两者合并成完整的 hybrid motion prediction，再进入下一次去噪。

这不是纯工程上的并行拆分，而是一种因果优先级：先决定角色的全球位置和方向，再让身体动作适配这条轨迹。

论文的消融实验支持这一设计。在多种约束任务中，一阶段模型的 waypoint error 为 0.164m，ARDY 两阶段模型为 0.024m；一阶段的 joint-position error 为 0.101m，ARDY 为 0.025m。纯显式表示在文本对齐、FID 和约束误差上也整体更差。

## 文本、路径和关键帧为什么能放在同一系统里

ARDY 把空间约束表示成一条带 mask 的运动序列。某个时间点、某个关节有目标，就把对应位置或旋转标记为已知；没有约束的部分保持 mask。这样，同一个接口可以表达：

- root waypoint 或连续地面路径；
- 全身关键帧；
- 手、脚等 end effector 的位置；
- 关节旋转与朝向；
- 上述约束的任意组合。

约束不必落在当前 2 秒生成窗口内。模型在训练时使用可变长度历史，并接收超出当前窗口的 future constraint tokens，因此可以提前朝较远目标调整动作。论文中的最大已训练历史与未来上下文为 8 秒，方法对比表则以 8 秒 history、10 秒 future 描述可支持范围。

这里要避免一个误读：ARDY 并不会一次“看见一分钟后的所有细节”。交互 demo 会截断输入上下文；例如一分钟后的目标先被排除，等播放进度把它带入未来上下文窗口后，系统才开始把它加入条件。它解决的是滚动式长程目标，不是无限上下文规划。

## Benchmark 说明了什么

在 HumanML3D 的自回归文本加约束对比中，ARDY 与 DiP 使用相同的 0.15 秒测量延迟，但控制误差差距明显。这组延迟在单张 A100 上测量，使用论文的 benchmark 配置，不能与前面 RTX 4090 交互 demo 的 4-step 33ms 直接横向比较。

| 场景 | 方法 | R-Precision ↑ | FID ↓ | 关节误差 ↓ |
|---|---|---:|---:|---:|
| 窗口内目标 | DiP | 0.609 | 0.967 | 9.20cm |
| 窗口内目标 | ARDY | 0.690 | 0.092 | 2.48cm |
| 窗口外目标 | DiP | 0.599 | 1.453 | 17.64cm |
| 窗口外目标 | ARDY | 0.684 | 0.100 | 2.92cm |

对 ARDY 最有意义的是窗口外结果。DiP 的目标被放到初始生成窗口之外后，误差从 9.20cm 升到 17.64cm；ARDY 仍维持在 2.92cm。它支持的并不只是“当前两秒内跟着点走”，而是从历史和较远约束共同推断怎样逐步接近目标。

论文还做了 240 组并排感知比较。对窗口外目标，参与者在 motion quality、semantic alignment 和 goal accuracy 三项上分别有 65.8%、67.5% 和 64.6% 选择 ARDY，选择 DiP 的比例为 9.2%、7.5% 和 4.2%，其余为平局。

这些都是论文作者在自己的实现与评估协议下报告的结果，不是独立第三方复现。HumanML3D 的预处理也经过调整，以保留实时动画需要的原生关节旋转；跨论文比较时，不能把表格数字脱离 retarget 和 evaluator 细节使用。

## 代码和模型到底开放到了什么程度

这次发布比只有论文和视频完整得多：

- GitHub 提供推理代码、交互 demo、命令行生成、可视化和 motion correction 扩展；
- Hugging Face 提供 4 个公开、非 gated checkpoint；
- Core 版本使用 27 关节骨架、20 fps，提供 8 帧和 40 帧 horizon；
- Unitree G1 版本使用 34 关节骨架、25 fps，提供 8 帧和 52 帧 horizon；
- 命令行输出 `.npz`，G1 还可输出 MuJoCo qpos `.csv`；
- 交互 demo 在本地 `http://localhost:2333` 运行。

安装仍不是“一键网页应用”。官方主要测试环境是 Ubuntu 22.04、Python 3.11、RTX 4090 和 NVIDIA driver 575。核心依赖 PyTorch 2.4+；TensorRT 是可选加速层，首次编译 engine 可能要等待几分钟。

文本编码器基于 LLM2Vec 与 gated 的 `Meta-Llama-3-8B-Instruct`，因此需要先获得 Hugging Face 访问权限并提供 token。默认 GPU bfloat16 文本编码器约占 14GB VRAM，也可以放到 CPU，以降低显存占用但牺牲 prompt 编码速度。

原帖提到 20–24GB VRAM，这是作者 Stefan 的实测描述，不是论文给出的统一显存 benchmark。官方能确认的是 RTX 4090 测试配置和文本编码器的约 14GB 占用；不同 checkpoint、TensorRT engine、精度和 CPU offload 会改变总显存。

“open source” 也要拆开看：代码是 Apache-2.0；模型 checkpoint 使用 NVIDIA Open Model Agreement；可选 Bones 数据集有自己的许可；Llama 3 文本编码器还受 Meta 的访问与许可条件约束。可以本地运行和商用，并不等于所有组成部分都使用同一份开源许可证。

## 从 demo 到动画生产，还差哪些层

ARDY 当前输出的是 pose sequence，包括 global root translation、关节旋转、关节位置和 foot contacts。它不是直接产出一个带蒙皮角色、镜头、布料、表情、碰撞和环境交互的 Unreal 或 Blender 场景。

真正接入生产还需要：

```text
文本 / 路径 / 关键帧
        ↓
ARDY 骨骼运动生成
        ↓
骨架映射与 retarget
        ↓
脚底修正、IK、碰撞与场景约束
        ↓
游戏引擎 / DCC / 仿真器中的最终角色
```

仓库自带 post-processing，可以降低脚滑并改善约束命中，但会变慢，而且默认关闭。模型卡还明确写出：模型可能脚滑、抖动、偏离文本；它更擅长行走、手势、战斗、舞蹈和日常动作，不理解角色周围的物体，也不生成卡通或违反物理的人体动作。每个 checkpoint 目前只输出一种骨架，Rigplay 训练的 SOMA 版本仍标记为 coming soon。

所以 ARDY 最接近的是 **motion planner / authoring controller**，不是完整动画 Agent。

## 机器人演示为什么不能说成“同一模型直接驱动机器人”

项目页展示了 Unitree G1 跟随在线文本与约束运动，但链路里还有关键一层：SONIC。

ARDY 生成目标运动，SONIC 作为 physics-based tracking policy，把运动学目标转成机器人可以执行的全身控制。真实机器人还要处理动力学、接触、平衡、关节限制和 sim-to-real 偏差。

更准确的架构是：

```text
用户文本 / waypoint / keyframe
              ↓
ARDY：实时运动规划
              ↓
SONIC：物理跟踪与控制
              ↓
Unitree G1：执行
```

这种分层反而比“一个模型包办一切”更有工程价值。动画和机器人可以共享上层动作语义与运动计划，底层则分别接游戏引擎的 retarget/IK 或机器人的物理控制器。

## 谁值得现在就试

ARDY 适合三类团队优先测试：

1. **游戏与虚拟人团队**：验证 NPC 能否在运行时接受文本意图，同时服从导航路径和关键姿势；
2. **动画工具团队**：把生成从“按钮出片”改成可在时间轴持续 steer 的动作草拟层；
3. **机器人与仿真团队**：把文本和稀疏空间目标转成动作计划，再交给物理策略执行。

评估时不要只播放官方 demo。更有价值的测试包括：

- 角色走到一半连续切换三次 prompt，动作是否自然过渡；
- 路径突然折返或 waypoint 移动时，root 是否稳定且没有脚滑；
- 同时给文字、手部目标和未来全身 keyframe，约束是否互相冲突；
- 长时间自回归后是否积累漂移、抖动或姿势退化；
- 导出到目标骨架后，retarget 和接触修正增加多少延迟；
- CPU text encoder 与 GPU text encoder 的实际交互延迟和显存差异；
- 在没有 TensorRT 的机器上，`torch.compile` 或纯 PyTorch 是否仍满足运行时预算。

## 结论

ARDY 把生成式动画推进到了一个更像控制系统的位置。

它保留文本的高层语义，同时把路径、关键帧和关节目标当成硬空间条件；它不等待完整片段生成，而是滚动预测未来窗口，并在用户输入改变时利用已有运动做连续重规划。显式 root 与 latent body 的混合表示、root-first 的两阶段去噪、以及 latency-aware replan buffer，构成了这套系统真正的技术核心。

它还不是动画制作的终点。物理、碰撞、对象交互、骨架适配、表情与最终镜头仍在模型之外，机器人执行也依赖 SONIC 这样的物理控制层。

但 ARDY 已经给出一个清楚的方向：**AI 动画的下一步不是更快地吐出一段动作，而是让动作生成成为一个可以持续接收意图、约束和环境反馈的实时运行时。**
