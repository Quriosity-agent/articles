# Stickman Video Director 源码拆解：它不是火柴人视频生成器，而是把 Codex 变成 Gemini 分镜导演的提示词生产线

> **结论先行：** [`donghaozhang/stickman-video-director`](https://github.com/donghaozhang/stickman-video-director) 不会渲染视频，也不直接调用 Gemini。用户提供的地址是 [`kaomei/stickman-video-director`](https://github.com/kaomei/stickman-video-director) 的同步 fork；核心只有一份 Codex Skill 和六份制作规范。它做的事情，是让 Coding Agent 先把文案改写成经过用户批准的导演提案，再输出一组约 10 秒、可以分别交给 Gemini Omni Flash 的独立提示词，最后由人去生成、筛片、拼接和加字幕。它不是 Remotion 式视频引擎，而是一条把“文案、导演决策、跨片连续性和生成提示词”串起来的前期生产线。

![Style 1 Light 官方演示中的黑色火柴人、白色空间与透视场景](imgs/stickman-video-director-codex-gemini-prompt-pipeline/classic-light.jpg)

本文固定审计 2026 年 10 月 13 日的提交 [`544254d`](https://github.com/kaomei/stickman-video-director/tree/544254ddf6430c7d0c35aca4c42211586e39efb0)。审计时，用户 fork 与上游 `main` 指向同一提交；上游有 1,849 stars、284 forks，采用 MIT 许可证，没有版本 tag 或 GitHub Release。数量和状态会变化，技术结论以固定提交为准。

---

## 01 | 先把边界说死：它输出 Prompt，不输出视频

仓库没有 React、Remotion、Canvas、FFmpeg 流水线，也没有 Gemini API、Flow 自动化、MCP server、时间线编辑器或视频拼接代码。安装后，用户在 Codex 中调用 `$directing-stickman-videos`；Skill 最终交付的是：

- 一份导演提案：标题、叙事弧、英文旁白、参考翻译、分镜、运镜、转场、音乐与音效；
- N 条独立英文视频提示词：目标时长每条约 10 秒，`N = 总时长 ÷ 10`；
- 一份拼接指南：每个片段如何接到下一个片段；
- 声线与音乐连续性说明；
- 可选的后期字幕建议，但字幕默认不进入视频模型提示词。

生成仍要在 Google Flow 或其他支持相应模型的工具中完成，费用、失败重试、账号操作和公开发布也不属于 Skill。仓库里的 MP4/GIF 是演示成片，不是本地代码渲染出来的测试结果。

因此，它与 Remotion 的关系很清楚：Remotion 接收 React 代码并确定性渲染每一帧；Stickman Video Director 接收文案，生产给概率视频模型使用的导演包。前者控制像素，后者控制意图。

---

## 02 | 真正的核心不是火柴人，而是“两阶段审批门”

普通 Agent 很容易在用户只给一个主题时，擅自选择 `9:16`、画风和旁白，然后直接交付一大段 Prompt。这个 Skill 故意设置两道门。

**Setup Gate** 要求先获得原始内容、`16:9` 或 `9:16` 画幅，以及明确画风；时长缺失才允许默认 60 秒。用户说“赶时间”“帮我选普通设置”或担心生成费用，都不能跳过这些选择。

**Approval Gate** 把工作拆成两个阶段：

1. Phase A 只输出导演提案，然后停止；
2. 用户明确批准当前版本后，Phase B 才读取完整 Prompt 合同并输出生产提示词。

如果用户改变画幅、时长、画风、旁白或整体方向，旧批准立即失效。把 `9:16` 字符串替换成 `16:9` 不算修改：横屏需要左右调度和横向跟拍，竖屏需要纵深、堆叠运动和手机安全区，Agent 必须重做构图再请求批准。

这个设计的价值不是流程变长，而是把最昂贵的错误挡在视频生成之前。用户先审批低成本的文字方案，再决定是否把六条提示词送去付费模型。

---

## 03 | 60 秒不是一条 Prompt，而是六个独立世界

默认一分钟被拆成六段约 10 秒的生成任务，每段又分为 `[0–3s]`、`[3–7s]`、`[7–10s]` 三个动作节拍。每条 Prompt 都必须自包含，因为视频模型不会自动记得上一轮生成。

这带来一个很具体的工程问题：**如何在六个无状态请求之间复制状态？** Skill 的答案不是只写“same character”，而是把关键状态重复写入每条 Prompt：

- 完整角色锚点、线宽、配色和环境定义；
- 画幅、时长、720p/24 FPS 目标与负面约束；
- 当前片段的第一帧继承状态和最终帧交接状态；
- 原封不动的完整旁白声线块，而不是“沿用上一段声音”；
- 从第一段延续的 BGM 乐器、速度和情绪方向；
- 精确英文台词，只允许作为音频出现，不允许模型改写或画成字幕。

它实际上是在用自然语言做一种“状态序列化”：每个生成请求都带着角色、声音、场景和转场的快照。这不能保证扩散模型服从，但比依赖聊天上下文或一句“保持一致”更可检查。

![Style 2A 用固定红帽、黄衣角色和明亮科技空间建立跨片角色锚点](imgs/stickman-video-director-codex-gemini-prompt-pipeline/modern-studio-tech.jpg)

---

## 04 | 五个已实现风格选项，六个还只是路线图

当前 Skill 真正实现的是四个视觉分支：

| 风格 | 视觉合同 | 适合内容 |
|---|---|---|
| Style 1 Light | 白底、黑色线稿、最多三种强调色 | 科普、心理、商业与概念解释 |
| Style 1 Dark | 黑底、白色线稿、冻结完整角色锚点 | 高对比叙事与抽象解释 |
| Style 2A Modern Studio Tech | 红色冷帽、黄色 T 恤、白色科技空间和青蓝 UI | AI、科技、产品解说 |
| Style 2B Cinematic Story | 同一角色进入彩色电影化场景 | 成长故事、生活与情绪话题 |
| Style 3 Prehistoric Dark Comedy | 史前手绘角色、土色环境、故事内固定演员表 | 职场讽刺、黑色幽默与儿童故事 |

严格来说这是五个可选项，其中 Style 2 共用一套角色 DNA。README 里的 Style 4–9，包括写实 3D 背景、讲台解说、绘本、涂鸦打斗、双人喜剧和卡牌闯关，都明确是未来计划，没有对应 Skill 合同、案例或测试，不能算已经支持。

Style 3 也不是给经典火柴人换一张洞穴背景。它覆盖了通用的“五阶段情绪引擎”，改用铺垫、升级和反转；允许表情与停顿，要求分别冻结每个角色、场景布局和道具所有权。石头从谁手里交给谁、最后落在哪里，也要写入相邻片段，避免凭空复制或瞬移。

![Style 3 官方 30 秒成片的代表帧；标题与字幕由用户在后期加入](imgs/stickman-video-director-codex-gemini-prompt-pipeline/prehistoric-dark-comedy.jpg)

---

## 05 | 为什么要冻结整段声线，而不是写“同一个旁白”

视频模型分别生成六段音频时，“same narrator”并没有共享引用对象。仓库因此把声线拆成身份/年龄、口音、音色、音区、共鸣、粗糙度、气息、表达方式、语速和录音处理，再把批准后的完整英文块逐字复制到每一段。

这是一种合理的 Prompt 工程修复，但证据边界需要保留。仓库报告只记录了一组三段式 Style 2A 男声对比：用户试听后认为新版本像同一个人；Agent 没有拿到音频做独立听评，也没有计算说话人嵌入相似度。女性、老年声线、跨风格、不同主题和更长视频没有同等级供应商实测。

所以“完整声线块”是更强的控制条件，不是声音克隆。若生产要求精确一致，仓库自己也建议在模型支持时使用音频参考，或后期覆盖一条连续外部旁白与 BGM。

---

## 06 | 它比直接让 Codex 写 Prompt 好在哪里

项目最有说服力的不是 Prompt 长，而是它把普通 Codex 容易偷懒的地方变成显式不变量：

| 直接让 Codex 写视频 Prompt | 使用 Stickman Video Director |
|---|---|
| Agent 可能静默选择画幅和风格 | 缺少关键设置就停止并一次问全 |
| 主题通过后可能直接生成最终 Prompt | 当前 Phase A 必须单独批准 |
| 画幅变化可能只是替换字符串 | 强制重新构图、重新审批 |
| 每段写“same character/voice” | 每段重复完整角色和声线状态 |
| 片段各自结束 | 明确保存最终帧并匹配下一段开场 |
| 模型直接生成字幕，容易乱码 | 默认禁止画面文字，字幕留给后期 |
| 失败后容易无限重试 | 要求先做小样，出现身份/动作漂移就停下报告 |

这让 Skill 更像一位执行制片和分镜导演，而不是新模型。它提高的是规划质量、可审核性和生成前的错误发现率；最终人物是否稳定、门会不会变形、声音是否一致，仍由视频模型和人工验收决定。

---

## 07 | 测试做得比一般 Prompt 仓库认真，但不是视频 CI

我在固定提交 `544254d` 上运行了仓库全部三个可执行检查：

| 检查 | 本机结果 | 实际证明什么 |
|---|---|---|
| `verify-readmes.sh` | 6 份 README 合同通过 | 语言入口、章节、安装命令和 12 个演示媒体存在 |
| `verify-classic-character.sh` | 通过 | 当前经典角色锚点和 Prompt 合同包含指定约束 |
| `verify-voice-continuity.py` | 通过 | 示例 Prompt 的完整声线块相等，缩写与冲突声线会被拒绝 |
| 6 个官方 MP4 | FFprobe 均可解码；4 个约 10 秒、2 个约 30 秒，H.264，720p/1080p | 仓库确实保存了可播放案例，不证明 Skill 自动生成它们 |

仓库还保存了一套项目方自建的行为评测。2026 年 8 月的报告显示：没有 Skill 时，五次 fresh-context Codex 都擅自选择设置并越过审批；加入 Skill 后五次都先询问缺失选项并停止，setup gate 从 0/5 提升到 5/5。后续提案、批准、重排和长文压缩场景也被报告为通过。

不过这些报告不是当前提交自动重跑的 CI。仓库没有 GitHub Actions；历史报告仍出现当前 Skill 已不接受的 `1:1`、现在被禁止的十六进制色值与画面文字。声线脚本在 `main` 上运行时，用 `origin/main` 当“旧版本”比较对象，因此它能验证当前结构，却不能在这个环境中独立证明历史内容只改了声音。

最准确的结论是：**仓库对指令回归有真实投入，但自动测试主要检查文字结构；最终视频仍缺少统一的视觉、音频和跨片相似度测试。**

---

## 08 | 官方案例本身也暴露了生成模型的边界

当前合同要求 Style 1 Light 使用平坦、纯白、无纹理、无渐变、无 3D 深度的画布；官方 Light 演示却明显出现透视地面、立体柱体和阴影。这不一定是 Skill 失效，因为演示可能早于当前合同，但它说明案例不能直接当成当前规则逐项通过的回归证据。

Style 3 成片包含标题和中文字幕，而当前合同要求生成画面无文字。项目报告解释这些字幕由用户在生成后拼接时添加，这正好证明最终作品还需要后期层，不能把 MP4 中看到的一切都归功于视频 Prompt。

仓库在这些地方相当克制：经典暗色人物只验证过一个三段焦虑样本，门和道具变形仍未解决；Style 3 只有一个 30 秒职场讽刺得到用户视觉认可；提示词重复不能保证脸、声音或音乐匹配。README 里“突破 60%+ 完播率”的叙事结构目标也没有平台分析数据支持，应理解为创作方法，而不是实测增长指标。

---

## 09 | 最准确的定位

Stickman Video Director 适合已经决定使用 Gemini/Flow 生成短视频，但不想直接把一整分钟文案扔给模型的人。它尤其适合知识解说、励志、心理、科技和轻故事内容：用户先控制叙事与美术方向，Agent 再把批准后的方案编译成一组相互衔接的生成请求。

它不适合需要确定性像素、可编辑时间线、自动批量生成、字幕渲染、成片导出或一键发布的人。这些工作仍需要 Remotion、QCut、剪映、FFmpeg、Flow 自动化或人工剪辑等下游工具。

所以它真正值得借鉴的不是“火柴人”这个外观，而是三件事：**生成前审批、无状态片段的完整状态复制，以及把 Prompt 合规与成片验收分开。** 说白了，它不是一个视频软件，而是一份让 Codex 在昂贵的视频模型前先学会当导演的生产规程。

---

## 主要来源

- [用户提供的 fork：`donghaozhang/stickman-video-director`](https://github.com/donghaozhang/stickman-video-director)
- [上游仓库：`kaomei/stickman-video-director`](https://github.com/kaomei/stickman-video-director)
- [固定审计提交 `544254d`](https://github.com/kaomei/stickman-video-director/tree/544254ddf6430c7d0c35aca4c42211586e39efb0)
- [Skill 核心合同](https://github.com/kaomei/stickman-video-director/blob/544254ddf6430c7d0c35aca4c42211586e39efb0/skills/directing-stickman-videos/SKILL.md)
- [导演提案合同](https://github.com/kaomei/stickman-video-director/blob/544254ddf6430c7d0c35aca4c42211586e39efb0/skills/directing-stickman-videos/references/storyboard-template.md)
- [Omni Flash Prompt 合同](https://github.com/kaomei/stickman-video-director/blob/544254ddf6430c7d0c35aca4c42211586e39efb0/skills/directing-stickman-videos/references/omni-flash-prompt-contract.md)
- [声线连续性合同](https://github.com/kaomei/stickman-video-director/blob/544254ddf6430c7d0c35aca4c42211586e39efb0/skills/directing-stickman-videos/references/voice-continuity.md)
- [无 Skill 基线报告](https://github.com/kaomei/stickman-video-director/blob/544254ddf6430c7d0c35aca4c42211586e39efb0/tests/reports/baseline.md)
- [项目方 forward-test 报告](https://github.com/kaomei/stickman-video-director/blob/544254ddf6430c7d0c35aca4c42211586e39efb0/tests/reports/forward.md)
- [Style 3 证据边界](https://github.com/kaomei/stickman-video-director/blob/544254ddf6430c7d0c35aca4c42211586e39efb0/tests/reports/style-3.md)

*审计日期：2026 年 10 月 13 日。stars、forks、模型名称、Flow 界面、仓库合同和案例会继续变化；技术结论固定到提交 `544254d`。文章图片是从该提交的官方 MP4 演示中抽取的本地帧。本文没有调用 Gemini 重新生成付费视频，也没有独立验证完播率、跨主题人物一致性、声纹相似度或商业生产稳定性。*
