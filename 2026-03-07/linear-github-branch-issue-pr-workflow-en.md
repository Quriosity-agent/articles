# Linear + GitHub: The Complete Issue → Branch → PR Workflow

> **TL;DR**: Once Linear and GitHub are integrated, any branch name or PR containing a Linear issue ID (e.g. `QUR-11`) is automatically tracked. When the PR merges, the issue auto-closes. This article covers the full workflow from Linear issue to GitHub PR.

---

## Prerequisites

1. **Linear workspace** created (e.g. with `QUR` prefix)
2. **GitHub Integration** connected: Linear → Settings → Integrations → GitHub → select repo
3. (Optional) Install `linear-cli`: `brew install schpet/tap/linear`

---

## The Core Rule

**Linear auto-links GitHub PRs via issue IDs.**

As long as `QUR-XX` appears in any of these:
- ✅ Branch name: `peter/qur-11-add-export`
- ✅ PR title: `[QUR-11] Add export feature`
- ✅ PR description: `Closes QUR-11`
- ✅ Commit message: `feat: add export (QUR-11)`

Linear will automatically associate the PR with the corresponding issue.

---

## Workflow: Three Approaches

### Approach A: Start from Linear (Recommended)

```
1. Create issue in Linear
   → Title: "Add video export feature"
   → Auto-assigned ID: QUR-11

2. Get branch name
   → Issue detail page → "Copy git branch name"
   → Generated: peter/qur-11-add-export

3. Create local branch
   git checkout -b peter/qur-11-add-export

4. Code & commit
   git add -A
   git commit -m "feat: add video export (QUR-11)"

5. Push & create PR
   git push -u origin peter/qur-11-add-export
   gh pr create --fill

6. Linear auto-tracks ✅
   → PR status syncs to Linear issue
   → PR merge → issue auto-marked Done
```

### Approach B: Start from GitHub

```
1. Create branch with issue ID in name
   git checkout -b qur-11-quick-fix

2. Code → commit → push → create PR

3. Include QUR-11 in PR title or description
   gh pr create --title "[QUR-11] Fix export bug"

4. Linear auto-links ✅
```

### Approach C: Use linear-cli (Easiest)

```bash
# Setup (one-time)
cd ~/Desktop/code/qcut/qcut
linear config

# Daily workflow
linear issue list                # see pending issues
linear issue start QUR-11        # auto-creates branch + marks In Progress
# ... code ...
linear issue pr                  # auto-creates PR via gh, fills title/description
# PR merge → Linear auto-closes issue ✅
```

### Approach D: Let Agents Do It (Orchestrator Mode)

```
1. Create issue in Linear: QUR-12 "Refactor payment module"

2. Tell agent: "Work on QUR-12"

3. Agent automatically:
   → git checkout -b agent/qur-12-refactor-payment
   → writes code
   → git commit + push
   → gh pr create (title includes QUR-12)

4. Linear auto-tracks ✅

5. You review PR → merge → issue auto-closes
```

---

## Linear Issue Auto-Transitions

| GitHub Event | Linear Issue Status |
|-------------|-------------------|
| Linked branch created | → In Progress |
| PR opened | → In Review |
| PR merged | → Done |
| PR closed (no merge) | → Reverts to previous |

> Enable in Linear Settings → Integrations → GitHub: "Auto-close issues" and "Auto-transition issues"

---

## Recommended PR Description Template

```markdown
## Summary
Brief description of changes

## Linear Issue
Closes QUR-XX

## Changes
- Change 1
- Change 2

## Testing
- [ ] Local tests pass
- [ ] CI passes
```

---

## FAQ

### Linear didn't auto-link my PR?
- Check branch name / PR title / description for `QUR-XX`
- Verify GitHub Integration is connected and the correct repo is selected
- Issue IDs are case-insensitive (`qur-11` = `QUR-11`)

### Multiple issues in one PR?
- List them in PR description: `Closes QUR-11, QUR-12`

### Agent PRs not linking?
- Ensure agents use `qur-xx-` prefix in branch names
- Or include issue ID in PR title

---

## 🦞 Lobster Summary

The entire workflow boils down to one rule:

**Branch name has ID → auto-linked → PR merge → auto-closed**

No manual syncing needed. The bridge between Linear and GitHub is just that `QUR-XX` issue ID.

Start simple: run a few issues manually with Approach A, then graduate to linear-cli or agent automation.

---

## Sources
- Linear GitHub Integration: <https://linear.app/docs/github>
- linear-cli: <https://github.com/schpet/linear-cli>

---

*Author: 🦞 Lobster Detective*  
*Date: 2026-03-07*  
*Tags: Linear / GitHub / PR Workflow / Issue Tracking / Git Branch / CI-CD*
