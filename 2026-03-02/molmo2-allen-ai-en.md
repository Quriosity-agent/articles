# Molmo 2: Allen AI Releases State-of-the-Art Open-Source Video Understanding Model That Outperforms GPT-5 and Gemini

> Allen Institute for AI (Ai2) releases Molmo 2, pushing open-source vision-language models from image understanding to a new frontier in video understanding. An 8B parameter model outperforms last year's 72B model, achieving SOTA results with just one-eighth of Meta's training data.

**Released:** December 11, 2025  
**By:** Allen Institute for AI (Ai2)  
**License:** Apache 2.0

![Molmo 2 Hero Image](images/molmo2-og-image.jpg)

---

## 1. What is Molmo 2?

Molmo 2 is the next-generation family of open vision-language models (VLMs) from the Allen Institute for AI (Ai2). Where the original Molmo (2024) redefined open-source image understanding, Molmo 2 extends those capabilities to **video understanding, multi-image reasoning, video tracking, and spatio-temporal grounding**.

Three variants serve different needs:

| Model | Parameters | Base LLM | Vision Encoder | Focus |
|-------|-----------|----------|---------------|-------|
| **Molmo 2 (8B)** | 8 billion | Qwen 3-8B | SigLIP 2 | Best overall performance |
| **Molmo 2 (4B)** | 4 billion | Qwen 3-4B | SigLIP 2 | Efficiency-optimized |
| **Molmo 2-O (7B)** | 7 billion | OLMo | SigLIP 2 | Fully open end-to-end |

The Molmo 2-O (7B) variant deserves special attention—built on Ai2's own OLMo language model, it offers a completely open stack from vision encoder to connector to language model, giving researchers full control over every component.

---

## 2. From Molmo 1 to Molmo 2: Key Breakthroughs

### 2.1 The Leap from Images to Video

The original Molmo made waves in 2024 with its image pointing capability, garnering over 3 million downloads. Molmo 2 takes a quantum leap forward:

- **Native video support**: Processes single images, multi-image sets, and video clips of varying length
- **Spatio-temporal grounding**: Not just describing scenes, but pinpointing where and when events occur
- **Multi-object tracking**: Maintains persistent object IDs across occlusions and re-entries
- **Dense video captioning**: Generates highly descriptive and searchable video narratives

### 2.2 Small Models, Big Capabilities

This is one of Molmo 2's most striking advances. As Ai2's computer vision research lead Ranjay Krishna notes:

> "Perhaps the most exciting part is that our 7B model now outperforms our last year's 72B model. It's a huge reduction in the amount of parameters you need to get really good capabilities."

Molmo 2 (8B) outperforms the original Molmo (72B) on key image pointing and grounding benchmarks, delivering stronger localization and reasoning in a far more efficient package.

### 2.3 A Victory for Data Efficiency

Molmo 2 outperforms Gemini 3 Pro on video tracking while training on just **9.19M videos**—compared to Meta's PerceptionLM which used **72.5M videos**. Achieving better results with one-eighth of the data demonstrates the power of careful curation and grounding-focused training objectives.

---

## 3. Benchmark Results

### 3.1 vs. Closed-Source Models

![Molmo 2 vs Closed Models](images/molmo2-vs-closed.png)

Molmo 2 competes strongly against major proprietary systems:

- **Image reasoning**: On an 11-benchmark average, Molmo 2 (8B) leads all open-weight models, landing just behind GPT-5 and GPT-5 mini, and **ahead of Gemini 2.5 Pro**
- **Human preference**: Molmo 2 (8B) **outperforms GPT-5 and Claude Sonnet 4.5**
- **Short-video QA**: Best open-weight score across 7 benchmarks including NextQA, PerceptionTest, MVBench, and Video-MME
- **Video tracking**: Beats Gemini 3 Pro by a wide margin along with all open-weight alternatives

### 3.2 vs. Open-Source Models

![Molmo 2 vs Open Models](images/molmo2-vs-open.png)

Among open models, Molmo 2 leads comprehensively:

- **Video counting**: Leads all tested open models by a comfortable margin
- **Video tracking**: Outperforms specialized trackers including Sa2VA variants and Molmo + SAM 2 baseline
- **Short-video QA**: The 4B variant delivers nearly identical performance to the 8B, offering excellent efficiency

### 3.3 vs. Previous Molmo Versions

![Molmo 2 vs Molmo 1](images/molmo2-vs-molmo1.png)

Molmo 2 (8B) shows consistent gains over both Molmo (7B) and Molmo (72B) on most core benchmarks, with the largest improvements on grounding and counting tasks like Point-Bench, PixMo-Count, and CountBenchQA. The one exception is InfoQA, where Molmo (72B) retains an edge—though Molmo 2 still substantially improves over Molmo (7B).

---

## 4. Architecture Deep Dive

![Molmo 2 Architecture](images/molmo2-architecture.png)

### 4.1 Overall Design

Molmo 2's architecture consists of three core components:

1. **Vision Encoder (SigLIP 2)**: Converts images or video frames into visual tokens
2. **Lightweight Connector**: Interleaves visual tokens with timestamps, image indices, and text
3. **Language Model Backbone (Qwen 3 or OLMo)**: Processes visual and text tokens jointly for reasoning

A key design choice: visual tokens—even from different frames or images—can **attend to each other**, which significantly boosts multi-image and video performance.

### 4.2 Two-Stage Training

**Stage 1: Pretraining for Alignment and Grounding**
- 60% captioning + 30% pointing + 10% natural language data
- Natural language supervision includes SFT data from Tulu to preserve strong language capabilities

**Stage 2: Multimodal SFT**
- Integrates images, multi-image sets, videos, and pure text
- Categories: captions, image QA, video QA, pointing, tracking, and NLP
- 25,000 training steps, batch size 128, max sequence length 16,384 tokens

### 4.3 Video Processing Strategy

- Samples up to **128 frames** per clip at ≤ 2fps
- ViT encodes frames, patches pooled into 3×3 windows
- Supports **SlowFast strategy**: high resolution on key frames + lower resolution on others, maintaining accuracy while significantly reducing vision tokens

### 4.4 Training Optimizations

- **Token-weighting scheme**: Balances learning across diverse tasks during fine-tuning
- **Sequence packing and message-tree scheduling**: Increases throughput
- **Bi-directional attention between visual tokens**: Further gains on grounding and tracking

---

## 5. Datasets: 9 New Datasets

![Molmo 2 Datasets](images/molmo2-datasets.png)

Molmo 2 constructed an open, video-centric multimodal corpus of over **9 million examples**:

| Dataset | Description | Scale |
|---------|-------------|-------|
| Molmo2-Cap | Dense video captioning | 104K videos + 431K clips |
| Molmo2-AskModelAnything | Human-authored video QA | 140K QA pairs |
| Molmo2-CapQA | Synthetic video QA | 1M QA pairs (200K videos) |
| Molmo2-SubtitleQA | Subtitle reasoning QA | 300K QA pairs (100K videos) |
| Molmo2-VideoPoint | Video pointing | 300K+ queries (160K videos) |
| Molmo2-VideoTrack | Point-based tracking | 3.6K clips; 15K queries |
| Molmo2-MultiImageQA | Multi-image QA | 45K sets; 72K QA |
| Molmo2-MultiImagePoint | Multi-image pointing | 470K+ samples |
| Molmo2-SynMultiImageQA | Synthetic multi-image QA | 188K examples |

At the core is a novel **long-form captioning pipeline**: human annotators narrate video clips in rich spoken descriptions, which are transcribed and enriched with frame-level details from Molmo itself. The resulting captions average hundreds of words per video—significantly denser than typical large-scale video caption datasets.

---

## 6. Open-Source Ecosystem

### Fully Open

Molmo 2's open-source commitment is comprehensive:

- ✅ **Model weights**: Three core variants + specialized pointing and tracking versions
- ✅ **Training data**: All new Molmo 2 datasets + detailed data recipes
- ✅ **Video captions**: 100,000+ unique video captions + 431,000 clip-level captions
- ✅ **Evaluation benchmarks**: Benchmarks and tools for grounded video evaluation
- ✅ **Training code**: Coming soon under open-source license
- ✅ **License**: Apache 2.0

### GitHub & HuggingFace

| Platform | Link | Stats |
|----------|------|-------|
| GitHub (Molmo 1) | [allenai/molmo](https://github.com/allenai/molmo) | ⭐ 874 stars, 92 forks |
| GitHub (Molmo 2) | [allenai/molmo2](https://github.com/allenai/molmo2) | ⭐ 171 stars, 4 forks |
| HuggingFace Models | [allenai/Molmo2-8B](https://huggingface.co/allenai/Molmo2-8B) | 155 likes |
| HuggingFace Collection | [allenai/molmo2](https://huggingface.co/collections/allenai/molmo2) | Models + Data |
| Live Demo | [Ai2 Playground](https://playground.allenai.org/?model=molmo2-8b) | Video upload supported |

---

## 7. Real-World Capabilities

Molmo 2 moves beyond "describe what you see" to "pinpoint where and when it happens":

### Counting and Localization
> **Q:** "How many times does the robot grasp the red block?"  
> **A:** Returns coordinates and timestamps for each grasp event

### Event Detection
> **Q:** "When did the cup fall?"  
> **A:** Returns the timestamp and location of the fall

### Multi-Object Tracking
> **Q:** "Point out every instance where the person in the striped shirt flexes their muscles"  
> **A:** Analyzes the entire clip, emits coordinates and timestamps for each event, maintains a stable ID for the person

### Referring Expression Resolution
> **Q:** "Find the window above the kitchen sink" / "Identify the voice-capturing device held by the woman in yellow"  
> **A:** Resolves referring expressions, localizes relevant regions, returns approximate locations and times

### Advanced Capabilities
- **Anomaly detection**: Flags rare or surprising events
- **Generative video artifact detection**: Points to flaws in AI-generated videos (inconsistent lighting, broken geometry)
- **Subtitle-aware QA**: Combines visual evidence with in-video subtitles

---

## 8. Industry Impact & Analysis

### 8.1 Molmo's Proven Influence

![Molmo Pointing Adoption](images/molmo-pointing-adoption.jpg)

The original Molmo's image pointing capability has already influenced the entire industry. As Ranjay Krishna notes:

> "When [Molmo] was released, our model was able to point and ground its reasoning capabilities directly in the pixels themselves. That capability has been adopted by all of the proprietary models. GPT, Gemini—these all can point and refer to things in the pixels nowadays. We're pushing the boundaries of not just what open science can do, but also what closed science can be capable of."

### 8.2 What This Means for the VLM Community

**1. Video Grounding Becomes the New Standard**  
Just as Molmo made image pointing standard across the open community, Molmo 2 brings video pointing, tracking, and dense captioning to the same level of accessibility.

**2. Data Quality > Data Quantity**  
Training on 9.19M videos to outperform models trained on 72.5M videos is a powerful demonstration that carefully curated, high-quality datasets matter more than raw scale.

**3. The Rise of Small Models**  
An 8B model outperforming a 72B model isn't just engineering optimization—it signals a paradigm shift in VLMs from "scale parameters" to "refine training." For deployment, this means SOTA-level video understanding on consumer GPUs.

**4. The Open-Closed Gap is Narrowing**  
Molmo 2 outperforms GPT-5 and Claude Sonnet 4.5 on human preference, and dominates Gemini 3 Pro on video tracking. Open models aren't just "approaching" proprietary systems—they're surpassing them on key tasks.

**5. The Value of Full-Stack Open Source**  
Molmo 2-O (7B) on OLMo provides a completely open pipeline from LLM to vision encoder. This is crucial for academic research and scenarios requiring full reproducibility.

### 8.3 Competitive Landscape

Where Molmo 2 stands in the current VLM landscape:

- **vs GPT-5 / Claude**: Competitive or superior on human preference and video tracking; gap remains on long-video understanding
- **vs Gemini 2.5 Pro / 3 Pro**: Ahead on image reasoning (vs 2.5 Pro), dominates video tracking (vs 3 Pro)
- **vs Qwen3-VL**: Narrowly ahead of Qwen3-VL-8B on human preference; strong rivals in the open-source tier
- **vs Meta PerceptionLM**: Comparable performance with 1/8th the training data—dramatically better data efficiency
- **vs Eagle2.5-8B**: Eagle has a slight edge on long-video QA

---

## 9. Getting Started

### Installation

```bash
conda create --name transformers4571 python=3.11
conda activate transformers4571
pip install transformers==4.57.1
pip install torch pillow einops torchvision accelerate decord2 molmo_utils
```

### Video QA Example

```python
from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

model_id = "allenai/Molmo2-8B"
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True, dtype="auto", device_map="auto")
model = AutoModelForImageTextToText.from_pretrained(model_id, trust_remote_code=True, dtype="auto", device_map="auto")

messages = [
    {
        "role": "user",
        "content": [
            dict(type="text", text="What is happening in this video?"),
            dict(type="video", video="your_video.mp4"),
        ],
    }
]

inputs = processor.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt", return_dict=True)
inputs = {k: v.to(model.device) for k, v in inputs.items()}

with torch.inference_mode():
    output = model.generate(**inputs, max_new_tokens=2048)

generated_text = processor.tokenizer.decode(output[0, inputs['input_ids'].size(1):], skip_special_tokens=True)
print(generated_text)
```

---

## 10. Conclusion

Molmo 2 isn't just a model update—it's a milestone marking open-source vision-language models' expansion from image understanding to video understanding. Through carefully curated datasets, innovative spatio-temporal grounding capabilities, and efficient architecture design, Ai2 has demonstrated that open models can not only compete with proprietary systems but lead the way on critical dimensions.

For the VLM community, the message is clear: video understanding is no longer the exclusive domain of closed-source giants. Any researcher or developer with a consumer GPU can now run, fine-tune, and extend a SOTA-level video grounding model—and it's completely open.

---

### Links

- 📝 [Blog Post](https://allenai.org/blog/molmo2)
- 📃 [Technical Report](https://allenai.org/papers/molmo2)
- 🎮 [Live Demo](https://playground.allenai.org/?model=molmo2-8b)
- 🤗 [HuggingFace Models](https://huggingface.co/collections/allenai/molmo2)
- 🤗 [HuggingFace Data](https://huggingface.co/collections/allenai/molmo2-data)
- 💻 [GitHub (Molmo 2)](https://github.com/allenai/molmo2)
- 💻 [GitHub (Molmo 1)](https://github.com/allenai/molmo)
