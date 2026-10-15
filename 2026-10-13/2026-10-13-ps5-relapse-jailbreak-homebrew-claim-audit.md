# Relapse PS5 越狱浪潮审计：7.00–13.60 的内核入口是真的，但“全面失守”和 AI 加速还没有证据

> **结论先行：** [MrWhite 白先生的帖子](https://x.com/neuronxwhite/status/2109987887945248960)抓住了一次真实的 PS5 Homebrew 加速：Relapse 确实把公开利用范围扩到固件 7.00–13.60，一批 Switch、Xbox、PS2 与 PS3 项目也在同一时期出现或快速推进。但帖子把**漏洞入口、Homebrew 运行层、独立模拟器、PC 兼容层和二手硬件行情**压成了同一条因果链。更准确的判断是：PS5 社区得到了一块覆盖面很广的公共底座，不是“所有 PS5 都被破解”，更不是 Relapse 一次性实现了 FPKG、四代主机模拟与 PC 原生运行。

![原帖使用的 Relapse GitHub 卡片](imgs/ps5-relapse-jailbreak-homebrew-claim-audit/source-post-card.jpg)

2026 年 10 月 13 日，原帖称“PS5 防线失守”，列出 FPKG 安装、Switch 与初代 Xbox 模拟、PS2 4K、PS3 实体盘启动、AnyPS5 在 PC 运行《死亡细胞》，以及 GameStop 二手 PS5 Pro 涨到 1,399 美元。两天后，我固定审计了 Relapse 提交 [`dd8e4e0`](https://github.com/ntfargo/Relapse-Exploit/tree/dd8e4e0914c5e9d066ee1f9b056be76cb992c8e0)，并交叉检查了这些下游项目。

最重要的区别只有一句话：**Relapse 提供入口，下游项目提供能力。**

---

## 01 | Relapse 真正交付了什么

Relapse 仓库明确写着支持固件 **7.00–13.60**，源码中也有 33 份对应固件的 offset 表，从 7.00、7.01 一直到 13.60。其公开链路由浏览器阶段和内核阶段组成，最终建立内核读写，并提供加载 Homebrew 程序所需的入口。

这足以证明帖子最核心的技术事实：它不是概念图，而是一条公开、可审计、覆盖多个固件代际的利用链。

但仓库同样写明了限制：浏览器阶段可能需要重试，内核阶段可能卡死或触发主机 panic，使用还可能带来系统不稳定、数据丢失与封号。它的支持表也不是“14.00 以下全部自动成功”：必须命中具体固件、正确环境和当时的下游组件，稳定性更不能从一张范围表推出。

---

## 02 | 为什么它仍然是一次重要变化

![Relapse 与下游 Homebrew 项目的分层关系](imgs/ps5-relapse-jailbreak-homebrew-claim-audit/relapse-ecosystem-layers.svg)

Relapse 的价值不在于自己变成应用商店，而在于降低了下游项目寻找“共同入口”的成本。过去，不同固件、不同漏洞和不同加载方式会把开发者切成小岛；当 7.00–13.60 可以围绕相近的内核读写与程序加载路径协作时，模拟器、驱动、SDK、Homebrew shell 与调试工具更容易共享测试者和基础设施。

从仓库边界看，完整链路至少分成四层：

1. **Relapse：**浏览器与内核利用链；
2. **运行环境：**etaHEN、kstuff、ShadowMountPlus 等独立项目；
3. **图形与开发底座：**PS5 Mesa/RADV、Vulkan、payload SDK 与打包工具；
4. **最终应用：**ProsperoEden、XPSemu、PS5SX2、PS3 实验项目等。

因此，“Relapse 之后很多项目突然可见”是合理观察；“这些能力都由 Relapse 实现”则不成立。

---

## 03 | 逐项核对：哪些是真的，哪些被说大了

![原帖主张的证据矩阵](imgs/ps5-relapse-jailbreak-homebrew-claim-audit/claim-evidence-matrix.svg)

| 原帖主张 | 当前证据 | 审计结论 |
|---|---|---|
| Relapse 支持 7.00–13.60 | README 与 33 份固件 offset 表一致 | **确认** |
| FPKG 已能安装 | 下游 Homebrew 环境已有相关能力；Relapse 仓库本身不是包管理器 | **结果可能成立，归因不准确** |
| Switch 模拟器在 PS5 上运行 | [ProsperoEden](https://github.com/blackbearreloaded/ProsperoEden)公开源码，视频、音频、输入和存档已有验证 | **确认，但仍是 early alpha** |
| 初代 Xbox 与《光环 2》60 帧 | [XPSemu](https://github.com/ZiZc3/XPSemu)是真实的 xemu PS5 移植，支持补丁；仓库没有把“《光环 2》稳定 60 帧”列为验收结果 | **项目确认，具体帧率缺少同等级证据** |
| PS2 游戏 4K | [PS5SX2](https://github.com/Swordpdf/PS5SX2)公开说明支持最高 6 倍内部分辨率与 4K 输出，并列出逐游戏测试 | **确认，但兼容性按游戏变化** |
| PS3 实体盘启动《GT5》 | 原帖没有附演示媒体；公开的 [KB-RPCS3](https://github.com/kamb205/KB-RPCS3)只发布源码，未发布 PS5 二进制，也未把《GT5》列入验证表 | **最多是演示级线索，不是可复现的广泛兼容** |
| AnyPS5 已在 PC 跑 PS5 游戏 | AnyPS5 是独立的 PC 重链接与兼容层项目 | **方向真实，与 Relapse 无因果依赖** |
| AI 加速了这一切 | Relapse 的 README、提交记录与致谢没有 AI 因果披露 | **未证实** |

这张表揭示了一个传播中的常见错位：**“有演示”不等于“有公开可复现版本”，“有项目”不等于“兼容性成熟”，“同一周发生”更不等于“由同一个项目造成”。**

---

## 04 | 模拟器浪潮是真的，但成熟度差得很远

ProsperoEden 是 Eden 的 PS5 移植，使用 PS5 上的 Mesa/RADV Vulkan 路径，提供 0.5 倍到 4 倍渲染比例以及 1080p、1440p、2160p 输出。仓库明确把它称为 early alpha，并提醒兼容性和性能随游戏变化；用户还必须自行提供合法转储的密钥、固件与游戏。

XPSemu 则把 xemu 的 Xbox CPU、NV2A GPU、音频和控制器系统移植到 PS5，仓库状态为 Alpha 2。它确实拥有补丁系统和分辨率缩放，但当前公开 README 不足以证明《光环 2》在完整游玩中稳定达到 60 FPS。把某个补丁、某一场景峰值和完整游戏表现写成同一句话，会抹掉最重要的测试条件。

PS5SX2 的证据最完整：它公开描述 PCSX2 重编译器、Vulkan 渲染器、最高 6 倍内部分辨率与 4K 输出，还维护逐游戏的主机型号、固件、分辨率和帧率记录。这仍不意味着“所有 PS2 游戏都能 4K 满速”，但至少读者可以追溯每个结果的测试边界。

PS3 端则明显更早。KB-RPCS3 Alpha 0.1.0 目前只有源码发布，因许可证组合问题没有可下载 PS5 二进制；仓库公开验证的是《LIMBO》《WWE '12》和《GTA IV》，并明确表示真实硬件截图仍待补充。它不能替原帖里的《GT5》实体盘演示背书，更不能证明 PS5 已获得成熟的 PS3 向后兼容。

---

## 05 | AnyPS5 是另一条方向，不能算作 Relapse 的“后果”

Relapse 解决的是：**怎样在特定旧固件 PS5 上获得 Homebrew 执行基础。**

AnyPS5 解决的是：**怎样把 PS5 的 x86-64 程序重链接成 Windows/Linux 可以加载的进程，再用替代系统库与 Vulkan 图形翻译补齐平台差异。**

它们的目标平台、输入产物和工程难点都不同。AnyPS5 不需要 Relapse 才能在 PC 上开发。原帖提到的 `OverkillLabs/DeadCells-PS5-Native` 曾被 GitHub 搜索索引为基于 AnyPS5 的《死亡细胞》独立 Windows 程序，但在 10 月 15 日审计时仓库已经返回 404；因此这项演示不应被当成持续可复现的公共发布。

关于 AnyPS5 的“原生”究竟意味着什么、进度百分比为何不是游戏完成度，可参阅此前的[完整源码审计](../2026-10-01/2026-10-01-anyps5-native-relinker-progress-metrics-audit.md)。

---

## 06 | 旧固件不是免费午餐

Relapse 的上限是 13.60，而 Sony 持续发布新系统软件。保留旧固件意味着用户可能失去新游戏要求的最低系统版本、PSN 功能、安全修复与正常更新路径；更新到已修补版本，又会失去现有入口。

所以“13.60 及以下有公开入口”不能翻译成“现在买一台 PS5 就能获得全部能力”。固件版本、联网历史、主机型号、下游运行环境和每个项目自己的兼容表，都会改变结果。这里存在的是一笔明确的交换：**Homebrew 可研究性，换取官方生态的及时性与稳定性。**

---

## 07 | 1,399 美元是真的，但不能拿来证明越狱需求

[Tom's Hardware](https://www.tomshardware.com/video-games/playstation/used-ps5-pros-now-cost-usd1-399-at-gamestop-50-percent-more-than-new-ones-retailer-bumps-price-of-refurbished-consoles-as-brand-new-units-remain-out-of-stock)在 10 月 6 日记录了 GameStop 将二手或翻新 PS5 Pro 标到 1,399.99 美元；因此原帖的价格数字有当时证据。

但价格上涨同时发生在新机缺货、官方价格上调和《GTA VI》需求升温的市场环境中。没有销售构成数据能把这 500 美元溢价归因于 Relapse 或 Homebrew。它是一个真实的市场事件，不是漏洞影响力的因果指标。

[Rockstar 官方页面](https://www.rockstargames.com/VI)列出的《GTA VI》发售日是 2026 年 11 月 19 日。至于“多久会被破解”，现有证据无法给出负责任的预测：游戏本身、主机固件、密钥、在线服务与反篡改机制是不同问题。

---

## 08 | “美国越狱违法”也说得过于绝对

美国《数字千年版权法》1201 条原则上限制绕过访问控制，但“任何越狱都违法”不是准确概括。[美国版权局现行 37 CFR §201.40](https://www.copyright.gov/title37/201/37cfr201-40.html)包含目的严格限定的例外，例如满足条件的善意安全研究；游戏保存和主机维修例外也各有非常窄的适用范围。主机维修目前限于光驱维修或更换，并要求恢复被绕过的保护措施。

这些例外不授权盗版、不保证免受其他法律追责，也不自动覆盖一般 Homebrew 使用。准确说法应该是：**法律结果取决于设备取得方式、绕过目的、后续使用、复制与分发行为以及所在司法辖区。** 本文不是法律意见。

---

## 09 | AI 也许降低了移植成本，但这次没有因果证据

AI 编程工具当然可能帮助开发者阅读移植错误、补齐构建脚本、整理日志或快速试验兼容层。AnyPS5 的公开讨论中也能看到开发者提到 AI 助手参与设置或测量。但这只能证明个别工作流使用了 AI，不能证明 Relapse 漏洞由 AI 发现，更不能把多个独立模拟器的出现统一归因于 AI。

更有证据的解释是：宽固件入口、成熟的开源模拟器、PS5 Mesa/RADV 图形驱动、payload SDK、Homebrew 运行层，以及更多可测试主机在同一时间汇合。AI 可能是加速器之一，但不是这条帖子已经证明的主因。

最终，更准确的一句话是：**PS5 没有“一夜全面失守”；它获得了一块覆盖 7.00–13.60 的公共研究底座，使多个长期积累的开源项目更容易在真实主机上汇合。真正的突破是生态协调成本下降，而不是所有游戏、所有固件和所有用途突然可用。**

---

## 主要来源

- [MrWhite 白先生原帖](https://x.com/neuronxwhite/status/2109987887945248960)
- [Relapse Exploit 仓库](https://github.com/ntfargo/Relapse-Exploit)
- [审计固定提交 `dd8e4e0`](https://github.com/ntfargo/Relapse-Exploit/tree/dd8e4e0914c5e9d066ee1f9b056be76cb992c8e0)
- [ProsperoEden](https://github.com/blackbearreloaded/ProsperoEden)
- [XPSemu](https://github.com/ZiZc3/XPSemu)
- [PS5SX2](https://github.com/Swordpdf/PS5SX2)
- [KB-RPCS3](https://github.com/kamb205/KB-RPCS3)
- [AnyPS5](https://github.com/boykopovar/AnyPS5)
- [美国版权局 37 CFR §201.40](https://www.copyright.gov/title37/201/37cfr201-40.html)
- [PlayStation 5 系统软件支持页](https://www.playstation.com/en-us/support/hardware/ps5/system-software/)
- [Rockstar Games：《GTA VI》](https://www.rockstargames.com/VI)

*审计日期：2026 年 10 月 15 日。仓库、兼容表、固件支持与零售价格会继续变化；技术判断固定到文中列出的审计快照。本文只做公开源码与主张核验，不提供漏洞利用、载荷执行、FPKG 安装、密钥提取或盗版操作方法。*
