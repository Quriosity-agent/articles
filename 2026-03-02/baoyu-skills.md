# baoyu-skills：当 Prompt 成为软件，一个中国开发者如何重新定义 AI 技能生态

> 6000+ Star，700+ Fork，15 个技能，从小红书图文到微信公众号一键发布——宝玉的 baoyu-skills 不只是一个 Claude Code 插件集，它代表着"提示词即软件"时代的到来。

## 一、引言：我们正在进入"提示词即软件"的时代

2026 年初，AI 编程助手的生态正在经历一场静默的范式转变。Claude Code 不再只是一个能写代码的终端工具——它正在变成一个可以安装"技能"的平台，就像 VS Code 可以安装扩展一样。

在这股浪潮中，一个名为 **baoyu-skills** 的项目悄然登上了 GitHub 趋势榜。截至 2026 年 3 月 2 日，它已经获得了 **6,095 颗 Star** 和 **701 个 Fork**——对于一个 Claude Code 插件项目来说，这个数字堪称现象级。

这个项目的作者，是中文技术社区里一个耳熟能详的名字——**宝玉**（@dotey）。

## 二、宝玉是谁？

**宝玉**（Jim Liu），GitHub ID `JimLiu`，Twitter/X 账号 `@dotey`，目前定居美国芝加哥。他的 GitHub 个人签名写着"Yesterday is history, tomorrow is a mystery, and today is a gift"——一句来自《功夫熊猫》的台词，透着一种乐观主义的极客气质。

在中文 AI 社区，宝玉可能是最具影响力的技术传播者之一。他以高质量的技术翻译和深度解读闻名，尤其擅长将英文世界前沿的 AI 论文、产品动态和技术思考翻译并介绍给中文读者。他曾提出一套广受好评的"两步翻译法"Prompt——先直译、再意译——被无数人引用和改良，甚至衍生出了专门的翻译优化项目（如 Humanizer-zh 等）。

但宝玉不只是一个翻译者。从 baoyu-skills 项目可以看出，他是一个深度的 AI 工具实践者——不只是使用 AI，而是在构建 AI 的工作流程。

## 三、baoyu-skills 是什么？

**baoyu-skills** 是一个为 Claude Code 打造的技能集（Skills Collection），专注于**内容创作和发布的全流程自动化**。

简单来说，它让你可以在 Claude Code 的终端里，用一行命令完成以下事情：

- 📱 把一篇文章变成小红书风格的系列信息图
- 📊 生成 20 种布局 × 17 种风格的专业信息图
- 🎨 为文章自动生成封面图（支持 5 维定制系统）
- 📽️ 把内容变成演示文稿幻灯片
- 🐦 一键发布到 X（Twitter）
- 📝 一键发布到微信公众号
- 🔗 把任意 URL 转换为 Markdown
- 🗜️ 智能压缩图片

### 项目数据（截至 2026-03-02）

| 指标 | 数值 |
|------|------|
| ⭐ Star 数 | 6,095 |
| 🍴 Fork 数 | 701 |
| 📅 创建时间 | 2026-01-13 |
| 🔄 最近更新 | 2026-03-02 |
| 💻 主要语言 | TypeScript |
| 📦 版本 | v1.42.3 |
| 🔧 技能数量 | 15 个 |

不到两个月，从 v1.0 迭代到 v1.42——这个更新频率本身就说明了项目的活跃度和作者的投入程度。

## 四、技能全景：三大类 15 个技能

baoyu-skills 将 15 个技能组织成三个插件包：

### 1. 内容技能（content-skills）

这是项目的核心，包含 8 个技能：

**baoyu-xhs-images** — 小红书信息图生成器，堪称项目的明星功能。它使用"风格 × 布局"二维系统，支持 9 种视觉风格（cute、fresh、warm、bold、minimal、retro、pop、notion、chalkboard）和 6 种信息布局（sparse、balanced、dense、list、comparison、flow），将内容自动拆解为 1-10 张信息图卡片。其工作流程颇具巧思：Claude Code 首先分析内容，为每张图生成一份详细的 **Prompt Markdown 文件**，其中精确指定了风格预设、布局规则、配色方案、排版指引和具体文案内容；然后调用底层的 **baoyu-image-gen**（默认使用 Replicate 上的 Nano Banana Pro 模型）将这些 Prompt 转化为高质量 PNG 图像。从第二张图开始，系统会将第一张图作为 `--ref` 参考图传入，确保整组图片在视觉风格上保持一致。

**baoyu-infographic** — 专业信息图生成器，更加强大。20 种布局类型（从鱼骨图到冰山模型，从漏斗图到韦恩图）配合 17 种视觉风格（从手工纸艺到赛博朋克，从像素风到宜家说明书风），组合出数百种可能性。

**baoyu-cover-image** — 封面图生成器，采用独创的五维定制系统：类型（Type）× 配色（Palette）× 渲染（Rendering）× 文字（Text）× 氛围（Mood）。

**baoyu-slide-deck** — 演示文稿生成器，支持 16 种预设风格，从蓝图风到粉笔板风、从企业风到像素艺术，可以自动生成完整的幻灯片图像序列。

**baoyu-comic** — 知识漫画生成器（Logicomix/Ohmsha 风格）。

**baoyu-article-illustrator** — 文章智能配图工具。

**baoyu-post-to-x** — X/Twitter 发布自动化（基于 Chrome CDP 浏览器自动化）。

**baoyu-post-to-wechat** — 微信公众号发布工具，支持 Markdown 到微信格式的转换。

### 2. AI 生成技能（ai-generation-skills）

**baoyu-image-gen** — 统一图像生成接口，支持多个后端：Gemini、DashScope（阿里云通义）、OpenAI、Replicate 等。是其他内容技能的底层依赖。

**baoyu-danger-gemini-web** — Gemini Web API 封装（逆向工程），通过浏览器 Cookie 认证，用于文本和图像生成。名字中的"danger"前缀表示它依赖非官方 API。

### 3. 工具技能（utility-skills）

**baoyu-url-to-markdown** — URL 转 Markdown 工具。

**baoyu-danger-x-to-markdown** — X/Twitter 内容转 Markdown，支持高分辨率媒体下载、嵌入推文渲染等。

**baoyu-compress-image** — 图片压缩工具。

**baoyu-format-markdown** — Markdown 格式化工具。

**baoyu-markdown-to-html** — Markdown 转 HTML，支持多主题、自定义配色、代码高亮等。

## 五、技术架构：极简但精巧

baoyu-skills 的技术实现有几个值得注意的设计决策：

### 零依赖哲学

整个项目**不依赖任何 npm 包**。所有 TypeScript 脚本通过 `npx -y bun` 直接运行，无需构建步骤。这是一个大胆的选择——意味着所有功能都是自行实现的，没有外部依赖链的脆弱性。

### 统一的技能结构

每个技能遵循相同的目录结构：
```
skills/baoyu-xxx/
├── SKILL.md          # YAML 前置数据 + 文档
├── scripts/          # TypeScript 实现
│   └── main.ts
├── references/       # 参考文档
└── prompts/          # AI 生成指引（可选）
    └── system.md
```

`SKILL.md` 是核心——它既是文档，也是 Claude Code 理解这个技能的"说明书"。这体现了"提示词即软件"的核心思想：**用自然语言描述的 SKILL.md 文件就是程序的接口定义**。

### 多维参数系统

项目中大量使用了"维度 × 维度"的组合设计模式。以 infographic 为例，20 种布局 × 17 种风格 = 340 种组合，但用户只需要指定两个参数（甚至可以完全不指定，让 AI 自动推荐）。这种设计将复杂性隐藏在简洁的接口背后。

### Prompt 驱动的图像生成

xhs-images 等视觉内容技能采用了一种独特的"Prompt 中间层"架构：Claude Code 并不直接生成图像，而是先生成结构化的 **Prompt Markdown 文件**，其中包含风格预设、布局规则、配色方案、排版指引和具体内容文案。这些 Prompt 文件随后被传递给 baoyu-image-gen（底层调用 AI 图像生成 API，默认为 Replicate 上的 Nano Banana Pro），由 AI 图像模型根据详细规格生成最终图像。为保持系列图片的视觉一致性，从第二张图开始，系统会通过 `--ref` 参数将第一张图作为参考传入。这种"提示词→提示词→图像"的两级架构，既保留了自然语言的灵活性，又确保了输出的可控性和一致性。

### 浏览器自动化

发布到 X 和微信公众号的功能基于 Chrome CDP（Chrome DevTools Protocol），这是一种务实的选择——与其等待平台开放 API，不如直接操控浏览器。这也是为什么这些技能名字中带有"danger"前缀——它们依赖可能随时失效的逆向工程。

## 六、生态位：Claude Code 技能市场的崛起

baoyu-skills 的成功不是孤立的。它诞生在 Claude Code 插件生态快速成长的窗口期。

2026 年 1 月，Claude Code 正式推出了插件市场（Marketplace）系统。开发者可以将技能打包为插件，通过 `/plugin marketplace add` 命令注册，用户可以浏览、安装和更新。这个机制与 VS Code 扩展市场异曲同工，但有一个根本性的区别：**Claude Code 的技能本质上是提示词工程的产物，不是传统意义上的代码扩展**。

这催生了一个新的创作形式。类似的项目还有：

- **cc-skills**（terrylica）— 一个包含 20 个插件的通用技能市场
- **create-agent-skill** — 一个"制造技能的技能"（Meta-skill）
- 各种垂直领域的单一技能（翻译、代码审查、文档生成等）

但 baoyu-skills 在这个生态中独树一帜，原因在于：它不是面向开发者的编程工具，而是**面向内容创作者的生产力工具**。它解决的问题是："我写了一篇好文章，怎么快速把它变成小红书图文、公众号推文、演示文稿和社交媒体帖子？"

这是一个被严重低估的痛点。

## 七、与其他项目的对比

### vs. Humanizer-zh 等翻译优化项目

宝玉本人因翻译 Prompt 闻名，社区中也有不少基于他思路的翻译优化项目。但 baoyu-skills 走的是完全不同的路线——它不是在优化 AI 的文字输出质量，而是在构建**从内容到视觉物料到分发渠道的完整管线**。

### vs. 通用 Claude Code 技能

大多数 Claude Code 技能面向开发者工作流（代码审查、文档生成、项目管理），baoyu-skills 则专注于**内容创作工作流**。这个差异化定位是它获得如此多 Star 的关键原因之一——它触达了一个更大的用户群体。

### vs. 独立内容创作工具（Canva、剪映等）

传统内容创作工具是 GUI 优先的，需要手动操作。baoyu-skills 是 CLI 优先的，通过自然语言驱动。你告诉 AI "把这篇文章变成小红书图文"，它就执行了。这是两种完全不同的交互范式。

## 八、社区反响

从项目的增长速度可以窥见社区的热情：

- **不到两个月** 获得 6000+ Star
- **701 个 Fork** 意味着大量的二次开发和学习
- **频繁的社区贡献**：从 CHANGELOG 可以看到来自 @zhao-newname、@xkcoding、@liye71023326、@justnode 等多位贡献者的 PR
- **知乎、Medium 等平台**上出现了多篇分析文章

知乎专栏有文章题为《从 baoyu-skills 看 Claude Code 插件的正确姿势》，将其作为 Claude Code 插件开发的标杆案例来分析。

## 九、更深层的意义：Prompt 即软件

baoyu-skills 最深刻的启示不在于它的具体功能，而在于它所代表的趋势。

传统软件是**代码编写的**：你用编程语言定义逻辑，编译成可执行文件，通过 API 接口交互。

baoyu-skills 中的技能是**自然语言描述的**：`SKILL.md` 文件用人类语言定义了技能的能力、参数和工作流程。TypeScript 脚本只负责胶水逻辑（文件 I/O、API 调用、浏览器自动化），真正的"业务逻辑"由 AI 在运行时根据 SKILL.md 的描述动态生成。

这就是"**Prompt 即软件**"（Prompt as Software）的含义：

1. **SKILL.md 是接口定义**（相当于 API Spec）
2. **自然语言描述是实现**（相当于源代码）
3. **AI 是运行时**（相当于编译器 + 虚拟机）
4. **用户的一句话是函数调用**（相当于 API Request）

这种范式的威力在于：**你不需要是程序员也能创建"软件"**。只要你能清晰地用自然语言描述一个工作流程，你就能创建一个 Claude Code 技能。

## 十、展望

baoyu-skills 的 v1.42 版本已经相当成熟，但从 CHANGELOG 的更新节奏来看，它仍在快速进化：

- **图像生成后端的多样化**：从 Gemini 到 DashScope 到 OpenAI 到 Replicate，支持越来越多的提供商
- **微信公众号工具链的完善**：Markdown 转换、主题系统、配色定制
- **社区贡献的加速**：越来越多的外部开发者提交 PR

可以预见的发展方向包括：
- 更多社交平台的支持（B 站、YouTube、LinkedIn）
- AI 视频生成技能
- 多语言内容的自动本地化
- 与更多 AI 模型的集成

## 结语

baoyu-skills 是 2026 年 AI 工具生态中一个极具代表性的项目。它证明了一件事：**在 AI 时代，最有价值的技能不是写代码，而是设计工作流程**。

宝玉用 15 个精心设计的技能，构建了一条从内容创作到视觉物料生成到多平台分发的完整管线。这不是一个程序员的炫技之作，而是一个内容创作者的生产力飞跃。

当提示词变成软件，当工作流程变成可安装的技能包，当"告诉 AI 你想做什么"取代了"手动操作每一个步骤"——我们正在见证软件分发方式的根本性变革。

而 baoyu-skills，正站在这场变革的最前线。

---

*本文写于 2026 年 3 月 2 日。项目地址：[github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)*
