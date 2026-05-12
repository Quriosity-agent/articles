# Thinking Machines Lab Interaction Models：把实时协作从 Harness 挪进模型本体

> Source: <https://thinkingmachines.ai/blog/interaction-models/>  
> Author: Thinking Machines Lab  
> Date: 2026-05-11  
> Tags: Thinking Machines Lab / Interaction Models / Real-time AI / Multimodal Models / Human-AI Collaboration / Inference Systems

![Thinking Machines Lab Interaction Models 封面](imgs/tml-interaction-models/hero-cover.jpg)

## 1. 这不是又一个语音助手，而是一种产品边界的重画

Thinking Machines Lab 这篇《Interaction Models: A Scalable Approach to Human-AI Collaboration》的核心主张很明确：**AI 的“交互性”不应该继续作为外部 harness 的补丁，而应该和智能一样成为模型本体可扩展的能力。**

今天大多数 AI 产品仍然是 turn-based：用户说完或打完，模型才开始看；模型生成时，外部世界对它基本冻结；如果要实现打断、实时翻译、视觉触发、工具并发、背景搜索，就在模型外面拼 VAD、ASR、TTS、turn detector、agent loop、UI state manager。这个工程栈能跑，但上限很明显：真正决定“什么时候该插话、什么时候该沉默、什么时候该继续听”的组件，往往不是最聪明的那个模型。

TML 的研究预览把问题反过来：训练一个原生持续接收音频、视频、文本，同时持续输出、思考、行动的 interaction model。它不是“让聊天机器人说话更快”，而是把协作界面从“写 prompt / 等结果”推向“共同在场”：用户可以说、看、指、停顿、纠正；模型也可以听、看、插话、保持沉默、后台委派任务并把结果自然接回。

这对 builder 的意义比 benchmark 更大：如果这条路线成立，下一代 AI 应用的核心不再只是 prompt engineering 或 agent planner，而是**实时协作协议**：输入流如何进入模型，输出流如何被用户打断，后台任务如何不抢主对话，UI 如何呈现模型“正在看、正在等、正在想、正在查”。

![交互示例缩略图](imgs/tml-interaction-models/animal-story-thumb.jpg)

## 2. 协作瓶颈：自治 Agent 变强，但人被界面挤出去了

TML 开头引用了 METR 关于长任务能力的研究：AI labs 越来越关注模型能独立完成多长、多复杂的任务。这个方向很重要，但它也带来一个产品副作用：界面越来越适合“交给 Agent 跑”，越来越不适合“人和 Agent 贴身协作”。

他们还引用了一份 Anthropic frontier model card 中的观察：在 interactive、synchronous、“hands-on-keyboard”的模式下，模型收益不如长期 autonomous agent harness 明显，一些用户觉得模型太慢。这句话很关键，因为它指出了当前 frontier model 的一个反直觉问题：模型越会长程推理，实时协作体验反而越可能变差。

TML 认为问题不在“人是否还需要参与”，而在“界面是否给人留下参与空间”。真实工作里，需求很少一开始就完整、准确、稳定。写代码、做设计、排查线上问题、辅导学习、看病问诊、训练运动动作，都需要人不断补充上下文、纠偏、表达偏好和判断。turn-based 界面把这种高频低粒度的 tacit knowledge 压成一个窄通道：你必须等一个 turn 结束，才能把新的判断塞进去。

这也是为什么 TML 强调 copresence、contemporality、simultaneity：共同看同一个对象、在信息产生时实时接收、同时输入和输出。用工程语言说，就是 AI 应用不应该只支持 request/response，还应该支持低延迟、多模态、可重入、可并发的 session。

## 3. 关键设计：200ms micro-turn，而不是更聪明的 turn detector

TML 的核心技术选择是 **multi-stream, micro-turn design**。模型不再等待一个完整 user turn，然后生成一个完整 assistant turn，而是以约 200ms 为单位持续交错处理输入和输出：每 200ms 输入音频/视频/文本片段，同时生成 200ms 输出片段。这样，输入 token 和输出 token 都是流，而不是一次性序列。

这听起来像 latency 优化，但它真正改变的是能力边界。

传统实时语音系统通常靠 VAD 或 dialogue manager 判断“用户是不是说完了”。这种 harness 可以模拟打断，但很难理解复杂语境：用户是在思考、让步、自我纠正、对别人说话，还是期待模型插入？如果判断组件不够聪明，产品只能做保守策略：少打断、等用户停、响应延迟更高。

micro-turn 把这些判断交给模型本体学习。结果是一些以前要特制 harness 才能做的能力，变成统一模型行为：

- **无缝对话管理**：模型隐式判断用户是否在思考、让话、修正或邀请回应；
- **语言与视觉插话**：用户说错、代码出现 bug、动作到达关键时刻，模型可以主动出声；
- **同时说话**：例如边听西班牙语边输出英语翻译；
- **时间感**：模型直接感知 elapsed time，可以按时间提醒、计时、纠正节奏；
- **工具和生成式 UI 并发**：一边听用户说话，一边搜索、浏览或生成界面，再在合适时机接回。

![示例视频帧](imgs/tml-interaction-models/example-frame-1.jpg)

## 4. 系统不是只有一个模型：前台交互模型 + 后台推理模型

TML 没有假装一个低延迟模型能同时解决所有长程推理问题。它采用的是前后台分层：

1. **Interaction model**：保持实时在场，持续接收音频、视频、文本，负责 turn-taking、插话、短响应、上下文保持；
2. **Background model**：当任务需要更深推理、工具调用、搜索或 agentic workflow 时异步运行；
3. **Context package**：前台模型委派时不是发一个孤立 query，而是把完整对话和任务上下文交给后台；
4. **流式回灌**：后台结果产生后流回前台，由 interaction model 判断什么时候、以什么形式插入当前对话。

这个设计对产品团队很有启发。很多 agent 产品的问题不是后台不会跑，而是后台结果回来时会“抢麦”：突然插入一大段、打断用户当前思路、或者和前台状态不一致。TML 的架构把“何时把后台结果带回人类注意力”交给交互模型处理，相当于在 AI 系统里引入一个实时 attention scheduler。

## 5. 模型与推理栈：早融合、流式 session、确定性调试

TML 公开了不少工程细节，值得 builder 重点看。

**Encoder-free early fusion。** 它没有把音频和视频先交给大号独立 encoder，再把结果塞给 LLM，而是尽量减少预处理：音频用 dMel，经轻量 embedding；图像切成 40×40 patches，用 hMLP 编码；音频 decoder 用 flow head；这些组件和 transformer 从头一起 co-train。相关链接包括 dMel、Vision Transformer/hMLP、Flow Matching 等论文。这条路线的取舍是：牺牲一些模块替换便利性，换取端到端学习“什么交互信号重要”的能力。

**Streaming sessions。** 200ms chunk 会造成大量小 prefill / decode 请求，而现有 LLM serving library 往往对这种模式开销很大。TML 的做法是在 inference server 里保留 persistent sequence in GPU memory：客户端每 200ms 发一个 chunk，服务端把它 append 到同一个 session，避免重复内存分配和 metadata 计算。他们还把相关 fast path upstream 到 SGLang PR `#19171`：`SessionAwareCache` 让 KV ownership 保持在 per-session slots，并绕过不适合流式场景的 radix prefix matching。

**Latency-oriented kernels。** 他们提到双向 serving 下用 gather+gemv 策略优化 MoE kernel，而不是标准 grouped gemm；同时强调 batch-invariant kernels 和 trainer-sampler bitwise alignment，用来提升训练稳定性和调试可复现性。这与 TML 之前《Defeating Nondeterminism in LLM Inference》的主题一致：如果你要调一个复杂实时多模态系统，不可复现会迅速吞掉工程速度。

## 6. Benchmark 结果应该这样读

TML 的研究预览模型叫 **TML-Interaction-Small**，参数规模是 276B MoE、12B active。它在 FD-bench、Audio MultiChallenge、BigBench Audio、IFEval、Harmbench 等测试里展示了“交互质量 + 智能”的组合能力。

几个具体数字值得记：

| 指标 | TML-Interaction-Small | 对 builder 的含义 |
|---|---:|---|
| FD-bench V1 turn-taking latency | 0.40s | 实时协作的体感门槛不是“生成快”，而是“该接话时能接上”。 |
| FD-bench V1.5 average | 77.8 | 在打断、backchannel、背景语音等场景上明显优于列出的实时基线。 |
| FD-bench V3 Audio + Tools | 82.8 / 68.0 | 工具调用不应让实时对话完全停摆。 |
| Audio MultiChallenge APR | 43.4 | 相比低延迟模型，仍保持一定指令跟随和推理能力。 |
| IFEval text | 89.7 | 交互模型不是只能语音聊天，也要保留文本 instruction following。 |
| Harmbench refusal | 99.0 | 实时语音安全不能靠“事后审查”补救。 |

更有意思的是他们新增或改造的 interactivity eval：TimeSpeak、CueSpeak、RepCount-A、ProactiveVideoQA、Charades。它们测试的是传统 benchmark 不覆盖的能力：按指定时间发声、听到 code-switch 时即时纠正、看用户做俯卧撑并计数、看到视频中答案出现才回答、判断动作开始和结束。

这些 eval 还不成熟，但方向正确：未来实时 AI 产品需要的不只是“回答是否正确”，还要评价**回答是否在正确时刻、以正确方式发生**。

## 7. 限制：这条路线很强，但不便宜，也还没产品化

TML 自己列出的限制很现实。

第一，**长会话上下文膨胀**。连续音视频会极快积累上下文。streaming session 能处理短中程互动，但很长的实时协作需要更主动的 context management：压缩、摘要、遗忘、状态机、可检索记忆，都需要重新设计。

第二，**部署条件苛刻**。低延迟流式音视频依赖稳定网络和 GPU serving。连接抖动会直接伤害体验。普通 SaaS 可以 tolerate 几秒慢响应，实时协作不行。

第三，**大模型太慢**。TML-Interaction-Small 已经是 276B MoE / 12B active；他们承认更大的预训练模型目前太慢，计划未来发布更大模型。这说明“智能 + 实时”仍是系统级 trade-off，不是简单扩大参数就完事。

第四，**安全问题更难**。实时语音里的拒绝不能像文本一样生硬；同时，多轮长语音对话、视觉上下文、并发工具调用，会带来新的越界和误触发风险。TML 用 TTS 生成拒绝/过拒绝训练数据，并用自动化 red-teaming harness 生成多轮 refusal 数据，但这仍是早期工作。

## 8. Builder 应该关注什么

如果你正在做 AI 产品，短期内不一定能直接用 TML 的 research preview，但可以先调整设计假设。

**第一，把 latency budget 当成产品规格。** 不要只测首 token 和总生成时间。实时协作要测 turn-taking latency、interrupt latency、visual event-to-speech latency、tool-result handoff latency。

**第二，减少“低智商 harness”做高智商决策。** VAD、规则 turn detector、固定 agent loop 可以先用，但要明确哪些判断未来应上移给模型：是否插话、是否继续听、是否沉默、是否切后台。

**第三，为前台/后台分层设计 UI。** 用户应该能感知：模型现在是在听我、在看屏幕、在后台查资料，还是准备插入结果。没有这种状态可见性，实时 AI 很容易变成“更吵的聊天机器人”。

**第四，设计可中断的工具调用。** 工具结果不是越快展示越好，而是要在当前人机节奏里找合适窗口。agent infrastructure 需要支持 partial results、cancellation、priority、handoff summary。

**第五，建立新的评测集。** 对教育、客服、编程、设计、运动、医疗等场景，单轮准确率不够。要录制真实 session，标注“何时该说、何时不该说、何时该看、何时该问”。

## 9. 我的判断

TML 这篇文章最重要的地方，不是它宣布了一个 276B MoE interaction model，而是把行业注意力从“AI 能不能独立完成任务”拉回到“AI 如何和人一起完成任务”。过去一年，agent 叙事很容易滑向“人写一句目标，然后等机器交付”。但大量高价值工作并不是这样发生的。

更可能的未来是混合形态：后台 Agent 越来越自治，前台 Interaction Model 越来越像一个实时协作伙伴。用户不需要在“完全自己做”和“完全交给 AI”之间二选一，而是可以随时介入、纠正、观察、委派、收回控制权。

这也是 Thinking Machines Lab 这条路线值得关注的原因：它不是把 prompt box 做得更漂亮，而是在重新定义 human-in-the-loop 的 loop 本身。