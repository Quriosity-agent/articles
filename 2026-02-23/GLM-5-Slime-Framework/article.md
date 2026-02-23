# 揭秘GLM-5技术底牌：「异步强化学习框架Slime」成终极杀招

**Source:** 机器之心 (WeChat)  
**URL:** https://mp.weixin.qq.com/s/Qmg6iOYo2BXB9qFf4TOpsg  
**Date:** 2026-02-23  
**Topic:** GLM-5, Async RL, Slime Framework, Agentic Engineering

---

## Summary

智谱发布 GLM-5 旗舰基座模型技术报告，揭示三大核心创新：DSA 稀疏注意力架构、异步强化学习框架 Slime、以及 Agent 强化学习算法。GLM-5 面向 Agentic Engineering 打造，在 SWE-bench、Terminal-Bench、BrowseComp 等基准测试中取得开源 SOTA 级表现。

## Key Points

### 1. DSA (DeepSeek Sparse Attention) — 降低训练与推理成本
- 动态打分，只挑出真正相关的少数 token 参与计算
- 长文本中约 90% 的注意力计算是冗余的，DSA 将长序列计算量压缩 1.5-2 倍
- GLM-5 参数规模扩展至 744B（40B 激活参数），训练 token 总量 28.5T
- **Muon Split 机制**：将矩阵拆分为不同头的更小矩阵，独立应用矩阵正交化
- **MLA-256 变体**：head dimension 从 192 提到 256，注意力头数减少 1/3，解码计算量显著下降
- 共享 3 层 MTP 参数，提升 token 接受率

### 2. Slime 框架 — 异步 RL 基础设施
- **核心问题**：传统同步 RL 中，整批训练速度由最慢的轨迹决定，GPU 大量空转
- **解法**：推理引擎与训练引擎部署在不同 GPU 上，完全异步并行运行
  - 推理引擎持续生成轨迹，累积到阈值后批量推送给训练引擎
  - 训练引擎持续消费数据、更新参数，每 K 次梯度更新后同步回推理引擎
- **TITO Gateway**：直接截获推理引擎的 token ID 序列和元数据，绕过文本中转，避免 tokenize 不一致
- **双侧重要性采样**：复用 rollout 时记录的 log 概率作为行为策略代理
  - 重要性采样比在区间内的 token 正常计算梯度
  - 超出范围的 token 梯度直接置零

### 3. Agent RL — 锻造长程智能体
- **DSA + RL 稳定性**：将非确定性 CUDA top-k 算子替换为确定性 torch.topk，冻结 Indexer 参数
- **RepoLaunch 框架**：构建 10000+ 可验证 SWE 环境，覆盖 Python/Java/Go 等 9 种语言
- **HTML 幻灯片三级奖励体系**：
  - Level-1：静态规则（布局、间距、字体）
  - Level-2：运行布局（分布式渲染，真实几何指标）
  - Level-3：视觉感知（异常空白、构图失衡检测）
  - 16:9 合规率从 40% 提升至 92%
- **跨阶段蒸馏**：解决多阶段 RL 训练中的灾难性遗忘
- **分层上下文管理 (HCM)**：BrowseComp 准确率从 55.3% 提升至 75.9%

## Performance
- 在 Coding & Agent 任务上取得开源 SOTA
- 与 Claude Opus 4.5 接近，部分任务超越
- 全栈适配 7 家国产 GPU（华为昇腾、摩尔线程、海光、寒武纪、昆仑芯、沐曦、燧原）

## References
- 技术报告: https://arxiv.org/pdf/2602.15763
- GitHub: https://github.com/zai-org/GLM-5
