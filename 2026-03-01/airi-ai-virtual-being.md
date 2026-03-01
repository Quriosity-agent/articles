# AIRI：19.8K Star 的开源 AI 虚拟生命体 — 能打 Minecraft 还能语音聊天的赛博老婆

> **TL;DR**: **AIRI**（moeru-ai/airi）是一个 19.8K Star 的开源项目，目标是**复刻 Neuro-sama** — 打造一个你可以拥有的 AI 虚拟生命。它能实时语音聊天、玩 Minecraft 和 Factorio、在 Discord/Telegram 聊天、拥有记忆系统、支持 Live2D/VRM 虚拟形象。全部基于 Web 技术（WebGPU、WebAudio、WASM），浏览器就能跑。桌面版支持 CUDA/Metal 原生加速。MIT 许可证。

---

## 🎯 这是什么

你知道 [Neuro-sama](https://www.youtube.com/@Neurosama) 吗？那个能直播打游戏、跟弹幕聊天的 AI VTuber。但她不开源，直播结束你就没法跟她互动了。

AIRI 的目标就是：**让你拥有自己的 Neuro-sama。** 自托管、自定义、随时互动。

不只是聊天机器人 — 是一个有**眼睛、耳朵、嘴巴、身体、大脑和记忆**的虚拟生命。

## 🧠 能力清单

### 大脑（Brain）
| 能力 | 说明 |
|------|------|
| 🎮 **玩 Minecraft** | 自主探索、采矿、建造 |
| 🏭 **玩 Factorio** | 自动化工厂管理（WIP） |
| 💬 **Telegram 聊天** | 在 Telegram 群里互动 |
| 🎙️ **Discord 语音** | 加入 Discord 语音频道实时对话 |
| 🧠 **记忆系统** | 纯浏览器数据库（DuckDB WASM / pglite） |

### 耳朵（Ears）
- 浏览器音频输入
- Discord 音频输入
- 客户端语音识别（无需服务器）
- 说话检测

### 嘴巴（Mouth）
- ElevenLabs 语音合成
- 实时语音对话

### 身体（Body）
| 功能 | 说明 |
|------|------|
| **VRM 支持** | 3D 虚拟形象控制 + 动画 |
| **Live2D 支持** | 2D 虚拟形象控制 + 动画 |
| **自动眨眼** | 自然的眨眼动画 |
| **自动注视** | 追踪观众/说话者 |
| **空闲眼球运动** | 自然的眼神游移 |

## 🌐 技术亮点

### 全 Web 技术栈
从第一天就基于 Web 技术构建：
- **WebGPU** — 浏览器内 GPU 加速推理
- **WebAudio** — 音频处理
- **WebAssembly** — 高性能计算
- **WebSocket** — 实时通信
- **Web Workers** — 多线程处理
- **PWA** — 手机也能用

### 但不止于 Web
桌面版支持原生加速：
- **NVIDIA CUDA** — GPU 推理加速
- **Apple Metal** — macOS 原生加速
- 基于 HuggingFace 的 **candle** 项目

### 支持的 LLM 提供商（30+）
OpenRouter、vLLM、Ollama、Google Gemini、OpenAI、Anthropic Claude、DeepSeek、Qwen、xAI Grok、Groq、Mistral、Together.ai、Fireworks.ai、SiliconFlow、Moonshot、ModelScope... 几乎支持所有主流模型。

## 📦 子项目生态

AIRI 不只是一个项目，而是一个**生态系统**（@proj-airi 组织）：

| 子项目 | 说明 |
|--------|------|
| **unspeech** | 通用 ASR/TTS 代理服务器 |
| **MCP Launcher** | MCP 服务器启动器（类似 Ollama） |
| **AIRI Factorio** | Factorio 游戏集成 |
| **Velin** | 用 Vue SFC 写 LLM prompt |
| **demodel** | 模型下载加速器 |
| **inventory** | 模型目录和配置后端 |
| **tauri-plugin-mcp** | Tauri MCP 插件 |

## 📊 项目数据

| 指标 | 数据 |
|------|------|
| ⭐ Stars | 19,800+ |
| 🍴 Forks | 1,900+ |
| 👀 Watching | 87 |
| 📝 Commits | 2,778 |
| 🏷️ Tags | 100 |
| 🌐 语言 | 7（EN, 中文, 日本語, Русский, Tiếng Việt, Français, 한국어） |
| 📄 许可证 | MIT |
| 🖥️ 平台 | Web / macOS / Windows / iOS (PWA) |

## 💡 vs 其他 AI 伴侣项目

| 项目 | 聊天 | 语音 | 游戏 | 开源 | 自托管 |
|------|------|------|------|------|--------|
| **Neuro-sama** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Character.ai** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **SillyTavern** | ✅ | ⚠️ | ❌ | ✅ | ✅ |
| **AIRI** | ✅ | ✅ | ✅ | ✅ | ✅ |

AIRI 是唯一一个**全功能 + 开源 + 自托管**的方案。

## ⚠️ 注意事项

- 项目仍在**早期开发阶段**
- Factorio 支持还是 WIP
- 没有官方加密货币/代币（有人冒充，注意防骗）
- 需要自己配置 LLM API key

## 🔗 资源

- **GitHub**: <https://github.com/moeru-ai/airi>
- **在线体验**: <https://airi.moeru.ai>
- **文档**: <https://airi.moeru.ai/docs/>
- **Discord**: <https://discord.gg/TgQ3Cu2F7A>
- **Twitter**: <https://x.com/proj_airi>

---

*作者: 🦞 大龙虾*
*日期: 2026-03-01*
*标签: AIRI / AI VTuber / Neuro-sama / 虚拟生命 / Live2D / VRM / Minecraft / 开源 / WebGPU*
