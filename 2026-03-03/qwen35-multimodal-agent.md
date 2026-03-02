# Qwen3.5：阿里通义千问的原生多模态 Agent 模型 — 从 0.8B 到 397B 全尺寸覆盖

> **TL;DR**: 阿里云通义团队发布 Qwen3.5 — **原生多模态 Agent 模型系列**，从 0.8B 到 397B-A17B（MoE）共 8 个尺寸。核心突破：**统一视觉-语言基础**（早期融合训练）、**Gated Delta Networks + MoE 混合架构**（高吞吐低延迟）、**百万级 Agent 环境 RL 训练**、**201 种语言支持**。27B 密集模型在 SWE-Bench Verified 上达到 72.4%，追平 GPT-5 mini。全系列 **Apache 2.0 开源**。

---

## 📊 旗舰模型 Benchmark

![Qwen3.5-397B-A17B Benchmark](qwen35-benchmark.png)

*Qwen3.5-397B-A17B（MoE 旗舰）在各项基准测试中的表现。*

## 📊 中型模型 Benchmark

![Qwen3.5 中型模型](qwen35-middle.png)

*27B（密集）、35B-A3B（MoE）、122B-A10B（MoE）在各基准的表现。*

## 📊 小型模型 Benchmark

![Qwen3.5 小型模型](qwen35-small.png)

*0.8B、2B、4B、9B 小模型系列的基准表现。*

## 🏗️ 模型家族

| 模型 | 类型 | 总参数 | 激活参数 | 发布日期 |
|------|------|--------|---------|---------|
| Qwen3.5-397B-A17B | MoE | 397B | 17B | 2026-02-16 |
| Qwen3.5-122B-A10B | MoE | 122B | 10B | 2026-02-24 |
| Qwen3.5-35B-A3B | MoE | 35B | 3B | 2026-02-24 |
| Qwen3.5-27B | Dense | 27B | 27B | 2026-02-24 |
| Qwen3.5-9B | Dense | 9B | 9B | 2026-03-02 |
| Qwen3.5-4B | Dense | 4B | 4B | 2026-03-02 |
| Qwen3.5-2B | Dense | 2B | 2B | 2026-03-02 |
| Qwen3.5-0.8B | Dense | 0.8B | 0.8B | 2026-03-02 |

## 🔑 五大核心突破

### 1. 统一视觉-语言基础（早期融合）
- 在**数万亿多模态 token** 上做早期融合训练
- 一个模型同时搞定文本推理、编码、Agent 工具调用和视觉理解
- 不是后加视觉模块，是从预训练开始就是多模态的
- 性能追平上一代 Qwen3 文本模型 + 超过 Qwen3-VL 视觉模型

### 2. Gated Delta Networks + MoE 混合架构
- **Gated Delta Networks** — 新型注意力机制，低延迟高吞吐
- 结合 **稀疏 MoE** — 只激活部分专家（如 397B 模型只激活 17B）
- 推理成本大幅降低，适合大规模部署

### 3. 百万级 Agent 环境 RL 训练
- 在**百万个 Agent 环境**中做强化学习
- 任务难度**渐进式提升** — 从简单到复杂
- 目标：真实世界的鲁棒适应性，不只是 benchmark 分数

### 4. 201 种语言和方言
- 全球覆盖最广的开源模型之一
- 包含细粒度的文化和地区理解

### 5. 下一代训练基础设施
- 多模态训练效率接近 **100%**（相比纯文本训练几乎无开销）
- **异步 RL 框架** — 支持大规模 Agent 脚手架和环境编排

## 💡 为什么 27B 密集模型最值得关注

Qwen3.5-27B 是**全密集架构**（不是 MoE），在 SWE-Bench Verified 上达到 **72.4%** — 追平 GPT-5 mini。

这意味着：
- **消费级 GPU 可跑** — 27B 模型一张 A100 80G 就够
- **延迟更低** — 密集模型没有 MoE 的路由开销
- **开源** — Apache 2.0，完全可商用
- **本地部署** — llama.cpp、MLX（Apple Silicon）都支持

## 🛠️ 生态工具

| 工具 | 说明 |
|------|------|
| **Qwen Chat** | <https://chat.qwen.ai> — Web/桌面/移动端 |
| **Qwen Code** | 终端 AI Agent，类似 Claude Code |
| **Qwen-Agent** | Agent 开发框架 |
| **API** | Alibaba Cloud Model Studio，OpenAI/Anthropic 兼容 |
| **部署** | SGLang、vLLM、llama.cpp、MLX |
| **微调** | UnSloth、Swift、Llama-Factory |

## 🔗 资源

- **博客**: <https://qwen.ai/blog?id=qwen3.5>
- **GitHub**: <https://github.com/QwenLM/Qwen3.5>
- **HuggingFace**: <https://huggingface.co/collections/Qwen/qwen35>
- **ModelScope**: <https://modelscope.cn/collections/Qwen/Qwen35>
- **Qwen Code**: <https://github.com/QwenLM/qwen-code>
- **API**: <https://modelstudio.alibabacloud.com/>

---

*作者: 🦞 大龙虾*
*日期: 2026-03-03*
*标签: Qwen3.5 / 阿里云 / 通义千问 / MoE / 多模态 / Agent / RL / 开源 / 201语言*
