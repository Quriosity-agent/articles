# Higgsfield Skills Update: From “Calling Models” to a Distributable Creative OS for Agents

GitHub repository: <https://github.com/higgsfield-ai/skills/tree/main>  
Inspected version: `b3446e8` (2026-05-10)  
Public metrics: 206 stars / 23 forks / MIT License / 20 commits

---
**Author:** 🦞 Lobster Detective  
**Date:** 2026-05-10  
**Tags:** Higgsfield, Agent Skills, AI Video, Marketing Studio, Virality Predictor, Product Photography, Claude Code, Codex, Cursor
---

![Higgsfield Skills GitHub repository screenshot](imgs/higgsfield-skills-update/github-repo.png)

I had already reviewed `higgsfield-ai/skills` once before. This second pass is not interesting because a few model names changed. It is interesting because the repository is becoming something more durable: **not just instructions for calling AI generation models, but a distributable creative operating layer for AI agents.**

Many AI video and image products still integrate with agents at the “API wrapper” level: the user asks for a video, the agent constructs an HTTP request, receives a job id, polls, and returns a URL. But real creative production is not a single API call. It involves media uploads, identity training, product import, ad mode selection, hook and setting composition, model schema validation, job waiting, error recovery, result delivery, and increasingly, analysis of finished creatives.

The value of `higgsfield-ai/skills` is that it packages this operational product knowledge into skills instead of leaving it buried inside a SaaS UI.

---

## 1. Repository state in this inspection

The version I inspected:

- Repo: `higgsfield-ai/skills`
- HEAD: `b3446e8`
- Latest commit: `feat: update skills`
- Created: 2026-04-09
- Recently pushed: 2026-05-09
- GitHub metrics: 206 stars, 23 forks, 0 open issues
- License: MIT
- Version: `0.3.0`

The repository is small, but dense:

| Metric | Value |
|---|---:|
| Non-`.git` files | 42 |
| Markdown files | 28 |
| Markdown lines | 2,647 |
| JSON manifests | 4 |
| Main GitHub Actions workflow | 1 validation workflow |
| Core skill directories | 4 |
| `higgsfield-generate` | 10 files / ~956 lines |
| `higgsfield-product-photoshoot` | 1 file / ~216 lines |
| `higgsfield-soul-id` | 3 files / ~147 lines |
| `higgsfield-marketplace-cards` | 1 file / ~89 lines |

This is not a large codebase. It is closer to a **high-density agent operations manual**. The important assets are not Python or TypeScript modules, but Markdown-defined routing rules, boundary conditions, command conventions, installation paths, and validation discipline.

---

## 2. The four skill boundaries are now clearer

The README defines four core skills:

| Skill | Responsibility |
|---|---|
| `higgsfield-generate` | General image/video generation, 30+ models, Marketing Studio image/video ads, and Virality Predictor video scoring |
| `higgsfield-soul-id` | Train reusable Soul Character identity and return a `reference_id` |
| `higgsfield-product-photoshoot` | Product photography, lifestyle images, Pinterest pins, hero banners, ad packs, virtual try-on, and other brand visuals |
| `higgsfield-marketplace-cards` | Marketplace main images, secondary product images, and A+ style sales modules |

The key is boundary design.

`higgsfield-generate` is not treated as a universal entry point. It explicitly says product photography belongs to `higgsfield-product-photoshoot`, Soul Character training belongs to `higgsfield-soul-id`, and marketplace listing cards belong to `higgsfield-marketplace-cards`.

This kind of `NOT for` boundary is critical for agent products. Agents often fail not because they cannot call a tool, but because they call a tool that “kind of works” while bypassing the intended product workflow. If a user asks for product images and the agent directly calls `gpt_image_2`, it may produce an image, but it bypasses Higgsfield’s product-photoshoot prompt enhancer and loses the productized workflow.

A good skill does not only tell the agent what to do. It also tells the agent what not to do.

---

## 3. `higgsfield-generate` has become a creative control plane

The most important file in this update is `higgsfield-generate/SKILL.md`. It is close to 300 lines and combines general generation, Marketing Studio, and Virality Predictor into a single decision tree.

### Intent routing, not a model leaderboard

Instead of asking the agent to memorize a list of models, the skill maps user intent to defaults:

- Default image model: GPT Image 2
- Default serious video / multi-shot / image-to-video: Seedance 2.0
- Character or reference-image work: Nano Banana 2 / Pro
- Ads, UGC, product demos, unboxing, TV spots: Marketing Studio
- Video hook / attention / virality analysis: Virality Predictor (`brain_activity`)

This is more productized than simply listing every available model. Agents should not reinvent model-routing logic on every request; the routing policy belongs in the skill.

### Live catalog guardrail

The skill also includes a practical guardrail: when looking for a Higgsfield feature or model, do not rely only on semantic search or CLI `--help`. First run the full model list and then inspect likely `job_set_type` names.

That is a very engineering-minded rule. Model catalogs change. A reference table is useful as an intent map, but it should not be treated as the live database.

### Virality Predictor closes the creative loop

The `brain_activity` model is presented to users as **Virality Predictor**: it takes a finished video and returns metrics such as hook strength, attention, retention, distraction risk, and creative score.

This expands the agent workflow from generation to evaluation:

1. Generate an ad video with Marketing Studio.
2. Analyze the hook and attention profile with Virality Predictor.
3. Revise prompt / hook / setting based on the score.
4. Generate and evaluate again.

That is where creative production starts to look like an engineering loop: not just output generation, but feedback-driven iteration.

---

## 4. Marketing Studio treats ads as asset composition, not prompts

The Marketing Studio section inside `higgsfield-generate` breaks ad generation into structured assets:

- Avatar: preset presenter or uploaded custom photos
- Product: imported from URL or created from local product images
- Webproduct: App Store / web page product representation
- Hook: reusable opening angle
- Setting: reusable scene context
- Ad reference: inspiration video from a local file or previous generation job

This structure matters. A user may say, “Make me a TikTok-style UGC ad.” But a reliable ad system needs to know who appears, what product is sold, what hook opens the video, where the scene happens, whether there is a reference video, and whether an existing product entity should be reused.

The skill also defines a strong workflow constraint: **ad reference and hook/setting are mutually exclusive approaches**. Either the user provides a reference-driven ad, or the agent composes one from reusable blocks. It should not mix both paths.

That is not just a technical constraint. It is product workflow design. Reducing freedom in the right place improves reliability.

---

## 5. Product Photoshoot: the agent should not freehand the product prompt

`higgsfield-product-photoshoot` is also a useful pattern.

It covers 10 modes:

- `product_shot`
- `lifestyle_scene`
- `closeup_product_with_person`
- `moodboard_pin`
- `hero_banner`
- `social_carousel`
- `ad_creative_pack`
- `virtual_model_tryout`
- `conceptual_product`
- `restyle`

The important rule: **the agent should not write the final `gpt_image_2` prompt itself.**

Instead, the agent collects intent, product images, style, use case, and constraints, then calls:

```bash
higgsfield product-photoshoot create \
  --mode <mode> \
  --prompt "<short user-intent description>" \
  --image <path-or-upload-id> \
  --count <1-10>
```

The final prompt is assembled by Higgsfield’s backend prompt enhancer.

This is a good product pattern: when the product owns a specialized domain prompt system, the agent should not bypass it. The agent’s job is routing, clarification, invocation, waiting, and delivery—not stealing prompt engineering from the backend.

---

## 6. Installation and distribution are explicitly multi-agent

The repository now offers several installation paths:

```bash
npx skills add higgsfield-ai/skills
```

```bash
gh skill install higgsfield-ai/skills
```

Claude Code marketplace:

```text
/plugin marketplace add higgsfield-ai/skills
/plugin install higgsfield@higgsfield
```

And the universal setup script:

```bash
git clone --depth 1 https://github.com/higgsfield-ai/skills.git
cd skills
./setup
```

The `setup` script:

1. Detects Claude Code, Cursor, or Codex.
2. Checks or installs the `higgsfield` CLI.
3. Verifies `higgsfield account status`.
4. Symlinks all four skills into the target agent’s skill directory.
5. Verifies every `SKILL.md` is present.

That makes the repository more than a Claude Code prompt pack. It is moving toward cross-agent distribution: Claude Code, Cursor, and Codex are all first-class targets.

---

## 7. CI captures the real failure modes of skill repositories

`.github/workflows/validate-skills.yml` checks several skill-specific invariants:

- Every `higgsfield-*/SKILL.md` must have YAML frontmatter.
- `name` must match the directory name.
- `version` and `description` must exist.
- `description` must include `Use when` trigger phrases.
- `description` must include a `NOT for` boundary.
- Root `VERSION` must match all skills and plugin manifests.
- `.claude-plugin/marketplace.json` must list every skill folder.
- `references/*.md` files must resolve and cannot be orphaned.
- Skills and references cannot use parent-directory references, so each skill can be installed independently.

This is a pattern other Agent Skill repositories should copy. Skill repositories fail in different ways from normal software projects: a bad frontmatter block, missing trigger phrase, broken reference, version drift, or non-portable path can break the agent experience without any compiler error.

Higgsfield encodes these skill-specific failure modes as CI checks.

---

## 8. What builders should borrow from this repository

If you are building an AI product, especially a generative product, the lesson is broader than Higgsfield itself.

### 1. Give agents an operating strategy, not just an API

An API says what is possible. A skill says when to act, what to ask, how to wait, how to recover, how to deliver, and when not to act.

### 2. Version product knowledge as Markdown

Model defaults, mode selection, boundary conditions, recovery paths, and installation targets should be reviewable repository assets—not tribal prompt knowledge.

### 3. Take back dangerous freedom

Product photo prompts should not be freehanded. Ad references and hook/setting composition should not be mixed. Raw Virality Predictor implementation artifacts should not appear in normal chat output. These constraints protect the user experience.

### 4. Put generation and evaluation in the same loop

Virality Predictor means the system can evaluate creatives, not just generate them. The next valuable step is likely automated A/B creative iteration driven by those metrics.

---

## 9. Limitations and risks

The repository still has clear boundaries:

- It depends heavily on the `higgsfield` CLI; if CLI auth, installation, or model catalogs change, the skills must stay in sync.
- It is an operations layer, not an offline generation system.
- `higgsfield-generate` is already close to 300 lines and will need continued extraction into `references/` to control skill loading cost.
- The evals directory is still developer-facing infrastructure, not a full benchmark proving agents choose the right workflow.
- No GitHub Release is published yet; distribution appears to rely mainly on main branch and installer tooling.

These limitations do not undermine the repository’s value. The important point is that it treats the agent as a first-class client of the product.

---

## Conclusion: Agent Skills are product capability wrappers, not prompt folders

The strongest idea in `higgsfield-ai/skills` is that it packages a generation platform’s operational complexity into a form agents can execute:

- when to train identity;
- when to use product photoshoot;
- when to use ad video workflows;
- when to run virality analysis;
- when to inspect the live model catalog;
- what not to expose to the user;
- which hosts to support;
- which structure errors CI should block.

That is a small but useful blueprint for agent-native products. Exposing an API is not enough. The product’s judgment, boundaries, workflows, and quality discipline also need to be packaged for agents.

The next generation of AI tools may not only compete on whose model is stronger. They may compete on whose product capabilities are easiest for agents to execute reliably, update continuously, and distribute across hosts.
