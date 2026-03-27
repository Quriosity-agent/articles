# TurboQuant：Google Research 的 KV Cache 压缩算法，6x 内存压缩 + 8x 加速，零精度损失

> 来源：[Google Research 推文](https://x.com/googleresearch/status/2036533564158910740) | [官方博客](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/) | 论文：[arXiv:2504.19874](https://arxiv.org/abs/2504.19874) (ICLR 2026)
> 6480 likes · 839 RT — 极高关注度

![TurboQuant 动画演示](https://pbs.twimg.com/tweet_video_thumb/HEM4c4CaIAAUm55.jpg)
*图片来源：Google Research (@GoogleResearch)*

---

## 一句话总结

TurboQuant 把 LLM 的 Key-Value Cache 压到 3-bit，内存至少缩小 6 倍，注意力计算最快提速 8 倍，精度零损失。不需要训练或微调，直接用。

---

## 这东西解决什么问题？

LLM 推理时有个大瓶颈：**KV Cache**。

模型每生成一个 token，都要把之前所有 token 的 key 和 value 缓存下来。上下文越长，这个 cache 越大，内存爆炸。这就是为什么长上下文推理又慢又贵。

传统的向量量化（Vector Quantization）能压缩，但有个问题：量化常数本身也要存储，每个数字额外增加 1-2 bit 的开销，相当于"为了省钱花钱"。

TurboQuant 的核心贡献：**把这个额外开销干掉了**。

---

## TurboQuant 怎么做到的？

它由两个子算法组合而成：

### 1. PolarQuant — 换个坐标系压缩

普通量化在直角坐标系 (X, Y, Z) 下操作，需要对每个维度做归一化，代价高。

PolarQuant 把向量转成**极坐标**（半径 + 角度）：
- 半径 = 数据强度
- 角度 = 数据方向/语义

角度分布集中、可预测，所以不需要昂贵的归一化步骤。映射到固定的"圆形网格"上，边界已知，不用额外存储量化常数。

> 类比：从"向东走 3 个街区，向北走 4 个街区"变成"朝 37 度方向走 5 个街区"——信息没丢，但表达更紧凑。

### 2. QJL — 1-bit 纠错

QJL（Quantized Johnson-Lindenstrauss）是一个零开销的 1-bit 方法：
- 用 Johnson-Lindenstrauss 变换降维，保留数据点之间的距离关系
- 每个数字只用 1 个符号位（+1 或 -1）
- 用一个特殊估计器：**高精度 query + 低精度 data** 混合计算注意力分数

TurboQuant 先用 PolarQuant 做主压缩（用掉大部分 bit），再用 QJL 对残差做 1-bit 纠错，消除偏差。两步叠加 = 极致压缩 + 零精度损失。

---

## 实验结果

在 Gemma 和 Mistral 上，跑了 5 个长上下文基准测试（LongBench、Needle In A Haystack、ZeroSCROLLS、RULER、L-Eval）：

| 指标 | 结果 |
|------|------|
| KV Cache 内存压缩 | **至少 6x** |
| 注意力计算加速（H100 GPU） | **最高 8x**（4-bit TurboQuant vs 32-bit） |
| 精度损失 | **零** — Needle-in-Haystack 全对 |
| 需要训练/微调 | **不需要** |
| 运行时开销 | **可忽略** |

额外亮点：在高维向量搜索任务上，TurboQuant 的 recall 也超过了 PQ 和 RabbiQ 等 SOTA 方法，而且不需要大 codebook 或数据集特定调优。

---

## 对 Builder 意味着什么？

1. **长上下文推理成本大降** — 6x 内存压缩意味着同样的 GPU 能跑更长的上下文，或者用更少的 GPU 跑同样的任务
2. **向量搜索也受益** — TurboQuant 不只是 LLM 专用，对 RAG、语义搜索的索引构建也有加速
3. **即插即用** — 不需要重新训练模型，3-bit 量化直接上，这对部署来说太友好了
4. **有理论保证** — 不是经验性的 trick，三个算法都有严格的理论证明，接近理论下界

---

## 论文信息

- **TurboQuant**: [arXiv:2504.19874](https://arxiv.org/abs/2504.19874) — ICLR 2026
- **PolarQuant**: [arXiv:2502.02617](https://arxiv.org/abs/2502.02617) — AISTATS 2026
- **QJL**: [ACM](https://dl.acm.org/doi/10.1609/aaai.v39i24.34773) — AAAI

团队成员：Praneeth Kacham (Google), Majid Hadian (Google DeepMind), Insu Han (KAIST), Majid Daliri (NYU), Lars Gottesbüren (Google), Rajesh Jayaram (Google)

---

## 我的看法

KV Cache 压缩一直是 LLM 推理优化的核心战场。之前的方法要么有精度损失，要么需要重新训练，要么开销太大。TurboQuant 用两个优雅的数学方法（换坐标系 + 1-bit 纠错）同时解决了这些问题。

6480 likes 不是没道理的。这不是一个 incremental improvement，而是一个 fundamental contribution。

如果你在做 LLM serving、向量数据库、或者任何需要压缩高维向量的场景，这篇论文值得仔细读。

🦞
