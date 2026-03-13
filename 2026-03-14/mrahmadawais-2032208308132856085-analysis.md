# Chartli：终端里的数据可视化，零配置出图

> 基于 [Ahmad Awais (@MrAhmadAwais)](https://x.com/mrahmadawais/status/2032208308132856085) 的推文分析

![chartli 终端图表示例](https://pbs.twimg.com/media/HDPXLWLbQAE5PXC.jpg)
*图片来源：Ahmad Awais Twitter*

## 这是什么

Ahmad Awais 发布了 **chartli v1.0**——一个终端里的图表 CLI 工具。输入数字，输出图表，就这么简单。

```bash
# 即装即用
npx chartli

# 或者全局安装
npm i -g chartli
```

不需要浏览器，不需要 matplotlib，不需要任何配置文件。管道输入数字，直接出图。

## 支持的图表类型

chartli 支持 8 种渲染模式，覆盖从简单到高密度的各种场景：

| 类型 | 特点 |
|------|------|
| **ascii** | 经典折线图，○◇◆● 标记 |
| **spark** | ▁▂▃▄▅▆▇█ 火花线，一行一个系列 |
| **bars** | 水平条形图，░▒▓█ 分层阴影 |
| **columns** | 垂直分组柱状图 |
| **heatmap** | 2D 网格，░▒▓█ 强度映射 |
| **unicode** | ▁▂▃▄▅▆▇█ 亚像素分辨率 |
| **braille** | ⠁⠂⠃ 2×4 点阵，最高密度 |
| **svg** | 矢量输出，圆点或折线 |

## 为什么值得关注

### 1. Unix 哲学的完美体现

输入格式极简：空格分隔的数字行，多列 = 多系列。完美兼容管道：

```bash
cat metrics.txt | chartli -t spark
```

这就是 Unix 工具该有的样子——做一件事，做好它，然后和其他工具组合。

### 2. braille 渲染器是亮点

每个 braille 字符编码一个 2×4 的点阵网格。16 字宽的图表就有 32 像素的水平分辨率。Unicode 免费给你的"抗锯齿"。

### 3. v1.0 新增标签系统

```bash
npx chartli data.txt -t ascii -w 28 -h 8 \
  --x-axis-label "day" \
  --y-axis-label "signups" \
  --data-labels \
  --first-column-x
```

坐标轴标签、数据标签、自定义刻度——终端图表终于可以自解释了。

### 4. 零配置但可完全覆盖

默认就能用。需要定制？`-w` 宽度、`-h` 高度、`-m` SVG 模式。没有配置文件，没有主题，没有仪表板。

## 实际使用场景

- **CI/CD 管道**：构建后在终端直接看性能趋势
- **服务器监控**：`ssh` 进去就能看图，不用开浏览器
- **快速数据探索**：CSV 转数字丢进去，秒出图
- **Agent 工具链**：AI Agent 可以直接在终端环境中可视化数据

## Builder 视角

Ahmad Awais 提到这是用 "Command Code" 配合他的 "CLI taste" 构建的。作为一个开源了数百个 CLI 的开发者，这个工具体现了他对终端工具的理解：

1. **即装即用** — `npx` 一行搞定
2. **输入格式极简** — 纯数字，空格分隔
3. **输出可组合** — 管道友好，SVG 可导出
4. **零依赖心智负担** — 不需要学新的配置语言

这正是 Agent-first CLI 设计理念的又一个好例子：工具应该简单到 AI Agent 都能直接调用。

## 链接

- 推文原文：[Ahmad Awais on X](https://x.com/mrahmadawais/status/2032208308132856085)
- 安装：`npx chartli` 或 `npm i -g chartli`

---

🦞
