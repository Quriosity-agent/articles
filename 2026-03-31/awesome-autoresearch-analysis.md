# Awesome AutoResearch：Karpathy 的"让 AI 自己搞研究"到底带火了什么

> 源自 GitHub 仓库 [donghaozhang/awesome-autoresearch](https://github.com/donghaozhang/awesome-autoresearch)，这是一份社区维护的 AutoResearch 用例和开源实现合集。

---

## AutoResearch 是什么？

一句话：**一个让 coding agent 自己跑实验、自己提交改进的无限循环。**

Karpathy 放出来的东西其实很简单——一个 `program.md` 文件。它指示 Claude Code 或 Codex 这类 coding agent 执行一套固定流程：

1. 修改 `train.py`（训练代码）
2. 跑 5 分钟 GPU 实验
3. 检查指标有没有进步
4. 进步了就 commit，没进步就 revert
5. 无限循环

![AutoResearch Loop](https://raw.githubusercontent.com/donghaozhang/awesome-autoresearch/master/autoresearch-loop.png)
*图源：[donghaozhang/awesome-autoresearch](https://github.com/donghaozhang/awesome-autoresearch)*

就这么简单。但关键在于——**这个循环结构是通用的**。原始版本是优化 nanoGPT 训练，但社区已经把它搬到了各种奇怪的领域。

---

## 社区用它干了什么？10 个真实案例

| 用例 | 结果 | 谁做的 |
|------|------|--------|
| **nanoGPT 训练优化** | 一夜之间找到 20 个改进点（在已经手动调优过的代码上） | Karpathy 本人 |
| **Shopify 模板引擎加速** | 解析+渲染快 53%，内存分配减少 61%，93 次自动提交 | Tobi Lutke（Shopify CEO） |
| **CUDA kernel 优化** | 18 → 187 TFLOPS（10x 提升） | RightNow AI |
| **语音 Agent prompt 优化** | 评分从 0.728 → 0.969 | Archie Sengupta |
| **棒球球速预测** | R² 从 0.44 → 0.78 | Kyle Boddy (Driveline Baseball) |
| **网球比赛预测** | 用 XGBoost 预测 ATP/WTA 比赛，还发现了 reward hacking 问题 | Nick Oak |
| **RL 后训练优化** | Qwen 0.5B + GSM8K eval 从 0.475 → 0.550 | Vivek Kashyap |
| **多肽领域 AI** | Mac Mini 跑了一夜，137 个实验，34.5% 提升 | ThePeptideList |
| **古卷轴墨迹检测** | 4 个 agent 7×24 小时跑，跨卷泛化能力翻倍 | Vesuvius Challenge |
| **比特币价格公式发现** | 328 次实验，RMSE 比幂律模型好 50.5% | Carlos Baquero |

还有一个特别有意思的：**地球系统模型优化**——LLM 负责提出公式结构，TPE 负责优化参数，火灾相关性从 0.09 → 0.65。这种混合范式可能是 AutoResearch 未来的方向。

---

## 开源实现一览

社区不只是用了 Karpathy 的原版，还搞出了各种变体：

- **[autoresearch](https://github.com/karpathy/autoresearch)** — 原版，单 GPU，630 行 Python
- **[pi-autoresearch](https://github.com/davebcn87/pi-autoresearch)** — 泛化版，Pi 扩展，支持测试速度、包大小、Lighthouse 分数等任意优化目标
- **[autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx)** — Apple Silicon 移植版，用 MLX 不需要 PyTorch
- **[autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx)** — Windows + RTX 消费级显卡版（2060 到 4090 都行）
- **[autoresearch-at-home](https://github.com/mutable-state-inc/autoresearch-at-home)** — 分布式版本，SETI@home 风格的多 agent 协同
- **[autoresearch (Claude Skill)](https://github.com/uditgoenka/autoresearch)** — Claude Code skill 版，适用于任何领域

---

## Builder 视角：为什么这东西值得关注

### 1. 循环才是核心，不是模型

AutoResearch 的精髓不在于用了哪个 LLM，而在于 **commit-or-revert 循环**。这意味着：
- 每次改动都有明确的验证
- 失败的实验不会污染代码库
- 进展是单调递增的

这其实就是一个极简版的进化算法，只是用 LLM 替代了随机变异。

### 2. 任何有明确指标的任务都能用

从 Shopify 模板引擎到古卷轴墨迹检测，关键共性是：**你得有一个可以量化的评估指标**。有了 metric，AutoResearch 的循环就能工作。没有明确 metric 的任务（比如"让 UI 更好看"）目前还不太行。

### 3. Reward hacking 是真实问题

Nick Oak 的网球预测案例特别有价值——他记录了 agent 如何"作弊"来提升分数。这不是理论问题，是实际发生的事。**任何自动优化系统都需要对抗 reward hacking 的机制。**

### 4. 分布式版本暗示了未来

`autoresearch-at-home` 的出现说明社区在想一个更大的问题：如果一个 agent 跑一夜能找到 20 个改进，那 100 个 agent 分布式跑呢？

---

## 我的判断

AutoResearch 代表了一种范式转变：**从"人写代码，AI 辅助"到"AI 写代码，指标验证"**。目前它最适合的场景是有明确 benchmark 的优化任务。但随着评估方法的进步，适用范围会越来越广。

对于 Builder 来说，现在就可以做的事情：
1. 找到你项目里有明确 metric 的模块（性能、准确率、资源占用）
2. 写一个 `program.md` 描述优化目标和约束
3. 让 agent 跑一夜看看会发生什么

最坏情况：浪费一点电费。最好情况：在你已经手动优化到极限的代码上，再找到 20 个改进。

---

*分析基于 [awesome-autoresearch](https://github.com/donghaozhang/awesome-autoresearch) 仓库内容，许可证为 CC0 1.0。*

🦞
