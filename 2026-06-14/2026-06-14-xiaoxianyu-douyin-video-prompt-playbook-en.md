---
title: "Xiao Xian Yu Douyin Video Prompt Playbook: The Reusable Part Is Not Magic Prompts but a Material–Style–Motion–Constraint Pipeline"
date: 2026-06-14
source: "https://docs.qq.com/doc/DVnF6YmNDZ25XaGNX"
source_title: "小咸鱼玩AI-抖音视频提示词分享"
source_type: "Tencent Docs shared prompt notes"
last_saved: "2026-06-14 17:03"
tags:
  - AI Video
  - Doubao
  - Douyin
  - Prompt Engineering
  - Short Video
  - Image-to-Video
  - Creator Workflow
---

# Xiao Xian Yu Douyin Video Prompt Playbook: The Reusable Part Is Not Magic Prompts but a Material–Style–Motion–Constraint Pipeline

This Tencent Docs page, [**小咸鱼玩AI-抖音视频提示词分享**](https://docs.qq.com/doc/DVnF6YmNDZ25XaGNX), looks like a collection of Douyin AI-video prompts: restoring old photos, turning family members into movie characters, anthropomorphizing pets, creating a game-opening interface, turning oneself into a game character, and generating a game-character ensemble clip.

The interesting part is not any single “magic prompt.” It is the creator workflow underneath: **turn source material into controllable reference images, then turn those references into short video; lock identity, composition, and style first, then specify motion, camera movement, timeline, and negative constraints.**

This kind of document is valuable because it is not a polished model-vendor demo. It is a set of production tricks from a short-video creator experimenting on real platforms. It turns AI-video generation from an abstract wish into an operational process.

## The one-sentence version

**This prompt collection shows that AI short-video generation is moving from “writing beautiful prompts” toward designing material chains, style anchors, motion storyboards, and fallback strategies.**

The prompt is only the final text interface. The result is shaped more by four upstream layers:

1. **Material anchoring**: original photos, three-view character sheets, game UI images, identity “avatars”;
2. **Style templates**: Hollywood film, Japanese dark fantasy, AAA game UI, western steampunk;
3. **Motion and camera design**: eye movement, wiping blood, drawing a gun, sitting down, 360-degree orbit, low tracking shot;
4. **Constraints and fallback**: 16:9, no face collapse, no limb distortion, no flicker, use an avatar or simplified reference if generation fails.

This is no longer single-turn prompt engineering. It is a small short-video production pipeline.

## The six template categories in the document

The source document contains six video directions:

| Episode | Theme | Main method |
|---|---|---|
| 1 | Old-photo restoration | image-to-image repair, then send the image to Doubao for video |
| 2 | Turning family into movie characters | first create a cinematic reference image using a GPT Image 2-like model |
| 3 | Anthropomorphic pets | use Doubao directly and describe the desired effect |
| 4 | Game-opening interface demo | character design → three-view sheet → UI images → one-shot video |
| 5 | Turning oneself into a game character | daily photo → selfie video → dark game-menu image → video |
| 6 | Game-character ensemble clip | write a complete 10-second CG storyboard plus negative prompts |

The later templates increasingly stop being “describe an image” and become “direct a shot.” Episodes four, five, and six explicitly use material chains, timeline design, camera language, and negative constraints.

## Template 1: old-photo restoration is identity preservation plus quality enhancement

The first prompt asks for 4K/8K restoration of old photos: remove scratches, stains, mildew, yellowing, fading, and damage while preserving facial features, hair texture, clothing, background, real skin tone, composition, perspective, and lighting.

The structure is useful:

```text
Task: 4K high-definition old-photo restoration
Repair targets: scratches, stains, mildew, yellowing, fading, damage
Identity constraints: preserve face, hair, clothing, and background 1:1
Texture target: natural skin, pores, skin color, saturation, contrast
Preserve: original composition, perspective, lighting atmosphere
Negative constraints: no over-smoothing, no distortion
```

The important words are not just “HD” or “8K.” The key is that enhancement and preservation are specified together. If the prompt only says “restore this photo,” the model may beautify, de-age, or rewrite the person. Identity and composition constraints tell it to improve the image without replacing the subject.

## Template 2: for movie characters, create the reference image before the video

The second episode first uses a GPT Image 2-like image model with the family photo as a reference, then applies a style such as “Hollywood-level makeup and lighting, blockbuster, desert cowboy, 8K details, HD.”

The strategy is more important than the wording: **fix identity and style in an image before asking for video.**

Video models struggle with two things:

- character identity drifting across time;
- abstract style words being reinterpreted frame by frame.

A strong reference image becomes a visual anchor. It is more controllable than merely writing “cinematic.”

## Template 3: anthropomorphic pets are easy to start but depend on taste feedback

The third episode is almost casual: Doubao generated the examples, and users can simply describe the effect they want.

That reveals a real state of the tooling. For pet anthropomorphism, model capability is often good enough. The harder question is direction:

- cute fairy-tale style or cool streetwear style?
- fully humanized occupation or semi-humanized animal traits?
- static portrait or short action clip?

The topic has a low barrier and fast feedback, but it also becomes homogeneous quickly. The durable advantage is not one prompt; it is a serialized character setting and a consistent visual world.

## Template 4: the game-opening interface is a full material pipeline

Episode four is the most useful. It does not ask the model to “make a game-opening video” directly. It breaks the work into steps:

1. generate a character design;
2. use the character image to create a three-view sheet;
3. use the three-view sheet to create a main-menu UI image;
4. use the same character sheet to create a weapon-display UI image;
5. create an outfit-customization UI image;
6. send the three images plus a video prompt to Doubao for a one-shot UI animation.

This is an AI-video asset chain. The value is not prompt length. Each step reduces uncertainty for the next step.

### Why the three-view sheet matters

A three-view sheet acts as a temporary character bible. It gives later UI images and video generation a stable identity, outfit, body ratio, and equipment set. Without it, each shot may produce a character that is only approximately the same person.

### Why create UI images before video?

The final video prompt mentions main menus, equipment pages, weapon-detail pages, stat bars, annotation lines, skin thumbnails, attachment slots, and component panels. If all of that is left to text alone, the video model can turn the interface into unreadable decorative lines. Static UI reference images improve consistency.

### The video prompt structure

The episode-four prompt includes:

- character identity: a cold young woman, codename NYX-A01/Raven;
- scene: pure white high-key void, minimalist AAA sci-fi action-game UI;
- UI elements: main menu, equipment page, weapon-detail page, stats, annotations;
- motion timing: 0–3s rising, 3–6s drawing the gun, 6–9s sitting down;
- physical details: coat drag, hair motion, muzzle distortion, mechanical-arm reflections;
- aspect ratio: 16:9.

This is close to a micro-storyboard rather than a normal prompt.

## Template 5: turning oneself into a game character depends on identity anchoring and fallback

Episode five first turns a daily-life photo into a selfie-style video, then creates a Japanese dark-fantasy game-menu image, and then uses that game image to generate a video.

The structure is practical:

```text
Subject anchoring: preserve face, hair, glasses, clothing
Action sequence: look up, wipe blood, tilt head, breathe, hair moves
Camera: push quickly from a tunnel wide shot, then settle on face and gun close-up
Atmosphere: abandoned concrete tunnel, blue cold light, wet fog
Rendering style: Japanese dark-fantasy game menu, volumetric light, low saturation, film grain
Constraints: no face collapse, no limb distortion, no flicker, no watermark, 16:9
```

The most interesting note is the failure fallback: if Doubao cannot generate it, use an avatar or “clone” of yourself, whiten the face, and try again.

That sounds like a creator’s field note, not an official tutorial. It shows that video generation is still unstable. Real identity, blood, guns, dark styling, and strong motion may trigger safety policies or generation failures. The creator’s solution is not to add more words; it is to change the input material so the model can accept it.

That is the practical lesson: **prompting does not solve everything; material preprocessing often works better.**

## Template 6: the character ensemble clip is a complete storyboard

The sixth episode is a full 10-second CG animation prompt. It defines the style as “western steampunk + dark mercenary squad + industrial wasteland” and divides the clip into four character entrances plus a final team pose:

- 0.0–2.4s: left-side female gunslinger with long coat, wide-brim hat, and rifle;
- 2.4–4.8s: hooded short-blade assassin with low sprinting motion and X-shaped blade light;
- 4.8–7.2s: central armored leader with mechanical arm, heavy weapon, steam, and bullet belt;
- 7.2–9.6s: tall gentleman gunman with top hat, mask, pistol, and thin sword;
- 9.6–10s: heroic triangular team composition.

The mature part is that it specifies not only what each character does, but also **how transitions happen**: bullet as occlusion transition, X-shaped blade light becoming a cape edge, metal fragments covering the frame, sword tip piercing toward the lens, smoke entering the final ensemble shot.

That matters for AI video. Many generated clips feel like slideshows because prompts describe frames but not the connective motion between them. Here, transitions are embedded into actions, giving the model a better chance to produce continuous movement.

## The reusable formula behind the document

Abstracting the six episodes gives a practical AI short-video prompt formula:

```text
1. Input material: original image / reference image / three-view sheet / UI image / avatar image
2. Subject anchoring: face, hair, clothing, body ratio, pose, identity traits
3. Style direction: film genre, game genre, era, palette, material
4. Scene environment: space, lighting, background, weather, atmosphere
5. Motion sequence: split actions by time; avoid only saying “make it move”
6. Camera direction: push, orbit, low angle, dive, close-up, tracking shot
7. Physical details: cloth, hair, smoke, shells, sparks, inertia
8. UI / text elements: if the interface matters, create static references first
9. Negative constraints: no broken faces, no distorted limbs, no flicker, no watermark, no low resolution
10. Fallback: change reference image, simplify motion, use avatar, split into steps
```

For creators, the most important pieces are #1 and #10. Input material determines the ceiling. Fallback strategy determines whether output can be produced consistently.

## Implications for QCut: prompts should become editable production graphs

From QCut’s perspective, this document suggests a product direction. Users should not have to put everything into one giant text box. They should be able to organize AI-video generation inside an editable production graph.

A better interface might include:

- **Material nodes**: upload a real photo, pet photo, character image, or three-view sheet;
- **Style nodes**: choose cinema, AAA game, dark fantasy, steampunk;
- **Image nodes**: generate character images, UI images, poster images first;
- **Storyboard nodes**: split actions into 0–3s, 3–6s, 6–9s sections;
- **Camera nodes**: push-in, orbit, dive, low tracking shot;
- **Constraint nodes**: identity preservation, no distortion, no flicker, 16:9;
- **Retry nodes**: if generation fails, simplify motion or swap reference material.

Then a prompt is no longer an unmaintainable wall of text. It becomes a reusable, tunable, reversible, and branchable production graph.

## Practical advice for creators

If you want to reuse this document, do not start by copying every prompt verbatim. A better approach is:

1. **Reuse the structure before the wording**: separate subject anchoring, scene, motion, camera, and constraints;
2. **Solve one hard problem per video**: identity, motion continuity, UI readability, or style consistency;
3. **Split longer videos into short segments**: a 10-second clip is already complex; split into three 3-second parts if needed;
4. **Image before video**: lock characters, UI, and scenes in still images before animating them;
5. **Keep failure samples**: record which terms fail and which references are more stable;
6. **Standardize negative constraints**: face, hands, limbs, flicker, watermark, aspect ratio, and clarity should be template fields.

## My take: short-video prompting is becoming directing

The most interesting thing about this Tencent Docs page is that it shows an ordinary creator naturally moving toward pipeline thinking.

In the early AI-image era, many people chased magic keywords. AI video is harder: characters must stay consistent, motion must be continuous, camera logic matters, UI must remain readable, timelines must be stable, and failures need retry paths. Prompt writing therefore becomes a hybrid of directing, storyboarding, production, and technical art.

The real lesson of this prompt collection is: **short-video generation does not scale through one magic prompt; it scales through a reusable production process.**

The creators who can turn material, style, motion, camera, constraints, and retry logic into controllable systems will produce content more consistently than those who merely collect prompts.
