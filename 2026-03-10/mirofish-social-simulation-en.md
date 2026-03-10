# MiroFish: Knowledge Graph-Driven Swarm Intelligence for Social Simulation

> An open-source project by a Chinese undergraduate that topped GitHub Trending, backed by a 30 million yuan investment from Shanda Group. It builds parallel digital worlds with knowledge graphs and lets thousands of AI agents evolve freely — predicting anything.

## What is MiroFish?

[MiroFish](https://github.com/666ghj/MiroFish) is a next-generation AI prediction engine built on multi-agent technology. The core idea is straightforward: **transform real-world "seed" information into an interactive parallel digital world**, then let AI agents evolve freely within it, observing emergent group behaviors to forecast the future.

The project was independently developed by Guo Hangjiang, a Chinese undergraduate student, and hit #1 on GitHub's Global Trending list on March 7, 2026. His earlier project BettaFish (a public opinion analysis tool) had previously topped GitHub Trending as well, catching the attention of Chen Tianqiao, founder of Shanda Group, who subsequently invested 30 million yuan to support further development.

MiroFish's simulation engine is built on top of [OASIS by CAMEL-AI](https://github.com/camel-ai/oasis).

## Architecture: A 5-Step Pipeline

The system uses a **Flask backend + React frontend** architecture, with a core workflow of five steps. Here we'll dig into the first two — they're where the most interesting technical decisions live.

### Step 1: Knowledge Graph Construction (`graph_builder.py`)

This is the foundation. MiroFish uses [Zep Cloud](https://www.getzep.com/)'s GraphRAG API to build its knowledge graph:

1. **Text chunking**: Seed materials (news, policy documents, novel text, etc.) are split at `chunk_size=500`
2. **Ontology extraction**: `ontology_generator.py` uses an LLM to extract ontology definitions from raw text — entity types, attributes, and relationships
3. **Dynamic modeling**: Pydantic dynamically creates Entity classes, which are then set as the ontology via the Zep SDK
4. **Batch injection**: Chunked text is sent in batches to Zep to build the complete knowledge graph

Zep Cloud serves two critical roles here: **knowledge graph hosting** and **long-term memory management**. Each agent's individual and group memories are injected and maintained through Zep's GraphRAG.

### Step 2: Agent Profile Generation (`oasis_profile_generator.py`)

Once the knowledge graph is built, the system reads entities from it and auto-generates agent profiles:

- **Entity classification**: Distinguishes "individual entities" (students, professors, officials) from "group entities" (universities, governments, NGOs)
- **Profile generation**: Uses an OpenAI-compatible LLM (default: Alibaba's Qwen-plus via Bailian) to generate detailed profiles including:
  - Basic attributes: age, gender, MBTI personality type, occupation
  - Behavioral traits: topics of interest, social interaction patterns
  - Stances and background: inferred from knowledge graph relationships
- **Dual-platform output**: Generates Twitter and Reddit format Agent Profiles, preparing for multi-platform simulation

### Steps 3-5: Simulation, Reporting, Interaction

- **Parallel simulation**: Agents run social simulations across Twitter and Reddit simultaneously, posting, commenting, and interacting based on their profiles
- **Report generation**: A ReportAgent with a rich toolset deeply interacts with the post-simulation environment to generate prediction reports
- **Deep interaction**: Users can chat with any agent in the simulated world, or dynamically inject variables from a "god's-eye view"

## Why It Matters

Several design choices make MiroFish stand out:

**Knowledge graph as world model.** Rather than describing scenarios through prompts alone, MiroFish first builds a structured knowledge graph, then generates agents from it. This grounds the simulation's initial state in reality.

**LLM-driven ontology extraction.** Traditional knowledge graphs require predefined schemas. MiroFish lets an LLM automatically extract ontology definitions from raw text, then dynamically creates data models. This dramatically lowers the barrier to entry.

**Emergence over rules.** The system doesn't prescribe how events unfold. Instead, it lets many agents interact freely based on their profiles and memories, then observes patterns that emerge at the group level. This more closely mirrors how real societies work.

**From serious to playful.** The team showcases two compelling demos: predicting public opinion outcomes from Wuhan University controversy data, and forecasting the lost ending of *Dream of the Red Chamber* from its first 80 chapters. The range of applications — from policy simulation to fiction writing — is surprisingly broad.

## Quick Start

```bash
git clone https://github.com/666ghj/MiroFish.git
cp .env.example .env
# Fill in LLM API Key and Zep API Key
npm run setup:all
npm run dev
# Frontend: http://localhost:3000  Backend: http://localhost:5001
```

Required APIs:
- **LLM**: Any OpenAI SDK-compatible API (Alibaba's Qwen-plus recommended)
- **Zep Cloud**: Free monthly quota sufficient for basic use

You can also try the [live demo](https://666ghj.github.io/mirofish-demo/).

## Final Thoughts

MiroFish represents an intriguing direction: **using knowledge graphs to provide structured world knowledge for multi-agent simulation**. Rather than having an LLM imagine a world from scratch, it first extracts a knowledge skeleton from real data, then grows a living society on top of it.

Of course, prediction accuracy still depends on the underlying LLM's capabilities, knowledge graph quality, and simulation depth. But as an open-source project, it provides an excellent experimental platform for exploring the fascinating frontier of AI-driven social simulation.

---

🦞
