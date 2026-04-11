# QCut CLI Refactor: Code Locations, Impact Surface, and Migration Plan

- Author: 🦞 龙虾侦探 / Lobster Detective
- Date: 2026-04-11
- Tags: QCut, CLI, refactor, command-compatibility, migration, TypeScript

## TL;DR

If QCut CLI naming changes from flat commands (for example `create-video`) to grouped commands (for example `gen video`), the critical changes are in **CLI entry parsing, command registry, dispatch routing, and help output**.

Execution internals (`execution/*`) and model/provider internals (`registry-data/*`, `infra/*`) usually should not change just because command names changed, as long as normalized canonical options remain stable.

Recommended migration architecture:
1. **Hierarchical Command Map** for new syntax (`gen video -> create-video`).
2. **Legacy Alias Adapter** for old syntax with deprecation warnings.

---

## 1) What code must change when CLI naming/architecture changes?

### A. CLI entry and dispatch (highest priority)

#### `electron/native-pipeline/cli/cli.ts`
- Responsibility: process entrypoint, arg parsing (`parseCliArgs`), command validation, execution setup.
- Must change:
  - Add command resolution before validation (map `gen video` to canonical command).
  - Validate against canonical command, not raw token only.
  - Capture whether invocation came from legacy syntax for warnings/telemetry.

#### `electron/native-pipeline/cli/cli-runner.ts`
- Responsibility: barrel re-export of runner APIs.
- Must change:
  - Usually minimal; update exports only if new alias/normalizer utilities are shared.

#### `electron/native-pipeline/cli/command-registry.ts`
- Responsibility: single source of truth for commands, categories, flags, examples.
- Must change:
  - If canonical command names change, update registry keys, categories, and examples.
  - If canonical names stay, keep keys and add router/alias mapping layer externally.

#### `electron/native-pipeline/cli/command-registry-types.ts`
- Responsibility: command metadata types.
- Must change:
  - Extend `CommandDef` if adding typed metadata such as `deprecated`, `aliases`, `replacement`.

#### `electron/native-pipeline/cli/cli-help.ts`
- Responsibility: `--help` text and JSON help envelopes.
- Must change:
  - Show grouped command UX (`gen`, `flow`, `system`) as primary.
  - Keep legacy list in a dedicated section or `--help-legacy`.
  - Update examples to new syntax.

#### `electron/native-pipeline/cli/interactive.ts`
- Responsibility: confirmation prompts and stdin handling.
- Must change:
  - Usually no core changes needed for naming refactor.

---

### B. CLI handler layer (second priority)

#### `electron/native-pipeline/cli/cli-handlers-*.ts`
- Responsibility: domain handlers (media, speech, editor, subtitle, phota, etc.).
- Impact:
  - Usually unchanged for pure naming migration.
  - Must update if semantic meaning/default behavior changes.

#### `electron/native-pipeline/cli/cli-runner/handler-*.ts`
- Responsibility: generation/pipeline/transfer/upscale dispatch handlers.
- Impact:
  - `handler-generate.ts` has explicit command branching (`generate-image`, `create-video`, `generate-avatar`), so canonical rename requires updates.

#### `electron/native-pipeline/cli/vimax-cli-handlers/**/*.ts`
- Responsibility: ViMax workflows.
- Impact:
  - If ViMax command family is regrouped (for example under `flow`), routing/help changes are needed, while algorithmic internals may remain unchanged.

---

### C. Pipeline execution layer (third priority, only for semantic changes)

#### `electron/native-pipeline/execution/*.ts`
- Responsibility: chain execution, retries, type transitions, parallel execution.
- Impact:
  - Command renaming alone should not require changes.
  - Option shape normalization changes may affect payload shaping in `step-executors.ts`.

#### `electron/native-pipeline/registry-data/*.ts`
- Responsibility: model registrations/defaults.
- Impact:
  - Usually unchanged for command naming only.
  - Update when migration introduces new default model/feature behavior.

---

### D. Infra/config/provider abstraction (fourth priority)

#### `electron/native-pipeline/infra/*.ts`
- Responsibility: API calls, key management, proxy, costs, registry abstraction.
- Impact:
  - Naming-only refactors generally do not touch provider calling logic.
  - If normalized command options alter payload conventions, update at `step-executors.ts` + `api-caller.ts` boundary.

#### `electron/native-pipeline/registry-data/platform-models.ts`
- Responsibility: platform model registration (Runway/HeyGen/D-ID/Synthesia/Phota).
- Impact:
  - Change only if migration also changes model policy/defaults.

---

## 2) Exact file locations in the QCut repo

Repo root: `/Users/peter/Desktop/code/qcut/qcut`

### CLI entry/dispatch
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/cli/cli.ts`
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/cli/cli-runner.ts`
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/cli/command-registry.ts`
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/cli/command-registry-types.ts`
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/cli/cli-help.ts`
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/cli/interactive.ts`

### CLI handlers
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/cli/cli-handlers-*.ts`
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/cli/cli-runner/handler-*.ts`
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/cli/vimax-cli-handlers/**/*.ts`

### Pipeline execution
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/execution/*.ts`
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/registry-data/*.ts`

### Infra/config/provider abstraction
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/infra/*.ts`
- `/Users/peter/Desktop/code/qcut/qcut/electron/native-pipeline/registry-data/platform-models.ts`

---

## Compatibility layer points: where to add aliases, warnings, and normalization

### [New] Suggested files
- `electron/native-pipeline/cli/aliases.ts`
  - `resolveCommand(argv)` for grouped syntax + legacy aliases.
  - `warnIfDeprecated(...)` for legacy flat commands.

- `electron/native-pipeline/cli/option-normalizer.ts`
  - `normalizeOptions(options)` for old/new flag compatibility (`--prompt`/`--text`, etc.).

### Hook points
1. **Command normalization**: at the start of `parseCliArgs()` in `cli.ts`.
2. **Session normalization**: inside `parseSessionLine()` in `cli-runner/session.ts`.
3. **Deprecation warning emission**:
   - Single run: in `main()` in `cli.ts` after parsing, before `runner.run()`.
   - Session mode: per command line in `runSession()`.
4. **Option normalization**:
   - Post parse in `cli.ts` before returning `CLIRunOptions`.
   - Post parse in `session.ts` before building final options.

---

## Migration architecture (Hierarchical Command Map + Legacy Alias Adapter)

1. Router resolves user syntax first:
   - `gen video` → canonical `create-video`
   - `gen image` → canonical `generate-image`
2. Legacy adapter accepts old commands:
   - old command still executes but gets deprecation warning.
3. Runner and handlers receive only canonical commands.
4. Help uses dual tracks:
   - modern syntax by default,
   - legacy syntax in `--help-legacy`.

---

## Checklist: code changes vs docs changes

### Code changes (required)
- [ ] `cli.ts`: command resolution + normalization
- [ ] `command-registry.ts`: command metadata/category/examples alignment
- [ ] `cli-help.ts`: help text/json updates
- [ ] `cli-runner/runner.ts`: switch dispatch aligned to canonical names
- [ ] `cli-runner/handler-generate.ts`: command branch updates
- [ ] `cli-runner/session.ts`: session parser normalization
- [ ] Add `aliases.ts` (legacy adapter + warning)
- [ ] Add `option-normalizer.ts` (flag compatibility)

### Docs changes (required)
- [ ] `docs/technical/guides/build-commands.md`
- [ ] `docs/technical/architecture/source-code-structure.md`
- [ ] Internal docs/examples containing old flat command syntax
- [ ] External public page: `https://quriosity.com.au/cli.html` (syntax, migration timeline, deprecation notice)

---

## 1-week implementation plan

- **Day 1**: Implement `aliases.ts` + `option-normalizer.ts`, wire into `cli.ts` and `session.ts`.
- **Day 2**: Update `command-registry.ts` and `cli-help.ts` for grouped UX.
- **Day 3**: Align `runner.ts` and `handler-generate.ts` canonical command handling.
- **Day 4**: Add tests for alias routing, warning behavior, JSON-noise safety, backward compatibility.
- **Day 5**: Update repo docs and migration guide.
- **Day 6**: Sync external docs (`https://quriosity.com.au/cli.html`) and release notes.
- **Day 7**: Roll out gradually, monitor command failure rates and syntax adoption.

---

## Risks + rollback plan

### Risks
1. Session mode and one-shot mode diverge in resolution behavior.
2. Warnings pollute JSON stdout and break machine consumers.
3. Docs lag behind code and cause operator confusion.
4. Hidden hardcoded command checks remain in handlers.

### Rollback
1. Keep feature flag like `LEGACY_COMMANDS_ENABLED=true`.
2. Allow router to fall back to flat commands only.
3. Roll back help defaults while keeping internal compatibility.
4. If post-release failure spikes, hotfix to previous command parsing behavior.

---

## 🦞 Lobster verdict

The key is not renaming strings, it is separating **syntax migration** from **execution semantics**.

Safest path:
- keep runner/handler/execution semantics stable,
- migrate at router/alias/help layer,
- ship with compatibility windows and clear deprecation messaging.

In short: **compat first, migrate second, retire last.**
