# AutoGo Deep Dive: Rebuilding AlphaGo Is Not Nostalgia, but Training an Automated AI Researcher

> Source: [Eric Jang on X](https://x.com/ericjang11/status/2055359839371772356), [AutoGo Tutorial](https://evjang.com/2026/04/28/autogo.html), [ericjang/autogo](https://github.com/ericjang/autogo), [Playable AutoGo](https://autogo.evjang.com)  
> Date: 2026-05-16  
> Author: Peter / Hermes  
> Tags: AutoGo, AlphaGo, AI Research Automation, Go, MCTS, Self-Play, Claude Code, Agent Harness

![AutoGo tutorial cover](./imgs/autogo-alpha-research-automation/tutorial-cover.png)

Eric Jang’s X post looks, at first glance, like a nostalgic project: he spent the last few months building a from-scratch implementation of AlphaGo, the 2016 AI breakthrough that helped inspire a generation of deep-learning researchers.

But the interesting part of AutoGo is not “someone rebuilt a Go engine.” The interesting part is that AlphaGo becomes a **cheap, controllable, fast-feedback research sandbox** for studying how an AI agent can drive the research process itself.

In the post, Eric writes that his casual understanding of AlphaGo was “search-augmented deep neural networks trained with self-play,” but that he wanted to understand it more deeply by creating it. He also makes the broader point: frontier deep-learning research is expensive, but any given capability gets cheaper quickly. In 2026, you do not need DeepMind-scale resources to train a reasonably strong Go AI; you can rent a few thousand dollars of compute and build a serious version yourself.

The point is not that Go is back. The point is that **AI research is becoming an operational workflow that can be packaged for agents**.

## This is not really a Go project. It is an automated-researcher project.

The AutoGo README is explicit: this is a minimal codebase for building a strong Go-playing AI from scratch — and, more importantly, for studying how to automate the AI researcher driving the project. The repository description is even shorter: `Autoresearch for Go`.

That reframes the project. The question is not merely “can the bot play Go?” The question is: can an AI agent run experiments, interpret results, change hyperparameters, fix systems issues, and continue iterating like a junior researcher?

Go is a good environment for that because it has a rare combination of properties:

- data is cheap because self-play can generate it;
- evaluation is relatively clean: win rate, value estimates, policy accuracy, and MCTS search behavior are all measurable;
- the system is complex enough to include model training, search, distributed sampling, replay data, checkpoints, evaluation, and visualization;
- the feedback loop is much faster than robotics, biology, or real-user product experiments;
- the failure modes are real: life/death errors, scoring rules, training instability, async data pollution, and infra failures all show up.

This is why the README references Dario Amodei’s “virtual biologist” framing. The valuable thing is not using AI merely as a data-analysis tool; it is using AI to execute, direct, and improve the research workflow. AutoGo is a compact version of that idea: not a virtual biologist, but a virtual Go researcher.

## Why AlphaGo instead of a modern LLM, VLM, or robotics benchmark?

![AutoGo playable web app](./imgs/autogo-alpha-research-automation/playable-app.png)

AutoGo is a smart choice precisely because AlphaGo is no longer mysterious, yet it still contains many of the primitives behind modern AI research.

First, **policy and value-network training resembles language-model training**. You are still predicting targets, minimizing losses, comparing train and validation curves, and watching distribution shift — the tokens are just board states and moves rather than words. The README explicitly compares Go policy/value learning to minimizing perplexity.

Second, **MCTS makes test-time compute visible**. Today, inference-time scaling, reasoning traces, and search over actions are central themes in LLMs. AlphaGo already offered a clean template: train a function approximator, then spend compute at inference time searching through candidate futures.

Third, **self-play is a natural environment for scaling laws and recursive improvement**. Go data can be generated indefinitely. Models can be evaluated against older versions, random policies, and MCTS variants. Compared with open-ended environments, the reward signal is cleaner and failures are easier to attribute.

Fourth, **it resembles a robotics stack while being much cheaper**. AutoGo needs logging, data collection, replay buffers, distributed RL, simulated evaluation, and infrastructure. Those are also robotics problems. But Go removes real hardware, sensors, dataset maintenance, safety risks, and slow physical-world iteration.

So AutoGo is not just a 2016 system rebuilt in 2026. It is a training ground for an agent-native AI research workflow.

## The repository: small, but complete enough to matter

I inspected `ericjang/autogo` on the `main` branch at commit `54ac8d4` (`bugfixes`). The GitHub API shows that the repository was created on 2026-04-27, uses the MIT license, and is primarily Python. At the time of inspection it had roughly **121 stars and 11 forks**. A shallow clone contained about **107 files**, including roughly **16.6k lines of Python**, **1.8k lines of C++**, plus shell scripts, Docker files, experiment figures, and Markdown documentation.

It is not a huge product repository, but it has the shape of a complete research system:

| Layer | Main components | Role |
|---|---|---|
| Go environment | `src/alpha_go/go.py`, C++ board/MCTS | Rules, moves, search, performance-critical logic |
| Model | `src/alpha_go/model.py` and related modules | Policy/value networks and PyTorch training |
| Agents | `src/alpha_go/agents/` | Random, MCTS, and model-backed agents |
| Experiments | `experiments/<datetime>-<slug>/` | Self-contained scripts, data, figures, reports |
| Infrastructure | `infra/cluster.py`, `remote_exec.py`, `gpu_lease.py` | Multi-GPU workers, SSH dispatch, Docker, leases |
| Web/demo | `autogo.evjang.com` | Playable 9×9/19×19 Go bot and teacher modes |
| Agent guidance | `CLAUDE.md`, `.claude` | Operating protocol for Claude/coding agents |

The `CLAUDE.md` file is especially revealing. It asks for self-contained, reproducible experiments that are easy for Claude to interpret; it standardizes test, typecheck, and self-play commands; it emphasizes simple code, fewer branches, single-GPU design, and tensor shape suffixes. It also lists canonical commands such as `uv run -m pytest tests/`, `uv run -m mypy src/`, and the self-play training loop.

This is not just a codebase where a human occasionally uses AI autocomplete. It is a codebase designed with AI coding agents as first-class operators.

## Infrastructure lesson: do not overfit to heavy orchestration

AutoGo’s infrastructure design is refreshingly practical. A dev container acts as the controller. GPU workers receive jobs over SSH. Each job is a one-shot `docker run --rm`. Worker nodes live in `cluster.toml`. `infra/cluster.py` provides commands such as `add`, `ping`, `build`, `pull`, and `status`; `infra/remote_exec.py` pushes files, runs the container, and pulls back outputs.

The README contains a lesson that many AI infra teams should take seriously: Eric spent a lot of time wrestling with distributed job-orchestration frameworks, and ultimately found that falling back to SSH plus Docker calls worked best and was more agent-friendly.

That matters because AI research automation does not always need the most enterprise-grade scheduler. An agent needs a system it can understand and repair:

1. What workers exist?
2. How do I package one experiment as a job?
3. Where are stdout, artifacts, figures, data, and checkpoints?
4. Did this fail because of code, data, environment, GPU leasing, or orchestration?
5. Can I rerun the same thing with a small command change?

Heavy orchestration can be powerful for platform teams, but opaque for agents. AutoGo optimizes for systems that are scriptable, debuggable, and recoverable.

## Experiments as a readable feedback loop

![Phase A progress from AutoGo experiments](./imgs/autogo-alpha-research-automation/phaseA-progress.png)

The README mentions two experiment-oriented skills: `autoresearch` and `experiment`. The former is for autonomously optimizing a metric, such as minimizing validation loss or maximizing moves/sec; the latter is for one-off analysis experiments. More importantly, experiment outputs are preserved under directories like `experiments/2026-04-28_00-38-fastlearn/figures/`, with plots for learning progress, KL divergence, train accuracy, holdout evaluation, iteration timing, league performance, and phase progress.

This structure lets an agent do more than “run training.” It can reason about the result:

- Did loss decrease without real playing strength improving?
- Did policy accuracy improve because of better learning or a narrower data distribution?
- Did better MCTS throughput translate into stronger play?
- Did a bad iteration come from the model, the data, the scoring rule, or async sampling?
- Should the system stay synchronous before attempting async RL?

Eric also notes that having Claude “run the training loop by hand” and stop when an iteration became unstable was useful. That detail is important. The target is not fully autonomous magic; it is an interactive research loop where the agent watches experiments, explains anomalies, and proposes the next move.

![Phase B progress from AutoGo experiments](./imgs/autogo-alpha-research-automation/phaseB-progress.png)

## The imperfections are part of the point

The AutoGo README does not pretend the project has solved Go. It says the best model “plays OK,” but still has bugs around life/death because it was trained with Tromp-Taylor scoring rules, and that this is being fixed.

That imperfection is valuable. Many AI-agent demos only show the happy path: the model calls a tool, generates a file, and appears successful. Real research automation lives in the long tail:

- the training objective differs subtly from the real goal;
- metrics improve while the actual evaluation gets worse;
- async data collection corrupts the distribution;
- value-network errors get amplified by search;
- the agent over-interprets a pretty chart;
- infrastructure failures masquerade as algorithmic failures.

AutoGo exposes those edges instead of hiding them. That makes it more useful than a polished but irreproducible demo.

## What builders should borrow

AutoGo offers four practical lessons for people building agents or AI infrastructure today.

First, **choose a fast-feedback domain that still has real system complexity**. Starting with real-world robotics or live product-growth experiments creates too many confounders. Go is simple enough to iterate quickly, but deep enough to exercise research skills.

Second, **turn the benchmark into a workflow, not just a score**. Many benchmarks only tell you how well a model performed. AutoGo is closer to a runnable research workbench: generate data, train, evaluate, plot, report, modify infra, and repeat.

Third, **write codebases for agents to read and operate**. `CLAUDE.md`, self-contained experiment folders, canonical commands, simple infrastructure, and clear tensor naming are all agent affordances. Future high-performing teams may design repositories not just for human maintainers, but for long-running AI collaborators.

Fourth, **do not underestimate old breakthroughs as teaching systems**. AlphaGo is ten years old, but it organizes search, learning, self-play, test-time compute, and distributed data collection in a remarkably clean way. Revisiting it can clarify what modern LLM agents and automated research systems are really doing underneath.

## Conclusion: from rebuilding AlphaGo to rebuilding the research loop

![X video thumbnail for the AutoGo / Dwarkesh lecture](./imgs/autogo-alpha-research-automation/x-video-thumbnail.jpg)

AutoGo is worth watching not because it will defeat the strongest Go engines, but because it asks a more relevant question: what kind of environment does an AI agent need in order to participate in research?

The answer is probably not a bigger chat box. It is an end-to-end research loop: a clear domain, generatable data, repeatable training commands, interpretable metrics, recoverable infrastructure, readable experiment reports, and an agent that can keep proposing the next step.

From that perspective, rebuilding AlphaGo is not nostalgia. It is a way to train the next generation of automated researchers.
