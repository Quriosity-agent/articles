# D2R Mobile Build 审计：它把实验性打包变成了可复用交付链，但绿色 Actions 不等于真机可玩

> **结论先行：** [`jiayx/d2r-mobile-build`](https://github.com/jiayx/d2r-mobile-build) 不是另一套 D2R Mobile 兼容层，而是围绕上游源码建立的交付工程：固定源码版本，校验预制输入，在 GitHub 托管的 macOS runner 上编译两档 iOS IPA，再把校验和与构建报告发布到使用者自己的私有 Release。它真正降低的是“准备 Xcode、工具链与打包脚本”的门槛，并没有消灭 Xcode、代码签名、游戏数据授权或真机验证。更重要的是，当前公开 Release 虽然已经由旧流水线成功产出 IPA 与配套 Data，项目仍明确写着尚未在真机验证；10 月 15 日刚切换的新版源码构建第一次运行也在准备阶段失败。它是一套进展很快、工程意识不错的交付链，还不是可把 CI 绿灯直接等同于完整产品的下载站。

![d2r-mobile-build 仓库与构建模板](imgs/d2r-mobile-build-ipa-delivery-pipeline/repository-readme.png)

2026 年 10 月 13 日，X 用户 [`@quc1z`](https://x.com/quc1z/status/2109825251966394654) 回复称，这里提供“打包好的 IPA 和 data 文件”，链接指向 `d2r-mobile-build`。这条帖子解决的是上一篇 [D2R Mobile 源码审计](../2026-10-12/2026-10-12-d2r-mobile-switch-arm64-ios-compatibility-layer.md) 留下的现实问题：兼容层源码存在，不代表普通用户能把它稳定变成可安装产物。

本文审计固定到 2026 年 10 月 15 日主分支提交 [`111f065`](https://github.com/jiayx/d2r-mobile-build/tree/111f065d85f42630eb042f7b868c2f3387225d2f)，并单独核对公开 `v1.0.15` Release 与对应 Actions。仓库两天内变化很大，因此必须把“原帖当时的打包分享”“已发布的旧流水线”和“今天主分支上的新模板”分开理解。

---

## 01 | 它补的是最后一公里，不是游戏兼容层本身

上游 [`jhaizhou-ops/d2r-mobile`](https://github.com/jhaizhou-ops/d2r-mobile) 负责真正困难的运行时：ARM64 程序改写、host 服务、NVN 到 Metal、shader、触控与游戏专项逻辑。`d2r-mobile-build` 不重写这些模块，它围绕上游做四件事：

1. 解析上游最新正式 Release，或锁定用户指定的 branch、tag、commit；
2. 下载带 SHA-256 的 `Prepared Input`，检查结构、文件清单、游戏程序、shader chain 与生成规则兼容性；
3. 在 GitHub Actions 的 `macos-26` runner 上，从所选源码编译 iOS 26 与 iOS 18–25 两个版本；
4. 校验 IPA 大小与摘要，将 IPA、`SHA256SUMS.txt`、`build-report.json` 发布到用户自己的私有 Release。

因此，它与上游的关系更像“可复用的构建与发布系统”。上游回答“这套兼容层怎样运行”，这个仓库回答“怎样让别人得到版本明确、可追溯、可重复更新的安装包”。

---

## 02 | “无需本机 Xcode”是真的，但 Xcode 只是被搬到了云端

项目现在的推荐流程是：用仓库模板创建一个**私有仓库**，配置 `PREPARED_INPUT` Secret，然后手动触发 `Build IPA`。使用者不需要在自己的 Mac 上安装 Xcode，也不需要逐条运行生成脚本。

但工作流本身明确使用 `macos-26` runner，并选择 macOS 26 与 iOS 26.4+ SDK，再调用原生编译工具生成两份 IPA。换句话说：

- 对下载或触发工作流的人，它可以是“本机无 Xcode”；
- 对整个构建系统，它依然是“必须有 Xcode”；
- 对安装环节，它仍然是 unsigned IPA，需要 Sideloadly、AltStore Classic、SideStore 等工具重新签名；
- 对运行环节，它仍然需要与版本匹配的 Data，A14–A16 设备还需要额外的 Legacy 资源包。

这不是文字游戏。它决定了故障边界：云端编译成功不能证明用户签名成功，签名成功不能证明资源导入正确，资源识别成功也不能证明长时间游戏稳定。

---

## 03 | Prepared Input 是这套系统最值得看的设计

新版流程没有每次都从原始商业游戏文件重新生成全部派生物，而是把昂贵且敏感的中间结果收敛成一个有 schema 的 Prepared Input。文档要求其中包含：

- `prepared.json`：格式版本、游戏版本、生产源码提交、每个文件的大小与 SHA-256；
- `source-payload.zip`：生成后的程序、界面资源、overlay 与预编译 Metal 库；
- `shader-chain.lock`：shader 工具链指纹；
- `resource-manifest.json`：匹配 Data 的名称、大小与摘要；
- 编译所需的少量 generated headers 与原生 artwork source。

验证代码不仅检查压缩包摘要，还会拒绝多余文件、路径穿越、异常文件类型、体积越界、payload 摘要不一致，以及“仍需手机现场编译 shader”的输入。它还把 Prepared Input 的 `producer.source_commit` 与当前源码的生成依赖比较：普通 native runtime 修改可以复用缓存；生成规则变化则要求新的输入。

这比“下载一个来历不明的 IPA”强得多，因为构建身份、源码提交、派生输入和最终 IPA 之间开始形成可审计关系。它也比每次把 5GB 以上资源重新塞进 CI 更实际。

---

## 04 | 供应链防护做了不少，但还没有形成完整 provenance

主分支里能看到几项有价值的约束：

- GitHub 官方 Actions 大多锁定到完整 commit SHA，而不是浮动 tag；
- 顶层工作流虽然引用 `pack.yml@main`，`resolve-tools` 会从本次 run 的 `referenced_workflows` 反查精确 40 位提交，再以该提交检出工具代码；
- `require_private()` 会拒绝在公开目标仓库里接触 Prepared Input 或发布游戏构建；
- 中间 native inputs 只保留 3 天，成功发布后会主动删除；
- IPA 上传后再次核对文件大小与 GitHub 返回的 SHA-256 digest；
- 两个系统版本必须使用相同的源码、payload、shader chain、资源清单与构建身份。

但 SHA-256 只能证明“拿到的字节与声明一致”，不能证明这些字节由谁生成、有没有合法分发权、内部是否安全。当前 README 直接提供一份社区 Prepared Input 的固定链接与摘要，也指向社区提供的 5.42GB Data 和约 1.02GB Legacy 包；公开 `v1.0.15` Release 还链接了相应数据 Release。本文没有下载、解密或重新分发这些内容。

这里存在一个必须说清的边界：仓库简介写的是 “Bring your own prepared game archive”，但默认文档实际上把社区包配置直接交给用户。私有仓库、短期 artifact 和摘要校验降低了意外公开与传输损坏的风险，却不会自动解决版权、来源可信度与第三方 runner 接触派生游戏内容的问题。

---

## 05 | Release 成功、Actions 通过、真机可玩是三种证据

![d2r-mobile-build Actions：大量工具检查通过，但新版 Source Build 首次运行失败](imgs/d2r-mobile-build-ipa-delivery-pipeline/actions-workflows.png)

截至审计时，Actions 页面有 110 次 workflow run。大量绿色记录来自 `Check build tools`，它们运行 Python 单元测试，覆盖输入解析、缓存预算、Prepared Input、发布和 Xcode 选择等逻辑。我也在固定提交 `111f065` 上本地运行了同一套测试，24 项全部通过。这证明构建工具有回归检查，不等于完整游戏已在真机运行。

公开 [`v1.0.15`](https://github.com/jiayx/d2r-mobile-build/releases/tag/v1.0.15) 对应的旧 `Build unsigned IPA #41` 在 10 月 15 日用约 11 分钟成功完成，步骤包括下载、解密与校验游戏输入、生成两个 IPA、复用或发布 Data，以及上传报告。Release 中两份 IPA 都约 140MB，并带 GitHub 计算的 SHA-256 digest。这是“云端确实产出了可下载包”的强证据。

![v1.0.15 Release 同时列出两档 IPA、Legacy 与游戏 Data](imgs/d2r-mobile-build-ipa-delivery-pipeline/release-v1.0.15.png)

但同一 Release 的说明也明确写着：**当前包尚未在物理设备验证**。首次 shader 准备时间“iPhone 17 Pro Max 约 6 分钟”只是参考，不是本文复测。

而 10 月 15 日刚合入主分支的新版 `Source build · latest release #1` 在 9 秒后失败，失败点是准备任务里的“固定工具 revision”，后续源码选择、Prepared Input 校验、原生编译和发布全部跳过。随后工具单测继续通过，说明失败集中在可复用 workflow 的运行时解析，而不是 Python 测试本身。

所以当前证据应这样分层：

| 层级 | 当前证据 | 能下的结论 |
|---|---|---|
| 工具代码 | 单元测试多次通过 | 输入、缓存、发布等函数在测试夹具下工作 |
| 旧交付链 | `v1.0.15` workflow 成功并发布两份 IPA | 旧流水线确实生成了可下载产物 |
| 新交付链 | 首次 Source Build 在准备阶段失败 | 主分支的新模板尚未用公开成功 run 证明端到端 |
| 真机 | Release 明示尚未验证 | 不能据此确认安装、首启、长时间游戏与性能 |

---

## 06 | 两档 IPA 和外置 Data，说明项目正在拆开“程序更新”与“内容更新”

`v1.0.15` 提供两个共享应用标识的变体：iOS 26+ 使用 Metal 4，iOS 18–25 使用 Metal 3 兼容构建。安装其中一个会覆盖另一个。游戏 Data 与 IPA 分开，匹配资源已经导入后，普通 native code 更新可以只覆盖安装新 IPA，不必重复搬运数 GB 数据。

这对迭代速度很重要：程序、shader、Data 和旧设备贴图不再被视为一个不可分割的大包。构建报告保存源码提交和资源摘要，理论上可以知道“哪份程序配哪份 Data”。

但这也增加了用户侧状态：系统版本、IPA 变体、签名身份、应用标识、Data revision、Legacy 包与存档必须保持一致。一个下载按钮变少了，版本矩阵并没有消失，只是被显式管理。

---

## 07 | 它今天甚至已经扩展到 Mac，但这不是原帖已经证明的能力

审计当天，主分支新增了 macOS 15–25 与 macOS 26 两档 Apple silicon App 构建。它们同样使用私有 Prepared Input，生成 ad-hoc signed app；首次启动时由用户选择包含 `data/build_manifest.psv` 的 RomFS 文件夹。

这说明仓库正在从“打包好的 iOS IPA 分享”快速演化成 D2R Mobile 的跨 Apple 平台构建模板。不过这些提交发生在原帖之后，而且公开 Actions 还没有给出与 iOS `v1.0.15` 同等级的已发布、已验证证据。文章可以记录方向，不能把它写成 10 月 13 日已经交付的事实。

---

## 08 | 最准确的产品判断

`d2r-mobile-build` 的价值不在于“有人把 IPA 放出来了”，而在于它开始把一次性打包整理为一套带版本身份、摘要、缓存、兼容性检查、双系统矩阵和私有发布的流程。对开发者，它比照着 `NO_XCODE.md` 手工拼包可靠；对普通用户，它把本机 Xcode 环境换成了模板、Secret 与一次 workflow dispatch。

但它没有把法律和验证成本变没：游戏与派生数据的来源仍需单独判断，云端构建仍依赖 Xcode，unsigned IPA 仍需签名，真机体验仍需实际安装与长时间运行。尤其在仓库高速变化时，README、Release 和主分支代表的并不是同一代流水线。

最终最准确的一句话是：**D2R Mobile Build 已经把“源码能不能打包”推进到“交付过程能不能被重复和核对”；它还没有把“CI 能产出 IPA”推进到“任何人下载后都能合法、稳定地在真机玩”。**

---

## 主要来源

- [原始 X 帖子：`@quc1z` 提供 IPA 与 Data 的仓库链接](https://x.com/quc1z/status/2109825251966394654)
- [`jiayx/d2r-mobile-build`](https://github.com/jiayx/d2r-mobile-build)
- [固定审计提交 `111f065`](https://github.com/jiayx/d2r-mobile-build/tree/111f065d85f42630eb042f7b868c2f3387225d2f)
- [Prepared Input 格式](https://github.com/jiayx/d2r-mobile-build/blob/111f065d85f42630eb042f7b868c2f3387225d2f/docs/PREPARED_INPUT.md)
- [可复用 iOS 构建工作流](https://github.com/jiayx/d2r-mobile-build/blob/111f065d85f42630eb042f7b868c2f3387225d2f/.github/workflows/pack.yml)
- [`v1.0.15` Release](https://github.com/jiayx/d2r-mobile-build/releases/tag/v1.0.15)
- [旧流水线成功运行：Build unsigned IPA #41](https://github.com/jiayx/d2r-mobile-build/actions/runs/38657699261)
- [新版流水线首次失败：Source build #1](https://github.com/jiayx/d2r-mobile-build/actions/runs/38691613808)
- [上游 `jhaizhou-ops/d2r-mobile`](https://github.com/jhaizhou-ops/d2r-mobile)

*原帖发布时间：2026 年 10 月 13 日。源码与在线状态复核日期：2026 年 10 月 15 日。仓库变化很快；代码结论固定到 `111f065`，Release 结论固定到 `v1.0.15`。本文未下载或分发游戏 Data、Prepared Input、密钥或商业游戏内容，也不提供法律意见。*
