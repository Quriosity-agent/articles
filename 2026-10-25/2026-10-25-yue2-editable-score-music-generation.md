---
title: "YuE 已更新到 YuE2：先写可编辑乐谱，再生成完整歌曲"
date: 2026-10-25
source: "https://github.com/multimodal-art-projection/YuE"
tags:
  - YuE
  - YuE2
  - Music Generation
  - Symbolic Planning
  - ABC Notation
  - Agentic Editing
  - SheetSage2
  - Open Weights
---

# YuE 已更新到 YuE2：先写可编辑乐谱，再生成完整歌曲

生成一首歌之后，最难表达的要求往往不是“再来一首”，而是“旋律别动，把和弦换一下”。如果唯一的交互入口是文字描述，这两种要求很容易落到同一种操作：重新抽取一个结果。

YuE2 提供了另一种控制入口：**把旋律和和弦变成可读取、可修改的乐谱计划，再将计划生成带人声与伴奏的完整录音。** 它既有音乐生成模型，也有供外部 Agent 调用的工具；不是只有一份提示词或 Skill。

![YuE2 官方演示中的乐谱与歌曲界面](imgs/yue2-editable-score-music-generation/official-score-demo.webp)

*2026 年 10 月 25 日实际打开官方演示页后的截图，展示生成歌曲、符号乐谱、歌词与风格信息。本文没有播放音频，也没有生成截图中的作品。*

## 先认清版本：同一个地址，现在主要讲 YuE2

本文核查的是仓库 `main` 的固定提交 [`1647252`](https://github.com/multimodal-art-projection/YuE/tree/1647252d68b70cbead046ffd3f7caf036dde47ee)，提交日期为 2026 年 10 月 6 日；文章日期是本次审阅日期，不是发布日。

原版 YuE 于 2025 年发布，其代码、文档和许可保留在 [`YuE-v1` 分支](https://github.com/multimodal-art-projection/YuE/tree/YuE-v1)。当前主分支是 2026 年 9 月发布的 YuE2 系列，不能把旧版的阶段模型、显存建议和 Apache 许可说明直接套给新权重。[当前 README](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/README.md)

最容易混淆的三个对象是：

| 对象 | 做什么 |
|---|---|
| YuE2-3B 与 VAE | 生成乐谱计划、音乐表示与音频 |
| SheetSage2 | 把已有录音转成可检查的谱面，用于翻唱和编辑入口 |
| `yue2-music` Skill 与辅助脚本 | 帮外部 Agent 调用模型、修改 ABC、检查约束和整理版本 |

模型名带有 `3B`，官方架构说明给出的参数量约为 3.58B。它不是让通用语言 Agent 仅靠写代码就凭空得到同等歌声；实际声音仍由音乐模型合成。[模型卡](https://huggingface.co/m-a-p/YuE2-3B)、[官方架构说明](https://map-yue2.github.io/#model-overview)

## 乐谱不是装饰，而是生成链条里的中间产物

YuE2 的默认流程可以理解为：

```text
歌词 + 风格要求
    → 旋律与和弦计划（ABC 文本记谱）
    → 音乐语义 Token
    → 声学潜变量
    → VAE 解码
    → 48 kHz 立体声音频
```

![YuE2 官方符号与音频统一架构](imgs/yue2-editable-score-music-generation/architecture.png)

*原仓库架构图：上方是乐谱到声音的生成路径，下方是训练监督来源。它不是本文绘制或测得的运行轨迹。*

技术报告将核心描述为统一的 AR–NAR Mixture-of-Transformers：自回归部分预测谱面和语义 Token，非自回归部分通过 flow matching 生成声学潜变量，再解码成声音。API 相应拆为 `plan()`、`generate_semantic()`、`synthesize()` 和 `decode()`。[技术报告](https://arxiv.org/abs/2609.33757)、[生成接口](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/generation.md)

ABC 是能以文本表示音符、节奏、调号等信息的记谱方式。这里的可编辑计划并不等于一份包含所有音轨、音色插件和自动化曲线的 DAW 工程；它暴露的是作曲层面的控制，而不是把整首录音的每个声音都变成独立可编辑素材。

## 三种模式，分别决定固定多少作曲内容

| 配置 | 控制方式 | 适用思路 |
|---|---|---|
| `cot="full"` | 旋律与和弦计划 | 想同时约束旋律和和声 |
| `cot="melody"` | 旋律计划 | 保留曲调，让伴奏有更多风格变化空间 |
| `cot="off"` | 不生成符号计划 | 直接从歌词和风格生成 |

用户也可以通过 `abc` 提供自己的谱面，搭配 `full` 或 `melody`。但任意 ABC 文件不保证原样兼容：项目辅助工具只检查有限的原生记谱子集。`melody` 模式也不是一个自动删和弦的按钮，输入应先准备成不带和弦符号的合适谱面。[生成指南](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/generation.md)、[翻唱指南](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/covers.md)

这让“保留什么、允许改变什么”比一句“爵士一点”更明确。不过，谱面写对不代表模型一定逐音准确演绎，结果仍需听音核对。

## Agent 改谱，YuE2 重新演绎：这是两种能力

外部 Agent 可以接收“旋律不动，只改和声”的要求，修改 ABC 中的和弦符号，运行辅助检查，然后让 YuE2 生成新版本。项目附带的示例将普通和弦换成七和弦，同时保留旋律、节奏、拍号与速度。[编辑指南](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/editing.md)

本次实际运行了它的符号比较命令：

```bash
python3 skills/yue2-music/scripts/abc_tools.py compare \
  examples/score.abc examples/score-jazz.abc
```

结果为 `match: true`，比较了 `Vocal` 与 `Ins` 声部。这个结果刻意允许和声变化，证明的是所检查的旋律与节拍信息保持一致，**不证明生成音频的和弦准确、歌声相同或听感更好**。

![YuE2 官方多轮 Agent 编辑案例](imgs/yue2-editable-score-music-generation/official-agent-editing-demo.webp)

*官方《The Last Train》案例页面，展示作者整理的 9 步、14 个版本编辑过程。这是上游示例，不是本文复现的多轮任务。*

最重要的限制是：**编辑会生成新的整首录音，不是只替换指定几秒并锁住其余波形。** 即使未改音符保持一致，演唱、音色和其他声音细节仍可能改变。把它当作可控重演绎更准确，而不是 DAW 级的无损局部修改。

## 翻唱和纯音乐各有额外步骤

翻唱流程并不是把一段录音直接塞进当前生成 API 就结束：先用 SheetSage2 转谱，核查旋律和歌词，再将谱面、歌词与目标风格交给 YuE2。官方建议转谱与生成使用独立依赖环境；SheetSage2 会加载所需的 MERT2 编码器，普通 YuE2 文本生成则不要求额外下载一套独立 MERT2 特征提取模型。[翻唱文档](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/covers.md)

这里的 zero-shot 指使用通用生成检查点，不为翻唱任务再做专门微调；不意味着没有转谱误差，也不等于精确复制原唱音色。

配套纯音乐流程默认仍由 YuE2 写谱，再把 `Vocal` 旋律转移到 `Ins` 声部后生成。Agent 负责调用和转换，而不是默认代替模型作曲。辅助文档也明确提示：音频时长可能不等于谱面时长，纯音乐仍要检查人声泄漏与跟谱程度。[纯音乐流程](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/skills/yue2-music/instrumental/README.md)

## 怎样读它与 Suno 的对比

官方 WildSongBench 的 2026 年 9 月 12 日比较包含 192 个提示、17 种系统设置。下表仅摘出 SongBench Avg，不能代表所有维度或所有听众的偏好。

| 设置 | 官方 SongBench Avg，越高越好 |
|---|---:|
| YuE2 best-of-8 | 6.9632 |
| Suno v5 | 6.8721 |
| YuE2 标准评测设置 | 6.7316 |
| Suno v6 | 6.5562 |

![YuE2 官方质量与文本匹配度概览](imgs/yue2-editable-score-music-generation/official-benchmark-overview.png)

*作者报告的比较图。横纵轴是归一化综合指标，不是成功率；气泡面积表示 AudioBox PQ。Bo8 是八候选筛选，不是单次生成。*

读分数时要保留这些条件：标准 YuE2 从两个候选中按较低 PER 选取；best-of-8 从八个候选中按音乐性、提示控制等规则选择，且涉及 SongBench 的一个维度。不同系统的候选预算并非完全一致，一次 API 调用只生成一个候选。

此外，报告使用 `YuE2-Vae-legacy` 解码器，日常默认听音是 `YuE2-Vae`。其他系统在部分指标上领先，较小的均值差距不构成统计显著性结论。本文没有复现这套评测，也不据此宣称“全面超过 Suno”。[完整分数与协议](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/benchmarks.md)

## 部署与许可：开放权重不等于没有门槛

当前仓库文档推荐 Linux、Python 3.12、支持 BF16 的 NVIDIA 24 GB 显卡作为生成起点。Hugging Face 较早的 wheel 示例和仓库源码的安装说明存在版本差异，使用时应固定同一套代码、依赖、模型与 VAE 版本。

源码确实包含 `mps` 与 CPU 的自动设备选择分支，但本次没有在 Apple Silicon 上跑模型，不能据此保证 Mac mini 能以可接受速度完成整首生成。24 GB 显存建议也不能直接当成 24 GB Mac 统一内存的等价承诺。[生成要求](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/generation.md)、[设备选择代码](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/src/yue2/pipeline.py)

许可同样要分层看：仓库主要代码是 Apache 2.0；YuE2 模型权重是 **CC BY-NC 4.0，加个人创作者额外许可**。该额外许可允许符合条件的个人创作者使用模型并变现输出，但不自动授权公司的商业权重使用；公司需向作者咨询商业许可。部分附带组件另有自身许可，不能用仓库徽章替代具体条款。翻唱素材、歌词和声音等第三方权利也不因模型许可而自动取得。[权重完整条款](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/MODEL_LICENSE)、[第三方说明](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/THIRD_PARTY_NOTICES.md)

## 本次验证与实际使用价值

在临时克隆中，本次运行 5 个 `test_skill_*.py` 文件中的 **35 项测试，全部通过**，并完成上述两个示例谱的比较。范围涉及 ABC 解析、约束检查、请求处理、模拟转谱接口、试听页与分发包检查，不涉及真实模型推理。没有安装推理依赖、下载模型权重、安装 Skill、调用付费服务或试听官方歌曲。

若要评估它是否适合实际制作，最有辨识度的实验不是再生成一批随机歌曲，而是保存一版自己有权使用的旋律，仅修改和声后重新生成，分别检查“谱有没有按要求改”和“声音有没有忠实实现”。保存 `save_artifacts()` 输出，查看 `truncated` 标志，不要把文件可播放当成歌曲已完整生成。[产物记录说明](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/generation.md)

**YuE2 最值得关注的是多了一层可以检查与编辑的作曲表示，而不只是多了一句能让 Agent 调用音乐模型的提示词。** 它让修改要求有了明确落点，但谱面保真、声音质量、演唱表现和最终可用性仍需逐项验收。

来源、媒体归属与测试命令见 [SOURCES.md](imgs/yue2-editable-score-music-generation/SOURCES.md)。
