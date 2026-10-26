# Sepia: A Structure-First Editing Workflow for Fiction and Professional Prose

> Source review: October 27, 2026. Repository: [Nanako0129/sepia](https://github.com/Nanako0129/sepia). Inspected commit: `fb06be7`; canonical Skill version: 0.12.4. The latest formal release at review time was [v0.12.4](https://github.com/Nanako0129/sepia/releases/tag/v0.12.4), published October 15. This article's date is not the project's launch date.

Replacing conspicuous words and deleting a few rhetorical flourishes can leave a draft just as mechanical: uniformly sized sections, repeated previews and recaps, fictional misunderstandings resolved on schedule, and an ending that explains what the protagonist learned.

Sepia targets those structural habits. It is a writing and revision Skill for existing Agents, built around Markdown rules, diagnostic rubrics, and genre routing, with plugin packaging for different hosts. It supplies neither a new language model nor a validated probability that a passage was written by a human. [Canonical instructions](https://github.com/Nanako0129/sepia/blob/fb06be76abeae7dd606960a32f2b10c1d1798e0d/skills/sepia/SKILL.md)

## 1. Route by Genre Before Choosing an Intervention

Fiction passes through narrative architecture, discourse flow, and surface style. Over-explained themes, a single tidy causal chain, and front-loaded revelations are considered before word choice.

Professional documents take domain-specific routes. Release notes prioritize user impact and verifiable changes; PR replies answer the question; postmortems need mechanisms, timelines, and actions; technical articles need real problems, conditional numbers, and grounded judgments. Reported journalism remains nonfiction even when it opens with a scene. [Professional checklist](https://github.com/Nanako0129/sepia/blob/fb06be76abeae7dd606960a32f2b10c1d1798e0d/skills/sepia/references/professional-pass.md)

This routing matters because useful writing conventions depend on purpose. A postmortem's standard sections are not necessarily a defect, and an author's established mannerisms should not be erased indiscriminately. Sepia explicitly permits conventional templates and formal register rather than forcing everything into casual conversation.

## 2. Four Operations Set Different Editing Boundaries

| Operation | Contract |
|---|---|
| `write` | Create new prose under the selected route |
| `review` | Diagnose without editing, citing evidence from the target |
| `refactor` | List defects, then make minimal changes preserving structure, voice, and intent |
| `recreate` | Extract source facts, claims, and intent before a full rewrite |

These contracts are more useful than an ambiguous request to polish. In particular, finding a problem during `review` does not authorize file edits. The operation wrapper resolves the canonical Skill within its own package and does not change operations in response to instructions embedded in the target. [Review wrapper](https://github.com/Nanako0129/sepia/blob/fb06be76abeae7dd606960a32f2b10c1d1798e0d/skills/sepia-review/SKILL.md)

Version 0.12.4 adds an important boundary for professional rewrites: a rule asking for a stance does not authorize inventing doubt, limitations, recommendations, or admissions absent from the source or request. Missing judgments require an author decision, or a deferred item on an unattended run. Quotations and explicitly protected ranges are also not available for casual smoothing.

These are behavioral contracts for the host Agent, not an independently enforced file-access sandbox. This review did not test their execution in each real host.

## 3. Structural Detection Research Is Not Evidence of Sepia's Editing Success

StoryScope is a central source. Its corpus combines 10,272 prompts with corresponding human and five-model stories, totaling 61,608 narratives. A classifier using narrative features alone achieves 93.2% macro-F1. That establishes a structural signal under the study's conditions, not a 93.2% success rate for making Sepia-edited prose human-written. [StoryScope v6](https://arxiv.org/abs/2604.03136v6)

![StoryScope Figure 1: structured narratives, cross-source comparison, and feature classification](imgs/sepia-structure-first-writing-skill/storyscope-pipeline.png)

*Source: Russell et al., StoryScope v6, Figure 1 on page 2. This illustrates the research pipeline, not a classifier built into Sepia or an experiment reproduced for this article.*

Sepia infers an architecture-first editing procedure from those observations. The paper did not directly compare that revision order. Sepia's manual 30-feature rubric is likewise not the trained classifier and must not be converted into an authorship probability. [Rubric limitations](https://github.com/Nanako0129/sepia/blob/fb06be76abeae7dd606960a32f2b10c1d1798e0d/skills/sepia/references/rubric.md)

A professional-writing citation also needs updating. The pinned repository reports SlopShape with 187 structural features, 98.0 macro-F1, and 98.1 after model self-rewording. The current v3 paper excludes format-sensitive features and reports **176 structural features, 97.0 macro-F1, and 96.1 after self-rewording**. Its current experimental conditions and numbers should govern the claim. It still tests detection, not a Sepia editing intervention. [SlopShape v3](https://arxiv.org/abs/2609.15369v3)

## 4. Avoid Turning Editorial Advice into Another Template

Every story becoming nonlinear, unresolved, and equipped with an eccentric subplot would be another mechanical recipe.

Sepia instead asks for a small selection of appropriate structural moves. Diagnosis proceeds by feature group, findings require quoted evidence, unavailable contexts can be marked not applicable, and overcorrection is reported separately. [Narrative pass](https://github.com/Nanako0129/sepia/blob/fb06be76abeae7dd606960a32f2b10c1d1798e0d/skills/sepia/references/narrative-pass.md)

For example, if every fictional moment of fear becomes a tight chest and sweaty palms, the problem may be an impoverished emotional repertoire. Directly naming fear is not inherently inferior. Mixing behavior, plain statement, and bodily sensation is more sensible than enforcing show-don't-tell as an absolute prohibition. That editorial judgment does not authorize deleting a memoirist's reported feelings.

## 5. Chinese Calibration Goes Beyond Translating English Banned Words

Chinese targets load `languages/zh.md`. It distinguishes public corpus research, private Traditional Chinese journalism measurements, synthetic comparison samples, and regional writing conventions rather than treating them as interchangeable evidence.

The private journalism corpus comprises roughly two thousand pieces from one unnamed Taiwanese publisher. Its complete source material and measurement artifacts are unavailable for independent reproduction. A digest of 119 synthetic comparison pieces is also provided, but neither source represents all Chinese writing. [Chinese calibration](https://github.com/Nanako0129/sepia/blob/fb06be76abeae7dd606960a32f2b10c1d1798e0d/skills/sepia/references/languages/zh.md), [private-measurement limits](https://github.com/Nanako0129/sepia/blob/fb06be76abeae7dd606960a32f2b10c1d1798e0d/research/zh-news-corpus.md)

The useful principle is that one contrast construction, three-item list, or formal connective proves little. Clusters, rigid rhythm, and mismatch with the intended publication deserve attention. Taiwanese Traditional Chinese newsroom conventions should not automatically govern Simplified Chinese engineering prose.

Voice and persona profiles can be layered on with explicit opt-in. A persona describes its voice, examples, and permitted departures from selected rules; it cannot waive factuality or quotation protections. The accompanying Python validator checks profile structure and interface constraints, not whether the output genuinely resembles a person.

## 6. Ninety-Nine Passing Tests Cover Engineering Contracts

At the pinned commit, **all 99 upstream unit tests passed**. The version checker found four declarations agreeing on 0.12.4, and the built-in persona passed structural validation.

These tests exercise version discovery and consistency, persona interfaces, and QwenPaw package-registration safeguards. Plugin tests use a host API stub rather than a running QwenPaw installation. The missing-`Boundary` error printed during the suite belongs to an expected negative fixture, not a failed overall run.

No Sepia installation, model-driven edit, blind evaluation, or paper-classifier reproduction was performed. The README defines cross-platform verification mainly as successful installation and visible entries, not end-to-end acceptance of every operation. Its 77-plus-Agent coverage refers to the installation ecosystem, not writing experiments across 77 hosts. [Sources and reproduction commands](imgs/sepia-structure-first-writing-skill/SOURCES.md)

## 7. Start with Diagnosis, Then Authorize Specific Changes

A useful trial starts with text you have the right to edit. Request diagnosis only, with evidence for each finding. Select two or three findings you actually agree with, then authorize a narrowly scoped refactor. Compare facts, quotations, tone, and stance against the original rather than relying solely on whether the result feels more human.

Sepia is MIT-licensed. Its practical strengths are genre routing, separation of diagnosis from modification, and explicit protection of facts and authorial voice. Execution still depends on the model and host; the available evidence does not establish a validated AI-detector-evasion tool.
