# QCut CLI Command Architecture Refactor Proposal (Inspired by MiniMax, Preserving QCut Depth)

- Author: 🦞 龙虾侦探 / Lobster Detective
- Date: 2026-04-11
- Tags: qcut, cli, information-architecture, minimax, developer-experience, agentic-tooling

## TL;DR

QCut is currently "high capability, uneven command surface": strong functionality, but mixed naming styles (`generate-*`, `create-*`, `vimax:*`, `list-*`) increase cognitive load for humans and reduce reliability for agent tool planning.

The fix is not capability reduction. The fix is **information architecture + naming unification**:

- `qcut gen <image|video|avatar|music|grid>`
- `qcut analyze <video|image|query>`
- `qcut audio <transcribe|translate|tts>`
- `qcut edit <autoclip|upscale|motion|compose>`
- `qcut flow <run|idea2video|script2video|novel2movie|script|characters|portraits|storyboard|registry>`
- `qcut system <auth|quota|config|doctor|quickstart|examples|models|project|publish>`

Roll out in 2 weeks with aliases and deprecation warnings, no script breakage in the transition window.

## Why QCut Feels Powerful but Slightly Chaotic

1. **Inconsistent naming for similar jobs**  
   - `generate-image` vs `create-video` vs `generate-avatar`
2. **Mixed command namespace styles**  
   - Flat commands (`run-pipeline`) + prefixed commands (`list-video-models`) + colon style (`vimax:idea2video`)
3. **Control-plane and data-plane mixed together**  
   - model discovery, key management, project ops, and content generation appear at similar levels
4. **Lower agent predictability**  
   - agents perform better with stable hierarchy and constrained verbs

Bottom line: QCut does not have a capability problem, it has a command IA consistency problem.

## MiniMax CLI Architecture Summary (Resource + Action)

MiniMax CLI is organized around:

- Top-level resources: `text|image|video|speech|music|vision|search|auth|config`
- Second-level actions: `chat|generate|synthesize|describe|query|login|set`
- Cross-cutting conventions: JSON output mode, async task polling, unified auth/config entry points

What matters for QCut:

- Resource-first grouping improves discoverability for both humans and agents
- Verb normalization (`generate`, `get`, `download`) reduces ambiguity
- Separate management plane (`auth/config/quota`) from creation/edit pipelines

## Proposed QCut Target Taxonomy

### 1) Generation layer

```bash
qcut gen image
qcut gen video
qcut gen avatar
qcut gen music
qcut gen grid
```

### 2) Analysis layer

```bash
qcut analyze video
qcut analyze image
qcut analyze query
```

### 3) Audio/language layer

```bash
qcut audio transcribe
qcut audio translate
qcut audio tts
```

### 4) Editing/production layer

```bash
qcut edit autoclip
qcut edit upscale
qcut edit motion
qcut edit compose
```

### 5) Workflow/orchestration layer (including ViMax)

```bash
qcut flow run
qcut flow idea2video
qcut flow script2video
qcut flow novel2movie
qcut flow script
qcut flow characters
qcut flow portraits
qcut flow storyboard
qcut flow registry create
qcut flow registry show
```

### 6) System/control layer

```bash
qcut system auth
qcut system quota
qcut system config
qcut system doctor
qcut system quickstart
qcut system examples
qcut system models
qcut system project init
qcut system project organize
qcut system project info
qcut system publish youtube
```

## Full Old → New Mapping Table (Migration Map)

| Old command | New command | Notes |
|---|---|---|
| `generate-image` | `qcut gen image` | Normalize generation verbs |
| `create-video` | `qcut gen video` | Fold `create-*` into `gen` |
| `generate-avatar` | `qcut gen avatar` | Keep behavior, improve namespace |
| `generate-grid` | `qcut gen grid` | Batch visual generation |
| `transfer-motion` | `qcut edit motion` | Move to edit namespace |
| `upscale-image` | `qcut edit upscale` | Move to edit namespace |
| `analyze-video` | `qcut analyze video` | Resource + action |
| `query-video` | `qcut analyze query` | Query analysis subdomain |
| `transcribe` | `qcut audio transcribe` | Isolate language ops |
| `translate-video` | `qcut audio translate` | Speech translation under audio |
| `autoclip` | `qcut edit autoclip` | Keep 4-stage pipeline semantics |
| `run-pipeline` | `qcut flow run` | Single orchestration entry |
| `vimax:idea2video` | `qcut flow idea2video` | Remove colon style |
| `vimax:script2video` | `qcut flow script2video` | Remove colon style |
| `vimax:novel2movie` | `qcut flow novel2movie` | Remove colon style |
| `vimax:generate-script` | `qcut flow script` | Simplify command name |
| `vimax:extract-characters` | `qcut flow characters` | Simplify command name |
| `vimax:generate-portraits` | `qcut flow portraits` | Simplify command name |
| `vimax:generate-storyboard` | `qcut flow storyboard` | Simplify command name |
| `vimax:create-registry` | `qcut flow registry create` | Nested resource pattern |
| `vimax:show-registry` | `qcut flow registry show` | Nested resource pattern |
| `vimax:list-models` | `qcut system models --scope vimax` | Consolidate model discovery |
| `list-models` | `qcut system models list` | Move to system namespace |
| `list-avatar-models` | `qcut system models list --type avatar` | Replace forks with typed flag |
| `list-video-models` | `qcut system models list --type video` | Same pattern |
| `list-motion-models` | `qcut system models list --type motion` | Same pattern |
| `list-speech-models` | `qcut system models list --type speech` | Same pattern |
| `estimate-cost` | `qcut system quota estimate` | Put cost into quota plane |
| `setup` | `qcut system auth setup` | Credential bootstrap |
| `set-key` | `qcut system auth set-key` | Unified key management |
| `check-keys` | `qcut system auth check` | Unified health check |
| `init-project` | `qcut system project init` | Project ops grouping |
| `organize-project` | `qcut system project organize` | Project ops grouping |
| `structure-info` | `qcut system project info` | Project ops grouping |
| `youtube:upload` | `qcut system publish youtube` | Explicit publishing namespace |

## Concrete Migration Examples

```bash
# Old
bun run pipeline create-video -m kling_2_6_pro -t "Ocean waves" -d 5s
# New
qcut gen video --model kling_2_6_pro --prompt "Ocean waves" --duration 5s

# Old
bun run pipeline vimax:idea2video --idea "A detective in 1920s Paris" -d 120
# New
qcut flow idea2video --idea "A detective in 1920s Paris" --duration 120

# Old
bun run pipeline list-video-models --json
# New
qcut system models list --type video --json
```

## Backward Compatibility Strategy

1. **Alias window (recommended: 2 minor versions)**
   - old commands remain executable, emit `DEPRECATED` warning plus exact replacement
2. **Deprecation phasing**
   - v1.x: warnings only  
   - v2.0: legacy commands off by default (`QCUT_ENABLE_LEGACY=1` temporary escape hatch)
3. **Semantic versioning discipline**
   - add new command surface: minor  
   - remove legacy aliases: major
4. **Script migration helper**
   - `qcut system doctor --rewrite-cli path/to/script.sh` outputs patch suggestions

## Agent-First Output Conventions

### 1) Stable JSON envelope

```json
{
  "status": "ok",
  "command": "qcut gen video",
  "command_id": "cmd-...",
  "duration_ms": 1234,
  "data": {},
  "error": null
}
```

### 2) Standardized exit codes

- `0` success
- `2` invalid args
- `3` model not found
- `4` missing credentials
- `5` upstream API failure
- `6` pipeline execution failure
- `7` input file not found
- `9` timeout

### 3) Deterministic logs

- `stdout`: result payload only (JSON or requested output)
- `stderr`: progress and diagnostics (optional JSONL)
- `--quiet`: no noisy progress output for batch agent runs

## 2-Week Rollout Plan

### Week 1 (Architecture + Alias)

- Implement new command tree (`gen/analyze/audio/edit/flow/system`)
- Add aliases for all legacy commands with deprecation notices
- Normalize key parameter names (`--text` and `--prompt` policy)
- Run regression tests for both old and new command paths

### Week 2 (Docs + Telemetry + Cleanup)

- Publish migration guide (full mapping + copy/paste replacements)
- Add telemetry metric `legacy_command_usage`
- Add output stability tests (JSON schema snapshots)
- Remove duplicated help entries and inconsistent docs branches

## Risks and Mitigations

1. **Risk: script breakage**  
   Mitigation: aliases, no immediate removals, doctor rewrite support
2. **Risk: short-term relearning friction**  
   Mitigation: `qcut system quickstart` and inline command suggestions
3. **Risk: docs drift from implementation**  
   Mitigation: generate docs from help metadata + CI check
4. **Risk: unstable agent parsing**  
   Mitigation: frozen JSON schema + golden test fixtures

## What to Borrow from MiniMax vs What NOT to Copy

**Borrow:**

- Resource-first grouping with constrained action verbs
- Separated auth/config/quota control-plane
- Async task pattern for generation workflows
- Strong machine-readable output conventions

**Do not copy blindly:**

- Do not flatten QCut’s deep orchestration into shallow "generate-only" commands
- Do not sacrifice ViMax/YAML composability for superficial minimalism
- Do not optimize only demo paths while neglecting production needs (batching, retries, traceability)

## 🦞 Lobster verdict

QCut does not need to become smaller. It needs to become cleaner.

Adopt MiniMax-style command IA (resource + action) for the surface, while preserving QCut’s production depth in ViMax, YAML orchestration, editing, and project operations. That gives a better learning curve for humans and a more reliable execution graph for agents.

Start the 2-week refactor now: unify command surface first, then keep improving internals.

## Sources

1. QCut CLI Reference: https://quriosity.com.au/cli.html
2. MiniMax CLI README: https://github.com/MiniMax-AI/cli
3. MiniMax CLI README (raw): https://raw.githubusercontent.com/MiniMax-AI/cli/main/README.md
