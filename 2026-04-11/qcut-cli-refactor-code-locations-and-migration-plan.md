# QCut CLI 重构：命名变更影响面、代码定位与迁移方案

- Author: 🦞 龙虾侦探 / Lobster Detective
- Date: 2026-04-11
- Tags: QCut, CLI, 重构, 命令兼容, 迁移方案, TypeScript

## TL;DR

如果把 `create-video` 改成 `gen video` 这类分层命令，**最核心改动在 CLI 入口、命令注册表、路由分发和帮助系统**；执行层（`execution/*`）和模型层（`registry-data/*`、`infra/*`）通常不需要跟着改命令名本身，但需要保证参数规范化后的入参不变。

建议采用两层迁移架构：
1. **Hierarchical Command Map（新语法）**：`gen video -> create-video`。
2. **Legacy Alias Adapter（旧语法兼容）**：旧命令继续可用，输出弃用警告，2 个小版本后再移除。

---

## 1) 命名/架构变化时，必须改哪些代码？

### A. CLI 入口与分发（第一优先级）

#### `electron/native-pipeline/cli/cli.ts`
- 责任：CLI 进程入口，参数解析（`parseCliArgs`）、命令合法性校验、执行调度。
- 必改点：
  - 命令解析前引入别名/分层路由解析（例如 `gen video -> create-video`）。
  - 命令校验不能只看原始 `argv[0]`，要看“规范化后的 canonical command”。
  - 在这里记录“是否通过旧命令进入”，给 warning 输出使用。

#### `electron/native-pipeline/cli/cli-runner.ts`
- 责任：barrel 导出（`CLIPipelineRunner` 等），非主要逻辑改动点。
- 必改点：通常无需直接改逻辑，但若类型/导出新增 alias 工具，需要补导出。

#### `electron/native-pipeline/cli/command-registry.ts`
- 责任：命令定义单一真源（命令名、分类、flags、examples）。
- 必改点：
  - 若 canonical 命令名真的更换，要改 `COMMANDS_REGISTRY` 键、`CATEGORIES` 和 examples。
  - 若只做“新语法映射到旧 canonical”，可保持旧 key 不变，只新增路由/别名层。
  - 帮助输出依赖这里，文案要与新语法一致。

#### `electron/native-pipeline/cli/command-registry-types.ts`
- 责任：命令/flag/category 类型定义。
- 必改点：如要表达 `deprecated`、`aliases`、`replacement`，应在 `CommandDef` 增字段。

#### `electron/native-pipeline/cli/cli-help.ts`
- 责任：`--help` 文本与 JSON 帮助。
- 必改点：
  - 新命令分组展示（例如 `gen`, `flow`, `system`）。
  - 旧命令进入 legacy 区，或通过 `--help-legacy` 暴露。
  - 示例命令统一更新。

#### `electron/native-pipeline/cli/interactive.ts`
- 责任：交互确认与 stdin 读取。
- 必改点：通常不改业务；如想把弃用提醒做成交互确认（不推荐默认），可在交互层挂钩。

---

### B. CLI Handler 层（第二优先级）

#### `electron/native-pipeline/cli/cli-handlers-*.ts`
- 责任：按业务域处理命令（media/speech/editor/subtitle/phota/...）。
- 影响：
  - 若只是“命令名映射”，多数 handler 无需改。
  - 若新命令语义变更（参数含义、默认值变化），需要改各 handler 的参数读取和校验。

#### `electron/native-pipeline/cli/cli-runner/handler-*.ts`
- 责任：核心生成/管线/传输/上采样等调度逻辑。
- 影响：
  - `handler-generate.ts` 对 `options.command` 有硬编码分支（`generate-image` / `create-video` / `generate-avatar`），canonical 改名时必须同步。

#### `electron/native-pipeline/cli/vimax-cli-handlers/**/*.ts`
- 责任：ViMax 子系统命令处理。
- 影响：
  - 若未来把 `vimax:*` 收敛为 `flow *`，这里通常不改核心算法，但 runner 路由和帮助体系要改。

---

### C. Pipeline 执行层（第三优先级，语义变化才改）

#### `electron/native-pipeline/execution/*.ts`
- 责任：链路执行、并行、重试、数据类型衔接。
- 影响：
  - 命令改名本身一般不影响。
  - 但若命令重构导致入参格式变化（如 duration/ratio canonical 化）会影响 `step-executors.ts` 的 payload 映射。

#### `electron/native-pipeline/registry-data/*.ts`
- 责任：模型注册与默认参数。
- 影响：
  - 命令名重构通常不改。
  - 若“新命令 = 新默认模型/新默认策略”，要改对应注册定义。

---

### D. Infra / Provider 抽象层（第四优先级）

#### `electron/native-pipeline/infra/*.ts`
- 责任：API 调用、密钥、代理、成本估算、注册表。
- 影响：
  - 命令名改动通常不触及 provider 调用流程。
  - 若新命令需要新的 provider 参数规范化，改 `api-caller.ts` / `step-executors.ts` 交界最合适。

#### `electron/native-pipeline/registry-data/platform-models.ts`
- 责任：Runway/HeyGen/D-ID/Synthesia/Phota 平台模型注册。
- 影响：
  - 仅在“命令重构伴随模型策略变化”时改。

---

## 2) QCut 仓库中这些文件具体在哪？

仓库根目录：`/Users/peter/Desktop/code/qcut/qcut`

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

## 兼容层设计：deprecated alias、warning、old/new 规范化放哪

###[新增] 建议文件
- `electron/native-pipeline/cli/aliases.ts`
  - `resolveCommand(argv)`: 解析 `gen video` / `create-video` 到 canonical。
  - `warnIfDeprecated(...)`: 旧命令输出 warning（非 JSON/quiet 模式）。

- `electron/native-pipeline/cli/option-normalizer.ts`
  - `normalizeOptions(options)`: 统一 `--prompt/--text`、`--input` 语义，兼容旧参数。

### 挂载点（强烈建议）
1. **命令规范化**：`cli.ts` 的 `parseCliArgs` 最前面（命令合法性校验前）。
2. **session 模式规范化**：`cli-runner/session.ts` 的 `parseSessionLine` 内。
3. **弃用警告**：
   - 单次命令：`cli.ts` 中 `main()`，在 `parseCliArgs` 后、`runner.run()` 前。
   - session 命令：`runSession()` 每行执行前。
4. **参数规范化**：
   - `cli.ts` parse 后返回前。
   - `session.ts` parse 后构造 `CLIRunOptions` 时。

---

## 迁移架构（Hierarchical Command Map + Legacy Alias Adapter）

1. Router 层先吃原始 token：
   - `gen video` → canonical `create-video`
   - `gen image` → canonical `generate-image`
2. Alias Adapter 再处理旧名称：
   - `create-video` 继续可用，但标记 deprecated。
3. Runner/Handlers 全部只接收 canonical command，业务层无感。
4. Help 层双轨：默认展示新语法，`--help-legacy` 展示旧语法。

---

## Checklist：代码改动 vs 文档改动

### Code changes（必须）
- [ ] `cli.ts`：命令解析与规范化入口
- [ ] `command-registry.ts`：命令定义/分类/examples 同步
- [ ] `cli-help.ts`：帮助文档和 JSON 帮助同步
- [ ] `cli-runner/runner.ts`：`switch(command)` 与 canonical 一致
- [ ] `cli-runner/handler-generate.ts`：命令分支条件同步
- [ ] `cli-runner/session.ts`：session 模式命令规范化同步
- [ ] 新增 `aliases.ts`（deprecated alias + warning）
- [ ] 新增 `option-normalizer.ts`（flag 兼容）

### Docs changes（必须）
- [ ] `docs/technical/guides/build-commands.md`（CLI 用法）
- [ ] `docs/technical/architecture/source-code-structure.md`（CLI 结构说明）
- [ ] 仓库内涉及 `qcut-pipeline create-video` 的文档示例
- [ ] 外部页面 `https://quriosity.com.au/cli.html` 同步（命令示例、迁移说明、deprecation 时间线）

---

## 一周实施计划（Day-by-day）

- **Day 1**：补 `aliases.ts` 与 `option-normalizer.ts`，接入 `cli.ts` 与 `session.ts`。
- **Day 2**：改 `cli-help.ts` 与 `command-registry.ts`，实现新语法展示。
- **Day 3**：修 `runner.ts` / `handler-generate.ts` 的 canonical 分支一致性。
- **Day 4**：补测试（旧命令兼容、新命令可达、warning 行为、JSON 静默 warning）。
- **Day 5**：更新 docs（仓库内），生成迁移指南。
- **Day 6**：同步 `https://quriosity.com.au/cli.html`，加升级公告。
- **Day 7**：灰度发布，观测失败率/命令分布，准备下版本移除策略。

---

## 风险与回滚方案

### 风险
1. session 模式与单次命令模式行为不一致。
2. JSON 输出混入 warning，破坏机器解析。
3. 文档未同步导致用户误用。
4. handler 仍依赖旧 command 字符串导致隐性 bug。

### 回滚
1. 保留 `LEGACY_COMMANDS_ENABLED=true` 开关（默认开）。
2. Router 层可一键退回“仅旧命令”模式。
3. 文档回滚到上个稳定版本，外部站点撤回新语法主推。
4. 发布后 24h 内若错误率异常，hotfix 恢复旧 help 默认视图。

---

## 🦞 Lobster verdict

这次重构的关键不是“换个名字”，而是**把命令语法升级与执行语义稳定解耦**。

最稳妥路径是：
- 执行内核（runner/handlers/execution）尽量不动语义，
- 在入口层（router/alias/normalizer/help）做迁移，
- 用双轨帮助和 deprecation 窗口平滑过渡。

一句话：**先兼容、再迁移、最后收口。**
