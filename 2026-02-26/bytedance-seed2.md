# ByteDance Seed2.0：字节跳动发布新一代通用 Agent 基础模型

**来源：seed.bytedance.com | 2026年2月**

---

## 一句话总结

字节跳动 Seed 团队发布 Seed2.0 系列模型（Pro / Lite / Mini 三档），定位"通用 Agent 模型"。多模态理解全面升级，LLM + Agent 能力大幅强化，在数学、代码、搜索、视觉推理等维度达到业界第一梯队，多项指标与 GPT-5.2、Claude Opus 4.5、Gemini 3 Pro 正面交锋。

---

## 三档定位

| 型号 | 侧重 | 适用场景 |
|------|------|----------|
| **Seed2.0 Pro** | 长链路推理 + 复杂任务稳定性 | 真实业务复杂场景 |
| **Seed2.0 Lite** | 生成质量 + 响应速度 | 通用生产级 |
| **Seed2.0 Mini** | 推理吞吐 + 部署密度 | 高并发 / 批量生成 |

---

## 核心能力

### 1. 多模态视觉理解
- 视觉推理 & 感知显著提升，MathVision **88.8**（超 GPT-5.2 的 86.8）
- 动态场景时间序列 & 运动感知理解增强，MotionBench 领先
- 从图像提取结构化信息、生成可运行的前端代码（含动效）

### 2. Agent 能力
- 长链路多步骤任务稳定推进（FreeCAD 建模等复杂工作流）
- SWE-Bench Verified **76.5**，Terminal Bench 2.01 **55.8**
- 搜索 Agent：BrowseComp **77.3**，BrowseComp-zh **82.4**（中文搜索超所有对手）

### 3. 数学 & 推理
- AIME 2026: **94.2**（GPT-5.2 93.3，Gemini 3 Pro 93.3）
- HMMT Feb 2025: **97.3**（与 Gemini 3 Pro 持平）
- ARC-AGI-2: **37.5**（仅次于 GPT-5.2 的 57.5）

### 4. 代码
- Codeforces **3020**（Gemini 3 Pro 2726，GPT-5.2 3148）
- LiveCodeBench v6 **87.8**（与 GPT-5.2 持平）

### 5. 视频理解
- VideoReasonBench **77.8**（超过人类 73.8）
- 流式视频、多视频对比、长视频全面覆盖

---

## 重点基准对比

| 基准 | Seed2.0 Pro | GPT-5.2 High | Claude Opus 4.5 | Gemini 3 Pro |
|------|-------------|-------------|-----------------|-------------|
| AIME 2026 | **94.2** | 93.3 | 92.5 | 93.3 |
| GPQA Diamond | 88.9 | **92.4** | 86.9 | **91.9** |
| Codeforces | 3020 | **3148** | 1701 | 2726 |
| SWE-Bench Verified | 76.5 | **80** | **80.9** | 76.2 |
| BrowseComp | **77.3** | 77.9 | 67.8 | 59.2 |
| MathVision | **88.8** | 86.8 | 74.3 | 86.1 |
| ARC-AGI-2 | 37.5 | **57.5** | 29.1 | 31.1 |

---

## 架构亮点

1. **通用 Agent 架构** — 不只是 LLM，而是原生为长链路 Agent 任务设计，多步骤指令稳定可靠
2. **多模态融合** — 视觉 + 文本 + 视频统一处理，从感知到推理端到端
3. **三档梯度** — Pro/Lite/Mini 覆盖从研究到高并发部署的全场景需求
4. **研究级能力** — 从竞赛级推理扩展到 FrontierSci 等研究级任务

---

## 为什么值得关注？

1. **中国 AI 模型首次全面对标国际顶尖** — Seed2.0 在数学、代码、搜索、视觉等全维度与 GPT-5.2 / Gemini 3 Pro 正面对决，不再只是单项突破
2. **Agent 能力是核心卖点** — 不只是跑基准，而是在真实复杂工作流中稳定推进，这才是模型落地的关键
3. **中文搜索能力碾压** — BrowseComp-zh 82.4 远超所有竞争者，中文场景下无出其右
4. **视频理解超越人类** — VideoReasonBench 77.8 vs 人类 73.8，多模态理解进入新阶段
5. **豆包生态整合** — 通过火山引擎 API 直接可用，字节生态内即刻落地

---

*原文：<https://seed.bytedance.com/en/seed2>*
*Model Card：<https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2/0214/Seed2.0%20Model%20Card.pdf>*
