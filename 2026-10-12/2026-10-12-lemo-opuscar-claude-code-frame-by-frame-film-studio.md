# Lemo-Opuscar 源码拆解：它不是 43 个提示词，而是把 Claude Code 组织成逐帧电影工作室

> **结论先行：** Lemo-Opuscar 不是视频生成模型，也不只是“给 Claude 一段风格 Prompt”。它把 43 种视觉风格写成可执行的制作规范，再用导演指南、逐帧浏览器渲染、统一时间线、TTS、程序化配乐、音效、字幕和 FFmpeg 混音，把 Coding Agent 组织成一间小型电影工作室。源码与公开样片证明核心管线确实能运行；但 43 个 demo 的可复现程度并不完全一致，CI 也只验证画廊发布，不代表每支影片都能从干净环境一键重建。

![Lemo-Opuscar 43 种风格样片总览](imgs/lemo-opuscar-claude-code-frame-by-frame-film-studio/style-library-cover.jpg)

用户提供的 [`donghaozhang/lemo-opuscar`](https://github.com/donghaozhang/lemo-opuscar) 是 [`lemomo-ai/lemo-opuscar`](https://github.com/lemomo-ai/lemo-opuscar) 的同步 fork，不是独立开发版本。本文审计两者共同指向的提交 [`227e00a`](https://github.com/lemomo-ai/lemo-opuscar/tree/227e00adfbbec1ef4b7065a4189c2e1c8be2fef4)，日期为 2026 年 10 月 12 日。

项目最容易被误读成“43 个风格 Prompt + Claude Opus 5.5 宣传片”。真正值得看的，是它如何把审美描述变成能被 Agent 反复执行、检查和交付的工程结构。

---

## 01 | 它不是视频模型，画面本质上是一段时间函数

Lemo-Opuscar 不调用文生视频模型，也不使用库存视频。每支影片的视觉部分是一张网页，向渲染器暴露：

```js
window.DUR = 54.2;
window.render = (t) => { /* draw the exact frame at time t */ };
window.READY = true;
window.EV = [{ t, type }];
```

Headless Chromium 在每个时间点调用 `render(t)`，把 Canvas 2D、Three.js 或 WebGL2 页面逐帧截成图像，再编码为视频。默认规格是 1920×1080、24 fps；竖屏等其他尺寸由同一套渲染工具接收 `--size` 参数。

这条路线和扩散式视频生成完全不同：

| 视频模型 | Lemo-Opuscar |
|---|---|
| 从提示词采样像素与运动 | Agent 编写确定性的场景与动画代码 |
| 同一提示词难以逐像素复现 | 任意时间点可独立重渲染 |
| 修改常常意味着重新生成整段 | 可以修改对象、镜头、节奏或单个时间段 |
| 长时一致性交给模型隐状态 | 一致性由代码中的角色 rig、场景与时间线维持 |
| 声音通常是另一条生成流程 | 画面、声音、字幕共享事件与节拍时间线 |

代价也很直接：它没有视频模型的“先出一版再挑”。Agent 必须真的写绘图、动画、镜头、音乐和混音代码，制作时间与 token 消耗会转移到软件工程一侧。

---

## 02 | `STYLE.md` 不是形容词列表，而是一份风格生产合同

![中国水墨风格样片海报](imgs/lemo-opuscar-claude-code-frame-by-frame-film-studio/ink-wash-poster.jpg)

每个 `styles/<slug>/STYLE.md` 都把一种风格拆成相同的决策面：

- 这种媒介的本质，以及它不是什么；
- 材质、渲染方法、颜色逻辑和字体规则；
- 运动质量、镜头语法、声音色板；
- 只有这种媒介适合完成的 native move；
- 常见失败模式与实现提示；
- 哪些故事、角色、开场和结尾必须由当前项目重新决定。

例如中国水墨不是简单要求“黑白、宣纸、毛笔”。规范定义了五种墨色、湿墨与干墨层、飞白、留白比例、山水的远近层次、人物在 twos 上运动、镜头与墨晕转场，以及古琴、箫、鼓和纸面 Foley 的声音关系。风格因此从形容词变成可检查的约束。

![玻璃产品风格样片海报](imgs/lemo-opuscar-claude-code-frame-by-frame-film-studio/glass-product-poster.jpg)

43 个正式风格横跨绘画、版画、排版、数据叙事、动画、游戏和 3D 产品视觉。审计中，43 个目录都同时包含 `STYLE.md`、`DEMO.md`、`style.json`、poster 和 demo 源码，共有 1,267 个 demo 文件。它们不是一张风格名称清单，而是一套带参考实现的可执行设计系统。

---

## 03 | Demo 的价值不是供 Agent 复制，而是证明这种语法能落地

普通 Prompt 库常见的问题是：描述很好看，却没有证据证明模型能稳定做出来。Lemo-Opuscar 为每种风格配了一支完整短片，并公开画面代码、事件、字幕、配乐与素材授权。

但项目同时设置了一个很关键的防复制顺序：

1. Agent 先根据用户主题提出三种结构；
2. 写出自己的 `TREATMENT.md`、镜头表、节拍表和声音设计；
3. 用真实绘图代码做风格帧；
4. 只有此后才能打开 demo，学习笔刷、rig、shader 或混音技术；
5. 交付前将新片与 demo 比较，结构、开场、标志镜头、镜头路径、配乐形状和结尾至少四项不同。

这不是法律意义上的自动原创保证，但它至少把“不要照抄 demo”从一句口号变成工作流顺序。参考实现负责证明技术，主题、人物、镜头与叙事仍由新项目重建。

---

## 04 | 真正完整的是声音与节奏，不只是画面 renderer

项目把电影管线定义为一个共同时间轴：

```text
timeline
  ├─ picture: render(t) → Chromium → frames → video
  ├─ voice: TTS/recording → ASR check → word timings
  ├─ music: samples + synthesis → stems
  ├─ sound: procedural foley at event times
  └─ subtitles: SRT + burned-in captions
mix → FFmpeg two-pass loudnorm → final MP4
```

`DIRECTOR.md` 明确把判断顺序写成 **声音、节奏、镜头、导演**，好看的单帧只是起点。Agent 必须先做 cue map，把剪辑、动作、字幕与音乐拍点放进同一时间网格；每个可见动作要有对应 Foley；混音目标约为 −14 LUFS，并通过双遍 loudnorm 与 true-peak 限制输出。

语音也不是“生成了就算完成”。英文默认可走本地 Kokoro，中文可走在线 edge-tts；每句语音再由 faster-whisper 回听转写。字幕既导出 `.srt`，也作为风格画面的一部分烧录。项目还提供 black-frame、可读时长、关键动作 0.2 秒帧条和最终响度等检查方法。

这说明 Lemo-Opuscar 更接近一套 production harness：它不仅告诉 Agent 怎么画，也规定成片如何被听见、读懂和验收。

---

## 05 | Skill 不是发动机本身，而是把 Agent 接入这套制片制度

Claude Code plugin 中真正的 `SKILL.md` 很短。它负责三件事：

1. 把共享库 clone/update 到 `~/lemo-opuscar`；
2. 按需安装 core、voice、music 三档依赖；
3. 把 Agent 交给 `AGENTS.md`、`DIRECTOR.md`、`TECHNIQUE.md` 与选中的 `STYLE.md`。

因此它和常见的 Remotion skill 并不等价。Remotion 提供 React 视频框架；Lemo-Opuscar 自己用 Playwright/Chromium、Canvas、Three.js、WebGL 与 FFmpeg，并在渲染器外增加了风格库、导演方法、音频工具和验收合同。

它也不是一个新 Agent。真正负责理解主题、写故事、生成代码、修渲染错误和做审美判断的，仍然是 Claude Code 或其他 Coding Agent。仓库只是让这些决策有顺序、有工具、有范例和可交付格式。

---

## 06 | 我实际验证了什么

我在 Apple M4 Pro Mac 上检出固定提交 `227e00a`，只安装 core 依赖，不下载语音模型或乐器包，得到以下结果：

| 检查 | 结果 | 证据边界 |
|---|---|---|
| 43 个风格目录完整性 | 43/43 均有规范、demo 说明、metadata、poster 与 demo 目录 | 证明风格库不是 README 清单 |
| `styleboard/build.py --site` | 成功，报告 43 styles、43 with film、总时长约 44 分钟 | 证明 catalog、海报和画廊结构可重建 |
| Core 安装 | Node 与 Python core 依赖成功安装 | 不包含 voice/music 扩展模型与素材包 |
| `pixel-rpg` 单帧 | 1.5 秒与 12 秒画面成功渲染 | 公共 browser renderer 可以执行 demo 页面 |
| `pixel-rpg` 完整画面视频 | 54.5 秒、1920×1080、24 fps、1,308 帧 H.264，约 17 秒完成 | 验证纯画面渲染闭环；不等于重新混出其完整声音成片 |
| 事件导出 | 151 个事件，时长 54.5 秒 | 时间线事件可由页面导出 |

![使用公共渲染器在本机重新生成的 pixel-rpg 第 12 秒画面](imgs/lemo-opuscar-claude-code-frame-by-frame-film-studio/pixel-rpg-local-render.jpg)

不过两个反例同样重要：

- `pixel-rpg` 没有实现较新的 `window.TEXTS(t)`，所以 `readcheck.mjs` 明确返回 **NOT CHECKED**，不能写成可读性检查通过；
- `ink-wash` 页面会请求仓库未附带的实际 TTF 字体，单帧渲染因网络字体错误终止。仓库只保留 OFL 文本，`TECHNIQUE.md` 也要求使用者自行下载字体。

上游最新 [GitHub Pages workflow](https://github.com/lemomo-ai/lemo-opuscar/actions/runs/38245847827) 为绿色，但它构建画廊、下载 release 中的 720p MP4 并检查链接，不会从源码重渲染 43 支 demo。CI 绿色证明发布站点完整，不证明每个 demo 的一键重建路径完整。

---

## 07 | 43 styles 与 OPUSCAR 98 不是同一个粒度

![OPUSCAR 98 公开风格手册](imgs/lemo-opuscar-claude-code-frame-by-frame-film-studio/opuscar98-stylebook.jpg)

项目首页同时出现两个数字，容易造成误会：

- **43 styles**：正式风格库。每个都有完整 `STYLE.md`、demo、poster、metadata 和源码。
- **OPUSCAR 98**：一支 6 分 31 秒影片，让同一个 Clawd 穿过 1927–2025 年 98 部奥斯卡最佳影片，每部用一种匹配的视觉处理重绘。公开的 stylebook 为每段提供 2D/2.5D/3D 标签、截图、可复制提示词和镜头导演说明，其中 77 个 2D、4 个 2.5D、17 个 3D。

98 条记录是真实公开的风格与镜头资料，但它们不是 98 个额外的完整 skill 包，也没有各自独立的通用 engine、demo 项目与 QA 合同。更准确的理解是：43 个是可复用制作模板，98 个是长片中逐段公开的风格研究与导演笔记。

---

## 08 | 它的先进之处，也正是它的限制

Lemo-Opuscar 的真正突破不是“Claude 会写动画”，而是把一次性的创作经验整理成四层可复用资产：

1. **风格语法**：颜色、材质、镜头、声音、native move 与失败模式；
2. **导演制度**：brief、treatment、风格帧、可选 storyboard、制作和最终审片；
3. **执行工具**：确定性逐帧渲染、事件导出、语音、配乐、Foley、字幕和混音；
4. **证明材料**：43 支成片、源码、poster、CREDITS 与公开画廊。

这让“让 Agent 做一支片”不再只依赖一段超长提示词。但边界也很清楚：

- 项目明确针对新片制作，不负责编辑或转换现有视频；
- 风格为 Claude Opus 5.5 调优，其他模型不保证复现同样质量；
- 30–60 分钟制作时间与成片质量是项目方经验，不是本文独立基准；
- 复杂 3D、语音、乐器和字体仍需要额外下载与 GPU/网络环境；
- QA 只有在项目实现相应接口、并真正运行检查时才有效；
- MIT 许可覆盖项目代码，demo 中第三方字体、声音与素材仍沿用各自授权，用户素材也由用户负责。

最终最准确的一句话是：**Lemo-Opuscar 不是替代视频模型的另一个模型，而是把 Coding Agent、可执行风格规范和浏览器逐帧渲染接成一套电影生产制度。它的竞争力来自可编辑性、可复现性与完整声音流程；它的成本则是更多代码、依赖、token 和人工审片。**

---

## 主要来源

- [用户提供的 `donghaozhang/lemo-opuscar` fork](https://github.com/donghaozhang/lemo-opuscar)
- [官方上游 `lemomo-ai/lemo-opuscar`](https://github.com/lemomo-ai/lemo-opuscar)
- [固定审计提交 `227e00a`](https://github.com/lemomo-ai/lemo-opuscar/tree/227e00adfbbec1ef4b7065a4189c2e1c8be2fef4)
- [在线风格与影片画廊](https://lemomo-ai.github.io/lemo-opuscar/)
- [`AGENTS.md`: Agent 工作流](https://github.com/lemomo-ai/lemo-opuscar/blob/227e00adfbbec1ef4b7065a4189c2e1c8be2fef4/AGENTS.md)
- [`DIRECTOR.md`: 导演与交付标准](https://github.com/lemomo-ai/lemo-opuscar/blob/227e00adfbbec1ef4b7065a4189c2e1c8be2fef4/DIRECTOR.md)
- [`TECHNIQUE.md`: 渲染、声音与 QA 管线](https://github.com/lemomo-ai/lemo-opuscar/blob/227e00adfbbec1ef4b7065a4189c2e1c8be2fef4/TECHNIQUE.md)
- [Claude Code skill 入口](https://github.com/lemomo-ai/lemo-opuscar/blob/227e00adfbbec1ef4b7065a4189c2e1c8be2fef4/plugin/skills/lemo-opuscar/SKILL.md)
- [OPUSCAR 98 风格手册](https://lemomo-ai.github.io/lemo-opuscar/opuscar98)

*审计日期：2026 年 10 月 12 日。stars、forks、release 下载量和代码会继续变化；技术结论固定到提交 `227e00a`。项目关于 Claude Opus 5.5、制作耗时和样片制作过程的说法均视为项目方自述；本文独立复现的范围只包括上文列出的结构检查、画廊构建、单帧、事件导出和纯画面视频。*
