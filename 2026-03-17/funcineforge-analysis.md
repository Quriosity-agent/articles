# FunCineForge：用 AI 给影视剧配音的完整开源方案

> 通义实验室 + 中科大联合开源，从数据集构建到零样本配音模型，一条龙解决影视配音问题。
> 仓库：[FunAudioLLM/FunCineForge](https://github.com/FunAudioLLM/FunCineForge) | 论文：[arXiv:2601.14777](https://arxiv.org/abs/2601.14777) | 演示：[funcineforge.github.io](https://funcineforge.github.io/)

![FunCineForge 项目概览](https://opengraph.githubassets.com/1/FunAudioLLM/FunCineForge)
*图：FunCineForge GitHub 仓库（来源：GitHub / FunAudioLLM）*

---

## 这个项目解决什么问题

影视配音听起来简单，实际坑很多：

1. **没有好数据集**——现有配音数据集规模小、标注粗、词错率高、还只有独白场景
2. **现有模型太弱**——只看嘴唇区域做对齐，复杂实拍场景（镜头切换、多人对话）根本搞不定
3. **人工标注太贵**——传统方式需要大量人工听写和标注，成本高到离谱

FunCineForge 的回答是：**搞一条自动化 pipeline + 一个多模态配音模型，端到端解决。**

---

## 核心架构：两个大块

### 1. 数据集生产 Pipeline（5 步流水线）

这是项目最实用的部分——给你一堆影视剧原始视频，自动生产出高质量配音训练数据：

| 步骤 | 做什么 | 用到的技术 |
|------|--------|-----------|
| ① 标准化 | 视频格式统一、裁剪片头片尾、提取音频 | ffmpeg |
| ② 人声分离 | 把人声和背景音乐/音效分开 | Speech Separation 模块 |
| ③ 视频切片 | 长视频切成句子级片段，生成字幕文件 | VideoClipper (ASR + 时间戳) |
| ④ 说话人识别 | 多模态主动说话人识别，提取面部/唇部数据 | Speaker Diarization（视频+音频） |
| ⑤ CoT 校正 | 用 MLLM 做思维链推理，校正 ASR 和说话人标注 | Gemini / Qwen 等多模态大模型 |

**第 5 步是关键创新**——用通用多模态大模型（推荐 Gemini 3 Pro）做 Chain-of-Thought 校正：

- 输入：音频 + ASR 文本 + RTTM 说话人标注
- 输出：校正后的文本 + 说话人属性（年龄、性别、音色）+ 情感线索
- 效果：**词错率从 4.53% 降到 0.94%，说话人识别错误从 8.38% 降到 1.20%**

比人工标注还准。

### 2. 配音模型（MLLM-based Dubbing Model）

基于多模态大模型的配音模型，核心特点：

- **不只看嘴唇**——利用整个视频场景信息，包括面部表情、场景上下文
- **支持多种场景**——独白、旁白、对话、多人说话
- **零样本配音**——不需要目标说话人的训练数据
- **情感感知**——理解角色情感并反映在语音中

推理代码已开源，消费级 GPU 就能跑：

```bash
cd exps
bash infer.sh
```

---

## CineDub 数据集：用经典影视剧训练

用这套 pipeline 构建了两个数据集：

- **CineDub-CN**：中文电视剧配音数据集（三国演义、红楼梦等经典）
- **CineDub-EN**：英文影视（唐顿庄园等）

每条数据包含极其丰富的标注：

```json
{
  "text": "哎呀，将军，不可连累老夫啊！",
  "speakers": [
    {"id": "1", "age": "中年", "gender": "男", "timbre": "低沉、苍老、颤抖"},
    {"id": "2", "age": "青年", "gender": "男", "timbre": "洪亮、有力、激昂"}
  ],
  "clue": "两名角色对话，第一位中年男性情绪紧张...",
  "emotion": "紧张 0.9"
}
```

这种标注密度在配音数据集里是前所未有的。

---

## CoT 校正的 Prompt 设计值得学习

`cot.py` 里的 prompt 设计非常精细，值得做多模态应用的人参考：

1. **明确角色**——"你是一个专注于中文音频分析和纠错的专家"
2. **分步任务**——确定人数 → 分析属性 → 识别内容 → 匹配说话人 → 总结情感
3. **严格输出格式**——给了完整的 JSON schema 和示例
4. **双语支持**——中英文各一套 prompt，不是简单翻译而是针对语言特点调整

这是工程化 MLLM 应用的教科书级实现。

---

## 对 Builder 的启发

### 直接能用的
- **数据 pipeline 可以直接复用**——如果你在做任何音视频标注项目，这套 5 步流水线省掉 80% 人工
- **CoT 校正思路通用**——用大模型校正专用模型输出，这个范式可以推广到任何标注任务
- **推理代码开源**——消费级 GPU 就能跑配音推理

### 值得关注的限制
- 目前仅支持 Linux
- CineDub 数据集用的是经典影视素材（CC-BY-NC 4.0），商用需注意版权
- 多人配音 API 还在开发中
- 训练代码尚未开源（只有推理）

### 技术方向思考
- **MLLM 做多模态校正**是大趋势——用通用大模型去修正专用小模型的错误，性价比极高
- **影视配音只是开始**——这套 pipeline 稍加修改就能用于有声书、游戏配音、教育视频
- **CosyVoice3 tokenizer** 的集成暗示了和通义语音生态的深度整合

---

## 快速上手

```bash
# 克隆 + 环境搭建
git clone git@github.com:FunAudioLLM/FunCineForge.git
conda create -n FunCineForge python=3.10 -y && conda activate FunCineForge
sudo apt-get install ffmpeg
python setup.py

# 跑推理
cd exps
bash infer.sh
```

如果你想构建自己的配音数据集，按 5 步 pipeline 走就行。最重要的是第 5 步 CoT 校正需要准备一个多模态大模型 API key。

---

## 一句话总结

FunCineForge 是目前最完整的开源影视配音方案——不只给你模型，还给你造数据的工具。通义实验室出品，学术质量有保证，工程质量也在线。

**适合谁：** 做语音合成、影视后期、配音工具、音视频数据标注的团队。

🦞
