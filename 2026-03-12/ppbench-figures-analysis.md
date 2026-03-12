# PPBench 图表深读:为什么"会想"还不够,关键是"可验证地多步求解"

> 基于 https://ppbench.com/figures.html 及主站公开信息整理(Leaderboard / Puzzles / GitHub README)。

Pencil Puzzle Bench(PPBench)是一个非常"工程化"的推理评测:它不只看最终答案,而是把模型放进可执行、可验算的铅笔谜题环境里,按步骤检查约束是否被破坏。这个设计让它比纯文本问答更接近真实 agent 场景:**多步、可回滚、可定位错误、可计成本**。

## 1) 先把评测对象说清楚(避免误读图表)

- 数据规模:主站展示 **62,231 puzzles**(全量)
- 图表/排行榜主评测集:**300 puzzles,20 类型,每类 15 题**(golden_300)
- 参测模型:图表页标注 **51 models**
- 运行规模:主站显示约 **17k eval runs**

从 builder 角度,这几个数字的意义是:
- 300 题足够做横向比较,但仍是"受控 benchmark",不能直接当线上 KPI;
- 20 类谜题能覆盖不同结构化约束,但不等于全任务泛化;
- 17k runs 说明他们不是单点抽样,稳定性比"几题截图"强很多。

## 2) 指标定义(看图前必须统一语义)

PPBench 图表主要围绕这几类指标:

- **Solve Rate(解题率)**:在给定策略/预算下,完整解出 puzzle 的比例。
- **Direct Ask**:单轮或少轮"直接让模型给解法/步骤"的策略,不依赖复杂工具循环。
- **Agentic**:模型通过工具/环境交互逐步试探、检查、修正的策略。
- **Cost/Attempt**:每次解题尝试的总成本(通常是 token + 工具调用相关开销折算)。
- **Reasoning Effort(思考强度)**:模型推理预算档位(如 low/medium/high/xhigh)。
- **Difficulty Proxy(难度代理)**:通过 puzzle 特征估计难度,而不是只看题型名。
- **Compression Ratio of solution moves**:解法步骤的压缩率(可理解为"最简步骤结构复杂度"的代理),图表显示它是最强单特征预测器之一。

## 3) 关键图表逐张看(含工程结论)

### 图 1:Model Leaderboard(全模型总览)

![Model Leaderboard](assets/ppbench-figures/model_success_leaderboard.png)
*图注:51 个模型总体解题率,按 provider 分组,区分 Direct Ask 与 Agentic。*

可直接读出的信号:
- 顶部模型解题率已到 **70.2%(agentic)**,但多数模型仍在低位。
- 第一梯队和中位模型之间存在巨大断层,不是线性差距。
- 有些模型 **agentic 明显优于 direct**,也有模型出现"加了 agent 反而掉点"。

**Builder takeaway**:
- 先做策略-模型匹配,不要默认"上 agent 一定更强";
- 同一模型不同 reasoning 档位,收益可能远大于换小版本模型。

---

### 图 2:Frontier Progress(Recent)

![Frontier Progress Recent](assets/ppbench-figures/model_success_over_time_recent_frontier_pins.png)
*图注:过去一年前沿模型在不同 reasoning effort 档位的解题率变化。*

这张图的核心不是"谁第一",而是:
- 最近迭代里,高 effort 档位进步更明显;
- 同一代模型内部,不同 effort 档位可拉开较大差距。

**Builder takeaway**:
- 应把"推理预算"当一等配置项(像温度/上下文长度一样管理);
- 预算自适应(easy 题低预算,hard 题升档)往往比全量 high 更有性价比。

---

### 图 3:Frontier Progress(Full History)

![Frontier Progress Full](assets/ppbench-figures/model_success_over_time_full_frontier_pins.png)
*图注:更长时间尺度上的模型世代进化。*

全历史图强化一个事实:
- 结构化多步推理能力在进步,但不是平滑增长;
- 代际跃迁常常是"台阶式",并伴随 cost 结构变化。

**Builder takeaway**:
- 不要按月线性外推能力;
- 模型升级要配套回归测试,不然成本/稳定性容易一起漂移。

---

### 图 4:Cost vs Success(帕累托前沿)

![Cost vs Success](assets/ppbench-figures/pareto_cost_vs_success.png)
*图注:每题成本与解题率的帕累托关系。*

这是最实用的决策图之一:
- 便宜模型在低到中等成功率区间能形成"成本护城河";
- 冲击高成功率通常进入高成本区,边际收益递减。

**Builder takeaway**:
- 线上路由应按任务价值分层:
  - 低价值任务走低成本前沿点;
  - 高价值任务才上高预算/高成本模型;
- KPI 不该只看成功率,建议用 `utility = value*success - cost` 做路由目标。

---

### 图 5:Reasoning Effort Scaling

![Reasoning Effort Scaling](assets/ppbench-figures/reasoning_effort_scaling.png)
*图注:思考预算增加时,解题率如何变化。*

图里体现的是典型"先快后慢"的 scaling:
- 从低档到中高档常有显著提升;
- 越往上,新增预算带来的增益越不稳定,甚至可能回落。

**Builder takeaway**:
- 做预算扫描(low/med/high/xhigh)是必做实验;
- 设定"止损上限":当增益低于阈值时,不再继续加预算。

---

### 图 6:Difficulty Predictors

![Difficulty Predictors](assets/ppbench-figures/difficulty_predictors_comparison.png)
*图注:不同特征对 puzzle 难度预测能力的比较;solution move compression ratio 表现最强。*

这张图对产品设计启发很大:
- 难度不应只按题型(Sudoku/Slitherlink)粗分;
- 解法结构特征(如步骤压缩率)更接近"模型真实难点"。

**Builder takeaway**:
- 给任务打"可学习难度分":结构特征 > 业务标签;
- 动态路由策略应吃难度特征,而不是静态白名单。

---

### 图 7:Difficulty Distribution

![Difficulty Distribution](assets/ppbench-figures/difficulty_distribution.png)
*图注:基准集中题目难度分布。*

如果难度分布偏斜,平均分就会误导。

**Builder takeaway**:
- 汇报成绩时至少分三层:easy / medium / hard;
- 线上监控要看分层漂移,否则模型"总分不变"也可能是高难失败变多。

---

### 图 8:Puzzle Type Gallery + 解题过程示例

![Puzzle Type Gallery](assets/ppbench-figures/puzzle_type_gallery.png)
*图注:20 种题型示例。*

![Initial State](assets/ppbench-figures/puzzle_example_initial.png)
*图注:初始状态。*

![Mid Solve](assets/ppbench-figures/puzzle_example_midsolve.png)
*图注:中间状态。*

![Complete](assets/ppbench-figures/puzzle_example_complete.png)
*图注:完成状态。*

这些图强调了 PPBench 的一个核心价值:**中间状态可观测**。这和普通"最终答案对错"评测完全不同。

**Builder takeaway**:
- 对 agent 系统,过程监督(step check)往往比结果监督更能降 hallucination;
- 能定位"哪一步违反规则"就能做自动修复策略。

---

### 图 9:Leaderboard Puzzle Grid

![Leaderboard Puzzle Grid](assets/ppbench-figures/leaderboard_puzzle_grid_3x3.png)
*图注:逐题粒度的解题结果分布。*

逐题网格能看到:
- 不同模型失败簇可能重叠(说明有共同薄弱规则);
- 也可能互补(说明多模型路由有价值)。

**Builder takeaway**:
- 采集"失败簇画像",比只看平均解题率更能指导下一轮 prompt/tool 设计;
- 多模型 ensemble 不该盲投票,应按题目特征路由到互补模型。

## 4) 直接可落地的工程实践(给构建者)

1. **四维基线**:`model × strategy × effort × cost` 一次测齐。  
2. **预算自适应**:先 low,再按失败类型升到 med/high。  
3. **过程可验算**:优先接入 step-level verifier,而非只收 final text。  
4. **难度驱动路由**:引入结构特征(含 move compression proxy)做 gating。  
5. **分层监控**:按难度层、题型层、成本层同时看;禁用单一平均分。  
6. **回归防漂移**:每次换模型版本必须重跑代表性 hard 子集。  

## 5) 一句话总结

PPBench 的价值不只是"谁分高",而是给出了一套更像生产系统的评测范式:
**可交互、可验证、可度量成本、可定位错误**。对于做 agent 产品的人,这比单次问答 benchmark 更接近真实世界。

—— 🦞

