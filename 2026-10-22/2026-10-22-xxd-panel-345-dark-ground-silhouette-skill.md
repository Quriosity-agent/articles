---
title: "XXD Panel 345：照片转绘 Skill 如何分开审美、生成与交付"
date: 2026-10-22
source: "https://github.com/nevertoday/xxd-panel-345"
verified: 2026-10-24
tags:
  - XXD Panel 345
  - Agent Skill
  - Image-to-Image
  - Art Direction
  - Silhouette
  - Raster Workflow
  - Visual QA
  - Source Audit
---

# XXD Panel 345：照片转绘 Skill 如何分开审美、生成与交付

同一张照片可以保留真实质感，也可以只留下几块足以认出主体的色面。XXD Panel 345 把这两个视图放在一起：一边是摄影，一边是暗底上的平涂剪影静物。

**它是一套带运行规则和辅助脚本的图像 Skill，不是新模型、滤镜引擎或可编辑矢量模板。** 项目固定审美约束，再把原图与交付条件交给已有的图像生成能力。真正值得拆解的，是它怎样防止外层 Agent 随手改风格，又怎样处理比例、文字、批量任务与检查。

![Panel 345 原仓库样例：茶具照片与暗底剪影](imgs/xxd-panel-345-dark-ground-silhouette-skill/sample-01-teapot-top-bottom.png)

*作者提供的 sample-01，1152×1536。下半保留茶具关系，省去图案和真实光影，把茶杯变成视觉亮点。它是原仓库样例，不是本文新生成的结果。*

- 项目：[nevertoday/xxd-panel-345](https://github.com/nevertoday/xxd-panel-345)，README 署名小小东 `@xiaoxiaodong01`
- 固定快照：[`6bad98d`](https://github.com/nevertoday/xxd-panel-345/tree/6bad98d47c8ac83b330da4abcbb949d1726c8e2e)，提交时间为 2026-10-22 UTC
- 核查日期：2026-10-24；阅读源码、检查样例清单、执行有限离线检查，没有安装 Skill 或调用生图服务
- 许可：[PolyForm Noncommercial 1.0.0](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/LICENSE)，不能按 MIT 式自由商用来理解

## 暗底剪影靠什么成立

Panel 345 并不是把原图压暗，再加一层颗粒。它要求重新组织画面：删去大部分环境，把主体和附近少量物件归成一个有遮挡关系的组合；不用轮廓线解释结构，而靠形状和明度区分前后。

颜色仍与照片有关，但不照搬摄影中的每一个亮部。画面压低整体饱和度，用一处接近暖白的亮面建立重点；背景保留深色的色相，而非直接铺纯黑。细颗粒和少量衬线文字负责收尾，不承担主要叙事。[原始审美稿](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/references/original-prompt/zh-CN.md)

从茶具样例可以看出，这种转译牺牲了装饰细节，却保留了壶、杯与托盘的关系。下面的花瓶样例则说明：改成横版之后，样式不需要跟着旋转，变化的是摄影区与设计区的摆放。

![Panel 345 原仓库样例：花瓶左右对照](imgs/xxd-panel-345-dark-ground-silhouette-skill/sample-21-vase-left-right.png)

*sample-21，1536×864。左侧是摄影，右侧重新安排色块、暗底与短词。样例能展示视觉方向，不能保证任意输入都得到同等质量。*

按这套构图逻辑，轮廓清楚的静物更容易作为第一张试稿。多人互动、复杂场景或必须保留细小结构的任务，需要先确认简化会不会损失核心信息。这是选图建议，不是成功率测试结果。

## 原始审美与交付规则各管一层

仓库把风格来源放在 `references/original-prompt/zh-CN.md`，把运行规则放在 `references/soldier-runtime.md`。`SKILL.md` 负责入口和 Panel 345 的专属限制。

这套划分的意义，是让“改成 16:9”只改变交付画布，而不是顺便把暗底、剪影、材质和文字逻辑全部重写。原始稿描述的上下结构可以被当前模式替换，其余审美要求继续保留。[Skill 入口](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/SKILL.md)、[运行适配器](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/references/xxd-panel-345-prompt.en.md)

需要注意，“规则写明了”并不等于程序已经强制执行。递归目录批量、逐图隔离、失败重试和最终审美验收，有相当部分是给宿主 Agent 的工作契约，并非一个 Python 主程序包办的流水线。

四种交付模式也应分开理解：

| 模式 | 最终画面 | 关键边界 |
|---|---|---|
| `top-bottom` | 摄影在上、设计在下 | 两区各半，文字不能变成额外横条 |
| `left-right` | 摄影在左、设计在右 | 两区各半，不能偷偷改回上下布局 |
| `design-only` | 全幅转绘 | 原照只作参考，不占据可见摄影区 |
| `wallpaper-pack` | 四类设备各自一张 | 关联套装借助共同参考，独立套装各自从原图出发 |

模式、尺寸和文字选项可以组合。批量成本也随组合放大：例如六张图、两种普通模式、三种尺寸，已经是 36 个目标输出，还没计入重试。这是按交付组合计算的数量，不是本文测得的费用。[运行契约](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/references/soldier-runtime.md)

## 四个脚本做什么，不做什么

| 文件 | 代码实际承担的工作 | 不应误认的能力 |
|---|---|---|
| `configured_imagegen.py` | 对接已配置的兼容图像接口，发送生成或编辑请求，解码并保存 PNG | 没有模型权重；也不是对所有宿主都适用的万能接入层 |
| `compose_panel.py` | 解析尺寸、计算半幅、裁切拼接、估计分界线位置 | 不会判断主体是否认得出、剪影是否漂亮或文案是否正确 |
| `panel_preferences.py` | 校验并存储交付偏好，拒绝白名单外字段 | 不负责保存源图、创作内容或完整任务状态 |
| `check_samples.py` | 检查清单、文件哈希、PNG 尺寸及验收标记 | 读取 `visual_review: passed`，不代表它自己完成了视觉审美判断 |

桥接脚本有实质代码，但仍依赖现成图像服务。它的配置探测把若干 HTTP 状态视为接口可达，不能据此保证指定模型、额度和参考图编辑一定可用。输出尺寸不匹配时还可能用 `ImageOps.fit` 裁切适配；像素尺寸正确，并不等于构图没有受损。[桥接实现](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/scripts/configured_imagegen.py)

正常流程按运行文档优先让模型一次生成完整画布，拼接脚本是检查或特定保真需求下的辅助。因此，不能把“双联图”理解成默认先生成两个面板、再由 Python 拼接，也不能把模型生成的摄影区域视为逐像素复制。[执行规则](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/references/soldier-runtime.md#bitmap-execution)

## 一个可复现的验收边界

本次对四个 Python 文件做了语法解析，并通过 10 项离线函数断言，覆盖半幅几何、奇数尺寸拒绝、偏好字段过滤和请求地址转换。没有读取本机图像服务配置或凭据，也没有发出生图请求。

还特意做了一次反例：把实际为 `1152×1536` 的 sample-01，交给审计命令并要求 `1152×1538`。

```text
size       OFF — requested 1152x1538, got 1152x1536
...
verdict    OK — the split is effectively exact.
```

命令退出码仍为 0。这里最后的 `OK` 指分界线，而不是尺寸、内容和审美全部通过。它说明该检查器的输出更适合人阅读，不能直接拿“退出码 0”充当发布门槛。要自动验收，需分别检查尺寸、分区和内容，并明确失败条件。[审计实现](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/scripts/compose_panel.py)

这个故意设置的错误期望，不是在指责样例尺寸有问题；样例文件本身与仓库清单一致。

## 40 张样例证明了什么

样例清单包含 20 张上下对照与 20 张左右对照，记录源提示词哈希、文件哈希、尺寸、主题、Unsplash 图片标识和作者的视觉验收状态。它让展示素材有了可核对的身份，比只放几张没有来源的效果图更容易复查。[样例清单](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/references/samples.json)

但 40 张成品没有给出失败尝试总数、重试成本或跨模型对照，不能据此计算一次成功率。本次只下载并视觉查看其中三张，三张 SHA-256 均与清单相符；没有对全部 40 张文件运行原仓库检查器。

![Panel 345 原仓库样例：马灯与环境的取舍](imgs/xxd-panel-345-dark-ground-silhouette-skill/sample-39-lantern-left-right.png)

*sample-39。右侧明显减少摄影中的反光与背景信息，用较亮的马灯轮廓建立主次；这有助于理解风格，但不是材质还原或结构精度基准。*

## 试用之前，先明确两件事

第一，Skill 不能替代图像生成能力。仓库文档给出的这类调用是交给已安装 Skill 的 Agent 的任务参数，不是独立命令行可执行文件：

```text
/xxd-panel-345 photo.jpg --mode design-only --size 3:4 --text none --prefs off
```

对于非商业个人试验，可以先用一张自己有权使用、轮廓清楚的照片确认风格，再扩展模式。若原照片涉及隐私，应先确认会发给哪个图像服务；本地运行脚本不等于照片不出机器。

第二，仓库采用 **PolyForm Noncommercial 1.0.0**，README 明确把 Skill、提示词、脚本、文档和随附样张都纳入范围。付费设计、商业产品或预期商业应用，不应仅凭公开仓库或会员广告判断已获授权，需向权利方确认相应许可。本文保留了随附图片来源及[原许可文本](imgs/xxd-panel-345-dark-ground-silhouette-skill/UPSTREAM-LICENSE.txt)。[上游许可说明](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/README.en.md#license)

## 最值得借鉴的是分工

Panel 345 展示了一种具体的图像 Skill 组织方式：原始审美稿决定画面语言，运行文档决定交付变量，脚本处理确定性细节，最终视觉结果另行验收。

它能减少每次从零描述风格的成本，却不能把模型的不确定性变成确定性，也不能把一张好看的样例变成对所有照片的质量保证。**把哪些事情交给模型、哪些事情交给脚本、哪些事情仍需人确认写清楚，才是这类仓库真正可复用的部分。**

### 来源与核查记录

- [固定源码快照](https://github.com/nevertoday/xxd-panel-345/tree/6bad98d47c8ac83b330da4abcbb949d1726c8e2e)
- [本次来源、样例哈希与检查范围](imgs/xxd-panel-345-dark-ground-silhouette-skill/SOURCES.md)
- 截至核查时 GitHub tags 与 Releases 查询均为空；存在打包工作流，不等于已有发布包。
- 本文是源码与样例分析，不是新生图测试、模型兼容性认证或商业许可意见。
