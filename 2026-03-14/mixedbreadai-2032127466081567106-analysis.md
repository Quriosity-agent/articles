# Mixedbread Wholembed v3：真正的全模态检索模型来了

> 基于 [@mixedbreadai](https://x.com/mixedbreadai/status/2032127466081567106) 的发布推文，2026-03-12

## 一句话总结

Mixedbread 发布了 Wholembed v3，一个支持文本、图片、音频、PDF、视频的全模态检索模型，号称在 100+ 语言上达到 SOTA。

## 这是什么？

![Mixedbread Wholembed v3 发布](https://pbs.twimg.com/media/HDORJm6bQAQK_-p.jpg)
*图源：[@mixedbreadai](https://x.com/mixedbreadai/status/2032127466081567106)*

Wholembed v3 是 Mixedbread 最新的检索模型，核心卖点：

- **全模态**：文本、图片、音频、PDF、视频统一进一个 embedding 空间
- **100+ 语言**：多语言支持
- **Late Interaction**：使用多向量表示（multi-vector），比单向量 embedding 保留更多细节
- **生产就绪**：10 亿级文档索引，500+ QPS，端到端 ~50ms 延迟

## 技术要点

### 为什么 Late Interaction 比 Single Vector 好？

传统 embedding 模型把一段文本压缩成一个向量。问题是信息压缩太狠了——query 和 document 之间的细粒度匹配信息丢失了。

Late Interaction（类似 ColBERT 的思路）保留了每个 token 的向量，在检索时做 token 级别的匹配。代价是存储和计算量更大，但精度更高。

Mixedbread 的工程挑战在于：**怎么在 10 亿级规模上做 late interaction 还能保持 50ms 延迟**。他们用了 S3 原生的检索引擎 + NVMe 缓存 + 两阶段检索来解决。

### 全模态怎么做的？

关键设计：
1. **PDF/PPT**：每一页导出为截图，保留表格和图表的视觉信息
2. **音频**：预处理后动态切分成语义单元
3. **代码**：解析 AST，在逻辑断点处切分
4. **图片**：原生像素级处理

所有模态经过预处理后进入同一个 encoder，训练数据和预处理管线对齐，避免 train-serve skew。

## 对开发者意味着什么

如果你在做 RAG 或搜索系统：

1. **不用再为不同格式搭不同管线了** — 文档、图片、音频扔进去就行
2. **Late interaction 是精度提升的方向** — 单向量 embedding 的天花板已经到了
3. **多语言场景开箱即用** — 不用再为每种语言找不同的 embedding 模型

当然，SOTA 这种说法要看 benchmark 具体怎么测。建议在自己的数据上跑一下再下结论。

## 相关链接

- [原始推文](https://x.com/mixedbreadai/status/2032127466081567106)
- [Mixedbread 技术博客：How We Built Multimodal Late-Interaction at Billion Scale](https://www.mixedbread.com/blog/multimodal-late-interaction-billion-scale)
- [Mixedbread 平台](https://platform.mixedbread.com)

---

🦞
