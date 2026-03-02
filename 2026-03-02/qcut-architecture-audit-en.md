# QCut Electron Architecture Layer Violation Audit Report

> Audit Date: 2026-03-02
> Project Path: `C:\Users\yanie\Desktop\qcut-fresh\qcut`

## 1. Architecture Assessment

### Overall Rating: ⭐⭐⭐⭐ (4/5) — Well-designed architecture with minor violations

QCut's Electron architecture layering is **quite good**:

- **Main process** (`electron/`) — Clean separation, 22 IPC handler files, FFmpeg, Claude integration
- **Renderer process** (`apps/web/src/`) — Accesses main via `window.electronAPI`
- **Preload bridge** (`electron/preload.ts` + `electron/preload-integrations.ts`) — Proper `contextBridge` isolation
- **Type definitions** — Dual types: `electron/preload-types/` (main-side) + `apps/web/src/types/electron/` (renderer-side, 24 files)

**Highlights:**
- Preload correctly uses `contextBridge.exposeInMainWorld`
- Complete `ElectronAPI` type definitions on renderer side
- CLAUDE.md explicitly states "Use Electron IPC for backend functionality"
- Component validator actively detects and rejects Electron/Node access

---

## 2. Violations Found

### 🔴 Violation 1: Direct `require('electron')` in Renderer — blog.tsx

**File:** `apps/web/src/routes/blog.tsx`, lines 14-16

```typescript
if (typeof window !== "undefined" && window.require) {
    const { shell } = window.require("electron");
    shell.openExternal("https://github.com/donghaozhang/qcut");
}
```

**Problem:** Bypasses preload bridge, relies on `nodeIntegration: true` (security risk), violates project's own CLAUDE.md.

**Fix:** Use `window.electronAPI?.openExternal(url)`

---

### 🟡 Violation 2: `process.env` in Renderer Code

CLAUDE.md says **"Don't use `process.env` in client code (use `import.meta.env`)"**, but 6 files still use it:

| File | Line | Usage |
|------|------|-------|
| `text2image.tsx` | 59 | `process.env.NODE_ENV === "development"` |
| `StickerElement.tsx` | 236 | `process.env.NODE_ENV === "development"` |
| `features.ts` | 67 | `process.env.NODE_ENV === "development"` |
| `zip-manager.ts` | 5 | `process.env.NODE_ENV === "development"` |
| `export-engine-remotion.ts` | 123 | `process.env` access |
| `debug-sticker-overlay.ts` | 120 | `process.env.NODE_ENV` |

**Severity:** Medium. Functionally works (Vite replaces statically), but AI agents will copy this pattern.

---

### 🟢 No Reverse Dependencies

No imports from `apps/web/src/` found in `electron/` directory. Clean separation confirmed.

---

## 3. Missing Architecture Guards

1. **No linter rules** enforcing Electron boundaries — no `no-restricted-imports` for electron in renderer
2. **No import restriction rules** — nothing prevents renderer from importing electron modules
3. **Type definitions split across two locations** — manual sync required, no automated verification

---

## 4. Recommendations

### A. Immediate Fixes (5 min)

1. Fix `blog.tsx`: Replace `window.require("electron")` with `window.electronAPI?.openExternal()`
2. Replace all `process.env.NODE_ENV` with `import.meta.env.DEV` (6 files)

### B. Add Linter Rules (30 min)

```javascript
// eslint.config.js (for apps/web/src/ only)
{
  files: ["apps/web/src/**/*.{ts,tsx}"],
  rules: {
    "no-restricted-imports": ["error", {
      patterns: [{
        group: ["electron", "electron/*"],
        message: "Renderer must not import electron directly. Use window.electronAPI"
      }]
    }],
    "no-restricted-syntax": ["error", {
      selector: "CallExpression[callee.object.name='window'][callee.property.name='require']",
      message: "Do not use window.require(). Use preload bridge instead."
    }]
  }
}
```

### C. Update CLAUDE.md (10 min)

Add explicit prohibitions with correct/incorrect examples.

### D. CI Check (15 min)

Add GitHub Actions workflow to grep for electron imports in renderer code.

---

## 5. Impact on AI Agents (Claude Code)

### Current Problems
- **Bad example pollution**: `blog.tsx`'s `window.require('electron')` will be learned and copied
- **Spec vs code mismatch**: CLAUDE.md says IPC, but code has counterexamples — AI gets confused
- **No automated detection**: Violations pass CI silently

### After Improvements
- CLAUDE.md with explicit bans → AI follows correct patterns
- Linter rules → AI gets immediate error feedback, self-corrects
- Remove bad examples → AI no longer sees wrong patterns to imitate

### Key Insight

> AI agents learn project patterns from two sources: **existing code** and **CLAUDE.md/AGENTS.md**.
> When they contradict, AI tends to follow existing code (because "code in use" is more convincing).
> **Fixing existing violations matters more than writing more documentation.**

---

## 6. Summary

| Dimension | Status | Action |
|-----------|--------|--------|
| Main/Renderer separation | ✅ Good | Keep |
| Preload bridge | ✅ Proper | Keep |
| Direct electron access | ❌ 1 violation | Fix blog.tsx |
| process.env usage | ⚠️ 6 non-compliant | Replace with import.meta.env |
| Linter rules | ❌ Missing | Add no-restricted-imports |
| CLAUDE.md guidance | ⚠️ Not specific enough | Add explicit bans |
| CI checks | ❌ None | Add architecture check |
| Type sync | ⚠️ Manual | Consider shared type package |

**Overall:** QCut's architecture is well-designed but lacks automated guards. For AI-assisted development, these guards are critical — AI won't "intuitively" know what not to do; it needs explicit rules and immediate feedback.
