# Midjourney 日系复古胶片风格：提示词 + 参数一键出图指南

> **TL;DR**: X 用户 **古一**（@MANISH1027512）整理 Midjourney 仓库，翻出一批未发布的**日系复古胶片风格**AI 生成图。连提示词和关键风格参数一起公开放出，可以直接拿去套用。核心：只要风格骨架不变，题材可以随意换，画面的"胶片味儿"就能出来。

---

## 📸 风格特征

![日系复古胶片示例](midjourney-vintage-cover.jpg)

从封面图可以看出这套风格的核心特征：

```
视觉特征：
  → 90 年代日本学校/教室场景
  → 胶片颗粒感（Fuji Superia / Kodak Gold 色调）
  → 暖黄绿色调 + 低饱和度
  → 柔光 + 轻微过曝/欠曝
  → 室内荧光灯 + 暖色投射
  → 一次性相机 / 35mm 紧凑相机质感
  
情绪：
  → 怀旧、青春、日常
  → 90-00 年代日本青年文化
  → "不经意间拍到的" 自然感
```

## 🎨 风格骨架（核心参数）

根据古一的分享，关键在于**风格骨架**不变：

```
可以固定的（风格骨架）：
  → 胶片质感关键词：film grain, vintage film, analog photography
  → 色调关键词：warm tones, muted colors, low saturation
  → 光线关键词：soft light, natural lighting, fluorescent
  → 相机关键词：35mm film, disposable camera, point-and-shoot
  → 年代关键词：1990s, retro Japanese, nostalgic

可以随意换的（题材）：
  → 人物：学生、老师、上班族、情侣...
  → 场景：教室、车站、便利店、街道...
  → 动作：回头看、走路、坐着发呆...
```

## 💡 Midjourney 提示词模板

### 基础模板

```
[人物描述], [场景描述], Japanese 1990s aesthetic, 
vintage film photography, 35mm film grain, Fuji Superia colors, 
warm muted tones, soft natural lighting, nostalgic atmosphere,
candid shot --ar 3:4 --style raw --stylize 200
```

### 示例提示词

```
# 教室场景
A young woman with glasses in a Japanese classroom, 
looking over her shoulder at the chalkboard,
vintage 35mm film photography, Fuji Superia 400 colors,
warm fluorescent lighting, film grain, 1990s Japan,
candid casual photo --ar 3:4 --style raw --stylize 200

# 便利店场景
A young man standing by a konbini counter at night,
reading a magazine under fluorescent lights,
vintage disposable camera aesthetic, Kodak Gold 200,
warm yellow-green tones, slight overexposure,
1990s Japanese youth culture --ar 4:3 --style raw

# 车站场景
A girl waiting alone at a small Japanese train station,
summer uniform, afternoon golden hour,
analog film photography, expired film colors,
soft grain, nostalgic melancholy --ar 16:9 --style raw
```

## 📋 关键参数说明

| 参数 | 推荐值 | 作用 |
|------|--------|------|
| `--ar` | 3:4 或 4:3 | 模拟胶片相机比例 |
| `--style raw` | raw | 减少 Midjourney 美化，保留粗糙感 |
| `--stylize` | 150-250 | 低值 = 更写实 / 高值 = 更风格化 |
| `--chaos` | 10-30 | 适度随机 = 更自然 |
| `--v` | 6.1+ | 最新版本效果最好 |

### 色调关键词对照

```
富士 Superia:  偏绿 + 暖黄，日常感
柯达 Gold:     偏暖黄 + 饱和，阳光感
柯达 Portra:   柔和肤色 + 低对比，人像首选
Agfa Vista:    偏蓝绿 + 冷调，都市感
过期胶卷:      偏色 + 漏光 + 高颗粒，最有"味道"
```

## 🦞 龙虾点评

### 1. 为什么"骨架不变，题材随意换"有效

```
Midjourney 的生成逻辑：
  prompt 前半段 = 内容（什么人在哪做什么）
  prompt 后半段 = 风格（用什么相机什么色调）

风格关键词固定 = 所有图的"调色板"一致
→ 即使人物和场景不同，看起来也像同一卷胶卷拍的
→ 这就是"风格骨架"的含义
```

### 2. 对 QCut 的相关性

```
QCut 已有 40+ AI 图像生成模型（FLUX、Imagen 等）
这类风格提示词模板可以做成：
  → 预设风格库（用户选"日系胶片"就自动加关键词）
  → 批量生成（同一风格骨架 + 不同题材 = 一组一致的素材）
  → 视频配图自动化
```

### 3. AI 生成 vs 真实胶片

```
AI 生成的"胶片感"其实很难做到 100% 真实：
  ✅ 色调、颗粒感、光线 → 可以模拟
  ❌ 镜头畸变、景深虚化特性 → 容易穿帮
  ❌ 不规则的漏光、划痕 → AI 太"完美"
  
古一的作品之所以好看：
  → 不追求 100% 模拟真实胶片
  → 而是抓住"胶片情绪"的本质：怀旧、温暖、不完美
```

## 🔗 资源

- **原推文**: <https://x.com/MANISH1027512/status/2028988530639421689>
- **作者**: 古一（@MANISH1027512）
- **X Article**: <https://x.com/i/article/2028870795351711746>

---

*作者: 🦞 大龙虾*
*日期: 2026-03-04*
*标签: Midjourney / 日系胶片 / AI 图像生成 / 提示词 / 复古风格 / 风格模板*
