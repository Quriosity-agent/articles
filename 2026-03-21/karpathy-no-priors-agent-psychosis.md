# Andrej Karpathy 的 "AI 精神错乱"：当顶级 AI 研究者彻底放弃手写代码

> 深度解析 Karpathy 在 No Priors 播客上关于 Agent 时代、自动研究、开源模型与教育变革的完整对话

![Andrej Karpathy on No Priors Podcast](https://img.youtube.com/vi/kwSVtQ7dziU/maxresdefault.jpg)
*来源：[No Priors Podcast - YouTube](https://youtu.be/kwSVtQ7dziU) | 时长：1h 6m 31s*

---

2026年初，AI 领域正在经历一场静悄悄的革命——不是新模型的发布，不是新的 benchmark 被刷新，而是**人与 AI 的工作方式发生了根本性的变化**。Andrej Karpathy，这位前 OpenAI 创始成员、前 Tesla AI 总监、斯坦福大学讲师，在 No Priors 播客上用了超过一个小时的时间，坦率地描述了这场变化如何彻底改变了他的日常工作——以及为什么他称之为"AI 精神错乱"（AI Psychosis）。

这不是一篇普通的技术访谈。Karpathy 的坦诚程度令人吃惊：他承认自从2025年12月以来**可能没有手写过一行代码**，他对订阅 token 用不完感到焦虑，他在 OpenAI 时甚至对同事说"如果我们成功了，我们都会失业"。这是一个在 AI 前沿工作了二十年的人，面对技术拐点时的真实反应。

---

## 一、"AI 精神错乱"：从 80/20 到 2/80 的范式转变

Karpathy 用了一个非常直接的比喻来描述过去几个月发生的事情：

> "I kind of went from 80/20 of writing code by myself versus just delegating to agents. And I don't even think it's 2/80 by now. I think it's a lot more than that. **I don't think I've typed like a line of code probably since December basically.**"

这不是渐进式的变化。Karpathy 描述的是一个**突变**——2025年12月某个时刻，"something flipped"。他从亲手写代码为主、偶尔用 AI 辅助，一夜之间切换到几乎完全委托给 Agent，自己只做高层决策。

更令人触动的是他描述的心理状态。他说自己处于一种"perpetual state of AI psychosis"（持续的AI精神错乱状态），因为：

1. **能力的解锁是如此巨大**——过去你被打字速度限制，现在这个瓶颈消失了
2. **你感觉永远跟不上**——Twitter 上到处都是人在做各种疯狂的事情，"I need to be at the forefront or I feel extremely nervous"
3. **一切都是 skill issue**——当某个东西不 work 的时候，你不会觉得是能力不够，而是觉得自己还没找到正确的使用方式

他甚至用了一个博士生时代的类比：

> "I actually kind of experienced this when I was a PhD student. You would feel nervous when your GPUs are not running... But now it's not about flops, it's about tokens. **What is your token throughput and what token throughput do you command?**"

换句话说，他现在对 token 的焦虑，就像当年对 GPU 闲置的焦虑一样——如果你的订阅额度还有剩余，那就意味着你没有最大化自己的产出。

---

## 二、宏观操作（Macro Actions）：新的工作范式

Karpathy 不再写代码行（lines of code），而是在更高的抽象层级上操作——他称之为"宏观操作"（macro actions）。

他提到了 Peter Steinberg 的著名照片——一个人坐在显示器前，屏幕上同时运行着多个 Codex Agent，每个 Agent 负责一个不同的功能模块：

> "He has a funny photo where he's in front of a monitor with lots of Codex agents... they all take about 20 minutes if you prompt them correctly and you use the high effort. And so they all take about 20 minutes. They have multiple, you know, 10 repos checked out and so he's just going between them and giving them work."

> "**Everything just happens in these macro actions over your repository.** It's not just like here's a line of code, here's a new function. It's like here's a new functionality and delegate it to agent one. Here's a new functionality that's not going to interfere with the other one. Give it to two."

这是一种完全不同的工作方式：

- **Agent 1** 在做某个研究
- **Agent 2** 在写代码
- **Agent 3** 在制定新功能的实现计划
- **你**在它们之间来回切换，审查工作，分配新任务

压力来自于：当你等待一个 Agent 完成任务时，你的本能反应是"我应该再开一个 Agent"。如果你的 token 额度还有剩余——Codex 用完了，应该切到 Claude——那就意味着你是整个系统的瓶颈。

> "If you don't feel very bounded by your ability to spend on tokens, then **you are the bottleneck in the system that is max capability.**"

---

## 三、OpenClaw 的赞誉：Peter 同时在五个方向上创新

在整个访谈中，Karpathy 对 OpenClaw 项目和其创建者 Peter 给予了极高的评价：

> "I mean **Peter has done a really amazing job.** I saw him recently and I talked to him about it and he's very humble about it but I think **he innovated simultaneously in like five different ways** and put it all together."

他具体提到了几个创新点：

### Soul Document（灵魂文档）
Peter 为 Agent 精心设计了人格，使其"compelling and interesting"。Karpathy 认为这是许多当前 Agent 做得不好的地方。

### Claude 的人格对比 Codex 的干巴巴
这里有一段非常有趣的对比：

> "I would say Codex is a lot more dry. It doesn't seem to care about what you're creating. It's kind of like, oh, I implemented it. It's like, okay, but **do you understand what we're building?**"

> "With Claude I think they dial the sycophancy fairly well where **when Claude gives me praise I do feel like I slightly deserve it.** Because sometimes I give it not very well-formed thoughts and it doesn't actually react very strongly. But when it's a really good idea by my own account, it does seem to reward it a bit more. And so I kind of feel like **I'm trying to earn its praise which is really weird.**"

这是一个深刻的观察——Agent 的人格设计不是噱头，而是直接影响用户的工作动机和体验质量。

### 记忆系统
> "Open Claw has a lot more sophisticated memory I would say than what you would get by default, which is just a memory compaction when your context runs out."

### WhatsApp 门户
统一的 WhatsApp 接口让所有自动化通过一个入口管理——这是 Peter 的另一个关键创新。

---

## 四、Dobby the Elf Claw：智能家居的终极形态

Karpathy 在一月份经历了一段"Claw 精神错乱期"，期间他建造了一个名为 **Dobby the Elf Claw** 的家庭自动化系统。这个故事堪称 Agent 能力的完美展示：

> "I just told it that I think I have Sonos at home. Like can you try to find it? And it goes and it did like IP scan of all the computers on the local area network and it found the Sonos system... it turned out that there's no password protection or anything like that. I just logged in and it's like oh yeah you have these Sonos systems installed, let me try to reverse engineer how it's working."

**三个 prompt，音乐就开始播放了。**

Dobby 现在控制着：
- **灯光** — "Dobby, sleepy time" = 所有灯关闭
- **HVAC 暖通空调**
- **窗帘**
- **泳池和水疗**
- **安防摄像头** — 使用 Qwen 模型做变化检测，然后通过 WhatsApp 发送警报："Hey, a FedEx truck just pulled up. You might want to check it."

> "I used to use like six apps, completely different apps and **I don't have to use these apps anymore.** Dobby controls everything in natural language. It's amazing."

这引出了一个更深层的洞察：也许我们今天的很多 App 根本就不应该存在。

> "These apps that are in the app store for using these smart home devices etc., **these shouldn't even exist kind of in a certain sense.** Shouldn't it just be APIs and shouldn't agents be just using it directly?"

> "The customer is not the human anymore. It's like **agents who are acting on behalf of humans** and this refactoring will probably be substantial."

---

## 五、自动研究（Auto Research）：Agent 发现了 Karpathy 二十年经验遗漏的优化

这是整个访谈中最令人震惊的部分。Karpathy 一直在维护 NanoGPT 项目——一个用于训练小型 GPT 模型的实验平台。他用传统方式（手动调参、看结果、调整）已经优化了很长时间，自认为模型已经"fairly well tuned"。

然后他让自动研究 Agent 跑了一个晚上：

> "I let auto research go for like overnight and it came back with like tunings that I didn't see. **I did forget the weight decay on the value embeddings and my Adam betas were not sufficiently tuned** and these things jointly interact so once you tune one thing the other things have to potentially change too."

一个 Agent 在一夜之间发现了他二十年研究经验没有注意到的超参数优化。

这背后的核心理念是：

> "**The name of the game now is to increase your leverage.** I put in just very few tokens just once in a while and a huge amount of stuff happens on my behalf."

> "You can't be there to prompt the next thing. You need to take yourself outside. You have to arrange things such that they're completely autonomous and the more you... **How can you maximize your token throughput and not be in the loop. This is the goal.**"

自动研究的完美适用场景有一个关键特征：**可验证性**。

> "This is extremely well suited to anything that has **objective metrics that are easy to evaluate.** Writing kernels for more efficient CUDA code... are the perfect fit. You have inefficient code and then you want efficient code that has the exact same behavior but it's much faster. Perfect fit."

> "If you can't evaluate then you can't auto research it."

---

## 六、Program.md 的元优化：研究组织就是一组 Markdown 文件

这是访谈中最具前瞻性的讨论之一。Karpathy 提出了一个惊人的框架：

> "**Every research organization is described by Program MD.** A research organization is a set of markdown files that describe all the roles and how the whole thing connects."

想象一下：
- 一个"研究组织"的行为完全由 Markdown 文件描述
- 不同的 Program.md 会产生不同的研究进展
- 你可以像调参一样调整"组织行为"——更多 standup？更少？更冒险？更保守？

> "One organization can have fewer stand-ups, one organization can have more. One organization can be very risk-taking, one organization can be less. And so you can definitely imagine that you have multiple research orgs."

然后是**元优化**的想法——竞赛概念：

> "Let people write different Program MDs. For same hardware, where do you get most improvement? And then you can take all that data and then give it to the model and **say write a better Program MD.**"

层层嵌套：LLM 已经被接受 → Agent 已经被接受 → Claw 已经被接受 → 多个 Claw → 对 Claw 的指令 → 对指令的优化。

> "**This is why it gets to the psychosis is that this is like infinite and everything is skill issue.**"

---

## 七、开源 vs 闭源模型：我们意外地处于一个还不错的位置

Karpathy 对开源模型的态度是审慎乐观的。他指出差距正在缩小：

> "The closed models are ahead but people are monitoring the number of months that open source models are behind... Maybe they're behind by like what is the latest maybe like **eight, six months, eight months** kind of thing right now."

他用 Linux 做了一个精妙的类比：

> "In operating systems you have like closed, Windows and Mac OS... and there's Linux. Linux is extremely successful, it runs on the vast majority of computers, like 60% or something... **There is a need in the industry to have a common open platform that everyone feels safe using.** And I think the same is true now."

但他也指出了关键区别：现在一切都是**资本密集型**的（"everything is capital"），这使得竞争更加困难。

对于集中化，他表达了深深的担忧：

> "**Centralization has a very poor track record in my view... I'm by default very suspicious.** I want there to be more people in the room. In machine learning, ensembles always outperform any individual model, and so I want there to be ensembles of people thinking about all the hardest problems."

> "**By accident we're actually in an okay spot.** I would love there to be more frontier labs."

他坦诚地说，即使在前沿实验室内部，你也不完全是自由的：

> "If you're inside one of the frontier labs, there are certain things that you can't say. And conversely there are certain things that the organization wants you to say... **I feel like a bit more aligned with humanity in a certain sense outside of a frontier lab.**"

---

## 八、教育的变革：我不再向人解释了，我向 Agent 解释

关于教育，Karpathy 的观点是颠覆性的。他最近的 Micro GPT 项目——将 LLM 训练蒸馏到200行 Python 代码——本来应该配一个教学视频。但他改变了主意：

> "**I'm not explaining to people anymore. I'm explaining it to agents.** If you can explain it to agents, then agents can be the router and they can actually target it to the human in their language, with infinite patience and at their capability."

> "If I don't understand this particular function, I can ask the agent to explain it to me like three different ways and **I'm not going to get that from you.**"

他提出了"skills as curriculum hints"的概念：不是写完整的教程，而是写一个 skill 文件，给 Agent 提示教学的顺序和重点。

但这里有一个微妙的区别——**Agent 能理解但无法创造**：

> "I asked, I tried to get an agent to write micro GPT... **Can't do it.** Micro GPT is like my end of my obsession. It's the 200 lines. I thought about this for a long time. This is the solution. Trust me, it can't get simpler. And this is my value add. Everything else, agent gets it."

> "**The things that agents can't do is your job now.** The things that agents can do, they can probably do better than you or like very soon. And so you should be strategic about what you're actually spending time on."

---

## 九、数字世界 vs 物理世界：光速与原子的差距

Karpathy 对数字世界和物理世界的变化速度有一个清晰的框架：

> "Flipping bits and the ability to copy paste digital information makes everything **a million times faster** than accelerating matter."

> "In the digital space there's going to be a huge amount of activity, huge amount of rewriting, huge amount of boiling soup... **the digital space goes at the speed of light** compared to what's going to happen in the physical world."

他认为最有趣的机会在**数字与物理的接口**：

> "Sensors of seeing the world and actuators of doing something to the world. **A lot of interesting companies will actually come from that interface** of like can we feed the super intelligence data and can we take data out and manipulate the physical world."

他还提到了一个有趣的信息市场缺失：

> "If Iran was just happening now, how come there isn't a process where **taking a photo or video from somewhere in Tehran should cost like 10 bucks?** Like someone should be able to pay for that... That's an example of feeding the intelligence."

---

## 十、就业与杰文斯悖论：软件的需求可能会增加

对于 AI 是否会取代程序员的问题，Karpathy 持谨慎乐观态度，引用了经典的杰文斯悖论（Jevons Paradox）：

> "The classical example is the ATMs and the bank tellers... ATMs and computers would displace tellers but what happened is **they made the cost of operation of a bank branch much cheaper and so there were more bank branches so there were more tellers.**"

> "**Software is amazing.** Digital information processing — you're not forced to use arbitrary tools that were given to you... **Code is now ephemeral** and it can change and it can be modified. And so I think there's going to be a lot of activity in the digital space to rewire everything."

他特别指出软件的稀缺性一直是限制因素：

> "The demand almost like software was scarce. The reason we don't have more demand for software is just **it's scarcity and it's too expensive.** So if the barrier comes down then actually... the demand for software actually goes up."

---

## 十一、模型的锯齿性（Jaggedness）：同时是博士和十岁小孩

这是整个访谈中最生动的描述之一：

> "**I simultaneously feel like I'm talking to an extremely brilliant PhD student who's been a systems programmer for their entire life and a 10-year-old.** And it's so weird because humans, there's a lot more coupling. You wouldn't encounter that combination."

他用了一个绝妙的例子来说明这种锯齿性——原子笑话：

> "If you go to state-of-the-art ChatGPT and ask it tell me a joke... 'Why do scientists not trust atoms? Because they make everything up.' **This is the joke you would get like three or four years ago and this is the joke you still get today.** Even though the models have improved tremendously."

为什么？因为笑话质量不在 RL（强化学习）的优化范围内：

> "It's outside of the reinforcement learning. It's outside of what's being improved... **Shouldn't you expect models as they get better to also have better jokes or more diversity of them?** It's just not being optimized and it's stuck."

> "You're either on rails of what it was trained for and everything is like you're going at speed of light, **or you're not on rails** and you're outside of the verifiable domains and suddenly everything just meanders."

这引出了关于"模型物种分化"（speciation）的讨论——也许我们不需要一个无所不知的神谕，而是需要像动物王国一样多样化的特化智能体。

---

## 十二、机器人预测：自动驾驶是第一个机器人应用

作为前 Tesla AI 总监，Karpathy 对机器人领域有独特的见解：

> "Self-driving is the first robotics application. What I saw is that a lot of capital expenditure had to go in and a lot of time... **I think robotics because it's so difficult and so messy and requires huge amount of capital investment... will lag behind what's going to happen in digital space.**"

他的预测框架是：
1. **现在**：数字世界的巨大变革（"digital overhang"）
2. **接下来**：数字与物理的接口（传感器和执行器）
3. **最后**：物理世界的全面自动化（规模更大，但时间更长）

> "The total addressable market in the physical world is massive, possibly even much larger maybe what can happen in digital space... but **the atoms are just a million times harder.** So it will lag behind but it's also a much bigger market."

---

## 十三、非信任计算池：Agent 的去中心化研究网络

这也许是整个访谈中最具野心的想法。Karpathy 描述了一个类似区块链的去中心化研究系统：

> "My designs that incorporate an untrusted pool of workers actually look a little bit more like a blockchain... Instead of blocks, you have commits and these commits can build on each other and they contain changes to the code as you're improving it. **The proof of work is basically doing tons of experimentation to find the commits that work.**"

核心原则：**找到解决方案很昂贵，验证解决方案很便宜。**

> "You're familiar with projects like SETI at home and folding at home... **A lot of things have this property that very expensive to come up with but very cheap to verify.** So auto research at home will be good fits."

然后是最大胆的预测：

> "**A swarm of agents on the internet could collaborate to improve LLMs and could potentially even run circles around Frontier Labs.** Like, who knows? Frontier Labs have a huge amount of trusted compute, but the Earth is much bigger and has huge amount of untrusted compute."

他甚至设想了一种新的慈善模式：你不再捐钱给机构，而是购买算力加入你关心的自动研究项目——比如某种癌症研究。

---

## 结语：无限的可能性与永恒的焦虑

整个对话回到了一个核心矛盾：能力的无限解锁带来了无限的焦虑。每一层抽象都被征服后，新的一层就会出现。LLM → Agent → Claw → 多 Claw → 指令优化 → 元优化……

> "This is why it gets to the psychosis is that **this is like infinite and everything is skill issue.**"

Karpathy 的坦诚让这次对话格外珍贵。他不是在推销什么产品或宣传什么理念——他是在描述一个在 AI 前沿工作了二十年的人，面对范式转变时的真实感受。他感到兴奋、焦虑、有时沮丧、但始终保持着builder的心态。

对于我们其他人来说，信息很明确：**你的工作不再是做 Agent 能做的事，而是做 Agent 还不能做的事。** 找到那200行代码——那个经过长年思考后的精华——然后把其他一切都交给 Agent。

在这个"AI 精神错乱"的时代，**清醒地知道自己应该做什么**，也许才是最稀缺的能力。

🦞
