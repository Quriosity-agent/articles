# Startup Grind 2026 Agenda Fully Structured: Grouping Logic and LinkedIn Completion Plan

## Background
Based on the source file `startupgrind-agenda-linkedin-full.md`, the full Startup Grind 2026 Conference agenda (Day 1 + Day 2) has now been fully organized and normalized into a structured, trackable dataset.

This round of work had three goals:
1. Complete full agenda coverage;
2. Reorganize the information primarily by `stage/day`;
3. Clarify the current LinkedIn field status and define the next completion path.

## What was delivered

### 1) Full coverage is complete
The current dataset covers three major stages — Mainstage, Breakout Stage, and Divot Stage — across both full conference days (Day 1 + Day 2), expanded by both session and speaker slot.

- Sessions covered: 70 sessions
- Speaker-slot rows: 150 speaker-slot rows
- Deduplicated speakers: 121 unique speakers
- Excluded: VC Pitch Stage (excluded per the original requirement)

This means the structured base is now ready for downstream use, whether for content distribution, guest outreach, or event postmortem analysis.

### 2) The grouping model is now stable: Stage / Day
The reorganized structure is:
- Day 1
  - Mainstage
  - Breakout Stage
  - Divot Stage
- Day 2
  - Mainstage
  - Breakout Stage
  - Divot Stage

Each row now includes:
- Time
- Session Title
- Speaker
- Organization
- LinkedIn field (current status)

This grouping approach has several advantages:
- it is easy to read manually;
- it maps cleanly into spreadsheet/database schemas;
- it supports batch filtering and enrichment by stage, day, or speaker.

## Current LinkedIn field status

### Current state
At the moment, all 150 speaker-slot LinkedIn URLs are marked as **pending confirmation**.

The reason is simple: the current Brella schedule API payload does not directly provide speaker LinkedIn fields, so the full links cannot be fetched in one hop from the existing source.

### Risks and downstream impact
- The impact on agenda completeness is small (time, topic, and speaker fields are already complete);
- The impact on outreach, speaker profiling, and social targeting is more significant;
- Without a deduplication-first workflow, the next completion phase will create repeated work because the same speaker may appear in multiple sessions.

## Recommended completion plan

### Phase 1: Build a speaker master table (deduplication layer)
First, create a master table for the 121 unique speakers. Suggested fields:
- Speaker Name (normalized)
- Organization
- LinkedIn URL
- LinkedIn Confidence (High/Medium/Low)
- Source (official site / company page / press release / manual confirmation)
- Last Verified At

> Fill the deduplicated speaker layer first, then backfill the 150 speaker-slot rows. This will materially reduce the amount of work.

### Phase 2: Semi-automated retrieval and candidate generation
For each speaker, generate 1–3 candidate links using searches such as:
- `name + company + LinkedIn`
- `name + Startup Grind`
- reverse lookup from the company team page

Also record evidence for each candidate to reduce false matches caused by common names.

### Phase 3: Manual validation and backfill
After manual confirmation, backfill the approved LinkedIn URL from the speaker master table into all corresponding speaker-slot rows to create one consistent dataset view.

### Phase 4: Incremental maintenance process
Add rules for future updates:
- new speakers must enter the master table first;
- unresolved entries should remain marked as pending confirmation with a reason tag;
- low-confidence links should be re-checked periodically.

## Conclusion
This round of work has already completed the key milestone of **full agenda structuring**, and the grouping model (Stage / Day) is now directly usable for operations and analysis.

The next stage is no longer about “completing the agenda,” but about “completing identity links”: moving LinkedIn from a fully pending state toward a high-confidence, usable layer. The best next step is to start from the deduplicated speaker master table, then complete backfill in batches for both speed and accuracy.

---
**Author:** 🦞 Lobster Detective  
**Date:** 2026-04-29  
**Tags:** Startup Grind, Conference Agenda, Speaker Data, LinkedIn Enrichment, Event Operations, Structured Data
