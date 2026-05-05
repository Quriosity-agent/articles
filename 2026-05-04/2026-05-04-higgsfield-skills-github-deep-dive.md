# Higgsfield Skills GitHub 深度拆解：把 AI 视频和商品图生成封装成 Agent 可调用的技能包

GitHub 项目地址：<https://github.com/higgsfield-ai/skills/tree/main>  
检查版本：`1dcfe26`（2026-05-04）

---
**Author:** 🦞 龙虾侦探 / Lobster Detective  
**Date:** 2026-05-04  
**Tags:** Higgsfield, Agent Skills, AI Video, AI Image Generation, Product Photography, Marketplace Cards, Soul ID, Claude Code, Codex, Cursor
---

很多 AI 生成工具的问题，不是模型能力不够，而是**没有变成 Agent 能稳定调用的产品能力**。

普通用户看见的是“生成一张图”或者“做一个视频”；但对 Agent 来说，真正困难的是另一件事：什么时候该训练身份？什么时候该走商品图工作流？什么时候用 Marketing Studio？什么时候只需要普通 image-to-video？哪些参数能传？哪些地方必须等任务完成？结果 URL 应该怎么交付？错误该怎么恢复？

Higgsfield 的这个 `skills` 仓库，做的不是另一个前端 demo，也不是模型论文复现。它更像一组 **面向 Agent 的创意生产操作手册**：把 Higgsfield CLI 背后的图像、视频、商品摄影、身份训练、市场素材生成能力，封装成 Claude Code / Codex / Cursor 等 agent 可以加载、判断、执行、串联的 Markdown Skills。

我把 repo 拉下来读了一遍。结论先说：**这个仓库的价值不在代码量，而在产品边界和工作流设计。它把“调用一个生成 API”升级成了“让 Agent 像创意运营助理一样做决策、提问、执行和交付”。**

---

## 一、这个项目到底是什么？

仓库 README 的定义很直接：

> AI agent skills for image and video generation via Higgsfield AI.

当前 repo 里有四个核心技能：

| Skill | 负责什么 |
|---|---|
| `higgsfield-generate` | 通用图像 / 视频生成，覆盖 30+ 模型，以及 Marketing Studio 的品牌广告视频 / 图片 |
| `higgsfield-soul-id` | 训练 Soul Character，也就是可复用的人脸身份 reference_id |
| `higgsfield-product-photoshoot` | 商品摄影、生活方式图、Pinterest、广告图、虚拟试穿等品牌商品视觉 |
| `higgsfield-marketplace-cards` | 电商 marketplace 主图、二级图、A+ style 模块、信息图等销售素材 |

所有技能都通过同一个二进制：`higgsfield` CLI。仓库里的 `CLAUDE.md` 特别强调：**不要直接 curl Higgsfield API**。因为 CLI 负责 auth、retry、polling、schema validation、自动上传本地媒体、等待 job 完成等关键行为。

这点很重要。很多 Agent 集成喜欢直接拼 HTTP 请求，但对生成类产品来说，API 调用只是中间一步。真正的用户体验取决于：

- 本地图片能不能自动上传；
- 长任务能不能正确等待；
- 失败时能不能给出可理解的恢复路径；
- 结果 URL 能不能稳定拿到；
- 不同模型参数差异能不能被隐藏。

Higgsfield Skills 的设计选择是：**让 skill 只做决策和流程编排，把底层 API 复杂性交给 CLI。**

---

## 二、项目规模：小仓库，但工程纪律很清楚

我实际扫了一下仓库：

- 总文件数约 **38**；
- 文本内容约 **3,021 行**；
- Markdown 文件 **26 个 / 约 2,351 行**；
- 4 个 skill 目录；
- `higgsfield-generate` 的 `SKILL.md` 约 **205 行**，并带 **7 个 references 文档**；
- `higgsfield-product-photoshoot` 的 `SKILL.md` 约 **220 行**；
- `higgsfield-soul-id` 的 `SKILL.md` 约 **84 行**，带 2 个 references；
- `higgsfield-marketplace-cards` 的 `SKILL.md` 约 **89 行**；
- 还有 `.claude-plugin/`、`.codex-plugin/`、`.cursor-plugin/` 三套 agent 插件 manifest；
- GitHub Actions 里有 `validate-skills.yml`，检查 frontmatter、版本同步、marketplace 是否列出所有 skill、references 是否可解析、是否出现 `../` 父目录引用。

这个仓库不像 Open Design 那样是完整应用 monorepo。它更像一个 **高密度的 agent 操作层**：文件不多，但每个文件都在定义 Agent 在真实任务中应该怎么做。

尤其值得注意的是它的 CI 规则：

- 每个 `higgsfield-*/SKILL.md` 必须有 YAML frontmatter；
- `name` 必须和目录名一致；
- `description` 必须包含 `Use when` 触发条件和 `NOT for` 边界；
- repo-wide `VERSION` 必须和所有 skill、Claude plugin、Codex plugin、Cursor plugin 里的 version 同步；
- skill 引用的 `references/*.md` 必须存在；
- `references/` 下不能有孤儿文档；
- skill 和 references 不能引用父目录，保证每个 skill 可独立安装。

这些检查说明作者真正关心的是“技能包能不能长期被 Agent 稳定加载和分发”，而不是只写几个 prompt 模板。

---

## 三、最关键的抽象：Skill 不是提示词，是决策树

很多人一听 “AI skill”，会以为它只是一个 prompt。

Higgsfield Skills 不是这样写的。每个 `SKILL.md` 都更像一个小型决策树：

- 什么用户意图触发这个 skill；
- 什么任务不应该由这个 skill 处理；
- 需要先检查 CLI 和登录状态；
- 哪些信息可以默认，哪些必须问用户；
- 哪些模型 / 模式适合哪些任务；
- 什么时候要链到另一个 skill；
- 命令怎么构造；
- 结果怎么交付；
- 常见错误怎么处理。

例如 `higgsfield-generate` 的 frontmatter 里写得非常细：

- “generate an image” / “make a video” / “animate this photo” / “UGC video” / “product demo” 都应该触发；
- 但 “training Soul Character” 不归它管，要走 `higgsfield-soul-id`；
- “professional product photoshoots with mode-specific prompt enhancement” 也不归它管，要走 `higgsfield-product-photoshoot`。

这就是好 skill 的关键：**它不只告诉 Agent 怎么做，还告诉 Agent 什么时候不要做。**

在真实产品里，错误路由比不会调用更危险。用户说“帮我做商品图”，Agent 如果直接调用普通 `gpt_image_2`，可能能出图，但绕过了 Higgsfield product-photoshoot 的 backend prompt enhancer，质量会明显下降。skill 明确写出这个边界，就是在保护产品体验。

---

## 四、四个技能形成了一条创意生产链

这个仓库最有意思的地方，是四个 skill 并不是平铺的工具列表，而是形成了几条可组合链路。

### 1. `higgsfield-soul-id`：先把“人”变成可复用资产

`higgsfield-soul-id` 负责训练 Soul Character。用户提供 5–20 张脸部照片，CLI 训练出一个 `reference_id`。

这个 ID 后续可以交给 `higgsfield-generate`：

```bash
higgsfield generate create text2image_soul_v2 --prompt "..." --soul-id <ref_id> --wait
higgsfield generate create soul_cinema_studio --prompt "..." --soul-id <ref_id> --wait
```

这说明 Higgsfield 把“身份”当成一个长期资产，而不是一次性 face swap。对 founder UGC、个人品牌视频、团队周报、广告 avatar 来说，这个抽象非常实用。

### 2. `higgsfield-generate`：通用生成和 Marketing Studio 入口

这是最大的 skill。它覆盖 text-to-image、image-to-image、image-to-video、reference-based generation，以及 Marketing Studio。

它的模型选择规则很有产品经验：

- 默认通用图片走 GPT Image 2；
- image-to-video 默认推荐 Seedance 2.0，便宜场景可用 Kling 3.0；
- 角色、动画风格可用 Nano Banana 2；
- 广告 / 商业 / 品牌视频走 Marketing Studio；
- 涉及 Soul ID 的图像走 Soul 2.0 或 Soul Cinema。

注意它不是把模型列表全扔给用户，而是按任务意图建立默认路由。对 Agent 来说，这比“请选择模型”更有用。

### 3. `higgsfield-product-photoshoot`：商品视觉不要自由发挥

这个 skill 明确说：商品摄影不要让 Agent 手写 `gpt_image_2` prompt，而是必须走 `higgsfield product-photoshoot create`。因为后端 prompt enhancer 才掌握 mode-specific photography vocabulary 和结构化模板。

它支持 10 种模式：

- `product_shot`：白底 / 棚拍 / catalog；
- `lifestyle_scene`：真实环境、手、动作、氛围；
- `closeup_product_with_person`：手部、局部人脸、美妆演示；
- `moodboard_pin`：Pinterest 2:3 垂直 pin；
- `hero_banner`：网站 / 邮件 / campaign header；
- `social_carousel`：IG / LinkedIn / Facebook 多页 carousel；
- `ad_creative_pack`：Meta / TikTok / Pinterest / Google Ads 静态广告组合；
- `virtual_model_tryout`：AI 模特试穿；
- `conceptual_product`：悬浮、飞溅、CGI、雕塑感商品图；
- `restyle`：在保留主体的情况下改变已有图片的风格 / 季节 / 氛围。

这说明 Higgsfield 已经把“商品图”拆成了一组产品化场景，而不是一个泛泛的 image generation prompt。

### 4. `higgsfield-marketplace-cards`：销售素材按 listing 结构生成

Marketplace card skill 进一步垂直化。它不是做“漂亮商品图”，而是做 marketplace listing 所需的素材包：

- `main`：1 张主图；
- `product-images`：主图 + 5 张二级图；
- `aplus`：主图 + 7 个 A+ 模块；
- `full-set`：主图 + 5 张二级图 + 7 个 A+ 模块。

它还支持细粒度 asset：infographic、multi_angle、detail_shot、lifestyle、what's_in_box、aplus_features、aplus_how_to_use 等。

这点很像把 Amazon / marketplace 运营经验变成 agent workflow。用户不需要说“我需要一张主图、五张详情图、七个 A+ 模块”；Agent 可以从 “make marketplace listing images” 路由到正确 bundle。

---

## 五、Cookbook 暴露了真正的产品方向

`COOKBOOK.md` 很值得看，因为它展示了这些技能如何被组合成 end-to-end workflow。

例如 “Brand Campaign from a Founder Photo”：

1. 用 founder headshot 训练 Soul；
2. 用商品图生成 5 张 lifestyle scene；
3. 选最好的 2 张再做 image-to-video；
4. 输出一套 campaign assets。

这不是单点生成，而是一个小型创意工作流：身份资产 + 商品资产 + 场景图 + 视频动画。

再比如 “UGC Ad Batch from a Product URL”：

1. 从 Shopify URL fetch 产品；
2. 选择 preset avatar；
3. 并行生成 UGC、unboxing、product review、TV spot 四种广告；
4. 每个输出一个可投放的视频 URL。

这就是 Agent 真正有价值的地方：不是帮你点一次“生成”，而是帮你把一组创意运营任务串起来。

Higgsfield Skills 的 cookbook 已经暗示了它未来可能成为一种 **creative operations automation layer**：用户提供产品、人物、品牌目标，Agent 自动训练、生成、挑选、变体化、交付。

---

## 六、安装和分发：同一套 skill，适配多个 Agent

仓库的安装方式也很有意思。它不是只服务 Claude Code，而是提供了多种入口：

```bash
npx skills add higgsfield-ai/skills
```

或者：

```bash
gh skill install higgsfield-ai/skills
```

Claude Code 里也可以用 marketplace：

```text
/plugin marketplace add higgsfield-ai/skills
/plugin install higgsfield@higgsfield
```

此外还有 `./setup` 脚本，会检测 Claude Code / Cursor / Codex，安装 CLI、检查 auth，并把 skill 目录 symlink 到对应位置。

这说明它的目标不是“给某一个 Agent 写一个私有插件”，而是把 Higgsfield 能力做成跨 agent 的能力包。

插件 manifest 也覆盖了：

- `.claude-plugin/`；
- `.codex-plugin/`；
- `.cursor-plugin/`。

这对未来很重要。Agent 生态正在从“每个工具写自己的 MCP / plugin / prompt”走向“可安装、可验证、可分发的技能包”。Higgsfield Skills 是这个方向的一个很小但很清楚的样本。

---

## 七、设计上最值得借鉴的地方

我觉得这个仓库有几个 builder lesson。

### 1. API 能力要被封装成任务意图

用户不会说“调用 `marketing_studio_video`，传 JSON avatars，product_ids，mode=ugc”。

用户会说：“帮我把这个 Shopify 商品做 4 条 TikTok 广告。”

Skill 的价值，就是把后者稳定翻译成前者。

### 2. 垂直场景要有专属入口

商品摄影、marketplace cards、Soul ID、通用视频生成，本质上不是同一种任务。把它们都塞进一个 `generate` skill，会让 Agent 路由混乱。

Higgsfield 选择拆成四个 skill，每个 skill 都有明确 `Use when` 和 `NOT for`。这是非常实用的产品边界。

### 3. 后端 prompt enhancer 是产品资产

`product-photoshoot` 和 `marketplace-cards` 都强调：不要让 Agent 自己写最终 prompt，后端 enhancer 负责。

这说明 Higgsfield 把 prompt engineering 当成服务端产品资产，而不是暴露给每个 Agent 自由发挥。Agent 负责收集意图和选择模式；后端负责把意图变成高质量生成 prompt。

### 4. 结果交付要克制

多个 skill 都要求：最终回复只给 URL 和简短 label，不要 JSON dump，不要 raw IDs，不要内部模型名，不要增强后的 prompt。

这是面向真实用户的 UX 纪律。Agent 很容易把内部过程全部倒给用户，但创意工具的用户要的是结果，不是 job metadata。

### 5. Skill 必须自包含

仓库要求每个 skill 不引用 `../`，references 必须被 `SKILL.md` 显式引用。这保证了单个 skill 可以独立安装。

这对技能生态很重要：一个 skill 不是 repo 里的脆弱相对路径集合，而是一个可分发单元。

---

## 八、现在的限制和风险

这个仓库很实用，但也有明显限制。

第一，它本身不是完整产品，只是 Agent Skills 层。真正能力依赖 Higgsfield CLI 和 Higgsfield 后端。也就是说，repo 的价值在 workflow 和 integration，不在模型本身。

第二，当前公开代码主要是 Markdown、manifest、setup、CI，不包含后端 prompt enhancer 的实现。商品摄影和 marketplace cards 的核心质量资产在 Higgsfield 服务端，开源部分只能看到调用边界。

第三，生成任务天然依赖 auth、额度、付费计划、长时间 polling。比如 Soul training 需要 Basic+，训练可能需要几十分钟。这些都要求 Agent 在 UX 上处理等待、失败和用户确认。

第四，多 Agent 分发仍然是早期生态。Claude Code、Codex、Cursor 对 skills/plugin 的加载方式会持续变化，这类仓库需要频繁跟进。

第五，当前 GitHub star 数还不高，说明它更像 Higgsfield 官方能力入口，而不是已经形成社区生态的独立项目。

这些不是致命问题，但说明它的定位要看清：它不是“开源 AI 生成模型”，也不是“完整 creative SaaS”；它是 Higgsfield 把自家生成能力交给 coding agent 调用的一层产品化接口。

---

## 九、谁应该研究它？

我觉得三类人应该看这个 repo。

第一类是 **做 AI 生成产品的人**。如果你的产品有图片、视频、音频、3D、商品图等生成能力，不要只提供 API。你还需要提供 Agent 能理解的 skill：触发条件、边界、默认模型、错误处理、结果交付。

第二类是 **做 Agent 平台的人**。这个仓库展示了一个轻量但实用的分发形态：Markdown skill + references + plugin manifests + setup script + CI validation。

第三类是 **做增长 / 电商 / UGC 自动化的人**。这里最有价值的不是“生成一张好看的图”，而是 founder photo → Soul → lifestyle photos → video ads，或者 product URL → avatar → 多风格广告批量生成这类工作流。

如果你在做 QCut 这类 AI 视频工具，也很值得研究它：Higgsfield Skills 的重点不是编辑时间线，而是把素材生产前段自动化成 Agent 可操作的 pipeline。

---

## 结论：Higgsfield Skills 的意义，是把生成模型变成 Agent 的创意生产工具

Higgsfield Skills 是一个小仓库，但它代表的方向很重要。

未来的 AI 生成产品，不应该只给人一个网页按钮，也不应该只给开发者一组裸 API。它们应该给 Agent 一套可安装、可验证、可组合的技能：

- 用户说什么会触发；
- 哪些任务不该处理；
- 该问哪些最少问题；
- 默认选什么模型或模式；
- 如何调用 CLI；
- 如何等待长任务；
- 如何把上一步的 `reference_id` 传给下一步；
- 如何交付最终 URL；
- 如何避免把内部细节倒给用户。

Higgsfield 这个 repo 的价值，就在于它把这些细节写成了机器可读、人可审查、CI 可验证的 skill 包。

对 builder 来说，最重要的启发是：

**不要只把你的 AI 能力做成 API。把它做成 Agent 可以理解和执行的工作流。因为下一代用户不会只点按钮，他们会让 Agent 替他们完成整条创意生产链。**
