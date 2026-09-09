---
title: "Cinematique Deep Dive: A 150-Technique Film-Grammar Compiler for AI Prompts"
date: 2026-07-16
source: "https://vvsvs.pro/cinematique"
canonical: "https://vvsvs.pro/cinematique"
author: "Ivan Flugelman / VVSVS"
tags:
  - Cinematique
  - VVSVS
  - AI Video
  - AI Image
  - Cinematography
  - Prompt Engineering
  - Film Grammar
  - Creative Workflow
---

# Cinematique Deep Dive: A 150-Technique Film-Grammar Compiler for AI Prompts

> **TL;DR:** [Cinematique](https://vvsvs.pro/cinematique) is neither a film-still search engine nor a video model. It is a free translation layer for cinematic language. The site organizes 150 film and photography techniques, including aerial shots, dollies, deep focus, dissolves, and mise-en-scène, into searchable prompts for generative image and video tools. A deep-dive page adds when to use the technique, how to describe its physical mechanism, and the mistakes that make it collapse. The library addresses a real bottleneck: creators often lack the vocabulary to express a shot, not another magic prompt. Templates still cannot guarantee camera physics, sequence continuity, or final quality. The site also calls itself open source, but its public pages currently link to neither a code repository nor a license.

- **Website:** [Cinematique](https://vvsvs.pro/cinematique)
- **Author:** Ivan Flugelman / VVSVS; the page says it is based on Tetsuo Corp's [grokfilm.app](https://grokfilm.app/) and expanded by VVSVS
- **Page version:** `v0.1.0`
- **Last updated:** July 16, 2026, according to the official sitemap; sampled technique pages also say Reviewed 16 July 2026
- **Pricing:** The web library is free. VVSVS separately sells a $29, 387-page offline ebook with 41 reference clips and eight book-exclusive Scene Recipes

![Cinematique's category, search, difficulty, and mood controls](imgs/vvsvs-cinematique-film-grammar-prompt-library/01-cinematique-browser.png)

## 1. The missing layer between film language and model language

Image and video models can readily produce something that looks cinematic. The word itself is a weak instruction. A user types `cinematic`, `epic`, or `dynamic`; the model may return an attractive frame without understanding how the camera should move, where attention belongs, how spatial relationships change, or why the choice serves the story.

Cinematique starts from a more precise sequence. It maps a creative intention to an established film technique, then expands that technique into visible conditions a model can attempt. Its Dolly Shot guidance specifies travel direction, speed, subject lock, and parallax across foreground, middle ground, and background. Its Handheld Shot entry distinguishes breathing drift, impact from sudden movement, motion blur, and the operator recovering the subject.

The site's strongest line captures the product idea: **"Direct the shot. Not the adjective."** Models cannot reliably execute abstract taste. They can at least attempt positions, directions, durations, depth relationships, light sources, and compositional constraints.

## 2. The 150 techniques form a taxonomy, not a prompt feed

The current interface counts exactly 150 entries across seven categories:

| Category | Count | Primary job |
|---|---:|---|
| Camera Work | 41 | Shot size, camera position, movement, and subject relationship |
| Lighting | 30 | Source direction, hardness, color temperature, time, and atmosphere |
| Composition | 21 | Attention, depth, balance, and frame structure |
| Editing | 17 | Transitions, time compression, parallel action, and rhythm |
| Storytelling | 12 | Point of view, information release, and dramatic organization |
| Visual Effects & Promptable FX | 8 | Visual transformations that generators can be asked to render |
| Genres & Styles | 21 | Genre conventions, media texture, and style direction |

Users can filter by Basic, Intermediate, or Advanced difficulty and by eight moods: Cinematic, Dramatic, Artistic, Horror, Action, Romantic, Documentary, and Nostalgic. Search appears to match names and descriptive text. Entering `dolly` returned Dolly Shot, Head-On Shot, Steadicam, and Vertigo Effect because all four descriptions involve a dolly mechanism.

This information architecture behaves like a compact knowledge base rather than a feed ranked by popularity. A creator can enter through "I need unease" or through "I need visible parallax," then arrive at a technique that can be copied and adapted.

## 3. The durable asset is the decision structure

Sampling Dolly Shot, Handheld Shot, Leading Lines, Dissolve, and One-er reveals a consistent content model:

1. **Definition and film references:** The page explains the technique and places it among specific filmmakers and films.
2. **Prompt template:** An English template includes a replaceable `[Subject]` placeholder.
3. **When to use:** The entry connects the technique to a dramatic purpose and identifies cases where another choice is better.
4. **Directing the AI:** The term is expanded into path, speed, composition, lighting, or continuity requirements.
5. **Common mistakes:** Three failure patterns help users remove conflicting directions.
6. **Fundamental and related techniques:** Each decision reconnects to broader ideas such as composition, editing, or pacing and to adjacent terms.
7. **Reference desk:** Links to sources such as StudioBinder and the BFI provide further technical and historical context.

Most prompt galleries save only the final string, leaving users unable to tell which words matter. Cinematique stores why a technique fits and how it fails. That makes the content more portable across model generations. A template can age quickly; camera mechanics, selection criteria, and failure modes are more durable.

## 4. Dolly Shot exposes five layers of a useful prompt

![Dolly Shot example: the usable signal comes from spatial layers around a centered subject](imgs/vvsvs-cinematique-film-grammar-prompt-library/02-dolly-shot.png)

The Dolly Shot page is primarily about spatial relationships, not the camera brand in its template. Its guidance breaks into five layers:

| Layer | Question | Function in a dolly shot |
|---|---|---|
| Dramatic intent | Why should the camera move? | Approach a threat or discovery, or pull away into isolation |
| Physical mechanism | How does it move? | Translate the camera through space instead of digitally enlarging the frame |
| Subject relationship | What remains stable? | Lock the subject's position and apparent size as intended |
| Spatial evidence | How will motion become visible? | Create parallax using readable foreground, middle-ground subject, and background |
| Visual finish | What completes the image? | Add lens behavior, lighting, color, and medium texture |

The same analysis works elsewhere. Leading Lines requires lines to terminate at a meaningful focal destination. Dissolve depends on two shots whose shape, luminance, or meaning can interact during the overlap. One-er needs a continuous route through doors, turns, actor crossings, focus changes, and lighting transitions.

![Leading Lines example: architecture and tracks direct attention toward the subject](imgs/vvsvs-cinematique-film-grammar-prompt-library/03-leading-lines.jpg)

## 5. Reusing one character creates a visual unit test

Cinematique says its reference images and videos were generated with xAI's Grok Imagine. Many visible examples reuse a white-haired character and a related industrial science-fiction environment. That limits visual variety, but it gives the library an unexpected teaching advantage. When subject and world remain roughly stable, changes caused by close-up, dolly, leading lines, or aerial framing become easier to inspect.

The examples function like visual unit tests for film terms: hold the world mostly constant, change one cinematography decision, and compare the output. That communicates a technique more clearly than a gallery in which every example changes subject, genre, palette, and rendering style at once.

![Close-Up example: the same character is reorganized around facial performance and shallow depth of field](imgs/vvsvs-cinematique-film-grammar-prompt-library/04-close-up.png)

This is not evidence that each template performs equally across every model, subject, or genre. The site calls the text technology-agnostic, meaning it does not depend on a proprietary parameter syntax. Its visual demonstrations still come mainly from Grok Imagine. Midjourney, Runway, Sora, and other systems may interpret focal length, camera position, and editing language differently.

## 6. A more reliable way to use the library

Cinematique works best between visual development and prompt writing, rather than as a copy-and-generate button.

### Step 1: State the dramatic job

Write one sentence describing what the audience should feel or learn. For example: "The character realizes someone is waiting at the far end of the corridor, and the threat should grow gradually." Choose a technique only after the job is clear.

### Step 2: Compare a few candidate techniques

Consider a dolly-in, slow zoom, handheld move, or rack focus. Give each shot one dominant decision instead of stacking every appealing technique.

### Step 3: Read the deep dive, not only the card

Focus on When to use, Directing the AI, and Common mistakes. These sections identify the spatial evidence that is missing and the instructions that conflict.

### Step 4: Rewrite the template as a project specification

A stronger structure is:

```text
[dramatic job] + [dominant technique] + [camera path and speed]
+ [subject action and frame position] + [depth or lighting evidence]
+ [character, prop, and screen-direction continuity] + [forbidden changes]
```

Remove camera, film-stock, or color terms that do not belong to the project. Equipment names in the template are style signals; the generation model is not operating that physical camera.

### Step 5: Test whether the mechanism appears

Change one variable at a time and compare at least three to five outputs. A dolly should show parallax rather than simple magnification. Handheld motion should correspond to operator and subject movement. Leading lines should actually terminate at the intended subject.

### Step 6: Promote accepted output into a shot spec

Record the prompt, model version, seed, references, duration, aspect ratio, start and end frames, and acceptance criteria. Cinematique supplies vocabulary; a project's shot list must preserve continuity and reproducibility.

## 7. Film-reference databases solve another problem

This repository previously covered [ShotDeck, Shot.Cafe, Flim, Film Vibes, and Frame Set](../2026-07-08/2026-07-08-cinematic-reference-stack-ai-video-preproduction-en.md), as well as [FrameThrower](../2026-07-08/2026-07-08-framethrower-cinematography-search-engine-en.md). Cinematique should sit beside those tools, not replace them:

| Layer | Input | Output | Best stage |
|---|---|---|---|
| ShotDeck / FilmGrab-style film libraries | Film, filmmaker, color, composition, or scene | Stills from finished films | Studying mature work and forming taste references |
| FrameThrower / Flim-style retrieval | Natural language, tags, or similar images | A filterable reference set | Expanding a moodboard and visual direction |
| Cinematique | Technique, difficulty, mood, or keyword | Definition, prompt, usage, and failure modes | Translating visual intent into model instructions |
| Generation model | Prompt, reference image, video, or controls | New images and clips | Production and iteration |
| Shot-list / continuity system | Approved shots and project state | Reproducible shot specifications | Sequence organization, delivery, and review |

A fuller workflow starts with real films to establish taste and composition, uses Cinematique to name the mechanism, translates that mechanism into a generation prompt, and stores accepted output in a shot list. Film stills alone do not tell a model what to execute. Prompt templates alone deprive the creator of a mature visual benchmark.

## 8. The free library is also a coherent product funnel

The free tier removes most friction: visitors can browse, filter, and copy without an account, and the FAQ permits commercial use of the templates. The site then routes deeper needs into three paid layers. The $29 ebook provides offline ownership and sequential reading. The World Building Codex expands from isolated techniques to world coherence. The $250 Academy teaches an end-to-end trailer workflow.

The packaging follows the content model. The website answers how to shoot one decision. The ebook sells a complete owned reference. The course sells the path from isolated shots to a finished sequence. It is a useful split for creative-tool businesses because basic vocabulary remains open and searchable.

The open-source label needs qualification. The page header and FAQ use that phrase and credit grokfilm.app as the basis for VVSVS's expansion. As of this review, however, the Cinematique page, site navigation, and search results expose no code repository or software license. The evidence supports free web access and commercial reuse of prompt templates. It does not establish a source-code license, redistribution terms, or a contribution process.

## 9. What the current version still lacks

Cinematique is already a useful terminology layer, but it is not yet a complete AI directing workspace:

1. **No project state.** It does not track characters, environments, props, screen direction, or dependencies between shots.
2. **No model adaptation.** One template is not automatically rewritten around the capabilities of Midjourney, Runway, Sora, or another engine.
3. **No output evaluation.** Examples are shown, but there is no cross-model success rate or reproducible prompt benchmark.
4. **No sequence assembly.** Editing and Storytelling are knowledge entries, not an executable timeline or storyboard.
5. **No prompt provenance.** Once a user copies and changes a template, the site does not retain model, seed, version, or output history.
6. **Film-history claims still need checking.** Individual pages provide further reading, but this is a creative guide rather than an academic film-history database.

Filling those gaps could turn Cinematique from a prompt library into a shot compiler: accept a dramatic objective and a project bible, produce a model-specific shot specification, then test the result for parallax, shot size, motion direction, and continuity. The present version has already made the essential first move: force the user to specify what is being directed.

## Conclusion

Cinematique's value is not the availability of 150 long strings. It restores film craft as a set of selectable, explainable, testable decisions. The user must move from a weak adjective such as `cinematic` to concrete questions: how does the camera move, which spatial relationship changes, where does attention land, and what dramatic purpose does the choice serve?

For a newcomer to AI video, it is a free entry point into film vocabulary. For an experienced image-maker, it is a structured index for drafting prompts quickly. For tool builders, it demonstrates a promising intermediate layer: traditional creative knowledge compiled into conditions a model can attempt.

The strongest use places Cinematique after film-reference research and before generation, with a shot list and human acceptance checks handling continuity. Cinematique does not direct on the user's behalf. It makes the user's direction specific enough to execute and evaluate.

## Sources

1. [Cinematique main library](https://vvsvs.pro/cinematique)
2. [Dolly Shot guide](https://vvsvs.pro/cinematique/dolly-shot)
3. [Handheld Shot guide](https://vvsvs.pro/cinematique/handheld-shot)
4. [Leading Lines guide](https://vvsvs.pro/cinematique/leading-lines)
5. [One-er guide](https://vvsvs.pro/cinematique/one-er)
6. [VVSVS site summary](https://vvsvs.pro/llms.txt)
7. [VVSVS sitemap](https://vvsvs.pro/sitemap.xml)
