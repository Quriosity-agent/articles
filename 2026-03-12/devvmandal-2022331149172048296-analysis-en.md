# What DevvMandal’s Tweet Signals: The Data Layer for Next-Gen Computer-Use Agents

> Original tweet: <https://x.com/DevvMandal/status/2022331149172048296>

DevvMandal announced the launch of an **open-source dataset of computer-use recordings** aimed at training the next generation of agents that can directly operate real software. The tweet highlights **300+ tasks** across different tools.

From the author’s follow-up replies in the same thread, we get two key links:

- Hugging Face dataset: <https://huggingface.co/datasets/markov-ai/computer-use>
- Product/site page: <https://www.markovstudios.com/>

This matters because it points to a practical shift: moving GUI agents from demo-centric hype to **data-centric engineering**.

## What was launched (tweet + thread context)

- Core claim in the tweet:
  - Open-source computer-use dataset
  - 300+ tasks (tweet wording)
  - Built for training computer-use agents
- Thread context:
  - A direct Hugging Face dataset link was posted in replies
  - A Markov landing page was also posted in replies
- Dataset card/README signals trajectory-style supervision with fields like:
  - actions
  - model responses
  - screenshots
  - accessibility trees
  - execution outputs/errors
  - recording paths (MP4)
  - multi-domain tasks (Chrome, VS Code, LibreOffice, GIMP, Thunderbird, VLC, etc.)

## Visuals

![Tweet video thumbnail showing the dataset launch](./assets/devvmandal-2022331149172048296/tweet-thumbnail.jpg)
*Figure 1: Native media thumbnail from the tweet announcing the launch.*

![Keyframe extracted from the tweet video](./assets/devvmandal-2022331149172048296/tweet-keyframe.jpg)
*Figure 2: Keyframe extracted from the attached video (~3s), showing desktop interaction context.*

## Why this is important technically

### 1) Data quality is still the main bottleneck for GUI agents
Most teams can produce a flashy click-demo. Far fewer can build robust agents that generalize across apps and workflows.

Common failure modes:
- narrow task distribution
- missing intermediate states
- weak grounding signals
- no post-action execution traces

A trajectory-rich dataset directly addresses these problems.

### 2) It combines perception, grounding, action, and feedback in one record
This is not just image-captioning or instruction-tuning data. The schema is useful for agent training loops:

- `screenshots` for visual observation
- `accessibility_trees` for structured UI grounding
- `actions` for executable behavior traces
- `exe_outputs/errors` for transition feedback

That unlocks practical workflows for:
- behavior cloning
- reward modeling / trajectory scoring
- recovery-policy training after failed actions

### 3) Open source enables reproducible iteration
With a public schema and trajectories, builders can:
- benchmark models on the same interaction traces
- contribute new domains/tools
- run ablations on grounding strategies (vision-only vs. vision+AX tree)

This is exactly the kind of infrastructure the ecosystem needs.

## Builder takeaways (practical)

1. **Lock your trajectory schema first.**
   Model upgrades are easy; inconsistent data contracts are expensive.

2. **Capture intermediate states, not just successful endpoints.**
   Agent reliability comes from decision traces, not final screenshots.

3. **Treat accessibility trees as first-class signals.**
   Pure visual control is fragile in complex desktop environments.

4. **Diversify domains before scaling sample count.**
   Heterogeneous tasks often improve generalization more than more of the same.

5. **Train on failure + recovery, not only perfect runs.**
   Real agents must self-correct in noisy environments.

## Bottom line

This release won’t instantly produce a universal desktop super-agent. But it does move the field in the right direction: **from prompt tricks to repeatable systems engineering**.

If you’re building in this space, the playbook is clear: start with high-success vertical tasks, then scale breadth using trajectory-native data pipelines like this.

---

🦞