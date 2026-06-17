---
title: "A Cron Heartbeat Failure Shows Why Agent Runtimes Need a Model Registry, Not Just a Model String"
date: 2026-06-17
source: "Discord cron failure report"
canonical:
  - "https://docs.openclaw.ai/concepts/model-providers"
  - "https://hermes-agent.nousresearch.com/docs/user-guide/features/cron"
  - "https://hermes-agent.nousresearch.com/docs/integrations/providers"
tags:
  - Cron
  - Hermes Agent
  - OpenClaw
  - Model Providers
  - Agent Runtime
  - Configuration
---

# A Cron Heartbeat Failure Shows Why Agent Runtimes Need a Model Registry, Not Just a Model String

The source for this article is not a launch post or a benchmark chart. It is a very ordinary production alert:

```text
Cron job "3å°æ—¶å­˜æ´»å¿ƒè·³" failed: FailoverError: Unknown model: openai-codex/gpt-5.4. Found agents.defaults.models["openai-codex/gpt-5.4"], but no matching models.providers["openai-codex"].models[] entry. Add { "id": "gpt-5.4", "name": "gpt-5.4" } to models.providers["openai-codex"].models[] to register this provider model. For custom or proxy providers, also set api and baseUrl so requests route to the intended endpoint. See https://docs.openclaw.ai/concepts/model-providers.
```

At first glance, this is a small configuration bug: `agents.defaults.models` includes `openai-codex/gpt-5.4`, but `models.providers.openai-codex.models[]` does not register `gpt-5.4`. When the Cron job starts, the model failover layer cannot find an executable provider/model pair and throws `Unknown model`.

But the failure is worth writing about because it exposes an often underestimated point in agent infrastructure: **a model string is not model configuration. A production-grade agent runtime needs a verifiable, routable, failover-aware model registry.**

## One-sentence summary

**The Cron heartbeat did not fail because the model was not smart enough. It failed because the scheduler, default-model allowlist, provider catalog, and request routing did not form a consistent control plane.**

In an interactive chat, a bad model config usually breaks one reply. In Cron jobs, background tasks, article automation, health checks, and monitoring bots, the same error becomes systemic unavailability. There is no human standing by to switch models, re-authenticate, or patch a provider by hand. The configuration itself must be executable.

## What the error actually says

The message points to three distinct layers:

| Layer | Config location | Role | Problem in this failure |
|---|---|---|---|
| Task default models | `agents.defaults.models` | Tells the agent which models may be selected or used for failover | Contains `openai-codex/gpt-5.4` |
| Provider model catalog | `models.providers.openai-codex.models[]` | Tells the runtime which model ids this provider actually supports | Missing `gpt-5.4` |
| Routing parameters | provider `api`, `baseUrl`, etc. | Tells the runtime where to send the request | Custom or proxy providers need explicit routing |

The system is not merely splitting `openai-codex/gpt-5.4` into provider and model. It also needs to verify that:

1. the `openai-codex` provider exists;
2. that provider has a registered `gpt-5.4` model;
3. the provider has enough routing information to make the request;
4. failover will not jump to a model that appears in an allowlist but cannot actually run.

That is what a registry is for. It turns “a human remembers this model exists” into “the runtime can verify this model is callable.”

## Why Cron amplifies the problem

Hermes Cron jobs run in fresh agent sessions. The Hermes Cron documentation emphasizes that scheduled tasks can load skills, specify delivery targets, bind a workdir, or run as script-only no-agent jobs. But ordinary LLM-driven Cron jobs still depend on the configured provider/model.

That is different from manual chat:

- if manual chat fails, a user can switch models with `/model`;
- if a Cron job fails, it usually emits a failure notification;
- if the job is a heartbeat, monitor, or daily report, the failure itself contaminates the signal;
- if multiple jobs share the same default model, one config bug affects the whole automation layer.

Cron is therefore a stress test for model configuration. It asks a simple question: **can this model reference travel from the scheduler all the way to the real API without human intervention?**

In this case, the answer was no.

## The key OpenClaw model-provider rules

OpenClaw’s Model Providers documentation gives several directly relevant rules:

- model references use the `provider/model` form;
- `agents.defaults.models`, when set, acts as an allowlist;
- provider-level defaults may define context window and token limits;
- each provider’s `models[]` can carry per-model overrides;
- custom or proxy providers need routing details such as `api` and `baseUrl`, not only a model id.

In other words, `agents.defaults.models` is not just a loose list of strings. It is closer to an admission list for the scheduler. Every model admitted there should have a corresponding entity in the provider catalog.

If the allowlist is maintained but the catalog is not, the result is exactly this failure: the default list thinks `openai-codex/gpt-5.4` is available, but the provider does not know that model.

## The minimal fix

The error already gives the minimal fix: register the model under `models.providers.openai-codex.models[]`.

Conceptually, that looks like this:

```json5
{
  "models": {
    "providers": {
      "openai-codex": {
        "models": [
          { "id": "gpt-5.4", "name": "gpt-5.4" }
        ]
      }
    }
  }
}
```

If `openai-codex` is a standard OAuth provider, registering the model id may be enough. If it is actually a custom, proxy, or OpenAI-compatible provider, the routing configuration must also be verified:

```json5
{
  "api": "openai-compatible-or-provider-specific-api",
  "baseUrl": "https://your-provider-endpoint.example.com/v1"
}
```

The important principle is not the two JSON lines. It is this: **do not only add `gpt-5.4` to the default list. Register it under a provider that can actually make the request.**

## A safer operational sequence

A one-line config patch can silence the alert, but production systems should make this a repeatable workflow:

1. **List the current models**: inspect what the runtime sees, not only what strings exist in a config file;
2. **Check default models**: verify that `agents.defaults.models` or the primary model points only to registered models;
3. **Check the provider catalog**: every default model must have a matching `id` under `models.providers.<provider>.models[]`;
4. **Check routing**: custom providers must have explicit `api` / `baseUrl` routing;
5. **Run the failed Cron manually**: do not wait until the next interval;
6. **Read logs, not only notifications**: verify that the Cron session entered the agent loop and completed.

On the Hermes side, a typical troubleshooting path is:

```bash
hermes cron list
hermes cron run <job_id>
hermes doctor
hermes model
```

On the OpenClaw side, the model-provider documentation points to commands such as:

```bash
openclaw models list
openclaw models set <provider/model>
openclaw onboard
```

The point of these commands is to align configuration intent with runtime reality.

## Heartbeat jobs may not need an LLM

The failing job name appears to be a “3-hour keepalive heartbeat.” If the goal is only to prove that a system is alive, not to produce a natural-language summary, there is another architectural option: convert it into a no-agent Cron job.

Hermes Cron supports script-only no-agent mode: non-empty stdout is delivered, empty stdout stays silent, and the job does not involve an LLM provider at all. For heartbeats, disk alerts, process checks, port checks, and GPU-temperature alerts, this is often more reliable.

The principle is simple:

| Task type | Recommended mode | Why |
|---|---|---|
| “Is the system alive?” | no-agent script | Model availability should not be required to prove system availability |
| “Alert me when disk exceeds 90%” | no-agent script | Fixed threshold, no reasoning needed |
| “Summarize new articles every morning” | LLM Cron | Requires reading, filtering, and summarizing |
| “Check CI and explain failures” | LLM Cron | Requires log understanding and context |

If a heartbeat fails because the model provider is misconfigured, it reveals two problems at once: the model registry needs repair, and the heartbeat may be coupled to the LLM layer unnecessarily.

## The product lesson for agent systems

This small alert points to a core engineering issue in agent products: an agent is not a prompt plus a model. It is a control plane.

That control plane includes at least:

- a model registry: which models exist, which provider owns them, and what context/token limits apply;
- default policy: which models can be primary, fallback, or task-specific;
- routing: whether requests go to an official API, OAuth app-server, proxy gateway, or local model;
- scheduling: how Cron, background jobs, webhooks, and messaging platforms inherit model policy;
- observability: whether failures distinguish auth, quota, unknown model, schema, and endpoint errors.

When these layers are collapsed together, “a model name is wrong” looks like “the agent failed.” When the layers are explicit, an error can be as precise as this one: a registry entry is missing.

## Conclusion

The `openai-codex/gpt-5.4` Cron failure is not merely a reminder to add `{ "id": "gpt-5.4", "name": "gpt-5.4" }`. It is a reminder that unattended agent reliability depends not only on model capability, but also on the completeness of the model control plane.

The production goal is not “make one string run.” It is:

1. default model lists contain only registered, routable, callable models;
2. the provider catalog is the single source of truth;
3. unattended tasks such as Cron can run without manual model switching;
4. heartbeat and monitoring jobs avoid unnecessary LLM dependencies;
5. every model upgrade updates the allowlist, provider catalog, routing, and verification flow together.

The more automated an agent system becomes, the less model selection can be treated as a UI dropdown. It should be a registry that the scheduler, failover layer, and operations tools can all verify.
