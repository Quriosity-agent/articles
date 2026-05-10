# GBrain Deep Dive: A Self-Maintaining Long-Term Brain for AI Agents

> Source: https://github.com/donghaozhang/gbrain  
> Upstream: https://github.com/garrytan/gbrain  
> Written: 2026-05-09  
> Keywords: GBrain / AI Agent / Long-Term Memory / Knowledge Graph / Hybrid RAG / MCP / OpenClaw / Hermes / Skills

![GBrain GitHub repository screenshot](imgs/gbrain-agent-memory-knowledge-graph/github-repo.png)

## One-line take

GBrain is not just another “embed Markdown and search it” RAG project. It is closer to a long-term memory operating system for AI agents: PGLite or Postgres + pgvector underneath; pages, chunks, embeddings, typed links, timelines, jobs, eval capture, CLI and MCP in the middle; and a thick layer of Markdown skills on top that tells agents how to ingest, enrich, cite, maintain, and improve memory over time.

If Claude Code, OpenClaw, or Hermes are the hands that do work, GBrain is trying to be the brain that compounds. Its core premise is simple: the next advantage for personal agents will not be how clever one reply is, but whether the agent can accumulate context across months of meetings, emails, code, social feeds, ideas, and tasks — and retrieve the right part when it matters.

## What I checked

I inspected `donghaozhang/gbrain`, which is a fork of `garrytan/gbrain`. The GitHub page reports the fork as up to date with the upstream `master` branch.

| Dimension | Observation |
|---|---|
| Repository | `donghaozhang/gbrain`, forked from `garrytan/gbrain` |
| Upstream description | “Garry's Opinionated OpenClaw/Hermes Agent Brain” |
| License | MIT |
| Main language | TypeScript / Bun |
| Current package version | `0.31.2` in `package.json` |
| Upstream traction | GitHub API shows roughly 14.2k stars and 1.8k forks for `garrytan/gbrain` |
| Code scale | Local clone has about 1,020 files and 343k lines; TypeScript accounts for about 707 files / 177k lines |
| Main directories | `src/` core and CLI, `skills/` agent skills, `docs/` documentation, `test/` extensive tests, `admin/` HTTP admin UI |
| Operation surface | About 89 operation names / CLI aliases can be parsed from `src/core/operations.ts` |
| Skills | About 39 `SKILL.md` files covering ingest, query, enrich, maintain, cron, reports, soul-audit, and more |

This is not a toy repository. It looks like fast-moving personal AI infrastructure: large codebase, substantial tests, long documentation, frequent releases, and a README that explicitly says it powers real OpenClaw and Hermes deployments.

## It solves forgetfulness, not just search

Basic RAG usually answers one question: “What can I retrieve from my documents right now?” A real personal agent has a harder problem:

1. If a person appears in today’s meeting, does a person page get created automatically?
2. If a company is mentioned repeatedly, does it graduate from a stub to a real dossier?
3. Will a user preference still be available three months later?
4. Can multiple repos, teams, and sources avoid contaminating each other?
5. When an agent writes a new page, are links, backlinks, and timeline entries created automatically?
6. If retrieval quality regresses, is there an eval/replay loop to catch it?

GBrain focuses on exactly these issues. The README’s framing line is the project’s best summary:

> Your AI agent is smart but forgetful. GBrain gives it a brain.

Here, “brain” does not mean only a database. It means a loop: signal arrives, pages are written, entities and links are extracted, embeddings are generated, maintenance runs, and the next query retrieves a richer context than the last one.

## Architecture: a knowledge graph plus hybrid RAG on Postgres

Underneath, GBrain is not merely a folder search tool. It is a Postgres-native knowledge system. It can run with embedded PGLite by default, or with Postgres / Supabase + pgvector for larger deployments.

Key components include:

- `pages`: knowledge pages, similar to wiki or Obsidian notes;
- `content_chunks`: chunk-level retrieval units;
- embeddings: vector search;
- `links`: typed edges such as `attended`, `works_at`, `invested_in`, `founded`, and `advises`;
- timeline entries: structured events;
- brain/source axes: many sources can live inside one brain, and multiple brains can be mounted;
- storage tiering: local files, DB-only paths, S3/Supabase Storage patterns;
- eval capture: real `query` and `search` calls can be captured and replayed to evaluate retrieval changes.

The difference from simple vector search is that GBrain treats memory as a maintainable knowledge base, not a bag of chunks. It wants memory to be auditable, linkable, replayable, and repairable.

## Hybrid search: keyword, vector, graph, salience, and recency

`src/core/search/hybrid.ts` reveals the retrieval philosophy:

- keyword search and vector search run together;
- RRF (Reciprocal Rank Fusion) merges rankings;
- compiled-truth chunks can receive a boost;
- cosine scores are blended back into ranking;
- pages with more backlinks can rank higher;
- newer versions add salience and recency boosts;
- two-pass retrieval expands from chunks back into useful context.

This matters because the failure mode of many personal knowledge systems is not simply “I cannot find anything.” It is “I found something, but the ranking does not understand importance.”

A random web clipping from three years ago, a person repeatedly mentioned in recent meetings, and a preference stated directly by the user should not be treated as equal just because their text is semantically similar. GBrain tries to turn importance into computable signals: links, source type, time, emotional weight, takes, and compiled truth.

## Thin Harness, Fat Skills

The most interesting part of GBrain may be `skills/`, not the database.

The repository ships a large set of Markdown skills, including:

- `signal-detector`: runs on every inbound message to capture original ideas and entities;
- `brain-ops`: forces brain-first lookup before answering;
- `ingest`, `media-ingest`, `meeting-ingestion`, `voice-note-ingest`: convert different input types into structured memory;
- `enrich`: upgrades people and company pages from stubs to useful dossiers;
- `maintain`: fixes citations, backlinks, orphans, and structure;
- `reports` and `briefing`: generate recurring reports and context summaries;
- `skillify` and `skill-creator`: turn repeated workflows into durable skills.

The philosophy is Garry Tan’s “Thin Harness, Fat Skills”: keep deterministic execution in CLI / SQL / TypeScript, and put judgment, process, routing, and quality bars into Markdown skills that agents can read.

This is different from many agent frameworks that expose every endpoint as another tool and then overload the context window with APIs. GBrain’s bet is: fewer primitive tools, thicker procedural recipes, and a resolver that loads the right recipe at the right time.

## MCP and HTTP OAuth: memory as a service

The README documents both local and remote interfaces:

1. an MCP stdio server for clients such as Claude Code, Cursor, and Windsurf;
2. an HTTP MCP server with OAuth 2.1 for clients such as ChatGPT, Claude Desktop, and Perplexity.

That means GBrain is not only a local CLI. It is designed to act as a memory service shared across agent clients.

The repository also pays significant attention to security boundaries: `remote`, `scope`, `localOnly`, `read/write/admin`, path validation, OAuth tokens, admin dashboards, request-log redaction, and protected operations. This matters because personal memory becomes sensitive very quickly once email, meetings, contacts, investments, and private ideas flow into it.

## Minions: background work for a living brain

Another heavy component is `src/core/minions/`, a job queue system for long-running background work. The README and code reference cron, dream cycles, subagents, shell jobs, aggregators, quiet hours, staggering, idempotency, retries, and wall-clock timeouts.

This is where a long-term brain diverges from a chatbot.

A chatbot is synchronous: ask, answer. A brain must be asynchronous:

- sync new files at night;
- rebuild embeddings;
- turn transcripts into people, company, project, and concept pages;
- repair citations;
- detect orphan pages;
- discover patterns;
- prepare tomorrow’s briefing.

GBrain wants the agent to get smarter while the user is asleep. That requires a durable job layer, not just a prompt.

## Direct lessons for Peter / QCut / Hermes

The most useful value for us is not necessarily copying GBrain wholesale. The more important value is architectural direction.

### 1. QCut needs a project brain

QCut context is scattered across repos, issues, Discord threads, video examples, user feedback, design ideas, and bug history. A real video agent will need project memory:

- Which export bugs have appeared before?
- Which user complaints repeat across channels?
- Which templates or subtitle styles work for which audience?
- What was the creative intent and asset lineage for a given video project?

That maps naturally to pages, chunks, typed links, timelines, and sources.

### 2. Hermes/OpenClaw skills need a maintainable memory layer

We already use Hermes skills, but skills should not remain purely manual. A good agent should detect repeated failures, update skills, retire stale rules, and run evals to prevent regressions.

GBrain’s `skillify`, `maintain`, eval replay, and dream-cycle concepts point toward a closed loop where skills and memory improve together.

### 3. Memory is more than preferences

Many agent products reduce memory to key-value preferences: preferred language, timezone, tools, style. That is only the first layer.

Production memory should represent people, companies, projects, events, documents, opinions, decisions, evidence, timelines, and relationships. GBrain’s typed graph model is much closer to that end state.

## Risks and open questions

GBrain is also risky.

First, it is complex. A personal memory system with 30+ skills, 80+ operations, HTTP OAuth, job queues, PGLite/Postgres engines, eval capture, and an admin SPA brings real learning and maintenance costs.

Second, it depends on agents actually following skills correctly. Markdown skills are powerful, but execution quality still depends on whether the agent reads, understands, and follows the right procedure. Resolvers, evals, and doctor commands help, but cannot eliminate this risk.

Third, the privacy burden is high. The more powerful the brain, the more likely it is to store email, meetings, contacts, investments, and private thoughts. Remote MCP, OAuth, background jobs, and file upload surfaces require continuous security review.

Fourth, graph quality matters. If entity extraction, link types, and timeline extraction are noisy, the brain can become more tangled over time. The README describes citation repair and maintenance cycles, but long-term quality still needs real-world validation.

## Why it matters

GBrain is not important because it is “another RAG tool.” It is important because it points to the next layer of agent infrastructure:

> Agents should not merely call tools. They should have a long-term knowledge layer that grows, organizes, cites, repairs, and reflects.

Many AI agents today are still context-window engineering: add more files to the prompt, add more MCP tools, add more chat history. GBrain argues for the opposite: keep a real brain outside the context window, maintain it continuously, and retrieve only what the current task needs.

If this direction is right, every long-running personal agent will eventually need three layers:

1. an execution harness for tools and conversations;
2. a skills layer for procedures and judgment;
3. a brain layer for memory, relationships, timelines, and self-maintenance.

GBrain is an ambitious attempt to engineer that third layer.
