# 影策 open-ai-canvas 源码审计：它不是 AI 生图白板，而是把影视资产、生成任务与 Agent 接成生产图

> **结论先行：** 影策不是一个“在无限画布上摆几张 AI 图片”的前端 demo。它是一套可自托管的 AI 影视工作台：用自研节点画布承载剧本、角色、分镜、图片、视频和音频，用 Go 后端管理素材归属、异步任务、模型渠道、计费与同步，再把 Agent、3D 预演和时间线剪辑接到同一份项目状态上。它也不是新的视频模型，真正的媒体仍由外部模型渠道生成；Agent 写画布与真实模型计费、3D 预演等关键路径，项目文档仍明确标记为需要真实环境验收。

![影策画布中的角色参考、分镜表、图片和视频节点](imgs/open-ai-canvas-ai-film-production-graph/storyboard-workflow.png)

用户提供的 [`donghaozhang/open-ai-canvas`](https://github.com/donghaozhang/open-ai-canvas) 是 [`ddcat-ai/open-ai-canvas`](https://github.com/ddcat-ai/open-ai-canvas) 的 fork，不是独立实现。本文固定审计 fork 的提交 [`27c8066`](https://github.com/donghaozhang/open-ai-canvas/tree/27c8066e6da9f0d4754dc0e5c40097049fe730cf)，提交日期为 2026 年 10 月 12 日；审计时上游已经领先两个提交，其中一个正是画布同步修复。因此下面的代码结论以这个固定快照为准，不把 fork 状态冒充成上游最新状态。

---

## 01 | “Canvas”不是它的产品边界，而是生产状态的可视化入口

普通 AI 画布通常完成三件事：放节点、拉连线、调用模型。影策的代码把这三件事继续向制片流程扩展：

- 文本、剧本、角色、场景、风格、分镜、图片、视频、音频与绘图都是有业务语义的节点；
- 连线不仅画关系，还决定参考图、首尾帧、音频参考和生成上下文；
- 生成任务有排队、进度、日志、取消、重试、报价、扣费与素材落库；
- 项目层还维护章节、角色资产、分镜表、3D 预演、时间线和版本状态；
- 管理端负责模型渠道、逻辑模型、价格、额度、对象存储、用户和运营数据。

所以它更像一张 **production graph**：画布上的节点是人可以看见和调整的生产对象，后端的任务、资产与权限则是让这些对象能够持续工作的状态机。

![项目工作台把章节、角色资产、画布与进度放在同一项目中](imgs/open-ai-canvas-ai-film-production-graph/project-workbench.png)

这也是它与“套一个 tldraw，再加几个模型按钮”最重要的区别。主创作画布并不是 tldraw。源码自己实现了平移缩放、触控手势、框选、节点拖拽、连线命中、空间索引、层级、LOD 和渲染预算；tldraw 5.2.5 与 Excalidraw 0.18.1 只作为**绘图节点内部的子编辑器**。新绘图默认使用 Excalidraw，旧 tldraw 文档继续兼容；生产构建若要创建 tldraw 绘图，还需要单独配置有效 License Key。

---

## 02 | 它的核心不是“多模型”，而是把模型输出变成可追踪资产

前端不会直接把任意 API 返回的 URL 当成完成。生成请求经过统一任务层，输出先被保存为归属于当前用户的资源，再绑定到节点和素材库。视频成功态之前还要完成资源缓存；删除素材时，后端会检查业务引用。

这条链路解决了 AI 影视工具里常见的三个断点：

1. 模型返回了结果，但刷新后节点找不到原文件；
2. 一次任务返回多张图，后续图片被错误合并或覆盖；
3. 画布看见的是临时 Blob URL，导出、跨设备或再次引用时失效。

模型接入也不是把每家供应商逻辑写进页面。这个快照包含 **102 个 `.yingce-plugin` 协议包**，其中既有图片、视频、音频和文本供应商，也有支付协议。插件清单声明能力、鉴权、端点、请求字段映射、轮询和结果归一化，宿主再负责渠道配置、逻辑模型、能力校验、任务与落库。

这不等于仓库内置了 102 个模型。模型权重和商业 API 都不在代码里，部署者仍需准备自己的渠道、密钥、额度与供应商合同。项目真正提供的是“把异构 API 变成同一套生产任务”的适配层。

---

## 03 | 画布同步已经接近小型数据库协议，但不是多人实时协同

早期无限画布常把整张 JSON 文档反复覆盖。影策当前的 [`canvas-operations-sync`](https://github.com/donghaozhang/open-ai-canvas/blob/27c8066e6da9f0d4754dc0e5c40097049fe730cf/docs/content/docs/backend/canvas-operations-sync.mdx) 改成按对象和字段提交 operation：

```text
browser draft
  ├─ add / update / delete node
  ├─ add / update / delete connection
  └─ set top-level production field
          ↓ mutationId + base version + field baseline
server transaction
          ↓ ownership / conflict / quota / reference validation
receipt + new version
```

每次写入带唯一 `mutationId`，网络中断后可以用同一个 ID 和 payload 重放；不同字段的并发修改可以合并，同一字段基线冲突则明确失败；删除后的迟到更新不会把对象“复活”。浏览器保留已确认基线与待确认操作，恢复网络后继续提交。

这比“最后保存的人覆盖所有人”可靠得多，但文档也明确写着：它**不提供多人实时协同**。它解决的是离线恢复、幂等、局部冲突和删除保护，不是 Figma 式多人光标与 CRDT 协作。

---

## 04 | Agent 的先进之处是受控写入，而不是旁边多了一个聊天框

影策的 Agent 不是只读 README 的问答机器人。代码中已经有持久会话、SSE 事件回放、计划、技能、记忆、画布摘要、结构化读取、写入操作、媒体生成和审批恢复。服务端会把一次写入拆成可解释动作，再检查：

- 当前用户是否拥有目标画布与资源；
- 运行使用的画布快照是否仍然一致；
- 节点类型与字段是否在 capability registry 中允许；
- 操作是否需要审批，审批的 `callHash` 是否仍匹配；
- 收费生成是否已经报价、获批并进入任务系统；
- 重试会不会重复提交一笔已经收费的生成。

这比“让大模型直接输出整张 canvas JSON”稳健。Agent 可以先读取有限摘要，再精读节点；写入经过结构化 operation；收费生成与普通画布修改分开审批；执行记录还能回放到聊天历史。

但这里必须保留一条看似矛盾、其实很重要的边界：项目 README 仍把云端 Agent 概括为“当前只读阶段”，而功能文档已经描述了审批后写入和生成实现，同时标注“真实模型计费与浏览器联调仍待验收”。最保守的解释是：**写入基础设施已经进入源码，项目方尚未把真实部署验收当成稳定承诺。** 本文没有配置付费模型和真实账号，因此不会把代码存在写成端到端已证实。

---

## 05 | 影视工作流不是装饰标签：3D 预演和时间线有独立执行层

![自由画布上的角色参考、生成节点和连接关系](imgs/open-ai-canvas-ai-film-production-graph/production-canvas.png)

项目里有两条常被“AI Canvas”产品省略的下游路径。

第一条是 **3D 导演台**。它使用 Three.js、React Three Fiber 和 Drei，在浏览器中布置演员、白模姿态、灯光、机位与镜头。预演视频不是模型想象出来的文本说明，而是由浏览器视口实际录制，再回写成画布视频节点。当前文档把它称为 3D-BOX 核心 MVP，并明确把复杂场景编辑、Agent 语义写入和多镜头剪辑留在后续阶段。

第二条是 **时间线编辑器**。项目为片段编排、拆分、修剪、字幕转写、预览与服务端导出定义了自己的 command protocol 和插件边界。浏览器负责低延迟预览，服务端负责可复现的最终导出；Whisper 转写与渲染任务进入统一任务中心。它还没有理由替代 Premiere 或 Resolve，但已经不只是“把几段 MP4 下载下来”。

这个设计的价值是让分镜、生成和剪辑共享资产身份：画布上确认的镜头可以进入时间线，预演又能返回画布继续参与下一轮生成，而不是在三个互不认识的工具之间手工搬文件。

---

## 06 | 后台暴露了它真正想做的生意：一套可运营的生成平台

![影策管理端的数据、模型、渠道、用量与成本视图](imgs/open-ai-canvas-ai-film-production-graph/operations-console.png)

如果只看创作端，很容易把影策理解为开源版 AI 白板。管理端则暴露了更完整的产品意图：

- 系统渠道与逻辑模型把同一展示模型映射到多个供应线路；
- 价格档、成本快照、积分、订单和对账支撑内部或商业化运营；
- 请求日志、成功率、延迟、队列与异常定位用于生产排障；
- 本地磁盘、OSS、COS 与 S3 兼容存储负责媒体交付；
- 功能开关、注册策略、公告、品牌外观与用户容量支持多用户实例。

技术栈也服务于这个目标：React 19、Zustand、localForage 和 SSE 负责前端工作区；Gin + GORM 负责 handler/service/repository 分层；本地可用 SQLite，部署可切 PostgreSQL + Redis；Nginx 只暴露 Web 入口；`yingce-agent` 还可以独立容器运行，避免 Agent 进程问题拖垮主 API。

这已经接近“生成型创意 SaaS 的开源底座”。相应地，它也比个人白板更重：数据库迁移、对象存储、队列、密钥、额度、备份和升级都成为部署者责任。

---

## 07 | 我实际验证了什么

我在 Apple Silicon Mac 上检出固定提交 `27c8066`，使用项目指定的 Bun 1.3.9 与本机 Go 1.26.3 完成了以下验证：

| 检查 | 结果 | 证据边界 |
|---|---|---|
| 仓库结构 | 4,187 个跟踪文件；1,014 个 `web/src` 文件；941 个后端 Go 文件 | 证明不是单页 demo，不代表代码质量 |
| 协议与技能 | 102 个 `.yingce-plugin` 包；71 个内置 `SKILL.md` | 包含支付协议；不等于 102 个免费模型 |
| 前端依赖 | `bun install --frozen-lockfile` 成功 | 只证明锁文件可安装 |
| 前端静态检查 | TypeScript typecheck 与 ESLint 通过 | 不等于浏览器交互全部正确 |
| 前端测试 | 2,207 项通过、0 项失败，覆盖 304 个测试文件 | 以仓库自动化用例覆盖范围为限 |
| 前端生产构建 | Vite build 成功 | 证明可编译，不证明真实生成链路 |
| 后端测试 | 先按 CI 安装 `backend/agent-runtime/pi` 生产依赖，再运行 `go test -timeout=20m ./...`，全量通过 | 本机未配置 CI 的 PostgreSQL DSN 与 Redis 依赖门槛 |
| Agent runtime 依赖审计 | `npm audit --omit=dev` 报告 2 个 high 条目 | `undici 7.28.0` 为直接依赖，`brace-expansion 5.0.9` 为传递依赖；修复版本可用 |

前端源码约 17.8 万行 TypeScript/TSX，后端约 19.7 万行 Go，后端仓库包含 373 个 Go 测试文件。第一次直接执行 README 中的 `go test ./...` 时，五个 Cloud Agent E2E 用例因找不到 `undici` 失败；项目 CI 实际会先在 `backend/agent-runtime/pi` 执行 `npm ci --omit=dev --ignore-scripts`。补齐这一步后，失败的 `internal/app` 包重跑通过，随后全量后端测试再次通过。这个差异说明 README 的最短验证命令没有完整表达 Agent runtime 的测试前置条件。

依赖审计同样不能省略：审计当日锁定的 Agent runtime 生产依赖会触发两个 high 级别条目，分别涉及直接依赖 [`undici 7.28.0`](https://github.com/advisories/GHSA-w293-vg96-wgc3) 与 `@earendil-works/pi-coding-agent` 下的传递依赖 [`brace-expansion 5.0.9`](https://github.com/advisories/GHSA-qhr7-859c-m2p7)；npm 报告两者都有修复版本。本文没有进一步证明这些漏洞在影策的具体调用方式中可被利用，但公网部署前应升级、复测并重新扫描。

数字说明工程投入很大，但不能替代用户验收。本文没有独立验证真实图片/视频渠道、收费扣款、对象存储、多人负载、3D 成片质量、时间线长片导出或公网升级回滚。

---

## 08 | 它比普通 AI Canvas 先进在哪里，又付出了什么代价

| 维度 | 普通节点画布 | 影策 open-ai-canvas |
|---|---|---|
| 节点 | 通用文本、图片、模型调用 | 剧本、角色、分镜、媒体、绘图、批量表与制片状态 |
| 输出 | 临时 URL 或下载文件 | 任务、资源、素材库、引用与版本绑定 |
| Agent | 聊天或整段 JSON 修改 | 摘要读取、结构化 operation、审批、快照与计费门 |
| 模型 | 页面内写死供应商 | 声明式协议包、渠道、逻辑模型与能力校验 |
| 下游 | 停在生成结果 | 3D 预演、字幕、时间线、服务端导出 |
| 部署 | 静态站或轻服务 | 数据库、队列、对象存储、Agent 容器和运营后台 |

先进之处并不是功能数量，而是**同一份生产状态有明确的归属、事务、任务和审核边界**。这让长流程更容易恢复、追踪和二次编辑。

代价同样真实：系统更难部署，更依赖供应商契约和数据库迁移；前端 bundle 很大；真实媒体调用仍受费用、网络与供应商稳定性约束；Agent 与 3D/剪辑链路的产品验收还没有完全收口。它适合愿意运营一套私有 AI 制片基础设施的团队，不适合只想打开网页偶尔生成一张图的人。

---

## 09 | 部署前最容易忽略的四个边界

1. **不要直接把默认实例暴露公网。** 项目要求先在受控网络注册首个管理员、关闭公开注册、显式设置 CORS、启用 HTTPS，并避免公开后端 8080 端口。
2. **不要把“开源”理解成所有依赖都可无条件商用。** 主项目采用 MIT，但第三方组件沿用各自许可；tldraw 生产使用需要自己的 License Key，默认新绘图引擎因此改为 Excalidraw。
3. **不要把插件数量理解成模型所有权。** API Key、供应商额度、模型可用性和输出授权仍由部署者负责。
4. **不要把测试通过理解成作品通过。** 单元测试和构建能证明代码合同，不能证明一次真实收费生成、长片导出、人物连续性或最终成片审美。

最终最准确的一句话是：**影策不是把模型按钮摆进无限画布，而是在尝试把 AI 影视生产的对象、任务、资产、成本和 Agent 操作变成一张可恢复、可审批、可继续编辑的生产图。它已经有相当厚的工程骨架，但离“部署后自动完成一部片”仍有真实模型、运营、安全与创作验收要补。**

---

## 主要来源

- [用户提供的 `donghaozhang/open-ai-canvas` fork](https://github.com/donghaozhang/open-ai-canvas)
- [官方上游 `ddcat-ai/open-ai-canvas`](https://github.com/ddcat-ai/open-ai-canvas)
- [固定审计提交 `27c8066`](https://github.com/donghaozhang/open-ai-canvas/tree/27c8066e6da9f0d4754dc0e5c40097049fe730cf)
- [项目 README 与架构、安全边界](https://github.com/donghaozhang/open-ai-canvas/blob/27c8066e6da9f0d4754dc0e5c40097049fe730cf/README.md)
- [功能清单与真实环境验收说明](https://github.com/donghaozhang/open-ai-canvas/blob/27c8066e6da9f0d4754dc0e5c40097049fe730cf/docs/content/docs/overview/features.mdx)
- [画布 operations 同步协议](https://github.com/donghaozhang/open-ai-canvas/blob/27c8066e6da9f0d4754dc0e5c40097049fe730cf/docs/content/docs/backend/canvas-operations-sync.mdx)
- [Agent HTTP 合同与审批边界](https://github.com/donghaozhang/open-ai-canvas/blob/27c8066e6da9f0d4754dc0e5c40097049fe730cf/docs/content/docs/backend/http-api.mdx)
- [时间线编辑器集成边界](https://github.com/donghaozhang/open-ai-canvas/blob/27c8066e6da9f0d4754dc0e5c40097049fe730cf/docs/adr/0001-editor-integration-boundary.md)
- [安全策略](https://github.com/donghaozhang/open-ai-canvas/blob/27c8066e6da9f0d4754dc0e5c40097049fe730cf/SECURITY.md)
- [前端依赖与验证命令](https://github.com/donghaozhang/open-ai-canvas/blob/27c8066e6da9f0d4754dc0e5c40097049fe730cf/web/package.json)

*审计日期：2026 年 10 月 13 日。项目功能、star、fork、release 与上游提交会继续变化；技术结论固定到提交 `27c8066`。产品能力描述以项目源码和文档为依据，涉及真实模型效果、计费、3D 预演与长片交付的结论均未作独立商业环境验证。*
