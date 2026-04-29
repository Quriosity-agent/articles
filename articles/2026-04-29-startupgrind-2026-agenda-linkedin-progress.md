# Startup Grind 2026 议程全量整理完成：分组结构与 LinkedIn 补全计划

## 背景
基于源文件《startupgrind-agenda-linkedin-full.md》，本次已完成 Startup Grind 2026 Conference（Day 1 + Day 2）的议程全量整理，并统一输出为可追踪的数据化清单。

本轮整理目标有三点：
1. 完成全量议程覆盖；
2. 以 `stage/day` 为主轴重组信息；
3. 明确 LinkedIn 字段现状与后续补全路径。

## 本次交付结果

### 1) 全量覆盖已完成
当前数据覆盖三大舞台（Mainstage / Breakout Stage / Divot Stage），包含两天完整议程（Day 1 + Day 2），并按「场次 + 演讲者槽位」展开。

- 覆盖场次：70 sessions
- 演讲者槽位：150 speaker-slot rows
- 去重后演讲者：121 unique speakers
- 不含：VC Pitch Stage（按原始要求排除）

这意味着，后续无论做内容分发、嘉宾触达，还是活动复盘分析，都可以直接在这份结构化底稿上继续推进。

### 2) 分组方式已稳定：按 Stage / Day 组织
整理后的主结构为：
- Day 1
  - Mainstage
  - Breakout Stage
  - Divot Stage
- Day 2
  - Mainstage
  - Breakout Stage
  - Divot Stage

每条记录已包含：
- 时间（Time）
- 议题标题（Session Title）
- 讲者姓名（Speaker）
- 公司/机构（Organization）
- LinkedIn 字段（当前状态）

该分组方式的优势是：
- 人工阅读时路径清晰；
- 后续导入表格/数据库时字段映射明确；
- 便于按舞台、日期、讲者批量筛选与补全。

## LinkedIn 字段现状

### 当前状态
目前 150 条演讲者槽位的 LinkedIn URL 均标记为「待确认」。

原因是：现有 Brella schedule API payload 未直接提供 speaker 的 LinkedIn 字段，因此不能从当前数据源一跳获取完整链接。

### 风险与影响
- 对议程完整性影响较小（时间/议题/讲者已完整）；
- 对后续外联、画像、社媒投放会形成信息缺口；
- 若不做去重策略，后续补全会出现重复劳动（同一讲者在多个 session 重复出现）。

## 后续补全计划（建议执行顺序）

### Phase 1：建立讲者主表（去重层）
先以 121 位 unique speakers 建立主表（Speaker Master），字段建议：
- Speaker Name（规范化）
- Organization
- LinkedIn URL
- LinkedIn Confidence（High/Medium/Low）
- Source（官网/公司页/新闻稿/人工确认）
- Last Verified At

> 先在去重层补齐，再回填 150 条 speaker-slot，可显著降低工作量。

### Phase 2：半自动检索与候选生成
针对每位讲者生成候选链接（1~3 个），优先组合检索：
- `姓名 + 公司 + LinkedIn`
- `姓名 + Startup Grind`
- 公司官网团队页反查

并记录候选证据，避免“同名误配”。

### Phase 3：人工校验与回填
人工确认后，将主表 LinkedIn URL 回填到所有对应 speaker-slot 行，形成一致数据视图。

### Phase 4：增量维护机制
为后续版本增加规则：
- 新增讲者先入主表；
- 无法确认时维持「待确认」并打上原因标签；
- 定期复核低置信度链接。

## 结论
本轮工作已经完成「议程全量整理」这一关键里程碑，且分组结构（Stage / Day）已可直接支撑后续运营与分析。

下一阶段的核心不再是“补议程”，而是“补身份链接”：把 LinkedIn 从“全待确认”推进到“高置信可用”。建议从讲者去重主表入手，按批次完成回填，确保效率与准确度同时达标。
