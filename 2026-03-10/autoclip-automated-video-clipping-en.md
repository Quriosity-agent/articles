# AutoClip: AI-Powered Video Clipping and Highlight Generation — A Source Code Deep Dive

> Repository: https://github.com/zhouxiaoka/autoclip

## What Is It?

AutoClip is an open-source AI video clipping system that automatically extracts highlights from long-form videos and generates short-form compilations. It supports downloading from YouTube and Bilibili (B站), analyzes content using large language models (Alibaba's Qwen/Tongyi Qianwen), identifies the best moments, and cuts them into standalone clips.

Think of it as: paste a 2-hour livestream URL → get a dozen polished highlight clips. Very useful for content repurposing and "secondary creation" (二创) workflows.

## Core Features

- **Multi-platform video ingestion**: YouTube, Bilibili URL parsing + download, local file upload
- **AI content analysis**: Uses Qwen (Tongyi Qianwen) LLM for video content understanding and outline extraction
- **Smart clipping**: Automatically identifies topic timestamps, scores each segment for "highlight-worthiness", generates clips
- **Collection generation**: AI-recommended video compilations with drag-and-drop reordering
- **Real-time progress**: WebSocket-based live progress updates and task monitoring
- **Bilibili upload** (in development): Planned auto-upload of clips to Bilibili
- **Subtitle editing** (in development): Visual subtitle editor with sync capabilities

## Architecture

AutoClip uses a modern decoupled frontend/backend architecture:

**Backend:**
- FastAPI (Python web framework)
- Celery + Redis (async task queue)
- SQLite (lightweight DB, upgradable to PostgreSQL)
- yt-dlp (video downloading)
- FFmpeg (video processing)
- Qwen / DashScope API (AI analysis)

**Frontend:**
- React 18 + TypeScript
- Ant Design (UI component library)
- Vite (build tool)
- Zustand (state management)

**Deployment:**
- Docker + Docker Compose for one-click setup
- Manual installation also supported (Python venv + npm)

## The Processing Pipeline: A Deep Dive Into the Source Code

AutoClip processes videos through a 6-step pipeline, each implemented as a dedicated Python module. Let's walk through each step with actual code analysis.

### Step 1: Outline Extraction ([step1_outline.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step1_outline.py))

**Goal:** Extract a structural outline from SRT subtitle files — identify what topics the video covers.

**How it works:**

1. **Parse SRT file**: Uses the `pysrt` library to parse subtitle files, extracting index, timestamps, and text for each entry
2. **Smart chunking**: `TextProcessor.chunk_srt_data()` splits subtitles into ~30-minute blocks. The chunking algorithm doesn't simply cut by time — it searches for "pause points" (gaps > 1 second between subtitles) to avoid splitting mid-conversation
3. **Per-chunk LLM calls**: For each text chunk, loads a prompt template from an external file and sends the subtitle text to the Qwen API
4. **Parse response**: Expects numbered list format (`1. **Topic Name**`), extracts topic titles and subtopics
5. **Merge and deduplicate**: Multiple chunks may produce duplicate topics; deduplication keeps the first occurrence

```python
# Core chunking: ~30-minute intelligent blocks
chunks = self.text_processor.chunk_srt_data(srt_data, interval_minutes=30)

# Per-chunk LLM calls
for i, chunk_file in enumerate(chunk_files):
    input_data = {"text": chunk_text}
    response = self.llm_client.call_with_retry(self.outline_prompt, input_data)
    parsed_outlines = self._parse_outline_response(response, i)
```

**Output format:** Each topic contains `title`, `subtopics` (list), and `chunk_index` (which block it came from).

**Design highlight:** Intermediate results (text chunks, SRT chunks) are persisted to disk in `step1_chunks/` and `step1_srt_chunks/` directories, enabling debugging and checkpoint recovery.

---

### Step 2: Timeline Extraction ([step2_timeline.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step2_timeline.py))

**Goal:** Locate precise time ranges (down to milliseconds) for each topic identified in Step 1.

**How it works:**

1. **Group by chunk_index**: Outlines are grouped by their original chunk
2. **Load corresponding SRT chunks**: Reads the subtitle data from `step1_srt_chunks/`
3. **Build LLM input**: Sends both the outline info and full SRT text to the LLM, asking it to locate start/end times for each topic

```python
# Build SRT text for the LLM prompt
srt_text_for_prompt = ""
for sub in srt_chunk_data:
    srt_text_for_prompt += f"{sub['index']}\\n{sub['start_time']} --> {sub['end_time']}\\n{sub['text']}\\n\\n"

input_data = {
    "outline": [{"title": o.get("title"), "subtopics": o.get("subtopics")} for o in chunk_outlines],
    "srt_text": srt_text_for_prompt
}
```

4. **Parse and validate**: Expects a JSON array with `outline`, `start_time`, `end_time` per item. Validates time format (`HH:MM:SS,mmm`) and clamps times to chunk boundaries if they exceed the range
5. **Retry mechanism**: Up to 2 retries on JSON parse failure, with increasingly strict formatting instructions:

```python
# Retry with reinforced formatting instructions
input_data['additional_instruction'] = """
[IMPORTANT] Output requirements:
1. Must start with [ and end with ]
2. Use English double quotes, not Chinese quotes
3. Quotes in strings must be escaped as \"
4. Do not add any explanatory text or code block markers
5. Ensure JSON format is completely correct"""
```

6. **Global sort and ID assignment**: All chunks' results are merged, sorted by start time, and assigned sequential IDs (1, 2, 3...)

**Robustness:** Raw LLM responses are cached in `step2_llm_raw_output/`, parsed results in `step2_timeline_chunks/`, and failed parse attempts in `debug_responses/`.

---

### Step 3: Highlight Scoring ([step3_scoring.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step3_scoring.py))

**Goal:** Have the LLM score each segment for "highlight-worthiness" and filter to high-quality content.

**How it works:**

1. **Batch by chunk_index**: Same grouping pattern as previous steps
2. **Data sent to LLM**: Each clip's outline, content, and time range

```python
input_for_llm = [{
    "outline": clip.get('outline'), 
    "content": clip.get('content'),
    "start_time": clip.get('start_time'),
    "end_time": clip.get('end_time'),
} for clip in clips]
```

3. **LLM returns**: Expected to return a same-length JSON array with `final_score` (0-1 float) and `recommend_reason` (text explanation) per item
4. **Filtering**: Clips below `MIN_SCORE_THRESHOLD` (configured in `shared_config.py`) are filtered out

**The scoring criteria are entirely defined by the external prompt file** (`recommendation` prompt), not hardcoded. Users can customize scoring behavior by editing the prompt template.

**Output:** Two files — `step3_all_scored.json` (all scores for analysis) and `step3_high_score_clips.json` (filtered high-scorers for subsequent steps).

---

### Step 4: Title Generation ([step4_title.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step4_title.py))

**Goal:** Generate catchy short-video titles for clips that passed the scoring filter.

**How it works:**

1. Group high-score clips by chunk_index
2. Batch send to LLM with clip ID, original outline, content summary, and recommendation reason

```python
input_for_llm = [{
    "id": clip.get('id'),
    "title": clip.get('outline'),
    "content": clip.get('content'),
    "recommend_reason": clip.get('recommend_reason')
} for clip in chunk_clips]
```

3. Expects a `{id: title}` dictionary response, writes to `generated_title` field
4. Falls back to the original outline if title generation fails

**Note:** Final `clips_metadata.json` is deferred to Step 6, avoiding duplicate saves.

---

### Step 5: Topic Clustering ([step5_clustering.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step5_clustering.py))

**Goal:** Group related clips into "collections" (multiple clips concatenated into one video).

**This step uses a fascinating "dual clustering" strategy:**

1. **Keyword pre-clustering**: A hardcoded keyword dictionary provides initial categorization across 8 theme categories:

```python
theme_keywords = {
    '投资理财': ['投资', '理财', '股票', '基金', ...],   # Investment/Finance
    '职场成长': ['职场', '工作', '技能', '学习', ...],   # Career Growth
    '社会观察': ['社会', '现象', '网络', '乱象', ...],   # Social Commentary
    '文化差异': ['文化', '差异', '欧美', '日本', ...],   # Cultural Differences
    '直播互动': ['直播', '互动', '弹幕', '粉丝', ...],   # Livestream Interaction
    '情感关系': ['恋爱', '情感', '社交', ...],          # Relationships
    '健康生活': ['健康', '运动', '跑步', ...],          # Health & Wellness
    '创作平台': ['创作', '平台', 'B站', '小红书', ...] # Content Creation
}
```

Each clip's title + summary is matched against keywords; the highest-scoring theme wins.

2. **LLM fine clustering**: The clip list plus pre-clustering results are sent to the LLM for more intelligent grouping
3. **Fallback cascade**: If LLM clustering is poor (< 3 collections), falls back to pre-clustering results. If that also fails, groups by score (high/medium) as the final fallback

**Collection size is capped by `MAX_CLIPS_PER_COLLECTION`** to prevent overly long compilations.

---

### Step 6: Video Generation ([step6_video.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/pipeline/step6_video.py) + [video_processor.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/utils/video_processor.py))

**Goal:** Use FFmpeg to cut the source video into individual clips and concatenate collections.

**Clip extraction** uses FFmpeg's stream copy mode (no re-encoding), making it extremely fast:

```python
cmd = [
    'ffmpeg',
    '-ss', ffmpeg_start_time,      # Input seeking (faster + more precise)
    '-i', str(input_video),
    '-t', str(duration),           # Duration, not absolute end time
    '-c:v', 'copy',                # Copy video stream, no re-encode
    '-c:a', 'copy',                # Copy audio stream
    '-avoid_negative_ts', 'make_zero',
    '-y',
    str(output_path)
]
```

**Key technical details:**
- `-ss` before `-i` enables input seeking (faster and more precise than output seeking)
- `-t duration` instead of `-to end_time` because input seeking changes the time base
- `copy` mode preserves original quality with near-zero CPU cost

**Collection concatenation** uses re-encoding (since different clips may have different parameters):

```python
cmd = [
    'ffmpeg',
    '-f', 'concat', '-safe', '0',
    '-i', str(concat_file),        # concat demuxer for multi-file joining
    '-c:v', 'libx264',             # H.264 encoding
    '-preset', 'ultrafast',        # Fastest encoding speed
    '-crf', '28',                  # Quality tradeoff for speed
    '-c:a', 'aac', '-b:a', '128k', # AAC audio
    '-movflags', '+faststart',     # Optimize for web streaming
    '-y', str(output_path)
]
```

**File naming:** Clips are saved as `{clip_id}_{sanitized_title}.mp4`; collection assembly finds clips via glob `{clip_id}_*.mp4`.

---

### The LLM Client: The Art of JSON Parsing ([llm_client.py](https://github.com/zhouxiaoka/autoclip/blob/main/backend/utils/llm_client.py))

All pipeline LLM calls go through `LLMClient`. Its most notable feature is the `parse_json_response()` method — a 5-layer fault-tolerance system:

1. **Preprocessing**: Strip non-JSON content (headings, explanatory text) from LLM output
2. **Markdown code block extraction**: Prioritize content from ` ```json ... ``` ` blocks
3. **Direct parsing**: Try `json.loads()` on the sanitized response
4. **Regex matching**: Use generic `\[[\s\S]*\]|\{[\s\S]*\}` regex to find JSON fragments
5. **Auto-repair**: Fix Chinese quotes, missing/trailing commas, single quotes, unquoted field names, mismatched brackets

```python
def fix_common_json_errors(json_str):
    json_str = re.sub(r'}\s*{', '},{', json_str)      # Missing commas
    json_str = re.sub(r',\s*}', '}', json_str)        # Trailing commas
    json_str = re.sub(r"'([^']*?)'\s*:", r'"\1":', json_str)  # Single → double quotes
    # ... plus bracket balancing, etc.
```

This reflects a real-world engineering challenge: **LLM JSON output is frequently imperfect**, requiring multiple layers of error recovery for reliable production use.

---

## Relevance to QCut

As a project closely related to our QCut video editor, AutoClip offers several interesting parallels and lessons:

- **AI Pipeline design**: AutoClip's 6-step pipeline (outline → timeline → scoring → title → clustering → generation) mirrors QCut's native CLI pipeline approach — both decompose complex video processing into composable steps
- **LLM-driven content understanding**: AutoClip uses Qwen to analyze subtitles for content comprehension, aligning with QCut's AI-powered video analysis direction
- **Subtitles as the bridge**: Both projects recognize that subtitle/transcript text is the critical bridge between "language understanding" and "video editing"
- **Automation vs. control**: AutoClip leans fully automatic (input URL → output clips), while QCut emphasizes editor control. Both approaches have their place
- **Externalized prompts**: AutoClip loads all LLM prompts from external files (via `PROMPT_FILES` config), a good practice that lets non-developers tune AI behavior
- **Intermediate file strategy**: Every step persists its results to disk (`step1_chunks/`, `step2_timeline_chunks/`, etc.), enabling checkpoint recovery and debugging — worth adopting

**Key differences:**
- AutoClip targets content repurposing/batch workflows; QCut is a creator-facing editor
- AutoClip depends on Alibaba Cloud's Qwen API; QCut supports multiple AI backends
- AutoClip's frontend is a standalone web app; QCut is a desktop editor
- Step 5's keyword clustering is hardcoded for Chinese livestream/podcast content, limiting generalizability

## Use Cases

- Content repurposing: Extract highlights from long videos for short-form content
- Content operations: Batch process podcasts, interviews, livestream replays
- Video archiving: Auto-organize and categorize video content
- Study notes: Extract key segments from lecture recordings

## Quick Start

```bash
# One-click Docker setup
git clone https://github.com/zhouxiaoka/autoclip.git
cd autoclip
cp env.example .env
# Edit .env with your Qwen/DashScope API key
docker-compose up -d
```

Access `http://localhost:3000` after startup.

## Summary

AutoClip solves a practical problem: automated long-form video clipping. Its 6-step pipeline — from subtitle chunking, outline extraction, timeline localization, highlight scoring, title generation, topic clustering, to final FFmpeg cutting — implements a complete "understand → decide → execute" chain.

Several engineering practices in the source code stand out:

- **Multi-layer JSON parse recovery**: Handling imperfect LLM output with 5 fallback strategies
- **Intermediate file persistence**: Every step saves to disk for checkpoint recovery and debugging
- **Dual clustering strategy**: Keyword pre-classification + LLM fine clustering + score-based fallback
- **FFmpeg stream copy**: Zero re-encoding for individual clips, maximizing speed while preserving quality

For content repurposers, it's a tool worth watching. For those of us building QCut, AutoClip's pipeline design, externalized prompt strategy, and JSON error recovery are all valuable reference points.

---

🦞
