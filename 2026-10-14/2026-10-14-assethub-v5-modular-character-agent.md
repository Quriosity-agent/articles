---
title: "AssetHub V5 拆解：AI 不是替代 Blender，而是把角色生成变成可编辑的部件装配线"
date: 2026-10-14
source: "https://x.com/Stefan_3D_AI/status/2110376391686619155"
canonical: "https://www.youtube.com/watch?v=CFA8Pfw6OIs"
tags:
  - AssetHub
  - Part Composer
  - Modular Character
  - 3D AI
  - Blender
  - Codex
  - MCP
  - Game Development
  - Agent Workflow
---

# AssetHub V5 拆解：AI 不是替代 Blender，而是把角色生成变成可编辑的部件装配线

> **TL;DR：** AssetHub V5 Agent 最重要的进步不是从一张图生成一个完整 3D 角色，而是把角色拆成身体、上装、下装、头发和装备等独立网格，再为各部件选择生成模型、控制面数并自动组装。这样得到的不是难以修改的一整块 AI mesh，而是一套可以替换、重生成和继续加工的模块化资产。54 秒短片强调“没有打开 Blender”，但 15 分钟完整测试明确展示了复杂角色仍有膨胀、尺度、贴合与隐藏几何问题，作者最终也进入 Blender 检查并手调。因此，更准确的判断是：它已经能自动完成相当有价值的部件化 first pass，却还没有消灭 DCC、拓扑验收、绑定、动画和引擎内 QA。

![AssetHub V5 modular character workflow contact sheet](imgs/assethub-v5-modular-character-agent/assethub-v5-workflow-contact-sheet.jpg)

- **来源帖：** [Stefan 3D AI on X](https://x.com/Stefan_3D_AI/status/2110376391686619155)
- **完整测试：** [You Can Now Create Modular 3D Character Without Blender](https://www.youtube.com/watch?v=CFA8Pfw6OIs)
- **产品入口：** [AssetHub](https://app.assethub.io/)
- **官方生产服务：** [AssetHub Studio](https://assethub.io/studio)
- **官方 CLI / SDK：** [AssetHub-inc/assethub-cli](https://github.com/AssetHub-inc/assethub-cli)
- **发布时间：** 2026-10-14
- **查阅时间：** 2026-10-15

## 一句话判断

**AssetHub V5 不是让 AI 学会“做完一个角色”，而是让 Agent 第一次可以编排一条从概念图到模块化角色首稿的生产链。**

这一区别很重要。单体 image-to-3D 模型已经能做出看起来不错的角色，但如果头发、衣服、身体和武器都焊在同一个网格里，艺术指导只想换一件上衣，也可能被迫重新生成整个角色。

AssetHub 的思路是把“生成一个物体”改写成“规划一组零件，然后组装”：

```text
一张角色概念图
        ↓
识别身体、服装、头发、装备等逻辑部件
        ↓
为部件生成参考图与多视图
        ↓
按部件选择 3D 模型、质量与面数约束
        ↓
生成多个独立 mesh
        ↓
自动调整位置、比例与贴合关系
        ↓
输出组合角色 + 独立部件 + 过程报告
```

真正的新意不在最后那张漂亮预览，而在中间保留下来的结构。

## 54 秒短片实际展示了什么

来源视频使用一名兔子角色做演示。画面中可以看到：

1. 输入完整角色概念图；
2. Agent 生成 production plan，决定拆分方式和生成步骤；
3. 身体、上衣、裤子等部件沿工作流分别生成；
4. Part Composer 把网格重新装配到同一角色上；
5. 右侧资产栏仍保留每个独立 mesh；
6. 最终角色可以切换实体与 wireframe 检查。

九张抽帧里最值得注意的不是开头和结尾，而是中间的节点图。它证明结果不是把一张完整人物图直接交给某个单模型，而是经过拆分、生成与组合多个阶段。右侧同时存在多件裤子、上衣和 body，也说明失败或较差的候选可以单独重做，不必推翻全身。

## “Agent 自动选择面数”需要更精确地理解

X 帖写道 Agent 会选择 polycount。完整视频给出的信息更细：创作者在 CLI 提示中明确设置了模型，并要求每个部件不超过约 5,000 面。也就是说，这里同时存在两层决策：

- **人给边界：** 目标模型、质量档、最大面数、部件数量或希望分开的服装；
- **Agent 做规划：** 如何拆部件、哪些部件进入哪条生成路径、如何组装与重试。

这比“AI 自己决定一切”更像真正的生产系统。项目负责人设定预算和交付约束，Agent 在边界里做路由。对于移动游戏，5,000 面的单件上限也不等于整体角色已经优化，因为多个部件叠加、隐藏身体几何、材质数量和骨骼影响仍会决定最终成本。

## 它比普通 image-to-3D 强在哪儿

| 普通整模生成 | AssetHub 部件化 Agent |
|---|---|
| 一张图变成一个整体 mesh | 先规划身体、服装与装备的逻辑部件 |
| 某个局部不对，常要整模重抽 | 只重生成或替换失败部件 |
| 服装与身体可能融在一起 | 各部件保持独立 mesh |
| 难以形成可复用资产库 | 审核通过的部件可以跨角色积累 |
| 生成结束就是流程终点 | 生成后继续组合、精修、绑定与引擎验证 |
| 模型选择通常固定 | Agent 或用户可以按部件与质量要求路由模型 |

这也是为什么“模块化”比“更漂亮”更有生产意义。游戏角色不是一张最终渲染图，而是会换装、受动画驱动、进入 LOD 和性能预算，并在数十次反馈中修改的资产。

## Part Composer 是一个 Agent 工作流，不是单一 3D 模型

公开材料显示，AssetHub 同时提供画布、CLI、托管 MCP 和 TypeScript SDK。完整视频中的创作者把 API key 配给 Agent，通过短提示调用整条工作流；官方 CLI 则把这些阶段暴露成结构化命令和运行记录。

当前公开 CLI 已经能表达：

- `parts split`：从概念图提取部件；
- `production analyze`：运行角色生产分析与装配流程；
- `production run --image`：把拆分、逐件 mesh 生成和 compose 包进一次任务；
- `composer run`：组合已有部件；
- `composer refine`：基于上一次组合继续修正；
- `runs get / watch / resume`：读取、等待或恢复长任务；
- MCP：让 Codex、Claude Code 或 Cursor 从 Agent 会话中调用同一能力。

所以这里的“V5 Agent”不是一个端到端神经网络吞掉概念图、直接吐出角色。它更像一个 control plane：根据目标和约束调用多个图像、3D、重拓扑与组装能力，再保存 lineage、运行状态和候选资产。

## 完整视频推翻了“Blender 已经不需要”的字面理解

15 分钟完整测试比短帖标题诚实得多。

### 简单角色：自动首稿已经有价值

第一名兔子角色大约拆成身体、上装和下装。第一次组合还有明显瑕疵，第二次尝试更好。创作者的判断是，这已经能节省时间，只需把 GLB 放进 Blender 做少量修正。

这说明流程的价值是真实的，但也说明它仍有随机性。若第二次明显优于第一次，生产环境就必须保留候选比较、成本上限和回退策略。

### 复杂角色：贴合和比例仍是难点

后续角色出现局部膨胀、尺度不一致和部件贴合问题。创作者认为这是他看到过最好的 AI-only 结果之一，但仍需要进入 Blender 检查，调整比例和形状。

这类问题并不奇怪。每个部件都是独立生成的，生成模型并不知道相邻网格的真实接触面、服装厚度和身体遮挡。组装 Agent 可以估计 placement 与 fit，却仍可能把衣服放在“视觉上接近”而不是“拓扑上可靠”的位置。

### 移动游戏：隐藏几何仍要清理

视频还指出，如果上衣永久遮住胸部，身体内部那部分几何最好删除。否则角色虽然每个部件都满足面数要求，整体仍会携带不可见三角形、额外 overdraw 和潜在穿插。

因此，“独立 mesh”是模块化的必要条件，但不是优化完成的证明。

## Wireframe 很有说服力，但不能证明 game-ready

![AssetHub V5 assembled character wireframe](imgs/assethub-v5-modular-character-agent/assethub-v5-modular-character-wireframe.jpg)

短片最后展示了组合角色的 wireframe，并在界面中列出顶点、三角形和面数。这是很好的可检查性设计：用户不只看到材质渲染，还能快速判断密度是否失控。

但一张 wireframe 截图仍不能证明以下事项：

- 关节附近是否有适合变形的 edge loops；
- 衣服与身体在大幅动作时是否穿插；
- UV 是否连续、密度是否一致；
- 多部件之间的材质、法线和切线是否统一；
- 骨骼层级、skin weights、碰撞体和 root motion 是否正确；
- LOD、draw calls、贴图尺寸和移动端性能是否达标；
- 导入 Unity 或 Unreal 后，动画与光照下是否仍然成立。

官方 CLI 文档也明确提醒，组合 GLB 是 triangulated preview，不是 Quad topology 的证明；`completed` 或 `reviewed` 表示执行结束，也不等于创作者已经批准。未解决问题可以以 `needs_review` 返回。

## V5、V5.1、V6 为什么同时出现

来源视频把被测能力称为 V5。查阅时的公开 CLI 已经同时出现了几套名称：

| 名称 | 当前公开文档中的含义 |
|---|---|
| V4 / V5 Character Assembly | 从图片规划部件、生成 mesh 并运行装配的受限生产 Agent |
| V5.1 Skill assembly | 在 Blender sandbox 中运行 Character Assembly Skill 的装配路径 |
| V6 Auto assemble | 需要 mesh 与对应部件参考图的自动组合路径 |

这些能力还受账号和 server rollout 控制，CLI 支持某个别名不代表每个工作区都能调用。公开仓库更新也很快，因此不能把社交视频里的 V5、产品画布显示的版本和最新 CLI 模型名简单视为同一个固定模型。

更稳妥的做法是先读取当前 workspace 的 capabilities、production agents 与 composer models，再决定工作流，而不是照抄一个会过期的模型 ID。

## 成本不是“一次生成”的价格

官方定价页把单次 image-to-3D 列为 25 到 140 credits，但模块化角色会对多个部件分别生成，再加上拆分、参考图、重拓扑、组合和可能的重试。因此总成本大致会随部件数和候选数增长，而不是只算一次 3D generation。

当前 CLI 的 `production run --estimate` 可以在提交前读取模型与 compose 报价，并用 `--max-cost` 设上限。不过官方文档也说明，part extraction 尚没有完整的 dry-run 价格来源，估算会把这一项标成 unknown，而不是编造数字。

这是一种比“全自动”更重要的 Agent 产品设计：付费动作必须可估算、可限额、可恢复，同一个 operation ID 重试时不能静默再开一单。

## 对 3D 生产的真正意义

AssetHub V5 目前最适合替代的不是 Blender，而是 Blender 之前和之中的一批重复劳动：

1. 从概念图人工列出部件清单；
2. 为每个部件制作参考图和多视图；
3. 在多个 image-to-3D 模型之间重复提交；
4. 下载、命名和追踪每个 mesh；
5. 把部件粗略缩放、定位到同一角色；
6. 发现某个部件失败后，只回退那一支；
7. 整理报告，告诉艺术家哪些问题仍需手工完成。

这会把 DCC 的角色从“每一步都由人执行”，变成“Agent 做 first pass，人负责审美、结构和验收”。AssetHub 自己的 Studio 页面也采用相同表述：AI first pass + artist finish，而不是 AI-only final asset。

## 采用前应该怎样验收

真正评估这类 Agent，不能只看正面站姿。至少应固定同一概念图，重复运行多个 seed，并检查：

- 部件拆分是否稳定，是否漏掉首饰、鞋、头发内层或武器；
- 每个 mesh 是否保持合理尺度、原点、朝向与命名；
- 贴合区域是否穿插，动作姿势下是否更严重；
- 单件和整角的三角面、材质、贴图与 draw-call 预算；
- 替换一件衣服时，其他已通过部件是否真的保持不变；
- 自动重试会增加多少 credits，失败能否从原 run 恢复；
- GLB/FBX 进入 Blender、Maya、Unity 或 Unreal 后是否保持结构；
- 自动绑定、动画、LOD 和移动端 profiler 是否通过项目标准。

本文没有使用付费 credits 独立运行 AssetHub V5，因此不把创作者展示的三个样本当作广泛成功率。可以确认的是：短片中的多阶段节点、独立部件、组合结果和 wireframe 都是真实可见的；完整视频也主动展示了重试、瑕疵、Blender 检查与人工修复边界。

## 结论

AssetHub V5 的方向比“一键生成更漂亮的 3D”更接近生产需要。

它把角色从不可分割的一次性结果，改造成一组有 lineage、可替换、可单独重试的部件。再通过 CLI、MCP 和 Agent，把拆分、模型路由、面数约束、生成、组装与报告串成一条长任务。对于换装角色、批量 NPC 和需要持续反馈的游戏项目，这个结构比单次模型分数更重要。

但短帖里的“without Blender”只能成立在首轮拆分和粗组装阶段。完整测试和官方材料都指向同一个现实：**AI 已经可以少开很多次 Blender，却还不能让团队永远不打开 Blender。**

真正的进步是，人不再从零手工装每一个部件，而是从一个可编辑的 Agent 首稿开始工作。

## 参考资料

- [Stefan 3D AI source post - X](https://x.com/Stefan_3D_AI/status/2110376391686619155)
- [You Can Now Create Modular 3D Character Without Blender - YouTube](https://www.youtube.com/watch?v=CFA8Pfw6OIs)
- [AssetHub app](https://app.assethub.io/)
- [AssetHub AI-native 3D production](https://assethub.io/studio)
- [AssetHub official CLI and TypeScript SDK](https://github.com/AssetHub-inc/assethub-cli)
- [CLI snapshot inspected for this article](https://github.com/AssetHub-inc/assethub-cli/tree/25666419b0204bff5e147fddffa25d932c91fa9e)
- [AssetHub pricing](https://assethub.io/pricing)
- [Theron production workflow](https://assethub.io/theron-workflows-2)

*本文查阅时间为 2026-10-15。CLI 审计快照为 `25666419b0204bff5e147fddffa25d932c91fa9e`，当时 CLI package 版本为 0.1.52。模型名称、工作区资格、价格和 server rollout 会继续变化。图片由来源帖 54 秒视频本地抽帧生成；完整视频的产品结论来自其公开字幕与画面。*
