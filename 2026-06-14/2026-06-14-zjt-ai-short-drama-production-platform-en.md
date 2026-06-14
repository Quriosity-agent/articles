# ZJT / ZhiJuTong Deep Dive: The Hard Part of AI Short Drama Is Turning Agents, Canvas, Compute, and Media Providers into a Production System

> Repo: [https://github.com/jeffstric/ZJT](https://github.com/jeffstric/ZJT)  
> Inspected commit: `6376022` (`main`)  
> Date: 2026-06-14  
> Tags: AI Video, Short Drama, Multi-Agent, Production Pipeline, Storyboard, Creator Tools, FastAPI, Python

![ZhiJuTong project hero](imgs/zjt-ai-short-drama-production-platform/hero.jpg)

Many AI-video projects stop at the demo layer: type a prompt, wait for a model, download a clip. Short drama production is different. It needs scripts, characters, locations, storyboards, first/last frames, reference images, voice, video generation, asset management, team collaboration, cost accounting, and failure recovery. ZJT, or ZhiJuTong, is interesting because it does not reduce “AI short drama production” to one model call. The repository exposes something closer to a production control plane.

At the time of inspection, `jeffstric/ZJT` is a public Python repository. GitHub API reports 165 stars, 38 forks, 162 open issues, creation on 2026-03-04, and latest push on 2026-06-13. The repository description positions it as an “AI-powered, open-source platform specifically designed for creating professional short dramas,” automating the pipeline from script and storyboard creation to final video synthesis. Its GitHub license field is `Other / NOASSERTION`, so commercial adopters should verify the real license boundary before reuse.

## First, the size: this is not a thin README demo

After a shallow clone, I counted 977 files. 965 were readable as text, with roughly 320,140 text/code lines. The main breakdown is:

| Dimension | Count |
|---|---:|
| Python files | 493 |
| Markdown docs | 295 |
| JavaScript files | 38 |
| JSON files | 37 |
| YAML / YML files | 29 |
| Text/code lines | ~320k |
| `server.py` routes | 89 FastAPI routes |
| `api/script_writer.py` routes | 60 routes |
| `api/admin.py` routes | 32 routes |

By directory, `web/` is roughly 80k lines, `.qoder/` around 49k, `tests/` around 30k, `auto_test/` around 24k, `script_writer_core/` around 22k, `task/` around 20k, `docs/` around 17k, and `model/` around 16k. The center of gravity is not a single inference script. It is a combination of Web product, backend APIs, data models, task orchestration, tests, docs, and agent workflows.

The dependency list is also revealing: FastAPI, uvicorn, gunicorn, PyYAML, OpenAI, httpx, pyJianYingDraft, APScheduler, cryptography, bcrypt, pymysql, Alembic, SQLAlchemy, qiniu, anthropic, litellm, mcp, pytest, Pillow, and OpenCV. ZJT connects LLMs, databases, object storage, auth/payment, MCP, JianYing draft generation, and media processing.

## Product layer: short drama creation is a collaboration chain, not one button

The README highlights eight expert agents, infinite canvas plus multi-panel storyboards, script-to-storyboard-to-video generation, multi-model support, team collaboration, user-level compute accounts, Windows/macOS/Linux/Docker startup, API testing, and admin operations.

![ZhiJuTong workflow](imgs/zjt-ai-short-drama-production-platform/workflow.jpg)

Product-wise, ZJT separates AI short drama into four classes of assets:

1. **Narrative assets**: outlines, episode scripts, dialogue, emotional arcs;
2. **Visual assets**: character profiles, locations, props, style, references;
3. **Production assets**: storyboards, first/last frames, video tasks, audio/TTS, JianYing drafts;
4. **Operational assets**: users, compute credits, payments, providers, model configs, admin analytics.

That is much closer to real teams than a “Prompt → Video” flow. In short drama, the expensive part is repeated alignment: characters must stay consistent, shots cannot drift, cost cannot run away, failed tasks need recovery, and multiple collaborators need the same project context.

## Architecture: FastAPI monolith plus configurable drivers plus agent workbench

The backend entry point is `server.py`, a large FastAPI module covering uploads, image proxies, thumbnails, image editing, text-to-image, AI app runs, RunningHub status, user roles, compute credits, check-ins, task status, and more. It also mounts modules such as `api/admin.py`, `api/script_writer.py`, `api/media.py`, `api/user.py`, and `api/system.py`.

A useful way to read the current architecture is six layers:

```text
Browser UI / infinite canvas / admin panels
        ↓
FastAPI routes: server.py + api/*
        ↓
Domain models: world / script / character / location / props / ai_tools / async_tasks
        ↓
Agent runtime: script_writer_core + agents/skills + SOP loader
        ↓
Task orchestration: task/*, pipeline_processor, visual/audio/async drivers
        ↓
External providers: LLMs, RunningHub, Volcengine, Vidu, Duomi, Qiniu, WeChat Pay, JianYingDraft
```

The advantage is shipping speed: one Python service wires together creation, media, configuration, tasks, admin, and operations. The drawback is also visible: `server.py` is about 8,900 lines. As the team grows, routes, services, domain logic, and task orchestration should continue to be separated.

## The most reusable layer: unified task configuration and provider drivers

`config/unified_config.py` is one of the repository’s core assets. It defines task categories such as image editing, text-to-video, image-to-video, text-to-image, visual enhancement, audio, and digital human. It also defines provider abstractions such as Duomi, RunningHub, Vidu, Volcengine, Local, and ZJT. `ImplementationConfig` can express display name, driver class, default compute cost, enablement, sort order, site number, sync mode, and required config keys.

This shows ZJT understands a practical truth: an AI-video product cannot bet on one provider. Model APIs queue, fail, change prices, rate-limit, and get replaced. Decoupling “task type” from “implementation provider” makes it possible to:

- support multiple implementations for the same task;
- let admins adjust priority by price, quality, and stability;
- let users choose their own model or provider;
- retry with another implementation after failure;
- calculate compute cost dynamically by task, duration, resolution, and mode.

For short drama tools, this matters a lot. Scripts, images, video, audio, and digital humans may all come from different vendors. The durable product moat is not “we called one API.” It is turning provider composition into a stable production pipeline.

## Pipeline layer: failure is not an exception; it is part of production

`task/pipeline_processor.py` shows how ZJT models production failures. It creates and dispatches steps, polls processing steps, and applies results back to `ai_tool`. For example, Seedance 2.0 image-to-video tasks with video input create a `face_mask` preprocessing step.

More importantly, failures are modeled explicitly:

- `SLOT_FULL` is recognized as capacity pressure and scheduled for retry with exponential backoff;
- steps can move through `PENDING / PROCESSING / COMPLETED / FAILED`;
- a `before_finish` stage can create implementation retries and choose an alternative provider;
- async tasks and pipeline steps are linked by IDs, keeping long-running work out of synchronous request handling.

This is the difference between an AI-video product and an AI-video script. A script only has to succeed once. A product has to deal with full queues, provider outages, image preprocessing failures, page refreshes, backend restarts, and long-task timeouts.

## Agent layer: SOP-loaded workflows, not prompt soup in code comments

`script_writer_core/chat_session.py` initializes a PM Agent and selects either the script agent or marketing agent depending on session type. The default script agent loads workflow content from `script_writer_core/skills/script-orchestrator/SKILL.md` plus SOP files. The marketing agent loads from `agents/skills/marketing-pm`.

`script-orchestrator/SKILL.md` reveals a strong product idea: the agent is not “just chat.” It executes around SOPs. The flow requires the agent to:

- inspect current project resources such as characters, scripts, locations, and props;
- use `ask_user` to collect requirements, preferably with options to reduce typing;
- load different SOPs for new scripts, continuation, or novel/script splitting;
- show progress at key steps;
- coordinate expert agents through a PM Agent.

The README lists eight expert agents: Story Writer, Character Creator, Location Creator, Plot Analyzer, Content Compliance, Novel Splitter, Character Designer, and Location Designer. This “PM plus experts” pattern is much more controllable than a generic chat box because it encodes user decision points, generation stages, and quality checks into a workflow.

## UI layer: the infinite canvas is the operating surface for AI short drama

![Infinite canvas and storyboard interface](imgs/zjt-ai-short-drama-production-platform/canvas.jpg)

The `web/` directory is large, and the README emphasizes browser-based real-time collaboration, SSE updates, infinite canvas, multi-panel storyboards, character profile editing, and team work. This direction is important: the core interface for AI video may not be a chat box. It may be an editable production board.

The reason is simple. Short drama state is spatial. Characters, locations, shots, assets, and timelines relate to each other. An infinite canvas lets the team see those relationships instead of hunting through chat history for a generated artifact. For builders working on tools like QCut, this is especially relevant: agents can generate content, but the output must land on a surface that is editable, reversible, and collaborative.

## Business layer: compute accounts are closer to real operations than model selection

One of ZJT’s most practical designs is the user-level compute account. The README says each user has an independent quota, can select providers, and admins can hot-update model configs, pricing, provider priority, user quotas, and limits. It also supports WeChat Pay top-ups.

That points beyond a personal toy. For education, teachers care about budget. For content teams, leads care about which member consumed how much compute, which provider failed most often, and when to switch models. These are not model-capability questions. They are operational control questions.

## Engineering: encouraging signs, with hardening work still ahead

ZJT includes `tests/`, `auto_test/`, `.github/workflows/guard-enterprise.yml`, `.gitlab-ci.yml`, Docker config, Alembic migrations, Sentry, admin panels, and extensive docs. `auto_test/` even includes a Claude launcher, context management, report generation, and test navigation, suggesting tooling for agent-assisted testing.

From a production-hardening perspective, I would watch five areas:

1. **Large entry-point risk**: `server.py` is too large, and route logic, file handling, task submission, and permission checks can become coupled;
2. **License ambiguity**: GitHub reports `NOASSERTION`, so “open-source” should not be treated as a commercial grant by default;
3. **Configuration and secret governance**: many providers, payment systems, and storage backends require strict separation between examples, production config, and user credentials;
4. **Provider observability**: drivers and retries are not enough; teams need per-provider success rate, latency, cost, and failure reason analytics;
5. **Media lifecycle management**: images, videos, caches, thumbnails, external URL mappings, and CDN cleanup need their own governance or they become a cost sink.

## Who should study ZJT?

Three groups should look closely:

- **AI-video tool founders**: learn how to move from model demo to the full product stack of tasks, providers, compute, canvas, and admin operations;
- **Agent product designers**: study how PM Agent, expert agents, SOP loading, `ask_user`, and progress display fit together;
- **Content-team or education-platform engineers**: focus on user-level compute, collaboration, and multi-provider redundancy instead of only comparing model outputs.

## Conclusion: ZJT’s value is the control plane, not merely short-drama generation

The most reusable thing about ZJT is not the claim that it can generate short dramas. It is that the repository puts the dirty production work in one place: user decisions, character/location assets, storyboard canvas, provider selection, compute billing, long-running task status, failure retry, admin management, testing, and deployment.

That is the next recurring problem for AI creation tools. Models will keep improving, but the hard product question moves from “can it generate?” to “can it organize production reliably?” ZJT’s answer is: use agents for narrative, a canvas for creative state, unified config for providers, pipelines for long tasks and failures, and compute accounts for operational cost.

It is not yet a perfect enterprise architecture. But as an open-source sample of an AI short-drama production system, it is already much closer to the real world than most single-point demos.
