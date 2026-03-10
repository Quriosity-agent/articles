# AutoClip：AI驱动的智能视频切片与高光提取工具

> 项目地址：https://github.com/zhouxiaoka/autoclip

## 这是什么？

AutoClip 是一个开源的 AI 视频切片处理系统，核心功能是：**从长视频中自动提取精彩片段，生成短视频合集**。支持 YouTube 和 B站视频下载，通过大语言模型（通义千问）分析内容，自动识别高光时刻并切割成独立片段。

简单说，就是把一个2小时的直播/播客/访谈，自动剪成十几个精华短视频。这在二创（二次创作）领域非常实用。

## 核心功能

- **多平台视频获取**：支持 YouTube、B站链接解析下载，也支持本地文件上传
- **AI 内容分析**：基于通义千问（Qwen）大语言模型，自动理解视频内容、提取大纲
- **智能切片**：自动识别话题时间点，对每个片段进行精彩度评分，生成切片
- **合集生成**：AI 推荐视频合集组合，支持拖拽排序和手动编辑
- **实时进度**：WebSocket 实时推送处理进度，任务状态一目了然
- **B站上传**（开发中）：计划支持自动上传切片到B站
- **字幕编辑**（开发中）：可视化字幕编辑与同步

## 技术架构

AutoClip 采用前后端分离架构，技术栈相当现代化：

**后端：**
- FastAPI（Python Web 框架）
- Celery + Redis（异步任务队列）
- SQLite（轻量数据库，可升级 PostgreSQL）
- yt-dlp（视频下载）
- FFmpeg（视频处理）
- 通义千问 / DashScope（AI 分析）

**前端：**
- React 18 + TypeScript
- Ant Design（UI 组件库）
- Vite（构建工具）
- Zustand（状态管理）

**部署：**
- Docker + Docker Compose 一键部署
- 也支持手动安装（Python venv + npm）

## 处理流水线

AutoClip 的视频处理是一个多步骤 pipeline：

1. **素材准备**：下载视频和字幕文件
2. **内容分析**：AI 提取视频大纲和关键信息
3. **时间线提取**：识别话题时间区间
4. **精彩评分**：AI 对每个片段打分
5. **标题生成**：为精彩片段生成吸引人的标题
6. **合集推荐**：AI 推荐视频合集方案
7. **视频生成**：FFmpeg 切割生成最终视频

这个 pipeline 的设计思路很清晰——先理解内容，再做决策，最后执行。每一步都有对应的代码模块（`step1_outline.py`、`step2_timeline.py`、`step3_scoring.py`、`step6_video.py`）。

## 与 QCut 的关联

作为 QCut 视频编辑器项目的关注者，AutoClip 有几个值得借鉴的地方：

- **AI Pipeline 设计**：AutoClip 的多步骤处理流水线（大纲→时间线→评分→生成）和 QCut 的 native CLI pipeline 思路类似，都是把复杂的视频处理拆解为可组合的步骤
- **LLM 驱动的内容理解**：AutoClip 用通义千问分析字幕来理解视频内容，这与 QCut 使用 AI 进行视频分析的方向一致
- **字幕作为桥梁**：两者都认识到字幕/转录文本是连接"语言理解"和"视频编辑"的关键桥梁
- **自动化 vs 控制**：AutoClip 偏全自动化（输入链接→输出切片），而 QCut 更强调编辑者的控制权。两种路线各有适用场景

**差异点：**
- AutoClip 是面向二创/搬运的批量工具，QCut 是面向创作者的编辑器
- AutoClip 依赖阿里云通义千问 API，QCut 支持多种 AI 后端
- AutoClip 的前端是独立 Web 应用，QCut 是桌面编辑器

## 适用场景

- 视频二创：从长视频中提取精彩片段做短视频
- 内容运营：批量处理播客/访谈/直播回放
- 视频归档：自动整理和分类视频内容
- 学习笔记：从课程视频中提取重点段落

## 快速开始

```bash
# Docker 一键启动
git clone https://github.com/zhouxiaoka/autoclip.git
cd autoclip
cp env.example .env
# 编辑 .env，填入通义千问 API Key
docker-compose up -d
```

启动后访问 `http://localhost:3000` 即可使用。

## 总结

AutoClip 解决了一个很实际的问题：长视频的自动切片。它的技术选型现代、架构清晰、部署方便。虽然目前还有一些功能在开发中（B站上传、字幕编辑），但核心的"下载→分析→切片→合集"流程已经完整。

对于做视频二创的人来说，这是一个值得关注的工具。对于我们做 QCut 的人来说，AutoClip 的 AI pipeline 设计和字幕分析思路都有参考价值。

---

🦞
