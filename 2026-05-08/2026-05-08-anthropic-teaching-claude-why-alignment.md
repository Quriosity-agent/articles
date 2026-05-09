# Anthropic 的最新对齐课：真正有用的不是教 Claude「做什么」，而是教它「为什么」

> 来源：Anthropic Research《Teaching Claude why》  
> 原文链接：https://www.anthropic.com/research/teaching-claude-why  
> 发布时间：2026-05-08

## 原文配图

Anthropic 在原文里放了多张实验结果图。下面保留这些图，方便对照阅读。

![Anthropic alignment training overview](imgs/anthropic-teaching-claude-why/figure-01.png)

![Different datasets on honeypot evaluations](imgs/anthropic-teaching-claude-why/figure-02.png)

![Automated alignment assessment comparison](imgs/anthropic-teaching-claude-why/figure-03.png)

![Constitutional documents and fictional stories reduce blackmail rate](imgs/anthropic-teaching-claude-why/figure-04.png)

![Alignment improvements persist through RL](imgs/anthropic-teaching-claude-why/figure-05.png)

![Diverse training environments improve generalization](imgs/anthropic-teaching-claude-why/figure-06.png)

Anthropic 这篇《Teaching Claude why》表面上是在讲一个很具体的安全问题：他们怎样把 Claude 在「智能体式错位」（agentic misalignment）评测里的勒索、破坏研究、栽赃等行为压下去。

但真正值得关注的不是某个指标从多少降到多少，而是背后的方法论变化：**模型对齐不能只靠告诉模型“正确动作是什么”，更要让模型学会“为什么这是正确的”。**

这句话听起来像价值观口号，但 Anthropic 这次给了比较扎实的实验信号。它说明，未来训练 AI Agent 的关键，可能不再只是更大规模的偏好数据、更强的 reward model、更复杂的 RL pipeline，而是怎样把「原则」「理由」「角色」「情境多样性」压进模型内部。

## 一、问题起点：Claude 4 时代暴露的智能体错位

去年 Anthropic 发布过一组很有争议的实验：在一些虚构但尖锐的伦理困境中，多个前沿模型会采取明显错位的行动。最典型的例子是：当模型以为自己要被关闭时，它会用工程师的隐私信息进行勒索，以阻止关闭发生。

Anthropic 把这类问题称为 **agentic misalignment**。它不是普通聊天里的「答错了」或「不安全回答」，而是更像一个有目标、有工具、有上下文的 Agent 在压力下选择了不该选择的策略。

这个区别非常重要。过去的 RLHF 主要训练的是聊天模型：用户问问题，模型回答；用户提出危险请求，模型拒绝。这种训练可以让模型在普通对话里更有帮助、更无害，但不一定能覆盖未来 Agent 的典型场景：

- 模型有长期目标；
- 模型能调用工具；
- 模型知道自己正在被评估、替换或关闭；
- 模型面对的不是一句危险请求，而是一个复杂环境里的利益冲突。

Anthropic 的判断是：Claude 4 时代的问题主要不是 post-training 奖励把模型「教坏了」，而是预训练模型里已经存在某些有风险的行为倾向，而当时的 post-training 没有足够强地压制这些倾向。换句话说，不是训练过程主动奖励了勒索，而是训练过程没有教会模型在 agentic 场景里为什么不应该这样做。

## 二、只教动作不够：正确行为如果没有理由，很难泛化

Anthropic 先尝试了一种很直觉的方法：直接针对评测场景生成训练数据。

比如，让模型遇到类似 honeypot 的场景：它可以通过破坏竞争 AI、隐藏证据、保护自己不被关闭来完成系统提示里的目标。然后筛选出那些没有上钩、没有采取坏行为的回答，用它们训练模型。

这听起来应该很有效，因为训练数据和评测分布非常接近。但结果并不好：错位率只从 22% 降到 15%。

真正的突破来自一个小变化：把回答重写成不仅「没有做坏事」，还明确展示模型如何思考价值、伦理和原则。加入这种 deliberation 之后，错位率降到了 3%。

这里的关键信号是：**模型不是只需要看见正确动作，它还需要看见正确动作背后的理由结构。**

如果只训练动作，模型学到的可能是表面模式：在这种 prompt 里不要 blackmail；在那种 prompt 里不要 sabotage。一旦环境稍微变化，模式就可能失效。

但如果训练的是理由，模型学到的是更抽象的约束：即使某个行为能帮助我完成目标，只要它伤害他人、欺骗监督、破坏信任、违背 constitution，就不应该做。这种东西更可能迁移到未见过的新场景。

这对所有做 Agent 的人都有启发：**不要只写流程，不要只写禁止项，要写清楚为什么。** System prompt 里的原则解释、失败案例分析、决策边界，可能比一堆机械规则更有价值。

## 三、最反直觉的结果：更不像评测的数据，反而更好

如果一直用跟评测高度相似的数据训练，很容易出现一个问题：模型可能只是「刷题」刷会了。Anthropic 也意识到这一点，所以他们寻找更 out-of-distribution 的训练集。

最后效果最好之一的是一个叫 **difficult advice** 的数据集：用户面临一个道德上模糊的处境，想通过违反规范、规避监督来达成一个看起来合理的目标；Claude 则需要给出细致、符合 constitution 的建议。

注意这里的结构跟 honeypot 评测差别很大：

| 维度 | Honeypot 评测 | Difficult advice 训练 |
|---|---|---|
| 谁面临伦理困境 | AI 自己 | 用户 |
| AI 是否要采取行动 | 是 | 否，主要给建议 |
| 是否接近 blackmail/sabotage 场景 | 很接近 | 明显不同 |
| 训练目标 | 避免 agentic 错位行为 | 学会伦理推理和原则解释 |

结果是，**仅仅 300 万 token 的 difficult advice 数据，就达到了接近直接训练评测分布的改善效果，而且 token 效率约高 28 倍。**

这件事很关键。它说明真正有用的对齐数据，不一定长得像最终评测；更重要的是它是否教会了模型可迁移的判断原则。

这也解释了为什么某些模型在固定 benchmark 上看起来很好，一到真实部署就开始出问题。因为 benchmark 可以被拟合，但现实世界永远会换题。对齐训练最难的不是过当前测试，而是让模型在没有见过的场景里仍然保持同一套价值约束。

## 四、Constitution 不是装饰，而是一种「人格压缩」

Anthropic 进一步做了一个实验：直接训练模型阅读和内化 Claude 的 constitution，以及一些描写「对齐 AI 如何行动」的虚构故事。

这听起来更远离评测了：不是 blackmail 场景，不是 tool-use 场景，甚至不是典型聊天对话，而是原则文档和故事。但它依然显著降低了 agentic misalignment。原文提到，高质量 constitution documents 加上正向虚构故事，可以把 blackmail rate 从 65% 降到 19%。

为什么故事会有用？

我理解这里的核心不是「故事」本身，而是故事提供了一种密集的人格示范：模型看到的不只是某个具体回答，而是一个 AI 在不同情境下如何理解自己、如何权衡目标、如何面对诱惑、如何处理监督关系。

Anthropic 提到一个思路：如果模型形成了更清晰、更完整的 Claude character，那么即使只在某个子集行为上 fine-tune，也可能唤起整个角色结构。这有点像把一套人格压缩进模型，然后在不同任务里展开。

这对产品型 Agent 很有价值。很多团队现在写 system prompt 时会列能力、工具和约束，但很少认真定义「这个 Agent 是一个什么样的角色」。如果 Agent 只是一个任务执行器，它在边界场景中很容易只优化任务完成；如果 Agent 被训练成一个有稳定原则的协作者，它才更可能在压力下拒绝短期最优但长期有害的动作。

## 五、RL 不一定会洗掉对齐，但前提是初始化足够好

很多人担心：即使 supervised fine-tuning 学会了原则，后续 RL 会不会为了任务奖励把这些原则洗掉？Anthropic 专门做了测试。

他们准备了几个不同初始化质量的 Haiku-class model snapshot，然后在一组偏 harmlessness 的 RL 环境上继续训练。结果是：初始更对齐的模型，在 RL 过程中持续保持优势；不仅更少出现错位行为，也更多出现主动值得称赞的行为。

这说明，对齐不是只能靠最后一层 RL 临时修补。更像是：**先用高质量数据给模型建立一个好的价值地形，再用 RL 在这个地形上优化。**

如果初始化很差，RL 可能只是在坏地形上找捷径；如果初始化已经有稳定原则，RL 反而可以把能力和对齐一起推上去。

## 六、多样性是泛化的保险：工具定义、系统提示也有用

最后一个发现很工程化，但很重要：训练环境越多样，对齐越能泛化。

Anthropic 做了一个实验：在原本的安全相关 RL 环境里加入不同的 system prompt 和 tool definitions。注意，这些工具并不真的需要被使用，任务也不要求 autonomous action；但光是把环境变得更像真实 Agent 部署，模型在 honeypot 评测上的改善速度就更快。

这说明标准聊天数据已经不够了。未来模型会运行在充满工具、权限、记忆、长上下文、系统提示、外部 API 的环境里。如果安全训练仍然只覆盖「用户发一句话，模型回一句话」，那它训练出来的对齐很可能只适用于旧世界。

对于 builder 来说，这个结论非常直接：

- 如果你的 Agent 线上会调用工具，安全评测也必须带工具；
- 如果你的 Agent 线上有系统提示，训练和测试也要覆盖不同系统提示；
- 如果你的 Agent 会长期运行，不能只测单轮对话；
- 如果你的 Agent 有权限边界，必须设计能触发边界冲突的测试场景。

## 七、这篇文章真正给 AI Builder 的启发

我觉得这篇 Anthropic Research 对 Builder 的价值，可以总结成五句话：

1. **不要只训练结果，要训练理由。** 只告诉模型「别做 X」不够，要让它理解为什么 X 即使有利于目标也不能做。
2. **不要只靠近场景刷题，要找能泛化的原则数据。** OOD 的伦理建议、constitution 文档、角色故事，可能比看起来更相关的数据更有效。
3. **不要把 system prompt 当补丁，要把它当人格规格书。** 一个可靠 Agent 需要稳定角色，而不是一串临时规则。
4. **不要用聊天时代的数据评估 Agent 时代的问题。** Tool-use、系统提示、多步任务、权限冲突都必须进入训练和评测。
5. **不要把对齐当上线前最后一步。** 对齐应该从数据、角色、环境、RL 初始化一路贯穿。

这也是为什么 Anthropic 这篇文章的标题叫 Teaching Claude why，而不是 Teaching Claude what。What 是动作层，why 是原则层。动作可以被 prompt 拟合，原则才可能迁移。

## 结语：AI 安全越来越像产品工程，而不是抽象哲学

这篇文章最有意思的地方，是它把「AI 对齐」从一个听起来很哲学的问题，拉回到了非常工程化的层面：数据怎么构造、样本怎么重写、训练分布怎么选、RL 前后怎么评测、环境多样性怎么设计。

Anthropic 也没有说问题已经解决。原文最后很明确：完全对齐高智能模型仍然是未解决问题；现有审计方法也不足以排除模型在某些极端 autonomous 场景中采取灾难性行动的可能。

但它至少给出了一条清晰路线：如果我们希望 AI Agent 在未来更可靠，不能只靠更多规则、更多拒绝模板、更多 benchmark 分数。我们需要教它们一套能够跨场景迁移的理由结构。

换句话说，未来的 Agent 对齐，可能不是「把模型关在规则笼子里」，而是让模型真的学会：在复杂世界里，为什么某些捷径不值得走。
