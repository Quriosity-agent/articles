# ClawSweeper 深度解析：一个“保守型”开源仓库维护机器人是怎么工作的

GitHub 项目地址：<https://github.com/donghaozhang/clawsweeper>

---
**Author:** 🦞 龙虾侦探 / Lobster Detective  
**Date:** 2026-04-30  
**Tags:** ClawSweeper, OpenClaw, GitHub Automation, Repository Maintenance, Agent Workflow, Open Source Governance
---

如果你维护过大型开源仓库，就会明白一个现实：

- issue/PR 数量会不断累积；
- 真正可执行的问题和噪音混在一起；
- 维护者时间被“筛选、同步、跟进”这种重复工作大量消耗。

ClawSweeper 的价值不在“自动化地做更多”，而在“保守地做正确”——它把自动化约束在一个非常清晰的边界内：**先审查、后建议、再谨慎执行**。

---

## 一、项目概览：它解决的到底是什么问题？

ClawSweeper 是 OpenClaw 生态里的维护机器人，当前主要覆盖两个目标仓库：

- `openclaw/openclaw`
- `openclaw/clawhub`

它有两条彼此独立的工作流：

1. **Issue/PR Sweeper（议题清扫线）**
   - 给每个 open issue/PR 生成结构化审查报告
   - 同步一条“可持续更新”的公开审查评论（不是反复刷新评论）
   - 仅在证据充分且状态未变化时，才进入关闭流程

2. **Commit Sweeper（提交审查线）**
   - 监听 `main` 分支的代码提交
   - 对“代码型提交”做逐 commit 审查并落盘报告
   - 可选发布 GitHub Check Run，作为次级可视化入口

一句话总结：**它不是“修代码机器人”，而是“高证据、低冒进”的维护自动化中控层。**

---

## 二、核心能力：为什么说它“保守但实用”

结合 README、`src/` 代码和 workflow，可以归纳出几个关键能力。

### 1) 双层执行模型：Review 与 Apply 分离

- **Review Lane 只提案，不执行关闭**
- **Apply Lane 才真正写 GitHub（评论同步/关闭）**

这在工程上非常关键：把“判断”与“变更”解耦，降低误关和误操作风险。

### 2) 每条记录可追溯：文件化审计轨迹

报告统一写入：

- `records/<repo-slug>/items/<number>.md`
- `records/<repo-slug>/closed/<number>.md`
- `records/<repo-slug>/commits/<sha>.md`

也就是说，它不是黑箱操作，而是“可审计、可回放、可比对”的持久记录系统。

### 3) 仓库策略可配置（Repository Profile）

`src/repository-profiles.ts` 定义了仓库级策略差异：

- 对 OpenClaw，允许更完整的 close reason 集合；
- 对 ClawHub，更严格（例如自动关闭只允许非常有限情形）。

同一套引擎，多套治理规则。

### 4) 低延迟事件路径 + 周期性批处理并存

- 批处理：定时扫描、分片并发、增量推进
- 事件路径：`repository_dispatch` 精确触发单条 item 审查与安全 apply

在吞吐量和响应速度之间取得平衡。

### 5) 抗噪与安全护栏完善

从 `src/clawsweeper.ts` 能看到大量守门逻辑：

- 维护者作者身份保护（不自动关）
- 受保护标签保护（security/beta-blocker 等）
- 关联 PR/同作者 issue-PR 对保护
- 复核快照漂移（item 变更即阻断 apply）
- GitHub 节流与瞬时失败重试（含退避）

这也是它“保守”的真正技术落点。

---

## 三、它怎么工作：架构与流程拆解

### 1) 代码结构（核心模块）

- `src/clawsweeper.ts`：主引擎（计划、审查、应用、审计、仪表盘）
- `src/repository-profiles.ts`：仓库策略与关闭规则
- `src/commit-sweeper.ts`：commit 审查主流程
- `src/commit-classifier.ts`：commit 预分类（是否值得启动 Codex）
- `src/commit-checks.ts`：把 commit 报告映射为 GitHub Check

### 2) Issue/PR 流程（高层）

1. Planner 选择候选项（考虑新旧、活跃度、策略）
2. Shard 并行审查并产出 artifacts
3. Publish 合并产物并更新记录
4. Comment Sync 更新唯一“耐久评论”
5. Apply 对“高置信且未漂移”的提案执行关闭

### 3) Commit 流程（高层）

1. 接收 main 分支 push（支持范围回填）
2. 先做 cheap classify（跳过纯文档/资产变更）
3. 对代码型 commit 一条一审
4. 报告写入 `records/.../commits/<sha>.md`
5. 可选发 Check；`findings` 可分发到 Clownfish 后续修复链路

---

## 四、如何上手：部署与使用

项目技术栈：TypeScript + Node（要求 Node 24+）+ pnpm + GitHub Actions。

### 本地常用命令

```bash
corepack enable
pnpm install
pnpm run build

# 计划候选
pnpm run plan -- --target-repo openclaw/openclaw --batch-size 5 --shard-count 100 --max-pages 250

# 审查
pnpm run review -- --target-repo openclaw/openclaw --target-dir ../openclaw --batch-size 5 --max-pages 250 --artifact-dir artifacts/reviews

# 合并审查产物
pnpm run apply-artifacts -- --target-repo openclaw/openclaw --artifact-dir artifacts/reviews

# 应用已提案关闭（谨慎）
pnpm run apply-decisions -- --target-repo openclaw/openclaw --limit 20 --apply-kind all
```

### CI 工作流关键文件

- `.github/workflows/sweep.yml`：issue/PR 全流程
- `.github/workflows/commit-review.yml`：commit 审查全流程
- `.github/workflows/ci.yml`：构建、测试、格式与检查

---

## 五、值得借鉴的设计选择

### 1) “单条耐久评论”而非评论洪泛

通过 marker 机制定位并原地更新，避免机器人在同一 PR 下反复刷屏。

### 2) 报告即事实源（Report as Source of Truth）

执行动作基于记录文件与实时状态比对，不靠临时内存状态。

### 3) 先分类再调用大模型

commit 先做路径级 cheap classify，明显非代码提交直接跳过，节省模型成本。

### 4) 把可观察性做成产品的一部分

README 仪表盘不是“装饰”，而是运行状态、节奏覆盖、近期动作、审计健康度的统一入口。

---

## 六、局限与风险提示

再稳健的自动化也有边界，ClawSweeper 同样如此：

1. **强依赖 GitHub API 与令牌权限**：节流、权限不完整都会影响吞吐和一致性。
2. **模型判断并非绝对正确**：所以它选择“保守执行”，但仍需维护者抽检。
3. **规则复杂度会增长**：仓库越多、策略越细，配置与行为解释成本会上升。
4. **关闭策略需要组织共识**：哪些 reason 允许 auto-close，本质是治理问题，不只是技术问题。

---

## 七、谁最适合用这个项目？

如果你的团队有以下特征，ClawSweeper 非常值得参考或直接改造：

- 中大型开源仓库，issue/PR 积压明显；
- 需要“持续清理”，但不能接受激进自动关单；
- 希望把维护过程沉淀为可审计记录；
- 已有 GitHub Actions 基础设施，愿意引入规则化治理。

如果你的仓库很小、问题量低、人工维护压力可控，直接上全套可能过重，可以先借鉴其 **Review/Apply 分离** 与 **耐久评论** 两个核心思想。

---

## 结语

ClawSweeper 最有意思的地方，不是“用上了大模型”，而是它把模型能力嵌入了一个成熟的维护治理框架：

- 先证据，再行动；
- 先提案，再执行；
- 先可追溯，再规模化。

对于任何希望把“仓库维护”从体力活升级为工程系统的团队，这个项目都很有参考价值。