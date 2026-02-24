# Anthropic 发布金融服务插件套件：让 Claude 变身华尔街分析师

**来源：GitHub - anthropics/financial-services-plugins**

---

## 一句话总结

Anthropic 开源了一套 Claude 金融服务插件，覆盖投行、股票研究、私募和财富管理四大领域，内置 41 个技能、38 个命令和 11 个数据源连接器，让 Claude 能直接输出专业级的财务模型、研究报告和交易材料。

---

## 这是什么？

这是一组为 **Claude Cowork**（Anthropic 的企业协作产品）和 **Claude Code** 设计的插件。它们不是通用聊天增强，而是**金融行业专用的工作流引擎**——把 Claude 从"能聊金融"变成"能干金融活"。

核心理念：**纯 Markdown + JSON，零代码、零基础设施、零构建步骤**。所有领域知识、工作流程和最佳实践都编码在文件里，Claude 运行时自动调用。

---

## 五大插件模块

### 1. Financial Analysis（核心插件，必装）

共享基础层，提供所有数据连接器和通用建模能力：

- **可比公司分析（Comps）** — `/comps AAPL` 一键生成
- **DCF 估值模型** — 含 Python 校验脚本
- **LBO 模型** — 杠杆收购回报分析
- **三表联动** — 从 SEC 文件自动填充利润表、资产负债表、现金流量表
- **PPT 质检** — 检查演示文稿的数据一致性和格式规范
- **竞争分析** — Porter 五力、SWOT 等框架

### 2. Investment Banking（投行）

投行日常工作全覆盖：

| 命令 | 功能 |
|------|------|
| `/cim` | 生成保密信息备忘录 |
| `/teaser` | 撰写项目概要 |
| `/buyer-list` | 构建潜在买家名单 |
| `/merger-model` | 并购模型分析 |
| `/one-pager` | 公司单页概况 |
| `/deal-tracker` | 交易进度追踪 |
| `/process-letter` | 流程信函 |

还内置了 Pitch Deck 技能，带完整的 XML 引用、格式标准和幻灯片模板。

### 3. Equity Research（股票研究）

卖方分析师的全套工具：

- **盈利分析** — 财报出来后快速生成更新报告
- **首次覆盖** — 从公司调研到估值到图表生成的五步流程
- **晨会笔记** — 每日晨报自动化
- **催化剂日历** — 跟踪影响股价的事件
- **投资论文跟踪** — 维护和更新投资逻辑

### 4. Private Equity（私募）

- **项目筛选** — `/screen-deal` 快速评估
- **尽调清单** — `/dd-checklist` 系统化检查
- **IC 备忘录** — `/ic-memo` 投委会材料
- **回报分析** — IRR/MOIC/DPI 等指标计算
- **投后管理** — 组合公司 KPI 监控

### 5. Wealth Management（财富管理）

- **客户会议准备** — `/client-review`
- **财务规划** — `/financial-plan`
- **组合再平衡** — `/rebalance`
- **税损收割** — `/tlh` 识别节税机会
- **客户报告** — `/client-report` 自动生成

---

## 11 个数据源连接器（MCP）

所有数据连接器集中在核心插件中，通过 MCP（Model Context Protocol）协议接入：

| 数据源 | 覆盖领域 |
|--------|---------|
| **Daloopa** | 财务数据自动提取 |
| **Morningstar** | 基金和股票分析 |
| **S&P Global** | Capital IQ 数据 |
| **FactSet** | 综合金融数据 |
| **Moody's** | 信用评级和风险 |
| **MT Newswires** | 实时新闻 |
| **Aiera** | 财报电话会议分析 |
| **LSEG** | 固收、外汇、宏观 |
| **PitchBook** | PE/VC 交易数据 |
| **Chronograph** | 另类投资管理 |
| **Egnyte** | 文档管理 |

还有两个合作伙伴插件：**LSEG**（8 个专业命令覆盖债券、外汇、期权、宏观）和 **S&P Global**（Tearsheet、盈利预览、融资摘要）。

---

## 架构亮点

### 纯文件驱动，零代码

```
plugin-name/
├── .claude-plugin/plugin.json   # 插件清单
├── .mcp.json                    # 数据连接器配置
├── commands/                    # 斜杠命令（Markdown）
└── skills/                      # 领域知识（Markdown）
```

每个 Skill 就是一个 Markdown 文件，定义触发条件和工作流步骤。Claude 根据上下文自动匹配并执行。这意味着：
- **无需部署** — 改个 Markdown 文件就生效
- **易于定制** — 换上你公司的术语、模板、流程
- **版本控制友好** — Git 管理，PR 审核

### 端到端工作流

不是零散的点工具，而是完整的链路：
- **研究→报告**：拉数据 → 分析财报 → 生成研究报告
- **数据→Excel**：自动生成带公式的 Comps/DCF/LBO 工作簿
- **分析→PPT**：从数据到品牌化演示文稿

---

## 定制化思路

Anthropic 明确说这些插件是**起点而非终点**：

1. **换数据源** — 编辑 `.mcp.json` 指向你的内部系统
2. **加公司上下文** — 在 Skill 文件里写入你的术语和流程
3. **导入模板** — 用 `/ppt-template` 教 Claude 你的品牌 PPT 风格
4. **调整工作流** — 按你团队实际做法修改指令

---

## 为什么值得关注？

这套插件的真正意义不在于"AI 能算 DCF"——它展示了一个模式：**用纯 Markdown 文件把行业专家知识系统化编码，让 LLM 变成领域专家**。

这个模式完全可以复制到法律、医疗、咨询等任何专业服务领域。41 个 Skill 文件就是 41 份"如何像资深分析师一样工作"的操作手册，只不过读者是 AI。

---

*仓库地址：<https://github.com/anthropics/financial-services-plugins>*
*本文基于该开源仓库内容编译整理。*
