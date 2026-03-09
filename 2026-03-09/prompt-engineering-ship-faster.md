# Prompt 工程实战：让 AI Coding Agent 10 倍提速的写法

> **TL;DR**: Prompt 工程不是魔法咒语，是**清晰度、结构和意图**的表达。基于 @nothiingf4 的推文和实际开发经验，整理出真正有效的 prompt 写法。核心原则：你给 AI 的上下文质量决定了输出质量。

---

## 核心原则

Prompt 工程不是 trick，是三件事：

- **Clarity（清晰）** — AI 不会读心，你说什么它做什么
- **Structure（结构）** — 有组织的输入产生有组织的输出
- **Intention（意图）** — 明确你要什么，不要让 AI 猜

---

## 策略 1：先给角色，再给任务

```
❌ "帮我写个函数"
✅ "你是一个 TypeScript 后端工程师。写一个函数，接收 userId，从 PostgreSQL 查询用户的最近 10 条订单，返回 Order[] 类型。使用 Drizzle ORM。"
```

**为什么有效：** 角色设定缩小了 AI 的搜索空间。说"TypeScript 后端工程师"，它就不会给你 Python 方案。

---

## 策略 2：给约束而不是给自由

```
❌ "写个好的 API"
✅ "写一个 REST API endpoint：
- POST /api/orders
- 输入：{ userId: string, items: { productId: string, qty: number }[] }
- 验证：userId 非空，items 至少 1 个，qty > 0
- 成功返回 201 + orderId
- 失败返回 400 + error message
- 用 Zod 做 schema validation"
```

**约束 = 质量。** 越具体的 prompt，越不需要来回修改。

---

## 策略 3：给例子（Few-shot）

```
"把这些 Git commit message 改成 conventional commits 格式：

输入：'fixed the login bug'
输出：'fix(auth): resolve login redirect loop'

输入：'added dark mode'
输出：'feat(ui): add dark mode toggle with system preference detection'

现在处理这些：
- 'updated deps'
- 'refactored user service'
- 'removed old code'"
```

**一个好例子胜过十句描述。**

---

## 策略 4：分步骤而不是一次全给

```
❌ "帮我建一个全栈电商网站，有用户系统、商品管理、购物车、支付、订单追踪"

✅ 分步：
1. "先设计数据库 schema：用户、商品、订单三个表，用 PostgreSQL + Drizzle"
2. "基于这个 schema，写 CRUD API routes"
3. "写前端商品列表页，用 React + TanStack Query"
4. "加上购物车逻辑，用 Zustand 状态管理"
```

**小步快跑 > 一步登天。** AI 在小范围内的准确率远高于大范围。

---

## 策略 5：告诉 AI 不要做什么

```
"重构这个函数。要求：
- 不要改变函数签名
- 不要添加新的依赖
- 不要修改测试
- 只优化内部实现"
```

**负面约束跟正面要求一样重要。** 很多 prompt 失败是因为 AI 做了你不想要的事。

---

## 策略 6：用文件/代码作为上下文

```
"看这个文件的代码风格（使用 early return、snake_case、no-else-after-return），
然后用同样的风格写一个新函数：processPayment(order: Order): Promise<Receipt>"
```

**让 AI 从现有代码学风格，比描述风格有效 10 倍。**

---

## 策略 7：要求结构化输出

```
"分析这段代码的问题，用这个格式输出：

## 问题
1. [严重程度: HIGH/MEDIUM/LOW] 问题描述
   - 位置：文件名:行号
   - 修复建议：具体修改

## 总结
- 高优先级：X 个
- 中优先级：X 个"
```

**模板化输出 = 可预测的质量。**

---

## 策略 8：迭代而不是重写

```
第一轮："写一个日志中间件"
→ AI 输出 v1

第二轮："给这个中间件加上：请求耗时统计、错误自动捕获、correlation ID"
→ AI 在 v1 基础上改进

第三轮："优化性能：避免序列化大 body，加 content-length 限制"
→ AI 在 v2 基础上优化
```

**跟 AI 对话就像 code review — 渐进式改进。**

---

## 对 AI Coding Agent 的特别建议

用 Claude Code / Codex / Cursor 这类 agent 时：

- **先让它读代码再改代码** — "先读 src/auth/ 目录下所有文件，理解认证流程，然后再改 login 逻辑"
- **给它 checklist** — "完成后检查：1) 类型安全 2) 错误处理 3) 测试覆盖 4) 无 console.log"
- **用 SKILL.md 固化常用 prompt** — 把团队规范写成 skill，每次自动加载
- **限制作用域** — "只修改 src/components/Header.tsx，不要动其他文件"

---

## 反模式

- ❌ "帮我写最好的代码" — "最好"没有定义
- ❌ 一个 prompt 塞 10 个需求 — 拆开
- ❌ 不给上下文直接要输出 — 垃圾进垃圾出
- ❌ 改完不 review 就用 — AI 会犯错，每次都 review
- ❌ 用 prompt trick 而不是清晰表达 — trick 脆弱，清晰度稳定

---

## 参考

- 原始推文: <https://x.com/nothiingf4/status/2030682331670056964>
- Prompt Engineering Guide: <https://www.promptingguide.ai/>

---

*写于 2026-03-09 by 🦞*
