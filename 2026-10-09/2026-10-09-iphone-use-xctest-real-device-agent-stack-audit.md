# iphone-use 源码审计：它不是 iPhone 镜像脚本，而是一套懂得“不要重试”的真机 Agent 控制栈

> **结论先行：** `iphone-use` 不是让模型对着 macOS 的 iPhone 镜像窗口点鼠标，也不只是一个教 Agent 操作手机的 Skill。它把自定义 XCTest Runner 安装到真实 iPhone，由 Mac 上的 Rust daemon 统一提供 HTTP API、26 个 MCP 工具、浏览器控制页和 iOS 遥控端。它真正有价值的部分不是“会点、会滑”，而是把无障碍元素、动作后的稳定画面、批处理、所有权和“这次失败能不能重试”做成协议。代价也很明确：需要 Mac、完整 Xcode、Apple 签名、Developer Mode 与一台保持解锁的 iPhone；手机端 Runner 端口没有认证，受保护 App 的视觉画面仍可能是空白。

![iphone-use 浏览器控制页](imgs/iphone-use-xctest-real-device-agent-stack-audit/iphone-use-browser-control.png)

用户提供的 [`donghaozhang/iphone-use`](https://github.com/donghaozhang/iphone-use) 是 2026 年 10 月 9 日创建的 fork，上游为 [`leeguooooo/iphone-use`](https://github.com/leeguooooo/iphone-use)。本文固定审计 fork 的 [`9aa2fb9`](https://github.com/donghaozhang/iphone-use/tree/9aa2fb94dffcb37b15f69cc142108c3b722d6fec)；该提交已经包含“控制期间保持唤醒，并在无密码设备上尝试解锁”的 PR #233，但 crate 版本仍为 `0.17.11`。审计过程中，上游又发布了 [`v0.17.12`](https://github.com/leeguooooo/iphone-use/releases/tag/v0.17.12)，并继续加入 iOS 15/16 的旧系统启动路径。因此下面的源码结论绑定到固定提交，发布状态则单独标明。

---

## 01｜它到底是什么：Skill 只是入口，控制能力来自四层系统

把整个项目叫作“iPhone Computer Use Skill”并不准确。源码里至少有四层：

| 层 | 负责什么 | 不负责什么 |
|---|---|---|
| Agent Skill | 规定读屏、确认副作用、登录、失败恢复和 Flow 复用方法 | 不直接控制手机 |
| MCP / HTTP API | 把元素、动作、批处理、Flow、测试和状态变成结构化协议 | 不替代真机执行层 |
| Rust daemon | 管理认证、Runner 生命周期、所有权、稳定等待、视频与多个客户端 | 不靠操作 Mac 桌面转发点击 |
| iPhone XCTest Runner | 在真机上读取无障碍树、合成触摸、输入文字并编码画面 | 不能绕过 Face ID、密码或 iOS 安全策略 |

当前路径自 `v0.14.0` 起已经用项目自己的 XCTest Runner 替换 WebDriverAgent，但保留 WDA 兼容 API。`v0.9` 之后，旧的 iPhone Mirroring backend 也已删除。换句话说，它不需要抢占 Mac 鼠标、键盘焦点或前台窗口，Agent 的动作直接进入手机端测试 Runner。

![iphone-use 当前控制架构](imgs/iphone-use-xctest-real-device-agent-stack-audit/current-architecture.png)

安装门槛并不轻：macOS 15+、完整的 Xcode.app、可用于开发签名的 Apple ID、开启 Developer Mode 的 iPhone，以及首次安装时的 USB 连接。手机在构建、启动和控制期间需要保持解锁；免费 Personal Team 的签名还需要周期性续期。这是一套面向开发者或自托管自动化团队的系统，不是装完即用的普通消费级遥控器。

---

## 02｜“读屏”首先是读无障碍树，不是让视觉模型猜坐标

`GET /agent/elements` 会从 XCTest 获取一次固定属性集的 accessibility snapshot，再压平成适合 Agent 消费的元素列表。模型看到的是 label、identifier、kind、value、enabled、visible、focused 与边界等信息，而不是只能对着截图估计按钮在哪里。

这带来三个直接好处：

1. 可以按唯一 label、identifier 或元素类型定位，不必持久化脆弱坐标；
2. 输入前能检查前台 App 和焦点字段，降低文字落进错误聊天框的风险；
3. 读屏结果可用于断言、Flow 兼容性检查和失败证据，而不只服务于一次点击。

元素索引还必须携带对应的 snapshot token。界面变化后再拿旧索引点击，daemon 会返回 `409 stale_element_snapshot`，并且不发送动作。这个约束看似麻烦，却阻止了 Agent 用已经过期的“第 7 个元素”去点击完全不同的目标。

截图仍然存在，但更多是辅助证据。元素树不足时，MCP 才会按需附图；动作 API 还能在同一次调用中返回界面稳定后的 delta。Agent 不必为了确认“设置页是否已经打开”额外进行一轮盲读。

---

## 03｜最成熟的设计不是点按，而是失败语义

手机自动化最危险的 bug 往往不是“按钮没点到”，而是“按钮其实点到了，但网络回包丢了，于是系统又点一次”。发送消息、提交订单、删除内容或付款时，这种重试可能造成真实副作用。

`iphone-use` 为动作返回明确状态：

| 返回语义 | 含义 | Agent 应如何处理 |
|---|---|---|
| `not_sent` | 动作在进入手机前被拒绝 | 只有 `retry_safe:true` 才可按原因修复后重试 |
| `applied` / `no_effect` | Runner 已执行，并观察到变化或未观察到效果 | 根据目标状态判断下一步 |
| `outcome_unknown` | 已经派发，但超时或传输中断，无法确认结果 | `retry_safe:false`，先重新读屏，禁止盲目重发 |

批处理 `/agent/actions` 最多接受 24 步，先整体校验，再顺序执行，并在第一处失败停止。返回结果保留已完成步数、已应用动作数、失败步骤、批次结果和最终画面。MCP 的压缩文本也刻意保留 `retry_safe`，不会为了节省 token 把关键安全语义抹掉。

`ok:true` 同样不等于业务目标已经达成。它只表示动作走过了可确认的执行路径；调用者仍应查看 settle、delta 或显式 postcondition。这个区分让“API 调用成功”和“用户想要的结果成功”不再混为一谈。

---

## 04｜它可以把 Agent 探索编译成 Flow、测试与定时任务

当 Agent 完成一次多步骤操作后，项目可以把过程整理为 per-app JSON Flow。后续执行由确定性 Runner 一次性重放，不再让模型每一步重新观察和决策。官方 Flow registry 位于独立仓库，下载内容带 SHA-256 校验；兼容性还会结合 App 版本、风险等级和验证时间给出结论。

Flow 不是无条件自动化。Skill 明确要求：

- 发送、发布、支付、删除和其他不可逆操作必须针对准确目标与输入得到用户确认；
- `outcome_unknown` 或 `retry_safe:false` 不能自动重放；
- 登录只能走专用登录/凭据路径，不能让模型索要、复述或固化密码；
- 保存私有 Flow 与发布到公共 registry 是两个独立决定；
- 每台手机同时只允许一个 owner 控制，租约用于协作，不是安全认证。

Flow 还可以进入 YAML/JSON 测试套件，输出退出码、JSON/JUnit 和失败现场，包括 screenshot、elements、steps 与 error。调度器能按 cron 运行 Flow 或测试；手机被占用时会延后，锁定时等待，错过窗口则记录 `missed`。这使项目从“Agent 可以操作手机”走向了可回归的移动端任务自动化。

---

## 05｜受保护画面不是被破解，而是退化为 accessibility wireframe

银行、钱包和支付 App 可以要求 iOS 屏蔽截图。`iphone-use` 没有绕过这个机制：所有视觉采集路径仍会得到空白区域。如果 daemon 检测到画面主体近似单色，而无障碍树在同一区域仍有可读元素，它会返回一张由元素边界、类型和 label 组成的 wireframe，并标记 `X-Capture-Redacted: 1`。

![受保护画面被转换为无障碍线框图的项目示例](imgs/iphone-use-xctest-real-device-agent-stack-audit/capture-redacted-accessibility-wireframe.png)

这说明“支持银行和支付 App”需要精确解释：**视觉画面仍可能不可见，但如果 App 暴露足够的 accessibility 信息，系统可以基于元素树导航。** 若 App 同时隐藏视觉内容且无障碍语义不足，Agent 也没有可靠依据。项目自己的 Skill 还明确禁止无人值守地操作付款或 2FA 页面，所以技术上可定位元素不等于适合自动授权资金动作。

---

## 06｜同一台 daemon 服务 Agent，也服务人

Mac daemon 默认监听 `127.0.0.1:44321`，向外提供三种主要入口：

- `/agent/*` HTTP API，供脚本和 Agent 使用；
- 26 个 MCP 工具，覆盖状态、观察、动作、批处理、登录、Flow 与指标；
- 浏览器控制页和原生 iOS Remote App，供人查看画面、点击、输入和接管。

原生 Remote App 采用 SwiftUI，要求 iOS 17+，可通过二维码配对，把凭据放进 Keychain，并接收 H.264 画面。它还能在网格中查看多台设备，并把同一手势同步到多个 daemon；每台被控 iPhone 仍有独立 Runner 和 daemon，不是一个进程共享多个虚拟设备。

人机共用时，`X-Phone-Owner` 提供默认 300 秒的控制租约，防止两个合作客户端同时操作。浏览器或人类接管会影响自动任务调度。但这个租约只是冲突协调，拿到网络访问权的攻击者不能因为“owner 名称不同”就被视为已隔离。

---

## 07｜最大的安全边界：44321 有认证，手机端 8100/9100 没有

daemon 的密码、cookie 或 bearer token 只保护 `44321`。状态改变请求还要带 `X-Phone-Control: 1`，浏览器 cookie 使用 `HttpOnly` 与 `SameSite=Lax`。这些是合理的控制面防护。

但真机 Runner 自己的控制端口 `8100` 和视频端口 `9100` 没有认证。USB relay 只把 Mac 侧监听限制在 loopback，却不会阻止同一 Wi-Fi 上的其他主机直接访问手机端口。官方文档因此要求使用可信、隔离网络，或者在 USB 控制时关闭 iPhone Wi-Fi。

把 daemon 绑定到 `0.0.0.0` 时必须配置密码和独立 Agent token，但这仍会把认证后的控制面暴露给整个局域网。远程使用应只通过可信 VPN、隧道或带认证的 HTTPS 反向代理访问 daemon，不能直接暴露 Runner 端口。

隐私方面，原生 Remote App 的政策声明开发者不运营中转服务器，不收集账号、分析、崩溃或广告数据；画面与输入只在用户指定的 Mac 和 App 之间传输。这是项目当前实现与政策的边界，不应扩写成对网络、第三方模型或用户自建代理的端到端隐私保证。

---

## 08｜工程成熟度比普通 MCP Demo 高，但真机证明仍有限

固定 fork 快照的核心目录包含约 111 个 Rust、Swift、Objective-C、Python 或 Shell 源文件、约 9.3 万行；86 个文件包含 Rust test、XCTest、pytest 或 unittest 标记。Rust workspace 拆为 `core`、`server`、`mcp` 与 `legacy-launch`，另有 XCTest Runner、SwiftUI Remote App、Web UI、Flow 示例和完整安装器。

PR 检查在 `macos-14` 上运行 Rust 1.96 的 clippy、server/MCP/legacy-launch 测试、二进制构建、26 工具 discovery、离线 Flow 校验、无签名 Runner 构建与脚本测试。PR #233 的测试和 MCP discovery 已通过；`v0.17.12` 也提供 universal macOS MCP 包、Runner 包和 `iPhoneUse.app.zip`，并附 SHA-256 文件。

但 CI 刻意不连接物理设备。它会把 daemon 指向一个必然失败的端口，避免测试误操作开发者手机。因此 CI 能证明协议、构建和模拟边界，不能证明某个 iOS 版本、某个 App 或当前签名在真机上完整可用。

项目报告的性能数字包括：同一台 iPhone 13 经 USB 读取树约 `0.08–0.135s`，点击并等待稳定约 `1.0s`；完整 Agent API 在 iPhone 17 Pro Max 上按 label 点击并返回稳定变化约 `1.9s`，视频流约 `27–28 fps`。这些数字来自项目自己的 2026 年 10 月测量，不是本文独立复测，不能直接外推到 Wi-Fi、复杂页面或所有 iPhone。

本轮本地验证运行了固定 fork 的 `server`、`iphone-use-mcp` 和 `legacy-launch` Rust 测试，全部通过；MCP 测试编译时出现一条未使用 import 的 warning。本文没有安装 Runner 到真实 iPhone，也没有对登录、支付、后台调度或多机同步做真机验收。因此确认的是源码架构、协议设计、公开 CI 与本机构建测试，不是端到端产品验收。

---

## 09｜适合谁，又不适合谁

它适合：

- 需要让 Agent 操作没有公开 API 的自有 iOS App 或内部工具；
- 要把真实手机上的人工流程变成可回归测试或受控 Flow 的团队；
- 愿意管理 Xcode 签名、Developer Mode、可信网络与专用测试设备的开发者；
- 希望人在浏览器/iOS Remote 与 Agent 之间安全交接控制权的实验环境。

它不适合：

- 想在 Windows/Linux 上直接控制 iPhone，或不愿维护 Mac/Xcode 签名的人；
- 期待绕过锁屏密码、Face ID、受保护截图或 App 自身权限的人；
- 把“元素可见”误当成“付款、发送或删除可以无人值守”的工作流；
- 需要 App Store 级稳定性，却无法接受 iOS/Xcode 更新、签名续期和 accessibility 变化的人。

---

## 10｜结语：真正的产品不是“手机上的鼠标”，而是可判断的动作协议

`iphone-use` 最容易传播的卖点是“Computer Use, but for the iPhone”。源码给出的更准确定位是：**一套以自定义 XCTest Runner 为执行层、以 Rust daemon 为控制面、以 accessibility snapshot 为观察基础、以 MCP/HTTP/Flow 为 Agent 接口的真机自动化栈。**

它已经远超过简单的 Remotion 式 Skill 或几条 Appium 脚本：Runner、视频、元素快照、并发 owner、批处理、Flow registry、测试套件和 Remote App 都是真实实现。与此同时，它仍受 Apple 开发链、真机解锁、无障碍质量和未认证 Runner 端口约束。

最值得其他 Agent 工具借鉴的，也许不是它如何合成一次点击，而是它敢于告诉模型：**这次动作可能已经发生，所以不要重试。** 对真实世界自动化来说，这比再多一个 `tap` 工具重要得多。

---

## 主要来源

- [用户提供的 fork：donghaozhang/iphone-use](https://github.com/donghaozhang/iphone-use)
- [上游项目：leeguooooo/iphone-use](https://github.com/leeguooooo/iphone-use)
- [固定审计提交 `9aa2fb9`](https://github.com/donghaozhang/iphone-use/tree/9aa2fb94dffcb37b15f69cc142108c3b722d6fec)
- [上游 v0.17.12 发布](https://github.com/leeguooooo/iphone-use/releases/tag/v0.17.12)
- [PR #233：保持唤醒与无密码设备解锁](https://github.com/leeguooooo/iphone-use/pull/233)
- [使用指南](https://github.com/donghaozhang/iphone-use/blob/9aa2fb94dffcb37b15f69cc142108c3b722d6fec/docs/guide.md)
- [Agent API](https://github.com/donghaozhang/iphone-use/blob/9aa2fb94dffcb37b15f69cc142108c3b722d6fec/docs/agent-api.html)
- [Agent 与 Flow 参考](https://github.com/donghaozhang/iphone-use/blob/9aa2fb94dffcb37b15f69cc142108c3b722d6fec/docs/agent-reference.md)
- [测试与调度](https://github.com/donghaozhang/iphone-use/blob/9aa2fb94dffcb37b15f69cc142108c3b722d6fec/docs/testing.md)
- [隐私政策](https://github.com/donghaozhang/iphone-use/blob/9aa2fb94dffcb37b15f69cc142108c3b722d6fec/docs/privacy.md)
- [MIT License](https://github.com/donghaozhang/iphone-use/blob/9aa2fb94dffcb37b15f69cc142108c3b722d6fec/LICENSE)

*审计日期：2026 年 10 月 9 日。仓库、发布、CI 与设备兼容状态会继续变化。本文没有在真实 iPhone 上安装或运行该项目；性能数据为项目方报告。配图中的浏览器控制页与 accessibility wireframe 来自上游仓库并随本文本地保存；当前架构图依据固定快照重绘。*
