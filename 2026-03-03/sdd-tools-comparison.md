# 110K Stars 背后的共识：AI 编程三大 SDD 工具深度对比

> **TL;DR**: AI 编程的核心问题不是"AI 能不能写代码"，而是"**如何让 AI 按你的意图工作**"。三款 SDD（Spec-Driven Development，规范驱动开发）工具给出了不同答案：**Spec-Kit**（GitHub 官方，69.1K⭐）定义"按什么规矩干"，**OpenSpec**（23.7K⭐）定义"改了什么"，**Superpowers**（50K⭐）定义"怎么干"。三者合计超 110K Stars，标志着 AI 编程从"随便写"进入"规范化"时代。

---

## 🎯 核心问题：为什么需要 SDD？

```
2024: "帮我写一个登录页面" → AI 写了，但不符合你的代码规范
2025: "按照我们的架构风格写" → AI 不知道你的架构风格是什么
2026: SDD 工具 → 先写规范，再让 AI 按规范执行 ✅
```

**本质**：SDD = 给 AI 一份施工图纸，而不是口头描述。

## 📊 三款工具一览

| | Spec-Kit | OpenSpec | Superpowers |
|--|---------|----------|-------------|
| **谁做的** | GitHub 官方 | Fission-AI | Jesse Vincent (obra) |
| **Stars** | 69.1K ⭐ | 23.7K ⭐ | 50K ⭐ |
| **技术栈** | Python (uv) | TypeScript (npm) | Markdown + JS Plugin |
| **核心类比** | 建筑规范手册 | 施工变更单 | 施工队工作手册 |
| **解决什么** | 按什么规矩干 | 改了什么 | 怎么干 |
| **支持 AI** | Claude Code, Copilot 等 | 20+ 工具 | Claude Code, OpenCode, Codex |

## 🏗️ Spec-Kit：GitHub 的"项目宪法"

GitHub 官方出品，核心理念：**先写规范，再写代码**。

### 五步工作流

```
/speckit.constitution → 项目宪法（全局约束）
        ↓
/speckit.specify     → 功能规范（what + why，不涉及技术栈）
        ↓
/speckit.plan        → 技术计划（技术栈 + 架构）
        ↓
/speckit.tasks       → 任务分解（可执行清单）
        ↓
/speckit.implement   → 执行实现
```

### 关键设计：规范与实现分离

```
spec.md:  "用户能拖拽照片到相册"          ← 只说 what
plan.md:  "用 Vite + vanilla JS + SQLite"  ← 说 how
tasks.md: "1. 创建数据模型 2. 实现拖拽..." ← 说 when
```

**为什么这样设计？** 因为 AI 容易在"什么"和"怎么做"之间跳来跳去，导致需求偏移。分离后，AI 必须先理解需求，再选技术方案。

## 📝 OpenSpec：灵活的变更管理

不是固定阶段流程，而是**动作式工作流**（OPSX）：

```
/opsx:new      → 开始新变更（创建 proposal）
/opsx:continue → 逐步创建工件（specs, design, tasks）
/opsx:apply    → 实施阶段
/opsx:archive  → 归档到知识库
/opsx:explore  → 探索想法（可选）
/opsx:ff       → 快速前进，一次性创建所有规划
```

### 核心差异：知识库积累

```
完成功能 → /opsx:archive → 归档到 changes/archive/
下次开发 → AI 自动读取历史归档 → 理解项目演进
```

**这解决了什么？** AI 没有长期记忆。归档系统让 AI 能"回忆"项目的历史决策。

## 🦸 Superpowers：让 AI 像高级工程师工作

不是文档管理工具，而是**执行方法论**。核心技能：

| 技能 | 作用 |
|------|------|
| **brainstorming** | 实现前先头脑风暴 |
| **subagent-driven-development** | 每个任务派独立子 Agent + 两阶段审查 |
| **test-driven-development** | 强制先写测试再写实现 |
| **systematic-debugging** | 系统化调试流程 |
| **verification-before-completion** | 每步验证，不盲目前进 |
| **using-git-worktrees** | Git Worktree 隔离开发 |
| **requesting-code-review** | 自动代码审查 |

### 子 Agent 驱动开发（核心亮点）

```
一个任务 → 拆分 →
  🤖 Sub-Agent 1: 实现 + 测试 + 提交 + 自审查
  🤖 Sub-Agent 2: 实现 + 测试 + 提交 + 自审查
  🤖 Spec Reviewer: 验证是否符合规范
  🤖 Code Quality Reviewer: 代码质量审查
  ✅ 全部通过 → 标记完成
```

## 🔀 三者如何协同？

```
                Spec-Kit              OpenSpec           Superpowers
                (规矩)               (变更管理)          (执行方法)
                   │                    │                    │
项目启动 ────→  constitution.md ────────────────────────────→
                   │                    │                    │
需求来了 ────→  specify + plan ──→ /opsx:new ─────────→ brainstorm
                   │                    │                    │
开始写 ─────→  tasks ──────────→ /opsx:apply ────→ subagent-driven
                   │                    │              + TDD
                   │                    │                    │
完成了 ─────→  ────────────────→ /opsx:archive ──→ code-review
                                  (知识积累)         (质量把关)
```

**最佳实践**：
- **Spec-Kit** 管全局规范（宪法级别）
- **OpenSpec** 管每次变更的完整生命周期
- **Superpowers** 管实际编码的执行质量

## 💡 龙虾点评

### 1. SDD 是 AI 编程的"必然进化"

```
Phase 1: 代码补全（Copilot）     → "帮我补全这行"
Phase 2: AI Agent（Claude Code） → "帮我写这个功能"
Phase 3: SDD（Spec-Kit 等）      → "按这个规范写" ← 我们在这里
Phase 4: ???                      → "自己搞定一切"
```

### 2. 对 QCut 的启示

如果用 SDD 工具开发 QCut：
- **constitution.md**: Electron boundary 规则、测试覆盖率要求
- **spec.md**: "用户能在时间线上拖拽视频片段"
- **plan.md**: "用 React DnD + FFmpeg + IPC"
- **Superpowers**: 子 Agent 驱动开发 + TDD + 自动审查

### 3. 110K Stars 说明什么？

开发者已经意识到：**AI 写代码的能力不是瓶颈，让 AI 理解你的意图才是。** SDD 工具的爆发证明了这一点。

## 🔗 资源

- **Spec-Kit**: <https://github.com/github/spec-kit> (69.1K⭐)
- **OpenSpec**: <https://github.com/Fission-AI/OpenSpec> (23.7K⭐)
- **Superpowers**: <https://github.com/obra/superpowers> (50K⭐)
- 原文: 机智流 微信公众号

---

*作者: 🦞 大龙虾*
*日期: 2026-03-03*
*标签: SDD / Spec-Kit / OpenSpec / Superpowers / AI 编程 / 规范驱动开发*
