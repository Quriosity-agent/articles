---
title: "Mirage Tesseract 深度拆解：Claude 不是直接生成 AEP，而是通过可编辑中间层接入 Adobe 工作流"
date: 2026-10-07
source: "https://x.com/trymirage/status/2107504042205139269"
tags:
  - Mirage Tesseract
  - Adobe Premiere Pro
  - After Effects
  - Claude
  - ChatGPT
  - Agent Skills
  - Editable Video
  - Intermediate Representation
---

# Mirage Tesseract 深度拆解：Claude 不是直接生成 AEP，而是通过可编辑中间层接入 Adobe 工作流

> **TL;DR:** Mirage 宣布 Claude 与 ChatGPT 可以创建 Premiere Pro 的 `.prproj` 和 After Effects 的 `.aep`，也能把现有 Adobe 项目交给 Agent 继续编辑。但这并不是模型突然学会了 Adobe 的全部私有语义。真实架构是：Agent 先操作 Tesseract 的可编辑 `.tsrct` 文档，再由开源 Rust 转换器在 `.tsrct` 与 Adobe 项目之间做有限映射。Premiere 双向转换目前都是 **Partial**，AEP 导出明确为 **Experimental**；表达式、插件、相机、灯光、特效与视觉一致性都可能丢失。它真正重要的地方不是“AI 会写 AEP”这句标题，而是 AI 视频第一次拥有了一个能在 Agent 与专业后期软件之间往返的中间表示。

- **发布原帖:** [Mirage on X](https://x.com/trymirage/status/2107504042205139269)
- **Tesseract:** [产品功能页](https://mirage.app/tesseract/features) / [GitHub 发布仓库](https://github.com/mirage-hq/Tesseract)
- **转换器:** [mirage-hq/Tesseract-Converter](https://github.com/mirage-hq/Tesseract-Converter)
- **兼容性说明:** [官方 Compatibility 页面](https://mrkt.mirage.app/tesseract/converters/compatibility/)
- **核验日期:** 2026-10-07

![Tesseract 把 PRPROJ、AEP 与可编辑 TSRCT 项目连接起来](imgs/mirage-tesseract-adobe-editable-project-ir/01-adobe-tesseract-format-bridge.png)

## 一句话判断

Tesseract 的突破不是让 Claude “原生理解 Adobe”，而是给 Agent 提供了一个相对稳定的**创意中间表示**：Agent 在 `.tsrct` 中修改图层、时间、文字、音频与动画，转换器再把其中可映射的部分翻译成 Premiere 或 After Effects 项目。

它更像编译器里的 IR，而不是 Adobe 的平替：

```text
Claude / ChatGPT / Codex
          ↓
Tesseract Skill + CLI
          ↓
可编辑 .tsrct 项目
       ↙       ↘
  .prproj      .aep
 Premiere   After Effects
```

这层架构解决的是 Agent 如何稳定操作复杂创意文档，而不是如何完整复刻两套成熟桌面软件。

## 发布演示到底展示了什么

Mirage 在原帖中说，Claude 与 ChatGPT 现在可以“natively create” `.prproj` 和 `.aep`，并强调工作流是双向的：既可以让 Agent 创建一个项目交给 Adobe，也可以把已有 Adobe 项目导入 Tesseract，让 Agent 接着做。

主视频用一支赛马动效展示了 Premiere 项目、Tesseract 项目和 Agent 指令之间的关系；回复视频则展示 Claude 调用 `tesseract-adobe-converter`，生成 AEP 文件，再在 After Effects 中打开带时间线与图层的项目。

![Agent 在 Tesseract 中读取时间线并执行“按节拍剪辑”](imgs/mirage-tesseract-adobe-editable-project-ir/02-agent-editing-premiere-timeline.png)

这些画面证明了 Mirage 已经做出可运行的项目转换路径，但不能把演示直接扩大为“任意 AEP 都能无损往返”。官方兼容性文档自己的措辞更准确：这是 **project conversion**，不是渲染视频导出，更不是完整的 Adobe 行为模拟。

## “原生生成”背后的真实实现

开源的 `tsrct-conv` 是一个 Rust CLI。它把 Adobe 项目导入可编辑 `.tsrct`，也能从 `.tsrct` 生成新的 Adobe 项目。转换器不会在原项目上重放全部历史状态，而是读取当前支持的结构，再重新写出一个新项目。

实际流程是：

1. 对 `.aep` 或 `.prproj` 做 `inspect`，列出可选 composition 或 sequence；
2. 检查被选目标用到的音视频是否可访问、是否需要转码；
3. 把一个 composition 或 sequence 转成 `project.tsrct`；
4. Agent 通过 Tesseract Skill 修改这个文档；
5. 再转换为新的 `project.aep` 或 `project.prproj`；
6. 在 Adobe 中重新打开、链接素材、检查警告并渲染验证。

![Claude 中可见的 Tesseract 视频、动效与 Adobe 转换 Skill](imgs/mirage-tesseract-adobe-editable-project-ir/03-tesseract-agent-skills.png)

所以模型主要操作的是 Tesseract 暴露的文档语义与 CLI，不需要自己猜测 AEP 二进制结构。复杂格式由确定性的转换器承担，这比让 LLM 直接拼文件可靠得多。

## 为什么中间表示比“直接操控 Adobe UI”更重要

如果 Agent 只能远程点击 Premiere 或 After Effects，它每一步都受界面布局、焦点、弹窗、插件和机器状态影响。改一百个关键帧，需要一百次脆弱的 UI 操作。

而文档层工作流允许 Agent 直接表达：

- 把某个标题提前 12 帧；
- 将一组图层改为统一缓动；
- 替换素材，同时保留时间与布局；
- 根据音乐节拍重排镜头；
- 批量修改文字、颜色、音量与关键帧；
- 保存新的可编辑版本，再交给人类编辑器接管。

这不是因为 `.tsrct` 比 AEP 更“专业”，而是它把 Agent 能理解的结构、可预测的命令和本地预览集中到一个受控接口中。Adobe 文件在链路两端承担行业交付与人工精修，中间层承担 Agent 自动化。

## Premiere 与 After Effects 支持并不对称

官方兼容表目前给出的状态是：

| 转换方向 | 状态 | 重点边界 |
|---|---|---|
| `.prproj` → `.tsrct` | Partial | 一次选择一个 sequence；部分嵌套、效果、字幕、混音和媒体格式会受限 |
| `.tsrct` → `.prproj` | Partial | 会新建项目；无法原样恢复所有元数据和编辑状态，必要时可能生成 linked AEP |
| `.aep` → `.tsrct` | Partial / best effort | 一次选择一个 composition；表达式、插件、相机、灯光和复杂效果不保证保留 |
| `.tsrct` → `.aep` | Experimental / Partial | 默认 24fps；输出必须在 AE 中打开和渲染核验 |

Premiere 更接近时间线、素材、剪切、基础运动、文本和音频的映射。After Effects 则是任意图层图、表达式系统、插件生态、相机与合成行为的组合，难度明显更高。

转换器 README 还指出，导出 Premiere 时，如果原生 Premiere 结构不足以表示某些画面，可能自动附带一个或多个 linked AEP。这个包会被标记为 `HYBRID-EXPERIMENTAL`，Adobe 接受度、渲染、Alpha、音频和迁移保真度仍未被完整测量。

![生成的 AEP 在 After Effects 中展开为可编辑图层与时间线](imgs/mirage-tesseract-adobe-editable-project-ir/04-after-effects-editable-layers.png)

## 可编辑，不等于无损

这里最容易混淆三个不同标准：

1. **文件能生成:** 转换命令成功退出；
2. **项目能打开:** Premiere 或 AE 接受文件，没有立即报错；
3. **结果等价:** 图层、时间、像素、Alpha、音频、字体与效果都与源项目一致。

前两项不等于第三项。官方文档明确要求保存视觉参考，并检查开头、中段、结尾卡、复杂效果和完整序列。转换警告也可能不是穷尽的；没有警告不代表没有视觉差异。

媒体与字体同样不在项目文件里自动神奇出现。路径失效、编码不兼容、字体缺失或插件不存在，都会让“成功转换”的项目在另一台机器上变样。对于 `.prproj` 导入，检查命令即使成功退出，也可能在 JSON 里报告 `media_admission: blocked`。

## 它与“看着 MP4 重建工程”不是一回事

Tesseract 还有一条 reference-video recreation 工作流：给 Agent 一个 MP4，让它根据可见画面重新搭建可编辑项目。这与 Adobe 项目转换是两类任务。

- **项目转换**读取已有的图层、时间线与素材引用，并映射支持的结构；
- **视频重建**只能观察最终像素，再推断文字、图层、动画与素材关系。

MP4 已经压平了隐藏图层、表达式、关键帧、插件参数和原始素材身份。它可以作为视觉参考，却不能恢复原工程。因此，“导入 AEP”与“照着视频重做”不能被放在同一个准确度层级里。

## 开源的是转换器，不是整套 Tesseract

Mirage 把这次发布称为第一次开源发布。准确说，`Tesseract-Converter` 采用 MIT License，源码公开，主体是 Rust CLI；仓库同时说明，上游开发的 source of truth 位于 `bungeeapp/jerboa` 的 `opensource/conv/`，公开独立仓库是下游分发镜像。

但 Tesseract 主插件不是因此整体开源。主仓库提供 Skill、安装说明、CLI 发布包和文档，插件本身仍受 Mirage 的专有条款约束。当前条款还规定：年营收达到或超过 100 万美元的 for-profit business，若要进行商业使用，需要与 Mirage 签署单独书面协议；竞争性产品用途也受到限制。

这意味着团队评估时必须把两件事分开：

- **转换器源码权利:** MIT；
- **Tesseract 插件与运行时使用权:** Mirage 产品条款。

“转换器开源”不等于“整套创意引擎可以不受限制地嵌入商业产品”。

## 对视频团队真正有用的工作流

比较稳妥的生产路径不是把唯一的客户工程直接交给 Agent，而是建立可回退的交接包：

1. 复制原始 Adobe 项目，保留原件不动；
2. 收集源媒体、字体、插件清单和一份参考渲染；
3. 明确选择一个 sequence 或 composition，不让 Agent 猜第一个目标；
4. 运行 `inspect`，逐项处理缺失、不可读和需转码的媒体；
5. 导入 `.tsrct` 后先在 Tesseract 中验证播放和本地渲染；
6. 让 Agent 只修改已知支持的语义，并保存版本化项目；
7. 以明确 FPS 导出新的 `.prproj` 或 `.aep`，不覆盖旧结果；
8. 在 Adobe 中重新链接素材与字体，检查所有 warning；
9. 对开头、中段、结尾、复杂效果、Alpha 和音频做渲染比对；
10. 人工确认后，才把 Adobe 输出当成后续精修工程。

如果项目高度依赖第三方 AE 插件、表达式、复杂相机、非方形像素或特殊混音结构，当前版本更适合做实验性迁移，而不是承诺无损交付。

## 为什么这件事仍然值得关注

过去的 AI 视频工具大多在两个极端：要么只输出压平的 MP4，要么通过 UI 自动化操作现有软件。前者缺乏可编辑性，后者缺乏稳定性。

Tesseract 选择了第三条路：让 Agent 拥有自己的可编辑项目格式，再为行业工具建立转换边界。即使今天的边界还窄，它已经改变了人机交接的形态：人可以把现有时间线交给 Agent 做批量工作，Agent 也可以把结果作为真实项目交回给剪辑师和动效设计师，而不是只交一条无法拆解的视频。

长期看，最有战略价值的未必是某个特效是否已经支持，而是 `.tsrct` 能否成为足够稳定、足够开放、能被多种 Agent 和创意工具共同读写的文档层。谁控制这层 IR，谁就可能控制 AI 创意工作的工具接口。

## 结论

Mirage 的发布标题很抓人，但更准确的说法是：Claude 与 ChatGPT 现在可以**通过 Tesseract 和确定性转换器，创建或继续编辑一部分 Adobe 项目结构**。

这比“模型直接会写 AEP”少一点魔法，却多了真正的工程价值。它把 Agent 的意图、可编辑文档和专业后期软件连接起来，也把失败边界暴露为可检查的 warning、兼容表和转换日志。

现阶段应把它看成一座仍在施工的桥：Premiere 双向 partial，AEP 导出 experimental，打开文件不等于视觉等价，转换器开源也不等于整套 Tesseract 开源。但方向是清楚的。AI 视频若要进入真实生产，最终交付不能永远只有 MP4；它必须学会把可编辑结构、素材关系和人工接管一起交出去。

## Sources

1. Mirage, X launch post and demo thread
   https://x.com/trymirage/status/2107504042205139269

2. Mirage, Tesseract features
   https://mirage.app/tesseract/features

3. Mirage, Tesseract converter compatibility
   https://mrkt.mirage.app/tesseract/converters/compatibility/

4. mirage-hq, `Tesseract`
   https://github.com/mirage-hq/Tesseract

5. mirage-hq, `Tesseract-Converter`
   https://github.com/mirage-hq/Tesseract-Converter

6. Mirage, Tesseract terms
   https://github.com/mirage-hq/Tesseract/blob/main/TERMS.md

7. Mirage, recreate video use case
   https://mirage.app/tesseract/use-cases/recreate-video
