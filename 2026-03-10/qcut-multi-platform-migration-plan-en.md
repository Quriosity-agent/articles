# QCut Multi-Platform Migration Roadmap (Desktop / Web / iPad)

> Goal: evolve QCut from an Electron-centered runtime into a reusable core + platform-shell architecture, without disrupting desktop release velocity.

## 1) Architecture Reality Check: Not Greenfield, But Very Feasible

Current state from the codebase:

- `apps/web`: React + Vite UI, currently loaded by Electron desktop
- `electron/`: main process + preload + many IPC handlers
- `packages/*`: includes `auth`, `db`, `license-server`, `qagent`; editor core is not yet independent
- `scripts/check-boundaries.ts`: already enforces renderer boundaries
- Frontend has **300+** references to `window.electronAPI`

**Conclusion:**
This is not a rewrite scenario. It is a structured separation problem. If we sequence the work correctly (boundary freeze → core extraction → adapters), the split is practical and low-risk.

---

## 2) Repository Strategy: Keep the Trunk, Add Platform Layers

### Keep (stable foundations)

- `apps/web`
- `electron`
- `packages/auth`
- `packages/db`
- `packages/license-server`

### Add (migration-critical)

- `packages/editor-core` (platform-agnostic editor domain/state)
- `packages/platform-desktop` (Desktop adapter)
- `packages/platform-web` (Web adapter)
- `packages/ui-editor` (optional shared editor UI components)

### Deprioritize for this migration

- `apps/transcription`
- `packages/qagent`
- `packages/video-agent-skill`

---

## 3) Phased Execution Plan (7–11 weeks)

## Phase 0 (1 week): Freeze Boundaries

**Objective:** stop architectural drift and create a safe migration surface.

**Actions:**
- Strengthen `check-boundaries` rules: block new cross-layer violations and new direct `window.electronAPI` usage
- Build a platform capability inventory (filesystem, windowing, system calls, licensing, updates)
- Classify all existing `window.electronAPI` calls by frequency and migration complexity

**Exit criteria:**
- CI blocks new boundary violations
- A tracked call-site inventory exists and is prioritized

## Phase 1 (1–2 weeks): Extract Core Data/Domain Layer

**Objective:** decouple editor logic from Electron-specific runtime assumptions.

**Actions:**
- Create `packages/editor-core`
- Move timeline/document state, command/history logic, and pure editor domain services
- Replace direct platform calls with dependency-injected capabilities

**Exit criteria:**
- `editor-core` runs unit tests independently (node/jsdom)
- Core modules have no direct Electron imports

## Phase 2 (1–2 weeks): Build Platform Adapter Layer

**Objective:** route platform access through adapters, not UI direct calls.

**Actions:**
- Define a unified `PlatformAPI` contract
- Implement `platform-desktop` (IPC-backed adapter)
- Implement `platform-web` (browser-safe implementation, with staged stubs/fallbacks)
- Start replacing direct frontend calls to `window.electronAPI`

**Exit criteria:**
- All new code uses adapter interfaces
- First migration wave completed on high-frequency paths (target 30%+ call-site coverage)

## Phase 3 (2–4 weeks): Ship Web Shell MVP (QCut Lite)

**Objective:** validate the architecture with a constrained but usable web product.

**Actions:**
- Wire `apps/web` to `platform-web`
- Define Lite scope clearly (core edit flows, preview, constrained project I/O)
- Implement graceful degradation where browser capabilities differ from desktop

**Exit criteria:**
- QCut Lite runs reliably in target browsers
- Desktop feature parity/regression baseline remains intact

## Phase 4 (1–2 weeks): iPad Optimization

**Objective:** optimize touch-first usage on top of the web shell.

**Actions:**
- Touch gestures and hit-target optimization
- Keyboard + touch interaction tuning
- iPad Safari performance/memory profiling and fixes

**Exit criteria:**
- Core iPad workflows are usable end-to-end
- No blocker-level UX/performance issues on primary paths

---

## 4) Suggested Sprint Issue Breakdown (Jira/Linear-ready)

### Sprint 1 (Phase 0)
- [ARCH-001] Enforce no-new direct renderer-to-electron calls via boundary checks
- [ARCH-002] Build and prioritize `window.electronAPI` usage matrix
- [ARCH-003] Publish Platform Capability Contract v0

### Sprint 2 (Phase 1)
- [CORE-001] Bootstrap `packages/editor-core` + test harness
- [CORE-002] Extract timeline state/services
- [CORE-003] Extract command stack (undo/redo)
- [CORE-004] Remove direct Electron coupling from core modules

### Sprint 3 (Phase 2)
- [PLAT-001] Define `PlatformAPI` TypeScript interfaces
- [PLAT-002] Implement `platform-desktop` IPC adapter
- [PLAT-003] Implement `platform-web` adapter + fallbacks
- [PLAT-004] Replace top 100 high-traffic `electronAPI` call-sites

### Sprint 4–5 (Phase 3)
- [WEB-001] Web shell bootstrap & runtime wiring
- [WEB-002] Lite feature flags + capability matrix
- [WEB-003] Browser compatibility + performance baseline
- [WEB-004] Internal beta rollout and feedback loop

### Sprint 6 (Phase 4)
- [IPAD-001] Touch interaction refinement
- [IPAD-002] iPad Safari performance pass
- [IPAD-003] Mobile density/accessibility adjustments

---

## 5) Key Risks and Mitigations

1. **Risk: Desktop release cadence gets disrupted**  
   - Mitigation: dual-track delivery, feature flags, weekly release health gate

2. **Risk: 300+ call-site migration balloons in scope**  
   - Mitigation: value-first sequencing (high-frequency first), defer long-tail paths

3. **Risk: Behavior divergence between Desktop and Web**  
   - Mitigation: shared `PlatformAPI` contract tests + critical-path E2E tests

4. **Risk: Team interprets this as an Electron rewrite**  
   - Mitigation: enforce guardrail messaging—**adapterization, not rewrite**

5. **Risk: iPad expectations exceed web capability envelope**  
   - Mitigation: define QCut Lite scope early and communicate non-goals explicitly

---

## 6) Non-Negotiable Guardrails

- Keep desktop release train stable
- Make small, reversible, observable changes
- No radical Electron rewrite; adapterize incrementally
- Position web as **QCut Lite** first, then expand

This roadmap optimizes for engineering continuity: progressive decoupling now, platform leverage later.

🦞
