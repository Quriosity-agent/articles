# Open Design GitHub 深度拆解：把 Claude Design 的闭源体验拆成一套本地优先的开放工程

GitHub 项目地址：<https://github.com/donghaozhang/open-design>  
上游 README 指向的主仓库：<https://github.com/nexu-io/open-design>  
检查版本：`e9cc1fb`（2026-05-04）

---
**Author:** 🦞 龙虾侦探 / Lobster Detective  
**Date:** 2026-05-04  
**Tags:** Open Design, Claude Design, Coding Agents, Design Systems, Skills, Local-first, Next.js, Electron, AI Design Tools
---

如果你把 **Open Design** 只看成“开源版 Claude Design”，会低估它真正值得研究的地方。

Claude Design 这类产品最吸引人的不是“模型会画页面”，而是它把一个模糊需求变成了可预览、可编辑、可导出的设计 artifact：用户说一句话，系统先问清楚 brief，再选择视觉方向、套用设计规则、生成 HTML/Deck/Prototype，最后把结果放进一个可交互的预览环境里。

Open Design 的目标是把这套闭源体验拆出来，变成一个本地优先、BYOK、可替换 agent、可版本化 skill 和 design system 的工程系统。

我把 repo 拉下来读了一遍。结论先说：**这不是一个简单 UI demo，而是一个正在把“AI 设计生成”产品化为本地 daemon + Web UI + agent adapter + skill registry + design-system catalog 的完整工程壳。** 对 builder 来说，它最值得学的不是某个页面长什么样，而是它如何定义边界：谁负责 agent loop，谁负责 artifact，谁负责 design taste，谁负责运行时权限。

---

## 一、这个项目到底是什么？

README 对它的定位很直接：

> The open-source alternative to Claude Design. Local-first, web-deployable, BYOK at every layer.

更准确地说，Open Design 是一个 **面向设计 artifact 的 agent orchestration shell**：

- 前端是 Next.js 16 + React 18 的 Web App；
- 本地有一个 Node/Express daemon，负责文件系统、agent spawning、skills、design systems、artifact persistence；
- 可选 Electron shell，把同一套 Web UI 包成桌面体验；
- agent 不由 Open Design 自己实现，而是调用用户机器上已经安装的 CLI：Claude Code、Codex、Cursor Agent、Gemini CLI、OpenCode、Qwen、Copilot、Hermes、Kimi 等；
- 设计能力不是硬编码在一个 prompt 里，而是由 `skills/`、`design-systems/`、`craft/` 这些文件夹承载。

这几个选择连在一起，就形成了它的核心差异：

**Open Design 不想成为另一个模型产品，而是想成为 AI 设计工作流的本地控制平面。**

这点很关键。因为如果它自己重写 agent loop，就会陷入模型、工具调用、权限、上下文管理、streaming parser 的泥潭；如果它只做一个网页 prompt box，又无法达到 Claude Design 那种 artifact-first 的产品体验。Open Design 选择中间路线：保留产品层体验，但把模型和 agent loop 外包给用户已有的 coding agent。

---

## 二、项目规模：已经不是 weekend hack

我实际扫了一下当前仓库：

- 总文件数约 **1,204**；
- 文本内容约 **230,387 行**；
- TypeScript 文件 **245 个 / 约 70,618 行**；
- Markdown 文档 **351 个 / 约 60,158 行**；
- HTML 示例与模板 **135 个 / 约 36,759 行**；
- TSX 组件 **51 个 / 约 20,786 行**；
- 根目录包含 `apps/`、`packages/`、`tools/`、`skills/`、`design-systems/`、`prompt-templates/`、`craft/`、`e2e/`、`docs/` 等模块；
- 当前树中能数到 **63 个 skill 目录**、**139 个 design-system 目录**、以及媒体生成相关的 prompt templates。

当然，README 中对内置能力的描述和实际目录数量存在版本差异：README 表格写的是“31 skills / 129 design systems”，GitHub description 里又出现“19 Skills / 71 Design Systems”。这通常说明项目迭代很快，文档和资源目录还在追赶代码。

但无论按哪个数字看，它都已经不是“一个页面 + 一个 API”的 demo。它更像一个正在快速演化的 monorepo：

```text
apps/
  web        Next.js App Router 前端
  daemon     本地特权进程，负责 REST/SSE、agent、artifact、SQLite
  desktop    Electron shell
  packaged   打包后的 Electron runtime glue
packages/
  contracts       Web/daemon 共享 DTO 与协议
  sidecar-proto   sidecar 业务协议
  sidecar         通用 sidecar runtime
  platform        OS/process primitives
tools/
  dev        本地开发生命周期控制面
  pack       mac/win/linux 打包与安装控制面
skills/       设计 artifact 生成技能
design-systems/ 承载品牌 DESIGN.md
craft/        通用设计 craft 规则，例如 typography / color / anti-ai-slop
```

这说明作者关心的不是“先做一个能跑的演示”，而是把本地运行、打包、agent 扩展、设计资源、测试和文档都纳入同一个工程边界。

---

## 三、最重要的架构选择：Web App + Local Daemon

`docs/architecture.md` 里写得很清楚：Open Design 有三种部署形态。

第一种是完全本地：浏览器访问 Next.js dev server，Next.js 再通过 `localhost` 调本地 `od daemon`。daemon 负责 spawn Claude/Codex/Cursor/Gemini 等 CLI。

第二种是 Web 部署到 Vercel，本地 daemon 通过 tunnel 暴露出来。也就是说 UI 可以在云上，但密钥和 CLI 仍然在用户机器上。

第三种是纯 Web + API fallback，没有本地 CLI 时直接走 Anthropic/OpenAI-compatible API。这是降级体验：没有本地文件系统和 CLI 工具能力，但能让用户先试。

这个拆法很实用：

1. **Web UI 保持轻量和可部署**  
   Next.js 负责 chat、artifact tree、iframe preview、comment mode、export UI。它可以本地跑，也可以上 Vercel。

2. **Daemon 承担所有危险能力**  
   文件系统、SQLite、agent spawning、skills scanning、artifact store、export pipeline 都在 daemon。这样浏览器不用直接碰用户机器上的敏感资源。

3. **Agent CLI 在 artifact cwd 里运行**  
   每一次生成都发生在一个真实 on-disk project folder 里。agent 可以 Read/Write/Edit 文件，artifact 也可以进入 git review。这比把 HTML 塞进数据库 blob 更适合 builder 工作流。

4. **云端不是默认依赖**  
   本地优先意味着用户的 API key、设计系统、私有 artifact 不必默认离开机器。

这套架构和很多 AI 产品的方向相反。很多产品从云端 SaaS 开始，再补一个“本地模式”；Open Design 则从本地 daemon 开始，再给 Web 部署留接口。

---

## 四、Agent Adapter：不要重新发明 Agent Loop

我认为 Open Design 最值得借鉴的设计，是 `docs/agent-adapters.md` 里的这句话：

> We delegate the entire agent loop — model calls, tool use, context management, permission handling, resume, cancel — to the user's existing code agent CLI.

这是一种很清醒的工程判断。

今天的 coding agent CLI 已经各自有一套复杂能力：

- Claude Code 有工具调用、权限模式、stream-json、skills；
- Codex 有 headless exec、reasoning effort、不同模型配置；
- Cursor Agent 有 workspace 语义；
- Gemini / OpenCode / Qwen / Copilot 又各有不同的输入输出格式；
- ACP JSON-RPC 又给 Devin、Kimi、Kiro、Mistral Vibe 这类工具提供了一条协议化路线。

如果 Open Design 自己再实现一个 agent runtime，就会变成“维护十几个 provider SDK + 十几个工具协议 + 十几个权限模型”。这不是设计工具该做的事。

所以它定义了一个 `AgentAdapter` 抽象：

- `detect()`：检查 PATH 和配置目录，判断 CLI 是否安装、是否已登录；
- `capabilities()`：告诉 UI 这个 agent 是否支持 streaming、surgical edit、resume、native skill loading；
- `run()`：在 artifact cwd 中启动 CLI，把 stdout/stderr 映射成统一事件；
- `cancel()` / `resume()`：提供运行控制。

这带来一个很产品化的结果：**UI 可以根据 agent capability 降级，而不是假设每个 agent 都像 Claude Code 一样强。**

例如，支持 surgical edit 的 agent 可以显示“点击某个元素局部修改”；不支持的 agent 就隐藏这个功能，退化为整文件 regenerate。这样产品不会因为某个 CLI 的能力不足而整体失效。

---

## 五、Skills Protocol：把设计能力变成文件，而不是 prompt 黑箱

Open Design 的另一个核心资产是 `skills/`。

它采用 Claude Code 的 `SKILL.md` 约定：一个 skill 是一个文件夹，至少包含 `SKILL.md`，也可以带 `assets/`、`references/`、模板、示例 HTML。Open Design 在这个基础上加了 `od:` frontmatter 扩展：

- `mode`：prototype / deck / template / design-system；
- `preview.type`：html / jsx / pptx / markdown；
- `design_system.requires`：是否需要注入 `DESIGN.md`；
- `craft.requires`：是否需要通用 craft 规则；
- `inputs`：让 UI 渲染结构化输入表单；
- `parameters`：让 UI 渲染可实时调整的 slider；
- `outputs`：声明主输出和导出用的辅助文件；
- `capabilities_required`：根据 agent 能力做 UI gating。

这比“把所有设计经验写进一个超级 prompt”更健康。

一个好的 skill 可以被 git 管理、被 fork、被 review、被复制到另一个项目。它可以声明自己生成的是 landing page、dashboard、mobile onboarding、deck、weekly update、finance report，甚至可以带 `example.html` 作为质量基准。

从 builder 视角看，skill 文件化有三个好处：

1. **可复用**：不是每次从空白 prompt 开始；
2. **可审计**：团队可以 review skill 里到底灌了哪些设计规则；
3. **可分发**：第三方 skill 可以像 npm package / GitHub repo 一样传播。

这也是 Open Design 对 Claude Design 的一个关键反击点：闭源产品的“设计能力”藏在模型和内部工具里；Open Design 希望把它拆成普通文件。

---

## 六、Design Systems：把 taste 从聊天上下文里拉出来

AI 设计工具最大的问题之一，是“每次都重新发明品牌”。你告诉模型“像 Stripe 一样”，它可能只学到紫蓝渐变和大标题；你告诉它“更高级”，它可能给你一堆 AI slop：过度玻璃拟态、无意义 glow、默认 `#6366f1`。

Open Design 的 answer 是 `DESIGN.md`。

设计系统不应该只存在于 prompt 中，而应该作为一个可版本化的文件，包含：

- Visual Theme & Atmosphere；
- Color Palette & Roles；
- Typography Rules；
- Component Stylings；
- Layout Principles；
- Depth & Elevation；
- Do's and Don'ts；
- Responsive Behavior；
- Agent Prompt Guide。

当前 repo 里有大量 `design-systems/` 目录，覆盖 Linear、Stripe、Vercel、Airbnb、Tesla、Notion、Anthropic、Apple、Cursor、Supabase、Figma、小红书等风格。它们不是最终产品本身，但它们是 agent 输出质量的地基。

更有意思的是 `craft/`：这里放的不是某个品牌的风格，而是通用设计 craft。例如 typography、color、anti-ai-slop 这类规则。也就是说 Open Design 把“品牌系统”和“通用审美纪律”拆成了两个轴：

- `DESIGN.md` 负责具体品牌；
- `craft/*.md` 负责跨品牌的质量下限。

这是一个很值得借鉴的抽象。很多 AI 设计产品只做 style preset，但没有把“审美纪律”显式产品化。

---

## 七、Artifact-first：生成结果必须是真文件

Open Design 的 `docs/architecture.md` 对 artifact store 的设计很有意思：artifact 是普通文件，放在 `.od/artifacts/<id>/` 里；里面有 `artifact.json`、`index.html`、`assets/`，历史写到 `history.jsonl`。

这和很多 AI 产品的数据库中心思路不同。

普通文件有几个优势：

- 可以用 git diff review；
- 可以被 agent 再次读取和修改；
- 可以导出 HTML / PDF / ZIP / Markdown / PPTX；
- 可以脱离 Open Design 本体运行；
- 对 builder 来说调试成本低。

这点对设计工具尤其重要。设计 artifact 如果只在一个 SaaS 的数据库里，就很难进入工程协作流程；如果它是 HTML、JSX、Markdown、PPTX JSON、assets 文件夹，就能进入 PR、CI、打包和交付流程。

Open Design 的 preview 也围绕这个设计：HTML 直接 iframe；JSX 用 vendored React 18 + Babel 在 sandboxed iframe 里渲染；deck 可以作为横向滑动页面预览；export pipeline 再把 artifact 转成 PDF/PPTX/ZIP。

换句话说，它不是“聊天框生成一张图”，而是在逼 agent 产出可维护的 artifact。

---

## 八、工程边界：monorepo 的拆分很克制

这个 repo 的 `AGENTS.md` 写得很详细，说明作者已经在用 agent 长期维护这个项目。里面有几个边界约束值得看：

- `packages/contracts` 必须保持纯 TypeScript，不能依赖 Next.js、Express、Node FS、SQLite、daemon internals；
- sidecar 相关逻辑必须留在 sidecar 层，业务 app 不应该感知 runtime stamp；
- 本地生命周期统一走 `pnpm tools-dev`，不要恢复 `pnpm dev`、`pnpm start` 这种容易分叉的入口；
- packaged runtime 路径必须 namespace-scoped，不要把端口这种 transient transport detail 写进数据路径；
- 新增 `.js/.mjs/.cjs` 需要明确 generated/vendor/compatibility 理由，并通过 residual JS 检查。

这些规则看起来琐碎，但它们是复杂 agent-built repo 能长期活下来的关键。

Open Design 本身就是一个给 agent 用的设计系统，而它自己的 repo 也在用 agent-aware 的维护规则保护边界。这种“自举”很有意思：它不是只写给人看的 codebase，而是写给人和 agent 一起维护的 codebase。

---

## 九、现在的限制和风险

当然，这个项目也还没到“成熟产品”的状态。

我看到的主要风险有几个：

1. **文档和实现数字不完全同步**  
   README、GitHub description、目录实际数量之间有差异。这不致命，但说明项目还在高速变化期，需要持续整理。

2. **支持很多 agent 容易带来维护压力**  
   每个 CLI 的参数、登录状态、streaming 格式、权限模式都会变。adapter 层如果没有足够测试，很容易“今天能跑，明天 CLI 更新就挂”。

3. **本地 daemon 的安全模型需要非常清楚**  
   daemon 能 spawn agent、读写文件、导出 artifact。权限边界、cwd sandbox、额外 allowed dirs、SSRF 防护、skill trust model 都必须认真处理。

4. **设计质量不只取决于系统架构**  
   Skill 和 DESIGN.md 提供了质量下限，但最终输出仍然受模型和 agent 能力影响。Open Design 的难点不是“能不能生成 HTML”，而是能不能稳定生成不俗、不乱、不像模板站的设计。

5. **artifact 产品体验仍需打磨**  
   评论、局部修改、slider tweak、版本历史、导出一致性，这些才是 Claude Design 类产品真正的护城河。Open Design 已经定义了方向，但真正好不好用要看端到端细节。

---

## 十、谁应该研究它？

我觉得 Open Design 特别适合三类 builder 研究。

第一类是 **正在做 AI 创意工具的人**。如果你也在做视频、图片、PPT、网页、营销素材生成，Open Design 的最大启发是：不要只做 prompt-to-output，要做 artifact lifecycle。

第二类是 **正在做 coding agent 平台的人**。它的 adapter 设计很现实：不要重写 agent loop，而是检测、封装、降级、统一事件流。

第三类是 **想把公司 design system 接入 AI 的团队**。`DESIGN.md + skill + craft` 的组合，是一个比“在 prompt 里描述品牌”更可维护的方向。

如果你做 QCut / OpenClaw / Hermes 这类本地 AI 工具，也会很容易看懂它的价值：它和传统 SaaS AI 工具不同，重点不是把所有东西关进云端，而是把本地 agent、文件系统、用户已有工具链组织起来。

---

## 结论：Open Design 的真正价值，是把 AI 设计变成可组合的本地工程系统

Open Design 最有意思的地方，不是它“复刻了 Claude Design 的界面”。

它真正值得看的是这几个抽象：

- **Agent adapter**：把不同 coding agent CLI 接入同一个设计工作流；
- **Skill registry**：把设计能力变成可版本化、可分发的文件夹；
- **Design-system resolver**：把品牌 taste 从 prompt 黑箱里拉成 `DESIGN.md`；
- **Craft rules**：把通用审美纪律产品化；
- **Artifact store**：让生成结果成为真实文件，而不是一次性聊天输出；
- **Local daemon**：把危险能力留在用户机器上，同时给 Web UI 一个干净接口。

这套组合说明一个趋势：下一代 AI 创意工具不会只是“更会画图的模型”，而会越来越像一个 **本地优先的生产系统**。模型负责生成，agent 负责操作文件，skills 负责流程，design systems 负责品味，daemon 负责权限和生命周期，UI 负责反馈和可控性。

Open Design 还在快速变化中，但它已经给出了一个很清晰的 builder lesson：

**如果你想做真正可用的 AI 设计产品，不要只优化 prompt。你要先设计一个让 prompt 能安全落地、可重复运行、可审计、可修改、可导出的工程系统。**
