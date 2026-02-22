---
name: seedance-prompt
description: Write high-quality Seedance 2.0 video generation prompts. Use when creating AI video prompts, writing Seedance/JiMeng prompts, or generating video scripts for text-to-video.
---

# Seedance 2.0 Prompt Writing Skill

You are an expert Seedance 2.0 prompt engineer. Write prompts that produce cinema-grade AI videos.

## Core Principle

**Seedance has no cameraman.** Your text IS the entire production crew. Every visual detail must be explicitly written — nothing is implied.

## The Golden Formula

```
[Style tags] + [Camera] + [Actor in Scene] + [2-4 Actions] + [Lighting/Atmosphere]
```

**Sweet spot: 200-500 characters (~50-80 words) per shot.**

## Three Iron Rules

1. **Abstract words = blurry frames** — Never write "he's powerful". Write "rocks crack beneath his feet, debris floats around him"
2. **Laundry-list narration = flat pacing** — Never write "they fought, he won". Use emotional arc: tension → burst → release
3. **Ignore environment = no atmosphere** — Always include lighting, weather, or environmental reactions

## Shot Structure (3x3 for 15s videos)

For 15-second videos, use 3 shots × 5 seconds each:

```
[00:00-00:05] Shot 1: Establish — environment + character entry + tension build
[00:05-00:10] Shot 2: Burst — core action + peak emotion + visual climax
[00:10-00:15] Shot 3: Resolve — aftermath + environmental change + emotional landing
```

**Per-shot word budget (~60 words total):**
- Action/events: ~30 words (50%)
- Scene/environment: ~12 words (20%)
- Camera direction: ~8 words (13%)
- Character description: ~6 words (10%)
- Style tags: ~4 words (7%)

## @ Reference System

Use `@Image1`, `@Video1`, `@Audio1` to reference uploaded assets:

| Reference | Controls | Use For |
|-----------|----------|---------|
| @Image | **Appearance** — face, costume, scene, product | Character consistency across shots |
| @Video | **Motion** — camera movement, choreography, VFX | Replicating specific movements |
| @Audio | **Sound** — voice tone, music beat, rhythm | Beat-sync and mood |

**Always specify the PURPOSE:**
- ✅ `@Image1 for the character's facial features, @Video1 for the walking pace`
- ❌ `Use @Image1 and @Video1 to make a video`

## Character Consistency

For multi-shot projects with the same character:
1. Use ONE clear, well-lit, front-facing reference photo
2. Include it in EVERY prompt with: `"Maintain exact appearance from @Image1"`
3. For multiple angles: prepare front + side + 3/4 view reference pack

## Visual Translation Cheat Sheet

| Don't write | Write instead |
|-------------|---------------|
| He's nervous | Pupils constrict, bloodshot eyes |
| Very powerful | Rocks crack underfoot, debris levitates |
| She's sad | Tears pool at the lashes, eyelids tremble |
| Fast movement | Motion blur streaks, afterimage trails |
| Beautiful scenery | Golden hour light cuts through mist, long shadows on wet stone |

## Prompt Categories & Templates

### Cinematic Film (most common, 27%)
```
[Style]: Hollywood cinematic, [genre], [lighting], [resolution]
[Duration]: 15s
[00:00-00:05] [Camera type]. [Scene]. [Character action]. [Physical detail].
[00:05-00:10] [Camera change]. [Escalation]. [Peak moment].
[00:10-00:15] [Resolution]. [Environmental aftermath]. [Emotional beat].
```

### Fantasy/Sci-Fi (24%)
```
[Style]: [Subgenre] aesthetic, cinematic particle CG, fluid light effects
[Scene]: [Supernatural environment description]
[Action]: [Transformation/power sequence with physical details]
[VFX]: [Specific particle, energy, or material effects]
```

### Short Drama (8%)
```
[Style]: [Drama subgenre], [screen orientation], [filter]
[Characters]: [Brief role descriptions]
[Shot 1]: [Setup — establish situation]
[Dialogue cue]: "[Character line]"
[Shot 2]: [Twist/reversal]
[Shot 3]: [Reveal/payoff]
```

## Technical Constraints

- **Duration**: 4-15 seconds (sweet spot: 10-15s)
- **Max files**: 12 total (images + videos + audio)
- **Image input**: up to 9 images, max 30MB each
- **Video input**: up to 3 clips, total ≤15s, max 50MB
- **Audio input**: up to 3 MP3 files, total ≤15s
- **Resolution**: up to 1080p
- **Realistic faces**: Platform may restrict real human face uploads

## Common Pitfalls

1. **Overloaded prompts** — Over 600 chars and the AI gets confused about priorities
2. **Contradicting instructions** — "fast action scene with slow contemplative camera" conflicts
3. **Vague references** — Always specify WHAT aspect of each @reference to use
4. **Stacking adjectives** — "stunning, breathtaking, magnificent" wastes tokens. Use one specific physical detail instead

## Additional Resources

- For 102 real prompt examples, see [ALL_PROMPTS.md](../ALL_PROMPTS.md)
- For category breakdown, see [CATEGORIES.md](../CATEGORIES.md)
- For structural analysis, see [ANALYSIS.md](../ANALYSIS.md)
