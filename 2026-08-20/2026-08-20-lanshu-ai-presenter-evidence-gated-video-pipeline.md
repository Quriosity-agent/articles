# lanshu AI Presenter 源码审计：它不是数字人模型，而是一条证据驱动的视频生产线

> **一句话结论：** `lanshu-create-ai-presenter-video` 不是数字人模型，也不是装好就能出片的一键应用。它是一份给 Coding Agent 使用的生产协议：外接配音、数字人和口型能力，把脚本、授权、预算、任务 ID、成片与 QA 证据收进同一个可恢复的状态机。

![AI Presenter 的八阶段证据状态机](imgs/lanshu-ai-presenter-evidence-gated-video-pipeline/presenter-pipeline.svg)

2026 年 8 月 20 日，`cclank/lanshu-create-ai-presenter-video` 首次公开。项目名称很容易让人以为仓库里藏着一个“上传照片即可说话”的数字人模型，但源码给出的答案完全不同：仓库没有训练权重、推理服务或任何固定厂商的 API 客户端，核心是一份 `SKILL.md`、一个 `job.json` 任务账本，以及围绕 FFmpeg、媒体探测和交付报告组成的本地工具链。

截至 2026 年 10 月 9 日，仓库有约 2,558 Star、392 Fork，当前提交为 `c24720a85d63b1bd494f6447e48a59384733647b`。10 月 6 日新增的九种无真人讲解风格，我已经在[上一篇源码拆解](../2026-10-06/2026-10-06-lanshu-explainer-skill-nine-hyperframes-styles.md)中分析过。本文回到项目最初的 `presenter` 路线，回答一个更基础的问题：**它究竟怎样把一张人物图和一份文案，组织成一条可以被审计的数字人口播生产流程？**

---

## 01｜先说清楚：它是什么，又不是什么

这套仓库可以分成三层：

| 层 | 实际内容 | 是否包含在仓库中 |
|---|---|---|
| 生产协议 | 输入约束、授权门槛、状态机、成本记录、失败恢复、视觉验收 | 是 |
| 本地工具 | 初始化任务、预检、分段、状态核验、FFmpeg 交付与 smoke test | 是 |
| 生成能力 | TTS、数字人动作、口型修复、ASR，以及可选合成器 | 否，需要 Agent 环境外接 |

所以它不是 HeyGen、Synthesia 一类 SaaS 的开源替代，也不是某个数字人底模。更准确地说，它是一个 **provider-neutral Agent Skill**：规定 Agent 应该调用哪类能力、在什么时候付费、产物放在哪里、什么证据满足后才能继续。

![仓库、Agent 与外部生成能力的边界](imgs/lanshu-ai-presenter-evidence-gated-video-pipeline/provider-boundary.svg)

这里的“厂商中立”有双重含义。优点是可以替换语音、数字人或口型供应商，任务结构不必重写；代价是仓库本身不会生成任何数字人。你仍然需要已经安装并有凭证的 CLI、API 或本地模型，由 Agent 把它们接进 `job.json` 的 capability slots。

---

## 02｜`job.json` 不是配置文件，而是生产账本

任务由 `scripts/init_job.py` 初始化。它会把脚本、人物图和补充素材复制到一个自包含目录，而不是直接引用散落在电脑各处的绝对路径。任务目录非空时会拒绝覆盖，原始输入也不会被修改。

真正重要的是 `job.json`。它同时记录：

- 人物图是否获得授权、是否为成年人；
- 是否允许上传到远程服务、是否允许声音克隆；
- 画幅、帧率、语音和创意路线；
- 预计付费秒数、估算成本、pilot 与完整生成是否获批；
- 语音、主数字人、短动作、口型修复、ASR、合成器和编码 QA 分别由什么能力承担；
- 每个阶段产生的文件、远程 task ID、人工复核结果和交付报告。

普通脚本通常只关心“下一条命令是什么”。这份 manifest 还关心“我们为什么有权运行这条命令”“这次重试会不会再次扣费”“中断后该继续轮询哪个任务”。这让它更像一个轻量生产数据库，而不是若干 Prompt 的容器。

---

## 03｜八个状态，把“做完了”变成可验证的声明

流程使用八阶段状态机：

```text
intake
→ content_locked
→ audio_locked
→ visual_plan_locked
→ presenter_generated
→ composition_checked
→ rendered
→ verified
```

状态不是 Agent 自己写一句“完成”就能推进。`scripts/check_state.py` 会从实际文件重新计算当前阶段：锁定脚本是否存在、音频和视频流能否解码、分段计划与人工复核是否齐全、最终报告是否证明 master 与 share 文件通过检查。如果 manifest 声称已经 `verified`，磁盘证据却只支持 `audio_locked`，工具可把状态写回真实阶段。

这套设计解决了长任务里很常见的问题：聊天上下文会中断，远程生成会延迟，Agent 也可能把“API 返回成功”误当成“成片已交付”。状态机把进度从对话记忆转移到可检查的产物上。

---

## 04｜为什么必须先锁音频

这条流程把最终旁白当作 **master clock**。顺序不是先让人物动起来再配音，而是：

```text
锁定文案 → 生成完整旁白 → ASR 核对 → 获取真实时长
→ 规划镜头与分段 → 生成数字人 → 静音视频原声 → 以锁定旁白完成合成
```

ASR 的任务不是重新写字幕，而是检查遗漏、添加、数字和专有名词。只有音频通过后，真实时长才进入镜头表、字幕、关键词图形与片尾。

这样做有两个直接收益。第一，所有画面与字幕共用同一时间基准，不会因为每一段分别合成而逐渐漂移。第二，如果某段动作可用但口型失败，可以保留已经付费的 motion plate，只对嘴部做修复，而不用把整段人物动作重新生成一次。

---

## 05｜分段不是平均切开，而是在真实停顿中找边界

许多数字人服务有单次时长上限，并可能按整秒计费。`scripts/plan_segments.py` 读取 ASR 的词级时间，搜索至少 0.25 秒的真实停顿，在供应商上限之前选择最晚的安全断点，并保证单段至少 2 秒。

它还可以按整秒计费规则计算请求时长，把每段起止点、接缝和总付费秒数写入计划。如果上限范围内没有停顿，工具会拒绝输出，而不是从一句话中间硬切。

这看起来只是一个小脚本，却体现了整套项目最实用的判断：**生产系统不应该假装所有限制都能自动绕过。找不到安全切点时，停下来改稿或换供应商，比制造一个不可修的口型接缝更便宜。**

---

## 06｜付费调用之前，先把成本和恢复路径写下来

每一次可能收费的远程调用前，规范要求记录：

- 上传了什么、请求了多少秒或多少单位；
- 单价、预计总成本，或明确标记价格未知；
- 是否先通过低成本 pilot；
- 预期产生什么文件；
- 失败时轮询还是重试，以及最多重试几次。

完整生成前必须先做短 pilot。远程任务中断后先保存并轮询 task ID，不能在结果不明时重新提交。连续三个付费候选被人工拒绝后，流程应停止并要求修改输入或策略。

这部分不是创意算法，却可能是仓库最有商业价值的地方。数字人工作流真正昂贵的常常不是第一次请求，而是“没看见结果，以为失败，再点一次”以及“口型有问题，于是整段重做”。它把这些隐性浪费写成了机器可执行的约束。

---

## 07｜交付不是导出一个 MP4，而是原子发布

`scripts/finalize_delivery.sh` 先在临时目录构建所有结果，检查失败时不发布半成品。默认交付过程包括：

1. 确认输入具有可解码的视频流和音频流；
2. 两遍响度归一化，目标约为 -16 LUFS、真峰值不高于 -1 dBTP；
3. 输出 H.264 `yuv420p` + AAC 的 master 与 share 版本；
4. 对两个文件执行完整解码；
5. 执行黑帧与冻结检测；
6. 生成九帧 contact sheet；
7. 写出不包含本机绝对路径的便携 JSON 交付报告；
8. 所有条件通过后，再一次性发布到 delivery 目录。

数值检查仍然不能代替人工验收。指南要求查看人物身份、脸部、头发与眼镜、衣服、手部、眨眼、光照、关键发音口型、分段接缝和片尾停留。也就是说，`verified` 证明文件在技术上可交付；人物是否自然、是否像本人、表达是否合适，仍要由人观看。

---

## 08｜我实际验证了什么

我在 macOS 上对当前提交 `c24720a` 运行了仓库的 `tests/smoke.sh`，七组检查全部通过：

- 初始化会复制输入并拒绝覆盖；
- 预检会阻止缺少人工授权的远程步骤，并生成便携报告；
- 状态检查会拒绝没有证据支撑的阶段声明；
- 分段器会在停顿内切分；
- 产物出现后状态才前进；
- finalizer 通过验证后才发布；
- 完整测试任务最终可以到达 `verified`。

GitHub Actions 的 `Validate Skill` 也在当前提交上通过，检查了 metadata、Python 编译与帮助命令、Shell 语法、JSON、绝对路径泄漏和两条路线的 smoke test。

但这个结论必须收窄：测试中的 presenter 是本地 FFmpeg 生成的 synthetic media，不会调用真实 TTS、数字人或口型服务。因此它证明的是 **编排、状态推进和交付工具可运行**，不是人物生成质量，也不是任何供应商已被端到端接通。

---

## 09｜当前仍有三类边界

### 1. 厂商中立，也意味着没有现成适配器

仓库没有固定 provider 的 Python/Node API client。Agent 必须知道当前环境中有哪些能力，并把结果按约定写回任务目录。对已经有工具链的团队，这是可移植性；对只想输入一张照片就出片的用户，这是缺失的一层产品化。

### 2. 测试覆盖了协议，没有覆盖真实人物质量

仓库没有随附原始 presenter 路线的真人样片，也没有跨供应商的身份保持、长时口型、接缝或费用 benchmark。视觉复核清单很完整，但真实服务表现仍需每个使用者单独验证。

### 3. 输入健壮性还有两个已复现的小缺口

当前开放的 [Issue #1](https://github.com/cclank/lanshu-create-ai-presenter-video/issues/1) 报告了两个异常。我在当前提交上都能复现：当 `--job-dir` 指向普通文件时，`init_job.py` 会抛出未处理的 `NotADirectoryError`；当 `supporting_media` 为 JSON `null` 时，`preflight.py` 会抛出 `TypeError`。CI 是绿色的，但还没有覆盖这两个边界输入。

它们不改变主流程设计，但说明“证据门槛严格”与“所有输入都能优雅报错”是两件不同的事。

---

## 10｜它适合谁

它适合已经拥有语音、数字人或口型工具，希望把零散调用变成可审计工作流的个人与团队。尤其适合这些场景：

- 同一套流程需要替换供应商；
- 生成任务昂贵，必须保存 task ID 与重试依据；
- 人物肖像和声音涉及明确授权；
- 任务可能跨会话中断，需要从磁盘状态恢复；
- 成片必须同时交付 master、share、字幕、contact sheet 与 QA 报告。

它不适合把 GitHub 仓库当作一键数字人 App 的用户。你仍需准备外部能力、凭证与人工视觉验收，也要接受某些失败需要改稿，而不是无限自动重试。

---

## 结语：它开源的是“怎样负责地出片”

`lanshu-create-ai-presenter-video` 最值得借鉴的并不是某一种数字人效果，而是把一条经常靠经验和聊天记录维持的生产流程，写成了状态、文件、授权和检查。

输入不是直接奔向生成按钮，而是先通过权利与预算门槛；旁白不是后期附属，而是全片主时钟；远程调用不是黑箱，而是有 task ID、pilot 和重试上限的账目；最终 MP4 也不是完成标志，只有完整解码、响度、黑帧/冻结检测、contact sheet 与人工观看共同组成交付证据。

所以，这个项目不是“开源数字人”。它开源的是一套让 Agent **怎样更可控、更省钱、也更负责任地制作数字人视频**的操作协议。对于 Agent 原生内容生产，这个边界比模型名字更重要。

---

## 主要来源

- [`cclank/lanshu-create-ai-presenter-video`](https://github.com/cclank/lanshu-create-ai-presenter-video)
- [首次开源提交 `04f6bce`](https://github.com/cclank/lanshu-create-ai-presenter-video/commit/04f6bceab888ad923e192fb02542eda06d1fdda8)
- [证据门槛与验证交付加固提交 `c76c6d3`](https://github.com/cclank/lanshu-create-ai-presenter-video/commit/c76c6d3)
- [当前 `SKILL.md`](https://github.com/cclank/lanshu-create-ai-presenter-video/blob/main/SKILL.md)
- [生成与分段指南](https://github.com/cclank/lanshu-create-ai-presenter-video/blob/main/references/generation.md)
- [QA 与恢复指南](https://github.com/cclank/lanshu-create-ai-presenter-video/blob/main/references/qa-recovery.md)
- [Smoke test](https://github.com/cclank/lanshu-create-ai-presenter-video/blob/main/tests/smoke.sh)
- [当前通过的 Validate Skill workflow](https://github.com/cclank/lanshu-create-ai-presenter-video/actions/runs/37442861791)

*审计日期：2026 年 10 月 9 日。Star、Fork、提交状态和开放 Issue 会继续变化。*
