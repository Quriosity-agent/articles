---
title: "reelbench-skills 源码拆解：AI 拉片真正需要的不是会看视频，而是把测量、判断与验收分开"
date: 2026-09-14
source: "https://mp.weixin.qq.com/s/E6SE4iIiDSPZEPE0zJ8PGQ"
canonical: "https://github.com/eternityspring/reelbench-skills"
inspected_commit: "18f2f63987337df0975a89973d38d50f3231ee31"
tags:
  - reelbench-skills
  - video-shots
  - video-sync
  - AI Video
  - Shot Analysis
  - Codex Skills
  - FFmpeg
  - Video QA
---

# reelbench-skills 源码拆解：AI 拉片真正需要的不是会看视频，而是把测量、判断与验收分开

> **TL;DR:** reelbench-skills 不是视频生成模型，也不是一个“把视频扔给大模型，等它自由发挥”的拉片提示词。它由 `video-shots` 和 `video-sync` 两个可安装到 Claude Code 或 Codex 的 Skill 组成：前者用 ffprobe、FFmpeg 和逐帧差分测出镜头边界、时长与运动证据，让模型只填写景别、类别、运镜、画面和节奏等语义字段，再用 15 道确定性质量门验收；后者把原片和镜头表合成为会随切点滚动、高亮的讲解视频。真正值得借鉴的不是“一行命令”，而是它把事实、判断和验收分成了三层。

- **微信来源:** [开源星探：《这个刚开源的拉片 skill 让 AI 视频拉片变成一行命令！》](https://mp.weixin.qq.com/s/E6SE4iIiDSPZEPE0zJ8PGQ)
- **项目:** [eternityspring/reelbench-skills](https://github.com/eternityspring/reelbench-skills)
- **首次提交:** 2026-09-11
- **检查时间:** 2026-09-14
- **检查版本:** [18f2f63](https://github.com/eternityspring/reelbench-skills/commit/18f2f63987337df0975a89973d38d50f3231ee31)
- **状态快照:** Apache-2.0；16 次提交；无 tag、无 GitHub Release

![video-shots 生成的桌面交互式拉片报告](imgs/reelbench-skills-measured-shot-analysis/01-video-shots-report.png)

## 一句话判断

reelbench-skills 最准确的定位是：**一套把视频测量、模型标注、规则验收和可视化交付串起来的 Agent 拉片工具链。**

它和此前介绍过的 [Lapian Notes 本地拉片工作台](../2026-07-09/2026-07-09-lapian-notes-ai-film-analysis-workbench.md) 有重叠，但重点不同。Lapian Notes 更像供人观看、记录与研究镜头的本地交互界面；reelbench-skills 更强调可执行流水线：哪些字段来自机器、哪些字段允许模型判断、什么错误必须由代码拦住，以及分析数据如何继续生成讲解视频。

项目目前包含两个 Skill：

| Skill | 输入 | 主要产物 | 解决的问题 |
|---|---|---|---|
| `video-shots` | 原始视频 | `shots.json`、`track.json`、关键帧、Markdown、交互式 HTML | 把成片拆成可检查、可复用的逐镜头数据 |
| `video-sync` | 原片、`shots.json`、关键帧 | 带镜头信息面板的同步 MP4 | 把分析结果变成适合教学、复盘和传播的成片 |

所以它不是类似 Remotion 的程序化视频引擎。Remotion 负责“代码怎样渲染成视频”；reelbench-skills 负责“怎样从一条现成视频得到有证据、可验收的镜头分析”，最后仍然由 FFmpeg 完成媒体处理与合成。

## 最重要的设计：机器量，模型判，代码查

README 用一句很短的话概括了项目的工程边界：切点与时长由 FFmpeg 测量，模型只判断该判断的内容，质量门再逐项对账。

拆开以后是三类完全不同的数据责任：

| 层 | 负责什么 | 典型字段 | 为什么这样分 |
|---|---|---|---|
| 机器测量 | 可从媒体直接计算的事实 | 视频时长、尺寸、帧率、cut 时间、每镜 start/end/seconds、运动曲线 | 防止模型编造时间轴和数值 |
| 模型标注 | 需要视觉语义判断的内容 | 景别、镜头类别、运镜、画面描述、人物、字幕、声音、节奏功能 | 让模型专注于其真正擅长的识别与归纳 |
| 代码验收 | 检查数据是否自洽、是否有证据 | 枚举合法性、时间连续、关键帧存在、人物表对应、运动描述一致 | 让“看起来完成”变成可执行的通过或失败 |

这一分层比“换一个更强的视觉模型”更重要。视频拉片最危险的错误通常不是语言写得不漂亮，而是切点错位、时长对不上、镜号缺失、固定镜头被写成大幅运镜，或者一整列字段看似完整却没有证据。模型可以生成流畅文本，但不应该成为这些机器事实的唯一来源。

## `video-shots` 实际怎样跑

`video-shots` 不是一次模型调用，而是一条有中间产物的流水线：

1. `seed` 用 ffprobe 读取媒体元数据，再用 FFmpeg scene detection 生成候选切点，同时计算逐帧运动曲线。
2. `frames` 在每个镜头约 15% 和 85% 的位置各抽一张图，形成 `S01a`、`S01b` 这样的首尾证据。
3. `sheet` 把关键帧排成 contact sheet，让模型能同时比较一个镜头开头和结尾的变化。
4. Agent 分批填写语义字段；Skill 建议每批不超过 25 镜，避免上下文过长造成漏项和串镜。
5. 如果场景检测漏切或误切，`recut --split` / `--merge` 只修改边界、重新编号并重算时长，同时把人工切点记入 `manualCuts`。
6. `validate` 执行 15 道质量门；有硬错误时返回非零退出码。
7. `render` 输出 Markdown 镜头表和单文件交互式 HTML 报告。

默认 scene threshold 是 0.3，但它不是通用真理。暗场、慢切影片可能要降到约 0.15；快速剪辑可以提高。叠化可能漏切，闪光、手持抖动和大幅主体运动也可能制造误切。因此项目把自动 cut 当作初始证据，而不是不可修改的答案。

## 运动曲线是证据，不是运镜识别器

项目默认以约 5 Hz 抽样，把帧缩到 64×36，再计算相邻帧平均像素差，并用镜头区间内部的中位数降低切点尖峰影响。这个方法便宜、稳定，适合回答“画面有没有明显变化”。

但它不能区分：

- 摄影机在推、拉、摇、移；
- 人物或物体在运动；
- 灯光、特效或曝光发生变化；
- 整个画面因为手持而抖动。

因此质量门采取了不对称策略：如果模型写了“大幅推镜或跟拍”，机器曲线却几乎为零，可以直接拦截；反过来，如果模型写“固定机位”而画面变化很大，只给 warning，因为变化可能来自主体，而不是摄影机。

这是一处很成熟的设计。系统没有把一个便宜的像素差指标包装成“AI 运镜检测”，而是明确规定它能够证明什么、不能证明什么。

## 15 道质量门到底检查什么

质量门覆盖的不只是 JSON 格式，而是镜头表能否被相信：

| 类别 | 检查内容 |
|---|---|
| 时间轴 | 镜头按序、首尾相接、从 0 到片尾；`seconds = end - start` |
| 标识与枚举 | 镜号连续；景别、类别、运镜和转场只能使用规定值 |
| 描述质量 | 画面描述必须可核对，不能用模板句批量复制 |
| 语义一致性 | 镜头人物应能在 cast 中对应；镜头类别需要描述证据 |
| 机器证据 | 运镜结论与运动曲线相容；边界来自检测结果或已登记的人工切点 |
| 资产完整性 | 每镜首尾关键帧真实存在 |
| 节奏标注 | rhythm 要么整列不做，要做就覆盖全部镜头并使用合法标签 |

还有一个容易忽略的细节：**skipped 不等于 passed。** 如果验证时没有传 `track.json`、cast 或关键帧目录，对应质量门只能标记为跳过，不能被统计成绿色通过。这避免了“因为没有证据，所以没有发现错误”的假成功。

本次检查直接运行了当前版本的自测：`video-shots` 为 **449 项断言全部通过**，而且 15 道门每一道都有专门的击穿用例。微信原文提到的是 436 项，这是项目继续迭代后的正常数字漂移，不应继续当作当前值引用。

## 报告不是截图，而是可操作的分析界面

`shots-report.html` 是无外部依赖的单文件页面，可以离线打开。它包含本地播放器、镜头节奏带、当前镜头同步高亮、点击跳转、搜索、筛选、排序、列表/卡片视图、首尾关键帧、景别与运镜分布、人物统计、质量门和 JSON 导出。

视频本身不会被打包进 HTML。报告记录原视频路径；换机器后，用户需要重新选择本地视频。这让报告保持轻量，但也意味着它不是一份真正自包含的媒体归档。

![video-shots 报告的移动端布局](imgs/reelbench-skills-measured-shot-analysis/02-report-mobile.png)

官方中文 demo 用一条 202.9 秒的 AI 短片得到 53 镜：平均镜长 3.83 秒，每分钟 15.7 切。15 道门全部通过，同时保留两条非阻塞提示作为范例：S46 被标成固定机位但实测运动偏高；片尾 S48-S53 连续六镜都使用 `close` 节奏标签。

我们用当前脚本重新验证了这份 demo，结果与仓库说明一致。英文 demo 也通过全部 15 道门：287.37 秒、46 镜、平均镜长 6.25 秒、每分钟 9.6 切。这里的长镜头没有被强行切碎，说明 scene detection 的结果可以保留真实不切镜，而不是为了“镜头数量好看”而制造边界。

## `video-sync` 怎样把镜头表变成视频

`video-sync` 接收原片、`shots.json` 和可选关键帧，然后生成一条原画面与镜头信息同步播放的 MP4。

![video-sync 的镜头信息面板](imgs/reelbench-skills-measured-shot-analysis/03-video-sync-panel.png)

它的实现没有为每一帧启动浏览器截图。脚本先用一个无头 Chrome/Chromium 渲染三张长面板：静态信息区、暗色镜头列表和高亮镜头列表。随后 FFmpeg 根据每个 cut 的时间，用 `sendcmd`、crop 和 overlay 控制列表滚动及高亮位置。

当前镜头默认被锚定在列表第二行附近；滚动在约 0.45 秒内缓动到位，然后停住，直到下一个切点。横版原片采用上下排列，竖版原片采用左右排列。原音轨通过 `-c:a copy` 直接复制，不做二次音频编码。

![竖版原片与同步镜头面板的合成结果](imgs/reelbench-skills-measured-shot-analysis/04-video-sync-output.png)

这套“少量浏览器截图 + FFmpeg 动态裁切”的方案比逐帧网页渲染更轻，也让视觉样式集中在 HTML/CSS 中。当前 `video-sync` 自测的 **122 项断言全部通过**，覆盖横版、方形、竖版布局、偶数尺寸、缩放范围、滚动锚点和命令生成；自测本身不启动浏览器或 FFmpeg。

## “一行命令”说法哪里需要降温

微信标题把产品体验概括为“一行命令”，这适合作为传播表达，但并不等于内部只有一个步骤。

用户确实可以在 Agent 会话里说“帮我拉片这条视频”，让 Skill 编排脚本与模型；仓库也提供安装脚本，把两个 Skill 软链接到 `~/.claude/skills/` 或 `~/.codex/skills/`。但完整工作仍包括探测、切点检测、抽帧、模型分批标注、必要时人工修切、验证、报告渲染，以及可选的同步视频合成。

运行依赖也需要说清楚：项目是**零 npm 依赖、零单独 API key**，不是“零依赖”。基础要求是 Node.js 18+、FFmpeg 和 ffprobe；`video-sync` 生成面板还需要 Chrome、Chromium 或 Edge。模型推理使用当前 Claude Code 或 Codex 会话额度，因此成本没有消失，只是没有额外配置 API key。

## 它明确不做什么

`video-shots` 的 Skill 文档把边界写得很具体：

- 不做 ASR；对白只能从画面烧录字幕读取，否则 audio 留空；
- 不做人脸识别，也不会自动把同一演员跨镜头合并成角色；
- 不评价影片“好不好”，只整理可核对的镜头事实和语义标签；
- 不剪辑或导出单独镜头片段；
- 不做镜头内部的物体检测与持续追踪。

还要补上三层现实限制。

第一，语义字段仍由模型或人填写。质量门可以发现不自洽，却不能保证“中景”“反应镜头”或“payoff”一定判断正确。第二，官方 demo 是作者随仓库提供的验证夹具，不是独立第三方 benchmark。第三，项目截至检查时只有几天历史，没有 tag 或 release，接口和断言数量仍可能快速变化。

## 对 AI 视频工作流真正有用的地方

它最适合做的不是给一条片子打一个神秘总分，而是建立可比较的数据层：

- 对同一提示词的多个生成版本，比较平均镜长、切速和景别分布；
- 检查某版是否出现连续过多近景、长时间无变化或节奏标签塌缩；
- 给剪辑教学、导演复盘和提示词研究生成同步讲解视频；
- 把镜头表作为后续 Agent 的结构化上下文，而不是反复让模型重新看整条视频；
- 在批量生成工作流里，把“测量结果”和“审美判断”分开保存，便于回溯。

对于 QCut 这类编辑器，最值得借鉴的是数据契约，而不只是界面：原始检测、人工修正、模型语义和验证状态应当分字段保存。这样用户才能知道一个结论来自像素证据、人工决定，还是模型推断。

## 结论

reelbench-skills 的价值不在于让 AI “更会看电影”，而在于让拉片结果更难胡说。

FFmpeg 负责可以测量的事实，模型负责必须理解画面才能完成的标注，代码负责检查时间轴、枚举、证据和资产是否闭合，最后再把结果渲染成可交互报告与同步视频。这条边界清楚、产物可检查、失败能定位的链路，比一次看似聪明的多模态回答更接近真正的生产工具。

它还不是自动剪辑师，也不是影片质量评委。更准确地说，它提供的是一条**镜头分析证据链**：从视频到切点，从切点到语义，从语义到规则验证，再从数据回到可播放的复盘载体。

## Sources

1. 微信原文：《这个刚开源的拉片 skill 让 AI 视频拉片变成一行命令！》
   https://mp.weixin.qq.com/s/E6SE4iIiDSPZEPE0zJ8PGQ

2. reelbench-skills repository and README
   https://github.com/eternityspring/reelbench-skills

3. Inspected repository revision
   https://github.com/eternityspring/reelbench-skills/tree/18f2f63987337df0975a89973d38d50f3231ee31

4. video-shots Skill specification
   https://github.com/eternityspring/reelbench-skills/blob/18f2f63987337df0975a89973d38d50f3231ee31/skills/video-shots/SKILL.md

5. video-shots implementation
   https://github.com/eternityspring/reelbench-skills/blob/18f2f63987337df0975a89973d38d50f3231ee31/skills/video-shots/scripts/video-shots.mjs

6. video-sync Skill specification and implementation
   https://github.com/eternityspring/reelbench-skills/tree/18f2f63987337df0975a89973d38d50f3231ee31/skills/video-sync

7. Apache License 2.0
   https://github.com/eternityspring/reelbench-skills/blob/18f2f63987337df0975a89973d38d50f3231ee31/LICENSE
