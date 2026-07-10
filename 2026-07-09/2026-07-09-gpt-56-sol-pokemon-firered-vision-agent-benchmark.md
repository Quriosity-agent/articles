---
title: "GPT-5.6 Sol 打通 Pokémon FireRed：Vision-only 长程 Agent 测试，真正测的不是游戏水平"
date: 2026-07-09
source: "https://x.com/Clad3815/status/2075268438025453666"
canonical: "https://x.com/Clad3815/status/2075268438025453666"
tags:
  - GPT-5.6
  - GPT-5.6 Sol
  - Pokémon FireRed
  - Vision Agent
  - Long-Horizon Agent
  - Computer Use
  - Benchmark
---

# GPT-5.6 Sol 打通 Pokémon FireRed：Vision-only 长程 Agent 测试，真正测的不是游戏水平

> **TL;DR:** Clad3815 把 GPT-5.6 Sol 和 GPT-5.5 放进 “GPT Plays Pokémon FireRed” 的 vision-only 条件下比较：只看原始游戏截图，不给 RAM、攻略或提示。作者自报告结果是 GPT-5.6 Sol 用 104h17m active playtime 成为 Champion，而 GPT-5.5 在 218h26m 后停止且未完成。这个结果最值得看的地方不是“模型会玩 Pokémon”，而是它把视觉 grounding、长期记忆、路线规划、错误恢复、菜单操作和稀疏奖励压进了一个大家能直观看懂的长程 agent 测试。

- **Source:** [Clad3815 on X](https://x.com/Clad3815/status/2075268438025453666)
- **Comparison video:** [side-by-side 218h vs 104h run](https://x.com/Clad3815/status/2075268454890766706)
- **Harness reference:** [Clad3815/gpt-play-pokemon-firered](https://github.com/Clad3815/gpt-play-pokemon-firered)
- **Model context:** [OpenAI GPT-5.6 release](https://openai.com/index/gpt-5-6/)
- **Accessed:** 2026-07-10
- **Tags:** GPT-5.6 Sol / Pokémon FireRed / vision-only agent / long-horizon benchmark / computer use / agent harness

![GPT-5.5 vs GPT-5.6 Sol Pokémon FireRed vision-only result chart](imgs/gpt-56-sol-pokemon-firered-vision-agent-benchmark/gpt-56-sol-firered-result.png)

## 一句话概括

**这个 benchmark 真正测的不是模型懂不懂 Pokémon，而是模型能不能在长时间、低带宽、强反馈延迟的视觉环境里持续做对小决策。**

Clad3815 的原推写得很直接：GPT-5.6 Sol vs GPT-5.5，任务是 “GPT Plays Pokémon FireRed” 的 vision-only edition。图里写明条件：full autonomous playthrough from raw screenshots only；no RAM、no walkthrough、no hints。

结果也很醒目：

| 模型 | 条件 | 结果 |
|---|---|---|
| GPT-5.5 | vision-only | 218h26m，stopped / never finished |
| GPT-5.6 Sol | vision-only | 104h17m，became Champion |

回复里还给了一个 24 分钟的 side-by-side 压缩视频，标注为 218 hours vs 104 hours。图表底部说明这是 active playtime，downtime excluded；图上还写着 run 是 `VISION-002`，日期跨度为 2026-06-21 到 2026-07-06。

![GPT-5.5 vs GPT-5.6 Sol side-by-side replay thumbnail](imgs/gpt-56-sol-pokemon-firered-vision-agent-benchmark/side-by-side-video-thumb.jpg)

这不是 OpenAI 官方 benchmark，也不是严格学术论文。但它很有价值，因为它测试的是很多标准榜单很难测出来的东西：视觉输入不完美、目标很远、局部奖励稀疏、错误会滚雪球、状态必须自己维护。

## 为什么 Pokémon FireRed 是一个好玩的长程 agent 测试

Pokémon FireRed 看起来像怀旧游戏，实际对 agent 很刁钻。

它要求模型连续解决几类问题：

- **视觉读取**：识别地图、角色朝向、NPC、菜单、战斗界面、文字框；
- **状态记忆**：记住自己在哪、目标是什么、队伍状态、道具、徽章、已探索区域；
- **导航规划**：穿过城镇、洞穴、建筑、迷宫和 Victory Road；
- **菜单操作**：使用道具、学习技能、切换 Pokémon、治疗、买药；
- **战斗策略**：理解属性、血量、技能、PP、切换和失败后的准备；
- **错误恢复**：走错路、卡住、输掉、忘记目标、被菜单困住后重新定位。

这和很多网页/桌面 agent 任务很像。网页任务里模型要看屏幕、点按钮、读表单、处理弹窗、记住上下文；Pokémon 只是把这些东西放进一个确定但很长的世界里。

更妙的是，它的成功标准直观：你是否成为 Champion。没有太多主观评分空间。

## Vision-only 的意义：去掉拐杖后，剩下的是视觉和行动闭环

Clad3815 早前开源的 `gpt-play-pokemon-firered` 仓库展示过一个更完整的 harness：mGBA 运行游戏，Lua 脚本暴露 socket bridge，Python FastAPI bridge 读取 game memory 并发送输入，Node.js agent loop 管理决策，前端 dashboard 展示日志、minimap、inventory、team、objectives。

这种 harness 很强，也很合理：它能让模型少被像素误读拖死，把更多注意力放到路线和策略上。

但这次图里强调的是 vision-only：raw screenshots only，没有 RAM、攻略或提示。这个变化很关键。它把问题从“模型能否在一个人类工程师精心铺好的状态机里推进游戏”，改成“模型能否只凭屏幕图像建立足够稳定的世界状态”。

这更接近真实 computer use 的难点。真实软件不会总给 agent 一个完美 JSON state。它给的是屏幕、按钮、文本、遮挡、布局变化、错误弹窗和上下文碎片。

## 为什么 104 小时仍然是进步

104h17m 听起来很慢。人类玩家当然不需要这么久。但对 agent benchmark 来说，重点不是 speedrun，而是是否能跨过长期崩溃点。

GPT-5.5 在图中是 218h26m 后未完成。GPT-5.6 Sol 不只是更快，而是完成了。这里的差别可能来自几个能力改进的叠加：

1. **更稳的屏幕理解**：不容易把菜单、地图、NPC 或文字框读错；
2. **更好的目标保持**：更少从主线目标漂移到无关探索；
3. **更强的错误恢复**：卡住后能换策略，而不是重复无效动作；
4. **更低的局部循环概率**：不在同一片区域反复走动；
5. **更好的行动承诺**：知道该推石头、该买药、该治疗时真的执行。

这也和 OpenAI GPT-5.6 发布页的产品叙述能对上。OpenAI 官方说 GPT-5.6 重点提升 agentic workflows、computer use、tool coordination、long-running work，并引入更高 reasoning effort 和 multi-agent ultra 模式。Pokémon 这个社区测试不是官方证据，但它提供了一个很具体的侧面：在一个长时间视觉行动闭环里，模型确实表现出更强的坚持和恢复能力。

## 这个结果不该被过度解读

这里必须加 caveat。

第一，这是社区自报告 benchmark。我们看到了图、推文、视频、开源 harness 参考和 Reddit 转贴，但这不是第三方可重复评测论文。运行设置、prompt、采样参数、人工介入边界、失败重启规则，都需要更完整公开才能严肃比较。

第二，Pokémon FireRed 是互联网上资料极多的游戏。模型没有被实时提供 walkthrough，并不等于它训练时没有见过大量攻略、地图、路线和机制解释。所以它测的是“已知世界里的视觉行动能力”，不是完全新环境泛化。

第三，vision-only 也不等于没有 harness。模型仍然需要一个外部系统给它截图、执行按键、保存历史、控制循环、可能还要维护日志。真正的比较必须说明：模型看到哪些历史？能不能写 notes？每步上下文多长？是否有自动摘要？失败后是否保留记忆？

第四，游戏 benchmark 有观赏性，但也有偏差。它强调导航、菜单、探索和长期坚持，不一定直接代表真实工作里的代码修改、办公自动化、研究分析或网页任务能力。

所以更准确的表述是：这是一条很强的 agent 信号，而不是完整排名。

## 它对 agent 产品有什么启发

这条推文真正提醒的是：未来的 agent 评测会越来越重视“持续行动”，而不是一次回答。

一个好的长程 agent 测试至少要覆盖：

| 能力 | Pokémon 中的表现 | 真实软件中的对应 |
|---|---|---|
| 视觉 grounding | 读屏幕、地图、菜单 | 读网页、UI、文档、表格 |
| 状态维护 | 记住任务、位置、队伍、道具 | 记住项目目标、文件、权限、上下文 |
| 行动闭环 | 按键、战斗、移动、交互 | 点击、编辑、运行命令、提交结果 |
| 错误恢复 | 迷路、失败、循环后修正 | 测试失败、网页变化、权限错误后修正 |
| 稀疏奖励 | 很久之后才拿徽章或通关 | 很久之后才看到任务是否真的完成 |

这也是为什么我一直觉得 harness 才是 agent 产品的核心。模型本身重要，但它能不能持续做好事，取决于外部系统怎么组织观察、记忆、动作、验证、回滚和日志。

Pokémon FireRed 这个测试把这个问题变得肉眼可见：一个模型不是因为一句 prompt 聪明才赢，而是因为它在上万次小循环里少犯足够多的错。

## 下一步应该怎么把它变成更严肃的 benchmark

如果要把这类实验从“很酷的社区演示”推进成更严谨的评测，我会看五件事：

1. **固定协议**：明确模型输入只包含哪些截图、历史、notes 和系统提示；
2. **公开运行日志**：每步动作、截图 hash、模型输出、失败恢复都可审计；
3. **多 seed / 多游戏**：不要只看一条 run，至少多次运行，换 FireRed/Crystal/Emerald/Blue；
4. **分项指标**：完成时间之外，还看循环次数、卡住时长、菜单错误、战斗失败、路线回退；
5. **harness 分层对照**：raw vision、vision + notes、vision + minimap、vision + RAM state 分别跑，拆清楚到底是模型进步还是工具进步。

这会比单一“是否通关”更有信息量。因为 agent 失败往往不是输在最终目标，而是输在一些重复但微小的行为上：看错一个门、忘记一个道具、重复走一条路、明明知道下一步却没有执行。

## 结论

Clad3815 这条 X 的价值，不是告诉我们 GPT-5.6 Sol 会玩 Pokémon，而是给了一个漂亮的长程 agent 信号：

**当模型只看屏幕、没有 RAM、没有攻略、没有提示时，它仍然能在一个复杂游戏世界里持续推进到终点。**

这比很多静态 multimodal benchmark 更接近真实 agent 的难点。真实世界的软件任务也不是一道截图问答题，而是几百上千步观察、判断、行动、修正和继续。

如果这个结果在更公开、更可复现的设置里站得住，那么它说明 GPT-5.6 Sol 的进步不只是“单题更聪明”，而是更接近“能在视觉环境里长期不散架”。这正是下一阶段 computer-use agent 最需要的能力。
