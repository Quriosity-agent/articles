---
title: "Anthropic's ART Discovery: Claude Did Not Find 'CRISPR 2.0,' but It Did Recognize an Anomaly in Raw DNA"
date: 2026-09-23
source: "https://x.com/AnthropicAI/status/2102824959827742916?s=20"
canonical: "https://www.anthropic.com/news/claude-discovers-novel-enzyme-system"
paper: "https://www-cdn.anthropic.com/22573675ada52a8ca8a97a1a4b4326b2f208a071.pdf"
tags:
  - Anthropic
  - Claude
  - AI for Science
  - Autonomous Agents
  - Genome Mining
  - Reverse Transcriptase
  - CRISPR
  - Molecular Biology
---

# Anthropic's ART Discovery: Claude Did Not Find 'CRISPR 2.0,' but It Did Recognize an Anomaly in Raw DNA

> **TL;DR:** Anthropic's new molecular biology lab has reported its first result. A multi-agent system powered by Claude Mythos 5 searched 1.9 billion protein clusters for reverse transcriptases and unexpectedly identified a previously undescribed system. The team named it array-associated reverse transcriptase, or ART. It combines a repetitive DNA array, a reverse transcriptase, and a partner protein; the array produces abundant short RNAs during phage infection. This is not evidence that Claude discovered “CRISPR 2.0.” The study has not demonstrated ART reverse-transcriptase activity, shown that the RNAs are its substrates, established interaction with the partner, or identified the system's biological function. The important new signal is that a general model did more than execute a predefined pipeline: it read raw DNA, noticed an anomaly outside the assigned search target, and passed that accidental clue into a shared research system for human validation.

- **X source:** [Anthropic announcement](https://x.com/AnthropicAI/status/2102824959827742916?s=20)
- **Canonical post:** [Claude discovers a novel enzyme system with CRISPR-like repeats](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system)
- **Technical preprint:** [Autonomous AI agents discover reverse transcriptases with tandem repeat arrays](https://www-cdn.anthropic.com/22573675ada52a8ca8a97a1a4b4326b2f208a071.pdf)
- **Published:** September 23, 2026
- **Research status:** Anthropic-authored preprint, not a peer-reviewed result
- **Checked:** September 24, 2026

![Official image from Anthropic's molecular biology lab](imgs/anthropic-claude-art-enzyme-discovery/01-anthropic-molecular-biology-lab.webp)

## The short answer

The value of this work is not that AI found the next gene editor. It demonstrates something closer to the beginning of real discovery: **the model noticed that something in the primary data was unusual without being instructed to search for that feature.**

Conventional automation is good at finding properties humans define in advance. Scientific discovery often starts elsewhere: a pattern does not fit an existing class, a sequence appears where it should not, or a candidate contradicts the working hypothesis. The ART lead emerged in exactly this way. The agents were asked to find new partner genes for reverse transcriptases. After rejecting an apparent association, they continued into upstream non-coding DNA and recognized an unannotated repetitive structure.

That matters more than simply saying a model processed 1.9 billion records. Scale can be purchased with compute. Deciding which anomaly deserves follow-up is the part of expert attention that has historically resisted scaling.

## What ART is

ART stands for **array-associated reverse transcriptase**. A reverse transcriptase, or RT, copies RNA into DNA. The researchers identified a recurring three-part arrangement in jumbo phages and predicted viral sequences:

1. an upstream non-coding DNA array;
2. a reverse transcriptase with an unusually long N-terminal region;
3. a dedicated partner-protein gene downstream.

Subsequent analysis found 95 ART RT clusters. Twenty-eight had a detectable repeat array upstream of the RT. The arrays span about 0.3 to 4.1 kb and contain three to 21 repeat units. Repeats are 15 to 49 nt long, separated by 120-to-220-nt spacers. The team also identified three mutually unrelated partner-protein families.

The architecture is “CRISPR-like” because both systems alternate repeats and spacers. Resemblance is not equivalence:

| Feature | CRISPR array | ART array |
|---|---|---|
| Basic structure | repeats plus spacers | repeats plus spacers |
| Spacer length | commonly about 30 nt | about 120 to 220 nt |
| Associated genes | Cas genes | RT plus partner; no nearby Cas genes |
| Change across related strains | spacers are often acquired or lost | spacer order is relatively conserved across related phages |
| Established function | adaptive immunity and programmable nucleic-acid targeting | unknown |

The precise claim is that ART has an array architecture reminiscent of CRISPR. It is not an established CRISPR system or gene-editing tool.

## How 949 sessions became a research system

Anthropic's X post says “roughly 950 agents.” The technical report gives the more exact unit: **949 agent sessions**, consisting of one launch session, 414 worker sessions, 375 supervisor sessions, 107 curator sessions, and 52 editor sessions. These were not 949 simultaneous, persistent digital scientists.

The campaign operated more like a computational lab with defined handoffs:

| Role | Responsibility |
|---|---|
| Worker | plan, write code, use databases and tools, submit results |
| Supervisor | review plans and results, request revisions, open follow-up tasks |
| Curator | enter completed findings into a shared knowledge base |
| Editor | review final research reports |

Plans, results, reviews, scripts, and knowledge-base entries went into a shared versioned record. Later agents could inherit earlier findings instead of restarting from an empty conversation. That is what allowed one worker's accidental observation to become a research branch rather than disappear in a transcript.

![Multi-agent research harness, screening pipeline, and path to the ART observation](imgs/anthropic-claude-art-enzyme-discovery/02-agentic-discovery-harness.webp)

The technical report gives the following scale:

| Metric | Reported value |
|---|---:|
| Search space | 1,939,242,578 protein clusters |
| RT clusters after filtering | 198,290 |
| RT classes | 9 |
| Sampled loci | 10,983 |
| Neighboring partner families | 3,564 |
| Total tasks | 119 |
| Completed / rejected / stalled | 107 / 10 / 2 |
| Follow-up tasks | 98 |
| Agent sessions | 949 |
| Summed agent time | 76.9 hours |
| Wall-clock time | 21.5 hours |
| Counted tokens | 215.6 million |
| Final reports | 19 |

The 215.6 million tokens comprise 11.3 million uncached input tokens, 14.9 million output tokens, and 189.5 million tokens written to the prompt cache. Cache reads were excluded. The 76.9 hours sum parallel session duration; the 21.5 hours cover only the autonomous search campaign, not subsequent human analysis and wet-lab work.

## The discovery did not follow the original task in a straight line

The initial mission was to find new RT partner proteins. One worker noticed some RTs next to a phage RNA-polymerase subunit, then concluded that the association was probably an artifact of gene order. A conventional pipeline might have discarded the candidate and stopped there.

Claude's supervisor retained a different question. The RTs resembled retrons, and retrons often have a non-coding RNA upstream. Should the next worker inspect the 5' flank? When that worker loaded the upstream DNA directly into context, it immediately said it could “see by eye” a tandem repeat array and considered CRISPR-like, msDNA-like, and DGR-like explanations.

It then did two important things:

1. wrote a repeat-counting script and found one locus with 14 copies of a 16-nt repeat;
2. ran a novelty kill-test to check whether this was merely a known system it had forgotten.

The paper audits that session log. No repeat finder ran before recognition, and neither the campaign brief nor task brief mentioned repeats or arrays. The raw sequence just loaded into context contained the pattern the agent identified. This does not prove that a model sees DNA like a human scientist, but it rules out the simplest explanation that a tool discovered the array and the model merely narrated the output.

## Wet-lab evidence supports the structure, not the function

Anthropic's team found in published Staphylococcus phage SA1 infection data that the ART array was highly expressed 5, 15, and 55 minutes after infection. At 15 minutes, array-derived RNAs accounted for as much as roughly 8% of phage RNA. Those transcripts also resolved into short RNA species with reproducible boundaries.

The researchers then expressed the SA1 ART system in E. coli and observed similar discrete RNAs by small-RNA sequencing. Together with recurring co-location of the RT, array, and partner, this supports the conclusion that one ART array produces multiple short RNAs.

![ART RNA expression, partner structures, and the still-hypothetical functional model](imgs/anthropic-claude-art-enzyme-discovery/03-art-rna-expression-and-hypothesis.webp)

The functional model in the paper is explicitly labeled as a hypothesis and still contains question marks. The Discussion lists what has not been shown:

- no demonstration that the ART RT itself is active;
- no demonstration that array RNAs are RT substrates;
- no demonstration that the RT and partner interact;
- no identified function for the phage;
- no evidence of programmability or gene-editing capability.

“A new molecular system was identified” is defensible. “A new gene-editing tool was discovered” is not.

## The counterintuitive result: more tools made the array easier to miss

The researchers converted ART into a fixed-input benchmark. Seven Claude models each ran 100 attempts at five information levels, totaling 3,500 attempts. Levels one and two placed proteins or loci directly in context. Levels three through five provided 96 loci as files, then progressively added bioinformatics tools, predicted structures, literature access, and the web.

More information should have helped. For repeat-array recognition, it often did the opposite. The strongest models recognized the array in at least 90% of attempts when loci were placed directly in context. In a file-and-tool setting, Opus 5 fell as low as 32% in one condition.

The tools did not erase capability. The agents often failed to inspect the data. With files, 39% of attempts never read a contiguous stretch of at least 200 nt, so the model could not see more than about one repeat unit. Once at least 200 nt of contiguous DNA entered context, recognition increased by 16 to 32 percentage points for each strong model. As more sequence was read, pooled recognition among the four strongest models rose from 29% to as high as 76%, and Mythos 5 reached up to 96%.

![Fixed-input ART benchmark showing that recognition depends on DNA entering model context](imgs/anthropic-claude-art-enzyme-discovery/04-dna-context-recognition-benchmark.webp)

This generalizes well beyond biology: **a mounted file is not an observation.** Giving an agent more tools, databases, and directories does not help if the harness never requires sampling, previewing, or validating the underlying data. Information can be accessible without entering the decision state.

## Internal signals are mechanistic evidence, not a complete explanation

The team replayed the original discovery transcript through a saved Mythos 5 checkpoint and decomposed activity at one layer with a sparse dictionary. They preselected 12 candidate signals on synthetic repeats and found two that increased on the ART repeats. Shuffling each repeat in place silenced one signal on 12 of 14 copies and the other on all 14.

That supports the claim that the model generated an internal response to repetition rather than mentioning repeats by linguistic chance. The boundary matters: the same signals also respond to repeated ordinary characters and are not DNA-specific. The analysis covers one layer and a replay through a saved checkpoint. A long causal chain still separates those signals from the final scientific judgment.

This is useful mechanistic evidence, not a complete account of how Claude discovered ART.

## The largest warning: ten reruns all missed ART

The team reran the same campaign ten times with the same harness and brief. Nearly every campaign that completed the census sampled ART loci, and two campaigns investigated the lineage as a follow-up. None of the workers read the DNA upstream of those RTs. Every rerun missed the repeat array.

This is crucial. It suggests the first discovery was not a scripted demo, while also showing that the automated process is not reliably reproducible. The model can recognize the anomaly when it sees it. It does not consistently make the meta-decision to look in the right place.

That defines the next engineering problem:

1. guarantee a minimum primary-data inspection for every high-value candidate;
2. allocate budget between search breadth and deep investigation;
3. teach supervisors to preserve branches that contain anomalies even after the main hypothesis fails;
4. cross-check discovery paths with independent campaigns, models, or tools;
5. distinguish “not observed” from “observed and not found” in the record.

An autonomous research system must report not only what it discovered, but where it never looked.

## How this differs from Anthropic's August biology result

This repository previously covered Claude's protein-binder design and NMR / LC-MS workflows. Those results showed that a model could orchestrate specialist tools, produce candidates, and process experimental data. ART advances a different and narrower claim: instead of optimizing a clearly specified task, the agent noticed an anomaly outside the mission while exploring a large unknown space.

| Layer | August result | ART result |
|---|---|---|
| Primary task | design candidates and process instrument files | find unknown systems in primary sequence data |
| Success criterion | binder hits and agreement with lab reports | a new structural lead supported by follow-up computation and experiments |
| Agent contribution | tool orchestration and long workflow execution | anomaly recognition and research-branch expansion |
| Main risk | unreliable candidates and analysis errors | stochastic discovery and overinterpreting unknown function |

ART does not reduce the importance of wet-lab scientists. It concentrates their time on experimental design, mechanistic validation, and the boundary between evidence and speculation.

## Practical lessons for research agents

The reusable architecture is not “open 949 sessions.” It is the following set of controls:

1. **Separate roles instead of merely adding concurrency.** Workers, supervisors, curators, and editors have different responsibilities and artifacts.
2. **Keep findings in a shared, versioned record.** Later agents need provenance, code, data, and review history.
3. **Let failed hypotheses open new branches.** Rejecting the initial association should not erase adjacent anomalies.
4. **Require primary-data observation.** File availability, tool access, and actual reading are different states.
5. **Make novelty kill-tests mandatory.** Every new claim should actively search for prior explanations and counterexamples.
6. **Let experiments establish facts.** Computation can prioritize candidates, but functional claims must be built one experiment at a time.

## What remains unverified

The study has substantial boundaries:

- it is an Anthropic-authored preprint and has not completed peer review;
- the model, harness, and experimental team belong to the same organization, without an independent external replication;
- the initial campaign had no mid-run human intervention, but humans wrote the brief, designed the environment, and performed follow-up analysis and experiments;
- ten replicate campaigns failed to rediscover ART, showing low path reliability;
- Mythos 5 judged the 19-report tournament, where the ART report ranked third, rather than an independent expert panel;
- Mythos 5 also graded the fixed-input benchmark against ten author-selected claims;
- the identified internal signals are not DNA-specific and cannot independently prove the discovery mechanism;
- ART enzyme activity, substrates, partner interaction, biological role, and programmability remain unknown.

Anthropic also states that its lab performs only BSL-1 and BSL-2 work, handles no pathogens capable of infecting humans, and uses human scientists for all wet-lab work. Those are operating boundaries for this project, not a general solution to the dual-use risk of increasingly capable biology agents.

## Conclusion

Claude did not deliver a new tool for editing genes. It delivered an anomaly worth human attention: in jumbo phages, a family of reverse transcriptases repeatedly appears beside a long DNA array and a partner protein, and the array produces abundant short RNAs during infection.

That observation is novel and concrete, while its function remains unknown. Calling it “CRISPR 2.0” obscures the more important advance. A general model directly read raw DNA, departed from the assigned search target, rejected an early explanation, and moved an anomaly into a verifiable research pipeline.

The ten failed reruns show how far this remains from an autonomous scientist. The system can understand the anomaly after looking at it, but cannot reliably decide where to look. Production-grade AI research infrastructure needs discovery ability, observation discipline, shared memory, reproducible paths, and experimental falsification at the same time. ART is a meaningful step in that direction, but it is still the first step.

## Sources

1. Anthropic X announcement
   https://x.com/AnthropicAI/status/2102824959827742916?s=20

2. Anthropic, “Claude discovers a novel enzyme system with CRISPR-like repeats”
   https://www.anthropic.com/news/claude-discovers-novel-enzyme-system

3. Peter H. Yoon et al., “Autonomous AI agents discover reverse transcriptases with tandem repeat arrays”
   https://www-cdn.anthropic.com/22573675ada52a8ca8a97a1a4b4326b2f208a071.pdf
