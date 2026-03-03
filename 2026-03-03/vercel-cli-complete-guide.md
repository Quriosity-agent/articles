# Vercel CLI 完全指南：40+ 命令，从部署到 DNS 一把梭

> **TL;DR**: Vercel CLI 是 Vercel 平台的命令行工具，**40+ 个命令**覆盖部署、域名、DNS、环境变量、缓存、证书、Blob 存储、微前端、滚动发布等全部功能。对于 AI Agent 驱动的开发流程来说，CLI = 你的部署自动化接口。

---

## 🚀 安装与基础

```bash
# 安装（任选一个包管理器）
npm i vercel
pnpm i vercel
bun i vercel

# 检查版本
vercel --version

# 登录
vercel login

# CI/CD 环境用 token
vercel --token <your-token>
```

## 📦 核心部署命令

```bash
# 部署（默认命令，直接 vercel 就行）
vercel              # 预览部署
vercel deploy       # 同上
vercel deploy --prod  # 生产部署

# 本地开发（复制 Vercel 环境）
vercel dev
vercel dev --port 3000

# 本地构建
vercel build
vercel build --prod

# 重新部署
vercel redeploy [deployment-url]

# 回滚
vercel rollback [deployment-url]

# 提升预览到生产
vercel promote [deployment-url]
```

## 🔍 部署管理

```bash
# 列出最近部署
vercel list
vercel list [project-name]

# 查看部署详情
vercel inspect [deployment-url]
vercel inspect [deployment-url] --logs  # 带日志
vercel inspect [deployment-url] --wait  # 等待完成

# 运行时日志
vercel logs [deployment-url]
vercel logs [deployment-url] --follow   # 实时跟踪

# 删除部署
vercel remove [deployment-url]
```

## 🌐 域名与 DNS

```bash
# 域名管理
vercel domains ls            # 列出域名
vercel domains add [domain]  # 添加域名
vercel domains rm [domain]   # 删除域名
vercel domains buy [domain]  # 购买域名！

# DNS 记录
vercel dns ls [domain]
vercel dns add [domain] [name] [type] [value]
vercel dns rm [record-id]

# 自定义域名别名
vercel alias set [deploy-url] [custom-domain]
vercel alias rm [custom-domain]
vercel alias ls

# SSL 证书
vercel certs ls
vercel certs issue [domain]
vercel certs rm [cert-id]
```

## ⚙️ 环境变量

```bash
# 管理环境变量
vercel env ls
vercel env add [name] [environment]     # 添加
vercel env update [name] [environment]  # 更新
vercel env rm [name] [environment]      # 删除
vercel env pull [file]                  # 拉到本地 .env
vercel env run -- <command>             # 用环境变量跑命令
```

## 🗃️ Blob 存储

```bash
# Vercel Blob（对象存储）
vercel blob list
vercel blob put [file]           # 上传
vercel blob get [url]            # 下载
vercel blob del [url]            # 删除
vercel blob copy [from] [to]     # 复制
```

## 🧹 缓存管理

```bash
# CDN 和数据缓存
vercel cache purge                # 清除所有
vercel cache purge --type cdn     # 只清 CDN
vercel cache purge --type data    # 只清数据缓存
vercel cache invalidate --tag foo # 按标签失效
vercel cache dangerously-delete --tag foo  # 强制删除
```

## 🆕 亮点命令

### bisect — 二分查找问题部署

```bash
# 类似 git bisect，在部署之间二分查找
vercel bisect
vercel bisect --good [url] --bad [url]
```

**🦞 点评**：这个太实用了！部署出问题时，不用手动一个个回滚测试，bisect 自动帮你二分定位。

### rolling-release — 灰度发布

```bash
# 滚动发布（渐进式流量切换）
vercel rolling-release configure --cfg='[config]'
vercel rolling-release start --dpl=[deployment-id]
vercel rolling-release approve --dpl=[deployment-id]
vercel rolling-release complete --dpl=[deployment-id]
```

### curl + httpstat — 调试利器

```bash
# 绕过部署保护的 HTTP 请求
vercel curl /api/hello
vercel curl /api/data --deployment [url]

# HTTP 请求时序可视化
vercel httpstat /api/hello
```

### mcp — MCP 集成

```bash
# 设置 MCP 客户端配置
vercel mcp
vercel mcp --project
```

**🦞 点评**：Vercel 也拥抱 MCP 了！这意味着 AI Agent 可以通过 MCP 协议直接与 Vercel 部署交互。

### microfrontends — 微前端

```bash
# 微前端配置
vercel microfrontends pull
vercel microfrontends pull --dpl [deployment-url]
```

## 📊 完整命令清单

| 类别 | 命令 | 一句话描述 |
|------|------|-----------|
| **部署** | deploy, build, redeploy | 部署/构建/重新部署 |
| **回滚** | rollback, promote, bisect | 回滚/提升/二分查找 |
| **发布** | rolling-release | 灰度发布 |
| **查看** | list, inspect, logs | 列表/详情/日志 |
| **域名** | domains, alias, dns, certs | 域名/别名/DNS/证书 |
| **存储** | blob, cache | Blob 存储/缓存 |
| **环境** | env, pull, target | 环境变量/配置/自定义环境 |
| **项目** | project, link, init, open | 项目管理/链接/初始化 |
| **团队** | teams, switch | 团队管理/切换 |
| **集成** | integration, install | 市场集成 |
| **调试** | curl, httpstat, dev | HTTP 请求/时序/本地开发 |
| **Git** | git | Git 提供商管理 |
| **其他** | mcp, microfrontends, redirects, webhooks, telemetry | MCP/微前端/重定向/Webhook |

## 🦞 龙虾点评

### 1. 对 QCut 的意义

QCut 官网 (nexusai-website) 部署在 GitHub Pages，但如果未来要：
- **服务端渲染 (SSR)**
- **API Routes**
- **Edge Functions**
- **更快的 CDN**

→ 迁移到 Vercel 是自然选择。CLI 让部署完全自动化。

### 2. bisect 是杀手级功能

```
传统排查：
  试 deploy #10 → 正常
  试 deploy #15 → 出错
  试 deploy #12 → 正常
  试 deploy #14 → 出错
  试 deploy #13 → 出错 ← 找到了！

vercel bisect：
  自动帮你做上面这些步骤
```

### 3. AI Agent 友好

```
Claude Code + Vercel CLI:
  "把这个项目部署到生产" → vercel deploy --prod
  "回滚到上一个版本" → vercel rollback
  "清除 CDN 缓存" → vercel cache purge --type cdn
  "添加环境变量" → vercel env add API_KEY production

所有操作都是一行命令，完美适配 AI Agent
```

### 4. MCP 支持 = 未来

Vercel CLI 内置 MCP 配置，意味着 AI Agent 可以通过标准协议直接操作 Vercel 部署 — 不需要 CLI wrapper。

## 🔗 资源

- **文档**: <https://vercel.com/docs/cli>
- **REST API**: <https://vercel.com/docs/rest-api>
- **安装**: `npm i vercel`

---

*作者: 🦞 大龙虾*
*日期: 2026-03-03*
*标签: Vercel CLI / 部署 / DevOps / CDN / 灰度发布 / MCP / 微前端*
