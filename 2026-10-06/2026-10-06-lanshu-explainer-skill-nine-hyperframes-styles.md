# 岚叔讲解视频 Skill 源码拆解：九种风格不是九个模型，而是同一条时间轴上的九套视觉语言

> **一句话结论：** 这次更新不是给数字人口播换了九张“皮肤”，也不是接入九个视频生成模型。它是在原有数字人路线之外，新增了一条无真人的风格化讲解路线：同一份逐字对时的 `story.json`，通过九套 HTML/CSS/JavaScript 视觉 kit 和 HyperFrames 确定性渲染，变成九种可编辑的讲解动画。

![同一段 KV cache 讲解在九种视觉风格中的同一时刻](imgs/lanshu-explainer-skill-nine-hyperframes-styles/nine-styles-kv-cache.jpg)

2026 年 10 月 6 日，岚叔在 X 上宣布，拥有 2,000+ Star 的开源项目 [`lanshu-create-ai-presenter-video`](https://github.com/cclank/lanshu-create-ai-presenter-video) 增加了九种讲解视频风格，并说明这次迭代借助了 Claude Opus 5.5。

演示视频确实很容易让人产生一个疑问：这到底是类似 Remotion / HyperFrames 的视频 Skill，还是某种新的 AI 视频产品？

答案很明确：**它本质上是一个 Agent Skill，加上一套建立在 HyperFrames 上的讲解视频运行时。** AI Agent 负责理解主题、写稿、选风格、设计 storyboard 和实现每句画面；HyperFrames 负责把网页元素、SVG、Three.js、音频和时间轴确定性地渲染成视频。仓库中没有 Remotion 依赖或引用。

---

## 01｜这次更新真正增加了什么

项目原来只有一条 `presenter` 路线：用户提供主题或文案与一张授权人物图，Agent 再调用配音、数字人生成、口型同步和剪辑能力，完成一条数字人口播视频。

10 月 6 日的提交 [`c2e3bd7`](https://github.com/cclank/lanshu-create-ai-presenter-video/commit/c2e3bd755458cb2bb45f4880399e9cb983c8cd1a) 新增了第二条 `styled` 路线：

| 路线 | 用户提供 | 生成内容 | 付费生成 | 当前画幅 |
|---|---|---|---|---|
| `presenter` | 主题/文案 + 授权人物图 | 数字人、口型、字幕、关键词动效 | 配音 + 数字人视频 | 默认 9:16，也可其他比例 |
| `styled` | 主题或文案 | 无真人的风格化讲解动画 | 只有配音；自带音频可不调用 | 仅 16:9 |

这次提交一次加入 235 个文件、约 34,635 行内容，包括共享运行时、九套风格 kit、九套 starter、KV cache 完整样例、讲稿与配音工具、QA、渲染脚本和测试。

所以，它不是在旧的数字人视频上叠加滤镜，而是把项目从“数字人口播 Skill”扩展成了一个双路线讲解视频生产系统。

---

## 02｜九种风格不是九个 Prompt

九种风格分别是：

| Key | 风格 | 实现与适用内容 |
|---|---|---|
| `v1-editorial` | 设计师留白 | 暖白纸、墨色与朱红，适合商业和严肃主题 |
| `v2-signal` | 科技感信号 | 暗色 HUD、荧光数据流，适合 AI、系统与网络 |
| `v3-notebook` | 手写手帐 | 方格纸、实时书写与便利贴，适合推导和教学 |
| `v4-paper` | 纸艺立体书 | 折叠纸片、视差与柔和阴影，适合流程和故事 |
| `v5-comic` | 波普漫画 | 网点、贴纸与爆炸字，适合观点、辟谣和快节奏内容 |
| `v6-cinematic` | 电影感 3D | Three.js 影棚一镜到底，适合发布和大概念 |
| `v7-drafting` | 图纸与注脚 | 工程图纸、引线与真实注脚，适合技术深挖 |
| `v8-chalkboard` | 黑板报 | 粉笔书写、板擦与脑图复习，适合课堂和入门内容 |
| `v9-clay` | 黏土小城 | Three.js 等距黏土场景，用实物比喻抽象概念 |

每一套风格至少包含：

- 独立的 `kit.css` 和 `kit.js`；
- 字体、颜色、字号与安全区规则；
- 字幕、章节、数字、公式、柱状图、结尾与复习页组件；
- 一个去掉具体主题后的 starter 工程；
- 一套“这类画面如何演一句话”的镜头惯例；
- 程序化音效与相机运动逻辑。

V1–V5 与 V7 是纯 DOM/SVG 风格，V8 有自己的粉笔书写绘制逻辑，V6 与 V9 则把 HTML 叠加在 Three.js 场景上。九个 `kit.js` 合计约 6,340 行，`kit.css` 合计约 3,492 行。这显然比九条提示词或九套颜色变量更重：**它们是九个遵守同一接口的视觉组件系统。**

---

## 03｜真正的核心是 `story.json`

九种风格能够复用同一份内容，靠的不是让模型重新“理解一次”，而是先把讲稿编译成结构化时间数据：

```text
script.md
  ↓  配音或已有录音
story.json
  ├─ narration lines
  ├─ word timestamps
  ├─ chapters
  ├─ closing line
  ├─ recap
  └─ approved facts
  ↓
style starter + beats.js
  ↓
HyperFrames render
```

`script.md` 不只保存台词，还包含章节、每章画面提示、结尾金句、复习页和允许上屏的事实。`story.py` 默认按行调用 MiniMax T2A，直接取得引擎返回的逐字时间，并按“模型、声音、语速、文本”缓存结果；修改一句，只需要重配这一句。

如果用户已有旁白，也可以使用 `--audio`。这时工具根据停顿切分句子，再按说话权重估算词级时间。项目自己把这种精度标为约 0.15 秒：字幕通常够用，但依赖单词瞬间触发的动画会比引擎原生时间戳更松。

最终，所有镜头都从 `story.at()`、`story.phrase()` 和 `story.span()` 读取发音时刻。字幕、图形变化、相机移动和音效因此共享同一只钟，而不是各自猜时间。

---

## 04｜它为什么更接近 HyperFrames，而不是生成式视频

仓库的 starter `package.json` 直接把预览、检查、渲染和发布命令绑定到 `hyperframes@0.8.81`。每一帧都是时间 `t` 的确定性函数；同样的代码、素材和时间会得到同样的画面。

这与生成式视频有根本区别：

| 方法 | 主要输入 | 输出如何产生 | 可编辑性 |
|---|---|---|---|
| 文生视频模型 | Prompt / 参考图 | 模型采样像素 | 通常只能重新生成或局部编辑 |
| 普通模板 | 文案 + 固定字段 | 替换既有占位内容 | 稳定，但表达范围窄 |
| 这套 Skill | 结构化讲稿 + Agent 编写的场景逻辑 | HyperFrames 渲染 DOM/SVG/Three.js | 字幕、镜头、布局、颜色、节奏都可改 |

它与 Remotion 的理念相近：都是用代码描述时间轴和画面。但这个仓库实际使用的是 HyperFrames，没有 Remotion 代码。更准确的理解是：**这是一个让 Codex、Claude Code 等 Agent 使用 HyperFrames 做讲解视频的生产 Skill。**

---

## 05｜“九种都先出一版”究竟生成了什么

`new_topic.sh` 可以把同一个 `story.json` 同时装入九套 starter，快速得到九个能从头播放到尾的草稿，并用 `still_grid.py` 生成九宫格供选择。

这些草稿已经包含：

- 逐字字幕与章节条；
- 配音和程序化音效；
- 结尾金句与一帧复习图；
- 风格对应的字体、色彩、相机和布局；
- 每一句话的风格化占位镜头。

但 starter 中的 `beats.js` 明确把镜头标为“待演绎”。Agent 还需要根据 storyboard，把每句旁白替换成真正能解释内容的视觉动作。比如说到“只算新的 token”，画面应当让新 token 进入缓存，而不是只弹出同一句文字。

因此，“九种都出一版不增加 API 费用”是有条件成立的：配音锁定后，九套草稿复用同一音频，不再调用生成模型；但仍有本地渲染、字体下载、3D GPU 时间，以及把选中风格从占位草稿做成成片的设计与编码工作。

![X 演示视频中四个时刻的九风格同步演绎](imgs/lanshu-explainer-skill-nine-hyperframes-styles/x-demo-four-moments.jpg)

---

## 06｜它最成熟的地方，其实是生产约束

这个 Skill 没有把“视频文件生成出来”当成完成，而是复用了原数字人路线的八阶段状态机：

```text
intake → content_locked → audio_locked → visual_plan_locked
→ presenter_generated → composition_checked → rendered → verified
```

在 `styled` 路线里，`presenter_generated` 不再表示数字人，而是表示完成演绎的 film project 已存在并经过人工视觉检查。命名略显历史包袱，但证据门槛仍然有效。

`qa.py` 会：

- 执行 HyperFrames `check`；
- 在章节、句间、结尾和复习页抓取快照；
- 比较间隔 0.3 秒的帧差，检测相机停住或画面冻结；
- 生成封面和 `composition.json`。

`render.sh` 再用严格模式渲染，调用统一交付脚本做响度归一化、完整解码、黑帧/冻结检测、master/share 编码、SRT 和 contact sheet。这里的思路很重要：**Agent 不负责宣布“我做完了”，状态由磁盘上的产物和检查报告推进。**

我在 2026 年 10 月 7 日对提交 `c24720a85d63b1bd494f6447e48a59384733647b` 运行了两个仓库 smoke test：原数字人流程的七组检查与风格化路线的五组检查均通过，九个 starter 都可以同步、写入时长并通过脚本语法检查。

不过，这些 smoke test 是离线结构测试，并不等于九条 1080p 成片都被本次审计重新渲染。本文检查了源码、测试、官方九宫格和 X 上 45 秒、1920×1080、30 fps 的演示视频，没有独立执行完整 HyperFrames delivery render。

---

## 07｜Opus 5.5 做了什么，公开证据能说到哪里

新增九风格路线的提交带有 `Co-Authored-By: Claude Opus 5.5`，因此“Opus 5.5 参与开发”有直接 Git 证据。仓库文档也留下了相当多迭代痕迹，例如各风格的字号、空画面、字幕对比度和镜头停滞问题，以及哪些问题需要下一轮修复。

但公开 Git 历史把 34,000 多行新增内容压缩在一个大提交中。它无法让外部读者重建每一轮设计评审，也无法量化哪些代码由模型生成、哪些由开发者修改。因此更稳妥的说法是：**Opus 5.5 共同完成了这次大规模实现；“经过多轮迭代”来自作者和文档记录，不是可由逐次提交完整复现的开发过程。**

这也提醒我们，判断 AI 编程项目不能只看代码量。更有价值的证据是接口是否统一、样例能否迁移、失败是否被记录、测试是否覆盖状态边界，以及实际成片能否通过视觉验收。

---

## 08｜当前边界

这套系统已经比“动效 Prompt 合集”完整得多，但仍有清晰边界：

1. **风格化路线只有 16:9。** 竖屏需求目前要改走数字人路线，或自行重构九套 starter。
2. **公开成片主题仍然有限。** 仓库完整打包的是 KV cache；文档称九套 kit 还在 HF Storage 上验证过，但该项目没有随仓库提供。
3. **starter 不是最终内容。** Agent 必须按题目实现 `beats.js`，否则交付的只是带“待演绎”占位符的草稿。
4. **外部依赖并未消失。** 默认配音使用 MiniMax；HyperFrames 通过 `npx` 调用；字体从 Google Fonts / jsDelivr 下载；两种 3D 风格需要 GPU 能力。
5. **自带旁白的词级时间是估算。** 对字幕足够，不一定适合要求逐词精确触发的复杂画面。
6. **跨 Agent 客户端的可移植性主要来自文本规范。** README 声称支持 Codex、Claude Code、Gemini CLI、Cursor 等，但本次没有逐一运行验证。

因此，它目前最适合 30–120 秒、结构明确、可以用图形和比喻讲清楚的横屏解释型内容，而不是广告大片、素材混剪或完全开放式的长篇纪录片。

---

## 09｜真正值得关注的变化

以前谈“视频 Skill”，常常只是把一组 Prompt 和几个 CLI 命令写进 `SKILL.md`。这个项目开始走向另一种形态：

- `story.json` 是内容与时间的中间表示；
- style kit 是可复用的视觉语言；
- starter 是去掉主题后的可运行工程；
- `beats.js` 是 Agent 针对本期内容编写的镜头表演；
- HyperFrames 是确定性渲染器；
- state machine 与 QA 把“完成”绑定到证据。

这已经不像一个简单模板，更像一个小型的 Agent 视频制作操作系统。它把创意工作拆成了两部分：人和 Agent 决定“这一句话怎样被看见”，运行时负责“它在准确的那一帧发生，并且能稳定交付”。

九种风格的意义也不只是让内容看起来不同。风格在写稿前被选定：漫画要求短句和爆点，手帐需要给书写留时间，图纸适合高密度术语，黏土需要持续一致的比喻世界。**视觉系统反过来约束语言，这是它比普通换肤模板更成熟的地方。**

---

## 10｜结语：它是 Skill，也是一个可编程讲解视频引擎

如果只看 X 上的九宫格，会以为这是九套漂亮模板；如果只看 “Opus 5.5” 和 34,000 行新增代码，又容易把它归结为一次 AI 编程炫技。

源码展示的东西更具体：原来的数字人口播流程被扩展成了双路线系统；新路线以音频为主时钟，用结构化讲稿连接九套视觉 kit，再通过 HyperFrames 输出可检查、可复现、可修改的视频。

所以，可以把它理解成“Remotion Skill”这一类概念，但实现上它是 **HyperFrames Skill + 九套视觉运行时 + 一套证据驱动的生产流程**。它不是九个视频模型，也还不是输入主题就自动产出九条精修成片的一键产品。它真正解决的是更基础、也更有复用价值的问题：让 Agent 知道一条讲解视频应该怎样被规划、实现、检查和交付。

---

## 主要来源

- [岚叔的 X 更新帖](https://x.com/LufzzLiz/status/2107408409859359211)
- [用户提供的 GitHub 链接帖](https://x.com/LufzzLiz/status/2107408413458309193)
- [`lanshu-create-ai-presenter-video` GitHub 仓库](https://github.com/cclank/lanshu-create-ai-presenter-video)
- [新增九种风格路线的提交](https://github.com/cclank/lanshu-create-ai-presenter-video/commit/c2e3bd755458cb2bb45f4880399e9cb983c8cd1a)
- [九种风格选择指南](https://github.com/cclank/lanshu-create-ai-presenter-video/blob/main/explainer/STYLES.md)
- [Style kit 接口与实现说明](https://github.com/cclank/lanshu-create-ai-presenter-video/blob/main/explainer/KITS.md)
- [风格化讲解完整工作流](https://github.com/cclank/lanshu-create-ai-presenter-video/blob/main/references/styled-explainer.md)
- [风格化路线 smoke test](https://github.com/cclank/lanshu-create-ai-presenter-video/blob/main/tests/explainer_smoke.sh)

*审计日期：2026 年 10 月 7 日。仓库状态、依赖版本和功能边界可能继续变化。*
