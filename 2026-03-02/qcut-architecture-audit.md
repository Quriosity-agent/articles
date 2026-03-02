# QCut Electron 架构层级违规审计报告

> 审计日期：2026-03-02
> 项目路径：`C:\Users\yanie\Desktop\qcut-fresh\qcut`

## 一、当前架构状态评估

### 整体评价：⭐⭐⭐⭐ (4/5) — 架构设计良好，存在少量违规

QCut 的 Electron 架构分层做得 **相当不错**：

- **Main 进程** (`electron/`) — 清晰独立，包含 22 个 IPC handler 文件、FFmpeg 处理、Claude 集成等
- **Renderer 进程** (`apps/web/src/`) — 通过 `window.electronAPI` 访问主进程功能
- **Preload 桥接层** (`electron/preload.ts` + `electron/preload-integrations.ts`) — 使用 `contextBridge` 安全暴露 API
- **类型定义** — 双向类型：
  - `electron/preload-types/` — 主进程侧类型
  - `apps/web/src/types/electron/` — Renderer 侧类型（24 个文件，按功能分组）

**亮点：**
- Preload 使用 `contextBridge.exposeInMainWorld` 正确隔离
- Renderer 侧有完整的 `ElectronAPI` 类型定义
- CLAUDE.md 明确写了 "Use Electron IPC for backend functionality"
- 组件验证器 (`component-validator`) 主动检测并拒绝 Electron/Node 访问

---

## 二、发现的具体违规

### 🔴 违规 1：Renderer 直接 `require('electron')` — blog.tsx

**文件：** `apps/web/src/routes/blog.tsx`，第 14-16 行

```typescript
if (typeof window !== "undefined" && window.require) {
    const { shell } = window.require("electron");
    shell.openExternal("https://github.com/donghaozhang/qcut");
}
```

**问题：**
- 绕过 preload 桥接层，直接在 renderer 进程中 `require('electron')`
- 这依赖 `nodeIntegration: true` 或 `contextIsolation: false`（安全隐患）
- 违反项目自己的 CLAUDE.md 规范（"Use Electron IPC for backend functionality"）

**修复方案：** 应通过 `window.electronAPI.openExternal(url)` 调用

---

### 🟡 违规 2：Renderer 代码中使用 `process.env`

CLAUDE.md 明确说 **"Don't use `process.env` in client code (use `import.meta.env`)"**，以下文件仍直接使用 `process.env`：

| 文件 | 行号 | 用法 |
|------|------|------|
| `apps/web/src/components/editor/media-panel/views/text2image.tsx` | 59 | `process.env.NODE_ENV === "development"` |
| `apps/web/src/components/editor/stickers-overlay/StickerElement.tsx` | 236 | `process.env.NODE_ENV === "development"` |
| `apps/web/src/config/features.ts` | 67 | `process.env.NODE_ENV === "development"` |
| `apps/web/src/lib/project/zip-manager.ts` | 5 | `process.env.NODE_ENV === "development"` |
| `apps/web/src/lib/remotion/export-engine-remotion.ts` | 123 | `process.env` 访问 |
| `apps/web/src/lib/stickers/debug-sticker-overlay.ts` | 120 | `process.env.NODE_ENV` |

**严重程度：** 中等。`process.env.NODE_ENV` 在 Vite 中会被静态替换，功能上没问题，但：
- 不符合项目规范
- AI agent 看到这些代码会认为 `process.env` 是可接受的模式并模仿
- 应统一使用 `import.meta.env.DEV` 或 `import.meta.env.MODE`

---

### 🟢 测试代码中的 `require` 用法（非违规，但需注意）

以下文件在测试中使用 `require`，属于测试 mock/fixture，不是真正的违规：

- `component-validator.test.ts:405` — 测试组件验证器能否检测到 `require('electron')` 并拒绝（正面的安全检测！）
- 多个 E2E 测试文件中使用 `require('fs')` 等

---

### 🟢 无违规：Main → Renderer 反向依赖

检查了 `electron/` 目录下所有 `.ts` 文件，**没有发现**从 `apps/web/src/` 导入的情况。主进程和渲染进程之间没有反向依赖。

---

## 三、缺失的架构守卫

### 1. 没有 Linter 规则强制 Electron 边界

**当前状态：**
- 根目录无 ESLint 配置（仅 `packages/qagent/eslint.config.js` 有局部 ESLint）
- 无 `biome.json`
- 使用 Ultracite（在 AGENTS.md 中提到规则），但没有自定义规则限制跨层导入
- **没有任何自动化工具**阻止 renderer 代码 `import` 或 `require` electron 模块

### 2. 没有 Import 限制规则

缺少：
- `no-restricted-imports` 禁止 `apps/web/src/` 中导入 `electron`
- `no-restricted-globals` 禁止 renderer 中使用 `require`

### 3. 类型定义分散在两处

- `electron/preload-types/` — 主进程侧
- `apps/web/src/types/electron/` — Renderer 侧

这两套类型需要手动保持同步，没有自动验证机制。

---

## 四、推荐的改进措施

### A. 立即修复（5 分钟）

**1. 修复 `blog.tsx` 的直接 electron 访问：**
```typescript
// 修改前
const { shell } = window.require("electron");
shell.openExternal("https://github.com/donghaozhang/qcut");

// 修改后
window.electronAPI?.openExternal("https://github.com/donghaozhang/qcut");
```

**2. 替换 `process.env.NODE_ENV` 为 `import.meta.env.DEV`：**
全局查找替换，6 个文件。

### B. 添加 Linter 规则（30 分钟）

在项目根目录添加 ESLint 配置，或在现有 Ultracite 配置中加入：

```javascript
// eslint.config.js (仅针对 apps/web/src/)
{
  files: ["apps/web/src/**/*.{ts,tsx}"],
  rules: {
    "no-restricted-imports": ["error", {
      patterns: [{
        group: ["electron", "electron/*"],
        message: "Renderer 进程不能直接导入 electron，请使用 window.electronAPI"
      }]
    }],
    "no-restricted-syntax": ["error", {
      selector: "CallExpression[callee.object.name='window'][callee.property.name='require']",
      message: "不要使用 window.require()，请通过 preload 桥接层访问"
    }, {
      selector: "MemberExpression[object.object.name='process'][object.property.name='env']",
      message: "Renderer 中请使用 import.meta.env 而非 process.env"
    }]
  }
}
```

### C. 更新 CLAUDE.md 添加明确禁令（10 分钟）

在 `Architecture Guidelines > DON'T` 部分添加：

```markdown
### DON'T
- ❌ `require('electron')` or `window.require('electron')` in renderer code
- ❌ `import` anything from `electron` package in `apps/web/src/`
- ❌ Use `process.env` in renderer (use `import.meta.env`)
- ❌ Import from `electron/` directory in renderer code
- ❌ Access `ipcRenderer` directly — all IPC must go through `window.electronAPI`

### Correct Pattern
// ✅ 正确：通过 preload 桥接
window.electronAPI?.openExternal(url)
window.electronAPI?.sounds.search(params)

// ❌ 错误：直接访问 electron
const { shell } = window.require('electron')
import { ipcRenderer } from 'electron'
```

### D. 添加 CI 检查（可选，15 分钟）

```yaml
# .github/workflows/architecture-check.yml
- name: Check electron boundary violations
  run: |
    if grep -r "require('electron')\|from 'electron'" apps/web/src/ --include="*.ts" --include="*.tsx" | grep -v "__tests__" | grep -v "test/"; then
      echo "❌ Found electron imports in renderer code!"
      exit 1
    fi
```

---

## 五、对 AI Agent（Claude Code）的影响

### 当前问题

1. **坏示例污染**：`blog.tsx` 中的 `window.require('electron')` 会被 Claude Code 作为"已有模式"学习并复制到新代码中
2. **规范与代码不一致**：CLAUDE.md 说用 IPC，但代码中有反例，AI 会困惑哪个是对的
3. **缺少自动检测**：即使 CLAUDE.md 写了规范，没有 linter 检查 = AI 写的违规代码能通过 CI

### 改进后的效果

- **CLAUDE.md 加入明确禁令 + 正确示例** → AI 生成代码时会遵循正确模式
- **Linter 规则** → AI 写出违规代码时，`bun lint:clean` 会立即报错，AI 可以自动修复
- **消除坏示例** → AI 在项目上下文中不再看到错误模式，减少模仿概率
- **CI 检查** → 即使 AI 绕过 linter，PR 也会被拦截

### 关键认知

> AI agent 学习项目模式主要靠两个来源：**已有代码**和 **CLAUDE.md/AGENTS.md**。
> 当两者矛盾时，AI 倾向于跟随已有代码（因为"实际在用"的代码更有说服力）。
> 所以**修复已有违规比写更多规范文档更重要**。

---

## 六、总结

| 维度 | 状态 | 建议 |
|------|------|------|
| Main/Renderer 分层 | ✅ 良好 | 保持现状 |
| Preload 桥接 | ✅ 规范 | 保持现状 |
| 直接 electron 访问 | ❌ 1 处违规 | 修复 blog.tsx |
| process.env 使用 | ⚠️ 6 处不规范 | 替换为 import.meta.env |
| Linter 规则 | ❌ 缺失 | 添加 no-restricted-imports |
| CLAUDE.md 指导 | ⚠️ 不够具体 | 添加明确禁令和示例 |
| CI 检查 | ❌ 无 | 添加架构检查 workflow |
| 类型同步 | ⚠️ 手动 | 考虑共享类型包 |

**总体判断：** QCut 架构设计优秀，但缺少自动化守卫。对于有 AI agent 参与开发的项目，这些守卫尤为重要 ── 因为 AI 不会"凭直觉"知道什么不该做，它需要明确的规则和即时的反馈。
