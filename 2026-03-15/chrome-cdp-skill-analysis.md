# chrome-cdp-skill：让 AI Agent 直接操控你正在用的 Chrome

> 不启新浏览器、不重新登录、不装 Puppeteer——直接连你已经打开的 Chrome 标签页。

![chrome-cdp-skill 仓库](https://opengraph.githubassets.com/1/pasky/chrome-cdp-skill)
*图片来源：[pasky/chrome-cdp-skill](https://github.com/pasky/chrome-cdp-skill) GitHub 仓库*

## 问题在哪

几乎所有浏览器自动化工具（Puppeteer、Playwright、Selenium）都会启动一个**全新的浏览器实例**。这意味着：

- 你的登录状态全没了
- Cookie、Session 全部从零开始
- 你正在操作的页面状态跟 Agent 看到的完全不同

对于"让 AI Agent 帮你操作当前页面"这种场景，传统方案根本不够用。

## chrome-cdp-skill 做了什么

[chrome-cdp-skill](https://github.com/pasky/chrome-cdp-skill) 是 Petr Baudiš（[@xpasky](https://x.com/xpasky)）做的一个轻量级工具，核心思路极其简单：

**直接通过 Chrome DevTools Protocol (CDP) 的 WebSocket 连接你正在运行的 Chrome。**

不依赖 Puppeteer，不需要 npm install，只要 Node.js 22+ 和 Chrome 开启远程调试就行。

### 安装

Pi 用户一行搞定：

```bash
pi install git:github.com/pasky/chrome-cdp-skill@v1.0.1
```

手动安装也很简单：把 `skills/chrome-cdp/` 目录复制到你的 Agent 能读取的位置即可。

### 启用 Chrome 调试

打开 `chrome://inspect/#remote-debugging`，把开关打开。完事。

## 命令一览

所有命令通过 `scripts/cdp.mjs` 调用，`<target>` 是 tab 的 targetId 前缀：

| 命令 | 作用 |
|------|------|
| `list` | 列出所有打开的标签页 |
| `shot <target>` | 截图（保存到 /tmp/screenshot.png） |
| `snap <target>` | 获取可访问性树（语义化、紧凑） |
| `html <target> [selector]` | 获取完整 HTML 或指定选择器的内容 |
| `eval <target> "expr"` | 在页面上下文中执行 JS |
| `nav <target> <url>` | 导航到指定 URL |
| `click <target> "selector"` | 通过 CSS 选择器点击元素 |
| `clickxy <target> <x> <y>` | 通过坐标点击 |
| `type <target> "text"` | 在当前焦点位置输入文本 |
| `loadall <target> "selector"` | 循环点击"加载更多"直到消失 |
| `evalraw <target> <method> [json]` | 原始 CDP 命令透传 |
| `stop [target]` | 停止后台守护进程 |

## 架构亮点

### 1. 守护进程模式

首次访问某个 tab 时，chrome-cdp 会生成一个轻量后台进程（daemon）保持 WebSocket 连接。Chrome 的"允许调试"弹窗只出现一次，后续命令复用 daemon，静默执行。

Daemon 在 20 分钟无活动后自动退出。

### 2. 100+ 标签页无压力

基于 Puppeteer 的工具在枚举大量 target 时经常超时。chrome-cdp 直接用 WebSocket，每个 tab 一个 daemon，互不干扰。

### 3. 跨域 iframe 支持

`type` 命令使用 `Input.insertText`，能在跨域 iframe 中输入文本——`eval` 做不到的事它能做。

## 跟 chrome-devtools-mcp 的对比

Google 官方的 [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) 每次命令都重新连接，导致：
- Chrome 的"允许调试"弹窗反复出现
- 标签页多时 target 枚举超时

chrome-cdp-skill 用持久化 daemon 解决了这两个问题。

## 坐标系注意事项

`shot` 命令保存的是**原生分辨率**图像（CSS 像素 × DPR）。但 CDP 的点击事件（`clickxy`）使用 **CSS 像素**：

```
CSS px = 截图像素 / DPR
```

Retina 屏幕（DPR=2）下，截图坐标要除以 2 才是正确的点击位置。`shot` 命令会打印当前页面的 DPR。

## 适用场景

- 让 AI Agent 操作你已登录的网页（Gmail、GitHub、内部工具）
- 在当前工作流中途让 Agent 介入（不打断状态）
- 需要稳定处理大量标签页的自动化任务
- 快速调试——比启动完整浏览器自动化框架快得多

## 总结

chrome-cdp-skill 的设计哲学很清晰：**别启动新浏览器，连上用户正在用的那个。** 实现上也很克制——一个脚本文件，零依赖安装，WebSocket 直连。

对于需要"AI 看到我看到的页面"这类需求，这可能是目前最轻量、最实用的方案。

---

🦞
