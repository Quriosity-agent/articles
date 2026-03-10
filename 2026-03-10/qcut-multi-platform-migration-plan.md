# QCut 多平台架构迁移路线图（Desktop / Web / iPad）

> 目标：在不打断桌面版本发布节奏的前提下，把现有 QCut 从“Electron 单体运行”演进到“核心能力可复用、平台壳可替换”的架构，为 Web 与 iPad/移动端铺路。

## 一、现状判断：不是重写，而是有序拆分

根据当前代码结构与依赖关系：

- `apps/web`：React + Vite 前端，目前由 Electron Desktop 加载
- `electron/`：主进程 + preload + 大量 IPC handlers
- `packages/*`：已有 `auth` / `db` / `license-server` / `qagent`，但 editor core 还未独立
- `scripts/check-boundaries.ts`：已具备 renderer 边界约束机制
- 前端中有 **300+** 处 `window.electronAPI` 引用

**结论**：
这不是 greenfield；但也不是不可拆。关键是按顺序做“边界冻结 → 核心抽离 → 适配层”，避免大爆炸式改造。

---

## 二、目录策略：保留主干，新增中间层

### 1) 保留（不动主路径）

- `apps/web`
- `electron`
- `packages/auth`
- `packages/db`
- `packages/license-server`

### 2) 新增（本次迁移关键）

- `packages/editor-core`（平台无关核心业务与状态）
- `packages/platform-desktop`（Desktop 适配器）
- `packages/platform-web`（Web 适配器）
- `packages/ui-editor`（可选，沉淀纯 UI 组件）

### 3) 本轮降优先级（避免干扰主线）

- `apps/transcription`
- `packages/qagent`
- `packages/video-agent-skill`

---

## 三、五阶段执行计划（7–11 周）

## Phase 0（1 周）：冻结边界

**目标**：停止架构“继续长歪”，给后续抽离创造稳定面。

**关键动作**：
- 扩展 `check-boundaries` 规则：禁止新增跨层直连、禁止新增裸 `window.electronAPI` 访问
- 建立“平台能力清单”（文件、窗口、系统、授权、更新等）
- 对 300+ `window.electronAPI` 调用做分类盘点（高频/低频、可替代/不可替代）

**验收标准**：
- CI 能阻止新增违规边界调用
- 形成可追踪的调用映射清单

## Phase 1（1–2 周）：抽离核心数据层

**目标**：把编辑器核心状态与业务逻辑从 Electron 绑定中解耦。

**关键动作**：
- 创建 `packages/editor-core`
- 抽出文档模型、时间线状态、命令/历史等纯业务能力
- 用依赖注入替代直接平台调用

**验收标准**：
- `editor-core` 可在 node/jsdom 下跑单元测试
- 核心逻辑不再直接 import Electron API

## Phase 2（1–2 周）：建立平台适配层

**目标**：将“能力调用”从 UI 中抽到 adapter，切断前端对 `window.electronAPI` 的直接依赖。

**关键动作**：
- 定义统一 `PlatformAPI` 接口
- 落地 `platform-desktop`（桥接 Electron IPC）
- 落地 `platform-web`（浏览器环境实现，先 stub 后完善）
- 逐步替换前端中的直接调用

**验收标准**：
- 新代码 100% 通过 adapter 调用平台能力
- 历史高频路径完成第一批替换（建议先覆盖 30%+ 调用点）

## Phase 3（2–4 周）：Web Shell MVP（QCut Lite）

**目标**：上线一个可用但范围受控的 Web 版本，验证架构可行性。

**关键动作**：
- 在 `apps/web` 里接入 `platform-web`
- 明确 Lite 功能边界：基础编辑、预览、项目打开保存（受限版）
- 补齐 web fallback（无本地文件系统能力时的降级路径）

**验收标准**：
- QCut Lite 可在主流浏览器稳定运行
- 桌面版功能不回退，发布节奏不中断

## Phase 4（1–2 周）：iPad 优化

**目标**：在已有 Web 壳基础上适配触控与移动性能。

**关键动作**：
- 触控手势与交互热区优化
- 键盘/触控混合输入策略
- iPad Safari 性能与内存专项优化

**验收标准**：
- iPad 端核心路径可用（打开、编辑、预览、导出/分享中的可支持部分）
- 关键交互无阻塞级体验问题

---

## 四、建议 Sprint Issue 拆分（可直接落 Jira/Linear）

### Sprint 1（Phase 0）
- [ARCH-001] 扩展 `check-boundaries`：禁止新增 renderer 越层访问
- [ARCH-002] 建立 `window.electronAPI` 调用清单与优先级矩阵
- [ARCH-003] 发布《平台能力接口草案 v0》

### Sprint 2（Phase 1）
- [CORE-001] 初始化 `packages/editor-core` 与测试框架
- [CORE-002] 抽离时间线状态管理
- [CORE-003] 抽离命令栈/撤销重做
- [CORE-004] 去除核心模块对 Electron 直接依赖

### Sprint 3（Phase 2）
- [PLAT-001] 定义 `PlatformAPI` TypeScript 接口
- [PLAT-002] 实现 `platform-desktop`（IPC adapter）
- [PLAT-003] 实现 `platform-web`（stub + fallback）
- [PLAT-004] 替换 Top 100 高频 `electronAPI` 调用

### Sprint 4-5（Phase 3）
- [WEB-001] Web Shell 路由与初始化流程
- [WEB-002] Lite 功能开关与能力矩阵
- [WEB-003] 浏览器兼容性与性能基线
- [WEB-004] 内测发布与反馈闭环

### Sprint 6（Phase 4）
- [IPAD-001] 触控手势优化
- [IPAD-002] iPad Safari 性能专项
- [IPAD-003] 移动端 UI 密度与可达性调整

---

## 五、主要风险与应对

1. **风险：迁移过程中拖慢桌面发版**  
   - 应对：双轨策略（feature flag + 小步合并），每周发布健康检查

2. **风险：300+ 调用点替换成本失控**  
   - 应对：按业务价值排序，先替换高频路径，长尾调用延后

3. **风险：Web 与 Desktop 行为不一致**  
   - 应对：统一 `PlatformAPI` 契约测试 + 关键流程端到端测试

4. **风险：团队误解为“重写 Electron”**  
   - 应对：明确 guardrail：**不重写 Electron，只做 adapterization**

5. **风险：iPad 体验受限于 Web 能力边界**  
   - 应对：先定义 Lite 能力上限，再做交互与性能优化，不承诺超范围能力

---

## 六、执行护栏（必须坚持）

- 保持 Desktop release train 稳定
- 所有改动小步、可回滚、可观测
- 不做激进重构，不推倒重来
- Web 第一阶段明确定位为 **QCut Lite**

这条路线的核心，不是“最快上线 Web”，而是建立可持续的跨平台工程系统：一次抽离，长期复用，持续交付。

🦞
