# Seedance 2.0 User Manual - Key Points

> Source: [ByteDance Lark Wiki](https://bytedance.larkoffice.com/wiki/A5RHwWhoBiOnjukIIw6cu5ybnXQ)
> Official Website: https://jimeng.jianying.com/
> Last Updated: Feb 10, 2026

---

## What is Seedance 2.0?

ByteDance's **JiMeng (即梦)** platform's next-gen AI video generation model. The biggest leap: it now accepts **4 input modalities** — image, video, audio, and text — making it a truly multimodal video creation tool. The core philosophy: video creation is not just "generation" but **controllable expression**.

---

## Core Highlights (What's New)

| Feature | Description |
|---------|-------------|
| **Reference Images** | Precisely reproduce composition, character details from reference photos |
| **Reference Videos** | Replicate camera language, complex motion rhythms, creative effects |
| **Video Extension** | Smooth continuation & stitching; generate continuous shots from user prompts ("keep shooting") |
| **Video Editing** | Character replacement, deletion, addition in existing videos |

---

## 1. Input Parameters

### Image Input
- **Formats**: jpeg, png, webp, bmp, tiff, gif
- **Max count**: 9 images
- **Max size**: 30 MB

### Video Input
- **Formats**: mp4, mov
- **Max count**: 3 videos, total duration **2-15 seconds**
- **Max size**: 50 MB
- **Resolution range**: 409,600 px (640x640, 480p) to 927,408 px (834x1112, 720p)
- Note: Using reference video costs more credits

### Audio Input
*(Partially behind login — inferred from TOC & capabilities)*
- Supports audio reference for rhythm/atmosphere
- Used for music beat-sync and voice tone matching

### Text Input
- Prompt-based control via text descriptions
- Supports `@image1`, `@image2`, `@video1` referencing syntax in prompts

---

## 2. Interaction / UI

### Main Interface
- Multimodal input area where you can upload images, videos, audio
- Text prompt box with **@ referencing** to tag uploaded assets

### "All-in-One Reference Mode" (全能参考模式) — How to use @
- In your prompt, use `@image1`, `@image2`, `@video1`, etc. to reference uploaded assets
- Example prompt patterns:
  - `@image1 as the opening frame, the woman in @image1 walks to the mirror, pose references @image2, emotional breakdown references @video1`
  - `@image1 as first frame, camera rotates and pushes in, character's face references @image2, expression references @image3, then transforms into a bear referencing @image4`

### Realistic Face Upload Warning
- Restrictions on uploading realistic human face materials
- Even using real faces only as motion/camera references may be blocked

---

## 3. Capabilities & Improvements

### 3.1 Core Quality Upgrades
- **More stable** — fewer artifacts and glitches
- **Smoother** — better temporal consistency
- **More realistic** — closer to real-world footage

### 3.2 Multimodal Capabilities Overview

The model supports free-form combination of inputs:
- Image(s) + Text prompt
- Video(s) + Text prompt
- Image(s) + Video(s) + Text prompt
- Image(s) + Video(s) + Audio + Text prompt

### 3.3 Specific Capability Breakthroughs

#### 3.3.1 Consistency (一致性)
- Major improvement in character/scene consistency across frames
- Characters maintain identity throughout generated video

#### 3.3.2 Camera Movement & Action Replication (运镜和动作复刻)
- High-difficulty camera movements can be precisely replicated
- Examples: focus-rotate, push-pull dance shots, car tracking shots, horror film camera work
- Controllable: user specifies camera behavior via reference video

#### 3.3.3 Creative Templates / Complex Effects (创意模版/特效复刻)
- Replicate complex visual effects from reference videos
- Fisheye lens, special transitions, stylized effects
- Template tables include: prompt, img1-3 refs, vid1-3 refs, and generated result

#### 3.3.4 Creativity & Story Completion (创意性/剧情补全)
- Model can intelligently fill in story/plot gaps
- Given partial scene info, it generates logical continuations

#### 3.3.5 Video Extension (视频延长)
- Extend existing videos smoothly
- Maintains continuity in character, scene, motion

#### 3.3.6 Voice Accuracy (音色更准/声音更真)
- More accurate voice tone reproduction
- More natural-sounding audio in generated content

#### 3.3.7 Shot Continuity / One-Take Feel (一镜到底)
- Stronger long-take coherence
- Can simulate continuous single-shot filming

#### 3.3.8 Video Editing Usability (视频编辑可用度)
- Edit existing videos with high usability
- Replace characters, add/remove elements

#### 3.3.9 Music Beat-Sync (音乐卡点)
- Can synchronize video motion/cuts to music beats
- Use audio input to drive rhythm of generated content

#### 3.3.10 Emotional Performance (情绪演绎)
- Better emotional expression in characters
- Example: character walking to mirror, reflecting, then having emotional breakdown — all driven by image + video + text prompt combo

---

## 4. Prompt Examples (from Cases)

### Example A — Emotional Breakdown Scene
> `@image1 woman walks to mirror, looking at her reflection, pose references @image2, after a moment of thought suddenly starts breaking down screaming, the grabbing-mirror-while-screaming emotion and expression fully references @video1`

### Example B — Range Hood Ad
> `@image1 as opening frame, woman elegantly cooking with no smoke, camera quickly pans right to @image2 man sweating profusely cooking with heavy smoke, camera pans left and pushes in to @image1 table showing a range hood, hood references @image4, the range hood is frantically extracting smoke`

### Example C — Character Transformation
> `@image1 as opening first frame, camera rotates and pushes in, character suddenly looks up, face references @image2, starts roaring loudly with comedic energy, expression references @image3, then body transforms into a bear referencing @image4`

---

## 5. Availability & Access

| Detail | Info |
|--------|------|
| **Platform** | JiMeng (即梦) — https://jimeng.jianying.com/ |
| **API Access** | Also available via Volcano Engine (火山引擎) experience center |
| **Pricing** | Free tier exists; membership not required to see 2.0 |
| **Rollout** | Gradual gray-scale release; not all users have access yet |
| **Queue** | Expect wait times during high demand |

---

## 6. Key Takeaways for Video Creators

1. **Think like a director**: Use images for visual style, videos for motion/camera reference, audio for rhythm, and text to tie it all together
2. **@ referencing is essential**: Master the `@image1` / `@video1` syntax to get controllable results
3. **Multi-reference = more control**: Combining multiple reference types yields the best results
4. **5-15 second sweet spot**: Generated video duration is currently 2-15 seconds
5. **Resolution cap is 720p**: Max output around 834x1112 pixels
6. **Realistic faces are restricted**: Platform limits use of real human faces in uploads
7. **Video extension works**: You can chain shots together for longer sequences
8. **Beat-sync with audio**: Upload music/audio to synchronize generated motion to beats
