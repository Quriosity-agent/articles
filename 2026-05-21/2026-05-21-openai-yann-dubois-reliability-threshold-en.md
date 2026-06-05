# Yann Dubois Interview Deep Dive: AI Suddenly Feels Real Not Because Intelligence Jumped, but Because Reliability Crossed a Threshold

> Source: [The MAD Podcast with Matt Turck — OpenAI’s Yann Dubois on Why AI Progress Suddenly Feels Real](https://www.youtube.com/watch?v=DhD1zZ8w8Mw&t=2s)  
> Published: 2026-05-21  
> Tags: OpenAI / Yann Dubois / GPT-5.5 / Post-training / RL / Evals / Agent Harness / Continual Learning

Why has AI suddenly started to feel real over the past few months?

In Yann Dubois’s interview with Matt Turck, the answer is not that models magically woke up one day. It is a more operational explanation: **capability may improve continuously, but once reliability crosses a threshold, user behavior changes discontinuously.**

A model improving from 70 to 80 may make demos more impressive. A model improving from 90 to 95 may make users willing to hand over real work. The perceived step change does not necessarily come from a sudden jump in intelligence. It comes from crossing the usability threshold.

That is why this interview is worth unpacking. It reframes today’s AI race around reliability, post-training, reinforcement learning, evaluation, agent harnesses, enterprise memory, and the last mile for startups.

## 1. The Real Threshold Is Not Capability Demonstration, but Reliability

Yann’s explanation of reliability maps directly onto agent engineering: if an agent has some probability of making a mistake every few minutes, the longer the task runs, the more likely the final outcome is to fail.

Short demos can survive on luck. Long-horizon work cannot.

Agent usefulness is not a linear function of single-step accuracy. It is closer to a multiplicative process:

- if each step is 95% reliable, the success rate falls quickly over twenty steps;
- if each step is 99% reliable, long tasks start to become commercially meaningful;
- if the workflow also includes tools, file edits, permissions, APIs, and ambiguous user intent, errors compound further.

So the important change is not that models can finally code, browse, summarize, or use tools. Those capabilities have existed for a while. The important change is that models are starting to make few enough basic mistakes that users are willing to trust them with real workflows.

This also explains why coding felt the shift first. Coding has built-in feedback loops: tests run, types check, diffs can be reviewed, and CI catches some errors. Compared with law, finance, consulting, or strategy work, coding has a clearer path to pushing reliability over the usability threshold.

## 2. GPT-5.5 Is About Horizontal Integration, Not One Isolated Skill

Yann mentions that GPT-5.5 had the internal codename Spud, and that OpenAI was highly aligned and excited around the release. From the outside, users may see “a stronger model.” From his description, the more important story is multi-dimensional integration.

GPT-5.5 is especially strong across several areas:

1. **agentic coding** — not just completing snippets, but editing, debugging, checking, and pushing work forward;
2. **computer use** — operating tools and interfaces rather than staying inside a chat box;
3. **knowledge work** — handling open-ended research, synthesis, and production;
4. **early scientific research** — participating in longer, uncertain research loops.

Yann’s Post-Training Frontiers team does not optimize only one vertical. It integrates improvements from vertical teams and smooths the model’s behavior across horizontal capabilities: instruction following, function calling, memory, and thinking-time allocation.

That matters because real-world tasks usually fail not because the model lacks some domain fact, but because horizontal behavior breaks:

- it misunderstands the instruction;
- it calls a tool with the wrong parameters;
- it fails to look something up;
- it guesses when it should ask for clarification;
- it rushes when it should think;
- it overthinks when it should execute.

A model becomes useful in workflows not through a peak benchmark score, but through stable horizontal behavior.

## 3. The Next Stage of Reasoning Moves from Clean Problems to Messy Work

The O1/O1 Preview breakthrough was test-time compute: models could think longer, and longer thinking increased the probability of correctness.

But the easiest early domains were math and competitive programming. The reason is simple: the answers are verifiable. Math problems have ground truth, and code problems can run tests. Reinforcement learning has a clean reward signal.

Yann’s point is that similar RL methods are now moving toward messier real-world tasks: real programming, knowledge work, computer use, and agent workflows.

That is much harder because real work often has these properties:

- the goal is underspecified;
- the information is not all in the prompt;
- the model must gather evidence;
- it must identify missing context;
- there may be many acceptable solutions;
- failures may only become visible at the end.

The challenge is not merely making the model think longer. It is making the model know when to think, what to think about, when to act, when to backtrack, and when to question the task definition.

## 4. Efficiency Is a Core Product Dimension

One underrated theme in the interview is GPT-5.5’s efficiency.

Yann says many tasks became roughly 2x faster. That speedup is not only inference engineering. It also comes from models learning to allocate thinking time better.

A reasoning model can be imagined as a curve:

- the x-axis is latency or thinking tokens;
- the y-axis is performance;
- normal mode aims for a good answer within reasonable latency;
- Pro mode moves further along the curve, spending more compute for higher correctness;
- research and engineering try to shift the whole curve left.

This explains the difference between GPT-5.5 Thinking and GPT-5.5 Pro. Pro is not a different kind of intelligence. It is more test-time compute. But gains are not linear; the curve eventually plateaus.

A more efficient model behaves like an expert. It does not explore every path equally. It learns which paths are promising, which ones should be abandoned, and when to backtrack early.

For products, this is crucial. Users do not care how many tricks the model uses internally. They care how long it takes, how much it costs, and whether the result is reliable.

## 5. Pretraining Has Not Hit a Wall, but It Is Not the Whole Story

Yann cannot discuss OpenAI’s internal pretraining details, but he is clear that pretraining is still producing gains.

This differs from a common intuition over the past two years: that internet text is nearly exhausted and pretraining is close to a wall. In Yann’s framing, larger models can still improve two things:

1. **capability** — knowing more and forming stronger abstractions;
2. **efficiency** — doing more implicit reasoning in the weights and requiring fewer explicit reasoning tokens.

The second point is especially interesting. A larger model does not always mean worse end-to-end latency. A stronger set of weights may reduce the number of visible reasoning steps, and inference engineering may parallelize GPU work more effectively.

So “bigger means slower” is not a universal rule. The full system matters: model size, token count, inference architecture, parallel efficiency, and task difficulty.

But pretraining only gives the model a giant library. It does not make it a useful colleague.

## 6. Mid-Training Is the Underrated Quality-Weighting Stage

Yann defines mid-training as the stage between pretraining and post-training, where the model continues training on higher-quality data closer to the desired final capabilities.

Pretraining learns from the broad internet, which includes Wikipedia, GitHub, papers, ads, random forums, duplicate content, and noisy text. Mid-training pulls the model toward higher-signal data.

This stage receives less public attention than post-training and RL, but it may be central to the model’s “feel.”

Many capabilities cannot be repaired only at the end. Post-training can teach the model how to respond, follow instructions, and call tools. But if the model has not absorbed enough high-quality code, knowledge structures, reasoning patterns, and professional text earlier, the final stages have to work much harder.

Mid-training moves the model from “internet average” toward “high-quality work corpus.”

## 7. Post-Training Turns Knowledge into Usefulness

Yann’s metaphor is useful: pretraining gives the model a huge library; post-training turns that library into a conversational expert.

Post-training usually includes several methods:

- **SFT** — humans provide ideal responses and the model imitates them;
- **RL with verifiable rewards** — math and code tasks where correctness can be checked;
- **RL with preferences or partial verification** — pairwise comparisons, model-as-judge, and user-utility signals.

SFT is useful but limited. It is behavior cloning. The model learns what a human demonstration looks like. If the demonstration is not excellent, the model struggles to surpass it.

RL is valuable because it optimizes a reward signal rather than simply imitating a gold answer. If the reward pipeline is good, the model can sample, compare, and reinforce strategies that outperform demonstrations.

But RL should not start too early. If the base model is weak, it must accidentally sample a good answer before it can receive useful reward. A better pattern is to use pretraining, mid-training, and SFT to bring the model to a strong starting point, then use RL to push the boundary.

## 8. Why RL Is Starting to Work Now

Many researchers used to see RL as fragile. Yann says that when he first saw ChatGPT’s RL story, his instinct was that SFT might reproduce much of the behavior. Stanford Alpaca partly came from that intuition.

His view has changed. Once the base model is strong enough and has good world priors, RL becomes much more effective.

That has implications for robotics and embodied AI. Robot RL has historically been difficult because world understanding was weak, exploration was expensive, and environments were complex. If the underlying model already has strong common sense and world priors, RL may become more stable.

Still, RL has two hard problems:

1. **sampling cost** — many candidate answers or rollouts are needed;
2. **sparse attribution** — long agent tasks often reveal success or failure only at the end, making it hard to know which step caused the outcome.

Open-source interest in GRPO makes sense in this light. It is simple and scalable: sample multiple answers and reinforce the better ones. In machine learning, simple methods that scale often win.

## 9. Jaggedness: The Unit Is Skill Class, Not Domain

Why do models look like experts in some areas and beginners in others? Yann suggests that the unit of capability may not be domain, but skill class.

Math contests and programming contests look like different domains, but they share underlying skills: symbolic reasoning, step-by-step verification, search, constraint satisfaction, and error checking. Improvements in one skill class may transfer to nearby tasks.

Conversely, two tasks that both look like “knowledge work” may transfer poorly if their underlying skill structures differ. Consulting, finance, law, and medicine all require expertise, but their real difficulties include permissions, fact-checking, ambiguous goals, professional judgment, liability, and compliance.

Benchmark intelligence does not automatically become productivity in every industry.

A vertical tends to improve quickly when three conditions exist:

- high-quality data is available;
- reward or evaluation can be constructed;
- people who deeply understand the vertical are continuously watching model behavior.

Coding improved quickly not only because code is abundant online, but because model developers use it every day, feedback loops are dense, and correctness is easier to check.

## 10. Hallucination: SFT Can Teach Models to Pretend They Know

Yann cites John Schulman’s view that SFT may encourage hallucination.

The reason is that behavior cloning imitates answer form. If a human gold answer cites a paper the model does not actually know, SFT may teach the model to produce similar-looking citations in similar contexts.

RL has a better chance of reducing this if the reward pipeline penalizes unsupported claims. Fake citations, false facts, and ungrounded inferences should not be reinforced.

Hallucination is therefore not only a problem of missing knowledge. It is also a problem of training objectives.

If the objective rewards “sounding like an expert,” the model learns expert style. If the objective rewards support, verification, and calibrated uncertainty, the model learns to say when it does not know, to check sources, and to cite evidence.

For products, the lesson is direct: enterprise AI systems should not optimize only fluency. They should evaluate evidence, citations, tool traces, permission boundaries, and refusal behavior.

## 11. Evals Are Becoming the Hardest Part

Yann argues that evaluation is getting harder for two reasons.

First, tasks are becoming more open-ended.

It is easier to evaluate “find this bug” when the bug is pre-labeled. It is much harder to evaluate “build a website that implements X.” Many answers may be acceptable, and quality depends on design, architecture, interaction, performance, and maintainability.

Second, models already exceed most human reviewers on some axes.

If a model writes code, proofs, designs, or research plans beyond the level of ordinary reviewers, who is qualified to judge it? This pushes evaluation toward more specialized, expensive, and dynamic processes.

That is why model-as-judge is becoming central. Stronger models can become better teachers and evaluators, creating a capability flywheel: models help generate training data, evaluate outputs, find errors, and improve future models.

But there is a paradox. Once you can construct a strong eval, you can often use similar methods to construct training data. The eval becomes stale quickly. The real challenge is continuously building evaluations that remain outside the training distribution while still representing real user utility.

## 12. Continual Learning May Be the Most Surprising Unsolved Problem

Late in the interview, Yann highlights continual learning. His mental chart is simple:

- the x-axis is time;
- the y-axis is user utility;
- a new model on day zero may already be more useful than many new employees;
- but human employees rapidly learn company context;
- current models usually do not truly keep learning, so their utility curve is flatter.

This may become one of the central enterprise AI problems.

Today’s memory and personalization are still early. Even single-user memory is not solved well. Enterprise memory is harder: permissions, privacy, team boundaries, knowledge freshness, false memories, auditability, and the right to forget all become system-level issues.

If solved, AI shifts from “a smart contractor” to “a long-term colleague that increasingly understands the company.”

Without continual learning, agents feel like temporary workers. With controlled continual learning, agents can become part of the organization.

## 13. Harnesses Will Not Disappear, but They Must Be Retuned

Matt asks whether the external agent harness will eventually be absorbed into the model itself.

Yann’s answer is balanced: harnesses are extremely valuable today, especially in specific verticals where they can move reliability from 80% to 85% or 90%. But he would not bet on one general harness remaining unchanged for long, because model capabilities change too quickly.

That is an important lesson for startups.

A harness should not be treated as a fixed wrapper. It is a workflow system that must be retuned as models improve. It includes:

- tool selection;
- permission control;
- context injection;
- task decomposition;
- intermediate state tracking;
- rollback and verification;
- human intervention points;
- evaluation and training-data capture.

If models froze today, excellent harnesses alone could unlock a lot of value. Even as models continue to improve, harnesses will not vanish immediately. Their boundary will move: some strategies will be internalized by the model, while the remaining value shifts toward permissions, integration, auditability, and organizational workflow.

## 14. Why Startups Still Have Room

The final signal for founders is clear: applications are still worth building.

The bottleneck is usually not raw intelligence. It is the last mile:

- permissions;
- connectors;
- data access;
- workflow integration;
- domain-specific product design;
- reliability inside a specific vertical;
- the user experience that makes people willing to delegate work.

Model companies like OpenAI will continue pushing horizontal capability. But each industry’s last mile is too specific, messy, and operational to be solved entirely by the general model layer.

That is where startups can win: not by building another chat box, but by choosing a concrete workflow and closing the loop across model, data, permissions, tools, evaluation, and human collaboration.

## Conclusion: The Next Stage Is Turning Intelligence into Trust

The central lesson of the interview is that AI progress is moving from “can it do the task?” to “can it be trusted with the task?”

Over the past few years, models have shown that they can code, solve problems, chat, summarize, draw, and use tools. The next race is about whether they can:

- stay on track for long periods;
- know when they are uncertain;
- spend thinking time where it matters;
- keep learning inside real organizations;
- be evaluated, audited, rolled back, and improved;
- enter concrete workflows through harnesses and product design.

AI suddenly feels real not because of a mysterious jump. It feels real because many continuous improvements accumulated until they crossed the reliability threshold inside users’ minds and business processes.

For model companies, the next step is stronger, steadier models that learn over time. For startups, the opportunity is the last mile: put these models into real work and polish 90% reliability into the 99% that users can actually trust.
