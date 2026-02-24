# Polymarket 官方 CLI：终端里玩预测市场，也是 AI Agent 的交易接口

**来源：GitHub - Polymarket/polymarket-cli**

---

## 一句话总结

Polymarket 发布了官方 Rust CLI 工具，让你在终端中浏览市场、下单交易、管理持仓和操作链上合约——所有命令支持 JSON 输出，天然适配脚本和 AI Agent。

---

## Polymarket 是什么？

Polymarket 是目前最大的去中心化预测市场平台，运行在 Polygon 链上。用户用 USDC 对真实世界事件下注（"BTC 年底能到 10 万吗？""某某会赢大选吗？"），价格反映市场共识概率。2024 年美国大选期间 Polymarket 爆火，单个市场交易量超过 1.45 亿美元。

---

## CLI 能做什么？

### 不需要钱包就能用（只读）

- **浏览市场** — `polymarket markets list` 查看所有活跃市场
- **查看事件** — `polymarket events list --tag politics` 按标签筛选
- **订单簿** — `polymarket clob book <market_id>` 查看买卖盘
- **价格历史** — `polymarket clob price-history <id> --interval 1d`
- **链上数据** — 查看合约状态、条件代币信息

### 需要钱包（交易）

- **限价单** — `polymarket clob create-order <id> buy yes 0.55 100` （以 55 美分买 100 份 Yes）
- **市价单** — `polymarket clob market-order <id> buy yes 50`
- **撤单** — 单个撤、按市场撤、全部撤
- **CTF 操作** — 拆分、合并、赎回条件代币
- **跨链桥** — 从其他链充值到 Polymarket

### 订单类型

| 类型 | 说明 |
|------|------|
| **GTC** | Good Till Cancelled（默认） |
| **FOK** | Fill or Kill（全成或全撤） |
| **GTD** | Good Till Date（到期自动撤） |
| **FAK** | Fill and Kill（部分成交，剩余撤销） |

---

## 为什么有 AI Agent 的味道？

关键设计：**所有命令都支持 `--output json`**。

```bash
polymarket markets list --active -o json
polymarket clob book <market_id> -o json
polymarket clob trades -o json
```

这意味着 AI Agent 可以：
1. 用 JSON 解析市场数据
2. 基于分析自动下单
3. 监控持仓并动态调整
4. 全程脚本化，无需人工干预

错误处理也是结构化的——JSON 模式输出 `{"error": "..."}` 到 stdout，非零退出码。对自动化来说非常友好。

---

## 技术细节

- **语言**：Rust（性能和安全性）
- **链**：Polygon（低 gas 费）
- **代币**：USDC（稳定币）+ ERC-1155 条件代币
- **钱包**：支持私钥、环境变量或配置文件三种方式
- **签名类型**：Proxy（默认）、EOA、Gnosis Safe
- **交互式 Shell**：`polymarket shell` 进入 REPL 模式

### 安装

```bash
# macOS / Linux (Homebrew)
brew install polymarket/tap/polymarket

# Shell 脚本
curl -fsSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh

# 从源码编译
cargo install --git https://github.com/Polymarket/polymarket-cli
```

---

## 典型工作流

### 研究市场
```bash
polymarket markets list --active --order volume
polymarket events get <event_id>
polymarket clob book <market_id>
polymarket clob price-history <id> --interval 1w
```

### 设置钱包并开始交易
```bash
polymarket wallet create
polymarket approve set         # 授权 USDC 和条件代币
polymarket clob create-order <id> buy yes 0.40 50
```

### 监控组合
```bash
polymarket clob positions
polymarket clob orders --open
polymarket clob trades --limit 20
```

---

## 为什么值得关注？

1. **预测市场 + AI Agent** — JSON API 天然适配自动化交易，可以想象一个 Agent 持续监控新闻、分析概率偏差、自动下单
2. **DeFi CLI 标杆** — 结构清晰的 Rust CLI，命令分组合理，输出格式统一，是 DeFi 工具的设计范本
3. **链上操作封装** — CTF 拆分/合并/赎回、跨链桥等复杂操作一行命令搞定
4. **⚠️ 实验性软件** — 官方明确警告：早期实验阶段，不要投入大额资金

---

*仓库：<https://github.com/Polymarket/polymarket-cli>*
*协议：MIT*
*本文基于该开源仓库内容编译整理。*
