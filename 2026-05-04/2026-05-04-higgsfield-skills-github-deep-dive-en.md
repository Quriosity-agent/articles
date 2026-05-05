# Higgsfield Skills GitHub Deep Dive: Turning AI Video and Product Image Generation into Agent-Callable Workflows

GitHub repository: <https://github.com/higgsfield-ai/skills/tree/main>  
Inspected commit: `1dcfe26` (2026-05-04)

---
**Author:** 🦞 Lobster Detective / 龙虾侦探  
**Date:** 2026-05-04  
**Tags:** Higgsfield, Agent Skills, AI Video, AI Image Generation, Product Photography, Marketplace Cards, Soul ID, Claude Code, Codex, Cursor
---

Many AI generation tools do not fail because the model is weak. They fail because the model capability has not been turned into something an agent can reliably operate.

A human sees “generate an image” or “make a video.” But for an agent, the hard part is different: when should it train an identity? When should it use the product-photoshoot pipeline? When should it use Marketing Studio? When is generic image-to-video enough? Which parameters are valid? Which commands should wait until completion? How should result URLs be delivered? How should errors be recovered?

Higgsfield’s `skills` repository is not another frontend demo or model implementation. It is a set of **agent-facing creative production runbooks**. It wraps Higgsfield CLI capabilities — image generation, video generation, product photography, identity training, marketplace cards, and branded ad generation — into Markdown Skills that Claude Code, Codex, Cursor, and other agents can load, reason over, execute, and chain.

I cloned and inspected the repo. My conclusion: **the value of this repository is not code volume. It is product boundary design and workflow design. It upgrades “call a generation API” into “let an agent behave like a creative operations assistant.”**

---

## 1. What is this project?

The README defines it simply:

> AI agent skills for image and video generation via Higgsfield AI.

The repository currently ships four core skills:

| Skill | Responsibility |
|---|---|
| `higgsfield-generate` | General image/video generation across 30+ models, plus Marketing Studio for branded ad images and videos |
| `higgsfield-soul-id` | Train a Soul Character: a reusable face-faithful identity `reference_id` |
| `higgsfield-product-photoshoot` | Brand product photography: studio shots, lifestyle scenes, Pinterest pins, ad creatives, hero banners, virtual try-on |
| `higgsfield-marketplace-cards` | Marketplace listing assets: main images, secondary images, infographics, and A+ style modules |

Every skill routes through one binary: the `higgsfield` CLI. The repository’s `CLAUDE.md` emphasizes a crucial rule: **do not call the Higgsfield API directly with curl**. The CLI owns auth, retries, polling, schema validation, local media auto-upload, and job completion handling.

That matters. For generation products, the API call is only one step. The real experience depends on whether:

- local images can be uploaded automatically;
- long-running jobs can be waited on correctly;
- failures produce recoverable errors;
- final URLs are reliably extracted;
- model-specific parameter differences are hidden from the user.

Higgsfield Skills makes a clear design choice: **skills should handle decision-making and orchestration; the CLI should handle low-level API complexity.**

---

## 2. Repository scale: small, but disciplined

A quick scan of the repository shows:

- Around **38 files**.
- Around **3,021 lines** of text.
- **26 Markdown files / ~2,351 lines**.
- 4 skill directories.
- `higgsfield-generate/SKILL.md` is around **205 lines** and has **7 reference docs**.
- `higgsfield-product-photoshoot/SKILL.md` is around **220 lines**.
- `higgsfield-soul-id/SKILL.md` is around **84 lines** with 2 reference docs.
- `higgsfield-marketplace-cards/SKILL.md` is around **89 lines**.
- The repository includes `.claude-plugin/`, `.codex-plugin/`, and `.cursor-plugin/` manifests.
- GitHub Actions includes `validate-skills.yml`, which checks frontmatter, version sync, marketplace coverage, reference validity, orphaned references, and parent-directory references.

This is not a large application monorepo like Open Design. It is a compact **agent operations layer**. The files are few, but each file defines how an agent should behave in real creative tasks.

The CI rules are especially revealing:

- Every `higgsfield-*/SKILL.md` must have YAML frontmatter.
- `name` must match the directory name.
- `description` must include `Use when` trigger phrases and a `NOT for` boundary.
- The root `VERSION` must match all skill versions and all plugin manifest versions.
- Every referenced `references/*.md` file must exist.
- Every reference file must be linked from the skill.
- Skills and references cannot use `../` parent-directory references, so each skill remains self-contained.

These checks show that the project is designed for long-term agent loading and distribution, not just prompt snippets.

---

## 3. The key abstraction: a Skill is a decision tree, not a prompt

When people hear “AI skill,” they often imagine a prompt template.

Higgsfield Skills are written differently. Each `SKILL.md` is closer to a small decision tree:

- What user intents trigger this skill?
- What tasks should not be handled by this skill?
- How should the agent check CLI installation and authentication?
- What can be defaulted, and what must be asked?
- Which model or mode fits which job?
- When should the agent chain into another skill?
- How should the command be constructed?
- How should results be delivered?
- How should common errors be handled?

For example, the frontmatter of `higgsfield-generate` is very explicit:

- “generate an image,” “make a video,” “animate this photo,” “UGC video,” and “product demo” should trigger it.
- But “training Soul Character” should use `higgsfield-soul-id`.
- “Professional product photoshoots with mode-specific prompt enhancement” should use `higgsfield-product-photoshoot`.

That is what makes a good skill: **it tells the agent not only what to do, but when not to do it.**

In real products, wrong routing is often more dangerous than no routing. If a user asks for product imagery and the agent directly calls generic `gpt_image_2`, it may produce an image, but it bypasses Higgsfield’s product-photoshoot backend prompt enhancer and lowers output quality. The skill protects the product experience by encoding that boundary.

---

## 4. The four skills form a creative production chain

The most interesting part of the repo is that the four skills are not just a flat tool list. They form composable creative workflows.

### 4.1 `higgsfield-soul-id`: turn a person into a reusable asset

`higgsfield-soul-id` trains a Soul Character. The user provides 5–20 face photos, and the CLI returns a `reference_id`.

That ID can later be consumed by `higgsfield-generate`:

```bash
higgsfield generate create text2image_soul_v2 --prompt "..." --soul-id <ref_id> --wait
higgsfield generate create soul_cinema_studio --prompt "..." --soul-id <ref_id> --wait
```

The abstraction is important: identity becomes a reusable asset, not a one-shot face swap. For founder UGC, personal-brand videos, team updates, and ad avatars, this is exactly the right primitive.

### 4.2 `higgsfield-generate`: general generation and Marketing Studio

This is the largest skill. It covers text-to-image, image-to-image, image-to-video, reference-based generation, and Marketing Studio.

Its model-routing rules encode real product judgment:

- General images default to GPT Image 2.
- Serious image-to-video defaults to Seedance 2.0; cheaper simpler scenes can use Kling 3.0.
- Character/cartoon-style work can use Nano Banana 2.
- Advertising, commercial, and branded videos should use Marketing Studio.
- Soul-aware outputs should use Soul 2.0 or Soul Cinema.

The skill does not dump a model catalog on the user. It maps user intent to sensible defaults. That is exactly what agents need.

### 4.3 `higgsfield-product-photoshoot`: product visuals should not freestyle

This skill is explicit: for product photography, the agent should not hand-write a `gpt_image_2` prompt. It must call `higgsfield product-photoshoot create`, because the backend prompt enhancer owns mode-specific photography vocabulary and structured templates.

It supports 10 modes:

- `product_shot`: neutral / studio / catalog background.
- `lifestyle_scene`: real-world environment, hands, action, atmosphere.
- `closeup_product_with_person`: hands, partial face, beauty application, demonstration.
- `moodboard_pin`: Pinterest-native 2:3 vertical pin.
- `hero_banner`: website, email, or campaign header.
- `social_carousel`: multi-slide IG / LinkedIn / Facebook carousel.
- `ad_creative_pack`: static ad variants for Meta, TikTok, Pinterest, or Google Ads.
- `virtual_model_tryout`: product worn or used by an AI-rendered model.
- `conceptual_product`: levitating, splash, CGI, sculptural product imagery.
- `restyle`: change the aesthetic, season, or mood of an existing product image while preserving the subject.

This shows that Higgsfield has productized “product image generation” into concrete commercial use cases, rather than treating it as generic text-to-image.

### 4.4 `higgsfield-marketplace-cards`: listing assets as structured bundles

The marketplace skill goes even more vertical. It is not just making “nice product images.” It creates marketplace listing asset packs:

- `main`: 1 compliant main image.
- `product-images`: main image + 5 secondary images.
- `aplus`: main image + 7 A+ modules.
- `full-set`: main image + 5 secondary images + 7 A+ modules.

It also supports fine-grained assets such as infographic, multi-angle, detail shot, lifestyle, what’s-in-box, A+ hero banner, A+ features, A+ how-to-use, and more.

This is marketplace operations knowledge turned into an agent workflow. The user does not have to specify “one main image, five secondary images, seven A+ modules.” A request like “make marketplace listing images” can be routed to the correct bundle.

---

## 5. The Cookbook reveals the real product direction

`COOKBOOK.md` is worth reading because it shows how the skills combine into end-to-end workflows.

For example, “Brand Campaign from a Founder Photo”:

1. Train a Soul from the founder’s headshot.
2. Generate 5 lifestyle scenes around the product.
3. Pick the best 2 and animate them into short clips.
4. Deliver a campaign asset set.

That is not a single generation. It is a small creative workflow: identity asset + product asset + scene imagery + video animation.

Another recipe, “UGC Ad Batch from a Product URL,” does this:

1. Fetch product metadata from a Shopify URL.
2. Pick a preset avatar.
3. Generate four ad styles in parallel: UGC, unboxing, product review, and TV spot.
4. Deliver one ready video URL per mode.

This is where agents become valuable. They do not merely click “generate.” They orchestrate creative operations.

The cookbook hints at a broader future: Higgsfield Skills can become a **creative operations automation layer**. A user supplies a product, person, and campaign goal; an agent trains, generates, varies, and delivers assets.

---

## 6. Installation and distribution: one skill set, multiple agents

The repository is not only for Claude Code. It offers several installation routes:

```bash
npx skills add higgsfield-ai/skills
```

Or:

```bash
gh skill install higgsfield-ai/skills
```

Claude Code marketplace install is also supported:

```text
/plugin marketplace add higgsfield-ai/skills
/plugin install higgsfield@higgsfield
```

There is also a `./setup` script that detects Claude Code, Cursor, or Codex, installs the CLI if needed, checks auth, and symlinks the skill directories into the expected location.

That means the target is not “a private plugin for one agent.” The target is a cross-agent capability pack.

The repository includes manifests for:

- `.claude-plugin/`
- `.codex-plugin/`
- `.cursor-plugin/`

This matters because the agent ecosystem is moving from ad-hoc prompts and one-off plugins toward installable, verifiable, distributable skills. Higgsfield Skills is a small but clear example of that direction.

---

## 7. What builders should borrow

Several design lessons stand out.

### 7.1 API capability should be wrapped as user intent

Users do not say: “Call `marketing_studio_video` and pass JSON avatars, product IDs, and `mode=ugc`.”

They say: “Make four TikTok ads for this Shopify product.”

The skill’s job is to translate the second into the first reliably.

### 7.2 Vertical workflows deserve dedicated entry points

Product photography, marketplace cards, Soul ID, and generic video generation are not the same task. If all of them were stuffed into one `generate` skill, routing would become messy.

Higgsfield splits them into four skills, each with clear `Use when` and `NOT for` boundaries. This is practical product design.

### 7.3 Backend prompt enhancers are product assets

Both `product-photoshoot` and `marketplace-cards` emphasize that the agent should not write the final prompt itself. Backend enhancement owns that.

That means Higgsfield treats prompt engineering as a server-side product asset, not something every agent should freestyle. The agent gathers intent and chooses a mode; the backend converts that intent into high-quality generation prompts.

### 7.4 Result delivery should be restrained

Multiple skills state that the final answer should contain URLs and short labels only — no JSON dumps, no raw IDs, no internal model names, no enhanced prompt text.

That is good UX discipline. Agents often expose too much internal machinery. Creative-tool users want results, not job metadata.

### 7.5 Skills must be self-contained

The repository disallows `../` parent-directory references and ensures every reference file is linked from its `SKILL.md`. This makes each skill independently installable.

That matters for a skill ecosystem. A skill should be a distributable unit, not a fragile bundle of relative paths inside one repository.

---

## 8. Limitations and risks

The repository is useful, but its boundaries are clear.

First, it is not a full product by itself. It is the Agent Skills layer. The actual generation capability depends on the Higgsfield CLI and Higgsfield backend.

Second, the open repository mostly contains Markdown, manifests, setup scripts, and CI. The backend prompt enhancers for product photography and marketplace cards are not open here. You can inspect the calling boundary, not the full quality engine.

Third, generation workflows depend on auth, credits, paid plans, and long-running polling. Soul training requires a Basic+ plan and can take many minutes. Agents need good UX around waiting, failure, and confirmation.

Fourth, multi-agent distribution is still an early ecosystem. Claude Code, Codex, and Cursor may continue changing their skill/plugin loading conventions. Repositories like this need active maintenance.

Fifth, the public GitHub star count is still small. This currently looks more like Higgsfield’s official agent capability gateway than a broad community ecosystem.

None of these are fatal. They just clarify the positioning: this is not an open-source generation model, nor a full creative SaaS. It is a productized interface that lets coding agents operate Higgsfield’s creative generation stack.

---

## 9. Who should study it?

Three groups should look closely at this repository.

First, **AI generation product builders**. If your product generates images, video, audio, 3D, product visuals, or creative assets, do not stop at APIs. Provide agent-readable skills: triggers, boundaries, defaults, error handling, and delivery rules.

Second, **agent platform builders**. This repo shows a lightweight but practical distribution shape: Markdown skills + references + plugin manifests + setup script + CI validation.

Third, **growth, ecommerce, and UGC automation builders**. The real value is not “make one pretty image.” It is workflows like founder photo → Soul → lifestyle photos → video ads, or product URL → avatar → multi-style ad batch.

If you are building an AI video tool such as QCut, this is also worth studying. Higgsfield Skills does not focus on timeline editing. It focuses on automating the upstream asset-production pipeline so an agent can operate it end to end.

---

## Conclusion: Higgsfield Skills turns generation models into agent-operated creative tools

Higgsfield Skills is a small repository, but the direction it represents is important.

Future AI generation products should not only offer a web button, and they should not only expose raw APIs. They should provide agents with installable, verifiable, composable skills:

- what user intents should trigger the capability;
- what should not be handled;
- what minimum questions to ask;
- what default model or mode to choose;
- how to call the CLI;
- how to wait for long-running jobs;
- how to pass a `reference_id` from one step to the next;
- how to deliver final URLs;
- how to avoid leaking internal details into the user experience.

The value of this repository is that it writes those details into a machine-readable, human-reviewable, CI-validated skill package.

The builder lesson is simple:

**Do not only turn your AI capability into an API. Turn it into a workflow that agents can understand and execute. The next generation of users will not just click buttons — they will ask agents to complete the entire creative production chain for them.**
