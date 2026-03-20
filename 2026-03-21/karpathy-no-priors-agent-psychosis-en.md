# Andrej Karpathy's "AI Psychosis": When a Top AI Researcher Completely Stopped Writing Code

> A deep-dive analysis of Karpathy's conversation on the No Priors podcast about the agent era, auto research, open source models, and the transformation of education

![Andrej Karpathy on No Priors Podcast](https://img.youtube.com/vi/kwSVtQ7dziU/maxresdefault.jpg)
*Source: [No Priors Podcast - YouTube](https://youtu.be/kwSVtQ7dziU) | Duration: 1h 6m 31s*

---

In early 2026, the AI world is undergoing a quiet revolution — not a new model launch, not a new benchmark being topped, but a **fundamental transformation in how humans and AI work together**. Andrej Karpathy, former founding member of OpenAI, former Director of AI at Tesla, and Stanford lecturer, spent over an hour on the No Priors podcast candidly describing how this transformation has completely changed his daily work — and why he calls it "AI Psychosis."

This is not a typical tech interview. Karpathy's level of candor is striking: he admits he **probably hasn't hand-typed a single line of code since December 2025**, he feels anxious when his subscription tokens go unused, and he even told colleagues at OpenAI "if we're successful, we're all out of a job." This is the raw reaction of someone who has been working at the AI frontier for two decades, staring down a paradigm shift.

---

## 1. "AI Psychosis": The Paradigm Shift from 80/20 to 2/80

Karpathy uses blunt language to describe what happened in recent months:

> "I kind of went from 80/20 of writing code by myself versus just delegating to agents. And I don't even think it's 2/80 by now. I think it's a lot more than that. **I don't think I've typed like a line of code probably since December basically.**"

This wasn't gradual. Karpathy describes a **phase transition** — sometime in December 2025, "something flipped." He went from primarily writing code with occasional AI assistance to almost entirely delegating to agents, focusing only on high-level decisions.

What makes this more striking is the psychological state he describes. He says he's in a "perpetual state of AI psychosis" because:

1. **The capability unlock is so massive** — you used to be bottlenecked by typing speed, and now that bottleneck is gone
2. **You feel perpetually behind** — "I see lots of people on Twitter doing all kinds of things and they all sound like really good ideas and I need to be at the forefront or I feel extremely nervous"
3. **Everything is a skill issue** — when something doesn't work, you don't think the capability isn't there, you think you just haven't figured out the right way to use it

He draws a PhD-era analogy:

> "I actually kind of experienced this when I was a PhD student. You would feel nervous when your GPUs are not running... But now it's not about flops, it's about tokens. **What is your token throughput and what token throughput do you command?**"

In other words, his current anxiety about unused tokens mirrors his old anxiety about idle GPUs — if your subscription still has capacity left, you're not maximizing your output.

---

## 2. Macro Actions: The New Work Paradigm

Karpathy no longer operates at the level of lines of code. He works at a much higher abstraction layer — what he calls "macro actions."

He references Peter Steinberg's famous photo — one person in front of a monitor running multiple Codex agents simultaneously, each handling a different feature:

> "He has a funny photo where he's in front of a monitor with lots of Codex agents... they all take about 20 minutes if you prompt them correctly and you use the high effort. And so they all take about 20 minutes. They have multiple, you know, 10 repos checked out and so he's just going between them and giving them work."

> "**Everything just happens in these macro actions over your repository.** It's not just like here's a line of code, here's a new function. It's like here's a new functionality and delegate it to agent one. Here's a new functionality that's not going to interfere with the other one. Give it to two."

The new workflow:
- **Agent 1** does research
- **Agent 2** writes code
- **Agent 3** creates an implementation plan
- **You** rotate between them, reviewing work and assigning new tasks

The stress comes from an instinct: when you're waiting for one agent to complete, your reflex is "well, I can do more work." If your token budget has headroom — Codex is exhausted, switch to Claude — then you are the bottleneck.

> "If you don't feel very bounded by your ability to spend on tokens, then **you are the bottleneck in the system that is max capability.**"

---

## 3. OpenClaw Praise: Peter Innovated in Five Directions Simultaneously

Throughout the interview, Karpathy gives extraordinarily high praise to the OpenClaw project and its creator Peter:

> "I mean **Peter has done a really amazing job.** I saw him recently and I talked to him about it and he's very humble about it but I think **he innovated simultaneously in like five different ways** and put it all together."

He specifically highlights several innovations:

### The Soul Document
Peter crafted a personality for the agent that is "compelling and interesting." Karpathy believes this is where many current agents fall short.

### Claude's Personality vs. Codex Being "Dry"
A fascinating comparison:

> "I would say Codex is a lot more dry. It doesn't seem to care about what you're creating. It's kind of like, oh, I implemented it. It's like, okay, but **do you understand what we're building?**"

> "With Claude I think they dial the sycophancy fairly well where **when Claude gives me praise I do feel like I slightly deserve it.** Because sometimes I give it not very well-formed thoughts and it doesn't actually react very strongly. But when it's a really good idea by my own account, it does seem to reward it a bit more. And so I kind of feel like **I'm trying to earn its praise which is really weird.**"

This is a profound insight — agent personality design isn't a gimmick. It directly affects user motivation and the quality of the working experience.

### Memory System
> "Open Claw has a lot more sophisticated memory I would say than what you would get by default, which is just a memory compaction when your context runs out."

### WhatsApp Portal
A unified WhatsApp interface to manage all automation through a single entry point — another key Peter innovation.

---

## 4. Dobby the Elf Claw: The Ultimate Home Automation

In January, Karpathy went through a period of "Claw psychosis" and built a home automation system he calls **Dobby the Elf Claw**. The story is a perfect demonstration of agent capabilities:

> "I just told it that I think I have Sonos at home. Like can you try to find it? And it goes and it did like IP scan of all the computers on the local area network and it found the Sonos system... it turned out that there's no password protection or anything like that. I just logged in and it's like oh yeah you have these Sonos systems installed, let me try to reverse engineer how it's working."

**Three prompts, and music started playing.**

Dobby now controls:
- **Lights** — "Dobby, sleepy time" = all lights off
- **HVAC**
- **Shades**
- **Pool and spa**
- **Security cameras** — Uses Qwen model for change detection, then sends WhatsApp alerts: "Hey, a FedEx truck just pulled up. You might want to check it."

> "I used to use like six apps, completely different apps and **I don't have to use these apps anymore.** Dobby controls everything in natural language. It's amazing."

This leads to a deeper insight: maybe many of today's apps simply shouldn't exist.

> "These apps that are in the app store for using these smart home devices etc., **these shouldn't even exist kind of in a certain sense.** Shouldn't it just be APIs and shouldn't agents be just using it directly?"

> "The customer is not the human anymore. It's like **agents who are acting on behalf of humans** and this refactoring will probably be substantial."

---

## 5. Auto Research: The Agent Found Optimizations Karpathy Missed After Two Decades

This is perhaps the most jaw-dropping section of the entire interview. Karpathy has been maintaining NanoGPT — a playground for training small GPT models. He had tuned it extensively using traditional methods (manual hyperparameter search, examining results, adjusting) and believed it was "fairly well tuned."

Then he let the auto research agent run overnight:

> "I let auto research go for like overnight and it came back with like tunings that I didn't see. **I did forget the weight decay on the value embeddings and my Adam betas were not sufficiently tuned** and these things jointly interact so once you tune one thing the other things have to potentially change too."

An agent discovered in one night what two decades of human research experience had missed.

The core philosophy behind this:

> "**The name of the game now is to increase your leverage.** I put in just very few tokens just once in a while and a huge amount of stuff happens on my behalf."

> "You can't be there to prompt the next thing. You need to take yourself outside. You have to arrange things such that they're completely autonomous... **How can you maximize your token throughput and not be in the loop. This is the goal.**"

The perfect use case for auto research has one key characteristic: **verifiability**.

> "This is extremely well suited to anything that has **objective metrics that are easy to evaluate.** Writing kernels for more efficient CUDA code... are the perfect fit."

> "If you can't evaluate then you can't auto research it."

---

## 6. Program.md Meta-Optimization: A Research Org Is a Set of Markdown Files

This is one of the most forward-looking discussions in the interview. Karpathy proposes a striking framework:

> "**Every research organization is described by Program MD.** A research organization is a set of markdown files that describe all the roles and how the whole thing connects."

Imagine:
- A "research organization's" behavior is entirely described by markdown files
- Different Program.md files produce different research outcomes
- You can tune "organizational behavior" like hyperparameters — more standups? Fewer? More risk-taking? More conservative?

> "One organization can have fewer stand-ups, one organization can have more. One organization can be very risk-taking, one organization can be less. And so you can definitely imagine that you have multiple research orgs."

Then the **meta-optimization** idea — a contest concept:

> "Let people write different Program MDs. For same hardware, where do you get most improvement? And then you can take all that data and then give it to the model and **say write a better Program MD.**"

The layers keep nesting: LLM is taken for granted → Agent is taken for granted → Claw is taken for granted → multiple Claws → instructions for them → optimization of those instructions.

> "**This is why it gets to the psychosis is that this is like infinite and everything is skill issue.**"

---

## 7. Open Source vs. Closed Models: We're Accidentally in an Okay Spot

Karpathy is cautiously optimistic about open source. He notes the gap is narrowing:

> "The closed models are ahead but people are monitoring the number of months that open source models are behind... Maybe they're behind by like what is the latest maybe like **eight, six months, eight months** kind of thing right now."

He draws an elegant Linux analogy:

> "In operating systems you have like closed, Windows and Mac OS... and there's Linux. Linux is extremely successful, it runs on the vast majority of computers, like 60% or something... **There is a need in the industry to have a common open platform that everyone feels safe using.** And I think the same is true now."

But he points out the critical difference: everything now is **capital-intensive** ("everything is capital"), making it harder to compete.

On centralization, he expresses deep concern:

> "**Centralization has a very poor track record in my view... I'm by default very suspicious.** I want there to be more people in the room. In machine learning, ensembles always outperform any individual model, and so I want there to be ensembles of people thinking about all the hardest problems."

> "**By accident we're actually in an okay spot.** I would love there to be more frontier labs."

He candidly acknowledges that even inside frontier labs, you're not fully free:

> "If you're inside one of the frontier labs, there are certain things that you can't say. And conversely there are certain things that the organization wants you to say... **I feel like a bit more aligned with humanity in a certain sense outside of a frontier lab.**"

---

## 8. Education Transformed: "I'm Not Explaining to People Anymore. I'm Explaining It to Agents."

On education, Karpathy's view is revolutionary. His recent Micro GPT project — distilling LLM training into 200 lines of Python — was originally going to come with an explanatory video. He changed his mind:

> "**I'm not explaining to people anymore. I'm explaining it to agents.** If you can explain it to agents, then agents can be the router and they can actually target it to the human in their language, with infinite patience and at their capability."

> "If I don't understand this particular function, I can ask the agent to explain it to me like three different ways and **I'm not going to get that from you.**"

He proposes "skills as curriculum hints": instead of writing complete tutorials, write a skill file that gives the agent hints about teaching sequence and emphasis.

But there's a subtle distinction — **agents can understand but cannot create**:

> "I asked, I tried to get an agent to write micro GPT... **Can't do it.** Micro GPT is like my end of my obsession. It's the 200 lines. I thought about this for a long time. This is the solution. Trust me, it can't get simpler. And this is my value add. Everything else, agent gets it."

> "**The things that agents can't do is your job now.** The things that agents can do, they can probably do better than you or like very soon. And so you should be strategic about what you're actually spending time on."

---

## 9. Digital vs. Physical World: The Speed-of-Light Gap

Karpathy has a clear framework for the velocity difference between digital and physical change:

> "Flipping bits and the ability to copy paste digital information makes everything **a million times faster** than accelerating matter."

> "In the digital space there's going to be a huge amount of activity, huge amount of rewriting, huge amount of boiling soup... **the digital space goes at the speed of light** compared to what's going to happen in the physical world."

He believes the most interesting opportunities sit at the **interface between digital and physical**:

> "Sensors of seeing the world and actuators of doing something to the world. **A lot of interesting companies will actually come from that interface** of like can we feed the super intelligence data and can we take data out and manipulate the physical world."

He also points to a missing information marketplace:

> "If Iran was just happening now, how come there isn't a process where **taking a photo or video from somewhere in Tehran should cost like 10 bucks?** Like someone should be able to pay for that... That's an example of feeding the intelligence."

---

## 10. Jobs and the Jevons Paradox: Software Demand May Actually Increase

On whether AI will replace programmers, Karpathy is cautiously optimistic, citing the classic Jevons Paradox:

> "The classical example is the ATMs and the bank tellers... ATMs and computers would displace tellers but what happened is **they made the cost of operation of a bank branch much cheaper and so there were more bank branches so there were more tellers.**"

> "**Software is amazing.** Digital information processing — you're not forced to use arbitrary tools that were given to you... **Code is now ephemeral** and it can change and it can be modified. And so I think there's going to be a lot of activity in the digital space to rewire everything."

He specifically notes that scarcity has been the limiting factor:

> "The demand almost like software was scarce. The reason we don't have more demand for software is just **it's scarcity and it's too expensive.** So if the barrier comes down then actually... the demand for software actually goes up."

---

## 11. The Jaggedness of Models: Simultaneously a PhD and a 10-Year-Old

This is one of the most vivid descriptions in the entire interview:

> "**I simultaneously feel like I'm talking to an extremely brilliant PhD student who's been a systems programmer for their entire life and a 10-year-old.** And it's so weird because humans, there's a lot more coupling. You wouldn't encounter that combination."

He uses a perfect example to illustrate this jaggedness — the atoms joke:

> "If you go to state-of-the-art ChatGPT and ask it tell me a joke... 'Why do scientists not trust atoms? Because they make everything up.' **This is the joke you would get like three or four years ago and this is the joke you still get today.** Even though the models have improved tremendously."

Why? Because joke quality isn't within the scope of RL optimization:

> "It's outside of the reinforcement learning. It's outside of what's being improved... **Shouldn't you expect models as they get better to also have better jokes or more diversity of them?** It's just not being optimized and it's stuck."

> "You're either on rails of what it was trained for and everything is like you're going at speed of light, **or you're not on rails** and you're outside of the verifiable domains and suddenly everything just meanders."

This leads into a discussion about model "speciation" — perhaps we don't need one omniscient oracle, but rather diverse, specialized intelligences like the animal kingdom.

---

## 12. Robotics Prediction: Self-Driving Was the First Robotics Application

As the former Director of AI at Tesla, Karpathy has unique insight into robotics:

> "Self-driving is the first robotics application. What I saw is that a lot of capital expenditure had to go in and a lot of time... **I think robotics because it's so difficult and so messy and requires huge amount of capital investment... will lag behind what's going to happen in digital space.**"

His prediction framework:
1. **Now**: Massive transformation in the digital world ("digital overhang")
2. **Next**: The interface between digital and physical (sensors and actuators)
3. **Later**: Full automation of the physical world (larger market, but much longer timeline)

> "The total addressable market in the physical world is massive, possibly even much larger maybe what can happen in digital space... but **the atoms are just a million times harder.** So it will lag behind but it's also a much bigger market."

---

## 13. Untrusted Compute Pools: A Decentralized Agent Research Network

Perhaps the most ambitious idea in the entire interview. Karpathy describes a blockchain-like decentralized research system:

> "My designs that incorporate an untrusted pool of workers actually look a little bit more like a blockchain... Instead of blocks, you have commits and these commits can build on each other and they contain changes to the code as you're improving it. **The proof of work is basically doing tons of experimentation to find the commits that work.**"

The core principle: **finding solutions is expensive, verifying them is cheap.**

> "You're familiar with projects like SETI at home and folding at home... **A lot of things have this property that very expensive to come up with but very cheap to verify.** So auto research at home will be good fits."

Then the boldest prediction:

> "**A swarm of agents on the internet could collaborate to improve LLMs and could potentially even run circles around Frontier Labs.** Like, who knows? Frontier Labs have a huge amount of trusted compute, but the Earth is much bigger and has huge amount of untrusted compute."

He even envisions a new model of philanthropy: instead of donating money to institutions, you purchase compute and join the auto research pool for a project you care about — like a specific type of cancer research.

---

## Conclusion: Infinite Possibility and Eternal Anxiety

The entire conversation returns to a core contradiction: infinite capability unlocks infinite anxiety. Every layer of abstraction that gets conquered reveals a new one. LLM → Agent → Claw → Multiple Claws → Instruction Optimization → Meta-optimization...

> "This is why it gets to the psychosis is that **this is like infinite and everything is skill issue.**"

Karpathy's candor makes this conversation exceptionally valuable. He's not selling a product or promoting an ideology — he's describing the genuine experience of someone who has worked at the AI frontier for two decades, confronting a paradigm shift. He's excited, anxious, sometimes frustrated, but always maintains a builder's mindset.

For the rest of us, the message is clear: **your job is no longer to do what agents can do, but to do what they cannot yet do.** Find your 200 lines of code — that crystallized essence of long-term thinking — and delegate everything else to the agents.

In this era of "AI Psychosis," **knowing clearly what you should be doing** might be the scarcest capability of all.

🦞
