# Cutia：开源的浏览器视频编辑器，CapCut 的平替方案

> **仓库地址：** [github.com/msgbyte/cutia](https://github.com/msgbyte/cutia)
> **协议：** MIT | **技术栈：** Next.js 16 + TypeScript + Bun + Zustand + FFmpeg.wasm
> **一句话：** 隐私优先、无水印、无订阅，直接在浏览器里剪视频。

---

![Cutia GitHub Repository](https://opengraph.githubassets.com/1/msgbyte/cutia)
*图片来源：GitHub — msgbyte/cutia*

## 这东西是什么

Cutia 是一个完全在浏览器里运行的视频编辑器。它的定位很简单：给那些不想付订阅费、不想被水印绑架、也不想被追踪的创作者提供一个够用的剪辑工具。

它 fork 自 OpenCut（commit `#fca99d6`），由 [msgbyte](https://github.com/msgbyte) 组织维护。msgbyte 就是做 Tailchat（开源 IM 平台）的那个团队，在开源社区有一定积累。

## 核心功能

- **时间线多轨编辑** — 视频、音频、文字、贴纸分轨排列
- **实时预览** — 编辑即所见，不用反复导出
- **浏览器端导出** — 用 FFmpeg.wasm 在浏览器里完成导出，无水印
- **本地优先** — 素材不上传服务器，隐私有保障
- **一键部署** — 支持 Vercel 一键部署、Docker 部署

## 技术架构拆解

这是一个 Turborepo monorepo 项目，结构清晰：

```
cutia/
├── apps/
│   └── web/          # Next.js 16 主应用（Turbopack 开发模式）
├── packages/
│   ├── ui/           # 共享 UI 组件（Radix UI + Tailwind）
│   └── env/          # 环境变量管理
├── docker-compose.yaml
└── package.json      # Bun 1.2.18 + Turbo
```

### 值得注意的技术选型

| 层面 | 选择 | 点评 |
|------|------|------|
| **框架** | Next.js 16 + Turbopack | 最新的 Next，开发体验快 |
| **包管理** | Bun 1.2.18 | 比 npm/yarn 快很多 |
| **状态管理** | Zustand | 轻量，适合编辑器这种复杂状态 |
| **视频处理** | @ffmpeg/ffmpeg + @ffmpeg/core | 浏览器端 FFmpeg WASM，核心能力 |
| **音频波形** | wavesurfer.js | 成熟的音频可视化库 |
| **AI 能力** | @huggingface/transformers | 浏览器端推理，可能用于字幕识别等 |
| **认证** | better-auth | 轻量认证方案，可选 |
| **缓存** | Upstash Redis（HTTP） | Serverless 友好 |
| **数据库** | PostgreSQL + Drizzle ORM | 认证启用后才需要 |
| **UI** | Radix UI + Tailwind + Motion | 组件化 + 动画 |
| **拖拽** | @hello-pangea/dnd | 时间线轨道拖拽排列 |
| **i18n** | i18next-toolkit | 多语言支持 |

### 浏览器端 FFmpeg 这事很关键

Cutia 用 `@ffmpeg/ffmpeg` 0.12.x 做浏览器端视频处理。这意味着：
1. 所有视频操作在用户浏览器里完成，服务器零负载
2. 素材不需要上传，隐私问题直接解决
3. 但性能受限于浏览器 WASM 性能，大文件可能吃力

### Hugging Face Transformers 的加入

依赖里有 `@huggingface/transformers`，说明项目计划或已经集成了浏览器端 AI 推理。最可能的用途是自动字幕（ASR）或素材智能识别，全部在本地完成。

## 快速上手

**最简路径（不需要后端服务）：**

```bash
git clone https://github.com/msgbyte/cutia.git
cd cutia/apps/web
cp .env.example .env.local
bun install
bun dev
```

打开 `http://localhost:3000` 就能用。

**完整本地开发（含 Redis + PostgreSQL）：**

```bash
docker compose up redis serverless-redis-http postgres -d
cd apps/web
cp .env.example .env.local
# 配置 .env.local：
# UPSTASH_REDIS_REST_URL="http://localhost:8079"
# UPSTASH_REDIS_REST_TOKEN="cutia_redis_token"
# DATABASE_URL="postgresql://cutia:cutia@localhost:5432/cutia"
# BETTER_AUTH_SECRET="$(openssl rand -base64 32)"
bun run db:migrate
bun run dev
```

## 对 Builder 的价值

1. **学习浏览器端视频编辑的好样本** — 用 FFmpeg.wasm + Canvas 实现完整编辑流程，架构值得参考
2. **可以快速 fork 定制** — MIT 协议，Vercel 一键部署，改改就能变成自己的产品
3. **Monorepo 工程实践** — Turborepo + Bun + Next.js 16 的组合是 2026 年的主流选择
4. **浏览器端 AI** — Hugging Face Transformers 集成是一个值得关注的方向

## 当前状态和局限

**活跃开发中的领域：**
- 预览面板内部（字体/贴纸/特效）
- 导出管线内部

**可以贡献的领域：**
- 时间线交互体验
- 项目管理和可靠性
- 性能优化和 bug 修复
- 预览之外的 UI 改进

**局限：**
- 浏览器端 WASM 处理大视频文件性能有限
- 功能上还不能和 CapCut/剪映完全对标
- 社区还在早期阶段

## 总结

Cutia 不是要取代 Premiere 或 DaVinci，它的目标用户是需要快速剪个视频、不想装软件、不想付费的创作者。技术上，浏览器端 FFmpeg + AI 推理的组合有想象空间。对开发者来说，这是一个架构清晰、容易二次开发的视频编辑器参考实现。

如果你正在做视频相关的产品，Cutia 的代码值得读一读。

🦞
