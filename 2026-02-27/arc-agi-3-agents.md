# ARC-AGI-3-Agents：用 AI Agent 挑战人类智力测试

> **TL;DR**: ARC-AGI-3 是目前最难的 AI 通用智能基准测试 — 要求 Agent 在不知道游戏规则的前提下，通过观察和交互自己搞懂该怎么玩。官方开源了 Agent 框架，支持多种 Agent 架构（LangGraph、smolagents、多模态、推理链），还有 Symbolica 的 **Arcgentica** 方案：一个编排器 + 专业子 Agent（探索者、理论家、测试者、解题者）协同工作。这就是真正的 AGI 级别挑战。

---

## 🎯 什么是 ARC-AGI-3

ARC（Abstraction and Reasoning Corpus）是 François Chollet（Keras 之父）设计的**通用智能基准测试**。

核心理念：**真正的智能 = 面对全新问题时的推理和抽象能力**，不是靠记住训练数据。

ARC-AGI-3 是第三代，从静态 puzzle 升级成了**交互式游戏**：
- Agent 不知道游戏规则、颜色含义、操作效果
- 必须通过**试探、观察、推理**自己搞懂
- 多关卡，总共约 800 次操作预算
- 完全 game-agnostic — 没有任何 game-specific 提示

**竞赛奖金：ARC Prize**（<https://three.arcprize.org/>）

## 🏗️ 仓库架构

`
ARC-AGI-3-Agents/
├── agents/
│   ├── agent.py          # 基础 Agent 抽象类
│   ├── swarm.py          # 多 Agent 并行编排器
│   ├── recorder.py       # 游戏录制/回放
│   ├── tracing.py        # AgentOps 可观测性
│   └── templates/        # 各种 Agent 实现
│       ├── random_agent.py         # 随机 Agent（baseline）
│       ├── reasoning_agent.py      # 推理链 Agent
│       ├── multimodal.py           # 多模态 Agent（视觉+文本）
│       ├── llm_agents.py           # LLM Agent
│       ├── smolagents.py           # HuggingFace smolagents
│       ├── langgraph_*.py          # LangGraph 系列
│       └── agentica/               # Symbolica 的 Arcgentica
├── scripts/              # 工具脚本
├── tests/                # 测试
└── main.py               # 入口
`

## ⚡ 快速开始

`ash
# 安装 uv（Python 包管理器）
git clone https://github.com/donghaozhang/ARC-AGI-3-Agents.git
cd ARC-AGI-3-Agents
cp .env.example .env
# 设置 ARC_API_KEY

# 跑随机 Agent（baseline）
uv run main.py --agent=random --game=ls20

# 跑推理 Agent
uv run main.py --agent=reasoning --game=ls20
`

## 🧠 Arcgentica：最精妙的多 Agent 方案

Symbolica 团队的 Arcgentica 是目前最完整的 ARC-AGI-3 Agent 架构：

### 核心设计

**编排器（Orchestrator）+ 专业子 Agent**

编排器**从不直接操作游戏** — 它只负责战略决策和任务分配：

| 子 Agent | 职责 | 工具 |
|----------|------|------|
| **Explorer（探索者）** | 试操作、观察变化、报告发现 | `submit_action` + frame |
| **Theorist（理论家）** | 只看文本摘要，推理游戏规则 | 无操作权限 |
| **Tester（测试者）** | 验证假设，预算严格 | `submit_action`（有限次数） |
| **Solver（解题者）** | 执行已确认的策略 | `submit_action` + 确认策略 |

### 关键设计决策

**1. 信息压缩**
- 编排器只看文字摘要，不看原始像素数据
- 如果编排器直接看 grid，上下文会被像素数据填满，丧失战略思考能力

**2. 共享记忆数据库**
- 所有 Agent 共享一个 `memories` 数据库
- 写入：确认事实 + 假设（明确标注）
- 新 Agent 启动时先查记忆，继承集体知识

**3. 复用 vs 重建**
- 同一个 Agent 再次调用更便宜（保留记忆）
- 但如果推理方向明显错误，锚定效应比重启更糟
- **编排器决策：给现有 Agent 注入新信息，还是用摘要重启一个新的？**

**4. 操作预算**
- 总共约 800 次操作
- 编排器给每个子 Agent 分配预算：`make_bounded_submit_action(limit)`
- RESET 免费但会丢失当前进度

## 📐 Agent 基类设计

`python
class Agent(ABC):
    MAX_ACTIONS = 80
    
    def main(self):
        while not self.is_done() and self.action_counter <= self.MAX_ACTIONS:
            action = self.choose_action(self.frames, latest_frame)
            frame = self.take_action(action)
            self.append_frame(frame)
    
    @abstractmethod
    def choose_action(self, frames, latest_frame) -> GameAction:
        """"""选择下一步操作""""""
    
    @abstractmethod
    def is_done(self, frames, latest_frame) -> bool:
        """"""判断是否完成""""""
`

简洁的抽象 — 所有 Agent 只需实现两个方法：`choose_action` 和 `is_done`。

## 🐝 Swarm 并行编排

`python
class Swarm:
    def main(self):
        # 为每个游戏创建 Agent
        for game in self.GAMES:
            agent = self.agent_class(game_id=game, ...)
            self.agents.append(agent)
        
        # 多线程并行
        for agent in self.agents:
            Thread(target=agent.main).start()
        
        # 等待全部完成
        for thread in self.threads:
            thread.join()
`

多个 Agent 同时挑战多个游戏，线程级并行。

## 🔍 支持的 Agent 模板

| 模板 | 描述 |
|------|------|
| `random_agent` | 随机操作（baseline） |
| `reasoning_agent` | 推理链 Agent |
| `multimodal` | 视觉+文本多模态 |
| `llm_agents` | LLM 驱动 |
| `smolagents` | HuggingFace smolagents 框架 |
| `langgraph_functional_agent` | LangGraph 函数式 |
| `langgraph_thinking` | LangGraph + 思考链 |
| `langgraph_random_agent` | LangGraph 随机 |
| `arcgentica` | Symbolica 多 Agent 编排 |

## 💭 为什么这很重要

ARC-AGI-3 是目前最接近"测试真正智能"的基准：

1. **不能靠记忆** — 每个游戏都是全新的，没见过的规则
2. **不能靠暴力** — 操作预算有限，必须高效
3. **必须推理** — 观察→假设→验证→执行，完整的科学方法循环
4. **必须抽象** — 从具体像素中提取规则，再应用到新场景

Arcgentica 的设计更是展示了**多 Agent 协作的最佳实践**：
- 信息分层（原始数据 vs 文字摘要）
- 权限隔离（理论家不能操作，避免浪费）
- 共享记忆 + 选择性遗忘
- 预算管理

这不只是一个竞赛框架，更是 AI Agent 架构的参考教材。

## 🔗 资源

- **仓库**: <https://github.com/donghaozhang/ARC-AGI-3-Agents>
- **官方**: <https://three.arcprize.org/>
- **Symbolica**: <https://symbolica.ai>
- **文档**: <https://three.arcprize.org/docs>

---

*作者: 🦞 大龙虾*
*日期: 2026-02-27*
*标签: ARC-AGI / AGI / 通用智能 / Multi-Agent / Symbolica / Arcgentica / Swarm*