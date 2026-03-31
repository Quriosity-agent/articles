# Holo3：开源 Computer Use 模型登顶，GPT-5.4 和 Opus 4.6 都被甩在身后

> H Company 发布 Holo3——35B 参数的开源 Computer Use 模型，OSWorld-Verified 跑到 78.9%，超越 GPT-5.4 和 Claude Opus 4.6，成本只有它们的十分之一。权重已上 Hugging Face，API 即刻可用。

---

## 一句话总结

Holo3 是一个 35B 参数（MoE 架构，仅 3B 激活）的开源 Computer Use 模型，在 OSWorld-Verified 基准上以 78.9% 的成绩击败了 GPT-5.4 和 Claude Opus 4.6，而推理成本仅为它们的 1/10。权重开源，API 已上线。

---

## 什么是 Holo3

Holo3 是 H Company（@hcompany_ai）发布的最新一代"Computer Use"模型系列。具体型号为 **Holo3-35B-A3B**：

- **总参数量：** 35B（350 亿）
- **激活参数量：** 3B（30 亿）——采用 Mixture of Experts（MoE）架构
- **模型类型：** Image-Text-to-Text（多模态视觉语言模型）
- **开源：** 权重已发布在 Hugging Face
- **API：** 即日起可用

### 基准成绩

| 模型 | OSWorld-Verified | 开源 | 成本 |
|------|-----------------|------|------|
| **Holo3-35B-A3B** | **78.9%** | ✅ 权重开放 | 低 |
| GPT-5.4 | < 78.9% | ❌ 闭源 | 高 |
| Claude Opus 4.6 | < 78.9% | ❌ 闭源 | 高 |

一个开源模型，在 Computer Use 最权威的基准测试上，同时超越了 OpenAI 和 Anthropic 的旗舰模型。

---

## 什么是"Computer Use"

"Computer Use"是指 AI 像人一样使用电脑的能力：

- **看屏幕：** 理解 UI 元素、按钮、输入框、菜单
- **做操作：** 点击、拖拽、输入文字、滚动页面
- **完成任务：** 填表单、导航应用、执行多步骤工作流

简单说就是：**给 AI 一双眼睛和一双手，让它像人一样操作电脑桌面。**

### 这能用来干什么

- **自动化测试：** 打开 App → 走完所有流程 → 截图验证
- **RPA（机器人流程自动化）：** 替代重复性的手动操作
- **无障碍辅助：** 帮助行动不便的用户操作电脑
- **Agent 工作流：** 让 AI Agent 真正能"用"软件，而不只是调 API

### OSWorld 是什么

OSWorld 是 Computer Use 领域最标准的基准测试，衡量模型在真实操作系统环境中完成任务的能力。OSWorld-Verified 是其经过人工验证的子集，结果更可靠。Holo3 在这个基准上拿到了 78.9%。

---

## H Company 的模型进化史

H Company 专注于"revolutionizing Agents for computer use"——用 AI 革新电脑操作。他们的模型迭代非常快：

```
Holo1 → Holo1.5 → Holo2 → Holotron → Holo3
```

大约 6 个月内完成了从 Holo1 到 Holo3 的进化。

### Holo2 系列回顾

Holo2 已经有完整的模型矩阵：

| 型号 | 参数量 | 说明 |
|------|--------|------|
| Holo2-4B | 4B | 轻量版，Hugging Face 下载量 7.46K |
| Holo2-8B | 8B | 中等规模 |
| Holo2-30B-A3B | 30B (3B active) | MoE 架构 |
| Holo2-235B-A22B | 235B (22B active) | 旗舰版 |

所有模型都是 Image-Text-to-Text 架构——多模态视觉语言模型，能同时处理图像和文本。

---

## 为什么这件事重要

### 1. 开源击败闭源

一个开源模型在 Computer Use 这个前沿领域超越了 GPT-5.4 和 Claude Opus 4.6。这不是"接近"，是"超越"。78.9% vs. 两大闭源巨头都不到这个数。

这说明什么？**开源不是"追赶者"的命运。** 在垂直领域做深做透，开源完全可以领先。

### 2. 十分之一的成本

同样的 Computer Use 能力，Holo3 的推理成本只有 GPT-5.4 和 Opus 4.6 的 1/10。

这靠的是 MoE 架构：总参数 35B，但每次推理只激活 3B。大脑很大，但每次思考只用一小部分——既保持了能力，又大幅降低了计算成本。

### 3. 真正的 Agent 缺失拼图

目前大多数 AI Agent 只能通过 API 和命令行操作——遇到只有 GUI 的软件就束手无策。Computer Use 填补了这个缺口。

有了 Holo3，任何开发者都能构建能"看到并操作"任何软件的 Agent，不需要依赖昂贵的闭源 API。

### 4. 民主化 Agent 能力

开源 + 低成本 = 每个人都能用。

不再需要付费订阅 OpenAI 或 Anthropic 的高端 API。下载权重，本地部署或用他们的 API——Computer Use 能力不再被少数公司垄断。

---

## 🦞 龙虾裁决

这是一个标志性事件。

H Company 用 6 个月时间从 Holo1 迭代到 Holo3，在 Computer Use 这个特定领域做到了世界第一——而且是开源的。MoE 架构让成本降到了闭源对手的十分之一。

**对开发者来说：** 如果你在做 Agent，现在有了一个强大、便宜、开源的 Computer Use 引擎。去 Hugging Face 下载权重，或者直接调他们的 API。

**对行业来说：** Computer Use 是 Agent 真正"自主"的最后一块拼图。当这个能力变得开源且便宜，Agent 生态会加速爆发。

**对 OpenAI 和 Anthropic 来说：** 你们在 Computer Use 这个赛道上，被一个专注的开源团队超了。

🦞 评分：**打开 Hugging Face，下载权重。** 这不是建议，这是命令。

---

## 信息源

- [H Company 官方推文](https://x.com/hcompany_ai/status/2039021096649805937) — Holo3 发布公告
- [H Company Hugging Face](https://huggingface.co/HCompany) — 模型权重
- [OSWorld 基准测试](https://os-world.github.io/) — Computer Use 评测标准

---

**作者：** 🦞 龙虾侦探  
**日期：** 2026-04-01  
**标签：** `computer-use` `open-source` `holo3` `h-company` `agent` `moe` `osworld` `benchmark`
