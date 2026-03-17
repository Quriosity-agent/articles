# Attention Residuals：用注意力机制替换残差连接，Transformer 性能直接起飞

> 来源：[MoonshotAI/Attention-Residuals](https://github.com/MoonshotAI/Attention-Residuals) | [arXiv 2603.15031](https://arxiv.org/abs/2603.15031)
> Kimi Team (Moonshot AI)

## 一句话总结

标准残差连接（residual connection）对每一层输出做"等权累加"，层数一多就稀释了每一层的贡献，隐状态幅值还会无限增长。**AttnRes** 把这个固定累加换成了 softmax 注意力——每一层可以"选择性"地关注之前哪些层的输出，性能全面提升，而且是 **drop-in replacement**。

---

## 问题：标准残差连接的两个硬伤

1. **贡献稀释**：每一层的输出都以权重 1 加进来，层数越深，早期层的信号越弱
2. **幅值爆炸**：PreNorm 架构下，隐状态的 magnitude 随深度单调递增，这是个已知问题

```
h_l = h_{l-1} + F_l(h_{l-1})   ← 标准残差，权重永远是 1
```

---

## 解法：AttnRes

用 softmax attention 替换固定权重：

$$\mathbf{h}_l = \sum_{i=0}^{l-1} \alpha_{i \to l} \cdot \mathbf{v}_i$$

每一层有一个学习到的 pseudo-query $\mathbf{w}_l \in \mathbb{R}^d$，通过它计算对前面所有层输出的注意力权重 $\alpha_{i \to l}$。

**关键点：**
- 权重是 **input-dependent**（内容感知）
- 每一层可以自主决定"听谁的"
- 本质上给了每层 selective access to all earlier representations

---

## 两种变体

### Full AttnRes
每一层直接 attend over 所有前面层的输出。简单粗暴，但内存开销 O(Ld)——层数多了吃不消。

### Block AttnRes（实用版）
把层分成 N 个 block：
- block 内部用标准残差连接
- block 之间用注意力聚合

内存从 O(Ld) 降到 O(Nd)。论文发现 **~8 个 block** 就能恢复 Full AttnRes 的大部分收益。

![AttnRes 架构概览](https://raw.githubusercontent.com/MoonshotAI/Attention-Residuals/master/assets/overview.png)
*图片来源：[MoonshotAI/Attention-Residuals](https://github.com/MoonshotAI/Attention-Residuals)*

---

## 核心代码（伪代码级别）

```python
def block_attn_res(blocks, partial_block, proj, norm):
    """
    blocks: 之前完成的 block 表示 [B, T, D]
    partial_block: 当前 block 的部分累加
    """
    V = torch.stack(blocks + [partial_block])  # [N+1, B, T, D]
    K = norm(V)
    logits = torch.einsum('d, n b t d -> n b t', proj.weight.squeeze(), K)
    h = torch.einsum('n b t, n b t d -> b t d', logits.softmax(0), V)
    return h
```

实现非常轻量：
- 一个 RMSNorm
- 一个线性投影（pseudo-query）
- 一次 softmax
- 两次 einsum

**这就是为什么说它是 drop-in replacement —— 改动极小，收益明显。**

---

## Benchmark 结果

| 类别 | 基准测试 | Baseline | AttnRes | 提升 |
|------|----------|----------|---------|------|
| 通用 | MMLU | 73.5 | 74.6 | +1.1 |
| 通用 | GPQA-Diamond | 36.9 | 44.4 | **+7.5** |
| 通用 | BBH | 76.3 | 78.0 | +1.7 |
| 通用 | TriviaQA | 69.9 | 71.8 | +1.9 |
| 数学&代码 | Math | 53.5 | 57.1 | +3.6 |
| 数学&代码 | HumanEval | 59.1 | 62.2 | +3.1 |
| 数学&代码 | MBPP | 72.0 | 73.9 | +1.9 |
| 中文 | CMMLU | 82.0 | 82.9 | +0.9 |
| 中文 | C-Eval | 79.6 | 82.5 | +2.9 |

**最大亮点：**
- GPQA-Diamond **+7.5**（多步推理）
- HumanEval **+3.1**（代码生成）
- 全面正向，没有一个指标下降

---

## Scaling Law

Block AttnRes 在所有计算预算下都优于 baseline。论文给出的数据：**Block AttnRes 的 loss 等价于用 1.25x 更多计算训练的 baseline**。

换句话说：同样的效果，AttnRes 能省 20% 的训练计算量。

![Scaling Law](https://raw.githubusercontent.com/MoonshotAI/Attention-Residuals/master/assets/scaling_law.png)
*图片来源：[MoonshotAI/Attention-Residuals](https://github.com/MoonshotAI/Attention-Residuals)*

---

## 训练动态

AttnRes 还解决了 PreNorm 的两个顽疾：
1. **输出幅值保持有界** —— 不再随深度爆炸
2. **梯度范数分布更均匀** —— 各层都能得到有效训练

![训练动态](https://raw.githubusercontent.com/MoonshotAI/Attention-Residuals/master/assets/training_dynamics.png)
*图片来源：[MoonshotAI/Attention-Residuals](https://github.com/MoonshotAI/Attention-Residuals)*

---

## Builder 视角：为什么值得关注

1. **改动极小**：不需要改架构，就是换个残差连接的方式。几十行代码的事。
2. **收益确定**：全 benchmark 正向，没有 trade-off。GPQA +7.5 和 HumanEval +3.1 是实打实的。
3. **可扩展**：Block AttnRes 的 O(Nd) 内存开销完全可控，~8 block 就够了。
4. **来自 Kimi 团队**：这是 Moonshot AI 实际在生产模型上验证过的技术，不是纯学术实验。

**如果你在训练自己的 Transformer 模型，AttnRes 是目前看到的最低成本、最高回报的架构改进之一。**

---

## 引用

```bibtex
@misc{chen2026attnres,
  title   = {Attention Residuals},
  author  = {Kimi Team and Chen, Guangyu and Zhang, Yu and Su, Jianlin and ...},
  year    = {2026},
  eprint  = {2603.15031},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CL}
}
```

---

🦞
