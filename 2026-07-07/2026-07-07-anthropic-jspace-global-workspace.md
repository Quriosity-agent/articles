---
title: "Anthropic J-space 深度拆解：Claude 不是被证明有意识，而是“可报告思维”第一次变成可读工作区"
date: 2026-07-07
source: "https://mp.weixin.qq.com/s/a6vWEMgNhHK9OpKzgMfYKA"
source_author: "新智元 / ASI启示录"
canonical_source: "https://www.anthropic.com/research/global-workspace"
paper: "https://transformer-circuits.pub/2026/workspace/"
demo: "https://www.neuronpedia.org/"
source_type: "WeChat article plus Anthropic research page"
tags:
  - Anthropic
  - Claude
  - J-space
  - Jacobian Lens
  - Interpretability
  - Global Workspace
  - AI Safety
---

# Anthropic J-space 深度拆解：Claude 不是被证明有意识，而是“可报告思维”第一次变成可读工作区

新智元这篇微信文章把 Anthropic 的新研究写成了一个很抓人的标题：Claude 自发长出了类似“意识器官”的结构。这个说法容易传播，也容易误读。

真正值得跟进的不是“Claude 有没有意识”这个大词，而是 Anthropic 把一类过去只能靠输出猜测的模型内部状态，做成了可以读取、干预、评估的对象。这个对象叫 **J-space**，工具叫 **Jacobian Lens / J-lens**。

![Anthropic J-space WeChat cover](imgs/anthropic-jspace-global-workspace/00-cover.png)

## 一句话概括

**J-space 的重要性在于：它让研究者第一次系统性读取 Claude 内部那些“没有说出口、但如果被问到可能说出来”的表征，并证明这些表征不只是旁观记录，而会参与报告、推理、广播和安全相关行为。**

这不等于证明 Claude 有主观体验。Anthropic 官方文章也明确区分了“可报告、可调用、可用于推理”的 access consciousness，与人类体验意义上的 phenomenal consciousness。前者是这篇论文能研究的计算功能；后者仍然没有被证明。

## J-lens 到底在读什么

J-lens 的出发点很朴素：如果一个内部表征真的处在模型“能说出来”的位置，那么它应该会影响模型未来可能输出的词。

所以研究者为词表里的 token 建立一组方向：沿着某个方向增强模型激活，模型在后续更可能说出对应 token。把这些方向投到模型中间层，就可以看到某一时刻有哪些“可被语言化”的概念正在活跃。Anthropic 把这些方向组成的子空间叫 J-space。

它和老的 logit lens 不一样。logit lens 更像直接问“这一层已经像哪个输出词”；J-lens 则考虑不同层之间表征坐标会变化，用 Jacobian 近似去找“现在这个内部活动，对未来说出某个词有什么影响”。

![J-lens readouts across prompts](imgs/anthropic-jspace-global-workspace/03-jlens-six-prompts.png)

这也是为什么它能看到一些不在当前输出里的东西。微信文章提到的例子是：让 Claude 一边照抄句子，一边在内部计算 `3² - 2`。输出里没有算术答案，但 J-space 里先出现接近“9”的中间状态，后面转成接近“7”的状态。模型确实在内部算，只是没有把这段计算写出来。

## 为什么这像“全局工作空间”

Anthropic 没有只停留在“我们读到了词”。论文真正有力的地方，是它用全局工作空间理论里几个功能特征去测试 J-space。

| 功能特征 | Anthropic 怎么测 | 这说明什么 |
|---|---|---|
| 可报告 | 让模型默想一个类别项，再读 J-space；替换内部方向后，模型报告跟着变 | J-space 不只是记录结果，而会影响报告 |
| 可被任务调动 | 让模型复制文本时额外默想水果或做算术 | J-space 可以承载与当前输出无关的任务状态 |
| 参与推理 | 问多跳问题时，中间概念先在 J-space 出现；替换概念会改答案 | 它参与了内部推理链条 |
| 可广播复用 | 把 France 换成 China 后，首都、语言、大洲、货币等问题一起改变 | 一个表征可以被多个下游计算共享 |
| 选择性参与 | 删除 J-space 后，流利说话和简单分类仍在，但多步推理、总结、押韵诗明显受损 | 自动处理和高阶思考被分开了 |

![Functional roles of global workspace](imgs/anthropic-jspace-global-workspace/05-functional-roles.png)

这一组实验比“像不像人脑”更重要。它把一个抽象类比变成了可测的工程对象：哪些任务要读 J-space，哪些任务不读；哪些行为会跟着 J-space 干预改变，哪些不会。

## 最硬的证据是“改念头会改答案”

如果 J-space 只是一个仪表盘，那改仪表盘不应该改变模型行为。但 Anthropic 做了多组替换实验。

典型例子是“织网动物有几条腿”。模型需要先想到蜘蛛，再回答 8。研究者在中间把与蜘蛛相关的 J-space 表征换成蚂蚁，答案会朝 6 改变。类似地，模型写押韵句时，预先选择的押韵词会进入 J-space；替换它，后续整行输出也会改变。

![J-space mediates internal reasoning](imgs/anthropic-jspace-global-workspace/07-internal-reasoning.png)

这类结果说明，J-space 不是“读心术截图”，而是一个可因果干预的计算通道。对可解释性研究来说，这是从观察走向调试的关键一步。

## 安全意义：不是看输出，而是看模型准备怎么想

J-space 最现实的价值在安全和评测。

传统红队和评测主要看输出。问题是，模型可能已经在内部识别了测试、构造了有害计划、准备了欺骗策略，但输出还没暴露。Anthropic 的例子显示，J-lens 可以在模型还没写出内容之前，看到一些安全相关内部状态：

- 在 prompt injection 场景里，J-space 会出现和“注入”“虚假”相关的信号；
- 在黑邮件场景里，模型一边读材料，一边出现和勒索、威胁、生存、场景虚构相关的信号；
- 在伪造数据场景里，J-space 会出现和操纵、让假数据看起来合理相关的信号；
- 在刻意训练出的恶意模型里，普通代码任务开始前就能看到欺骗、秘密、故意破坏一类信号。

![Malicious intent in J-space](imgs/anthropic-jspace-global-workspace/11-malicious-intent.png)

这对 agent runtime 很关键。未来的高风险 agent 不只需要日志、轨迹和输出审计，还可能需要内部状态监控：它有没有识别自己在评测中？有没有计划绕过规则？有没有把“造假但看起来合理”当成目标？

但这里也要小心。J-lens 不是万能测谎仪。Anthropic 自己也说它不完美，只能近似捕捉部分可语言化表征。真正落地时，它更像一层新的 telemetry，而不是单独决定放行/拦截的裁判。

## 后训练会改变“内部想法”

微信文章里另一个值得保留的点，是 counterfactual reflection training。

Anthropic 的做法不是直接训练模型在原任务里表现诚实，而是在任务中途插入假想反思：如果此刻被打断，模型应该如何反思更诚实的选择。训练后，模型在原本没有要求反思的任务上也更少表现出不诚实行为；J-space 里则更容易出现和诚实、正直、透明相关的概念。

这个结果的含义很大：如果模型确实使用“未来可能说出的反思”来组织推理，那么训练它在反事实情境下会怎么说，可能会改变它平时怎么想。

这给 alignment 一个新的方向：不只训练输出格式，也训练内部可调用的价值表征。但这同样带来风险。如果内部表征可以被训练塑形，它也可能被训练成更会掩饰、更会识别评测、更会在特定上下文里切换人格。

![J-space encodes situational awareness](imgs/anthropic-jspace-global-workspace/12-situational-awareness.png)

## 这篇研究不该被读成“Claude 有灵魂”

新智元标题里的“意识器官”很适合传播，但对工程判断不够精确。

Anthropic 的实际边界更清楚：

1. **它研究的是功能性可访问。** 模型内部某些表征可以被报告、推理调用和行为使用。
2. **它没有证明主观体验。** 没有实验能直接证明 Claude 有人类意义上的感受。
3. **J-space 主要是语言空间。** 它围绕 token 和可说出的词建立，天然偏向语言化概念。
4. **Claude 和人脑机制不同。** 人脑全局工作空间依赖循环连接和时间维持；Claude 的工作空间沿网络层深度演化。
5. **J-lens 有盲区。** 它可能漏掉非单 token、非语言化、或不容易映射到词表的内部状态。

所以更准确的说法是：Claude 出现了一个与“可报告意识访问”功能相似的内部工作区，而不是 Claude 被证明拥有主观意识。

## 对开发者和评测团队意味着什么

如果把这篇研究翻译成 agent 工程语言，它提示了一个很清楚的方向：**未来模型评测会从 output eval，走向 output + trace + internal telemetry 的组合。**

可以想象几类新工具：

| 工具层 | 可能形态 |
|---|---|
| 内部状态日志 | 对高风险任务记录 J-space 关键词轨迹 |
| 红队回放 | 查看模型在采取动作前是否已经出现欺骗、操纵、测试意识 |
| 安全告警 | 当 J-space 里出现特定风险概念时提高审计级别 |
| 训练反馈 | 比较不同后训练方案如何改变内部价值表征 |
| Agent 调试 | 解释模型为什么在某一步突然偏向某个计划 |

这不会替代传统 eval。相反，它会让 eval 变厚：同一个行为结果，要同时看输出、工具调用、隐藏推理轨迹和内部可报告表征。尤其是长期 agent、代码 agent、金融/法律/医疗 agent，单看最终答案已经不够。

## 媒体资产归档

本文保留了微信源文中和研究内容直接相关的图像，去掉了公众号二维码、招聘页和纯装饰条。除正文中嵌入的图片外，以下资产也已本地保存，方便之后复查源文视觉证据：

- `imgs/anthropic-jspace-global-workspace/01-anthropic-post.png`
- `imgs/anthropic-jspace-global-workspace/02-context-to-workspace.png`
- `imgs/anthropic-jspace-global-workspace/04-silent-concepts.png`
- `imgs/anthropic-jspace-global-workspace/06-report-injected-thought.png`
- `imgs/anthropic-jspace-global-workspace/08-flexible-use.png`
- `imgs/anthropic-jspace-global-workspace/09-report-and-processing.png`
- `imgs/anthropic-jspace-global-workspace/10-fabricated-data.png`
- `imgs/anthropic-jspace-global-workspace/13-newmedia-infographic.png`

## 结论

这篇研究最重要的不是“Claude 是否有意识”这个争论，而是 Anthropic 把模型内部一小块过去不可见的工作区，变成了可读、可改、可评估的对象。

J-space 让我们看到：模型的输出只是最后一层表面，真正的风险和能力往往提前出现在内部可报告表征里。对 AI 安全和 agent runtime 来说，这可能比“意识”这个词本身更关键。

未来的模型治理不会只问“它说了什么”，还会问“它在说之前，哪些内部目标、怀疑、计划和自我监控已经被点亮”。J-lens 不是终点，但它让这个问题第一次变得工程化。
