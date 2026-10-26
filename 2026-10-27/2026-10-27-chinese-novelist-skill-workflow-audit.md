# Chinese Novelist Skill：用文件、文风基准与事实账本组织中文长篇创作

> 阅读与实测日期：2026 年 10 月 27 日。项目：[PenglongHuang/chinese-novelist-skill](https://github.com/PenglongHuang/chinese-novelist-skill)。检查的主分支提交为 `7017828`，提交于 10 月 21 日；当时最新正式 Release 为 [v2.3.1](https://github.com/PenglongHuang/chinese-novelist-skill/releases/tag/v2.3.1)，发布于 10 月 20 日 UTC。本文日期是审阅日期，不是项目首发日期。

Chinese Novelist Skill 给现有编码 Agent 提供一套中文小说生产流程：先问清创意，再落盘人物与大纲，随后逐章写作、更新摘要并检查字数。它没有训练新模型，也没有提供独立的桌面编辑器。检查的仓库以 Markdown 指令、模板和指南为主，另有一个 Python 字数检查脚本。

最值得看的地方，是它如何让 Agent 在长任务里反复回到同一套资料。最需要保持清醒的地方，则是「写进了规则」与「程序强制保证」之间的距离。[Skill 入口](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/SKILL.md)

![上游示例：规划摘要与写作模式选择](imgs/chinese-novelist-skill-workflow-audit/phase2-plan.png)

*本文三张图均为上游仓库提供的演示截图，不是本次生成小说的结果。部分图中的文件编号早于当前规范，应以本文所述的固定提交为准。*

## 1. 一套可阅读、可修改的写作操作规程

入口 `SKILL.md` 把详细要求拆到各阶段文档：初始化、递进式问答、标题选择、规划确认、写作模式选择、逐章创作和最终校验。Agent 进入相应阶段时，再读取对应流程。

这比一句「帮我写三十章小说」多出的，是稳定的操作顺序和交付物，而不是新的推理能力。目录是否创建、文件是否更新、工具是否调用，都需要宿主 Agent 执行。仓库自身没有常驻的任务调度服务。

规划确认之后，指令要求连续写到结束，不再逐章询问。它偏向批量产出草稿，而非每章等待作者签字的编辑模式。模型费用、宿主工具权限和运行时限制仍然存在；开源 Skill 免费不代表生成整部长篇没有成本。

## 2. 作品记忆由几份不同用途的文件承担

当前规范把创作材料分为以下几类：

| 文件 | 用途 |
|---|---|
| `00-人物档案.md` | 性格、缺陷、说话方式、恐惧与关系 |
| `01-大纲.md` | 章节事件、承接、悬念，以及设定与事实词典 |
| `02-写作计划.json` | 章号、路径、状态、字数、重试次数与写作模式 |
| `03-文风基准.md` | 文风指纹、范例段落、负面清单与本书校准段落 |
| `99-章节摘要.md` | 每章完成后追加的剧情摘要 |
| `第XX章-标题.md` | 章节内容 |

摘要不再不断塞回大纲，进度也不靠聊天里的「写到第几章了」判断。初始化流程要求读取计划状态，寻找未完成项目；计划损坏时，再尝试借摘要、现存文件和字数结果重建进度。[规划流程](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/flows/phase2-planning.md)、[共享机制](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/flows/shared-infrastructure.md)

另有 `user-preferences.json` 保存题材、视角、基调等偏好。这里的「记忆」是 Agent 读写文件，不是模型被重新训练，也不是自动获得无限上下文。计划和偏好如果没有及时落盘，中断恢复就没有可靠依据。

![上游示例：创作偏好与未完成项目入口](imgs/chinese-novelist-skill-workflow-audit/memory-demo.png)

## 3. 文风基准与事实账本，分别约束怎么写、能写什么

文风基准不是只有「冷峻」「电影感」几个标签。规划文档要求保存范例正文，第一章完成后再挑选本书段落作为后续参照。这比抽象风格形容词提供了更具体的模仿对象。

事实词典则区分读者已经知道的内容、完整真相和计划揭示章节，还要求登记时间、年龄、金额、人数等硬事实。它试图减少两种常见错误：数字前后变化，以及过早泄露尚未揭示的设定。[事实词典模板](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/guides/outline-template.md)

但这些仍是给 Agent 的读写规则。仓库没有独立程序自动从正文抽取事实、证明人物知识边界，或检测所有矛盾。一个错误一旦被 Agent 登记进账本，也可能继续传播。账本让错误更容易定位，不会自动把错误变成正确事实。

## 4. 并行写作以大纲换速度，也增加接缝风险

项目提供串行、分批子 Agent 和 Agent Teams 三种流程描述。子 Agent 模式把章节分成不重叠的批次，批次内顺序写，批次间并行。

关键细节是：后一个批次开始时，前一个批次的末章可能还没写完。流程明确允许后批次按大纲中的承接与悬念先写，不等待前文落盘，再由主 Agent 检查批次接缝。这是速度与依赖完整性的取舍，不能理解为多 Agent 天然拥有一致的故事现场。

共享文件要求改前重读、只修改自己负责的字段，并依赖宿主编辑工具发现过期修改。仓库没有另外实现跨文件事务或文件锁；团队任务独占也依赖宿主真的提供相应能力。没有团队能力时，文档要求回退子 Agent 模式，实际兼容性仍需逐个宿主验证。[并行流程与写入协议](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/flows/phase3-writing.md)

## 5. 自动校验首先是字数检查，不是小说质量认证

本次没有安装 Skill 或调用模型，只对唯一的 Python 脚本做了 **10 项合成样本行为检查**，全部得到可重复的预期结果，其中也包括局限：

- 默认门槛是 3000，统计范围是 `U+4E00–U+9FFF` 的汉字，不计英文与数字；它不是 token 数或通用词数。
- 提取器跳过章节标题后，会继续统计后面的全部内容，没有专门隔离 `## 正文`。只有两个汉字的正文，加上摘要、背景和小节标题，样本计为八字。
- 5001 字也会通过默认检查：脚本只检查下限，不执行写作要求里的 5000 字上限。
- `--all` 扫描现有的 `第*.md`，不读取写作计划。计划里缺失的章节不会仅靠目录扫描自动报出，仍需 Agent 另查存在性。
- 低于门槛与缺失单文件的退出码分别为 1、2；阿拉伯章号按数值排序。另一个边界是负数门槛未被拒绝，空正文也可通过。

这些检查验证脚本行为，不验证文学质量。复现脚本保存在 [probe_wordcount.py](imgs/chinese-novelist-skill-workflow-audit/probe_wordcount.py)，证据说明见 [SOURCES.md](imgs/chinese-novelist-skill-workflow-audit/SOURCES.md)。[上游字数脚本](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/scripts/check_chapter_wordcount.py)

「量化去 AI 味」也应按实际实现理解：指南给出句式、意象和重复动作的次数约束，由 Agent 自查，没有配套独立的文风检测程序。[文风检查指南](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/guides/chapter-guide.md)

![上游示例：文件树与章节 Markdown 预览](imgs/chinese-novelist-skill-workflow-audit/phase4-done.png)

## 6. 试用时要看未通过项，而不只看 completed

最终校验文档规定最多三轮修复，但超过次数后仍可将项目标为 `completed`，并在报告中注明不合格章节。因此，这个状态更接近「流程结束」，不等于全书通过检查。逐章清单另一方面要求字数不足就继续扩充，说明不同层级的停止条件仍需明确协调。[最终校验流程](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/flows/phase4-validation.md)

更稳妥的试用方式是先限制章数、预算和重试次数，使用串行模式；检查事实词典能否追踪一个关键数字，关键信息是否按时揭示，中断后计划与实际文件是否一致。确认这些基础行为后，再测试并行收益。

仓库采用 MIT 许可。Roadmap 仍把可视化面板列为进行中，不应把演示截图当成一款已经内置完整面板的软件。README 的第三方模型服务赞助也不是使用该流程的必要依赖，宣传价格与服务质量不在本次验证范围。[Roadmap](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/ROADMAP.md)

**它的实际贡献，是把长篇创作里容易忘的步骤整理成可复用规程。文件分工、正文风格参照和事实登记值得借鉴；跨章一致性、并发安全与最终可读性，仍需要宿主能力、作者审阅和真实作品测试来兑现。**
