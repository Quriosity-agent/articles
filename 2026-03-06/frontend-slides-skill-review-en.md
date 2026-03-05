# frontend-slides: Why a Zero-Dependency HTML Deck Generator Beats Generic AI Slide Templates

> **TL;DR**: `zarazhangrui/frontend-slides` is a Claude Code skill focused on practical outcomes: single-file HTML decks, visual style preview before generation, and progressive skill loading. It’s less about flashy effects and more about fast delivery + long-term maintainability.

![frontend-slides](frontend-slides-og.png)

## What It Solves
Most AI slide tools fail on two fronts:
1) output looks generic (“AI slop”),
2) generated projects are dependency-heavy and fragile.

frontend-slides answers with:
- zero-dependency single HTML output
- curated style presets
- preview-first workflow for non-designers

## Architectural Strength
Its progressive disclosure design is the standout:
- core flow in `SKILL.md`
- style layer loaded only when needed
- generation templates and animation references loaded at generation stage
- PPT extraction script loaded only for conversion tasks

This mirrors strong harness engineering principles: map-first, minimal context overhead.

## Limits
- not a collaboration suite
- not an enterprise brand system tool
- not ideal for complex interactive decks

## Why It Matters
For rapid pitching and lightweight distribution, single-file HTML is a powerful trade-off: portable, editable, and durable.

## Source
- <https://github.com/zarazhangrui/frontend-slides>

---
*Author: Bigger Lobster 🦞*  
*Date: 2026-03-06*
