# Arcgentica 架构拆解：Symbolica 如何用多 Agent 编排打 ARC-AGI-3

> **TL;DR:** Symbolica AI 开源了 Arcgentica —— 一个基于 Agentica SDK 的 ARC-AGI-3 多 Agent harness。核心思路：一个 Orchestrator 管全局，动态 spawn Explorer / Theorist / Solver 子 Agent，通过共享 Memory 数据库跨 Agent 传递知识，配合 action budget 控制资源消耗。代码干净，prompt 工程扎实，值得做 Agent 系统的人仔细看。

**Repo:** [symbolica-ai/ARC-AGI-3-Agents (symbolica/arcgentica 分支)](https://github.com/symbolica-ai/ARC-AGI-3-Agents/tree/symbolica/arcgentica)

---

## 背景：ARC-AGI-3 是什么

ARC-AGI-3 是 ARC Prize 推出的第三代通用智能基准测试。跟前两代不同，AGI-3 是一个**视觉交互游戏**——Agent 面对一个 64×64 的彩色网格，需要通过方向键、空格和鼠标点击等操作，在多个关卡中发现游戏规则并通关。没有说明书，没有教程，纯靠试。

这对 Agent 系统是个极好的试炼场：你必须做探索、形成假说、验证、迭代，还要在有限的 action 预算内完成。

## 整体架构

![ARC-AGI-3 Game Interface](https://opengraph.githubassets.com/1/symbolica-ai/ARC-AGI-3-Agents)

*图片来源：[symbolica-ai/ARC-AGI-3-Agents](https://github.com/symbolica-ai/ARC-AGI-3-Agents/tree/symbolica/arcgentica) GitHub OG 图*

Arcgentica 的架构可以用一句话概括：**Orchestrator 不玩游戏，只调度 Agent。**

```
Orchestrator (Claude Opus 4.6 / GPT-5.2)
  │
  ├── spawn_agent("Explorer") + bounded_submit_action(50)
  │     ├── 探索网格、测试操作、记录发现
  │     └── 写入 Memories
  │
  ├── spawn_agent("Theorist")
  │     ├── 读 Memories、分析 Explorer 报告
  │     └── 形成/验证假说
  │
  └── spawn_agent("Solver") + bounded_submit_action(100)
        ├── 读 Memories 获取已知规则
        └── 执行通关序列
```

### 关键设计决策

**1. Orchestrator 只管不做**

Orchestrator 拿不到 `submit_action`，只有 `make_bounded_submit_action(limit)` 工厂函数。它**必须**把操作权下放给子 Agent。这不是建议，是架构层面的硬约束。

```python
# Orchestrator 的作用域里没有 submit_action
# 只能创建有预算限制的版本给子 Agent
orchestrator = await spawn(
    model=self.model.main_agent_model,
    premise=premise(self.model),
    scope={
        "spawn_agent": self.spawn_agent,
        "make_bounded_submit_action": make_bounded_submit_action,
        "memories": memories,
        ...
    },
)
```

**2. Action Budget 是硬性约束**

`bounded_submit_action` 是一个带计数器的 wrapper。NOOP 和 RESET 不计数，但 ACTION1-ACTION6 每次调用都递减。超预算直接抛异常。

```python
class bounded_submit_action:
    def __call__(self, action_name, x=0, y=0):
        if upper != "NOOP" and upper != "RESET":
            if self._used >= self._limit:
                raise ValueError("Action budget exhausted")
            self._used += 1
        return self._inner(action_name, x, y)
```

为什么这很重要？因为子 Agent spawn 子子 Agent 时，共享同一个 `submit_action`——预算不会被重置。这防止了 Agent 无限套娃消耗资源。

**3. 共享 Memory 是跨 Agent 知识传递的核心**

`Memories` 类不只是一个 list。它有：
- `add(summary, details)` —— 结构化写入
- `summaries()` —— 快速浏览已知信息
- `query(return_type, question)` —— 自然语言查询，底层用一个独立的 memory agent 做检索

```python
# 自然语言查询 memory
result = await memories.query(str, "What does ACTION3 do?")
failed = await memories.query(list[str], "What strategies have failed?")
```

这意味着一个 Explorer 发现"ACTION5 是确认键"之后，Solver 不需要重新探索——直接问 memory 就行。

## Frame：Agent 看到的世界

`Frame` 类是 Agent 与游戏交互的核心接口。它包装了 64×64 的 grid 数据，提供了一套实用的检查工具：

| 方法 | 用途 |
|------|------|
| `render(crop=...)` | 文本渲染网格，支持裁剪 |
| `diff(other)` | 找出两帧之间的变化区域 |
| `change_summary(other)` | 一行一个区域的变化摘要 |
| `find(*colors)` | 找到指定颜色的所有像素 |
| `bounding_box(*colors)` | 颜色的包围盒 |
| `color_counts()` | 颜色频率统计 |

Frame 是**不可变的**——一旦创建就不能修改。这保证了 Agent 在推理时不会意外篡改游戏状态。

```python
# 每次操作后检查变化
new_frame = submit_action("ACTION4")  # 向右移动
print(new_frame.change_summary(old_frame))
# 输出: "24 cells changed across 3 region(s):
#   [10,5)-[15,10): 8 cells -- 0→5 ×6, 3→5 ×2 ..."
```

## Prompt 工程：不是提示词，是操作手册

`prompts.py` 里的 `GAME_REFERENCE` 不是普通的 system prompt，更像一份 Agent 操作手册。几个亮点：

**坐标是手段不是目的：**
> "Think 'A must reach B' not 'A must reach row 38.' If your hypothesis includes a specific coordinate as part of the goal, it is wrong."

**RESET 是最后手段：**
> "RESET throws away ALL the work you did on this attempt... NEVER reset to 'think more carefully' or to 'try a clean approach.'"

**知道什么时候该放弃：**
> "If you have tried 2-3 variations of an approach and none produce the expected result, do NOT keep trying. Return to your caller with a clear report."

这些不是空话——它们直接影响 Agent 的行为模式，减少无谓的 action 浪费。

## 模型配置

支持两套预设：

| 配置 | 主 Agent | 子 Agent | Context | Reasoning |
|------|----------|----------|---------|-----------|
| OPUS_4_6 | claude-opus-4-6 | claude-opus-4-6 | 200K | high |
| GPT_5_2 | gpt-5.2 | gpt-5.2 | 400K | high |

用 `ModelConfig` dataclass 管理，切换模型只需改一行。

## 可视化和调试

Arcgentica 内置了一个 WebSocket 实时可视化系统：

- `EventServer` —— WebSocket 服务器 + JSONL 日志
- `WsLogger` —— 把 Agent 生命周期事件推送到前端
- `UsageTracker` —— token 用量追踪
- 单文件 HTML 前端，无构建步骤
- 支持录制回放（`replay.py`）

```bash
# 启动可视化
VISUALIZE=1 uv run main.py --agent=arcgentica --game=ls20

# 回放录制
uv run python -m agents.templates.agentica.logging.replay session.jsonl --speed 4
```

## 实战表现

从 Symbolica 的公开记录来看，他们已经在多个 ARC-AGI-3 游戏上跑通了完整流程：ls20、vc33、ft09 等，并且提供了完整的回放日志。他们还在持续扩展到 25+ 个游戏（ar25, bp35, cd82, cn04 等），说明这个架构具有一定的泛化能力。

## 对 Agent 开发者的启发

1. **Orchestrator 不应该直接干活。** 把决策权和执行权分离，让管理者管理、执行者执行。用架构约束（不给 submit_action）而不是靠 prompt 约束。

2. **共享 Memory 比传消息更高效。** 子 Agent 之间不需要直接通信——都写进 Memory，都从 Memory 读。简单、解耦、可扩展。

3. **给 Agent 预算，然后硬执行。** `bounded_submit_action` 的设计很优雅：计数器、共享状态、超限报错。比"请节约使用"这种 prompt 靠谱一百倍。

4. **不可变数据结构减少 bug。** Frame 一旦创建就不能改。Agent 需要比较两个状态？用 diff。不用担心谁改了谁。

5. **Prompt 是设计文档的一部分。** Arcgentica 的 prompt 不是事后补的，是跟代码一起设计的。每条规则都有代码层面的对应。

---

**Source:** [symbolica-ai/ARC-AGI-3-Agents](https://github.com/symbolica-ai/ARC-AGI-3-Agents/tree/symbolica/arcgentica) — MIT License

🦞
