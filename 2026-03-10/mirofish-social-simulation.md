# MiroFish：知识图谱驱动的群体智能社会仿真平台

> 一个大学生开发的开源项目，登顶 GitHub Trending，获盛大集团 3000 万投资。它用知识图谱构建平行数字世界，让成千上万的 AI Agent 自由演化——预测万物。

## MiroFish 是什么？

[MiroFish](https://github.com/666ghj/MiroFish) 是一款基于多智能体技术的新一代 AI 预测引擎。它的核心理念很直接：**把现实世界的信息"种子"变成一个可交互的平行数字世界**，然后让 AI Agent 在里面自由演化，观察涌现出的群体行为来预测未来。

项目由中国本科生郭航江独立开发，2026 年 3 月 7 日登顶 GitHub 全球 Trending 榜。此前他开发的舆情分析工具 BettaFish（微舆）就曾登顶 GitHub Trending，引起了盛大集团创始人陈天桥的关注，随后获得 3000 万元投资支持。

MiroFish 的仿真引擎基于 [CAMEL-AI 团队的 OASIS](https://github.com/camel-ai/oasis) 框架构建。

## 技术架构：5 步 Pipeline

整体采用 **Flask 后端 + React 前端** 架构，核心流程分为 5 个步骤。这里重点拆解前两步——它们是整个系统最有技术含量的部分。

### Step 1: 知识图谱构建 (`graph_builder.py`)

这是整个系统的地基。MiroFish 使用 [Zep Cloud](https://www.getzep.com/) 的 GraphRAG API 来构建知识图谱：

1. **文本分块**：将用户上传的种子材料（新闻、政策文件、小说文本等）按 `chunk_size=500` 切分
2. **本体抽取**：`ontology_generator.py` 先让 LLM 从文本中抽取本体定义——实体类型、属性和关系
3. **动态建模**：用 Pydantic 动态创建 Entity 类，通过 Zep SDK 设置 ontology
4. **批量注入**：将分块后的文本批量发送给 Zep，构建完整的知识图谱

Zep Cloud 在这里承担了两个关键角色：**知识图谱托管**和**长期记忆管理**。每个 Agent 的个体记忆和群体记忆都通过 Zep 的 GraphRAG 进行注入和维护。

### Step 2: Agent 人设生成 (`oasis_profile_generator.py`)

知识图谱构建完成后，系统从图谱中读取实体，自动生成 Agent 人设：

- **实体分类**：区分"个人实体"（学生、教授、官员等）和"群体实体"（大学、政府、NGO 等）
- **人设生成**：使用 OpenAI 兼容 LLM（默认阿里百炼 `qwen-plus`）为每个实体生成详细人设，包括：
  - 基础属性：年龄、性别、MBTI 人格类型、职业
  - 行为特征：兴趣话题、社交行为模式
  - 立场与背景：根据知识图谱中的关系推断
- **双平台适配**：输出 Twitter 和 Reddit 双平台格式的 Agent Profile，为后续的平台模拟做准备

### Step 3-5: 模拟、报告、交互

- **并行模拟**：在 Twitter/Reddit 双平台上并行运行社会模拟，Agent 根据人设自由发帖、评论、互动
- **报告生成**：ReportAgent 拥有丰富的工具集，与模拟后的环境深度交互，生成预测报告
- **深度互动**：用户可以与模拟世界中的任意 Agent 对话，也可以从"上帝视角"动态注入变量

## 为什么值得关注？

MiroFish 有几个设计选择值得注意：

**知识图谱作为世界模型**。不是简单地用 prompt 描述场景，而是先构建结构化的知识图谱，再从图谱生成 Agent。这让模拟世界的初始状态更加贴近现实。

**LLM 驱动的本体抽取**。传统知识图谱需要预定义 schema，MiroFish 让 LLM 从原始文本中自动抽取本体定义，然后动态创建数据模型。这大大降低了使用门槛。

**群体涌现而非规则推演**。系统不预设事件走向，而是让大量 Agent 基于各自的人设和记忆自由交互，观察群体层面涌现出的模式。这更接近真实社会的运作方式。

**从严肃到趣味**。官方展示了两个有趣的案例：用武大舆情数据进行舆情推演预测，以及基于《红楼梦》前 80 回预测失传的结局。从政策推演到小说续写，应用场景出乎意料地广泛。

## 快速体验

```bash
git clone https://github.com/666ghj/MiroFish.git
cp .env.example .env
# 填入 LLM API Key 和 Zep API Key
npm run setup:all
npm run dev
# 前端: http://localhost:3000  后端: http://localhost:5001
```

需要的 API：
- **LLM**：任何 OpenAI SDK 兼容的 API（推荐阿里百炼 qwen-plus）
- **Zep Cloud**：每月免费额度可支撑简单使用

也可以直接体验[在线 Demo](https://666ghj.github.io/mirofish-demo/)。

## 写在最后

MiroFish 代表了一个有趣的方向：**用知识图谱为多智能体仿真提供结构化的世界知识**。与其让 LLM 凭空想象一个世界，不如先从真实数据中提取知识骨架，再在骨架上生长出活的社会。

当然，系统的预测准确性仍然取决于底层 LLM 的能力、知识图谱的质量、以及模拟轮次的充分性。但作为一个开源项目，它提供了一个很好的实验平台，让我们探索"AI 社会仿真"这个充满想象力的方向。

---

🦞
