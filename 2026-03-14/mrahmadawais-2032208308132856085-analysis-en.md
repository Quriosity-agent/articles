# Chartli: Zero-Config Data Visualization in Your Terminal

> Based on [Ahmad Awais (@MrAhmadAwais)](https://x.com/mrahmadawais/status/2032208308132856085)'s tweet

![chartli terminal chart examples](https://pbs.twimg.com/media/HDPXLWLbQAE5PXC.jpg)
*Image credit: Ahmad Awais on Twitter*

## What Is It

Ahmad Awais just shipped **chartli v1.0** — a CLI that turns plain numbers into terminal charts. Pipe numbers in, get a chart out.

```bash
# Run instantly
npx chartli

# Or install globally
npm i -g chartli
```

No browser. No matplotlib. No config files. Just numbers → charts.

## Chart Types

Eight rendering modes spanning the full range of Unicode density:

- **ascii** — Line charts with ○◇◆● markers
- **spark** — ▁▂▃▄▅▆▇█ sparklines, one row per series
- **bars** — Horizontal bars, ░▒▓█ shading per series
- **columns** — Vertical grouped bars
- **heatmap** — 2D grid with ░▒▓█ intensity mapping
- **unicode** — ▁▂▃▄▅▆▇█ sub-cell resolution bars
- **braille** — ⠁⠂⠃ 2×4 dot matrix, highest density
- **svg** — Vector output, circles or polylines

## Why It Matters

### 1. Unix Philosophy Done Right

Input format is dead simple: rows of space-separated numbers. Multiple columns = multiple series. Composes with pipes:

```bash
cat metrics.txt | chartli -t spark
```

One job. Does it well. Plays nice with everything else.

### 2. The Braille Renderer Is the Star

Each braille character encodes a 2×4 dot grid. A 16-character-wide chart gives you 32 pixels of horizontal resolution. Free anti-aliasing courtesy of Unicode.

### 3. v1.0 Adds Labels & Annotations

```bash
npx chartli data.txt -t ascii -w 28 -h 8 \
  --x-axis-label "day" \
  --y-axis-label "signups" \
  --data-labels \
  --first-column-x
```

Axis labels, data labels, custom ticks, series names — terminal charts that finally explain themselves.

### 4. Zero Config, Full Override

Works out of the box. Need customization? `-w` width, `-h` height, `-m` SVG mode. No config files. No themes. No dashboards.

## Practical Use Cases

- **CI/CD pipelines** — Visualize performance trends right after builds
- **Server monitoring** — SSH in, see charts, no browser needed
- **Quick data exploration** — Dump CSV numbers in, instant visualization
- **Agent toolchains** — AI agents can invoke this directly in terminal environments

## Builder's Perspective

Awais built this with "Command Code" using his "CLI taste" — honed from open-sourcing hundreds of CLIs. The design principles are clear:

1. **Instant start** — One `npx` command, zero setup
2. **Minimal input format** — Plain numbers, space-separated
3. **Composable output** — Pipe-friendly, SVG exportable
4. **Zero cognitive overhead** — No config language to learn

This is another good example of agent-first CLI design: tools should be simple enough that an AI agent can invoke them directly without ceremony.

## Links

- Original tweet: [Ahmad Awais on X](https://x.com/mrahmadawais/status/2032208308132856085)
- Install: `npx chartli` or `npm i -g chartli`

---

🦞
