# Humanizer-zh: When AI Learns to Erase Its Own Fingerprints

> A 3,500-star Claude Code skill that removes AI writing traces from Chinese text. Not to fool detectors — but to make words feel human again.

## Project Overview

| Metric | Data |
|--------|------|
| **GitHub** | [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) |
| **Stars** | 3,535 ⭐ |
| **Forks** | 318 |
| **Created** | January 19, 2026 |
| **License** | MIT |
| **Author** | 歸藏 / Guizang (op7418) |
| **Upstream** | [blader/humanizer](https://github.com/blader/humanizer) |

---

## The Problem: AI Text Has a Smell

You've read text like this:

> Nestled in the picturesque heart of Hangzhou, this café boasts a rich cultural heritage and breathtaking décor. Serving as a focal point of the city's coffee culture, it provides a seamless, intuitive, and vibrant experience for patrons.

Nothing factually wrong. But something feels off — every adjective is precisely inflated, every structure symmetrically polished. It reads like it came off an assembly line. That's what people call "AI smell."

Since 2024, with hundreds of millions using ChatGPT, Claude, and other LLMs, AI-generated text has flooded the internet. Wikipedia's WikiProject AI Cleanup found that articles were being quietly replaced with AI content sharing eerily consistent patterns — inflated significance, vague attributions, tricolon structures, and a vocabulary stuffed with "furthermore," "crucial," and "evolving landscape."

**Humanizer-zh** was built to fight exactly this problem — in Chinese.

## What Is It?

Humanizer-zh is a Claude Code Skill created by Chinese developer Guizang (GitHub: op7418), localized from the English project [blader/humanizer](https://github.com/blader/humanizer). At its core is a comprehensive SKILL.md file that defines rules for identifying and fixing 24 distinct AI writing patterns.

In practice: you feed it AI-generated Chinese text, and it works like an experienced editor — identifying "AI smell" sentence by sentence, then rewriting into more natural human expression.

### One-line install:

```bash
npx skills add https://github.com/op7418/Humanizer-zh.git
```

Or manually clone to `~/.claude/skills/humanizer-zh/`, restart Claude Code, and invoke with `/humanizer-zh`.

## The 24 Patterns of AI Writing

The SKILL.md catalogs AI writing fingerprints in four categories:

### I. Content Patterns (What AI Says)

1. **Significance inflation** — "marking a pivotal moment in the evolution of..."
2. **Notability name-dropping** — stacking media names without context
3. **Superficial -ing analyses** — "symbolizing... reflecting... showcasing..."
4. **Promotional language** — "nestled within," "breathtaking," "vibrant"
5. **Vague attributions** — "experts believe," "industry reports suggest" (which experts? which reports?)
6. **Formulaic "challenges and outlook"** — the universal template ending

### II. Language Patterns (How AI Says It)

7. **AI vocabulary** — "furthermore," "crucial," "delve into," "landscape," "tapestry"
8. **Copula avoidance** — replacing "is" with "serves as," "stands as," "marks"
9. **Negative parallelisms** — "it's not just X, it's Y"
10. **Rule of three overuse** — forcing ideas into triads
11. **Synonym cycling** — protagonist → main character → central figure → hero
12. **False ranges** — "from the Big Bang to dark matter's mysterious dance"

### III. Style Patterns (What AI Looks Like)

13. **Em dash overuse** — mimicking "punchy" sales copy
14. **Boldface overuse** — mechanically bolding key terms
15. **Inline-header lists** — every bullet starts with **Bold Title:**
16. **Title Case headings** — less relevant in Chinese
17. **Emoji decoration** — 🚀💡✅
18. **Curly quotes** — ChatGPT's typographic signature

### IV. Conversational Artifacts (Who's Talking)

19. **Chatbot phrases** — "I hope this helps!"
20. **Cutoff disclaimers** — "As of my last training update..."
21. **Sycophantic tone** — "Great question! You're absolutely right!"
22. **Filler phrases** — "In order to achieve this" → "To"
23. **Excessive hedging** — "could potentially possibly be considered..."
24. **Generic positive conclusions** — "The future looks bright"

## Beyond Removal: Injecting Soul

The most valuable part of Humanizer-zh isn't the 24 rules — it's its philosophy about what good writing actually is.

From the SKILL.md:

> Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as machine-generated content. Good writing has a real person behind it.

Six principles for injecting soul:

- **Have opinions** — Don't just report facts; react to them
- **Vary rhythm** — Mix long and short sentences
- **Acknowledge complexity** — Real people have complicated feelings
- **Use "I" when appropriate** — First person is honesty, not unprofessionalism
- **Allow some mess** — Perfect structure feels algorithmic
- **Be specific about feelings** — Replace abstractions with details

This isn't a "fool the detector" tool. It's a writing guide. It teaches not how to disguise, but how to write with genuine human voice.

## The Chinese Language Challenge

Localizing the English Humanizer for Chinese wasn't a straight translation. Guizang noted several key adaptations:

1. **Some English patterns manifest differently in Chinese** — e.g., Title Case (pattern 16) doesn't apply
2. **Chinese-specific examples** — All before/after demonstrations use Chinese text
3. **Expressions adjusted for Chinese conventions** — AI Chinese has its own distinctive quirks

Chinese AI text has unique characteristic problems:

- **Four-character idiom stacking** — AI loves inserting chengyu to appear "cultured"
- **Excessive "的" (possessive/attributive particle)** — Long chains of modifiers
- **Translation-ese** — AI Chinese often carries English thought patterns underneath
- **Empty parallel constructions** — "不仅……而且……更……" (not only... but also... furthermore...)
- **Formulaic transitions** — "然而" (however), "尽管如此" (despite this), "值得注意的是" (it's worth noting)

These are patterns that Chinese AI detection specifically needs to watch for, and Humanizer-zh addresses them with native Chinese sensibility.

## The Author: Guizang's AI Toolkit Empire

Humanizer-zh's creator Guizang (op7418) is a prolific builder in the Chinese AI community. His GitHub profile reveals a suite of high-quality projects:

- **guizang-s-prompt** (999 ⭐) — AI prompt library
- **NanoBanana-PPT-Skills** (1,500 ⭐) — AI-powered PPT generation
- **CodePilot** (2,600 ⭐) — Desktop GUI for Claude Code (Electron + Next.js)
- **ai-claude-start** (212 ⭐) — Multi-profile Claude Code launcher
- **Humanizer-zh** (3,535 ⭐) — The subject of this article

He's also active on X (Twitter), frequently sharing AI tools and insights. Humanizer-zh's rapid adoption after release signals that the Chinese-speaking community has a strong appetite for "de-AI-ification" tools.

## The Bigger Picture: Ethics of AI Text Humanization

Humanizer-zh touches on an increasingly important question: as AI-generated text becomes ubiquitous, how do we respond?

### The Arms Race: Detection vs. Anti-Detection

In 2025-2026, an arms race is playing out between AI text detectors (GPTZero, Turnitin's AI detection, etc.) and AI text "humanizer" tools. Every time detectors get more precise, new tools learn to circumvent them.

But Humanizer-zh occupies an interesting position — it explicitly disclaims the adversarial framing:

> Tip: This tool isn't designed to "fool" AI detectors, but to genuinely improve writing quality. The best "de-AI" method is to give text real human thought and voice.

### Quality Improvement vs. Identity Deception

There's a subtle but important distinction:

- **Improving writing quality** — Making AI-assisted text better, more natural, more informative
- **Disguising AI as human** — Making people think AI content was human-written

Humanizer-zh is a technical tool that doesn't presume user intent. But its existence raises the question: in a world where AI writing is the norm, what does "authenticity" even mean?

### Practical Use Cases

- **Content editing** — Polishing AI-drafted first drafts for publication
- **Academic writing** — Ensuring papers aren't falsely flagged as AI-generated
- **Brand communications** — Making marketing copy less "template-y"
- **Writing education** — Using the 24 rules as a teaching framework for recognizing and avoiding AI patterns

## Technical Elegance: The Skill Architecture

From a technical perspective, Humanizer-zh's implementation is clever — it's not standalone software but a Claude Code Skill.

This means:

1. **Zero code** — The entire project is one SKILL.md file and a README.md
2. **Plug and play** — Install to Claude Code's skills directory and go
3. **Leverages LLM capability** — Uses AI to fix AI; uses Claude's comprehension to execute the rules
4. **Extensible** — Anyone can fork and add their own rules

This "behavior defined by prompt" Skill architecture represents an increasingly popular way to distribute AI tools — no code to write, no servers to deploy, just a carefully crafted instruction document. It's the emergence of "prompt as software."

## Community Reception

3,535 stars and 318 forks for a project only 6 weeks old is exceptional. This tells us several things:

1. **The "AI smell" problem in Chinese is widely recognized** — People are genuinely bothered by AI text
2. **The Claude Code ecosystem is growing fast** — Skills are becoming a new content distribution medium
3. **"De-AI-ification" is a real need** — Whether motivated by quality or detection avoidance

Discussions on Threads and X confirm the sentiment. Users frustrated by "AI-style text taking over social media" recommend Humanizer-zh as a solution.

## Conclusion

Humanizer-zh isn't a large or complex technical project. Its core is a single 8,000+ character Markdown file listing 24 AI writing patterns and their fixes.

But its value lies in systematizing years of Wikipedia community observations about AI writing, then presenting them in a format Chinese developers can use directly. It reminds us that in an era of AI content saturation, "writing like a human" has itself become a skill that requires deliberate practice.

The best way to de-AI your writing? Not a tool to erase traces, but actually thinking, feeling, and then writing those thoughts down — imperfections and all.

---

*Published March 2, 2026. Project data as of writing.*

*Source: [GitHub - op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)*
