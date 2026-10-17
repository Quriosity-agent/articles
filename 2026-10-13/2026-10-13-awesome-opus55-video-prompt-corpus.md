---
title: "Awesome Opus 5.5 Videos 拆解：703 个爆款提示词不是视频源码，而是一套 Agent 视觉能力样本库"
date: 2026-10-13
source: "https://github.com/donghaozhang/awesome-opus5-5-videos"
canonical: "https://github.com/yihui-dev/awesome-opus5-5-videos"
tags:
  - Claude Opus 5.5
  - AI Video
  - Code-Generated Video
  - Prompt Corpus
  - Skillry
  - Canvas
  - SVG
  - Three.js
  - GSAP
  - Agent Workflow
  - Source Audit
---

# Awesome Opus 5.5 Videos 拆解：703 个爆款提示词不是视频源码，而是一套 Agent 视觉能力样本库

> **TL;DR：** `awesome-opus5-5-videos` 收集了 703 条与 Claude Opus 5.5 视频作品相关的提示词和社交媒体出处，其中 418 条在 Skillry 上有独立重制。它最有价值的地方不是证明“输入一句话就能稳定生成爆款视频”，而是把一轮集体实验整理成了可搜索的数据：人们正在用 Canvas、SVG、Three.js、shader 和 GSAP，把视频从不可编辑的像素结果改造成可检查、可重渲染、可交互的程序。与此同时，仓库不包含 HTML/JavaScript 源码、视频文件、资产包、运行日志或统一评测；207 条提示词还被明确标记为不完整。因此它是一套很好的灵感库和能力样本，不是一套可直接复现的生产工程。

![Opus 5.5 code-generated video mosaic](imgs/awesome-opus55-video-prompt-corpus/opus55-video-mosaic.webp)

- **用户提供的仓库：** [donghaozhang/awesome-opus5-5-videos](https://github.com/donghaozhang/awesome-opus5-5-videos)
- **上游仓库：** [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)
- **审计快照：** [`92aee2f`](https://github.com/yihui-dev/awesome-opus5-5-videos/tree/92aee2f586ac0715cb3cbcb6384834f98a33383d)
- **数据最后更新：** 2026-10-13
- **查阅时间：** 2026-10-18

## 一句话判断

**这不是“Opus 5.5 视频生成器”，而是一个由原作、提示词、技术标签和第三方重制组成的视觉 Agent 样本库。**

仓库把散落在 X 上的作品收拢起来，让人可以从结果反查提示词，再观察另一个执行环境能否做出相似作品。这个结构比单纯的“爆款视频合集”更有研究价值，因为它开始形成四层对应关系：

```text
原作者发布的成片
        ↓
公开或整理出的提示词
        ↓
Skillry 的独立重制
        ↓
媒介与技术标签
```

但这四层并不等于一条可重复构建链。原作者的源文件、Agent 对话、外部资产、模型设置和人工修改通常都不在仓库里。

## 仓库里究竟有什么

源码快照只有四类内容：`README.md`、`LICENSE`、`data/videos.json`，以及 `prompts/` 下的 Markdown 文件。没有 HTML、JavaScript、Python、Blender 工程、视频二进制、测试或 GitHub Actions。

本地核对结果如下：

| 项目 | 数量 | 含义 |
|---|---:|---|
| JSON 记录 | 703 | 每条包含作者、原帖、类别、提示词、海报和重制状态等字段 |
| Markdown 提示词文件 | 703 | 与 JSON slug 一一对应 |
| Skillry 重制 | 418 | 有外部重制页面与技术标签 |
| 暂无重制 | 285 | 有提示词卡片，但没有 Skillry 重制链接 |
| 标记为部分提示词 | 207 | 约占 29.4%，不能视为完整输入 |
| 少于 50 个字符的提示词 | 31 | 更接近一句需求，而不是制作规格 |
| 重复 slug | 0 | 数据主键保持一致 |
| JSON 与 Markdown 孤儿项 | 0 | 两套表示完整对齐 |

数据一致性做得不错。机器可以读取 `videos.json` 做筛选，读者也可以打开单独的 Markdown 卡片复制提示词。真正缺失的是生成过程本身。

## 703 条记录呈现出的媒介分布

完整数据集按类别分成：

| 类别 | 数量 |
|---|---:|
| Motion graphics | 369 |
| 3D scenes | 117 |
| Explainers | 116 |
| Games & interactive | 101 |

在 418 条已有重制的记录里，出现最多的技术标签是 Canvas 267 次、SVG 183 次、Three.js 131 次、shader 92 次、GSAP 86 次。标签会重叠，因此不能相加为作品总数；它们描述的也是 Skillry 重制采用的技术，不一定等于原作者的实际栈。

这些数字仍然揭示了一个明确趋势：所谓“AI 视频”在这里常常不是扩散模型输出 MP4，而是 Agent 写出一个确定性或半确定性的浏览器场景，再由浏览器播放、录屏或逐帧导出。

## 视频开始变成一个程序

浏览器原生栈特别适合 Agent，原因不神秘：

- Canvas 可以把每一帧直接写成绘图函数；
- SVG 让图形、文字与路径保持可编辑；
- Three.js 把相机、光照、材质和空间关系暴露为参数；
- shader 适合粒子、流体、发光与程序纹理；
- GSAP 把时间线和缓动变成可检查的代码；
- Web Audio 可以让交互和声音在同一页面运行。

传统视频生成模型给出像素结果；代码视频先给出场景规则。前者擅长摄影质感和自然运动，后者擅长精确文字、品牌色、图表、循环、交互和可修改性。这个仓库真正记录的，是视觉 Agent 在后一条路线上的集中爆发。

## “原作对重制”很有用，但不是严格 benchmark

![Skillry original and remake comparison](imgs/awesome-opus55-video-prompt-corpus/skillry-original-remake-compare.webp)

Skillry 把原作者视频和独立重制放在同一页面，读者可以直观看构图、节奏和视觉语言是否被保留。这比只看提示词更有价值，因为它暴露了提示词的迁移能力。

不过，侧边对比不能直接当成模型排行榜：

- 原作和重制可能使用不同模型版本、工具链与运行时间；
- 原提示词可能依赖附件、已有项目、私有 skill、本地路径或 API；
- 视频时长并不总是一致，例如同一页面可能是 5 分钟原作对 1 分钟重制；
- 没有统一记录迭代轮数、人工修复、失败样本、成本和耗时；
- 没有像素、运动、音频、交互或人工偏好的统一评分。

所以它更接近“行为样例库”：告诉你一种视觉任务曾经做出来，也可以被另一个 Agent 近似重建；它还不能回答哪一个模型更强、一次通过率是多少。

## 提示词不等于制作配方

仓库的提示词长度中位数约为 221 个字符，最长超过 1.5 万字符，最短只有 11 个字符。这个跨度本身就说明，“提示词”在这里至少包含四种不同东西：

1. 一句话愿望，例如做一个 Tron 游戏；
2. 带风格和时长约束的创意 brief；
3. 包含技术、镜头、字体和验收要求的制作规格；
4. 依赖附件、文件夹、API、已有 skill 和大量上下文的完整 Agent 任务。

本次静态扫描还发现，至少 23 条明确提到附件、本地路径、MP4 或参考文件；224 条提到 API、Blender、Remotion、FFmpeg、Three.js、GSAP 等外部工具或运行环境。这个扫描只是关键词统计，不能覆盖所有隐含依赖，但足以说明“复制提示词”常常只是复现的第一步。

例如仓库中一条长音乐视频任务要求读取本地资料、复用音轨、调用 ElevenLabs 和 Seedance、生成角色与场景、反复看片并校验同步。Markdown 保存了任务文字，却没有保存那些输入文件、API 状态、生成结果和中间选择。把它粘贴到另一个 Agent 中，得到的是同方向新作品，不是原作的确定性重建。

## 最值得借鉴的样例：逐帧确定性

![Deterministic frame-based rendering example](imgs/awesome-opus55-video-prompt-corpus/deterministic-frame-rendering.webp)

集合里最有工程价值的思想之一，是把视频写成 `frame = draw(n)`：每一帧只依赖帧号，不读系统时间，不使用不可控随机数。

这样做带来几个直接好处：

- 可以跳到第 720 帧单独排查，不必从头播放；
- 同一帧重复渲染应得到同一像素结果；
- 循环视频可以直接比较首尾帧；
- 修复文字遮挡后只需重渲染，不需要重新“抽卡”；
- 无头浏览器可以逐帧截图，再交给 FFmpeg 编码；
- Agent 可以用脚本检查越界、空白帧、运行错误和循环接缝。

这也是代码视频与普通实时网页的关键区别。网页动画追求“现在看起来在动”，视频渲染追求“第 n 帧永远可重建”。模型能力固然重要，但稳定导出往往取决于这个工程契约。

## 这套数据最能证明什么

**相对可信的结论：**

- Opus 5.5 可以在大量视觉任务中组织 Canvas、SVG、Three.js 和动画库；
- 代码生成已经能覆盖动态图形、解释视频、3D 场景和轻量游戏；
- 同一提示词可以跨执行环境产生可辨认的视觉对应物；
- 单文件网页是当前视觉 Agent 很有效的交付格式；
- 结构化收藏比零散社交媒体案例更适合检索和学习。

**不能由仓库单独证明的结论：**

- 703 个结果都是一次提示完成；
- 所有作品只使用 Opus 5.5，没有外部模型、素材或人工修改；
- 复制提示词就能得到相同质量；
- Skillry 重制忠实还原了原作的全部实现；
- Opus 5.5 在统一条件下优于其他模型；
- 展示视频对应的代码已经开放。

尤其需要强调最后一点：仓库开放的是目录与提示词，不是 703 个视频工程。

## 如果要把它升级成真正的视觉 Agent benchmark

这套收藏已经有很好的题库雏形。再补上以下证据，就能从灵感站进化成更严格的测试集：

| 需要补充 | 解决的问题 |
|---|---|
| 固定模型标识与运行日期 | 避免把不同版本混在一起 |
| 完整 prompt、附件与资产哈希 | 区分公开文字和隐藏上下文 |
| 生成的 HTML/JS 与依赖锁文件 | 让重制可检查、可重跑 |
| Agent 对话、工具调用和人工介入 | 统计真实的一次通过率与修复成本 |
| 固定 viewport、fps、字体和浏览器 | 消除渲染环境差异 |
| 帧级输出、音频和交互录制 | 覆盖静态截图看不到的问题 |
| 自动 QA 与多人盲评 | 同时检查工程正确性和审美质量 |

理想的单条记录不只是 `prompt + video`，而应是：

```text
任务 + 输入资产 + 环境清单 + Agent 轨迹
     + 源码 + 确定性渲染参数 + 成片
     + 自动检查 + 人工评价
```

有了这些，原作与重制之间的差异才可以被解释，而不只是被观看。

## 对实际创作者最有用的使用方式

不要从“复制最火的提示词”开始，而应从媒介和验收方式开始：

1. 先按 `motion / explainer / 3d / interactive` 找与目标相近的案例；
2. 再看技术标签，决定 Canvas、SVG、Three.js 还是混合栈；
3. 从提示词中提取时长、画幅、镜头、字体、配色、节奏和交互约束；
4. 把缺失的附件、素材授权、字体和音频单独列成输入清单；
5. 要求 Agent 输出源码、帧函数、导出脚本和 QA 报告，而不只是录屏；
6. 保存每次修改与最终环境，确保下次还能重渲染；
7. 最后用人工观看判断叙事、品牌感和审美，不把“页面能跑”当成“成片完成”。

仓库适合回答“还有哪些做法”，不适合替你定义“这次交付怎样才算通过”。

## 许可证边界

仓库根目录使用 MIT License，但 README 同时写明，每条视频和提示词属于对应创作者。更稳妥的理解是：MIT 许可覆盖仓库自身的整理结构与相关材料，不应被自动解释为获得了所有第三方视频、音乐、品牌资产和原始提示词的再授权。

实际采用时，应保留作者与原帖链接；用于商业项目前，还要单独检查素材、音乐、字体、商标与人物形象的授权。公开可见不等于可以无条件再发布。

## 结论

`awesome-opus5-5-videos` 最容易被误读成“703 个一键视频魔法咒语”。源码审计后，更准确的定位是：它把一次快速扩张的社区实验变成了可搜索的提示词语料和视觉能力地图。

它显示了 Opus 5.5 在浏览器图形上的广度，也显示了代码视频为什么适合 Agent：元素可寻址、时间可参数化、帧可重建、结果可交互。但作品的真正质量并不只来自模型名称。长任务里的参考资料、工具、素材、审美判断、迭代次数和导出 QA，往往比最后保存下来的那段提示词更关键。

把它当灵感库，价值很高；把它当可复现源码库，证据不足；把它当视觉 Agent benchmark 的原型，则非常值得继续建设。

## 参考资料

- [donghaozhang/awesome-opus5-5-videos - user-provided fork](https://github.com/donghaozhang/awesome-opus5-5-videos)
- [yihui-dev/awesome-opus5-5-videos - upstream](https://github.com/yihui-dev/awesome-opus5-5-videos)
- [Skillry Opus 5.5 video collection](https://skillry.dev/ai-videos/opus-5-5)
- [Machine-readable dataset](https://github.com/yihui-dev/awesome-opus5-5-videos/blob/92aee2f586ac0715cb3cbcb6384834f98a33383d/data/videos.json)
- [Deterministic frame-based rendering prompt](https://github.com/yihui-dev/awesome-opus5-5-videos/blob/92aee2f586ac0715cb3cbcb6384834f98a33383d/prompts/0xkarmi-129839.md)
- [Blender previs prompt](https://github.com/yihui-dev/awesome-opus5-5-videos/blob/92aee2f586ac0715cb3cbcb6384834f98a33383d/prompts/tonysurix-596746.md)

*本文审计于 2026-10-18。用户提供的仓库是 `yihui-dev/awesome-opus5-5-videos` 的 fork；审计时两者 `main` 指向同一 SHA `92aee2f586ac0715cb3cbcb6384834f98a33383d`。数量来自本地解析 `data/videos.json` 与 703 个 Markdown 文件；关键词依赖统计属于静态扫描，不代表完整运行时溯源。三张配图来自仓库 README 与其链接的 Skillry 媒体。*
