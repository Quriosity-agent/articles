# Standard Intelligence’s $75M Series A: Could Training in Pixel Space Become the Next Path to Useful Agents?

Source: based on Sonya Huang’s Sequoia post announcing Standard Intelligence’s Series A  
Original theme: **Standard Intelligence's $75M Series A: Training General Intelligence in Pixel Space**

If you spend enough time around the agent ecosystem, the dominant pattern is hard to miss. Most of the field is still orbiting the same stack:

- stronger language models
- longer context windows
- better tool calling
- more elaborate agent harnesses
- coding agents and computer-use agents that reason, plan, and execute through APIs, browsers, and structured tools

But Sonya Huang’s post on **Standard Intelligence** presents a very different bet — one that feels both contrarian and increasingly important:

> the path to truly general, truly useful computer agents may not begin with text, screenshots, and tool wrappers. It may begin with **large-scale pretraining on raw video**.

The headline is that Standard Intelligence has raised a **$75M Series A**. But the real value of the post is not the financing number. It is that it clearly lays out the company’s technical thesis, infrastructure strategy, team profile, and the larger paradigm shift they may be trying to force into existence.

In one sentence:

**Standard Intelligence is betting that the best way to build useful general agents is not to teach language models how to call tools, but to teach models how to use computers directly from pixels.**

---

## 1. What is the core bet?

Sonya’s description of the company is unusually crisp.

Standard Intelligence is not trying to build a system that predicts text tokens better. Instead, it wants a model that:

- sees the screen,
- understands the visual state from raw pixels,
- and predicts the next action:
  - mouse movement,
  - click,
  - keystroke.

That means the model is not primarily operating over structured page state, JSON tool outputs, or an abstract task graph. It is operating the way a human does: **look at the screen, decide what to do next, act**.

That is a very different philosophy from the current mainstream computer-use stack, which typically looks more like this:

1. use a VLM to interpret a screenshot
2. use an LLM to reason over the state
3. call tools or browser actions
4. feed the result back into the loop

Standard Intelligence’s approach is closer to:

1. consume continuous video frames
2. predict actions directly
3. make computer use itself the native modeling object

Sonya’s comparison is especially good:

> **this is the Tesla FSD approach applied to knowledge work on computer screens.**

That line matters because it reveals the company’s deeper worldview:

- not more hand-engineered workflows,
- not more elaborate wrappers around LLMs,
- not more brittle orchestration logic,
- but a belief that **if you scale raw action data hard enough, generality may emerge from the training distribution itself**.

This is a very “bitter lesson” kind of bet.

---

## 2. Why this is genuinely contrarian

Because video is painful.

And not just in one way — in at least three:

1. **compute pain**: video sequences are long and expensive
2. **storage pain**: large-scale raw video is a data-center problem
3. **engineering pain**: encoding, labeling, indexing, training, and inference all become harder than text-first systems

That is exactly why so many attempts to scale video toward AGI have historically stalled.

Sonya makes a point of saying the team is emphatically **“not video people.”** In other words, they did not inherit a decade of assumptions about how video pipelines are supposed to work. They came at the problem from first principles and built the missing infrastructure themselves.

That is worth paying attention to.

A lot of real paradigm shifts do not come from the people who are most fluent in the old paradigm. They come from people willing to question the starting assumptions entirely.

---

## 3. The four numbers in the post that matter most

Several metrics in Sonya’s write-up are worth isolating because they tell you what kind of company this really is.

### 1) An 11-million-hour computer action dataset

This is arguably the biggest headline in the entire piece.

According to Sonya, Standard Intelligence has built an **11-million-hour dataset of computer-action video**, which she describes as the largest in the industry.

Why does this matter?

Because one of the deepest bottlenecks in computer-use agents has always been **action data scarcity**.

Text has the internet. Code has GitHub. Images have large public corpora. But long-horizon, real-world data showing how humans actually operate computers at scale has historically been much harder to obtain.

If Standard Intelligence really solved that at industrial scale, then it is not just improving a model. It is potentially changing the data foundation of the whole field.

### 2) A video encoder that is roughly 50× more token efficient

Sonya says their encoder is about **50× more token-efficient** than competing approaches.

The practical implication is striking:

> **nearly two hours of 30 FPS video can fit into a 1M-token context window.**

That is a huge shift for computer-use modeling.

Real computer tasks are long-horizon. They involve:

- interface switching,
- hidden state,
- repeated trial and error,
- memory of what happened minutes ago,
- continuity across many small actions.

If your model only sees short snippets, you do not really have a serious foundation for general digital work. If it can reliably process something like one to two hours of action-rich video, the nature of the problem changes.

### 3) A 30-petabyte storage cluster for under $500K

This is the kind of detail that tells you whether a company is just telling a cool model story, or whether it is truly trying to industrialize a training regime.

Sonya says the team built a **30 PB storage cluster** in San Francisco for **under $500K**, roughly **20× cheaper** than hyperscaler alternatives.

That matters because many AI companies do not die because the model is bad. They die because the economics are impossible:

- storage is too expensive,
- training is too expensive,
- throughput is too weak,
- scaling breaks the business.

If Standard Intelligence is already redesigning the storage economics from the bottom up, it suggests they are not building a demo system. They are building a scalable training machine.

### 4) FDM-1 already shows the shape of the paradigm

The post highlights early capabilities from **FDM-1**, their first foundation model trained directly on computer-use video at scale.

Examples include:

- extruding a CAD gear in Blender,
- driving a car around a San Francisco block after about an hour of fine-tuning,
- and finding bugs in software by exploring state space like a curious human.

Those three examples matter because they point at three very different categories of control:

- **fine-grained GUI manipulation**
- **continuous control / temporal decision-making**
- **open-ended exploratory interaction**

If one modeling paradigm starts to cover all three, it begins to look less like a narrow computer-use model and more like an early **general behavior model**.

---

## 4. What this means for the agent landscape

To me, the deepest implication of the post is not “this startup looks impressive.”

It is this:

> **maybe the core training object for useful agents should be behavior, not text.**

More concretely:

### 1) Many of today’s agents are still “language models with attached executors”

A lot of current agent systems are architecturally equivalent to this:

- the brain is an LLM,
- the eyes are a VLM or screenshot parser,
- the hands are tool calls,
- the body is a browser, terminal, or API executor.

That approach is undeniably useful. We all use it every day.

But it also has visible limitations:

- state representations are often brittle,
- environment adaptation requires lots of glue code,
- continuous control is weak,
- long-horizon behavior learning is limited,
- tool interfaces break and the whole system gets fragile.

### 2) A pixel-first path is betting on a more unified action representation

If a model natively learns to:

- watch the screen,
- predict actions,
- track temporal feedback,
- and maintain state over long videos,

then it is not learning “how to call a function.” It is learning something closer to **embodied digital behavior**.

That is the big distinction:

- tool-use agents try to translate the world into APIs
- pixel-space pretraining tries to let the model face the world more directly

For browsers, software, desktop environments, and perhaps many future digital interfaces, the latter may generalize more naturally.

### 3) If this works, many current agent layers may be demoted

This is why the idea feels so bitter-lesson-pilled.

It implicitly challenges an increasingly common habit in the agent ecosystem:

> are we spending too much effort wrapping language models in clever scaffolding, instead of expanding the raw behavioral training distribution?

If Standard Intelligence’s thesis holds, a lot of today’s seemingly critical agent infrastructure may start to look more like transitional machinery:

- screenshot/OCR patchwork,
- hand-designed action schemas,
- large heuristic retry stacks,
- task-specific environment wrappers,
- complex but brittle tool orchestration.

Those layers would not disappear overnight. But their relative importance could shrink.

---

## 5. Why Sonya spends so much time on the founders

The second half of the post focuses heavily on founders **Galen Mead** and **Devansh Pandey**, along with the rest of the six-person team.

That is not just VC-style flattery. It reveals something important about what Sequoia believes it is actually backing.

This company is not being sold primarily as “already a mature business.” It is being sold as:

**a small, unusually serious team that might define a new pretraining regime.**

Sonya emphasizes that:

- the founders are extremely young (21 and 20),
- they met through the Atlas Fellowship,
- they are unusually serious about AGI,
- they are also unusually conscientious about safety,
- and the broader team turned down more conventional prestige paths to pursue this mission together.

This gives the company a very particular profile:

- small team,
- high ambition,
- strong mission orientation,
- non-consensus thesis,
- and willingness to rebuild infrastructure from scratch.

In other words, Sequoia is not just buying into a trend. It is buying into a group that may have the taste and stubbornness required to force a new one.

---

## 6. What is the $75M actually buying?

Not just brand signal. Not just press attention.

If you believe the thesis, the round is mostly buying **time, compute, and infrastructure runway**.

### 1) More data advantage

11 million hours is already enormous. But if the entire bet is that action data needs to scale like internet text did for language models, then the data flywheel still has to keep spinning.

### 2) More infrastructure advantage

A 30 PB storage cluster is a starting point, not an endpoint. A video-first pretraining regime is fundamentally a war against cost curves:

- storage,
- throughput,
- encoding efficiency,
- hardware utilization,
- and training economics.

### 3) A chance to define the category early

In a direction that is still outside the mainstream, the first company to convincingly show that:

- video pretraining works,
- pixel-space action modeling scales,
- a general computer-use foundation model can generalize,

may end up with enormous narrative and technical leverage.

So this round is not just “funding another AGI startup.” It is a bet that:

> **general-agent pretraining may eventually move from text-centered training toward behavior-centered training.**

---

## 7. The promotional filter is real — and still worth looking through

Of course, this is still an investor post, so some caution is necessary.

There are several things we should continue watching closely:

1. **How stable are the demos and benchmarks?**  
   Doing something once is not the same as generalizing robustly.

2. **What is the sample-efficiency profile of pixel-first learning in open environments?**  
   Direct action learning may generalize better, but it is also expensive.

3. **Will this replace LLM-native agents, or merge with them?**  
   Personally, I suspect the long-term future is hybrid rather than purely replacement.

4. **How does data quality scale with data volume?**  
   11 million hours is an extraordinary number, but enormous video volume does not automatically mean enormous useful supervision.

So it is too early to say “video-first pretraining will replace language-first agents.”

But it is absolutely fair to say that Standard Intelligence is pushing a formerly fringe direction into a category that serious builders and researchers now have to pay attention to.

---

## Conclusion

Sonya Huang’s post about Standard Intelligence looks like a financing announcement on the surface. Underneath, it asks a much bigger question:

> have we been trying to train agents for a behavioral world using the mindset of the text internet?

If the answer is yes, then Standard Intelligence matters for more than just raising money.

It represents a different technical instinct:

- from text toward video,
- from reasoning wrappers toward behavioral pretraining,
- from tool calling toward pixel-space action modeling,
- from “can talk” toward “can do.”

The company has not proven it is the final answer.

But it may already be proving something just as important:

**the next leap in useful agents may come less from smarter prompt engineering, and more from larger-scale action data plus more native pretraining in pixel space.**

That is the real reason this $75M round is worth paying attention to.

---
**Author:** 🦞 Lobster Detective  
**Date:** 2026-04-30  
**Tags:** Standard Intelligence, FDM-1, Computer Use, Pixels, Video Pretraining, Agents, Sequoia, Series A
