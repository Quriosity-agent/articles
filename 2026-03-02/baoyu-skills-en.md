# baoyu-skills: How One Developer Is Defining the "Prompt as Software" Era

> 6,000+ stars, 700+ forks, 15 skills, from Xiaohongshu graphics to WeChat publishing in one command — baoyu-skills isn't just a Claude Code plugin collection. It's a glimpse into what software distribution looks like when prompts become programs.

## The Rise of Installable AI Skills

In early 2026, something quietly shifted in the AI coding assistant landscape. Claude Code stopped being merely a terminal that writes code and started becoming a **platform that runs skills** — downloadable capability packages that extend what the AI can do, much like VS Code extensions extend an editor.

Among the first breakout hits of this new ecosystem is **baoyu-skills**, a collection of 15 Claude Code skills focused on content creation and publishing. Created by Chinese tech influencer **Baoyu** (宝玉, aka Jim Liu, @dotey on X), the project has accumulated **6,095 stars** and **701 forks** in under two months — numbers that would be impressive for any open source project, let alone one in an entirely new software category.

## Who Is Baoyu?

Jim Liu, known online as **宝玉** (Baoyu) or **@dotey**, is based in Chicago, IL. His GitHub bio reads: *"Yesterday is history, tomorrow is a mystery, and today is a gift"* — a Kung Fu Panda quote that belies a prolific output.

In the Chinese-speaking AI community, Baoyu is one of the most influential technical communicators. He's known for:

- **High-quality translations** of cutting-edge AI papers and technical content from English to Chinese
- A widely-cited **"two-pass translation" prompt technique** (direct translation first, then idiomatic refinement)
- Deep, opinionated commentary on AI products and industry trends on X/Twitter

But baoyu-skills reveals another dimension: he's not just writing *about* AI tools — he's building production-grade workflows *with* them.

## What Is baoyu-skills?

**baoyu-skills** is a skill collection for Claude Code that automates the entire **content creation → visual asset generation → multi-platform publishing** pipeline.

In practical terms, it lets you run commands like:

```bash
# Turn an article into a series of Xiaohongshu (RedNote) infographics
/baoyu-xhs-images posts/ai-future/article.md --style notion --layout dense

# Generate a professional infographic with fishbone layout
/baoyu-infographic content.md --layout fishbone --style cyberpunk-neon

# Create a slide deck from markdown
/baoyu-slide-deck article.md --style corporate --slides 15

# Publish to X/Twitter
/baoyu-post-to-x "Thread about AI skills ecosystems"

# Publish to WeChat Official Account
/baoyu-post-to-wechat article.md
```

### Project Stats (as of March 2, 2026)

| Metric | Value |
|--------|-------|
| ⭐ Stars | 6,095 |
| 🍴 Forks | 701 |
| 📅 Created | January 13, 2026 |
| 🔄 Last Updated | March 2, 2026 |
| 💻 Language | TypeScript |
| 📦 Version | v1.42.3 |
| 🔧 Skills | 15 |

From v1.0 to v1.42 in under two months — a release cadence that speaks volumes about both the author's commitment and community demand.

## The 15 Skills: A Complete Content Pipeline

The skills are organized into three plugin packages:

### Content Skills (8 skills)

**baoyu-xhs-images** — The flagship feature. A Xiaohongshu (RedNote) infographic series generator with a **Style × Layout** two-dimensional system: 9 visual styles (cute, fresh, warm, bold, minimal, retro, pop, notion, chalkboard) × 6 information layouts (sparse, balanced, dense, list, comparison, flow). The generation workflow is notably clever: Claude Code first analyzes the content and generates a detailed **prompt markdown file** for each image, specifying style presets, layout rules, color palettes, typography guidelines, and the actual text content. These prompts are then fed to the underlying **baoyu-image-gen** skill (which defaults to the **Nano Banana Pro** model via Replicate) to produce high-quality PNG images. From image 2 onward, the system passes image 1 as a `--ref` reference to ensure visual consistency across the entire series.

**baoyu-infographic** — A professional infographic generator with **20 layout types** (fishbone, iceberg, funnel, Venn diagram, pyramid, timeline, mind map, and more) × **17 visual styles** (from craft-handmade to cyberpunk-neon, pixel-art to IKEA-manual). That's 340 unique combinations.

**baoyu-cover-image** — Article cover image generator with a novel **5-dimensional customization system**: Type × Palette × Rendering × Text × Mood. Nine color palettes × six rendering styles = 54 base combinations.

**baoyu-slide-deck** — Presentation slide generator with 16 style presets, a 4-dimensional style system (Texture × Mood × Typography × Density), and automatic outline generation.

**baoyu-comic** — Knowledge comic generator in Logicomix/Ohmsha style.

**baoyu-article-illustrator** — Smart illustration placement for articles.

**baoyu-post-to-x** — X/Twitter posting automation via Chrome CDP browser automation.

**baoyu-post-to-wechat** — WeChat Official Account publishing with Markdown-to-WeChat format conversion, theme systems, and color customization.

### AI Generation Skills (2 skills)

**baoyu-image-gen** — A unified image generation interface supporting multiple backends: Gemini, DashScope (Alibaba Cloud), OpenAI, Replicate, and Google's multimodal models. This is the foundational dependency for other content skills.

**baoyu-danger-gemini-web** — A reverse-engineered Gemini Web API wrapper that authenticates via browser cookies. The "danger" prefix is an honest acknowledgment that it depends on unofficial APIs.

### Utility Skills (5 skills)

**baoyu-url-to-markdown**, **baoyu-danger-x-to-markdown** (with high-res media download and embedded tweet rendering), **baoyu-compress-image**, **baoyu-format-markdown**, and **baoyu-markdown-to-html** (with multiple themes, custom colors, and code highlighting).

## Technical Architecture: Elegant Minimalism

Several design decisions stand out:

### Zero External Dependencies

The entire project has **no npm package dependencies**. All TypeScript scripts run directly via `npx -y bun` with no build step. Everything is self-contained — no fragile dependency chains, no `node_modules` bloat.

### Uniform Skill Structure

Every skill follows the same directory pattern:
```
skills/baoyu-xxx/
├── SKILL.md          # YAML frontmatter + documentation
├── scripts/          # TypeScript implementation
│   └── main.ts
├── references/       # Reference documents
└── prompts/          # AI generation guidelines (optional)
    └── system.md
```

The `SKILL.md` file is the soul of each skill — it's both human-readable documentation and the instruction set that Claude Code uses to understand the skill's capabilities. **The natural language description IS the program's interface definition.**

### Combinatorial Parameter Design

The project extensively uses **dimension × dimension** combinatorial systems. For infographics: 20 layouts × 17 styles = 340 combinations. For cover images: 6 types × 9 palettes × 6 renderings × 4 text modes × 3 moods. Yet users can specify as few as zero parameters — the AI auto-selects based on content analysis.

This is a masterclass in API design: **hide complexity behind intelligent defaults**.

### Prompt-Driven Image Generation

The visual content skills (xhs-images, infographic, etc.) employ a distinctive **"prompt intermediate layer"** architecture. Claude Code doesn't generate images directly — instead, it first produces structured **prompt markdown files** containing style presets, layout rules, color palettes, typography guidelines, and the actual content text. These prompt files are then passed to baoyu-image-gen (which calls AI image generation APIs — defaulting to **Nano Banana Pro** on Replicate) to produce the final PNG output. To maintain visual consistency across a series, images from the second onward are generated with the first image passed as a `--ref` reference. This two-tier "prompt → prompt → image" architecture preserves the flexibility of natural language while ensuring controllability and visual coherence across the output.

### Browser Automation for Publishing

Publishing to X and WeChat uses Chrome CDP (Chrome DevTools Protocol) — a pragmatic choice. Rather than waiting for platforms to offer APIs (or dealing with restrictive API limits), just automate the browser. The "danger" prefix on these skills is a refreshingly honest admission that they depend on reverse-engineered interfaces.

## The Broader Ecosystem: Claude Code's Plugin Marketplace

baoyu-skills didn't emerge in a vacuum. It's riding the wave of Claude Code's plugin marketplace system, launched in January 2026.

The marketplace lets developers package skills into plugins, register them via `/plugin marketplace add`, and distribute them to users who can browse, install, and auto-update — a workflow directly analogous to VS Code's extension marketplace. But with a fundamental difference: **Claude Code skills are primarily prompt engineering artifacts, not traditional code extensions.**

Other notable projects in this ecosystem include:

- **cc-skills** (terrylica) — A general marketplace with 20 plugins spanning development workflows
- **create-agent-skill** — A meta-skill that helps you build Claude Code skills
- Various vertical skills for translation, code review, documentation

What makes baoyu-skills unique in this landscape is its **target audience**: it's not a developer productivity tool — it's a **content creator productivity tool**. It solves the problem: "I wrote a great article. How do I quickly turn it into Xiaohongshu graphics, a WeChat post, presentation slides, and social media content?"

This is a massively underserved pain point.

## Prompt as Software: The Deeper Implications

The most profound aspect of baoyu-skills isn't its feature set — it's what it represents about the future of software.

Traditional software is **code-authored**: you define logic in a programming language, compile it, and expose it through API interfaces.

Skills in baoyu-skills are **naturally-language-described**: the `SKILL.md` file defines capabilities, parameters, and workflows in human language. TypeScript scripts handle only glue logic (file I/O, API calls, browser automation). The actual "business logic" is dynamically generated by the AI at runtime based on the SKILL.md description.

This is what **"Prompt as Software"** means:

1. **SKILL.md is the interface definition** (equivalent to an API spec)
2. **Natural language description is the implementation** (equivalent to source code)
3. **The AI is the runtime** (equivalent to compiler + virtual machine)
4. **The user's one-liner is a function call** (equivalent to an API request)

The revolutionary implication: **you don't need to be a programmer to create "software."** If you can clearly describe a workflow in natural language, you can create a Claude Code skill.

## Community Reception and Contributions

The growth metrics tell the story:

- **6,000+ stars in under 2 months** — viral adoption
- **701 forks** — extensive secondary development and learning
- **Active community contributions**: the CHANGELOG shows PRs from @zhao-newname, @xkcoding, @liye71023326, @justnode, and others
- **Analysis articles** appearing on Zhihu, Medium, and tech blogs
- A Zhihu column post titled "Learning the Right Way to Build Claude Code Plugins from baoyu-skills" treats it as the canonical example

The project's rapid iteration (v1.42 in 7 weeks) with community-driven features like Replicate provider support, OpenAI endpoint integration, and new infographic styles shows a healthy open-source feedback loop.

## Comparison with Related Projects

### vs. Translation optimization projects (Humanizer-zh, etc.)

Baoyu himself is famous for translation prompts, and the community has spawned numerous translation-focused projects inspired by his techniques. But baoyu-skills takes a completely different path — it's not optimizing AI text output quality, it's building the **complete pipeline from content to visual assets to distribution channels**.

### vs. General Claude Code skills

Most Claude Code skills target developer workflows (code review, documentation, project management). baoyu-skills focuses exclusively on **content creation workflows**. This differentiated positioning is key to its star count — it reaches a much larger user base than developer-only tools.

### vs. Standalone content creation tools (Canva, etc.)

Traditional content tools are GUI-first, requiring manual interaction. baoyu-skills is CLI-first, driven by natural language. You tell the AI "turn this article into Xiaohongshu graphics" and it executes. Two fundamentally different interaction paradigms.

## What's Next

At v1.42, the project is already mature, but the CHANGELOG shows no signs of slowing:

- **Diversifying image generation backends**: Gemini → DashScope → OpenAI → Replicate → Google multimodal
- **Maturing the WeChat toolchain**: Markdown conversion, theme systems, color customization
- **Accelerating community contributions**: more external developers submitting PRs

Likely future directions include:
- More platform support (Bilibili, YouTube, LinkedIn)
- AI video generation skills
- Automatic multi-language content localization
- Deeper integration with emerging AI models

## Conclusion

baoyu-skills is one of the most representative projects of the 2026 AI tooling landscape. It proves something important: **in the AI era, the most valuable skill isn't writing code — it's designing workflows.**

With 15 carefully crafted skills, Baoyu has built a complete pipeline from content creation to visual asset generation to multi-platform distribution. This isn't a programmer's flex — it's a content creator's productivity revolution.

When prompts become software, when workflows become installable skill packages, when "tell the AI what you want" replaces "manually execute every step" — we're witnessing a fundamental shift in how software is distributed and consumed.

And baoyu-skills is standing right at the frontier.

---

*Written March 2, 2026. Project: [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)*
