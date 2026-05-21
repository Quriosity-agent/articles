# New API Deep Dive: The AI Model Gateway Is Becoming an Enterprise Model Switch

> Project: [QuantumNous/new-api](https://github.com/QuantumNous/new-api)  
> Website: [newapi.ai](https://www.newapi.ai)  
> Docs: [docs.newapi.pro](https://docs.newapi.pro/en/docs/api)  
> Sources: GitHub repository / README / source code / GitHub API  
> Date: 2026-05-20  
> Tags: New API / AI Gateway / OpenAI Compatible / Claude / Gemini / Model Routing / Billing / Enterprise AI Infrastructure

![New API architecture diagram](imgs/new-api-ai-gateway/architecture.svg)

The most interesting thing about New API is not that it is “another OpenAI-compatible proxy.” It is that it turns model access into something closer to an enterprise **AI model switch**.

The GitHub description is direct: New API is a unified AI model hub for aggregation and distribution. It supports converting various LLMs into OpenAI-compatible, Claude-compatible, or Gemini-compatible formats, while providing a centralized gateway for personal and enterprise model management. The repository currently has roughly **34.5k stars and 7.7k forks**, is primarily written in Go, and is licensed under AGPL-3.0.

From the code, New API is not a simple HTTP reverse proxy. It handles users, tokens, groups, channels, model mapping, format conversion, billing expressions, retries, sensitive-word checks, logs, dashboards, payments, OAuth, caches, WebSocket Realtime, Midjourney/Suno/video tasks, and more. In other words, it is trying to own not just “where the request is forwarded,” but the entire operational surface of model usage.

This article breaks down what problem New API solves, how its architecture works, why it reflects a real trend in AI infrastructure, and what value and risks it may bring inside an enterprise.

---

## 1. The model access problem has shifted from “Do we have an API?” to “How do we govern the API?”

Two years ago, many AI applications started with a simple integration:

```text
App → OpenAI API
```

Then model providers multiplied:

```text
App → OpenAI / Azure / Claude / Gemini / DeepSeek / OpenRouter / Bedrock / local models ...
```

At that point, the real problems begin:

- Provider API schemas differ.
- The same model capability can have different prices, latency, limits, and reliability across channels.
- Different users, teams, and projects need different quotas.
- Failures require retry, fallback, or degradation policies.
- Tokens must be estimated, pre-consumed, settled, and audited.
- Streaming, tool calling, images, audio, Realtime, and other interfaces all need compatibility work.
- Administrators need visibility into usage, logs, balances, and errors.
- Security requires key isolation, permissions, sensitive-text checks, request-size limits, CORS, and OAuth.

So the value of a model gateway is no longer just forwarding `/v1/chat/completions`. It is turning model providers into a governable resource pool.

New API follows exactly this direction: externally, it preserves client-facing OpenAI / Claude / Gemini style APIs; internally, it manages channels, billing, permissions, and conversion logic.

---

## 2. Architecturally, it is a Go backend, React admin console, and multi-adapter relay layer

The repository size already shows that this is not a toy project. A rough scan, excluding build artifacts, shows about **1,989 files**: 571 Go files and more than 1,200 frontend TS/TSX/JSX/JS files. The core structure looks like this:

| Directory | Role |
|---|---|
| `main.go` | Service startup, resource initialization, caches, background tasks, Gin server |
| `router/` | API, relay, dashboard, video routes |
| `controller/` | Request entrypoints, management APIs, relay orchestration |
| `middleware/` | TokenAuth, Distribute, CORS, rate limiting, stats, request decompression |
| `relay/` | OpenAI / Claude / Gemini / image / audio / embedding / rerank / responses handlers |
| `relay/channel/` | Provider adaptors, currently 37 provider directories |
| `model/` | GORM models: users, tokens, channels, logs, subscriptions, pricing |
| `service/` | Billing, token estimation, retries, tasks, OAuth, conversions |
| `setting/` | System, ratio, performance, and model settings |
| `web/default/` | New admin console based on React 19, TypeScript, Rsbuild, and TanStack Router |

The startup path is also revealing. `main.go` initializes resources and the database, enables memory/Redis cache, starts channel-cache synchronization, hot option sync, quota dashboard updates, channel auto-tests, Codex credential refresh, subscription quota resets, upstream model update checks, Midjourney/task polling, Pyroscope profiling, and finally the Gin server with embedded frontend assets.

This is not an SDK-level helper. It is a long-running server-side control plane.

---

## 3. Relay routes: one gateway carrying multiple API semantics

`router/relay-router.go` shows that New API exposes a broad set of API surfaces:

- `/v1/models`, `/v1/chat/completions`, `/v1/completions`;
- `/v1/responses`, `/v1/responses/compact`;
- `/v1/images/generations`, `/v1/images/edits`;
- `/v1/audio/transcriptions`, `/v1/audio/translations`, `/v1/audio/speech`;
- `/v1/embeddings`;
- `/v1/rerank`;
- `/v1/realtime` WebSocket;
- `/v1/messages` for Claude Messages;
- `/v1beta/models/*path` for Gemini;
- `/mj/*` for Midjourney proxy;
- `/suno/*` for Suno tasks;
- video task endpoints.

More importantly, these routes do not simply forward to a fixed upstream. They pass through a unified pipeline:

```text
Request
  → CORS / decompress / stats
  → TokenAuth
  → ModelRequestRateLimit
  → Distribute channel selection
  → request validation
  → token estimate
  → price / pre-consume billing
  → relay handler
  → retry / refund / settlement / log
```

The `Relay()` function in `controller/relay.go` makes this clear. It parses and validates the request, generates `RelayInfo`, performs sensitive-text checks, estimates tokens, calculates price, pre-consumes quota, enters a retry loop, selects channels, and finally invokes the relevant relay helper. When a request fails, it refunds the pre-consumed quota and may charge a violation fee if needed.

That is a complete model transaction processing system, not just a proxy layer.

---

## 4. The Distribute layer is the core: requests are routed to a suitable channel

New API’s channel abstraction is central. `model.Channel` includes:

- `Type`;
- `Key` and multi-key metadata;
- `BaseURL`;
- `Models`;
- `Group`;
- `Weight` and `Priority`;
- `Balance`;
- `ResponseTime`;
- `AutoBan`;
- `ModelMapping`;
- `StatusCodeMapping`;
- `ParamOverride` and `HeaderOverride`;
- `Setting` and `OtherSettings`.

In practice, this turns “an upstream API key” into an operable resource object.

Inside `middleware/distributor.go`, a relay request is distributed through roughly this flow:

1. Read the requested model from the request.
2. Check token-level model access restrictions.
3. Read the user’s current group.
4. If a playground request specifies a group, validate that the user can use it.
5. Try channel affinity.
6. Otherwise select a channel that satisfies the group/model constraints.
7. Store the selected channel, group, and model mapping into request context.

This resembles load balancing, but with model identity, user permissions, groups, pricing, balances, and failure policy attached. For enterprises, this is exactly the abstraction model governance needs: applications express the model capability they need; the platform decides which provider, key, group, price, and fallback path should serve it.

---

## 5. Multi-format conversion: New API is an AI API protocol translation layer

New API supports not only OpenAI-compatible APIs, but also Claude Messages, Google Gemini, OpenAI Responses, Realtime, Rerank, Midjourney, Suno, and more.

The README lists several conversion capabilities:

- OpenAI Compatible ⇄ Claude Messages;
- OpenAI Compatible → Google Gemini;
- Google Gemini → OpenAI Compatible;
- OpenAI Compatible ⇄ OpenAI Responses, still under development;
- thinking-to-content conversion.

The code reflects this. In `relay/channel/openai/adaptor.go`, Claude requests can be converted through `service.ClaudeToOpenAIRequest()`, and Gemini requests through `service.GeminiToOpenAIRequest()`. Gemini routes also have dedicated `GeminiHelper` and embedding handling.

This protocol translation layer is valuable because it reduces repeated provider-specific logic in application code:

```text
Claude client → /v1/messages → New API → OpenAI-compatible upstream
Gemini client → /v1beta/models/... → New API → OpenAI-compatible upstream
OpenAI client → /v1/chat/completions → New API → Claude / Gemini / OpenRouter / Azure / ...
```

Of course, protocol conversion can never be perfectly lossless. Tool calling, system prompts, thinking, cache control, multimodal content, safety settings, and response schemas all carry provider-specific semantics. New API’s value is centralizing these differences in the gateway instead of forcing every business service to write its own compatibility layer.

---

## 6. Billing expressions: from ratio tables to programmable billing contracts

One of the most interesting modules in New API is `pkg/billingexpr`.

Its design philosophy is: **One expression, one truth**. A single expression defines the billing logic for a model, including input, output, cache, images, audio, tiered pricing, time-based discounts, and request-aware multipliers.

A simple expression looks like:

```text
tier("base", p * 2.5 + c * 15 + cr * 0.25)
```

Variables include:

- `p`: input tokens;
- `c`: output tokens;
- `cr`: cache read tokens;
- `cc` / `cc1h`: cache creation tokens;
- `img` / `img_o`: image input/output tokens;
- `ai` / `ao`: audio input/output tokens;
- `len`: full context length for long-context tiering.

It also supports functions like `param(path)`, `header(key)`, `hour(tz)`, and `weekday(tz)`, allowing billing to depend on request body, headers, or time.

This direction matters because model pricing is becoming increasingly complex:

- cache hits and cache writes;
- long-context tiers;
- reasoning effort;
- audio/image/video tokens;
- batch discounts;
- different provider units;
- internal enterprise markups or discounts.

A simple `model ratio` table will collapse under these requirements. By expressing billing logic as a configurable expression, New API turns billing from hardcoded rules into a programmable contract.

---

## 7. The frontend console is an operations dashboard, not just a config page

`web/default` uses React 19, TypeScript, TanStack Router, TanStack Query, Zustand, Base UI, Tailwind CSS, VChart, and i18next. The frontend is large, which implies that the admin console carries significant product weight.

From its dependencies and structure, the UI appears to cover:

- users, tokens, channels, and models;
- logs and usage statistics;
- dashboards and charts;
- billing and pricing configuration;
- subscriptions, payments, and redemption codes;
- internationalization;
- playground;
- theming and responsive management UI.

This is a practical requirement. A model gateway that only exposes YAML configuration may work for individual developers, but a team or enterprise needs an operational interface. Quotas, balances, channel health, failure rates, logs, and permissions need to be managed continuously without code changes.

---

## 8. New API is best suited for multi-model, multi-team, multi-channel environments

If you are building a small personal demo, using the OpenAI or OpenRouter SDK directly may be simpler. New API becomes valuable in scenarios like these:

### 8.1 A unified internal model entrypoint

If many internal services call models, they can all route through New API:

```text
Business apps → New API → multiple model providers
```

Business services no longer need to store provider keys or implement every provider-specific edge case.

### 8.2 Multi-provider cost and reliability management

The same model capability may be available through an official API, a cloud vendor, a third-party aggregator, or a local deployment. New API can distribute by group, priority, weight, retry policy, and channel status.

### 8.3 A unified external API platform

If a team wants to provide a unified AI API service to internal users or customers, New API already includes users, tokens, billing, payments, logs, and quotas.

### 8.4 Compatibility with multiple client ecosystems

Many tools only support OpenAI-compatible APIs; others increasingly support Claude or Gemini native formats. New API’s multi-format entrypoints reduce client adaptation work.

---

## 9. Risks and caveats: the stronger the gateway, the more responsibility it concentrates

New API is powerful, but a production deployment carries real engineering responsibility.

### 9.1 Security boundary

A model gateway stores many upstream API keys and user tokens. It is a high-value target. Production deployment must take care of:

- `SESSION_SECRET`;
- `CRYPTO_SECRET`;
- database permissions;
- Redis security;
- HTTPS;
- administrator accounts;
- sensitive data in logs;
- backup and recovery.

The README explicitly warns that multi-node deployments must set `SESSION_SECRET`, and shared Redis deployments must set `CRYPTO_SECRET`.

### 9.2 Limits of protocol conversion

OpenAI, Claude, and Gemini do not have identical semantics. A gateway reduces adaptation cost, but developers should not assume every model is interchangeable. Tool calling, structured output, thinking, cache, and multimodal fields still need model-specific testing.

### 9.3 Billing accuracy

Pre-consumption, streaming output, retries, cache tokens, image/audio tokens, and failure paths all affect final billing. Enterprise deployments should validate billing expressions using real request replays, not only default ratios.

### 9.4 AGPL-3.0 license

New API uses AGPL-3.0. Internal deployment may be straightforward, but if you modify it and provide it as a network service, you should carefully evaluate AGPL source-code obligations.

---

## 10. Why this project matters: AI infrastructure is entering the model operations stage

Projects like New API show that AI application engineering is entering a new stage.

The first stage was **API access**: just call the model.  
The second stage was **SDK compatibility**: make everything look OpenAI-compatible.  
The third stage is **model operations**: manage models as enterprise resources, with permissions, quotas, billing, routing, audit, fallback, and monitoring.

New API is clearly in the third stage.

It abstracts model providers as channels, user access as groups and tokens, pricing as billing expressions, API schema differences as relays and adaptors, and operational needs as dashboards and logs. This abstraction is complex, but it is close to what real production environments need.

Future systems in this category will likely evolve toward:

- finer-grained cost-optimization routing;
- quality/latency-aware automatic model selection;
- cross-provider standardization for prompts, tools, and response schemas;
- eval-driven routing policy;
- integration with enterprise IAM, SIEM, and FinOps systems;
- full audit trails for agent traces and tool use.

From this perspective, New API is not merely “another one-api fork.” It is a concrete prototype of the AI gateway product category.

---

## Conclusion: the endgame of model gateways is not proxying, but control planes

New API’s core value can be summarized in one sentence:

> It turns scattered, inconsistent, hard-to-govern model APIs into a resource pool that teams can centrally manage, route, bill, and audit.

For individual developers, it is a powerful multi-model aggregation tool.  
For teams, it is a unified model entrypoint and cost-control layer.  
For enterprises, it points to an increasingly important layer of AI infrastructure: the model operations control plane.

As the number of models, interface types, and pricing strategies keeps growing, direct application-to-provider integrations will become harder to maintain. A more sustainable architecture will likely place a gateway like this between business applications and model providers.

That is the significance of New API: it does not just make model calls cooler. It makes them manageable.
