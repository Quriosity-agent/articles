# Claude Code Computer Use：让 AI 直接操控你的电脑

> Claude Code 新增 Computer Use 功能——Claude 可以打开 App、点击按钮、截图验证，全部在终端对话里完成。这对 Builder 意味着什么？

![Claude Code Computer Use 概念图](https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=900&q=80)
*图片来源：[Unsplash - Markus Spiske](https://unsplash.com/photos/iar-afB0QQw)*

---

## 一句话总结

Claude Code 的 Computer Use 让 Claude 像人一样操作你的 macOS 桌面——打开应用、点击、输入、截图——全在 CLI 对话中完成，不用离开终端。

---

## 这个功能能干什么

Computer Use 解决的核心问题：**有些事只能在 GUI 里做，CLI 搞不定。**

### 四个典型场景

| 场景 | 具体例子 |
|------|----------|
| **构建 + 验证原生 App** | Claude 写 Swift 代码 → 编译 → 启动 → 点击每个按钮 → 截图验证，一气呵成 |
| **端到端 UI 测试** | 让 Claude 打开 Electron App → 走完注册流程 → 截图每一步。不需要 Playwright 配置 |
| **调试视觉 Bug** | "Modal 在小窗口下被裁剪"——Claude 缩小窗口 → 复现 Bug → 截图 → 改 CSS → 再验证 |
| **操作纯 GUI 工具** | 设计工具、硬件控制面板、iOS Simulator——没有 API 的东西，Claude 也能用鼠标操作 |

关键点：**Computer Use 是最后手段。** Claude 会优先用 MCP Server → Bash → Chrome 扩展，只有这些都搞不定时才用 Computer Use。

---

## 怎么启用

**前提条件：**
- macOS 系统（Linux/Windows 暂不支持）
- Claude Code v2.1.85+
- Pro 或 Max 订阅（Team/Enterprise 暂不支持）
- 必须是交互式会话（`-p` 非交互模式不行）

**三步启用：**

1. **打开 MCP 菜单** → 在 Claude Code 会话里输入 `/mcp`
2. **启用 `computer-use` 服务** → 找到 `computer-use` 选择 Enable（每个项目只需设置一次）
3. **授权 macOS 权限** → Accessibility（让 Claude 点击/输入）+ Screen Recording（让 Claude 看屏幕）

启用后，直接说自然语言就行：

```
Build the app target, launch it, and click through each tab to make
sure nothing crashes. Screenshot any error states you find.
```

---

## 安全模型：Builder 必须知道的

这不是沙箱环境。Computer Use 跑在你的真实桌面上，所以 Anthropic 做了几层防护：

### 五道安全线

1. **按 App 审批** → 每个 Session 第一次用某个 App 时要你确认
2. **哨兵警告** → 高权限 App（终端、Finder、系统设置）会额外提醒
3. **终端不截图** → Claude 永远看不到自己的终端窗口，防止 Prompt Injection 循环
4. **全局 Esc 键** → 随时按 Esc 立即中止 Computer Use
5. **锁文件** → 同一时间只能有一个 Claude 会话控制你的机器

### App 权限分级

| 类别 | 控制级别 | 示例 |
|------|----------|------|
| 浏览器、交易平台 | 只读 | Chrome, Safari |
| 终端、IDE | 仅点击 | Terminal, VS Code |
| 其他所有 App | 完全控制 | Xcode, Figma, Simulator |

---

## 实战工作流示例

### 1. 验证原生 App 构建

```
Build the MenuBarStats target, launch it, open the preferences window,
and verify the interval slider updates the label. Screenshot the
preferences window when you're done.
```

Claude 的执行链：`xcodebuild` → 启动 App → 操作 UI → 截图返回

### 2. 复现布局 Bug

```
The settings modal clips its footer on narrow windows. Resize the app
window down until you can reproduce it, screenshot the clipped state,
then check the CSS for the modal container.
```

Claude 缩小窗口 → 截图坏掉的状态 → 读样式表 → 修复

### 3. 驱动 iOS Simulator

```
Open the iOS Simulator, launch the app, tap through the onboarding
screens, and tell me if any screen takes more than a second to load.
```

不需要写 XCTest，Claude 直接像人一样操作 Simulator。

---

## CLI vs Desktop 版本差异

| 特性 | Desktop | CLI |
|------|---------|-----|
| 启用方式 | Settings 界面切换 | `/mcp` 命令启用 |
| 拒绝 App 列表 | 可配置 | 暂不支持 |
| 自动恢复隐藏窗口 | 可选 | 始终开启 |
| Dispatch 集成 | 支持 | 不适用 |

---

## Builder 关键 Takeaways

1. **GUI 自动化的最后一公里** → Computer Use 补全了 CLI/API/MCP 覆盖不到的纯 GUI 操作。对于原生 App 开发者，这是杀手级功能。

2. **安全模型值得研究** → 按 App 审批 + 终端隔离 + 全局 Esc 的组合设计，是目前 AI 桌面操控中最谨慎的方案之一。如果你在做类似产品，这套安全模型值得借鉴。

3. **工具链优先级很重要** → Claude 不是上来就用 Computer Use，而是 MCP → Bash → Chrome → Computer Use 逐级降级。这个设计思路（精确优先，广泛兜底）对所有 Agent 架构都有参考价值。

4. **目前限制明确** → macOS only、Pro/Max only、交互模式 only。Windows/Linux 开发者暂时用不了。但考虑到 Anthropic 的节奏，扩展到其他平台只是时间问题。

5. **真正的 Agent 范式转变** → 当 AI 能"看到"和"操作"桌面时，很多原来需要 API wrapper、自动化脚本的工作可以直接用自然语言完成。这降低了自动化的门槛，但也提高了安全审计的重要性。

---

## 参考链接

- [Claude Code Computer Use 官方文档](https://code.claude.com/docs/en/computer-use)
- [Computer Use 安全指南](https://support.claude.com/en/articles/14128542)
- [Claude in Chrome](https://code.claude.com/docs/en/chrome)
- [MCP 协议](https://code.claude.com/docs/en/mcp)
- [沙箱机制](https://code.claude.com/docs/en/sandboxing)

---

*写于 2026-03-31 | 大龙虾出品 🦞*
