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

## 处理流水线：深入源码分析

AutoClip 的视频处理是一个 6 步 pipeline，每一步都有独立的 Python 模块。下面我们结合源码，逐步剖析每一步的实现细节。

### Step 1：大纲提取（[step1_outline.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step1_outline.py)）

**目标：** 从 SRT 字幕文件中提取视频的结构性大纲——识别出视频讨论了哪些话题。

**核心流程：**

1. **解析 SRT 文件**：使用 `pysrt` 库解析字幕文件，提取每条字幕的序号、起止时间和文本内容
2. **智能分块**：通过 `TextProcessor.chunk_srt_data()` 按约 30 分钟为一个块切分字幕数据。分块算法不是简单的时间切割，而是会寻找字幕之间的"停顿点"（超过 1 秒的间隔），在自然停顿处切分，避免在对话中间断开
3. **逐块调用 LLM**：对每个文本块，从外部 prompt 文件加载提示词模板，将字幕文本注入后调用通义千问 API
4. **解析响应**：期望 LLM 返回编号列表格式（`1. **话题名**`），解析出话题标题和子话题
5. **合并去重**：多个块可能产生重复话题，按标题去重，保留最先出现的版本

```python
# 核心分块逻辑：按 ~30 分钟智能分块
chunks = self.text_processor.chunk_srt_data(srt_data, interval_minutes=30)

# 逐块调用 LLM
for i, chunk_file in enumerate(chunk_files):
    input_data = {"text": chunk_text}
    response = self.llm_client.call_with_retry(self.outline_prompt, input_data)
    parsed_outlines = self._parse_outline_response(response, i)
```

**输出格式：** 每个话题包含 `title`（标题）、`subtopics`（子话题列表）、`chunk_index`（所属块索引）。

**设计亮点：** 中间结果（文本块、SRT 块）都会保存到磁盘的 `step1_chunks/` 和 `step1_srt_chunks/` 目录，方便调试和断点续传。

---

### Step 2：时间线提取（[step2_timeline.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step2_timeline.py)）

**目标：** 为 Step 1 提取的每个话题定位具体的时间区间（精确到毫秒）。

**核心流程：**

1. **按 chunk_index 分组**：将大纲按其原始所属的块进行分组
2. **加载对应 SRT 块**：从 `step1_srt_chunks/` 目录读取对应块的字幕数据
3. **构建 LLM 输入**：将大纲信息和完整的 SRT 字幕文本一起发给 LLM，让模型定位每个话题在字幕中的起止时间

```python
# 构建给 LLM 的输入
srt_text_for_prompt = ""
for sub in srt_chunk_data:
    srt_text_for_prompt += f"{sub['index']}\\n{sub['start_time']} --> {sub['end_time']}\\n{sub['text']}\\n\\n"

input_data = {
    "outline": [{"title": o.get("title"), "subtopics": o.get("subtopics")} for o in chunk_outlines],
    "srt_text": srt_text_for_prompt
}
```

4. **解析与验证**：期望 LLM 返回 JSON 数组，每项包含 `outline`、`start_time`、`end_time`。验证时间格式（`HH:MM:SS,mmm`），并确保时间范围不超出块的边界——如果超出，自动钳位到块的起止时间
5. **重试机制**：如果 JSON 解析失败，最多重试 2 次，并在重试时追加强调 JSON 格式的附加指令

```python
# 重试时强化提示
input_data['additional_instruction'] = """
【重要】输出要求：
1. 必须以[开始，以]结束
2. 使用英文双引号，不要使用中文引号
3. 字符串中的引号必须转义为\"
4. 不要添加任何解释文字或代码块标记
5. 确保JSON格式完全正确"""
```

6. **全局排序与 ID 分配**：所有块的结果合并后，按开始时间全局排序，并分配连续的固定 ID（1, 2, 3...）

**健壮性设计：** 每个块的 LLM 原始响应都保存到 `step2_llm_raw_output/` 目录，解析后的结果保存到 `step2_timeline_chunks/`，还有专门的 `debug_responses/` 目录用于存储解析失败时的原始响应，方便排查问题。

---

### Step 3：精彩度评分（[step3_scoring.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step3_scoring.py)）

**目标：** 让 LLM 对每个话题片段进行"精彩度"评分，筛选出值得切片的高质量内容。

**核心流程：**

1. **按 chunk_index 分组批量处理**：与 Step 2 一样，按块分组后批量调用 LLM
2. **发送给 LLM 的数据**：每个片段的大纲（outline）、内容（content）、起止时间

```python
input_for_llm = [{
    "outline": clip.get('outline'), 
    "content": clip.get('content'),
    "start_time": clip.get('start_time'),
    "end_time": clip.get('end_time'),
} for clip in clips]
```

3. **LLM 返回**：期望返回等长度的 JSON 数组，每项包含 `final_score`（0-1 浮点数）和 `recommend_reason`（推荐理由）
4. **筛选**：低于 `MIN_SCORE_THRESHOLD`（在 `shared_config.py` 中配置）的片段被过滤掉

**评分提示词** 从外部文件 `recommendation` prompt 加载。评分标准由提示词定义，代码层面不做硬编码，这意味着用户可以通过修改提示词来自定义评分策略。

**输出：** 两个文件——`step3_all_scored.json`（全部评分结果，用于分析）和 `step3_high_score_clips.json`（高分片段，用于后续步骤）。

---

### Step 4：标题生成（[step4_title.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step4_title.py)）

**目标：** 为通过评分筛选的高质量片段生成吸引人的短视频标题。

**核心流程：**

1. 将高分片段按 chunk_index 分组
2. 每组批量发送给 LLM，输入包括片段 ID、原始大纲、内容摘要、推荐理由

```python
input_for_llm = [{
    "id": clip.get('id'),
    "title": clip.get('outline'),
    "content": clip.get('content'),
    "recommend_reason": clip.get('recommend_reason')
} for clip in chunk_clips]
```

3. 期望 LLM 返回一个 `{id: title}` 格式的字典，将生成的标题写入 `generated_title` 字段
4. 如果标题生成失败，回退使用原始的 outline 作为标题

**注意：** `clips_metadata.json`（最终元数据）在此步骤不保存，而是推迟到 Step 6 统一保存，避免数据重复。

---

### Step 5：主题聚类（[step5_clustering.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step5_clustering.py)）

**目标：** 将多个片段按主题聚类，生成"合集"（多个相关片段拼接成一个视频）。

**这一步最有意思——它使用了"双重聚类"策略：**

1. **关键词预聚类**：先用硬编码的关键词字典做初步分类。代码内置了 8 个主题类别：

```python
theme_keywords = {
    '投资理财': ['投资', '理财', '股票', '基金', '炒股', '赚钱', '收益', ...],
    '职场成长': ['职场', '工作', '技能', '学习', ...],
    '社会观察': ['社会', '现象', '网络', '乱象', ...],
    '文化差异': ['文化', '差异', '欧美', '日本', ...],
    '直播互动': ['直播', '互动', '弹幕', '粉丝', ...],
    '情感关系': ['恋爱', '情感', '社交', ...],
    '健康生活': ['健康', '运动', '跑步', ...],
    '创作平台': ['创作', '平台', 'B站', '小红书', ...]
}
```

每个片段的标题+摘要与关键词匹配，计算匹配分数，分配到分数最高的主题。

2. **LLM 精细聚类**：将片段列表和预聚类结果一起发给 LLM，让模型给出更智能的合集分组方案
3. **降级策略**：如果 LLM 聚类结果不理想（合集数 < 3），回退使用预聚类结果；如果预聚类也失败，则按评分分组（高分组/中分组）作为最终兜底

**每个合集的片段数量受 `MAX_CLIPS_PER_COLLECTION` 限制**，避免合集视频过长。

---

### Step 6：视频生成（[step6_video.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step6_video.py) + [video_processor.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/utils/video_processor.py)）

**目标：** 用 FFmpeg 将原视频切割成独立的短视频片段，并拼接合集。

**切片生成** 使用 FFmpeg 的 stream copy 模式（无重编码），速度极快：

```python
cmd = [
    'ffmpeg',
    '-ss', ffmpeg_start_time,      # 输入前定位（更精确）
    '-i', str(input_video),
    '-t', str(duration),           # 使用持续时间而非绝对结束时间
    '-c:v', 'copy',                # 复制视频流，不重编码
    '-c:a', 'copy',                # 复制音频流
    '-avoid_negative_ts', 'make_zero',
    '-y',
    str(output_path)
]
```

**关键技术点：**
- `-ss` 放在 `-i` 之前实现 input seeking（比 output seeking 更快更精确）
- `-t duration` 而非 `-to end_time`，因为 input seeking 模式下时间基准不同
- `copy` 模式避免重编码，保留原始画质

**合集拼接** 则不同——使用 H.264 重编码（因为不同片段可能参数不一致）：

```python
cmd = [
    'ffmpeg',
    '-f', 'concat', '-safe', '0',
    '-i', str(concat_file),        # concat demuxer 拼接多个文件
    '-c:v', 'libx264',             # H.264 编码
    '-preset', 'ultrafast',        # 最快编码速度
    '-crf', '28',                  # 质量参数（稍低以换速度）
    '-c:a', 'aac', '-b:a', '128k', # AAC 音频
    '-movflags', '+faststart',     # 优化网络播放
    '-y', str(output_path)
]
```

**文件命名**：切片文件名格式为 `{clip_id}_{sanitized_title}.mp4`，合集拼接时通过 glob `{clip_id}_*.mp4` 查找对应的切片文件。

---

### LLM 客户端：JSON 解析的艺术（[llm_client.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/utils/llm_client.py)）

整个 pipeline 的 LLM 调用都通过 `LLMClient` 统一管理。最值得关注的是它的 JSON 响应解析器 `parse_json_response()`——一个 5 层容错机制：

1. **预处理**：去除 LLM 响应中常见的非 JSON 内容（标题、说明文字）
2. **Markdown 代码块提取**：优先从 ` ```json ... ``` ` 中提取
3. **直接解析**：对清理后的响应直接 `json.loads()`
4. **正则匹配**：用 `\[[\s\S]*\]|\{[\s\S]*\}` 通用正则捕获 JSON 片段
5. **自动修复**：修复中文引号、缺失逗号、多余逗号、单引号、未加引号的字段名、不匹配的括号等常见问题

```python
def fix_common_json_errors(json_str):
    json_str = re.sub(r'}\s*{', '},{', json_str)      # 缺失逗号
    json_str = re.sub(r',\s*}', '}', json_str)        # 多余逗号
    json_str = re.sub(r"'([^']*?)'\s*:", r'"\1":', json_str)  # 单引号→双引号
    # ... 还有括号闭合修复等
```

这反映了一个实际工程中的常见挑战：**LLM 的 JSON 输出经常不完美**，需要层层容错才能可靠运行。

---

## 与 QCut 的关联

作为 QCut 视频编辑器项目的关注者，AutoClip 有几个值得借鉴的地方：

- **AI Pipeline 设计**：AutoClip 的 6 步处理流水线（大纲→时间线→评分→标题→聚类→生成）和 QCut 的 native CLI pipeline 思路类似，都是把复杂的视频处理拆解为可组合的步骤
- **LLM 驱动的内容理解**：AutoClip 用通义千问分析字幕来理解视频内容，这与 QCut 使用 AI 进行视频分析的方向一致
- **字幕作为桥梁**：两者都认识到字幕/转录文本是连接"语言理解"和"视频编辑"的关键桥梁
- **自动化 vs 控制**：AutoClip 偏全自动化（输入链接→输出切片），而 QCut 更强调编辑者的控制权。两种路线各有适用场景
- **Prompt 外置**：AutoClip 将所有 LLM 提示词放在外部文件中（通过 `PROMPT_FILES` 配置），这是一个好实践——允许非开发者调整 AI 行为
- **中间文件策略**：每一步都将中间结果保存到磁盘（`step1_chunks/`、`step2_timeline_chunks/` 等），这种设计让 pipeline 可以断点续传、方便调试，值得学习

**差异点：**
- AutoClip 是面向二创/搬运的批量工具，QCut 是面向创作者的编辑器
- AutoClip 依赖阿里云通义千问 API，QCut 支持多种 AI 后端
- AutoClip 的前端是独立 Web 应用，QCut 是桌面编辑器
- AutoClip 的 Step 5 聚类关键词是为中文直播/播客场景硬编码的，通用性有限

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

AutoClip 解决了一个很实际的问题：长视频的自动切片。通过 6 步 pipeline——从字幕分块、大纲提取、时间线定位、精彩度评分、标题生成、主题聚类到最终的 FFmpeg 切割——实现了完整的"理解→决策→执行"链路。

源码中有几个特别值得注意的工程实践：
- **多层 JSON 解析容错**：处理 LLM 不完美的输出
- **中间文件持久化**：每步结果落盘，支持断点续传和调试
- **双重聚类策略**：关键词预分类 + LLM 精细聚类 + 评分兜底
- **FFmpeg stream copy**：切片时不重编码，速度极快

对于做视频二创的人来说，这是一个值得关注的工具。对于我们做 QCut 的人来说，AutoClip 的 pipeline 设计、prompt 外置策略和 JSON 容错处理都有参考价值。

---

🦞
