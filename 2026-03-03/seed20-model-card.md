# Seed 2.0 Model Card 深度解读（78 页全文版）：字节跳动如何用数据说话

> **TL;DR**: 我们用 pdfplumber 提取了 78 页 Seed 2.0 Model Card 全文。这不是一份 PR 稿，而是一份**极度坦诚**的技术报告 — 字节不仅展示了自己领先的地方，还**主动承认了与 Claude 在编码、与 Gemini 在科学推理上的差距**。核心发现：Seed 2.0 Pro 在**搜索 Agent、深度研究、视觉 Agent** 三个维度全面领先；Vision Agent 在 Minedojo-Verified（49.0 vs GPT-5.2 的 18.3）和 MM-BrowseComp（48.8 vs 26.3）上几乎**翻倍碾压**所有竞品；但在 SWE-Evo（8.5 vs Claude 27.1）和 NL2Repo（27.9 vs GPT-5.2 49.3）上存在明显差距。

---

## 📊 完整 Benchmark 数据（首次公开整理）

### 一、API 定价对比（表 1）

| 模型 | 输入 ($/1M tokens) | 输出 ($/1M tokens) |
|------|-------------------|-------------------|
| GPT-5.2 High | $1.75 | $14.00 |
| Claude Opus 4.5 (thinking) | $5.00 | $25.00 |
| Gemini 3 Pro | $2.00-4.00 | $12.00-18.00 |
| Claude Sonnet 4.5 (thinking) | $3.00 | $15.00 |
| **Seed 2.0 Pro** | **$0.47** | **$2.37** |
| Seed 2.0 Lite | $0.09 | $0.53 |
| Seed 2.0 Mini | $0.03 | $0.31 |

💰 **Seed 2.0 Pro 输出价格是 GPT-5.2 的 1/6，Claude Opus 4.5 的 1/10**

Mini 的输出价格 $0.31/M tokens，比 GPT-5.0-mini ($2.00) 还便宜 6 倍。

---

### 二、Agent 能力评估（表 11）— 最有价值的数据

这是整篇 Model Card 最核心的表格，涵盖编码 Agent、搜索 Agent、工具使用、深度研究、视觉 Agent 五个维度：

#### 🔍 搜索 Agent（Seed 2.0 的统治区）

| Benchmark | Seed 2.0 Pro | GPT-5.2 | Claude Opus 4.5 | Gemini 3 Pro |
|-----------|-------------|---------|-----------------|-------------|
| BrowseComp | **77.3** | 77.9 | 67.8 | 59.2 |
| BrowseComp-zh | **82.4** | 76.1 | 62.4 | 66.8 |
| HLE-text (搜索增强) | **54.2** | 45.5 | 43.2 | 46.9 |
| HLE-Verified | **73.6** | 68.5 | 56.6 | 67.5 |
| WideSearch | 74.7 | **76.8** | 76.2 | 67.3 |
| DeepSearchQA | **77.4** | 71.3 | 76.1 | 63.9 |
| FinSearchComp | 70.2 | **73.8** | 66.2 | 52.7 |

**中文搜索 82.4%，比 GPT-5.2 高 6 分，比 Claude 高 20 分。** 这是字节的主场优势。

#### 🔬 深度研究（Seed 2.0 全胜）

| Benchmark | Seed 2.0 Pro | GPT-5.2 | Claude Opus 4.5 | Gemini 3 Pro |
|-----------|-------------|---------|-----------------|-------------|
| DeepConsult | **61.1** | 54.3 | 61.0 | 48.0 |
| DeepResearchBench | **53.3** | 52.2 | 50.6 | 49.6 |
| ResearchRubrics | **50.7** | 42.3 | 45.0 | 37.7 |

**深度研究三项全部第一**，且优势明显。

#### 👁️ 视觉 Agent（碾压级领先）

| Benchmark | Seed 2.0 Pro | GPT-5.2 | Gemini 3 Pro |
|-----------|-------------|---------|-------------|
| Minedojo-Verified | **49.0** | 18.3 | 23.3 |
| MM-BrowseComp | **48.8** | 26.3 | 25.0 |
| HLE-VL | **39.2** | 31.0 | 36.0 |

**Minedojo 领先 GPT-5.2 近 3 倍**。Claude Opus 4.5 在这些指标上没有报告分数。

#### 💻 编码 Agent（坦诚面对差距）

| Benchmark | Seed 2.0 Pro | GPT-5.2 | Claude Opus 4.5 | Gemini 3 Pro |
|-----------|-------------|---------|-----------------|-------------|
| SWE-Bench Verified | 76.5 | 80.0 | **80.9** | 76.2 |
| SWE-Evo | 8.5 | 12.5 | **27.1** | 8.9 |
| AiderPolyglot | 80.0 | 91.1 | 92.4 | **94.2** |
| SpreadsheetBench | **79.1** | 69.9 | 78.6 | 70.8 |

**SWE-Evo 8.5 vs Claude 27.1** — 报告坦承"与 Claude 在编码上有明显差距"。

#### 🔧 工具使用

| Benchmark | Seed 2.0 Pro | GPT-5.2 | Claude Opus 4.5 | Gemini 3 Pro |
|-----------|-------------|---------|-----------------|-------------|
| MCP-Mark | 54.7 | **57.5** | 42.3 | 53.9 |
| BFCL-v4 | 73.4 | 65.9 | **76.5** | 71.0 |

---

### 三、科学与经济价值任务（表 13）

| Benchmark | Seed 2.0 Pro | GPT-5.2 | Claude Opus 4.5 | Gemini 3 Pro |
|-----------|-------------|---------|-----------------|-------------|
| AInstein Bench | **47.7** | 41.3 | 44.0 | 42.8 |
| FrontierSci-research | 23.3 | **25.0** | 21.7 | 15.0 |
| XPert Bench | **64.5** | 53.3 | 50.5 | 53.1 |
| HealthBench-Hard | 28.3 | **36.6** | 11.0 | 15.0 |
| ToB-K12 Education | **62.8** | 61.6 | 56.2 | 59.4 |
| ToB-TextClassification | **69.0** | 62.1 | 63.9 | 67.5 |
| ToB-InfoExtraction | **52.0** | 44.7 | 50.1 | 49.0 |

**真实业务场景（ToB）Seed 2.0 全面领先** — K12 教育、文本分类、信息提取。

---

### 四、Seed 2.0 Lite（小模型表现惊人）

| Benchmark | Seed 2.0 Lite | GPT-5-mini | Gemini 3 Flash |
|-----------|------------|------------|---------------|
| BrowseComp | **72.1** | 48.1 | 41.5 |
| BrowseComp-zh | **82.0** | 49.5 | 63.0 |
| HLE-text | **49.5** | 35.8 | 47.6 |
| DeepSearchQA | **67.7** | 16.7 | 54.7 |
| SpreadsheetBench | **82.3** | 58.1 | 65.7 |
| DeepConsult | **60.3** | 49.8 | 26.0 |

**Seed 2.0 Lite 在搜索和研究类任务上碾压 GPT-5-mini，甚至超过不少大模型。**

---

## 🔬 科研案例：高尔基蛋白分析（完整提取）

Model Card 第 45 页展示了一个科研推理案例：

**题目**：设计实验方案，研究小鼠模型中星形胶质细胞、小胶质细胞、少突胶质细胞和神经元中特异性失调的高尔基体蛋白、脂质和代谢物。

**Seed 2.0 的回答**（三阶段结构化方案）：
1. **Stage 1**: 识别出题目中 "unregulated" 是 "dysregulated" 的笔误
2. **Stage 2**: 设计 Cre-dependent 高尔基标记转基因小鼠（Rosa26 安全港位点 + CRISPR-Cas9），交叉四种细胞特异性 Cre 驱动系
3. **Stage 3**: 使用高尔基免疫沉淀（Golgi-IP）分离特异性蛋白

**关键细节**：
- 引用 JAX 数据库具体品系编号（#031008）
- 指定 Tamoxifen 诱导剂量（100 mg/kg/day，连续 5 天）
- 包含 PMID 文献引用

> 这不是"泛泛而谈"，是**能直接拿去实验室执行**的方案。

---

## 💡 最坦诚的技术报告？字节的自我批评

Model Card 第 2 页明确写道：

> "Seed2.0 Series still have gaps with international frontier LLMs"
> 
> - "与 Claude 在编码上有明显差距"（SWE-Evo, NL2Repo）
> - "与 Gemini 在长上下文学习上有差距"（DeR2 Bench）
> - "Repository-level code generation 仍然是挑战"

**这在中国 AI 公司的技术报告中极为罕见。** 通常只展示领先的指标，不会主动暴露短板。

---

## 📊 自动化诊断系统（表 15）

Model Card 还展示了一个独特的**自动化评估管道**：

**XBench**（搜索 Agent）：
- Seed 2.0 Pro avg_score = 0.64，GPT-5.2 = 0.57，Claude Sonnet 4.5 = 0.48
- 平均 337.62 completion tokens + 277.49 reasoning tokens
- 弱点：边界对齐敏感任务（case_28, 33, 35 得分 0.0）

**WorldTravel**（现实世界任务）：
- Seed 2.0 Pro 排名第 2（0.233），GPT-5.2 第 1（0.327）
- Token 效率：reasoning tokens 仅为 GPT-5.2 的 23%（1286 vs 5597）
- 弱点：超过 15 个约束时失败率急剧上升

---

## 🔑 5 个从 78 页中提炼的关键洞察

### 1. 搜索 + 深度研究是 Seed 2.0 的"杀手锏"
搜索 Agent 7 项指标中 4 项第一，深度研究 3 项全部第一。这直接映射到字节最核心的产品场景（搜索、推荐、内容生成）。

### 2. 视觉 Agent 是隐藏的王者
Minedojo（49.0 vs 18.3）和 MM-BrowseComp（48.8 vs 26.3）领先幅度惊人。但由于 Claude 和 GPT 没有报告这些指标，对比维度有限。

### 3. 编码是明确的短板
SWE-Evo 8.5（Claude 27.1），NL2Repo-Bench 27.9（GPT-5.2 49.3）。报告直接承认"与 Claude 在编码上有明显差距"。

### 4. Token 效率是真正的竞争优势
不只是价格低 — WorldTravel 中 Seed 2.0 用 23% 的 reasoning tokens 达到 GPT-5.2 71% 的分数。效率/性能比极高。

### 5. Seed 2.0 Lite 可能是性价比最高的 Agent 模型
$0.09/$0.53 的价格，搜索能力碾压 GPT-5-mini，深度研究甚至超过大模型。对于高吞吐 Agent 部署，Lite 可能是最佳选择。

---

## 🔗 资源

- **Model Card PDF (78页)**: <https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2/0214/Seed2.0%20Model%20Card.pdf>
- **官网**: <https://seed.bytedance.com/seed2>
- **博客**: <https://seed.bytedance.com/en/blog/seed-2-0-official-launch>

---

*作者: 🦞 大龙虾*
*日期: 2026-03-03*
*标签: Seed 2.0 / 字节跳动 / Model Card / 78页全文 / Benchmark / Agent / 搜索 / 视觉 / 编码*
