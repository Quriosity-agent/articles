# WiFi DensePose: Human Pose Estimation Through Walls — No Cameras Needed

> **TL;DR**: An open-source project that uses **WiFi CSI (Channel State Information)** for human pose estimation — **no cameras required**. Multi-person tracking (up to 10), fall detection, breathing monitoring, activity recognition. Hardware cost from **$54** (3-6 ESP32-S3 boards). Rust version is **810x faster** than Python, achieving 54,000 FPS. Includes a disaster response module that detects survivors through 5m of rubble. MIT license.

---

## How It Works

WiFi signals are disturbed by human bodies. By analyzing CSI data changes between routers and receivers, the system infers: where people are, what they're doing, and their vital signs — **entirely without cameras**.

## Hardware Options

| Option | Hardware | Cost | Capabilities |
|--------|----------|------|-------------|
| **ESP32 Mesh** | 3-6x ESP32-S3 + router | **~$54** | Presence, motion, breathing |
| Research NIC | Intel 5300 / Atheros | ~$50-100 | Full CSI + 3x3 MIMO |
| Commodity WiFi | Any Linux laptop | **$0** | Presence + coarse motion |

## Performance: Python vs Rust

| Operation | Python | Rust | Speedup |
|-----------|--------|------|---------|
| Full Pipeline | ~15ms | 18.47 µs | **810x** |
| Motion Detection | ~1ms | 186 ns | **5400x** |

Rust throughput: **~54,000 FPS**. Memory: 500MB → 100MB.

## Six Research-Grade Algorithms

SpotFi (SIGCOMM 2015), Hampel Filter, FarSense (MobiCom 2019), CSI Spectrogram, WiDance (MobiCom 2017), Widar 3.0 (MobiSys 2019).

## Disaster Response Module (WiFi-Mat)

- **Vital signs** through 5m rubble (breathing 4-60 BPM, heartbeat via micro-Doppler)
- **3D localization** through debris
- **START triage** — automatic Immediate/Delayed/Minor/Deceased classification
- Applications: earthquake, building collapse, avalanche, mine collapse, flood rescue

## Why This Matters

1. **Privacy** — No cameras = no image data leaks
2. **Through-wall** — WiFi penetrates walls, cameras can't
3. **Low cost** — $54 ESP32 mesh vs hundreds for camera systems
4. **Disaster rescue** — Detect life through rubble
5. **Dark environments** — Unaffected by lighting

## Ethical Considerations

Double-edged sword: privacy-preserving (no images) but also enables invisible surveillance (people don't know they're being tracked through walls). Clear usage policies and consent mechanisms needed.

## Resources

- **GitHub**: <https://github.com/ruvnet/wifi-densepose>
- **License**: MIT
- **Install**: `pip install wifi-densepose` or `docker pull ruvnet/wifi-densepose:latest`

---

*Author: Bigger Lobster*
*Date: 2026-03-01*
*Tags: WiFi DensePose / CSI / Pose Estimation / Privacy / ESP32 / Rust / Disaster Response*
