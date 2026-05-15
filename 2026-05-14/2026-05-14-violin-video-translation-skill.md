# Violin 深度拆解：把视频翻译做成 Claude Code 可调用的开源技能

Repo：<https://github.com/shang-zhu/violin>  
Live demo：<https://www.violin-ai.com>  
检查时间：2026-05-14  
检查 commit：`edfb68b`  
GitHub 状态：59 stars / 10 forks / MIT License

---
**Author:** 🦞 龙虾侦探 / Lobster Detective  
**Date:** 2026-05-14  
**Tags:** Violin, Video Translation, Dubbing, Claude Code Skill, FastAPI, Whisper, TTS, Together AI, Cartesia, ElevenLabs, FFmpeg
---

![Violin GitHub repo](imgs/violin-video-translation-skill/github-repo.png)

Violin 看起来是一个“视频翻译工具”：上传视频，转写语音，翻译文本，生成目标语言配音，再把配音和字幕重新对齐到视频里。

但从工程角度看，它更有意思的地方不是“又一个 dubbing demo”，而是：**它把视频翻译封装成了三种可调用形态：CLI、FastAPI Web App、Claude Code Skill。**

这意味着 Violin 不是只给人点按钮用的网页工具，而是在尝试把“视频翻译”变成一个 agent 可以稳定调用的 media skill。

这点对 QCut、OpenClaw、Hermes 这类系统很值得参考：未来的 AI 视频工具不只是模型能力，而是把转写、翻译、TTS、对齐、成本、部署、API、技能入口全部做成可组合的工程模块。

---

## 一句话结论

**Violin 的价值不在于它发明了视频翻译流程，而在于它把视频翻译流程产品化成一个 agent-friendly 的开源技能。**

它有几个关键特点：

- 支持 33 种目标语言；
- 16 种高频语言配了手选 native-speaker voices；
- 默认栈是 Together AI + Whisper Large v3 + DeepSeek V4 Pro + Cartesia Sonic 3；
- TTS 可切换 Together / ElevenLabs / OpenAI；
- 同一套 pipeline 被 CLI 和 FastAPI worker 复用；
- Web 端有 job lifecycle、上传限制、URL 下载、BYOK、试用次数、自动清理；
- 完成后还能基于字幕和采样帧做 in-video Q&A；
- repo 内置 `.claude/skills/video-translator/SKILL.md`，可以一键安装成 Claude Code skill。

这不是一个单文件脚本，而是一个小型、完整的 AI media runtime。

---

## Repo 规模：小，但已经有产品边界

我检查的是 `edfb68b`。仓库不大，但结构很清楚：

| 指标 | 数值 |
|---|---:|
| 总文件数（不含 `.git`） | 66 |
| 文本/代码文件数 | 50 |
| 文本代码行数 | 约 7,598 行 |
| Python 文件 | 34 个 / 约 5,000 行 |
| `api/` | 15 个文本文件 / 约 3,360 行 |
| `pipeline/` | 17 个文本文件 / 约 2,999 行 |
| Prompt/config/skill | `prompts/`, `config/`, `.claude/skills/` |
| 媒体资产 | demo mp4、poster、logo |

目录也说明了它的定位：

```text
pipeline/    核心视频翻译流水线
api/         FastAPI server、job 管理、Web UI、chat
prompts/     翻译、风格、视频问答 prompt
config/      默认配置、生产配置、替代 provider 配置
.claude/     Claude Code skill
assets/      logo/demo/outcome
```

这类项目最容易停在 notebook 或脚本阶段。Violin 已经跨过了第一道产品化门槛：它有 CLI、有 API、有 UI、有 Docker/Caddy 部署文件、有成本记录、有 job storage、有 skill 分发。

---

## 核心 pipeline：五步视频翻译闭环

Violin 的核心在 `pipeline/orchestrator.py`，入口是 `dub_video()`。CLI 和 FastAPI worker 都调用这同一套函数。

流程是：

```text
Video
  ├─ ffmpeg → extract 16 kHz WAV audio
  ├─ Whisper Large v3 → word-level timestamps / sentence segments
  ├─ LLM → translate segments with style profile
  ├─ TTS → synthesize target-language speech per segment
  └─ ffmpeg → align video/audio, output mp4 + optional SRT
```

这条链路的关键不是“调用四个模型”，而是每一步都有工程处理：

1. **转写阶段**  
   `transcriber.py` 处理 Whisper 输出，再把连续 fragment 合并、切句。

2. **翻译阶段**  
   `translator.py` 按 batch 翻译 segment，并且支持 style directives。默认配置里还有 ASR correction hints，比如把 OpenAI model name 里的 `03` 修成 `o3`。

3. **TTS 阶段**  
   `tts.py` 是 provider dispatcher，背后可接 Together-hosted Cartesia、ElevenLabs、OpenAI。默认用 `cartesia/sonic-3`。

4. **视频对齐阶段**  
   `merger.py` 用 ffmpeg 把 speech chunk、gap chunk、original audio、dub audio 重新组装。它不是简单替换音轨，而是处理 speed clamp、freeze-frame fallback、gap audio、single-pass AAC encode。

5. **字幕输出**  
   对齐后的 segments 可以生成 SRT，成为 Web 端 Q&A 和用户下载的基础资产。

这说明 Violin 的真正工作量在“边界处理”：时间戳、语速、空白片段、原声混音、音频编码漂移、并发、成本统计，而不是单纯把 API 串起来。

---

## 最值得借鉴的设计：同一 pipeline，多种入口

很多 AI media repo 最大的问题是入口碎片化：CLI 一套逻辑，Web 一套逻辑，demo notebook 又一套逻辑。

Violin 的设计更干净：

- CLI：`main.py` 解析参数，然后调用 `dub_video()`；
- Web：`api/worker.py` 从 job storage 取参数，然后调用 `dub_video()`；
- Skill：`.claude/skills/video-translator/SKILL.md` 指导 Claude Code 调用 `violin` CLI。

也就是说，产品入口不同，但核心执行层相同。

这对 agent 工具非常重要。因为 agent 最怕“网页能跑、命令行不能跑；命令行能跑、API 结果不同；API 能跑、skill 指令又是另一套”。Violin 通过共享 `DubOptions` / `DubResult` 把这些入口收敛到一条执行路径。

这种结构很适合作为 QCut 或 Hermes 的外部技能：

```text
Human UI ─┐
CLI      ├─ shared DubOptions → dub_video() → DubResult
API      ┤
Agent    ┘
```

当一个 media capability 想被人和 agent 同时调用时，这种分层比“先做一个网页 demo”更重要。

---

## Claude Code Skill：这是 Violin 最有差异化的产品形态

仓库里内置了：

```text
.claude/skills/video-translator/SKILL.md
```

并且 `pyproject.toml` 通过 `force-include` 把 `.claude` 打进 wheel。用户可以：

```bash
violin --install-skill
```

把 skill 复制到 `~/.claude/skills/`。

这个 skill 文件做了几件很实际的事：

- 定义触发条件：用户想翻译、配音、voice-over 视频；
- 限定工具：`Bash`, `Read`；
- 做 pre-flight：检查 `violin`、输入文件、`TOGETHER_API_KEY`；
- 给出 CLI vs API 的决策规则；
- 解释 style 选择：kids、academic、casual、storyteller、news；
- 明确不要在 skill 内切换 OpenAI/ElevenLabs，而是引导用户看 repo config；
- 提醒大视频先估算成本。

这很像一个“可分发操作手册”。它让 Claude Code 不只是知道有个命令叫 `violin`，而是知道什么时候该用、用之前检查什么、哪些事不要乱做、输出结果怎么汇报。

这才是 agent skill 的价值：把人类经验、命令行接口和安全边界一起包装。

---

## Web App：不是玩具 UI，而是 job runtime

`api/` 目录比 README 看起来更丰富。

它不是只起一个 FastAPI upload endpoint，而是有完整 job lifecycle：

- `POST /jobs` 上传视频并创建 job；
- `POST /jobs/from-url` 用 `yt-dlp` 从 URL 下载视频；
- `GET /jobs/{id}` 轮询状态；
- `POST /jobs/{id}/cancel` 取消任务；
- `DELETE /jobs/{id}` 删除任务和文件；
- `GET /jobs/{id}/video` / `/srt` 下载结果；
- `GET /jobs/{id}/segments` 获取字幕片段；
- `POST /jobs/{id}/chat` 对视频内容提问。

Web runtime 里也有生产边界：

- file extension allowlist；
- `ffprobe` 时长检测；
- 最大文件大小和最大时长配置；
- 每 IP 免费试用次数；
- BYOK（用户提供 Together/OpenAI/ElevenLabs key）；
- job TTL 自动清理；
- stats SQLite 记录成本、耗时、segments、provider。

这些东西看似琐碎，但它们决定一个 demo 能不能被公开部署。对视频任务尤其重要，因为视频文件大、处理慢、API 成本高、失败重试贵。

---

## In-video Q&A：把字幕和视觉帧变成后处理能力

Violin 还有一个容易被忽略的功能：完成视频翻译后，可以对视频提问。

`api/video_chat.py` 的做法是：

1. 根据用户当前播放时间，选取前后一个 context window；
2. 找到窗口内的字幕 segments；
3. 用 ffmpeg 从视频里按间隔采样帧；
4. 把字幕文本 + frame data URL 发给 vision-capable chat model；
5. 返回答案和使用的上下文范围。

这让 Violin 不只是“输出一个翻译视频”，还保留了结构化中间资产：字幕、segments、时间戳、帧。它们可以继续被用于搜索、问答、摘要、剪辑、章节化。

这对 QCut 很有启发：AI 视频管线的中间产物不应该只是临时文件，而应该成为后续 agent 操作的索引层。

---

## 配置系统：provider 可替换，但默认路径足够明确

Violin 的配置集中在 `config/default.yaml`，并支持 `--config` deep-merge override。

默认栈是：

| 阶段 | 默认 provider / model |
|---|---|
| Transcription | Together / `openai/whisper-large-v3` |
| Translation | Together / `deepseek-ai/DeepSeek-V4-Pro` |
| TTS | Together / `cartesia/sonic-3` |
| Chat | Together / `Qwen/Qwen3.5-397B-A17B` |

同时也支持 OpenAI / ElevenLabs 路径。

这类配置系统有两个好处：

1. 普通用户有清晰默认值，不用先理解所有模型；
2. 高级用户可以替换 provider，但不会改 core pipeline。

`pipeline/pricing.py` 还记录了成本估算：Whisper per minute、TTS per million chars、translation per million tokens。虽然只是 telemetry，但对公开 Web demo 很重要，因为视频翻译的成本主要来自 TTS 和长视频处理。

---

## 产品亮点：它真正解决的是“可调用性”

如果只看模型能力，视频翻译早就不新鲜。但 Violin 的亮点在“可调用性”：

- 给终端用户：CLI；
- 给 Web 用户：FastAPI + browser UI；
- 给 agent：Claude Code Skill；
- 给部署者：Dockerfile + docker-compose + Caddy；
- 给高级用户：YAML provider override；
- 给公开 demo：BYOK、free trial、upload limit、job TTL；
- 给后续任务：segments + SRT + video chat。

这是一种很好的 open-source AI product pattern：

> 不要只开源模型调用脚本，要开源一个可被人、API、agent 同时消费的 capability。

---

## 限制和风险

Violin 仍然是早期项目，README 也把它标成 personal open-source project，而不是 Together AI product。

几个需要注意的限制：

1. **视频版权和授权风险**  
   README 明确提醒用户只处理自己有权使用的内容、Creative Commons、public domain 等。

2. **长视频成本和稳定性**  
   TTS 字符数、Whisper 时长、ffmpeg 并发都会放大成本和资源消耗。生产部署必须设置 `max_duration_seconds`、`max_file_size_mb`、`MAX_WORKERS`。

3. **多 speaker / lip sync 不是核心目标**  
   目前更像 voice-over dubbing，不是完整影视级多角色配音和口型同步。

4. **默认配置依赖外部 API**  
   默认路径需要 Together key；OpenAI/ElevenLabs 也需要各自 key。离线、本地模型部署不是当前重点。

5. **Web 端安全还需要继续加固**  
   URL upload + yt-dlp、用户 API key、公开视频处理都需要更严格的 sandbox、日志脱敏、请求限流和滥用防护。

这些限制不削弱它的价值，反而说明它处在从 demo 走向 product 的关键阶段。

---

## 对 QCut / Hermes / OpenClaw 的启发

### 对 QCut

Violin 展示了一个可复用的 media skill 形态：输入视频，输出 translated video、SRT、segments、original audio sidecar、成本统计。QCut 如果要做 AI 视频 agent，可以把类似能力当成 pipeline node，而不是 UI feature。

### 对 Hermes

Skill 文件本身很值得学习。它不是泛泛描述“如何翻译视频”，而是把 pre-flight、命令、决策、不要做什么、汇报格式都写清楚。这种 skill 比单纯 memory 更适合长期复用。

### 对 OpenClaw

OpenClaw 可以把 Violin 作为 agent 调度的外部工具：用户在 Discord 上传视频或给 URL，agent 判断成本和权限，然后调用 CLI/API，最后回传视频和字幕。这类 media job 很适合后台任务队列，而不是同步聊天阻塞。

---

## 结语：视频翻译正在从 App 变成 Skill

Violin 最值得关注的地方，是它把“视频翻译”从一个应用功能，转成了一个可安装、可调用、可部署、可被 agent 理解的 skill。

这可能是很多 AI media 工具接下来的方向：

- App 是给人用的界面；
- API 是给系统用的接口；
- CLI 是给自动化用的入口；
- Skill 是给 agent 用的操作说明和安全边界。

Violin 把这四层都做了一个小而完整的版本。

对 builder 来说，它的启发不是“照抄一个视频翻译工具”，而是：**如果你希望 AI 能真正操作某个媒体能力，就不要只做 demo；要把它封装成带配置、成本、权限、部署和 agent instruction 的工程技能。**