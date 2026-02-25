# QuiverAI: $8.3M Seed from a16z to Reinvent Vector Design with AI

**Source: @joanrod_ai tweet + quiver.ai**

---

## TL;DR

QuiverAI, founded by Joan Rodriguez, raised an $8.3M seed round led by a16z. Their first model, Arrow-1.0, generates production-ready SVG vector graphics from text and images — logos, illustrations, typography, and animations. Public beta is live now.

---

## What Is This?

QuiverAI calls itself a "frontier AI lab for vector design." It's not another image generator — **it outputs SVG code**, not pixels.

This matters because:
- Logos scale infinitely without quality loss
- Designers can edit paths, colors, and details directly
- File sizes are tiny (great for web/mobile)
- Animations are CSS-driven, lightweight, and controllable

---

## What Arrow-1.0 Can Do

### Available Now
- **Text → SVG** — Describe what you want, get vector graphics
- **Image → SVG** — Upload PNG/JPEG/WebP, convert to editable SVG
- **Streaming** — Real-time progressive rendering

### Coming Soon
- **SVG Editing** — Modify existing SVGs with text prompts
- **SVG Animation** — Add CSS animations to any vector
- **Typography** — Custom vector letterforms and fonts

---

## API

```javascript
fetch('https://api.quiver.ai/v1/svgs/generations', {
  method: 'POST',
  headers: {
    Authorization: 'Bearer <key>',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'arrow-preview',
    stream: false,
    prompt: 'Generate an icon of a unicorn'
  })
})
```

Clean REST API with streaming support. Docs at docs.quiver.ai.

---

## Why This Matters

### 1. Fills the Critical Gap in AI Design

Midjourney, DALL-E, and Flux all produce **raster images** (pixels). Designers still need to manually retrace in Illustrator for production use. QuiverAI outputs SVG directly — **zero friction from AI generation to production**.

### 2. The a16z Signal

$8.3M seed led by a16z. Their AI portfolio (Character.ai, Mistral, ElevenLabs) suggests they see real market opportunity in vector design AI.

### 3. Designer-Friendly, Not Designer-Replacing

Key positioning: **"Built by researchers. Made for designers."** Output is editable SVG code — designers retain full control. This accelerates exploration, not replaces craft.

### 4. Developer-First

API-first design means it can be embedded anywhere — Figma plugins, CI/CD pipelines, design system automation, or custom tools.

---

## Team

- **Joan Rodriguez** (@joanrod_ai) — Founder
- **Maxim Leyzerovich** (@round) — Co-founder
- Positioned as a research-driven AI lab + product company

---

*Product: <https://quiver.ai>*
*API Docs: <https://docs.quiver.ai>*
*Article compiled from tweet and website content.*
