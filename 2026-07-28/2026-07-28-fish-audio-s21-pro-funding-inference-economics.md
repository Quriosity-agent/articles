---
title: "Fish Audio S2.1 Pro 深度拆解：5200 万美元融资背后，TTS 正在变成推理基础设施生意"
date: 2026-07-28
source: "https://x.com/FishAudio/status/2082152596739862853"
canonical: "https://fish.audio/blog/fish-audio-52m-seed-funding/"
related_sources:
  - "https://fish.audio/blog/tts-inference-optimization-s2-pro-free/"
  - "https://fish.audio/blog/s2-1-pro-free-api/"
  - "https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits"
  - "https://docs.fish.audio/features/voice-cloning"
  - "https://github.com/fishaudio/fish-scales-ops"
  - "https://arxiv.org/abs/2603.08823"
tags:
  - Fish Audio
  - S2.1 Pro
  - Text to Speech
  - Voice Cloning
  - Voice Agent
  - Inference Infrastructure
  - Startup Funding
  - FP8
---

# Fish Audio S2.1 Pro 深度拆解：5200 万美元融资背后，TTS 正在变成推理基础设施生意

> **TL;DR：** Fish Audio 在 2026 年 7 月 28 日的 X 帖子中同时宣布 5200 万美元 Seed 融资和 S2.1 Pro 的 public launch。官方给出的增长数据是：22 人团队、2100 万美元 ARR、800 万以上用户、200 万以上社区声音模型，企业贡献约三分之二收入。产品侧的卖点包括 5 秒参考音频克隆、83 种语言、逐词情绪/语调/节奏控制，以及约 70–90ms 首包延迟。真正值得研究的不是“声音又自然了一点”，而是 Fish Audio 把价格战做进了推理栈：FP8 内核、DualAR-aware continuous batching、GPU 混部、自有 500 卡集群、网络和存储，使官方声称同等负载从 4 张 H200 降到 1 张。需要注意：速度、质量和竞品对比主要来自 Fish Audio 自测；“ElevenLabs 六分之一成本”只在特定模型和英文字符计费口径下接近成立；免费 API 目前到 8 月 31 日，没有 SLA，可能保留请求用于模型改进。S2 是开放权重，S2.1 Pro 则是商业 API，不能把“免费”误写成“开源”。

- **发布帖：** [Fish Audio on X](https://x.com/FishAudio/status/2082152596739862853)
- **融资文章：** [5 Models, 22 People, 1 Year](https://fish.audio/blog/fish-audio-52m-seed-funding/)
- **推理工程：** [How We Made Our Text-to-Speech API Free](https://fish.audio/blog/tts-inference-optimization-s2-pro-free/)
- **免费 API：** [S2.1 Pro Free API](https://fish.audio/blog/s2-1-pro-free-api/)
- **发布日期：** 2026-07-28（X 帖子；融资文章发布于 7 月 27 日）
- **访问与价格核验时间：** 2026-07-29

## 一句话判断

**Fish Audio 这次发布的核心不是一张“更强 TTS”成绩单，而是一套垂直整合策略：用表达力赢得产品，用推理效率打价格，用自有基础设施守住毛利，再用融资把 API 变成企业语音层。**

![Fish Audio announces a $52M seed round](imgs/fish-audio-s21-pro-funding-inference/01-funding-announcement.png)

*图：Fish Audio 官方融资封面。公司把 5200 万美元 Seed、800 万以上 builders 和成立一周年放在同一叙事里。来源：Fish Audio。*

## 1. 这次到底发布了什么

X 帖子把三件事压在了一起：

1. Fish Audio 完成 **5200 万美元 Seed 融资**；
2. S2.1 Pro 进行正式 public launch；
3. 通过一个月免费、迁移优惠和企业成本承诺拉新。

融资由 Coreline Ventures 和 Capital Today 领投，359 Capital、Play Time、HF0、645 Ventures、Parable、Carya Venture Partners、Alphalist Partners 等参与。官方没有披露估值或股权比例。

“public launch”不能理解为 S2.1 Pro 在 7 月 28 日才第一次可用。Fish Audio 已在 6 月 23 日发布 `s2.1-pro-free` API，7 月 23 日又公开推理工程文章。7 月 28 日更像是融资新闻、产品成熟度和企业定位合并后的正式市场发布。

![Contact sheet from the Fish Audio S2.1 Pro launch video](imgs/fish-audio-s21-pro-funding-inference/02-launch-video-contact-sheet.jpg)

*图：发布视频帧。视频依次展示实时声音克隆、竞品图表、语音 Agent 订餐演示、企业客户和一个月免费活动。本文保留画面作为发布证据，不把演示音频当作独立质量评测。来源：Fish Audio X 视频。*

## 2. 5200 万美元买的不是一次训练，而是完整语音栈

Fish Audio 自报的一周年数据相当激进：

| 指标 | 官方披露 |
|---|---:|
| 团队 | 22 人 |
| 年度经常性收入 | 2100 万美元 ARR |
| 平台用户 | 800 万以上 |
| 社区声音模型 | 200 万以上 |
| 收入结构 | 企业约占三分之二 |
| 已发布模型 | 4 个 TTS、1 个 STT |

这些数字未经第三方审计，应视为公司披露，而不是财务核验结果。但它们解释了为什么这一轮资金会投向基础设施，而不是只扩大研究团队。

Fish Audio 已经在经营约 500 张 GPU 的多数据中心集群，自建 ASN 和 300Gbps 网络、Cloudflare peering，以及 NVMe、混合存储和自托管 Ceph 组成的分层存储。未来计划还包括 Audio Understanding Language Model、speech-to-speech、开发者工具、API 和企业销售。

这是一条重资产路线。它押注的是：当 TTS 进入 HeyGen、LiveKit、Retell、Sanas、OpenArt 等生产链路，模型质量只是入场券，长期竞争会转向延迟、吞吐、稳定性、合规部署和单位经济。

## 3. S2.1 Pro 的产品变化：从“朗读”转向“表演”

S2.1 Pro 延续 S2 的核心方向：不是只把文字念对，而是让用户控制文字怎样被说出来。

官方能力包括：

- 83 种语言由同一个模型处理；
- 逐词插入自然语言控制标签；
- 控制情绪、语调、节奏、停顿和副语言事件；
- instant clone 与 persistent clone；
- 多说话人、多轮生成；
- 普通 API 与实时流式端点；
- 通过 `reference_id` 在后续生成中复用声音身份。

融资文章称其支持 15,000 种以上自然语言控制。这里更合理的理解是可组合的控制表达空间，而不是 15,000 个经过逐项验收的固定按钮。

“5 秒克隆”也需要拆开看。发布帖证明系统可以从约 5 秒参考音频启动克隆；官方工程文档的质量建议则是：至少约 10 秒，干净、单人、单声道；一分钟或两分钟清晰语音会进一步提高保真度。**能生成**和**适合生产**不是同一个门槛。

## 4. 免费 API 不是补贴故事，而是推理效率故事

Fish Audio 对 S2.1 Pro 的定价解释非常直接：自回归 TTS 每一步都是小矩阵运算，还要反复读取 KV cache；在低并发下，昂贵 GPU 可能只在 10–20 微秒的短突发中工作，其余时间花在调度和内存等待上。

它的优化不是一个 kernel，而是五层叠加：

![Fish Audio end-to-end inference optimization stack](imgs/fish-audio-s21-pro-funding-inference/03-inference-stack.png)

*图：Fish Audio 公布的端到端推理栈。continuous batching、FP8 内核、K8s/Slurm 混部、自有硬件、网络和存储共同构成成本优势。图中数字均为公司自测。来源：Fish Audio。*

### Serving 层

基于 SGLang 思路做 continuous batching：短请求完成后，新请求立即进入活动 decode batch，不必等待最长输出结束。S2.1 Pro 的 DualAR 还要求 scheduler 正确维护 coarse/fine codebook 和 `previous_tokens` 滑动窗口，否则吞吐正常，声音却可能发生身份漂移。

### Compute 层

开源 `fish-scales-ops` 针对 TTS 常见的 `M ≤ 128` decode shape，提供 H200/Hopper 的 block-scaled FP8 GEMM，以及 Blackwell/RTX 5090/RTX 6000 Pro 的 MXFP8 与 FlashAttention。官方称相对 `torch.compile` 融合后的 cuBLAS，在相关 decode shape 上快 2.1–4.3 倍。

### Scheduling 层

Kubernetes 服务推理，Slurm 服务训练；可抢占的数据清洗任务填补空闲 GPU。官方称整体利用率从约 50% 提升到 90% 以上。

### Hardware 与 Infrastructure 层

H200 承担高并发，RTX 5090/6000 Pro 承担部分边缘端点；自有网络降低云出口费用，自托管存储避免长期训练数据持续支付对象存储溢价。

公司最终把这些收益汇总为：过去需要 4 张 H200 的请求量，现在 1 张可以承载。这个“4×”是整套系统的合并结果，不能与单个 kernel 的 4.3× 直接相乘。

## 5. 8,006 tok/s 的意义，不是单个用户听到 52 倍速度

H200、bsgemm FP8 的官方并发测试如下：

| 并发 | 总吞吐 | TTFB p50 |
|---:|---:|---:|
| 1 | 154 tok/s | 73.2ms |
| 8 | 1,206 tok/s | 81.2ms |
| 32 | 4,099 tok/s | 96.9ms |
| 64 | 8,006 tok/s | 109.8ms |
| 512 | 19,517 tok/s | 525.1ms |

![Fish Audio S2.1 Pro throughput and latency under concurrency](imgs/fish-audio-s21-pro-funding-inference/04-throughput-latency.jpg)

*图：并发提高时，总吞吐从 154 tok/s 增长到 19,517 tok/s，p50 首包时间也从约 73ms 增长到 525ms。来源：Fish Audio 内部 H200 benchmark。*

Fish 所说的 52×，是 `c=1 → c=64` 的**总吞吐扩展**，不是单个请求快了 52 倍。在 c=64 时，p50 首包反而从 73.2ms 增到 109.8ms。对 API 公司而言，这个交换很划算：每张卡同时服务更多客户，单请求延迟只增加约 37ms。

对开发者而言，则要区分三件事：

- 模型 token 生成速度；
- 服务端 TTFB/TTFA；
- 用户端端到端延迟，包括连接、网络、音频缓冲和播放。

Fish 的文章也交替使用 TTFB 与 TTFA。实时端点还把 prefill 放在连接建立时完成，从“首个音频 chunk”开始计时。不同厂商如果选择不同计时起点，“2 倍更快”就未必是同一项指标。

## 6. 为什么“六分之一成本”大致成立，又为什么不能照抄

截至核验时，Fish Audio 付费 `s2.1-pro` 的公开价格是：

- **15 美元 / 100 万 UTF-8 bytes**；
- 官方换算约 18 万英文单词或 12 小时音频；
- 免费型号 `s2.1-pro-free` 为 0 美元，但受 Fair Use 和时间窗口约束。

ElevenLabs 当前公开 API 价是：

- Flash/Turbo：0.05 美元 / 1000 characters；
- Multilingual v2/v3：0.10 美元 / 1000 characters。

对英文来说，一个字符大致对应一个 UTF-8 byte，所以 Fish 的 15 美元 / 百万，约是 ElevenLabs Multilingual/v3 的 **6.7 分之一**，与发布帖的“六分之一”接近；相对 Flash/Turbo 则约为三分之一。

但 Fish 按 bytes 计费，ElevenLabs 按 characters 计费。常见汉字通常占 3 个 UTF-8 bytes，因此 1000 个汉字在 Fish 约为 0.045 美元，而不是 0.015 美元。此时相对 ElevenLabs 0.10 美元的倍率只有约 2.2 倍。语言、模型档位、长文本标点、套餐折扣和企业合同都会改变结果。

所以“六分之一”不是通用账单定律，而是**特定英文输入与竞品高质量模型的公开单价比较**。

## 7. 量化之后，最危险的不是慢，而是高速生成错误声音

FP8 可以降低带宽和显存压力，但 TTS 的量化错误未必表现为崩溃。Fish Audio 披露过一个 MXFP8 权重 stride bug：kernel 性能完全正常，logit 相对误差却达到约 53%，最终表现为重复 semantic token 和声音退化。

因此推理栈每次变更要同时通过两类门禁：

![Fish Audio inference correctness and performance gates](imgs/fish-audio-s21-pro-funding-inference/05-quality-gates.png)

*图：正确性门禁要求固定输入的前五个音频 frame 与 BF16 token-exact；性能门禁要求 c=1/16/64 的 decode throughput 不低于冻结基线 5% 以上。两者都通过才部署。来源：Fish Audio。*

这个设计很实用，但也有边界。前五帧 token-exact 擅长发现系统性 logit 损坏，不能单独证明长文本中的音色一致性、情绪控制和多语言发音完全不受影响。生产团队仍要补充长程 speaker similarity、WER/CER、主观听测和业务场景回归。

## 8. 质量 benchmark 有信息量，但不是独立第三方结论

Fish Audio 在 3 月 26 日到 4 月 5 日做过一次生产流量盲测：10 天内收集 71,000 组 paired groups，其中 5,098 组跨厂商对比满足筛选条件。用户必须至少各播放两次，并且只下载其中一个版本，下载版本被记为胜者。

其 S2 Pro 获得 3.07 Bradley-Terry 分数、65.7% 总胜率；对 ElevenLabs V3 的 581 组 head-to-head 中，Fish 为 60%、ElevenLabs 为 40%。这套测试比只听几条官方样音更接近真实使用，因为文本、语言和声音来自生产平台。

但它仍然由 Fish Audio 设计、集成、运行和分析：

- API 用户未纳入；
- 约 30% 是回访用户，可能熟悉 Fish 声音；
- 各厂商支持的标签不同，进入的请求子集也不同；
- 部分竞品样本量只有数百；
- 测试对象主要是 S2 Pro，不等同于对 S2.1 Pro 的独立评测。

因此，“最 expressive”与竞品胜率应写作官方自测结果。真正的采购评测仍应使用自己的语言、声音、文本长度和终端网络。

## 9. 免费的边界，比“0 美元”更重要

`s2.1-pro-free` 当前免费到 **2026 年 8 月 31 日**，没有硬性字符上限，但受 Fair Use Policy 约束。官方同时写明：

- 没有 SLA；
- 没有延迟保证；
- 请求可能被保留用于模型质量改进；
- 部分商业场景有限制；
- ARR 超过 100 万美元的产品应联系 Fish Audio；
- 需要生产 SLA、完整商业许可和 zero-data-retention 时应使用付费或企业方案。

发布帖所说的“一个月免费”和“无法降低 50% 成本就送一年”，也分别属于社交活动与企业销售承诺，不是公开 API 的永久合同条款。

声音克隆还需要独立处理权利问题。技术上 5–10 秒就能启动，并不意味着开发者有权复制任何人的声音。应保存被克隆者授权、用途范围、撤回机制和生成日志；品牌、客服、医疗与金融场景还需要把 disclosure、滥用检测和身份认证做进产品，而不是只依赖供应商。

## 10. 开源边界：S2、S2.1 Pro 与推理栈不是一回事

这一发布最容易出现三个概念混用：

| 项目 | 当前开放方式 |
|---|---|
| Fish Speech S2 | 代码与权重已公开 |
| S2.1 Pro | Fish Audio 商业 API；免费期不等于公开权重 |
| `fish-scales-ops` | FP8 GEMM / FlashAttention 内核开源 |
| 完整 production serving stack | 仅部分公开，更多组件处于计划或候选状态 |

如果团队需要本地部署、权重审计或私有微调，应评估 S2 开放权重路线；如果需要最低集成成本、83 语言和官方延迟优化，则评估 S2.1 Pro API。二者建立在相关技术基础上，但采购、许可证、数据治理和运维责任完全不同。

## 11. 团队应该怎样评估 S2.1 Pro

不要只复制官方 demo。用一份可重复的业务测试集：

1. **音色：** 不同参考长度下测 speaker similarity，至少覆盖 5 秒、10 秒和 60 秒。
2. **表达：** 对同一句话测试逐词情绪、节奏、停顿和重音是否真的可控。
3. **长程：** 检查 5、15、30 分钟输出中的音色漂移、漏字和重复。
4. **语言：** 分别评估中文、英文、日文及 code-switch，不要用“83 语言”替代逐语言验收。
5. **延迟：** 在目标地区测 p50/p95 首包和完整生成时间，包含真实网络与播放缓冲。
6. **吞吐：** 按业务请求长度测 concurrency，而不是直接套用 H200 tok/s。
7. **成本：** 按 UTF-8 bytes 重新计算自己的语料，加入重试、缓存和峰值并发。
8. **治理：** 明确数据保留、声音授权、模型删除、zero retention 和 SLA 条款。

免费期最适合做这套评估，而不是提前认定长期生产成本为零。

## 结论：语音模型竞争正在下沉到每一层成本

Fish Audio 的融资数字很亮眼，但更重要的是它展示了一种新的 TTS 公司形态：研究模型、开放基础模型、商业 API、CUDA kernel、scheduler、GPU 集群、网络和企业合规由同一团队向下贯通。

S2.1 Pro 的表达控制决定声音能否进入角色、内容和 Agent；70–90ms 首包决定对话能否自然；8,006 tok/s 决定一张 H200 能服务多少并发；按 UTF-8 bytes 的 15 美元单价决定客户是否愿意迁移；zero-data-retention、HIPAA 和 on-premise 决定企业采购能否通过。

这也是 5200 万美元 Seed 背后的真正命题：当模型能力逐渐接近，TTS 不再只是“谁的样音更像真人”，而是谁能用更低的系统成本，把可控声音稳定地送进每一次真实交互。
