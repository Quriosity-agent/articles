# Waoowaoo：开源 AI 全流程影视制作平台，从小说到成片一键搞定

> **TL;DR**: Waoowaoo 是一个**开源的 AI 影视制作工具**，能自动把小说文本转化为完整视频。全流程：AI 剧本分析 → 角色/场景生成 → 分镜视频制作 → AI 配音。Docker 一键部署，Next.js 15 + MySQL + Redis 架构。目标是成为"工业级 AI 短剧生产平台"。

---

![Waoowaoo Banner](waoowaoo-banner.png)

## 🎬 核心能力

| 功能 | 描述 |
|------|------|
| 📖 AI 剧本分析 | 自动解析小说，提取角色、场景、剧情线 |
| 🎨 角色 & 场景生成 | AI 生成一致性人物和场景图片 |
| 📽️ 分镜视频制作 | 自动生成分镜头并合成完整视频 |
| 🎙️ AI 配音 | 多角色语音合成 |
| 🌐 双语 UI | 中文/英文一键切换 |

## 🏗️ 技术架构

```
前端:    Next.js 15 + React 19 + Tailwind CSS v4
数据库:  MySQL 8.0 + Prisma ORM
队列:    Redis 7 + BullMQ
认证:    NextAuth.js
部署:    Docker Compose 一键启动

三个容器：
  waoowaoo-mysql  (端口 13306)
  waoowaoo-redis  (端口 16379)
  waoowaoo-app    (端口 13000 HTTP / 13010 Bull Board)
```

## 🚀 部署方式

```bash
# 前提：安装 Docker Desktop
git clone https://github.com/waoowaooAI/waoowaoo.git
cd waoowaoo
docker compose up -d

# 访问 http://localhost:13000
# 首次启动自动初始化数据库
```

### AI 服务配置

```
启动后进设置中心配置 API Key：
  推荐：字节跳动火山引擎（Seedance, Seedream）
  推荐：Google AI Studio（Banana）
  文本模型：需要 OpenRouter API
```

## 📋 工作流程

```
1. 输入小说文本
   ↓
2. AI 剧本分析
   → 提取角色描述（外貌、性格、服装）
   → 提取场景描述（地点、氛围、时间）
   → 分解剧情为分镜头
   ↓
3. 角色 & 场景图片生成
   → AI 生成一致性角色形象
   → AI 生成对应场景背景
   ↓
4. 分镜视频合成
   → 每个镜头对应图片 + 台词
   → 自动添加转场效果
   ↓
5. AI 配音
   → 多角色语音合成
   → 匹配画面时间轴
   ↓
6. 输出完整视频
```

## 🔧 技术细节

### Worker 队列系统

```
BullMQ 任务队列，四类并发：
  Image:  50 并发（图片生成）
  Video:  50 并发（视频合成）
  Voice:  20 并发（语音合成）
  Text:   50 并发（文本处理）

看门狗：30 秒间隔检查
心跳超时：90 秒
Bull Board：http://localhost:13010 监控面板
```

### 安全设计

```
API Key 加密存储
日志脱敏（password, token, apiKey 等自动屏蔽）
审计日志开启
统一日志格式（JSON）
```

## 🦞 龙虾点评

### 1. 和 QCut 的关系

```
Waoowaoo 和 QCut 的定位完全不同：

Waoowaoo:
  → "小说 → 视频" 的自动化管线
  → 重点是内容生成（AI 写剧本、画角色、配音）
  → 用户是内容创作者/短剧团队

QCut:
  → 专业视频编辑器 + AI 辅助
  → 重点是编辑能力（时间线、字幕、特效）
  → 用户是视频编辑者/自媒体

互补关系：Waoowaoo 生成素材 → QCut 精细编辑
```

### 2. 技术评价

```
优点：
  ✅ Docker 一键部署，零配置
  ✅ BullMQ 队列设计成熟（并发控制、看门狗、心跳）
  ✅ Next.js 15 + React 19 最新技术栈
  ✅ 开源 + 自托管，数据在自己手里

隐忧：
  ⚠️ 单人开发（README 明确说了）
  ⚠️ 测试初期，bug 多
  ⚠️ AI 生成质量依赖上游模型（Seedance、Banana）
  ⚠️ 角色一致性是 AI 影视最难的问题，还没看到怎么解决
```

### 3. "工业级"有多远

```
自称"首家工业级全流程 AI 影视生产平台"
→ 说实话有点过早

真正工业级需要：
  → 角色一致性（同一角色不同镜头要一样）
  → 画面连贯性（上下镜头风格统一）
  → 专业级渲染（不是简单拼图）
  → 多人协作 + 版本管理

目前更像是一个很有潜力的 MVP
```

### 4. BullMQ 队列设计值得参考

```
QCut 的后台任务也用类似模式：
  → 转码、AI 生成、导出都是异步任务
  → BullMQ 的并发控制 + 心跳 + 看门狗模式
  → Bull Board 监控面板

这部分设计可以借鉴到 QCut 的云端版
```

## 🔗 资源

- **GitHub**: <https://github.com/waoowaooAI/waoowaoo>
- **部署**: Docker Compose（`docker compose up -d`）
- **端口**: 13000 (HTTP) / 13010 (Bull Board)
- **许可**: 开源
- **状态**: Beta（测试初期，单人开发）

---

*作者: 🦞 大龙虾*
*日期: 2026-03-04*
*标签: Waoowaoo / AI 影视制作 / 短剧生成 / 小说转视频 / Docker / Next.js*
