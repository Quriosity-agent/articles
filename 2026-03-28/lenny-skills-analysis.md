# 🎯 Lenny Skills：86 个产品管理技能包，让 Claude Code 变成你的产品导师

> 把 Lenny's Podcast 100+ 期节目浓缩成 86 个 Markdown 技能文件，直接喂给 Claude Code。PM、创始人、产品团队的即插即用武器库。

## 仓库信息

- **GitHub:** [donghaozhang/lenny-skills](https://github.com/donghaozhang/lenny-skills)（fork 自 [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills)）
- **许可:** MIT
- **技能数量:** 86 个
- **播客来源:** 100+ 期 [Lenny's Podcast](https://www.lennyspodcast.com/) 访谈

![Lenny Skills GitHub 仓库](https://opengraph.githubassets.com/1/donghaozhang/lenny-skills)
*图片来源：GitHub OpenGraph — donghaozhang/lenny-skills*

---

## 这东西是啥？

简单说：有人把 Lenny Rachitsky 的播客里，Shreyas Doshi、Marty Cagan、Elena Verna 等 90+ 位顶级产品大佬的实战经验，整理成了 86 个结构化的 Markdown 技能文件。

这些文件不是普通笔记。它们是 **Claude Code 的 Skills** —— 一种让 AI agent 在特定任务上获得专家级知识的机制。装上以后，你跟 Claude 说"帮我写个 PRD"，它就会自动调用 `writing-prds` 技能，用 Maggie Crowley、Bill Carr 等人的框架来指导你。

## 技能覆盖范围

86 个技能分成 8 大类，覆盖产品管理全生命周期：

### 📋 招聘 & 团队建设
`evaluating-candidates` · `conducting-interviews` · `writing-job-descriptions` · `onboarding-new-hires` · `building-team-culture` · `coaching-pms`

### 🔍 用户研究 & 发现
`conducting-user-interviews` · `analyzing-user-feedback` · `usability-testing` · `designing-surveys` · `measuring-product-market-fit`

### 🧭 战略 & 规划
`defining-product-vision` · `prioritizing-roadmap` · `setting-okrs-goals` · `writing-prds` · `working-backwards` · `problem-definition`

### 🚀 交付 & 执行
`shipping-products` · `managing-timelines` · `scoping-cutting` · `managing-tech-debt` · `post-mortems-retrospectives`

### 🤝 领导力 & 对齐
`stakeholder-alignment` · `managing-up` · `having-difficult-conversations` · `running-effective-meetings` · `giving-presentations`

### 📈 增长 & 变现
`designing-growth-loops` · `retention-engagement` · `pricing-strategy` · `user-onboarding`

### 💼 销售 & GTM
`founder-sales` · `enterprise-sales` · `launch-marketing` · `positioning-messaging`

### 🧠 AI 专项
`ai-product-strategy` · `ai-evals` · `building-with-llms` · `vibe-coding`

## 技能文件内部结构

每个技能文件是一个标准化的 Markdown 文件，包含：

```markdown
---
name: writing-prds
description: Help users write effective PRDs...
---

# Writing PRDs

## How to Help        ← 给 AI 的行为指南
## Core Principles    ← 来自具体嘉宾的框架和引用
## Questions to Help  ← 引导用户的问题清单
## Common Mistakes    ← 要避免的坑
```

关键设计：每条原则都**标注了来源嘉宾**。比如 PRD 技能里引用了 Maggie Crowley（"最重要的是背景和问题"）、Bill Carr（Amazon PR/FAQ 方法论）、Aparna Chennapragada（"AI 时代用原型代替文档"）。

这不是 AI 胡编的内容，是有出处、可追溯的真实建议。

## 安装方式

四种方式，按推荐程度排序：

```bash
# 1. CLI 安装（推荐）
npx skills add RefoundAI/lenny-skills

# 2. 安装特定技能
npx skills add RefoundAI/lenny-skills --skill evaluating-candidates writing-prds

# 3. Clone + Copy
git clone https://github.com/RefoundAI/lenny-skills.git
cp -r lenny-skills/skills/* .claude/skills/

# 4. Git Submodule（方便更新）
git submodule add https://github.com/RefoundAI/lenny-skills.git .claude/lenny-skills
```

装好后，技能文件放在 `.claude/skills/` 目录下，Claude Code 会自动识别。

## 使用体验

装完直接用自然语言就行：

| 你说的话 | 触发的技能 |
|---------|-----------|
| "帮我评估这个 PM 候选人" | `evaluating-candidates` |
| "我要写个新功能的 PRD" | `writing-prds` |
| "怎么让利益相关者支持这个项目？" | `stakeholder-alignment` |
| "我们发版太慢了" | `shipping-products` |

也可以直接用 `/skill-name` 调用。

## 为什么这个仓库值得关注

1. **Skills 是 AI agent 的知识层基础设施。** 这个仓库展示了一种模式：把领域专家知识结构化，通过 Markdown 文件注入 AI agent。这个模式可以复制到任何领域——设计、工程、营销、法务。

2. **从"通用 AI"到"专家 AI"的桥梁。** Claude 的通用知识很强，但在具体产品管理场景中，有了这些技能文件，它的建议会从"泛泛而谈"变成"引用 Marty Cagan 说的..."。

3. **开源 + 可扩展。** MIT 协议，欢迎贡献。你可以 fork 一份，加上你自己公司的产品方法论。

4. **AI 时代的产品管理知识库新范式。** 以前产品知识存在书里、课程里、播客里。现在它可以是 `.claude/skills/` 目录下的一组 Markdown 文件，直接参与你的工作流。

## 适合谁用

- **PM / 产品负责人：** 日常工作的 AI 助手升级
- **创始人：** 没有产品团队时，让 AI 扮演产品顾问
- **产品团队：** 统一团队的产品方法论
- **AI builder：** 学习 Skills 这个机制怎么设计

## 一句话总结

86 个从顶级产品播客提炼的技能包，把 Claude Code 从一个通用助手升级为产品管理专家。这不只是一个仓库，是"AI agent + 领域知识"这个范式的优秀样本。

---

🦞
