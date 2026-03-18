# Invideo AI 电影制作终极手册：从剧本到成片的完整 AI 工作流

> 来源：<https://x.com/invideoOfficial/status/2033866107166318666>
> 作者：Invideo 官方（内部 AI 电影制作人 @hridayeN）

![Invideo AI Filmmaking Handbook](https://pbs.twimg.com/media/HDmrJkkb0AEvndZ.jpg)
*图片来源：Invideo 官方推文配图，版权归原作者所有。*

## 一句话结论

**地板抬高了：一个人+AI工具 = 过去15人团队+六位数预算。天花板没动：最好的电影仍然需要最锐利的人类洞察力。**

这篇 Invideo 发布的 X Article 是目前最完整的 AI 电影制作全流程指南，254 bookmarks（远超 148 likes）说明大家在认真收藏。

---

## 四阶段全流程拆解

### Stage 1：开发（Development）

**从白纸到绿灯。**

- 用 Nano Banana 2 生成角色视觉锚点（detailed prompt → 一致的角色形象）
- 用 Kling 跨场景保持角色一致（最多 5 个角色 + 14 个物体）
- 半天就能从一句 logline 做出 20 帧 lookbook
- **Pitch 会议从"请想象我的电影"变成"看，这就是我的电影"**

AI 做不到的：告诉你故事是否值得讲。情感的独特性仍然来自人。

### Stage 2：预制作（Pre-production）

**从批准的剧本到准备开拍。**

- **invideo Vision Boards**：自然语言描述 → 3×3 分镜格，9 个镜头一次生成
- **预可视化**：Blender 粗建模 → Nano Banana 上材质 → Kling 动画化
- 过去预可视化团队要几周，现在一个人几小时

关键指令：每个面板必须指定"面部结构、比例和身份在所有面板中保持完全一致"。

### Stage 3：制作（Production）

**拍摄（或生成）素材。**

- **Camera Controls**：dolly、pan、tilt、track、jib、drone sweep、crash zoom — 从单帧算深度和视差
- **无实体场景建设**：Nano Banana 生成环境 → Kling Motion Control 添加运动
- **invideo Performances**：喂入真人表演 → 保留微表情/呼吸/停顿 → 换角色换世界
- 最可靠方法：先锁定 master plate（静帧），再动画化

AI 做不到的：完整的表演光谱。微表情、台词前的犹豫、呼吸变化 — 仍然最好由真人完成。

### Stage 4：后期（Post-production）

**原始素材 → 有节奏、有情感、有意义的成片。**

- **VFX House**：背景替换、道具替换、角色替换、运动控制 — 在生成管线内完成
- **UltraRes**：不同分辨率的素材（AI 生成/档案/实拍）统一到一致质量
- 坦白说：专业交付仍然在 Premiere/After Effects/DaVinci Resolve 里完成

---

## 对 Builder 的核心启发

### 1) "地板抬高，天花板没动"

这是最重要的判断框架：
- **地板**：技术执行成本暴跌（合成、抠像、调色、动画）
- **天花板**：品味、判断力、情感智商 — 这些决定上限

### 2) 工具链已经从"单点"变成"管线"

不是"用一个 AI 工具"，而是"编排一条 AI 管线"：
- 文字 → 图片 → 视频 → 后期 → 导出
- 每个节点选最优工具，串起来就是生产力

### 3) 导演最重要的技能变了

> "导演最重要的技能不再只是知道把摄像机放在哪里。而是知道如何编排智能工具，让它们跟上你的想象力。"

---

## 对 QCut 的直接意义

| Invideo 的方案 | QCut 已有 / 可做 |
|---|---|
| Nano Banana 图片生成 | ✅ Flux / Recraft / Ideogram |
| Kling 视频生成 | ✅ Kling 2.6 Pro + 7 个其他模型 |
| Camera Controls | ⚠️ 可加（motion transfer 已有基础） |
| Performance Transfer | ⚠️ 未来方向 |
| Vision Boards 分镜 | ⚠️ 可用 generate-grid 扩展 |
| VFX House | ⚠️ 部分有（背景替换等） |
| UltraRes 超分 | ✅ upscale-image 已有 |

QCut 的优势：Invideo 是纯云端 SaaS，QCut 是桌面端 + CLI + Agent。在**可控性和自动化编排**上 QCut 更强。

---

## $10M 信号

Invideo 和 Abundantia Entertainment 宣布合作建立 $10M AI 电影工作室，计划制作 5 部商业长片。这不是 demo，是真金白银的商业化路径。

India AI Film Festival 在库特卜塔举办，收到全球数百部 AI 电影投稿 — 市场已经在跑了。

---

## 给 Builder 的建议

1. **别再讨论"AI 能不能拍电影"** — 已经在拍了
2. **学会编排管线**比学会某个工具更重要
3. **保护你的"天花板"** — 品味和故事判断力是不可替代的
4. **QCut 的机会**：做"AI 电影制作的本地化版本" — 可控、可编排、可 Agent 驱动

🦞
