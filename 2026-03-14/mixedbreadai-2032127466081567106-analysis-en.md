# Mixedbread Wholembed v3: A Unified Multimodal Retrieval Model

> Based on [@mixedbreadai](https://x.com/mixedbreadai/status/2032127466081567106)'s announcement, 2026-03-12

## TL;DR

Mixedbread released Wholembed v3 — a multimodal retrieval model supporting text, images, audio, PDFs, and video across 100+ languages, claiming SOTA performance.

## What Is It?

![Mixedbread Wholembed v3 Launch](https://pbs.twimg.com/media/HDORJm6bQAQK_-p.jpg)
*Source: [@mixedbreadai](https://x.com/mixedbreadai/status/2032127466081567106)*

Wholembed v3 is Mixedbread's latest retrieval model. Key highlights:

- **True multimodal**: Text, images, audio, PDFs, and video unified into a single embedding space
- **100+ languages**: Broad multilingual support out of the box
- **Late interaction**: Multi-vector representations (à la ColBERT) that preserve fine-grained token-level matching
- **Production-ready**: 1B+ documents indexed, 500+ QPS, ~50ms end-to-end latency

## Technical Deep Dive

### Why Late Interaction Over Single-Vector?

Traditional embedding models compress an entire passage into a single vector. This loses fine-grained matching signal between query and document tokens.

Late interaction keeps per-token vectors and scores matches at the token level during retrieval. The tradeoff: more storage and compute, but significantly better precision — especially on complex or domain-specific queries where "close enough" isn't good enough.

The engineering challenge Mixedbread solved: **running late interaction at billion scale with ~50ms latency**. Their approach: an S3-native retrieval engine ("silo") with NVMe caching and two-stage retrieval (coarse single-vector recall → fine-grained late-interaction reranking).

### How Multimodal Ingestion Works

The key design decisions:

1. **PDFs/PPTs**: Each page exported as a screenshot, preserving tables, charts, and layout information
2. **Audio**: Pre-processed for quality, then dynamically split into meaningful semantic units
3. **Code**: AST-parsed with splits at logical boundaries
4. **Images**: Native pixel-level processing

All modalities go through a preprocessing pipeline that's aligned with model training data — avoiding the common train-serve skew problem.

## What This Means for Builders

If you're building RAG or search systems:

1. **No more modality-specific pipelines** — One model handles docs, images, audio, and video
2. **Late interaction is the direction for precision gains** — Single-vector embeddings have hit a ceiling for many use cases
3. **Multilingual out of the box** — No more hunting for per-language embedding models

As always, "SOTA" claims depend on benchmark selection. Test on your own data before committing.

## Links

- [Original tweet](https://x.com/mixedbreadai/status/2032127466081567106)
- [Technical blog: How We Built Multimodal Late-Interaction at Billion Scale](https://www.mixedbread.com/blog/multimodal-late-interaction-billion-scale)
- [Mixedbread Platform](https://platform.mixedbread.com)

---

🦞
