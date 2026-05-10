# video-use 深度拆解：把视频剪辑变成 Agent 可执行的工程流水线

> Repo: <https://github.com/browser-use/video-use>  
> Inspected commit: `fbcf29f`  
> Date: 2026-05-09  
> Tags: video-use / Claude Code / Coding Agent / FFmpeg / ElevenLabs Scribe / Agentic Video Editing

![browser-use/video-use GitHub repo](imgs/video-use-agentic-video-editor/github-repo.png)

## 1. 这不是一个「AI 视频生成器」，而是一个剪辑工程 harness

`browser-use/video-use` 的 README 把产品说得很轻：把素材丢进文件夹，和 Claude Code / Codex / Hermes 这类有 shell 权限的 agent 对话，最后拿到 `edit/final.mp4`。但从代码和 `SKILL.md` 看，它真正有意思的地方不是“AI 帮你剪视频”这个口号，而是：**它把视频剪辑拆成一组 agent 可以可靠调用、可验证、可缓存、可复盘的工程步骤。**

传统视频编辑器的交互对象是时间线、轨道、按钮和预设；video-use 的交互对象是：

- word-level transcript；
- on-demand timeline composite PNG；
- EDL JSON；
- ffmpeg render pipeline；
- session memory `project.md`；
- 一组写死在 skill 文档里的 production correctness rules。

这和 browser-use 的思路相似：不要让 LLM 盲看截图，而是给它结构化 DOM。video-use 的版本是：不要把 30,000 帧视频都塞给模型，而是让模型先读文字，再在关键节点看合成图。

## 2. 仓库事实：小仓库，但不是 toy demo

本次检查的是 `browser-use/video-use`，当前 HEAD 为 `fbcf29f`，最近一次提交是 `docs: add HyperFrames animation option (#13)`。GitHub 页面显示约 **7.1k stars**、**1k forks**、**11 commits**，默认分支是 `main`。

本地扫描结果：

| 类型 | 文件数 | 行数 |
|---|---:|---:|
| `.md` | 19 | 3,638 |
| `.py` | 6 | 1,908 |
| `.toml` | 1 | 22 |
| `.html` | 1 | 305 |
| `.svg` | 1 | 181 |
| `.png` | 1 | 12,016 |
| `.sh` | 1 | 14 |
| `.example` | 1 | 1 |
| no extension | 1 | 60 |
| **Total** | **32** | **18,145** |

主要目录：

- `helpers/`：6 个 Python helper，约 1,908 行，是实际执行层；
- `skills/manim-video/`：vendored Manim skill，17 个文件、约 3,060 行，其中 references 14 个文件、约 2,759 行；
- `static/`：README banner 和 timeline-view SVG；
- 根目录的 `SKILL.md`、`install.md`、`README.md`：不是普通文档，而是 agent runtime contract。

依赖也很克制。`pyproject.toml` 只声明 Python `>=3.10`，依赖为 `requests`、`librosa`、`matplotlib`、`pillow`、`numpy`，可选动画依赖为 `manim`。没有服务端、没有 Web app、没有数据库迁移、没有复杂包管理。真正的重型依赖在系统层：`ffmpeg` / `ffprobe`，以及转写所需的 ElevenLabs API key。

## 3. 架构核心：LLM 不看视频，LLM 读视频

README 的关键句是：**The LLM never watches the video. It reads it.** 这句话解释了整个架构。

video-use 把视频理解拆成两层：

### Layer 1：始终加载的音频转写

`helpers/transcribe.py` 会先用 ffmpeg 抽取 mono 16kHz WAV，再调用 ElevenLabs Scribe：

```python
SCRIBE_URL = "https://api.elevenlabs.io/v1/speech-to-text"

data = {
    "model_id": "scribe_v1",
    "diarize": "true",
    "tag_audio_events": "true",
    "timestamps_granularity": "word",
}
```

这几个参数非常关键：

- `timestamps_granularity=word`：每个词都有起止时间，剪辑点可以对齐 word boundary；
- `diarize=true`：多说话人场景能区分 speaker；
- `tag_audio_events=true`：笑声、掌声、叹息这类事件会保留为剪辑信号；
- 输出缓存到 `<edit_dir>/transcripts/<video_stem>.json`，已有文件时直接跳过，不重复烧 API quota。

### Layer 2：按需生成的视觉合成图

`helpers/timeline_view.py` 会针对一个 `[start, end]` 范围生成 PNG：上方是 filmstrip，中间是 waveform，下方有词标签和时间刻度，长静音会被高亮。它的 docstring 特意强调：

> Do NOT call it in a scan loop over every utterance; it's an on-demand drill-down, not a background index.

这很重要。它不是把视频预处理成海量视觉 tokens，而是在“有歧义的停顿、retake 比较、cut point sanity check”时生成一张 compact view。对 agent 来说，这是一种 token-budget-aware 的视觉探针。

## 4. `takes_packed.md`：真正的中间表示

如果只看 README，可能会以为转写 JSON 就是核心数据。但实际 agent 使用的是 `helpers/pack_transcripts.py` 生成的 `takes_packed.md`。

它做的事情很朴素：读取 `<edit>/transcripts/*.json`，把 word-level Scribe 结果按 **静音 ≥ 0.5s 或 speaker change** 分组成 phrase-level markdown：

```markdown
## C0103  (duration: 43.0s, 8 phrases)
  [002.52-005.36] S0 Ninety percent of what a web agent does is completely wasted.
  [006.08-006.74] S0 We fixed this.
```

为什么这层重要？因为 raw JSON 太啰嗦，SRT 又丢失了子秒级 gap 信息。`takes_packed.md` 是折中：保留足够精确的时间范围和 speaker 信息，同时把一小时素材压成 agent 可以读的文本。`SKILL.md` 直接称它为 **the LLM's primary reading view**。

从 builder 视角看，这就是 video-use 的“DOM”：不是最终媒体，也不是低层编码，而是给 agent 做决策的结构化视图。

## 5. EDL 是 agent 与渲染器之间的契约

`SKILL.md` 定义的 EDL 格式很直接：

```json
{
  "version": 1,
  "sources": {"C0103": "/abs/path/C0103.MP4"},
  "ranges": [
    {"source": "C0103", "start": 2.42, "end": 6.85,
     "beat": "HOOK", "quote": "...", "reason": "Cleanest delivery"}
  ],
  "grade": "warm_cinematic",
  "overlays": [
    {"file": "edit/animations/slot_1/render.mp4", "start_in_output": 0.0, "duration": 5.0}
  ],
  "subtitles": "edit/master.srt",
  "total_duration_s": 87.4
}
```

这里有几个工程上的优点：

1. **LLM 负责决策，不直接拼 ffmpeg 命令。** 它输出结构化 EDL，渲染细节交给 `render.py`。
2. **每段都有 `beat`、`quote`、`reason`。** 这让剪辑决策可 review，不只是时间码。
3. **路径解析集中处理。** `render.py` 的 `resolve_path()` 支持绝对路径和相对 edit dir 的路径。
4. **字幕、调色、overlay 都挂在 EDL 上。** 这让后续迭代可以改数据，而不是改一大段 shell 脚本。

对 agentic workflow 来说，EDL 是一个很好的边界：上游是语言推理，下游是确定性执行。

## 6. `render.py`：最值得看的不是功能，而是顺序

`helpers/render.py` 是仓库里最大的一段工程代码，核心不是“能不能渲染”，而是它把剪辑中容易静默失败的顺序固定下来。

它的 docstring 已经写明 pipeline：

1. 每个 segment 单独 extract，内嵌 color grade 和 30ms audio fade；
2. 用 concat demuxer 做 lossless `-c copy` concat；
3. 如果有 overlay 或 subtitles，再做一次 filter graph；
4. overlay 要用 PTS shift；
5. subtitles 必须最后应用。

这背后对应 `SKILL.md` 的 hard rules：

- 字幕必须在 filter chain 最后，否则 overlay 会盖住字幕；
- 不要用单次大 filtergraph，否则带 overlay 时会重复编码；
- 每个 cut 边界加 30ms audio fade，避免 pop；
- overlay 用 `setpts=PTS-STARTPTS+T/TB`，确保动画第 0 帧落在窗口起点；
- master SRT 要用 output timeline offsets，否则 concat 后字幕错位；
- 永远不要切在词中间。

这些都不是“审美建议”，而是视频工程里的 silent failure 防线。video-use 把这些规则写进 helper 和 skill 文档，等于给 agent 加了一条护栏：你可以有艺术自由，但不能破坏 production correctness。

## 7. 调色、HDR、响度：它在处理真实素材的坑

这个仓库不是只拼接 demo clip。`render.py` 和 `grade.py` 暴露出不少真实素材会遇到的问题。

### HDR → SDR

`render.py` 会用 ffprobe 检测 `color_transfer`，如果是 `smpte2084` 或 `arib-std-b67`，就 prepend 一段 `zscale + tonemap` chain，把 iPhone HLG / PQ 这类 HDR 源转成 Rec.709 SDR。代码注释解释得很具体：只降 bit depth 不做 tone mapping，会导致上传或屏录后过曝、过饱和。

### 自动调色不是 LUT

`grade.py` 默认是 auto mode：采样若干帧，用 ffmpeg `signalstats` 算亮度、对比、饱和度，然后生成一个保守的 `eq=` filter。所有调整被限制在约 ±8% 范围内。它的目标不是“电影感”，而是 **make it look clean without looking graded**。

预设只保留少量：

- `subtle`；
- `neutral_punch`；
- `warm_cinematic`；
- `none`。

### 社交平台响度

`render.py` 还包含 two-pass loudnorm：目标为 -14 LUFS integrated、-1 dBTP、LRA 11。这说明它考虑的是最终发布质量，而不是只生成一个能播放的 mp4。

## 8. 动画系统：不是绑定一个引擎，而是按 slot 选择工具

README 提到 overlay animation 可以通过 HyperFrames、Remotion、Manim 或 PIL 生成。`SKILL.md` 更清楚：**每个动画 slot 选择最合适的引擎**。

- HyperFrames：HTML/CSS/GSAP、产品 UI motion、网站/landing page/mockup 视频；
- Remotion：React/CSS composition、已有 React brand system；
- Manim：公式、图、状态机、形式化解释；
- PIL + PNG sequence + ffmpeg：简单卡片、计数器、typewriter、bar reveal。

值得注意的是，动画不是在 video-use 根目录里安装一堆全局依赖，而是在 `<edit>/animations/slot_<id>/` 内隔离 scaffold。多个动画还要求用 parallel sub-agents，不要顺序执行。这是典型的 agent 工程思路：把可并行的创作任务拆成 slot，把 wall time 降到最慢那个 slot。

## 9. 安装设计：它把 repo 当作 skill，而不是 CLI 产品

`install.md` 说明了 video-use 的定位：它不是一个你安装后运行 `video-use edit` 的传统 CLI，而是一个被 Claude Code、Codex、Hermes、Openclaw 等 agent 发现的 skill。

手动安装流程：

```bash
git clone https://github.com/browser-use/video-use ~/Developer/video-use
ln -sfn ~/Developer/video-use ~/.claude/skills/video-use
uv sync   # or pip install -e .
brew install ffmpeg
cp .env.example .env
```

几个冷启动约束很实际：

- symlink 整个目录，不是只 symlink `SKILL.md`，因为 helpers 必须和 skill 文档在一起；
- ElevenLabs API key 放在 repo root 的 `.env`，不要写进用户素材目录；
- install 验证不要默认跑转写，因为 Scribe 会花钱；
- Node.js/npm 只有用 HyperFrames 或 Remotion 时才需要；
- `yt-dlp` 是 optional。

这说明作者很清楚 agent skill 的分发形态：**文档 + helper scripts + 本地系统依赖 + 用户项目目录约束**，四者缺一不可。

## 10. 工作流：ask → confirm → execute → self-eval → persist

`SKILL.md` 最强的部分其实是流程约束，而不是代码。

一次 session 的推荐流程是：

1. Inventory：ffprobe 所有源文件，转写并 pack transcript，抽样 timeline view；
2. Pre-scan：从 `takes_packed.md` 里找口误、false start、要避开的表达；
3. Converse：根据素材提问，不用固定 checklist；
4. Propose strategy：用 4–8 句话说明结构、take choice、动画、调色、字幕、长度估计，等待确认；
5. Execute：生成 EDL，必要时看 timeline view，动画并行生成，render；
6. Preview；
7. Self-eval：对 rendered output 的每个 cut boundary 跑 timeline view，检查跳帧、音频 pop、字幕被盖、overlay 错位；
8. Iterate + persist：把 session 记录追加到 `<edit>/project.md`。

这里有一个很重要的产品判断：video-use 没有让 agent “自主剪完再给你惊喜”，而是把 strategy confirmation 设为 hard rule。视频是高主观性产物，先确认方向比盲目自动化更可靠。

## 11. 局限和风险：它强在 talking footage，弱在全自动视觉理解

从当前代码看，video-use 的边界也很清楚。

第一，它高度依赖 ElevenLabs Scribe。没有 API key，转写主流程就跑不起来；语言、口音、噪音环境都会影响 word boundary 的可信度。

第二，视觉理解是 on-demand，不是全量视觉索引。这是优点也是限制：对于以对白为主、可通过 transcript 驱动的 talking head / interview / tutorial，非常高效；但对于音乐视频、纯视觉 montage、体育镜头、动作场景，它需要更多人工提示和更多 timeline_view sampling。

第三，`timeline_view.py --edl` 目前明确写着 `Not yet implemented`，完整项目时间线视图还没有做完。

第四，它不是 GUI，也不是给非技术用户的 CapCut 替代品。它假设用户愿意使用本地 agent、shell、ffmpeg、API key、文件夹约定。

第五，很多“智能”来自 `SKILL.md` 的流程和提示约束，而不是一个稳定的 Python API。换句话说，它的产品形态更接近 agent harness / skill bundle，而不是传统 SDK。

## 12. Builder 视角：video-use 最值得借鉴的 5 个设计

如果你在做 agentic media tooling，我觉得 video-use 最值得抄的不是具体代码，而是这几个设计原则：

1. **给 LLM 一个中间表示。** `takes_packed.md` 之于视频，就像 DOM 之于网页，比 raw frames 更适合推理。
2. **把创作决策和确定性执行分开。** LLM 输出 EDL，Python/ffmpeg 负责执行。
3. **把 silent failure 写成 hard rules。** 字幕顺序、audio fade、word boundary、PTS shift 这些必须工程化。
4. **视觉能力按需调用。** 不扫描全视频，只在决策点生成 compact visual artifact。
5. **把 session memory 放在用户项目目录。** `project.md` 让下一次 session 能接上上下文，同时不污染 skill repo。

video-use 的价值不在于它今天就能取代专业剪辑师，而在于它展示了一个更现实的方向：**AI 视频工作流不一定从“生成像素”开始，也可以从“把剪辑决策结构化”开始。**

对于 builder 来说，这可能比又一个 text-to-video demo 更有启发。因为真实视频生产里，难点往往不是按一下生成按钮，而是素材管理、转写、选句、切点、字幕、调色、响度、返工和交付。video-use 选择把这些脏活变成 agent 可以执行的 pipeline，这才是它值得深入研究的地方。
