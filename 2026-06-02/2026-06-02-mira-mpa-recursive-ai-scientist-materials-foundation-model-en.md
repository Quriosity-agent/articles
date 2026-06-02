# MIRA / MPA Deep Dive: The Important Part Is Not “A New Materials Model,” but Turning Model R&D into a Recursive Loop

> **TL;DR:** The WeChat article and Deep Principle’s MPA technical report are not just about another SOTA result in materials property prediction. The important signal is that an **AI Scientist system, MIRA, is beginning to automate the model-development workflow itself**: literature research, code refactoring, data cleaning, training strategy, loss functions, readout design, evaluation, and iteration. MPA’s improvements across 40 experimental property tasks suggest that early hard metrics for “AI for AI / AI for Science” are starting to appear.

- **Source:** [AGI将至！40项实验全面SOTA，超级递归智能体自主打造最强材料基座模型](https://mp.weixin.qq.com/s/Do3sauQ8oSoRluaCptYe-g)
- **Technical report:** [Materials Property Axiom: Scaling Foundation Models to Experimental Property Generalists via Multi-phase Training](https://www.deepprinciple.com/papers/mpa.pdf)
- **Report date:** 2026-06-01
- **Tags:** AI Scientist / MIRA / Materials Property Axiom / MPA / AI for Science / Recursive Self-Improvement / Materials Foundation Model / Experimental Property Prediction

![MPA cover](imgs/mira-mpa-recursive-ai-scientist/00-cover.jpg)

## 1. Why this is bigger than “a materials model reached SOTA”

The original article places MPA in a larger context: recursive self-improvement is moving from an AGI concept into an operational R&D workflow. Anthropic’s Jack Clark has publicly discussed the probability of recursive self-improvement by the end of 2028, OpenAI has posted roles for recursive self-improvement safety research, and AI4S has already seen systems such as Co-Scientist, FutureHouse Robin, and Google ERA.

![Recursive self-improvement discussion](imgs/mira-mpa-recursive-ai-scientist/02-jack-clark-recursive-self-improvement.png)

Deep Principle’s **Materials Property Axiom (MPA)** looks, on the surface, like a model for materials experimental property prediction. But the deeper point is that it was developed with the help of **MIRA**, an AI Scientist platform. According to the article, MIRA handled key parts of the research process: preliminary research, backbone model adaptation and updating, automated training and evaluation loops, experiment analysis, and report drafting.

That is why this is more interesting than a normal SOTA announcement. If an agent can refactor code, clean data, design training workflows, run ablations, read experimental feedback, and continue iterating inside a specialized field such as materials science, it is no longer merely a tool caller. It is becoming a primitive R&D operating system.

![MPA overview](imgs/mira-mpa-recursive-ai-scientist/03-mpa-overview.png)

## 2. MPA targets experimental properties, not just computational properties

A common route for materials foundation models has been “brute-force scaling”: larger models, larger computational-property datasets, and larger GPU clusters. The WeChat article mentions Suiren-1.0, released in March 2026 by the Shanghai AI Laboratory for Science, as a 1.8B-parameter molecular foundation model trained with 320 NVIDIA H800 GPUs and roughly 70 million quantum-chemistry molecular conformations, beating the long-standing UniMol family.

The structural blind spot, highlighted by Deep Principle’s report, is that many materials foundation models focus mainly on **computational properties** such as thermodynamic stability, adsorption energy, and other quantum-chemistry-derived labels. These properties are scalable and relatively clean, but they are still one step away from industrial materials discovery.

Real materials R&D cares about **experimental properties**: boiling point, flash point, toxicity, solubility, enthalpy of combustion, Gibbs free energy, and similar endpoints. These are harder for three reasons:

1. **Sparsity:** experiments are expensive, so many endpoints have limited samples;
2. **Noise:** measurements vary across labs and conditions;
3. **Mechanistic heterogeneity:** thermodynamic, interfacial, biological, intensive, and extensive properties follow different physical mechanisms.

So the question is not simply whether we can add more data. The question is whether a model can learn transferable physical structure across tasks. MPA’s central hypothesis is exactly that: transfer across materials property tasks is governed not only by statistical similarity, but by shared physics.

## 3. MIRA’s AutoResearch: from humans tuning models to AI doing model R&D

![MIRA AutoResearch](imgs/mira-mpa-recursive-ai-scientist/04-mira-autoresearch.png)

The AutoResearch architecture described in the article is the key. Human scientists provide intent and stage-level review, while MIRA autonomously performs literature research, code implementation, data processing, model training, result analysis, and next-step planning.

![AutoResearch architecture](imgs/mira-mpa-recursive-ai-scientist/05-autoresearch-architecture.png)

This differs from ordinary AutoML. AutoML usually searches hyperparameters, model structures, or pipeline combinations. MIRA works on a broader R&D object:

- research-path selection: deciding whether a UniMol-v2-style 3D pretrained encoder is a reasonable starting point;
- code refactoring: adapting model code and standardizing pre-training, mid-training, and post-training interfaces;
- data engineering: integrating OPERA, Yaws, CRC, TDC, MoleculeNet, and other sources;
- data cleaning: handling unit inconsistency, duplicate samples, label noise, suspicious points, and leakage risks;
- training strategy: designing a three-phase training framework;
- architecture design: introducing hybrid readout with attention pooling and atomic summation branches;
- evaluation iteration: adjusting the system based on feedback across 40 experimental endpoints.

![MIRA brainstorm](imgs/mira-mpa-recursive-ai-scientist/06-mira-brainstorm.png)

The valuable part is the loop. MIRA does not generate a plan once and stop. It reportedly ran more than a hundred “hypothesis → verification → adjustment” cycles over roughly a month. Each round of results changed the next round’s data, architecture, loss function, or inference strategy.

## 4. Three-phase training: moving the LLM training pattern into materials models

![Three-stage training](imgs/mira-mpa-recursive-ai-scientist/08-three-stage-training.png)

The MPA report’s title is explicit: **Scaling Foundation Models to Experimental Property Generalists via Multi-phase Training**. The idea borrows the training pattern of large language models:

1. **Pre-training:** learn general representations from a broad corpus;
2. **Mid-training / alignment:** align the model using high-quality, capability-relevant data;
3. **Post-training / task SFT:** perform supervised fine-tuning for downstream tasks.

MPA transfers this pattern to materials models, but with a crucial change: mid-training data should not be selected merely because it is available or large. It must share physical mechanisms with the downstream experimental endpoint.

According to the technical report abstract, MPA improves mean absolute error by about 15% on average compared with direct fine-tuning from a pretrained model, with up to about 55% improvement on selected individual properties. The WeChat article uses a slightly different framing: across 40 experimental property prediction tasks, MPA refreshes SOTA, reduces average MAE by about 10%, and reaches a maximum reduction of about 51%; it also says MPA beats Suiren on 35 of 40 comparable endpoints and reduces average error by another 5.4%. The numbers differ by evaluation framing, but the direction is consistent: multi-phase training materially improves experimental property prediction.

![Physical alignment](imgs/mira-mpa-recursive-ai-scientist/09-physical-alignment.png)

This matters for AI4S. It suggests that materials-model scaling is not just “more molecules plus bigger models.” It also needs **physically aligned mid-training**. In other words, materials models need their own version of instruction tuning / alignment, but the alignment target is not human preference. It is physical mechanism.

## 5. Hybrid readout: putting physical priors back into the model structure

![Hybrid readout](imgs/mira-mpa-recursive-ai-scientist/10-hybrid-readout.png)

One elegant MPA design is **hybrid readout**. During iteration, MIRA found that different experimental properties have different physical structures:

- some are **extensive properties**, scaling approximately additively with molecular size, such as some thermodynamic quantities;
- others are **intensive or non-additive properties**, such as flash point, where simple atomic summation is insufficient.

MPA therefore combines two readout paths:

1. **Attention pooling branch:** a flexible non-additive molecular summary;
2. **Atomic summation branch:** an atom-level decomposition and summation path, giving the model an inductive bias for extensive properties;
3. **Learnable coefficient α:** a task-adaptive weight that lets the model balance the two branches.

This is not merely a deep-learning trick. It encodes physical priors into the architecture. The article says hybrid readout reduces MAE by up to 21.38% under scaffold split for thermodynamic quantities, while the attention branch dominates on non-additive properties.

That suggests MIRA’s value is not just automatic hyperparameter tuning. It can identify a physical classification behind the task and translate that classification into architecture design.

## 6. Data cleaning and loss functions: the real scientific intuition lives in the dirty work

A serious test for an AI Scientist is not whether it can write elegant equations, but whether it can handle messy real data. MPA’s downstream benchmark covers 40 experimental property tasks from OPERA, Yaws Handbook, CRC Handbook, TDC, MoleculeNet, and other sources. These sources contain unit inconsistencies, duplicates, outliers, label noise, and possible data leakage.

The article emphasizes that MIRA performed multi-stage cleaning and used physical intuition to identify suspicious data. For example, if a molecule’s boiling point was inconsistent with its molecular weight and functional groups, MIRA could flag it as suspicious and remove it.

On the objective-function side, MIRA also replaced MSE with Huber / Smooth L1 loss to reduce the impact of extreme experimental outliers. The report similarly emphasizes that readout and training objective determine how structure is mapped to scalar endpoints.

For industry, this kind of “dirty-work automation” may be more valuable than any single model trick. In real materials projects, the bottleneck is often not running the model. It is making the data clean enough to trust.

## 7. Final results: SOTA is the outcome; robust generalization is the real signal

![Final results](imgs/mira-mpa-recursive-ai-scientist/11-final-results.png)

The WeChat article summarizes MPA’s final results as follows:

- compared with a pretrained-only baseline, 38 of 40 experimental properties improve, with average error reduced by 14.0%;
- thermodynamic properties benefit most: enthalpy of combustion error drops by 51.1%, Gibbs free energy by 31.6%;
- against Suiren, MPA wins on 35 of 40 comparable endpoints and reduces average error by another 5.4%;
- out-of-distribution generalization is more robust: on new molecular scaffolds, MPA degrades by 25.7%, compared with 31.8% for Suiren.

The last point is especially important. Materials discovery cares about molecules, scaffolds, and combinations the model has not seen before, not just clean in-distribution numbers. MPA’s smaller degradation under scaffold / out-of-distribution evaluation suggests that it may have learned more transferable physical structure.

![MIRA iteration log](imgs/mira-mpa-recursive-ai-scientist/12-iteration-log.png)

## 8. What to be cautious about

This is important, but it should not be treated as “AGI has arrived.” Several things should be separated:

1. **MPA is strong evidence, not full recursive self-improvement:** it shows AI participating in model R&D and forming an iterative improvement loop, but humans still set goals, review stages, and constrain the process.
2. **The results need third-party replication:** both the article and technical report come from the releasing team. Public data, code, model weights, evaluation protocol, and independent replication will matter.
3. **Materials science is not a universal template for all science:** property prediction has clear benchmarks and numeric metrics, making it suitable for automated iteration. Open-ended theory discovery, experiment design, and wet-lab loops are harder.
4. **Agent safety and auditability become central:** once agents edit code, filter data, run training, and draft reports, logs, version control, leakage checks, cost limits, and human review must become product features.

The more precise conclusion is: MIRA / MPA is not AGI itself. It is a measurable milestone on the path toward more autonomous AI research systems.

## 9. My read: AI Scientist competition will move from “tool use” to “improving the R&D system”

MIRA / MPA also has implications for agent-native systems such as QCut and OpenClaw. A real agent product should not stop at “run this command for me.” It should form an auditable improvement loop:

- define the goal;
- decompose the R&D path;
- change code and data;
- run experiments;
- read results;
- propose the next hypothesis;
- preserve evidence;
- ask for human review at the right checkpoints.

That is the practical meaning of “AI for AI.” It does not require a model to suddenly wake up. It means more and more parts of the R&D workflow are being taken over by agents, with each loop producing measurable improvement.

MPA’s significance is exactly there. It turns recursive self-improvement from a philosophical discussion into a concrete question: can an AI Scientist produce a stronger materials foundation model? Across these 40 experimental property tasks, the answer is beginning to look like yes.

## Appendix: media archive

This article preserves the key visual assets from the original WeChat post. Two additional source images not discussed in the main body are archived below for future reference:

![Article title bar](imgs/mira-mpa-recursive-ai-scientist/01-title-bar.png)

![MIRA model choice](imgs/mira-mpa-recursive-ai-scientist/07-model-choice.png)
