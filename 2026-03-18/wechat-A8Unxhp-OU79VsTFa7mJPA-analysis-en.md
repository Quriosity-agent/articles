# LibTV: The First AI Video Product Designed for Both Humans and Agents

> Source: [数字生命卡兹克 (WeChat)](https://mp.weixin.qq.com/s/A8Unxhp-OU79VsTFa7mJPA)
> Analysis date: 2026-03-18

![LibTV Cover](https://mmbiz.qpic.cn/sz_mmbiz_jpg/2jjfQoZLoqVrsZiaBKrBbQpeGgNnXzgibAoBmxHTKf3yJh2iaekdsDpoDkia1LME9Ro3SIfLNEkWibtqL3Z5lfbqreWp9oyzJxsiajbavDNIF9iaEs/0?wx_fmt=jpeg)
*Image source: LibTV / 数字生命卡兹克*

## TL;DR

- **LibTV is the first AI video creation product designed for both humans and AI agents** — https://www.liblib.tv/
- Humans get an **infinite canvas** (node-based editor); Agents get **Skills** (one-sentence invocation of backend capabilities)
- Core design principle: **unified atomic capabilities, two entry points serving two types of users** — possibly the definitive product design pattern for the Agent era

---

## 1. What Is LibTV?

LibTV is an AI video creation platform from liblib.art. Its unique selling point isn't "yet another AI video tool" — it's the **dual-entry architecture**:

1. **For professional users**: A node-based infinite canvas supporting the full pipeline from script → images → video → audio
2. **For casual users / Agents**: Skills-based invocation where one sentence triggers the backend Agent to handle storyboarding, model selection, and parameter tuning automatically

Both entry points share the same underlying atomic capabilities.

## 2. For Humans: The Infinite Canvas

### Image Processing (Described as "Insane-Level")

- **Basics**: Upscaling, outpainting, inpainting, erasing, matting
- **Multi-angle generation**: Preset viewpoints — drop in one image, get any angle with a 3D preview
- **Lighting control**: One-click lighting adjustments (angle, brightness, rim light), extremely stable results
- **Prompt extraction**: Reverse-engineer text prompts from any image
- **Image-to-image / Image-to-video**: Seamless downstream task chaining

### Camera Controls

The standout feature — a **real camera parameter UI**:

- Physical camera body selection (e.g., Canon K-35)
- Physical lens parameters
- Aperture and focal length controls
- Style presets, aspect ratios, resolution, model selection

### Video Generation

- Supports "almost all" video models (missing Seedance 2.0 — no public API yet)
- Post-generation: editing, super-resolution
- **Analysis mode**: Frame-by-frame breakdown of generated videos

### Script & Storyboarding

- Script node: input a script → auto-generate storyboard
- Character setup + description → storyboard generation
- Particularly useful for AI short dramas and AI manga

### Other Features

- Audio nodes: voice-driven digital humans, music generation
- Slash commands (`/`) for hidden features and presets
- Credits and membership synced with liblib — zero-cost migration

## 3. For Agents: The Skills Architecture

**This is the section builders should pay the most attention to.**

### Installation

```
Install this skill: https://github.com/libtv-labs/libtv-skills
```

Works with Claude Code, Codex, OpenClaw, and other mainstream Agent platforms. Set up your Access Key and you're ready to go.

### Architecture (The Key Insight)

LibTV's Skills use a **strategically smart architecture**:

```
User Prompt → Agent (Claude Code, etc.) → LibTV Skills (trigger + communication) → LibTV Backend Agent → Model calls → Return results
```

**Critical design decision: The user-facing Skills only handle triggering and communication. All real capabilities run on the backend Agent.**

This means:
- The backend can continuously iterate on prompts, model strategies, and storyboard logic — invisible to the outside
- Core know-how isn't leaked through open-source Skills
- What's published externally is the **interface, not the brain**

### Why This Architecture Matters

> Agent ecosystems need openness, but openness ≠ giving away your core competitive advantage.

Many Skills developers put all their logic directly in SKILL.md or scripts — essentially running naked. LibTV's approach:

- **Open layer**: Lightweight Skills for triggering and communication only
- **Protected layer**: Core model calls, storyboard generation, parameter optimization — all on the backend
- **Commercial viability**: Barriers create protection; protection creates business potential

### Usage Examples

**Image generation:**
```
Generate images: black and white, blurry opera ballet dancers, shot with Canon K-35,
Jeanloup Sieff style, 16:9, 2K, generate 4 images.
```

Agent auto-invokes LibTV Skills → backend processing → ~30 seconds → 4 images returned + auto-downloaded locally + canvas project link.

**Video generation:**
Select a generated image, tell the Agent "make a 10-second video from this" → ~2 minutes to completion.

**Advanced workflows:**
- One sentence to replicate a viral video → generate a TVC ad
- One sentence to create a music video (e.g., "Make an MV for Ryuichi Sakamoto's *Rain*")

### Canvas Integration

Every Agent task **automatically creates a canvas project** with nodes pre-connected. You can:
- Continue manual refinement on the canvas
- Link with existing real projects

This creates the complete workflow: **Agent produces a 70% draft → Human refines to 100% on the canvas**.

## 4. Core Builder Takeaways

### 1. Product Design: The Dual-Entry Model

Same product, same underlying capabilities, two fundamentally different entry points serving two types of users:

- **Professional users** → Infinite canvas (complexity = power)
- **Casual users** → Agent Skills (speak and it happens)

This isn't the old "lite vs. pro" playbook. It's a **fundamentally different interaction paradigm split**.

### 2. Skills Architecture: Interface, Not Brain

For Skills developers:
- User-facing Skills should only trigger and communicate — stay lightweight
- Core logic belongs on the backend — protect your know-how
- This is how you create iteration space and commercial potential

### 3. Agent + Human Collaboration Model

> Agent creates the first draft; humans refine it — this is probably the most common creative workflow of the future.

LibTV turns this into a product loop: Agent generates → auto-creates canvas project → human refines on canvas.

### 4. What's Missing

- No Seedance 2.0 support (API not publicly available)
- Agent experience is still early-stage; entry point isn't prominent enough
- User-facing Skills expose relatively few features

## 5. Conclusion

LibTV might be the first AI video tool that has genuinely figured out "how should products be designed in the Agent era."

Core thesis: **Atomic capability layer + dual entry points (human canvas / Agent Skills) = the product form factor for the Agent era**.

For builders, the most valuable takeaway isn't the feature list — it's the architectural thinking:
- Can your product serve both humans and Agents simultaneously?
- Are your Skills "giving away the brain" or "exposing an interface"?
- Does your Agent collaboration form a complete loop?

LibTV offers a solid reference answer to these questions.

🦞
