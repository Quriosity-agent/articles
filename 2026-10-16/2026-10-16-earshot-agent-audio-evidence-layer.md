---
title: "earshot 源码审计：它没有让 Agent 长出耳朵，而是把声音变成可测试的证据"
date: 2026-10-16
source: "https://github.com/donghaozhang/earshot"
canonical: "https://github.com/Leonxlnx/earshot"
tags:
  - earshot
  - Audio QA
  - Coding Agent
  - MCP
  - CLAP
  - AudioSet
  - Sound Design
  - Procedural Audio
  - FFmpeg
  - Source Audit
---

# earshot 源码审计：它没有让 Agent 长出耳朵，而是把声音变成可测试的证据

> **TL;DR：** earshot 不是语音转写工具，也不是把一段音频直接交给大模型写感想。它在本地 CPU 上组合 CLAP、AudioSet 分类器和传统音频测量，把声音转换成 Agent 能处理的文字、JSON、时间轴与分析图：某个音效像不像“厚重机械键”、长录音中哪 240 毫秒最合适、冲击声是否晚于画面切点、整支发布片的响度与动态是否落在参考范围。它还提供 `forge`，让 Agent 用代码合成音效、听取评分、变异参数并再次生成。真正的新意是把声音从不可见的附件变成可回归测试的工程证据；但它不能判断审美、情绪、版权或台词内容，混音中的事件标签也远没有宣传语那么可靠。

![Frames from the earshot launch film](imgs/earshot-agent-audio-evidence-layer/earshot-launch-frames.png)

- **用户提供的仓库：** [donghaozhang/earshot](https://github.com/donghaozhang/earshot)
- **上游仓库：** [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot)
- **v0.1.0 发布：** [Release and 22-second launch film](https://github.com/Leonxlnx/earshot/releases/tag/v0.1.0)
- **审计快照：** [`108763c`](https://github.com/Leonxlnx/earshot/tree/108763c62648c78dbac14f5bebcd3c61ac7931cd)
- **发布时间：** 2026-10-16
- **查阅时间：** 2026-10-17

## 一句话判断

**earshot 不是给 Agent 模拟一双人耳，而是给音频生产增加一套 Agent 可读的仪表、检索器和验收回路。**

今天的 Coding Agent 已经可以写 Remotion、Three.js 或游戏代码，也能调用 FFmpeg 导出视频。但完成渲染之后，它通常只能看到画面，无法可靠回答：

- 这个按键声是厚实的 `thock`，还是廉价的 `click`？
- 一段十分钟现场录音里，哪一个击打最干净？
- 音效是否比切镜晚了 80 毫秒？
- 音乐高潮有没有落在产品揭晓处？
- 混音是安静、过热、被压扁，还是只在某几秒失控？
- 修改后的版本真的更接近参考片，还是 Agent 只是换了一套形容词？

earshot 的答案不是“让模型自由发挥听后感”，而是先把声音转换成可重复读取的中间证据。

## 它把“听”拆成了三种不同能力

### 第一层：不需要模型的客观测量

`measure` 使用传统信号处理读取 LUFS、true peak、LRA、噪声底、attack、decay、频谱、tempo 与 key。这一层最接近仪表，不需要猜测“听起来像什么”。

对于交付验收，这些数字往往比形容词更重要。比如音效是否削波、片尾是否真正衰减到静音、AAC 解码后峰值是否越界，都属于可以直接判定的问题。

### 第二层：用开放模型回答语义问题

earshot 下载两个模型，总计约 1.4 GB：

- **CLAP `laion/larger_clap_general`：** 把文字和音频映射到同一 embedding 空间，用于 `describe`、`match`、`rank`、`find` 和参考音频相似度；
- **AST `MIT/ast-finetuned-audioset-10-10-0.4593`：** 给出 527 类 AudioSet 标签，作为独立的宽类别线索。

仓库没有把 CLAP cosine 冒充概率。它先用词表和校准统计把相似度转成 z-score，再输出 `strong / plausible / weak / no match`，同时保留最接近的替代解释。Agent 因此可以看到“这是强匹配，但更像 Enter 键而不是空格键”，而不是只收到一个看似精确的 0.83。

### 第三层：把整支影片变成时间证据

`timeline` 会列出声音事件、段落、响度曲线、节拍、画面切点和 cue 的同步偏移；`sheet` 再把视频帧、事件标签、频谱、波形、响度与同步标记画成一张 PNG。

![earshot annotated listening sheet](imgs/earshot-agent-audio-evidence-layer/earshot-listening-sheet.png)

这张图是整个项目最准确的产品说明。对不能直接播放音频的 Agent 来说，声音第一次变成了可以“看”的时间结构：哪里密集、哪里留白、哪个冲击落在切点、哪个 whoosh 只是缓慢经过而没有形成新 onset。

## 16 个 CLI 命令，实际上对应四条生产回路

| 回路 | 主要命令 | Agent 得到什么 |
|---|---|---|
| 选择素材 | `describe`、`match`、`rank`、`find` | 声音描述、语义匹配、候选排序、长录音中的最佳 trim |
| 对比与验收 | `compare`、`ab`、`realness`、`measure` | 与参考库的距离、A/B 差异、真实录音/程序合成倾向、客观测量 |
| 检查影片 | `timeline`、`sheet`、`critique`、`profile` | 声画同步、听觉时间轴、分析图、基于自定义参考片的 scorecard |
| 制作与接入 | `forge`、`llm`、`mcp`、`doctor` | 程序化音效搜索、可选 Gemini 意见、Agent 工具接口、安装诊断 |

这种拆分比“上传文件，返回一段评论”更适合自动化。每个动作都有明确输入、结构化输出和失败码；文本摘要给 Agent 快速阅读，`--json` 提供完整数据，`--out` 可以保存成审计产物。

## 它与普通 Audio LLM 的区别

earshot 默认不把音频上传到云端。模型在本地 CPU 上运行，embedding 和结果缓存在磁盘中，分析命令可以离线重复执行。只有可选的 `llm --yes-upload` 会调用 Gemini，而且代码同时检查 API key 与显式同意。

二者适合回答的问题也不同：

| 本地 earshot | 通用 Audio LLM |
|---|---|
| 精确响度、峰值、时间与同步偏移 | 整体听感、叙事和语言化建议 |
| 在几百个候选中稳定排序 | 对少量样本做开放式评论 |
| 生成 JSON、时间轴和可比较指标 | 输出自然语言意见 |
| 可建立自己的参考 profile | 依赖模型隐含审美与训练分布 |
| 默认不上传文件 | 通常需要发送音频 |
| 不能理解台词内容 | 可能具有转写和语言理解能力 |

最合理的关系不是二选一。earshot 负责仪表、定位和回归；Audio LLM 可以提供第二意见，但它的时间戳和审美判断仍要回到 `timeline`、`ab` 与人工听审验证。

## `forge` 才是最有野心的部分

`earshot forge` 不使用录音作为合成材料。recipe 用 modal resonator、接触激励、滤波噪声、计算出的房间和麦克风噪声生成 48 kHz 音频，再让 critic 从多个方向评分：

```text
定义物理合成 recipe 与参数空间
        ↓
批量渲染候选，统一到 -1 dBFS
        ↓
比较目标文字、混淆项、真实参考和客观音色
        ↓
保留精英，缩小步长并变异参数
        ↓
用新随机种子 robust 重渲染
        ↓
Agent 阅读问题、修改 recipe 结构，再跑一轮
```

仓库目前自带 click、impact、keypress、pluck、pop、whoosh 六类 recipe。搜索不是神经音频生成，而是对可解释 DSP 参数做进化式优化。每个候选保留参数、seed 和评分，因此一个差结果可以被定位为“500-630 Hz 高出所有参考 16 dB”或“尾音比参考长”，而不是只能重新抽卡。

不过，作者也明确写出了 Goodhart 风险：搜索器优化的正是 earshot 自己的模型，最终可以让模型分数全部通过，却没有让声音真正更好。`p_real` 也很容易被 modal resonator、房间响应和噪声底骗过。

README 报告了一次 15 轮的小型盲测：同一名作者在真实录音与合成结果之间识别出程序合成项 8 次，接近抛硬币。这个结果值得继续测，但一个听者、15 次试验不能证明“与真实录音不可区分”。真正可靠的终点仍应包括模型外频谱测量、新 seed 重渲染和多人盲听。

## MCP 让它适合 Agent，但并非所有命令都进了 MCP

MCP server 暴露 13 个工具：`measure`、`describe`、`match`、`rank`、`find`、`compare`、`ab`、`realness`、`timeline`、`sheet`、`critique`、`doctor` 和 `llm_critique`。

这有两个工程价值：

1. 模型只在 server 首次调用时加载，后续命令不再反复支付 20-40 秒冷启动；
2. tool schema 明确区分只读、本地写图和联网上传，`llm_critique` 被标记为开放网络且必须获得同意。

但 README 中“same tools as an MCP server”不能按字面理解。`forge` 与 `profile` 没有进入 MCP 的 `TOOLS` 注册表，Agent 需要通过 CLI 或 Python API调用；MCP 调用也由全局锁串行执行，避免多个重模型任务同时压满 CPU。

这并不是严重缺陷，却说明 v0.1.0 的最佳运行方式仍然是混合式：高频分析走常驻 MCP，批量 profile 和 forge 由脚本编排。

## 验证结果有诚实的数字，也有明确的适用范围

仓库把评估命令、派生 JSON 和结果表放在 `eval/` 与 `docs/VALIDATION.md`。几个核心结果如下：

| 能力 | 发布时报告的结果 | 应怎样理解 |
|---|---|---|
| 语义匹配 | 保留库中 `strong` 对“正确声音类别”的估计精度约 98% | 精确变体只有约 61%；强结果建立在仅 3 个错误 pair 上，区间很宽 |
| 真实/合成分类 | 1,484 个片段、分组留出 ROC-AUC 0.922 | 阈值在同一批留出预测上选择；长文件只有 23 个合成样本参与弱校准 |
| 混音事件检测 | 60 秒影片中找回 93.2% 已放置音效 | 音乐下低 6 dB 以上的安静事件只找回 64.7% |
| 声画同步 | 140 个 attack-aligned cues 中 96% 的偏移误差在一帧内 | soft whoosh 和 swell 仍可能被错报为“没有声音” |
| 事件标签 | 暴露事件约一半类别正确，埋在音乐下约四分之一 | 事件时间和电平比标签可信 |
| 发布片 scorecard | 七支参考片 leave-one-out 有 86% 指标落在其他六支范围内 | 不是盲测，部分规则在第一次结果后修改；只代表这七支影片的风格 |

这些限定语恰好是项目可信的地方。它没有把 AUC 说成“92% 准确”，也没有把七支 SaaS/AI 发布片的范围包装成普遍审美标准。

## 它能判断什么，不能判断什么

**相对可信：**

- LUFS、dBTP、LRA、时间、频谱和硬切同步；
- 暴露的单个音效是否匹配明确描述；
- 从一批候选里排序，并在长录音中找干净片段；
- 明显程序合成的简单声音；
- 同一交付物修改前后的客观差异。

**只能作为线索：**

- 忙碌混音里每个事件的具体类别；
- 音乐类型与情绪；
- 七支参考发布片定义的“正常范围”；
- `realness` 对设计感很强的 chime、whoosh 和电子音乐的判断。

**不能判断：**

- 一段声音是否美、是否有情感、是否适合品牌；
- 台词说了什么；
- 录音来源、授权和归属；
- 被更响声音完全遮住的程序合成层；
- 模型前端听不到的 14 kHz 以上细节。

所以 earshot 最适合做 sound QA 和候选检索，不适合成为最终艺术总监。

## 源码审计：可检查，但还不是即插即用的成熟产品

用户提供的 `donghaozhang/earshot` 是 `Leonxlnx/earshot` 的 fork。查阅时，两边 `main` 都指向同一个 SHA `108763c`，仓库只有一个根提交；`pyproject.toml` 标记版本 `0.1.0`、Development Status 为 Alpha、代码采用 MIT 许可。

这份快照包含：

- 完整 Python package、16 个 CLI 命令与 13 个 MCP 工具；
- CLAP/AST wrapper、校准词表、realness 权重和 launch profile；
- 六类 forge recipe 与进化搜索；
- 两个 Agent skills：分析声音的 `earshot`，以及从授权录音制作成片音轨的 `real-sound`；
- 测试、评估脚本、派生 JSON、验证报告和限制文档。

本次在 Python 3.14 上对 package、tests、eval 与 skills 中的 Python 文件运行了 `compileall`，语法检查通过。没有安装 PyTorch、Transformers、SciPy 等完整依赖，也没有下载约 1.4 GB 模型，因此没有把仓库记录的“128 passed、14 skipped”冒充本机测试结果。

完整评估也不能只靠 clone 复跑。受许可限制的 344 份 Freesound/Mixkit 录音、七支专业影片和成片工程没有分发；仓库保存的是脚本、说明和派生数字。这比只贴 benchmark 截图透明得多，但仍属于“方法与结果可审查，原始数据无法完整复算”。

最后，单提交快照已有少量文档漂移：`docs/DESIGN.md` 还写着“不生成合成交付物”，而 README 与 skill 已把 `forge` 作为核心能力；skill 某处仍说“尚无人听过”，README 则加入了作者的 15 次盲测。它不影响代码主路径，却提醒采用者把 README、skill 和设计文档视为快速迭代中的 v0.1 材料，而不是稳定规范。

## 对视频、游戏和 Agent 工作流最实际的价值

earshot 最适合插在“已经能自动渲染，但还不能自动听审”的流程中：

1. Agent 从素材库下载多个音效后，用 `rank` 缩小范围；
2. 用 `find` 从长录音中取出干净片段；
3. 用 `describe`、`realness` 与客观测量做准入检查；
4. 混音后生成 `timeline` 与 `sheet`；
5. 根据 cue 检查声画同步，用 `ab` 验证修改；
6. 用项目自己的参考影片建立 `profile`，而不是盲从内置七支片；
7. 最终仍由人试听审美、叙事和品牌感受。

仓库内的 `real-sound` skill 已经把这条链扩展成更完整的音轨制作流程：授权清单、设计 JSON、确定性 mixer、stems、响度与同步 QA、credits 和 mux。换句话说，earshot 本体是“耳朵和仪表”，skill 才是把它组织进生产的 SOP。

## 结论

earshot 的价值不在于宣称 AI 终于像人一样听见声音。它做了一件更工程化、也更可信的事：把音频转换成 Agent 能保存、比较、引用和触发返工的证据。

对于单个音效，它能描述、检索、裁切和比较；对于整支影片，它能生成事件时间轴、声画同步和分析图；对于程序化声音，它还能把合成参数放进一个“生成-评分-变异-复测”的循环。CLI、Python API、MCP 与 skill 又让这些能力可以进入 Coding Agent 的长任务，而不是停留在独立音频 App。

但“可测量”不等于“有品位”，“像真实”不等于“来源真实”，“通过自身 critic”也不等于“人类喜欢”。如果把 earshot 当作自动艺术总监，它会过度承诺；如果把它当作声音生产的测试框架与证据层，它提供了一块目前非常稀缺的基础设施。

## 参考资料

- [donghaozhang/earshot - user-provided fork](https://github.com/donghaozhang/earshot)
- [Leonxlnx/earshot - upstream](https://github.com/Leonxlnx/earshot)
- [v0.1.0 release and launch film](https://github.com/Leonxlnx/earshot/releases/tag/v0.1.0)
- [Validation report](https://github.com/Leonxlnx/earshot/blob/108763c62648c78dbac14f5bebcd3c61ac7931cd/docs/VALIDATION.md)
- [Documented limits](https://github.com/Leonxlnx/earshot/blob/108763c62648c78dbac14f5bebcd3c61ac7931cd/docs/LIMITS.md)
- [Design notes](https://github.com/Leonxlnx/earshot/blob/108763c62648c78dbac14f5bebcd3c61ac7931cd/docs/DESIGN.md)
- [MCP server implementation](https://github.com/Leonxlnx/earshot/blob/108763c62648c78dbac14f5bebcd3c61ac7931cd/earshot/mcp_server.py)
- [Forge search implementation](https://github.com/Leonxlnx/earshot/blob/108763c62648c78dbac14f5bebcd3c61ac7931cd/earshot/forge/search.py)

*本文审计于 2026-10-17，源码快照为 `108763c62648c78dbac14f5bebcd3c61ac7931cd`。用户提供的 fork 与上游在当时完全一致。发布影片已验证为 22 秒、1920x1080、H.264/AAC；两张配图来自仓库 `docs/media/`。本次完成静态语法检查，没有安装完整模型依赖或复跑受许可数据约束的 benchmark。*
