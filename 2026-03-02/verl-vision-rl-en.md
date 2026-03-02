# verl: The Open-Source Framework Redefining Reinforcement Learning for Large Language Models

> **TL;DR:** verl (Volcano Engine Reinforcement Learning) is an open-source RL training framework initiated by ByteDance's Seed team and maintained by the community. With its innovative hybrid-controller architecture and 3D-HybridEngine, it achieves 1.5x–20x throughput improvements over existing baselines. As of March 2026, it has **19,500+ GitHub stars** and **3,330+ forks**, making it one of the most active LLM post-training infrastructure projects in the world.

---

## 1. Why Does verl Exist?

The 2024–2025 period saw a fundamental shift in how large language models are trained: **post-training**—particularly reinforcement learning for alignment and reasoning enhancement—went from "nice to have" to "essential." DeepSeek-R1 demonstrated that RL algorithms like GRPO can unlock powerful reasoning capabilities in LLMs.

But RL training at scale is brutally complex:

- **Multi-model orchestration**: PPO requires four models (Actor, Critic, Reference, Reward) running simultaneously
- **Training-generation alternation**: Constant switching between rollout and training phases wastes GPU cycles
- **Distributed complexity explosion**: Each model is itself a distributed program; inter-model communication is many-to-many multicast
- **Rapid algorithm iteration**: Researchers need to quickly experiment with PPO, GRPO, DAPO, VAPO, and beyond

Existing frameworks force a trade-off: either flexible but slow (single-controller like DeepSpeed-Chat) or fast but rigid (multi-controller like OpenRLHF). verl was built to eliminate this trade-off.

---

## 2. Core Architecture: HybridFlow

verl's academic paper, **HybridFlow** (published at EuroSys 2025), introduces a hybrid paradigm that combines the best of both worlds:

### 2.1 The Programming Model

```
┌─────────────────────────────────────────────┐
│           Single Controller (Python)         │
│  ┌───────┐  ┌───────┐  ┌───────┐  ┌──────┐ │
│  │ Actor │  │Critic │  │  Ref  │  │Reward│ │
│  │(Multi-│  │(Multi-│  │(Multi-│  │(Multi│ │
│  │ Ctrl) │  │ Ctrl) │  │ Ctrl) │  │Ctrl) │ │
│  └───────┘  └───────┘  └───────┘  └──────┘ │
└─────────────────────────────────────────────┘
```

- **Inter-node level**: A single controller orchestrates the RL dataflow using native Python syntax to define algorithm logic
- **Intra-node level**: Each model internally uses a multi-controller paradigm for efficient distributed computation (FSDP/Megatron-LM)
- **Result**: Define complex RL algorithms like PPO/GRPO in a few lines of code, while maintaining near-hand-optimized performance

### 2.2 3D-HybridEngine

This is verl's most critical performance innovation. During RL training, the Actor model must constantly switch between **training mode** (parameter sharding) and **generation mode** (requires full weights). Traditional approaches either maintain redundant copies (wasting GPU memory) or perform full communication (bandwidth bottleneck).

3D-HybridEngine achieves:
- **Zero memory redundancy** model resharding
- Significantly reduced communication overhead
- Flexible mapping across DP×TP×PP 3D parallelism

Experimental results: **1.53x to 20.57x throughput improvement** over state-of-the-art baselines.

### 2.3 Flexible Device Mapping

verl supports placing different models on different GPU sets, scaling efficiently from a single 8-GPU machine to clusters with hundreds of GPUs. This typically requires extensive manual configuration in other frameworks.

---

## 3. Supported Algorithms and Models

### RL Algorithms (as of March 2026)

| Algorithm | Description |
|-----------|-------------|
| **PPO** | Classic Proximal Policy Optimization |
| **GRPO** | Group Relative Policy Optimization (DeepSeek) |
| **DAPO** | Distributed Alignment PPO, 50 pts on AIME 2024 |
| **VAPO** | Value-Augmented PPO, 60.4 pts on AIME 2024 |
| **REINFORCE++** | Enhanced REINFORCE |
| **RLOO** | Leave-One-Out policy gradient |
| **ReMax** | Maximum reward RL |
| **PF-PPO** | Policy-Filtered PPO (ICML 2025) |
| **PRIME** | Process reward model guided training |
| **SPPO** | Self-Play Preference Optimization |
| **DrGRPO** | Regularized GRPO variant |
| **GSPO** | Group-based scoring policy optimization |

### Model Support

- **Text**: Qwen-3, Qwen-2.5, LLaMA 3.1, Gemma2, DeepSeek-LLM (including 671B MoE)
- **Vision-Language**: Qwen2.5-VL, Kimi-VL, Qwen3-VL
- **Scale**: From 1.5B to **671B** (trillion-parameter scale via Expert Parallelism)

### Backend Integration

- **Training**: FSDP, FSDP2, Megatron-LM
- **Inference**: vLLM, SGLang, HuggingFace Transformers
- **Hardware**: NVIDIA, AMD, Huawei Ascend

---

## 4. Multimodal and Vision RL: The New Frontier

verl is not just a text-LLM RL framework—it is becoming the **standard infrastructure for multimodal RL training**.

### 4.1 Native VLM Support

The main repository directly supports GRPO training for vision-language models like Qwen2.5-VL with ready-to-use example scripts. This means you can use RL to enhance a VLM's visual reasoning—for example, teaching a model to "see" and solve geometry problems.

### 4.2 VLA (Vision-Language-Action) Experiments

Under `verl/experimental/vla`, the team is exploring RL training for vision-language-action models, directly connecting to the needs of embodied AI.

### 4.3 Multi-Turn Tool Calling

verl supports multi-turn conversation + tool-calling RL training via SGLang integration—a critical capability for building agent systems.

---

## 5. The Ecosystem: Who's Building on verl?

Perhaps verl's most impressive aspect isn't the framework itself, but the thriving ecosystem growing around it:

### 5.1 Easy-R1

- **Repository**: [hiyouga/EasyR1](https://github.com/hiyouga/EasyR1)
- **Focus**: A user-friendly fork of verl specializing in multimodal VLM RL training
- **Highlights**: Extremely low barrier to entry, one-click Docker deployment, supports Qwen2.5-VL/Qwen3-VL
- **Team**: LLaMA-Factory (hiyouga), one of the most active open-source forces in China's LLM community
- **Significance**: Made VLM+RL accessible to everyone, not just research labs

### 5.2 verl-agent

- **Repository**: [langfengQ/verl-agent](https://github.com/langfengQ/verl-agent)
- **Focus**: Agent training extension for verl
- **Key Innovation**: **Step-independent multi-turn rollout mechanism**—instead of simply concatenating histories, each step has customizable input structures, history management, and memory modules
- **Algorithms**: GiGPO (Group-in-Group Policy Optimization, NeurIPS 2025), HGPO (ICLR 2026)
- **Environments**: ALFWorld, WebShop, Sokoban, Search tool-calling, AppWorld
- **Significance**: Extends verl from "model training" to "agent training"

### 5.3 VAGEN

- **Repository**: [mll-lab-nu/VAGEN](https://github.com/mll-lab-nu/VAGEN)
- **Focus**: Multi-turn RL framework for training VLM agents
- **Core Idea**: FreeThink—trains VLM agents to produce natural language reasoning, allowing visual state reasoning to emerge without predefined structures
- **Built on**: verl's agent-loop infrastructure

### 5.4 verl-recipe

- **Repository**: [verl-project/verl-recipe](https://github.com/verl-project/verl-recipe)
- **Focus**: Official algorithm recipe repository containing full reproduction code for DAPO, PRIME, SPPO, DrGRPO, and more
- **Significance**: Transforms verl from a framework into a reproducible research platform

### 5.5 Additional Ecosystem Projects

- **ReTool**: Multi-turn conversation + code sandboxing to improve mathematical reasoning
- **OpenManus-RL**: Supports verl-agent-style training pipelines
- **ROLL (Alibaba)**: Integrated GiGPO algorithm from verl-agent
- **Megatron-Bridge (NVIDIA)**: Joint trillion-parameter model training with verl

---

## 6. Landmark Research Results

verl isn't just infrastructure—it has directly powered multiple state-of-the-art research achievements:

### DAPO (March 2025)
- Based on Qwen2.5-32B pretrained model
- **50 points on AIME 2024**, surpassing DeepSeek-R1-Zero
- Fully trained using verl, code open-sourced

### VAPO (April 2025)
- Value-based Augmented PPO
- **60.4 points on AIME 2024**, outperforming DAPO
- Paper: arXiv:2504.05118

### Seed-Thinking-v1.5 (April 2025)
- ByteDance Seed team's internal model
- **AIME 2024: 86.7** | Codeforces: 55.0 | GPQA: 77.3
- Trained with verl

### Doubao-1.5-pro (January 2025)
- ByteDance's Doubao LLM v1.5
- RL scaling preview reached OpenAI O1-level math performance
- AIME pass@1: 70.0

### Mind Lab Trillion-Parameter RL (December 2025)
- Using verl + Megatron-Bridge
- GRPO LoRA training for **trillion-parameter model** on 64 H800 GPUs

---

## 7. How verl Compares to Other Frameworks

| Dimension | verl | OpenRLHF | DeepSpeed-Chat | TRL |
|-----------|------|----------|----------------|-----|
| **Architecture** | Hybrid controller | Multi-controller | Single controller | Single controller |
| **Flexibility** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Throughput** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Max Scale** | 671B (MoE) | 70B+ | 70B | 70B |
| **VLM Support** | ✅ Native | ❌ | ❌ | Limited |
| **Multi-turn Agent** | ✅ | ❌ | ❌ | ❌ |
| **Megatron Support** | ✅ | ❌ | ❌ | ❌ |
| **Community Activity** | 🔥🔥🔥 | 🔥🔥 | 🔥 | 🔥🔥 |

verl's core advantages:
1. **Balances flexibility and efficiency**—the hybrid-controller architecture is unique
2. **Highest scale ceiling**—supports 671B MoE + hundreds of GPUs
3. **Native multimodal support**—VLM, VLA, and Agent coverage
4. **Richest ecosystem**—from algorithm reproduction to agent training, the most downstream projects

---

## 8. Deep Dive: Technical Innovations

### 8.1 Why HybridFlow Beats Pure Single/Multi-Controller

**Single-controller problem (e.g., DeepSpeed-Chat)**: All distributed operations are dispatched by one Python process. Every GPU operation passes through the controller, creating massive scheduling overhead. When models span 64+ GPUs, the controller becomes the bottleneck.

**Multi-controller problem (e.g., native Megatron-LM)**: Each model runs as an independent distributed program—efficient, but inflexible. Implementing a new RL algorithm requires modifying low-level communication logic.

**HybridFlow's solution**:
- Use a single controller to define the RL dataflow (high flexibility)
- Use multi-controllers to execute each model's internal computation (high efficiency)
- Carefully designed hierarchical APIs decouple computation and data dependencies

### 8.2 The Real-World Impact of 3D-HybridEngine

In PPO training, Actor model resharding (switching between training sharding and generation sharding) is the performance killer. verl's 3D-HybridEngine supports zero-redundancy switching across DP×TP×PP 3D parallelism combinations—extremely challenging in engineering, but delivering order-of-magnitude performance gains.

### 8.3 Async and Off-Policy Architecture

verl's experimental directory includes `fully_async_policy`, `one_step_off_policy`, and `transfer_queue` modules, indicating the team is exploring asynchronous RL training—which can further improve GPU utilization and represents the direction of next-generation RL training paradigms.

---

## 9. Who's Behind verl?

### Core Team

verl was initiated by **ByteDance's Seed team**—the fundamental AI research group responsible for technical development of products like Doubao (ByteDance's flagship LLM).

In January 2026, verl migrated to an independent [verl-project](https://github.com/verl-project) GitHub organization, signaling a transition from "corporate project" to "community project."

### Community

- **First in-person meetup**: January 10, 2026 in Shanghai, co-hosted by Volcengine and NVIDIA
- **Academic presentations**: EuroSys 2025, NeurIPS 2024, ICLR 2025, PyTorch Conference 2025, ICML 2025
- **International reach**: AWS AI Hours (Singapore), GOSIM (Paris), Ray Summit, vLLM Meetup, and more

### Key Metrics

| Metric | Value |
|--------|-------|
| GitHub Stars | 19,510 |
| Forks | 3,330 |
| Open Issues | 1,833 |
| Created | October 2024 |
| Language | Python |
| License | Apache-2.0 |

Growing from creation in October 2024 to nearly 20,000 stars by March 2026 is remarkable, reflecting the community's intense demand for high-quality RL training infrastructure.

---

## 10. Why verl Matters

### 10.1 It Fills a Critical Infrastructure Gap

Before verl, LLM RL training meant choosing between toy frameworks from academic labs (functional but slow) or proprietary internal systems from big tech (fast but closed). verl was the first to offer a **production-grade, open-source, and flexible** three-in-one solution.

### 10.2 It Accelerates RL-for-Reasoning Research

Milestone achievements like DAPO, VAPO, and Seed-Thinking were all built on verl, demonstrating that good infrastructure genuinely accelerates research. When researchers don't spend 80% of their time on engineering, they can validate new ideas faster.

### 10.3 It Defines the Direction of Multimodal RL

From text to VLM to VLA, verl is building a unified multimodal RL training stack. In the age of agents and embodied intelligence, this will be core infrastructure.

### 10.4 It Represents a New Model for Open-Source AI Infrastructure

ByteDance open-sourcing an internal system, migrating it to a community organization, and evangelizing it at global academic conferences—this pattern is being adopted by an increasing number of Chinese AI companies. verl is the benchmark case for this model.

---

## Conclusion

verl is not "just another RL training framework." It is **critical infrastructure for the LLM post-training era**, a bridge connecting research innovation with engineering practice, and a signal that the de facto standard for multimodal RL training is taking shape.

If you're doing RL training for LLMs—whether academic research or industrial applications—verl deserves your serious attention.

---

**Links:**
- GitHub: https://github.com/verl-project/verl
- Paper: https://arxiv.org/abs/2409.19256
- Documentation: https://verl.readthedocs.io
- Slack: https://join.slack.com/t/verl-project
- Twitter: https://twitter.com/verl_project
