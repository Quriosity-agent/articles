# Linear + GitHub：Issue → Branch → PR 完整工作流

> **TL;DR**: Linear 和 GitHub 集成后，只要分支名或 PR 里带上 issue ID（如 `QUR-11`），Linear 就能自动追踪 PR 状态。PR merge 后 issue 自动关闭。本文梳理从 Linear issue 到 GitHub PR 的完整流程。

---

## 前置条件

1. **Linear workspace** 已创建（如 `QUR` 前缀）
2. **GitHub Integration** 已连接：Linear → Settings → Integrations → GitHub → 选择 repo
3. （可选）安装 `linear-cli`：`brew install schpet/tap/linear`

---

## 核心规则

**Linear 靠 issue ID 自动关联 GitHub PR。**

只要以下任一位置出现 `QUR-XX`：
- ✅ 分支名：`peter/qur-11-add-export`
- ✅ PR 标题：`[QUR-11] Add export feature`
- ✅ PR 描述：`Closes QUR-11`
- ✅ Commit message：`feat: add export (QUR-11)`

Linear 就会自动把 PR 关联到对应 issue。

---

## 工作流：三种方式

### 方式 A：从 Linear 出发（推荐）

```
1. Linear 建 issue
   → 标题: "添加视频导出功能"
   → 自动分配 ID: QUR-11

2. 获取分支名
   → Linear issue 详情页 → "Copy git branch name"
   → 生成: peter/qur-11-add-export

3. 本地建分支
   git checkout -b peter/qur-11-add-export

4. 写代码 & commit
   git add -A
   git commit -m "feat: add video export (QUR-11)"

5. 推送 & 提 PR
   git push -u origin peter/qur-11-add-export
   gh pr create --fill

6. Linear 自动追踪 ✅
   → PR 状态同步到 Linear issue
   → PR merge → issue 自动标记 Done
```

### 方式 B：从 GitHub 出发

```
1. 直接建分支（名字里带 issue ID）
   git checkout -b qur-11-quick-fix

2. 写代码 → commit → push → 提 PR

3. PR 标题或描述里带 QUR-11
   gh pr create --title "[QUR-11] Fix export bug"

4. Linear 自动关联 ✅
```

### 方式 C：用 linear-cli（最省事）

```bash
# 配置（只需一次）
cd ~/Desktop/code/qcut/qcut
linear config

# 日常流程
linear issue list                # 看待办 issues
linear issue start QUR-11        # 自动建分支 + 标记 In Progress
# ... 写代码 ...
linear issue pr                  # 自动用 gh 提 PR，标题描述自动填充
# PR merge 后 Linear 自动关闭 issue ✅
```

### 方式 D：让 Agent 干（Orchestrator 模式）

```
1. Linear 建 issue: QUR-12 "重构支付模块"

2. 告诉 agent: "搞 QUR-12"

3. Agent 自动：
   → git checkout -b agent/qur-12-refactor-payment
   → 写代码
   → git commit + push
   → gh pr create（标题带 QUR-12）

4. Linear 自动追踪 ✅

5. 你 review PR → merge → issue 自动关闭
```

---

## Linear Issue 状态自动流转

| GitHub 事件 | Linear issue 状态变化 |
|-------------|---------------------|
| 建了关联分支 | → In Progress |
| 提了 PR | → In Review |
| PR merge | → Done |
| PR close (不 merge) | → 回到之前状态 |

> 需要在 Linear Settings → Integrations → GitHub 里开启 "Auto-close issues" 和 "Auto-transition issues"

---

## PR 描述模板（推荐）

```markdown
## Summary
简要描述改了什么

## Linear Issue
Closes QUR-XX

## Changes
- 改动 1
- 改动 2

## Testing
- [ ] 本地测试通过
- [ ] CI 通过
```

---

## 常见问题

### Linear 没有自动关联 PR？
- 检查分支名/PR标题/描述里有没有 `QUR-XX`
- 确认 GitHub Integration 已连接且选对了 repo
- issue ID 大小写不敏感（`qur-11` = `QUR-11`）

### 多个 issue 关联同一个 PR？
- PR 描述里写多个：`Closes QUR-11, QUR-12`

### Agent 提的 PR 没关联？
- 确保 agent 建分支时用 `qur-xx-` 前缀
- 或在 PR 标题里带上 issue ID

---

## 🦞 龙虾总结

整个流程的核心就一句话：

**分支名带 ID → 自动关联 → PR merge → 自动关闭**

不需要手动同步任何东西。Linear 和 GitHub 之间的桥梁就是那个 `QUR-XX` issue ID。

从简单开始：先用方式 A 手动跑几个 issue，熟了再上 linear-cli 或让 agent 自动化。

---

## Sources
- Linear GitHub Integration: <https://linear.app/docs/github>
- linear-cli: <https://github.com/schpet/linear-cli>

---

*作者: 🦞 龙虾侦探*  
*日期: 2026-03-07*  
*标签: Linear / GitHub / PR Workflow / Issue Tracking / Git Branch / CI-CD*
