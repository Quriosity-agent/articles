# Compositor 源码审计：它不是“AI Photoshop”，而是把图层工程开放成文件系统协议的原生 Mac 编辑器

> **结论先行：** [`robbietilton/Compositor`](https://github.com/robbietilton/Compositor) 首先是一款真的能画、能修、能导入 PSD、能处理 RAW/HDR 的原生 Mac 图像编辑器，而不是套着聊天框的 AI 产品。它最值得关注的设计，是把 `.comp` 工程做成“图片文件 + JSON 清单”的公开目录：Codex、Claude Code 或普通脚本只要会写文件，就能创建和修改可编辑图层；应用通过文件系统事件在约 0.3 秒后重载画布。Agent 不需要插件，也不需要操纵鼠标，人与机器最终交接的是普通图层，而不是一张不可追溯的扁平图。

![Compositor 的主编辑器、画布、变换控件与图层面板](imgs/compositor-agent-native-image-editor/editor.png)

本文固定审计 2026 年 10 月 11 日的提交 [`f5ae5ba`](https://github.com/robbietilton/Compositor/tree/f5ae5bad0b25b32dda9f254e62d2f07f59478698)。审计时仓库有 451 个提交，最新发布版为 [`v1.4.10`](https://github.com/robbietilton/Compositor/releases/tag/v1.4.10)，主分支对应 CI 成功。以下结论以这个快照为准。

---

## 01 | 名字叫 Compositor，但它不是视频合成器

它没有时间线、关键帧、节点图或视频编码管线，不应该拿来和 After Effects、Nuke、Remotion 或 HyperFrame 比。作者给出的产品定位很直接：一款围绕 Photoshop 式合成与后期流程构建的免费开源图像编辑器。

源码里已经存在的核心能力包括：

- 图层、文件夹、透明度、完整的 Photoshop 顺序混合模式；
- 图层蒙版、文件夹蒙版、剪贴蒙版和非破坏变换；
- Curves、Levels、Exposure、Gradient Map、Gaussian Blur 等调整图层；
- 画笔、橡皮、仿制图章、污点修复、Content-Aware Fill、选区和对象/主体选择；
- 可继续编辑的文字和基础形状；
- Camera Raw、RAW develop、色彩与镜头校正；
- JPEG、PNG、HEIC、TIFF、WebP、SVG、RAW、PSD/PSB、EXR 与 Radiance HDR 输入。

这不是“功能清单放在 README 里就算完成”。仓库的 UI 测试会实际启动应用并保存主编辑器、滤镜、Image Size、Hue/Saturation、Camera Raw 与多标签界面截图。下面这张 Camera Raw 截图就是当前主分支成功 CI 的产物。

![CI 实际启动的 Camera Raw 面板](imgs/compositor-agent-native-image-editor/camera-raw.png)

---

## 02 | 真正的新意：`.comp` 不是黑箱文件，而是一份可写协议

一个最小工程就是这样：

```text
Example.comp/
├── manifest.json
└── images/
    ├── <layer-uuid>.png
    └── <layer-uuid>.mask.png
```

`manifest.json` 记录画布尺寸、分辨率、活动图层、图层从下到上的顺序，以及每层的位置、尺寸、旋转、翻转、采样、透明度、混合模式、父文件夹、蒙版、调整参数、文字和效果。像素仍是普通 PNG；16 位图层使用 16-bit PNG，HDR 图层使用 EXR。

这让 `.comp` 同时具备三种身份：

1. 对 Compositor，它是原生可编辑工程；
2. 对 Finder、Git 和备份工具，它是普通文件夹；
3. 对 Coding Agent，它是无需 SDK 的结构化输出协议。

Agent 可以先写图片，再把临时 manifest 原子重命名为 `manifest.json`。应用通过 `DispatchSource` 监听工程目录、manifest 和 images 目录，写入停止 300 毫秒后计算内容摘要；有效变更会在原标签页中重载，并尽量保留缩放、滚动位置和仍存在的图层选择。如果用户有未保存修改，应用会要求在“Revert”和“Keep Mine”之间选择，不会静默覆盖人的工作。

这比“让 Agent 操作 Photoshop 菜单”稳定，也比“模型输出一张 PNG”更可继续编辑。它开放的不是 UI 自动化，而是**作品状态本身**。

---

## 03 | 它为什么对 Codex 有用，又不是什么魔法

普通 Codex 已经会创建 PNG、JSON 和目录，所以不需要专门的 Compositor Skill 才能工作。项目提供的 [`writing-comp-files.md`](https://github.com/robbietilton/Compositor/blob/f5ae5bad0b25b32dda9f254e62d2f07f59478698/docs/writing-comp-files.md) 相当于协议说明：Agent 读完后，就能逐层构图、加入蒙版或调整层，并让人边看边接管。

它比单纯写图片更先进的地方有四个：

- **结果可拆。** 背景、主体、文字、色彩调整和效果可以分层交付；
- **结果可查。** manifest 明确记录每层的位置、混合和关系；
- **结果可接管。** 人可以直接在应用里移动、擦除、改透明度或画蒙版；
- **迭代可见。** Agent 每完成一两层，打开的画布就能刷新，而不必等最终导出。

但 Compositor 不会替 Agent 生成优质像素，也没有语义级“把人物移到左边”的模型接口。Agent 仍要自己调用图像工具、编写栅格程序或处理已有素材，再严格维护 UUID、文件名、尺寸和 manifest。它提供的是一个好的可编辑终点，不是审美模型。

---

## 04 | 渲染不是一句“Metal 加速”能概括的

Compositor 采用的是混合渲染栈：AppKit/SwiftUI 负责原生界面，Core Graphics 承担大量图层绘制，Core Image 处理部分滤镜与 Core Graphics 不正确或不支持的混合模式，Metal 则用于 GPU 画布、画笔覆盖、Liquify/Smudge、噪声与图层效果。部分像素内核用 C 实现。

这套结构有两个务实之处：

- 编辑中的像素按 tile 和 patch 管理，缩小时使用降采样缓存，不需要每一笔都重建整张巨图；
- Metal 路径不可用时，若干效果仍有 CPU/Core Graphics 回退，不把“有 GPU”误写成“所有操作都在 GPU”。

完整混合模式也并非直接相信系统 API。源码明确指出 Core Graphics 的 Color Burn/Color Dodge 在半透明边缘会得到错误结果，另有 Linear Burn、Vivid Light、Hard Mix 等模式根本没有对应实现，因此这些模式转到 Core Image，并强制在 sRGB gamma 空间计算，以接近 Photoshop 行为。

![滤镜菜单展示了从调整、模糊到噪声和背景移除的编辑路径](imgs/compositor-agent-native-image-editor/filter-menu.png)

---

## 05 | PSD、16-bit 与 HDR：能力是真的，边界也很具体

PSD/PSB 导入只承诺 8-bit RGB，不支持 CMYK。文件夹、蒙版、混合模式、填充矩形/椭圆和简单横排文字可以保留可编辑；更复杂的矢量与竖排文字会栅格化。应用会先展示 conversion report，再把结果应用到工程。这更像“尽量保留结构的迁移入口”，不是 Photoshop 文件 100% 往返兼容。

工程格式已经演进到 v13：v12 加入 16-bit PNG 图层，v13 加入 half-float extended-sRGB 的 EXR HDR 图层。高光可以在部分调整与导出路径中继续保留，但当前显示与许多编辑工具仍通过裁到白位、抖动到 8-bit 的代理图像工作；不理解高位深的破坏性操作可能把图层降回 8-bit。

这里还有一个值得警惕的文档漂移：代码把 `ProjectManifest.current` 设为 13，但项目格式文档开头仍写“新保存为 version 12”，Agent 快速示例则使用 version 11，并概括为 8-bit PNG。完整格式文档后半段已经补上 v12/v13。外部写入者若需要 16-bit/HDR，应该固定应用版本并依据当前代码和完整 schema，而不是机械复制 quickstart。

---

## 06 | 文件协议的安全边界比看起来更成熟

项目加载器不会盲信目录内容。它限制：单边 30,000 像素、单文档 10,000 层、manifest 4 MiB、单资源 512 MiB，并按机器内存计算像素预算。图层文件必须位于工程内，文件名必须与 UUID 对应；重复 ID、非法层级、循环蒙版、坏图片和不支持的版本会在替换当前文档前被拒绝。

保存则通过 `NSFileCoordinator` 和原子 package replacement 完成，避免写到一半留下损坏工程。外部变更比较的是 manifest 内容以及图片名称/大小，不依赖容易被同步软件扰动的 mtime。

仍有三个操作边界：

1. 非法外部写入会被忽略，当前画布保持不变，但界面不显示具体错误；Agent 需要自己验证 schema；
2. 外部重载会保留视口和选择，却会清空当前 undo 历史；
3. 若新图片恰好与旧图片字节大小相同，还要同时改变 manifest，否则摘要可能判定为没有变化。

---

## 07 | 我实际验证了什么

我在 Apple Silicon、macOS 26.6.2 上检出固定提交 `f5ae5ba`，使用 Xcode 27 完成 build-for-testing；项目锁定的唯一 Swift Package 外部依赖是 Sparkle 2.10.0。随后按仓库 CI 脚本运行全量单元测试：四组共执行 613 项，613 项通过、0 项失败或跳过。

| 检查 | 结果 | 证据边界 |
|---|---|---|
| 代码规模 | 235 个 Swift 文件，约 52,985 行 Swift | 证明是完整原生应用，不代表每个功能成熟 |
| 本机测试 | 82 个单元测试文件；四组共 613 项通过，0 项失败、0 项跳过 | 测试数不等于独立产品场景数 |
| 本机编译 | `build-for-testing` 成功 | 使用 Xcode 27，项目 CI 固定 Xcode 26.6 |
| 官方主分支 CI | 提交 `f5ae5ba` 的 unit 与 screenshots job 成功 | UI 截图是信息性任务，未到达某页面不会让 workflow 失败 |
| 发布 | v1.4.10 提供签名/公证流程生成的 DMG；发布资产带 SHA-256 | 本文未独立审计 Apple 公证链与自动更新服务 |

第一次启动测试时，Xcode 27 的临时签名让 Sparkle framework 与 App 出现 Team ID 不一致，测试宿主在用例执行前被 dyld 拦截；对本机构建产物重新做 ad-hoc 深度签名后，同一批测试全部执行通过。测试与编译能证明当前快照可构建，文件格式、PSD、渲染和编辑路径有较厚的回归覆盖；它们不能证明对任意大型 PSD 的完全兼容，也不能替代长期使用中的性能与色彩管理验收。

---

## 08 | 它适合谁，不适合谁

它最适合三类人：希望在 Mac 上使用轻量 Photoshop 式编辑器的人；需要把 PSD/RAW/普通图片整理成分层工程的人；以及想让 Codex/Claude 生成“可继续编辑交付物”的 Agent 工作流开发者。

它不适合需要 Windows/Linux、CMYK 印前、Photoshop 插件生态、智能对象完整往返、多人云协作或视频/动效时间线的人。运行门槛也不低：当前要求 Apple silicon 与 macOS 26.0 以上，源码构建要求 Xcode 26 以上。

最终最准确的评价是：**Compositor 并不是靠 AI 自动完成图像编辑，而是把一个真正的原生图层编辑器设计成 Agent 也能读写的开放工程格式。它的突破不在聊天框，而在于人和 Agent 终于可以围绕同一份透明、可验证、可接管的图层状态协作。**

---

## 主要来源

- [项目仓库与 README](https://github.com/robbietilton/Compositor)
- [固定审计提交 `f5ae5ba`](https://github.com/robbietilton/Compositor/tree/f5ae5bad0b25b32dda9f254e62d2f07f59478698)
- [面向 Agent 与脚本的 `.comp` 写入说明](https://github.com/robbietilton/Compositor/blob/f5ae5bad0b25b32dda9f254e62d2f07f59478698/docs/writing-comp-files.md)
- [工程格式 v1-v13](https://github.com/robbietilton/Compositor/blob/f5ae5bad0b25b32dda9f254e62d2f07f59478698/docs/project-format.md)
- [工程加载、校验与原子保存](https://github.com/robbietilton/Compositor/blob/f5ae5bad0b25b32dda9f254e62d2f07f59478698/Compositor/IO/ProjectStore.swift)
- [外部文件变更与热重载](https://github.com/robbietilton/Compositor/blob/f5ae5bad0b25b32dda9f254e62d2f07f59478698/Compositor/IO/ProjectController%2BExternalChanges.swift)
- [GPU 画布](https://github.com/robbietilton/Compositor/blob/f5ae5bad0b25b32dda9f254e62d2f07f59478698/Compositor/Rendering/GPUCanvas.swift)
- [主分支验证 workflow](https://github.com/robbietilton/Compositor/actions/runs/38207213985)
- [v1.4.10 发布页](https://github.com/robbietilton/Compositor/releases/tag/v1.4.10)

*审计日期：2026 年 10 月 13 日。star、fork、版本、功能和文档会继续变化；技术结论固定到提交 `f5ae5ba`。界面图片来自该提交成功 CI 的 screenshots artifact。本文没有独立验证大型商业 PSD、打印色彩链路、Apple 公证或长期生产稳定性。*
