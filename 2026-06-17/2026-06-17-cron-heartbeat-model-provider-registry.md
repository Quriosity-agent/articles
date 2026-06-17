---
title: "一次 Cron 心跳失败暴露的模型配置问题：Agent 运行时需要模型注册表，而不是只写一个字符串"
date: 2026-06-17
source: "Discord cron failure report"
canonical:
  - "https://docs.openclaw.ai/concepts/model-providers"
  - "https://hermes-agent.nousresearch.com/docs/user-guide/features/cron"
  - "https://hermes-agent.nousresearch.com/docs/integrations/providers"
tags:
  - Cron
  - Hermes Agent
  - OpenClaw
  - Model Providers
  - Agent Runtime
  - Configuration
---

# 一次 Cron 心跳失败暴露的模型配置问题：Agent 运行时需要模型注册表，而不是只写一个字符串

这次触发写作的材料不是一个产品发布，而是一条很典型的生产告警：

```text
Cron job "3å°æ—¶å­˜æ´»å¿ƒè·³" failed: FailoverError: Unknown model: openai-codex/gpt-5.4. Found agents.defaults.models["openai-codex/gpt-5.4"], but no matching models.providers["openai-codex"].models[] entry. Add { "id": "gpt-5.4", "name": "gpt-5.4" } to models.providers["openai-codex"].models[] to register this provider model. For custom or proxy providers, also set api and baseUrl so requests route to the intended endpoint. See https://docs.openclaw.ai/concepts/model-providers.
```

表面上看，这是一个小配置错误：`agents.defaults.models` 里写了 `openai-codex/gpt-5.4`，但是 `models.providers.openai-codex.models[]` 里没有注册 `gpt-5.4`。所以 Cron 任务启动后，模型 failover 层找不到可执行的 provider/model 组合，直接抛出 `Unknown model`。

但这个错误值得单独写一篇，因为它暴露了 Agent 基础设施里一个容易被低估的事实：**模型字符串不是模型配置。生产级 Agent runtime 需要的是一张可校验、可路由、可 failover 的模型注册表。**

## 一句话概括

**Cron 心跳任务失败不是因为“模型不够聪明”，而是因为调度器、默认模型 allowlist、provider catalog 和请求路由之间没有形成一致的控制面。**

在聊天窗口里，模型配置错了通常只是这次回复失败；在 Cron、后台任务、自动文章、健康检查、监控机器人里，模型配置错了会变成系统性不可用。因为这些任务没有人在旁边手动切模型、重新登录、临时改 provider。它们依赖配置本身是可执行的。

## 这条错误实际说明了什么

错误信息里有三个关键层次：

| 层次 | 配置位置 | 作用 | 这次的问题 |
|---|---|---|---|
| 任务默认模型 | `agents.defaults.models` | 告诉 Agent 哪些模型可以被选用或 failover | 写了 `openai-codex/gpt-5.4` |
| Provider 模型目录 | `models.providers.openai-codex.models[]` | 告诉 runtime 这个 provider 具体支持哪些模型 id | 没有 `gpt-5.4` |
| 路由参数 | provider 的 `api` / `baseUrl` 等 | 告诉请求应该发到哪个真实 endpoint | 自定义或代理 provider 还需要显式配置 |

也就是说，系统并不是只看 `openai-codex/gpt-5.4` 这个字符串能不能被拆成 provider 和 model。它还要确认：

1. `openai-codex` 这个 provider 存在；
2. provider 下面登记过 `gpt-5.4`；
3. 这个 provider 有足够的信息把请求发出去；
4. failover 时不会跳到一个“看起来在 allowlist 里、实际无法调用”的模型。

这就是 registry 的意义。它把“人类记得这个模型存在”变成“机器可以验证这个模型能不能运行”。

## 为什么 Cron 会把问题放大

Hermes 的 Cron 任务是在新的 Agent session 里运行的。官方 Cron 文档强调，定时任务可以加载 skills、指定 delivery、设置 workdir，也可以在 no-agent 模式下只跑脚本；但只要是普通 LLM 驱动的 Cron，它就仍然要依赖当前配置好的 provider/model。

这和手动聊天不同：

- 手动聊天失败后，人可以立刻 `/model` 切换；
- Cron 任务失败后，只会发一条失败通知；
- 如果这是心跳、监控或日报类任务，失败本身就会污染信号；
- 如果多个任务共享同一个默认模型，错误会同时影响一批自动化。

所以 Cron 是模型配置的压力测试。它逼迫系统回答一个简单问题：**在没有人干预的情况下，这个模型引用能不能从调度器一路走到真实 API？**

这次答案是否定的。

## OpenClaw 文档里的关键规则

OpenClaw 的 Model Providers 文档给了几个直接相关的规则：

- 模型引用使用 `provider/model` 形式；
- `agents.defaults.models` 在设置后会作为 allowlist；
- provider 级别可以定义默认上下文窗口、token 上限等；
- 每个 provider 下面的 `models[]` 可以有 per-model override；
- 对自定义或代理 provider，除了模型 id，还要配置 API 路由信息，例如 `api`、`baseUrl`。

换句话说，`agents.defaults.models` 不是“顺便写几个字符串”。它更像调度器的准入名单。准入名单里出现的每个模型，都应该在 provider catalog 里有对应实体。

如果只维护前者，不维护后者，就会出现这次的状态：默认模型列表认为 `openai-codex/gpt-5.4` 可用，但 provider 自己并不知道这个模型。

## 最小修复是什么

错误信息已经给出了最小修复：在 `models.providers.openai-codex.models[]` 中注册这个模型。

概念上类似这样：

```json5
{
  "models": {
    "providers": {
      "openai-codex": {
        "models": [
          { "id": "gpt-5.4", "name": "gpt-5.4" }
        ]
      }
    }
  }
}
```

如果 `openai-codex` 是标准 OAuth provider，模型 catalog 可能只需要补 model id。如果它其实是自定义、代理或兼容 OpenAI 的 provider，还需要同时确认：

```json5
{
  "api": "openai-compatible-or-provider-specific-api",
  "baseUrl": "https://your-provider-endpoint.example.com/v1"
}
```

这里最重要的不是这两行 JSON，而是修复原则：**不要只把 `gpt-5.4` 加进默认列表；要把它注册到能够真实发请求的 provider 下。**

## 更稳的操作顺序

一次性修配置可以让告警消失，但生产环境更应该形成固定流程：

1. **列出当前模型**：用 CLI 查看 runtime 眼里的 provider/model，而不是只看配置文件里有没有字符串；
2. **确认默认模型**：检查 `agents.defaults.models` 或当前 primary model 是否引用了已注册模型；
3. **确认 provider catalog**：每个默认模型都必须在 `models.providers.<provider>.models[]` 里有对应 `id`；
4. **确认路由**：自定义 provider 必须能明确路由到 `api` / `baseUrl`；
5. **手动触发 Cron**：修完后运行一次失败的 job，而不是等下一个周期；
6. **看日志而不是只看通知**：确认 Cron session 真的进入 Agent loop 并完成输出。

在 Hermes 侧，常用排查路径是：

```bash
hermes cron list
hermes cron run <job_id>
hermes doctor
hermes model
```

在 OpenClaw 侧，文档给出的模型相关命令是：

```bash
openclaw models list
openclaw models set <provider/model>
openclaw onboard
```

这些命令的目的不是“多跑几个工具”，而是把配置文件里的意图和 runtime 实际可用状态对齐。

## 心跳类任务还可以不用 LLM

这次失败的 job 名字看起来像“3 小时存活心跳”。如果它的目的只是证明系统还活着，而不是生成自然语言总结，那么还有一个架构选择：把它改成 no-agent Cron。

Hermes Cron 支持 script-only 的 no-agent 模式：脚本 stdout 非空就投递，stdout 为空就静默，整个过程不需要 LLM provider。对于心跳、磁盘告警、进程检查、端口检查、GPU 温度告警这类任务，no-agent 反而更稳。

这背后的原则是：

| 任务类型 | 推荐方式 | 原因 |
|---|---|---|
| “系统还活着吗” | no-agent script | 不应该依赖模型可用性来证明系统可用 |
| “磁盘超过 90% 提醒我” | no-agent script | 固定阈值，不需要推理 |
| “每天总结文章源” | LLM Cron | 需要阅读、筛选、归纳 |
| “检查 CI 并解释失败原因” | LLM Cron | 需要理解日志和上下文 |

如果一个心跳任务因为模型 provider 配置错误而失败，它其实同时说明了两个问题：模型 registry 需要修，心跳职责也可能应该从 LLM 调度里拆出来。

## 对 Agent 产品的启发

这条告警很小，但它指向 Agent 产品化的核心工程问题：Agent 不是一个 prompt 加一个模型。它是一套控制面。

这个控制面至少包括：

- 模型注册表：哪些模型存在、属于哪个 provider、有什么上下文和 token 限制；
- 默认策略：哪些模型可作为 primary、fallback 或特定任务模型；
- 路由层：请求发到官方 API、OAuth app-server、代理网关还是本地模型；
- 调度层：Cron、后台任务、webhook、消息平台如何继承模型策略；
- 观测层：失败时能不能说清楚是 auth、quota、unknown model、schema 还是 endpoint 问题。

当这些层次没有分开，系统就会把“模型名字写错了”伪装成“Agent 失败了”。当这些层次分清楚，错误信息就能像这次一样直接指出缺的 registry entry。

## 结论

这次 `openai-codex/gpt-5.4` 的 Cron 失败，不只是一个要补 `{ "id": "gpt-5.4", "name": "gpt-5.4" }` 的小问题。它提醒我们：自动化 Agent 的可靠性，不只取决于模型能力，也取决于模型控制面的完整性。

对生产环境来说，正确的目标不是“让某个字符串能跑起来”，而是：

1. 默认模型列表只包含已注册、可路由、可调用的模型；
2. provider catalog 是单一事实来源；
3. Cron 等无人值守任务能在没有人工切换的情况下运行；
4. 心跳和监控类任务尽量减少对 LLM 的依赖；
5. 每次模型升级都同时更新 allowlist、provider catalog、路由和验证流程。

Agent 系统越自动化，越不能把模型选择当成 UI 里的下拉框。它应该是一套能被调度器、failover 层和运维工具共同验证的 registry。
