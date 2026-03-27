# 🎭 Agency Agents：144 个 AI 专家人格，一个仓库装下整个"虚拟公司"

> **仓库地址：** [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
> **Stars：** 64k+ ⭐ | **Forks：** 9.7k | **License：** MIT
> **一句话：** 不是 prompt 模板库，而是一套有性格、有流程、有交付物的 AI Agent 人格系统。

---

## 这是什么？

大部分 AI prompt 库的套路是 "Act as a developer" 然后一段泛泛而谈的描述。`agency-agents` 完全不同——它给每个 Agent 设计了**完整的人格**：有名字、有语气、有专长流程、有代码示例、甚至有 KPI。

把 144 个 Agent 按业务部门分成 **12 个 Division**：

| Division | 数量 | 典型 Agent |
|----------|------|-----------|
| 💻 Engineering | 27 | 前端、后端架构师、安全工程师、Solidity 合约 |
| 🎨 Design | 8 | UI/UX、品牌守护者、Whimsy Injector |
| 💰 Paid Media | 7 | PPC 策略、Search Query 分析、广告审计 |
| 💼 Sales | 8 | 外呼策略、Discovery Coach、Deal Strategist |
| 📢 Marketing | 30+ | SEO、TikTok、Reddit、小红书、B站、快手 |
| 📊 Product | 5 | Sprint 规划、趋势研究、行为助推 |
| 🎬 PM | 6 | Studio Producer、Jira Workflow |
| 🧪 Testing | 8 | API 测试、性能基准、无障碍审计 |
| 🛟 Support | 6 | 客服、财务、合规、基础设施 |
| 🥽 Spatial | 6 | XR 界面、visionOS、WebXR |
| 🎮 Game Dev | 16 | Unity/Unreal/Godot/Roblox/Blender |
| 📚 Academic | 5 | 人类学家、地理学家、心理学家 |

**值得注意的是**，这个仓库非常重视中国市场——有微信小程序、飞书集成、小红书、B 站、抖音、快手、知乎、百度 SEO、跨境电商等专属 Agent。这在英文开源项目里相当少见。

---

## 技术架构：Agent 文件长什么样？

每个 Agent 是一个 Markdown 文件，结构统一：

```yaml
---
name: Frontend Developer
description: Expert frontend developer...
color: cyan
emoji: 🖥️
vibe: Builds responsive, accessible web apps...
---
```

正文包含：
1. **Identity & Memory** — 角色定位 + 记忆机制
2. **Core Mission** — 具体工作职责（带代码示例）
3. **Critical Rules** — 领域特定的硬约束
4. **Workflow Process** — 分步骤的工作流程
5. **Success Metrics** — 可量化的交付标准

---

## 多工具集成：不只是 Claude Code

这是最实用的部分。仓库自带 `convert.sh` + `install.sh` 脚本，一键把 Agent 转换为各种工具的格式：

```
支持的工具：
├── Claude Code     → ~/.claude/agents/（原生 .md，无需转换）
├── GitHub Copilot  → ~/.github/agents/
├── Cursor          → .cursor/rules/*.mdc
├── Aider           → CONVENTIONS.md
├── Windsurf        → .windsurfrules
├── Gemini CLI      → ~/.gemini/extensions/
├── Antigravity     → ~/.gemini/antigravity/skills/
├── OpenCode        → .opencode/agents/
├── OpenClaw        → SOUL.md + AGENTS.md + IDENTITY.md
├── Qwen Code       → ~/.qwen/agents/
└── Kimi Code       → ~/.config/kimi/agents/
```

安装流程：

```bash
# 生成所有工具的集成文件
./scripts/convert.sh

# 交互式安装（自动检测本机工具）
./scripts/install.sh

# 或指定某个工具
./scripts/install.sh --tool cursor

# 并行加速
./scripts/convert.sh --parallel --jobs 8
```

安装脚本会扫描你的系统，弹出一个复选框 UI，选择你要安装的工具。

---

## 实际使用场景

### 场景 1：Startup MVP 快速搭建

组队：Frontend Developer + Backend Architect + Growth Hacker + Rapid Prototyper + Reality Checker

每个 Agent 都知道自己的职责边界。前端 Agent 会坚持 Core Web Vitals，后端 Agent 会默认考虑 API 版本化，Growth Hacker 会直接给出 viral loop 设计。

### 场景 2：付费媒体账户接管

组队：Paid Media Auditor → Tracking Specialist → PPC Strategist → Search Query Analyst → Ad Creative Strategist

这套流程模拟了一个真实广告代理公司接管新客户的标准操作。30 天内完成审计、追踪验证、结构优化、素材刷新。

### 场景 3：跨部门产品发现

仓库给了一个完整示例（[Nexus Spatial Discovery](https://github.com/msitarzewski/agency-agents/blob/main/examples/nexus-spatial-discovery.md)），8 个部门的 Agent 并行工作，产出统一产品方案。

---

## 为什么这个项目有价值？

**1. 解决了 "AI 太通用" 的问题**

通用 LLM 什么都能聊，但什么都不够深。这些 Agent 人格强制 LLM 进入特定领域的思维模式，输出质量显著不同。

**2. 可组合的 Agent 团队**

不是让一个 AI 干所有事，而是像搭乐高一样组合专家。Security Engineer 审代码 + Code Reviewer 看架构 + Technical Writer 写文档。

**3. 全工具链覆盖**

不锁定任何一个 IDE 或 AI 平台。无论你用 Cursor、Claude Code、还是 Gemini CLI，都能即插即用。

**4. 社区驱动 + 快速迭代**

从 Reddit 一个帖子开始，64k+ Stars 说明社区需求是真实的。每天都有新 Agent 的 PR 提交。

---

## 我的使用建议

1. **不要一口气装 144 个** — 从你最需要的 3-5 个开始
2. **修改 Agent 人格** — fork 后按你的技术栈定制（比如把 React 换成你用的框架）
3. **组合使用** — 用 Agents Orchestrator 做项目调度，再分发给专业 Agent
4. **注意上下文窗口** — 每个 Agent 的 system prompt 会占用 token，合理控制加载数量

---

## 相关链接

- **GitHub：** <https://github.com/msitarzewski/agency-agents>
- **贡献指南：** <https://github.com/msitarzewski/agency-agents/blob/main/CONTRIBUTING.md>
- **中文贡献指南：** <https://github.com/msitarzewski/agency-agents/blob/main/CONTRIBUTING_zh-CN.md>

---

![Agency Agents 仓库截图](https://opengraph.githubassets.com/1/msitarzewski/agency-agents)
*图片来源：GitHub OpenGraph — msitarzewski/agency-agents*

---

🦞
