---
title: "SeedRealtime Deep Dive: The Next Layer of Real-Time Voice Agents Is Audio-Visual Full Duplex"
date: 2026-08-05
source: "https://seed.bytedance.com/en/seedrealtime"
canonical: "https://seed.bytedance.com/en/blog/seedrealtime-audio-visual-full-duplex-llm-released-toward-omni-modal-natural-interaction"
product: "https://seed.bytedance.com/en/seedrealtime"
tags:
  - ByteDance Seed
  - SeedRealtime
  - Audio-Visual Full Duplex
  - Real-Time Voice Agent
  - Doubao
  - Multimodal Interaction
---

# SeedRealtime Deep Dive: The Next Layer of Real-Time Voice Agents Is Audio-Visual Full Duplex

> **TL;DR:** ByteDance Seed released SeedRealtime on August 5, 2026, positioning it as a native audio-visual full-duplex LLM. The important part is not simply faster voice response. SeedRealtime is designed to continuously receive audio, video, and temporal information, then watch, listen, and speak in the same live interaction loop. ByteDance says it has fully rolled out in the Doubao app, and that end-to-end human evaluation shows conversational pacing issues reduced by roughly half compared with cascaded systems. The larger signal is a product shift: real-time agents are moving from “wait for a turn, then answer” toward continuous perception, timing judgment, target selection, and safe action.

- **Source:** [SeedRealtime product page](https://seed.bytedance.com/en/seedrealtime)
- **Technical blog:** [SeedRealtime: An Audio-Visual Full-Duplex LLM Released, Toward Omni-Modal Natural Interaction](https://seed.bytedance.com/en/blog/seedrealtime-audio-visual-full-duplex-llm-released-toward-omni-modal-natural-interaction)
- **Published:** 2026-08-05
- **Topic:** audio-visual full duplex / real-time voice agent / multimodal interaction / Doubao
- **Cross-checks:** [LiveKit's Gemini Live integration docs](https://docs.livekit.io/agents/integrations/realtime/gemini/) (turn detection and frame-sampling defaults verified for this article); demo details, Seeduplex's earlier figures, and the three-way comparison also draw on [Xiaohu's write-up](https://best.xiaohu.ai/article/seed-realtime/)

![SeedRealtime official hero](imgs/bytedance-seedrealtime-full-duplex-audio-video/01-seedrealtime-hero.jpeg)

## One-line Takeaway

**SeedRealtime is not just “a voice model plus camera input.” It is an attempt to put audio, video, text, and interaction timing into one real-time runtime.**

That sounds like a product feature. Architecturally, it is a bigger turn.

Many voice assistants are still turn-based. A user speaks, speech is transcribed into text, an LLM generates an answer, and TTS plays it back. Even when each component is fast, the interaction still depends on the boundary of “are you done speaking?” Camera support is often added as another attachment path: capture an image, sample a video frame, convert it into a description, and send that description to the language model.

SeedRealtime targets a different problem: the real world is not a sequence of submit buttons. People pause, interrupt, look at objects, get interrupted by others, and express intent through half-sentences in noisy environments. A real-time agent needs to answer four questions continuously:

- Who is speaking now?
- Which object in the scene is the user referring to?
- Is this pause a thought, an ending, or noise?
- Should I speak now, keep listening, give a short acknowledgement, or call a tool?

That is why audio-visual full duplex matters more than simply reducing voice latency.

## Full Duplex Is Not Just Interruption Handling

The easiest way to describe full duplex is “the user can interrupt the AI.” That is only the visible surface.

The deeper change is that input and output are no longer mutually exclusive. The model has to keep listening while it speaks. It has to decide whether to speak while it listens. It has to keep updating objects, actions, positions, and user attention while watching the scene. The system is optimizing interaction rhythm, not only single-turn response time.

ByteDance’s positioning is explicit: SeedRealtime is a native audio-visual full-duplex LLM that jointly understands audio, visual, and temporal information, delivering a watch-listen-speak experience. The key words are “jointly” and “temporal.” If video is first converted into captions and audio is first converted into text, the model receives discrete artifacts. A full-duplex system has to operate on continuous streams.

That changes how voice agents should be evaluated. Traditional metrics include ASR accuracy, first-token latency, and TTS naturalness. Future real-time agents also need to be measured on:

- false interruption rate;
- stop speed after user interruption;
- false trigger rate in background noise;
- target-speaker selection in multi-person scenes;
- stability of visual reference resolution;
- timing of tool-call insertion;
- context and pacing across longer interactions.

In other words, a real-time agent is not only a talking model. It is a conversation scheduler.

## The Bottleneck in Cascaded Systems: Timing Gets Lost at Every Layer

ByteDance contrasts SeedRealtime with multi-stage cascaded systems. A typical pipeline looks like this:

```text
microphone / camera
  -> ASR / visual recognition / video understanding
  -> text or structured descriptions
  -> LLM reasoning
  -> TTS / spoken output
```

This architecture is practical and easy to compose from existing models. Its weakness is that every stage can compress away interaction signals.

Hesitation, stress, elongation, overlap, and background sounds lose detail after speech becomes plain text. Gaze, motion changes, object appearance, and gestures become less precise if video is reduced to captions. The language model receives processed summaries rather than the synchronized scene itself.

SeedRealtime’s official description points to an end-to-end unified audio-visual modeling framework, putting perception, understanding, decision-making, and response in one model to reduce information loss and error accumulation from multi-stage pipelines. Strategically, the model is not only generating content. It is also participating in the decision of when to answer, whom to answer, and how granular the answer should be.

That makes it closer to an interaction model than a simple speech recognition or video understanding model.

## The Real Dividing Line Is VAD, Not "Can It See the Camera"

Treating every "real-time AI that sees your camera" as one category misses what actually changed here. Before SeedRealtime there were three ways to let an assistant watch and talk, each stuck somewhere different:

| Approach | How it works | Where it breaks |
|---|---|---|
| Cascade | ASR → visual understanding → LLM → TTS, four stages in a relay | Latency stacks per stage; tone, pauses, and timing are gone at the transcription step |
| End-to-end audio only | One model takes audio in and emits audio out | Fast and fluid, but blind |
| End-to-end audio + bolted-on vision | Frames reach the model, but turn-taking is still decided by VAD | Video informs *what* to say, never *when* to say it |

The third is the one most easily mistaken for a solved problem. VAD (voice activity detection) is a separate, audio-only module with one job: decide whether someone is speaking right now, then infer from silence duration whether the user is finished. Guess early and you cut the user off; guess late and you leave dead air. It cannot see, so it cannot tell whether the user is addressing the camera or has turned to talk to someone standing next to them.

This dividing line isn't an outside reading — ByteDance draws it in the launch post itself: many end-to-end approaches still rely on an external VAD to decide turns and therefore remain, in substance, half-duplex question-and-answer; SeedRealtime instead decides turn-taking continuously from multimodal information rather than handing it to external VAD rules. **Removing the VAD is presented as the headline of the release, not as an implementation detail.**

This isn't hypothetical. Google's Gemini Live does support camera and screen sharing, and LiveKit's integration documentation states plainly that the Gemini Live API includes built-in VAD-based turn detection, enabled by default. The same document gives the default video sampling cadence: one frame per second while the user speaks, one frame every three seconds otherwise. (That sampling rate is a LiveKit framework default, adjustable via a `video_sampler` parameter, not a ceiling on Gemini. The VAD-based turn detection, however, is a property of the Gemini Live API itself.)

So the substantive change in SeedRealtime is precisely here: **turn-taking moves from an external rule to a decision the model makes continuously — and that decision can see.** The bolted-on VAD stops being necessary. "Full duplex is not just interruption handling," stated earlier, comes down architecturally to this one sentence.

## What the Official Demos Actually Show

ByteDance published seven demo clips of one to three minutes each alongside the release. Walking through them explains "video participates in the decision" better than any abstract description.

**Recognizing who's who, and who's speaking.** Four friends at dinner; the user introduces each person, the model binds names to people by appearance (light-haired, wearing glasses), then keeps track of who said what through overlapping conversation, finally producing a trip plan that reconciles constraints voiced by different people — one wants beach photos, one hates heat, one is allergic to seafood.

**Cross-language grounding in the scene.** At a Sichuan restaurant, the model reads dishes off a Chinese menu visually, recommends them in English, and explains the cultural background — why *yuxiang* pork has no fish in it, how century eggs are made. When a server remarks in passing that a dish goes well with rice, it interprets that against the food actually on the table and translates. Visual information never has to become a text description first.

**Holding a task until the trigger appears on screen.** At the Hebei Museum the user says once, "tell me when you see the gold-and-silver-inlaid tiger-and-deer screen stand," then wanders off; the model speaks up when the camera passes that exhibit. At an espresso machine, the user dumps whole beans into the portafilter and the model corrects it immediately, then after extraction suggests shortening the shot by 2–3 seconds based on the crema. Reading the ResNet paper, asked to flag the training-parameters section, it catches "3.4 Implementation" during fast scrolling and interrupts. Three clips, one mechanism: the task lives in context and the trigger is visual.

**Not getting derailed.** At Daxing Airport a companion mentions a flight in passing and the model does not respond; when the user asks directly — by which point the flight board has left the frame — it answers from what it saw earlier. In the children's English clip, someone is on the phone in the background and the model stays with the child's pointing finger.

These are four faces of the same change: because video participates in the "should I speak" decision, proactive reminders, noise robustness, and reference resolution all become possible at once.

The official material also names two hard problems. Video offers no natural pauses to exploit — speech has silence as a boundary, but a video stream is always on and continuously changing, so judgment has to be continuous over a stream with no segmentation points. And reference resolution: when the user says "how does this work," the model has to bind "this" against the current frame, the user's gesture, their gaze, and their actions from the last few seconds, using the scene to disambiguate homophones as well.

## Three Capabilities: Understand, Initiate, Wait

ByteDance frames SeedRealtime’s progress in three areas: audio-visual joint understanding, proactive interaction, and conversational timing.

The first is audio-visual joint understanding. The model needs to connect voice, scene, and time. In overlapping multi-speaker conversation, it has to infer who is speaking, whom the user may be asking about, and which visual object is currently relevant. Requests like “what is this?”, “was that person right?”, or “translate what she just said” are fragile if the system only has text transcripts.

![SeedRealtime multi-speaker audio-visual understanding demo](imgs/bytedance-seedrealtime-full-duplex-audio-video/02-multispeaker-audio-visual.webp)

The same capability also extends into cross-language and scene explanation. When a user points the camera at a menu, exhibit, device, or sign, the model is not only translating text. It is explaining context based on what is visible and what the user is asking right now.

![SeedRealtime context-aware cross-language demo](imgs/bytedance-seedrealtime-full-duplex-audio-video/03-context-aware-cross-language.webp)

The second is proactive interaction. Traditional assistants behave like passive Q&A machines. SeedRealtime emphasizes persistent environmental awareness and proactive communication: recognizing what a user is looking at in a museum, offering next-step guidance in device operation, or helping with reading and study tasks based on visual context.

![SeedRealtime proactive museum interaction demo](imgs/bytedance-seedrealtime-full-duplex-audio-video/04-proactive-museum.webp)

The third is conversational timing. This sounds less glamorous than model size or benchmark scores, but it is central to voice experience. In human conversation, silence does not always mean the turn has ended. Background audio does not always mean the user is talking to the AI. Speech from another person is not always an instruction. ByteDance says SeedRealtime can perceive conversation state and rhythm, reducing false triggers and poorly timed interruptions in noisy stations, airports, and multi-speaker home environments.

![SeedRealtime noisy conversation timing demo](imgs/bytedance-seedrealtime-full-duplex-audio-video/05-noisy-conversation.webp)

Together, these capabilities point to something beyond “smarter chat.” SeedRealtime is trying to behave more like an assistant that is present in the scene. It needs to know whether it should step in at all.

## The Doubao Rollout Is the Real Product Signal

The product page says SeedRealtime has been fully rolled out in the Doubao app, and describes it as a scaled deployment of audio-video full-duplex technology. That matters more than a demo alone.

The hard part of real-time audio-video models is not only model capability. It is deployment cost and product safety. The system has to handle continuous streaming input, low-latency output, mobile network variability, camera and microphone permissions, accidental triggers, multi-person scenes, youth safety, privacy notices, and tool-use boundaries. Once it enters a consumer app, it faces messier conditions than a lab demo.

This is why full-duplex modeling is not solved by pushing latency lower. The cost comes from long-lived connections and continuous perception:

- how audio-video streams are chunked into the model;
- how output is generated as a stream;
- how inference is quantized and optimized;
- what runs on device versus in the cloud;
- how to reduce discomfort around persistent camera and microphone input;
- how proactive reminders and tool calls avoid overstepping.

ByteDance mentions chunked audio-visual input, streaming generation output, quantization, and inference optimization. It does not publish the full system design, but those terms show the problem has moved into real-time inference engineering, not ordinary offline multimodal QA.

## Placing It on the Timeline: Four Steps in ByteDance's Line

The release makes more sense positioned against ByteDance's own path:

| Date | Milestone | What changed |
|---|---|---|
| Before | Doubao Realtime Voice | Half duplex: the model waits for you to finish |
| 2026-04-09 | Seeduplex | Audio-only full duplex, rolled out to all Doubao App users |
| 2026-06-18 | Volcano Engine API (Doubao Realtime Voice 3.0) | From first-party app to developer access |
| 2026-08-05 | SeedRealtime | Video enters the decision; when to speak is decided with sight for the first time |

There's an actionable inference in that path: **the previous generation shipped in the app on April 9 and only reached an API on June 18, about ten weeks later.** SeedRealtime currently has one announced entry point — update the Doubao App, tap the call button in the chat box to enter video calling, free, no waitlist — with no API or developer access announced. If the same cadence holds, developer access would likely be roughly a quarter out. That's an inference from the prior release, not a company commitment.

For context, here is where the other two stand publicly:

| Offering | Can it see? | Who decides when to speak | Availability |
|---|---|---|---|
| SeedRealtime (ByteDance) | Yes, video streams into the model | The model itself, watching and listening continuously | Doubao App, all users, free |
| GPT-Live (OpenAI) | Not yet in ChatGPT for camera or screen share; officially "later" | The model itself (full duplex), but it only hears | Shipped |
| Gemini Live (Google) | Yes, camera and screen sharing | Built-in VAD, enabled by default | Shipped |

The Gemini Live row is sourced from LiveKit's integration documentation, verified for this article; GPT-Live's camera status comes from OpenAI's public statements. Checked against those two, ByteDance's claim of being first to deploy audio-visual full duplex at scale holds within this comparison set: **the one that can see delegates turn-taking to VAD, and the one with the most complete full duplex cannot see yet.** The check has a boundary — only OpenAI and Google's public status were verified; other Chinese vendors were not individually checked.

## How It Relates to Seed2.1 and Seedream

Placed beside ByteDance Seed’s recent model releases, SeedRealtime is not a repeat of Seed2.1 or Seedream.

Seed2.1 is closer to general productivity, reasoning, coding, and stable agent execution. Seedream 5.0 Pro focuses on image generation and design production. SeedRealtime sits in a different layer: the real-time interaction runtime between users and models.

One way to separate them:

| Direction | Focus | Core question |
|---|---|---|
| Seed2.1 | text, reasoning, coding, agent tasks | Can the model complete complex work reliably? |
| Seedream | image generation, design, visual production | Can the model produce visual assets reliably? |
| SeedRealtime | audio-visual full-duplex interaction | Can the model intervene naturally in real scenes? |

So SeedRealtime’s competitors are not only voice assistants. It is closer to the front control layer of future real-time agents: listen, watch, wait, speak, interrupt, confirm, remind, and call tools.

## Read the Evaluation Claims Carefully

ByteDance says end-to-end human evaluation shows SeedRealtime reduces conversational pacing issues by half compared with cascaded systems, while also reducing interruption, latency, false triggers, and improving single-turn usability.

That direction is important, but it should still be read as an official launch claim. The page does not publish the full evaluation set, sample size, scoring rubric, baseline configuration, or confidence intervals. The safer interpretation is: ByteDance reports that its end-to-end full-duplex architecture is materially better than cascaded systems in experience evaluation, while external reproducible testing is still needed to map the boundary.

One comparison sharpens this: **the same team disclosed considerably more four months ago.** When the audio-only Seeduplex shipped on 2026-04-09, the numbers were specific — false-response and false-interruption rates halved, barge-in rate down 40% relative, endpointing up 8%, and an 8.34 percentage-point absolute gain in call satisfaction in large-scale A/B testing. SeedRealtime offers one number, pacing issues halved, plus an unquantified claim that the probability of a complete, smooth single conversation improved noticeably.

Also absent are the metrics that matter most in real-time interaction: end-to-end latency in milliseconds, model size, any public benchmark, and third-party reproduction. The official outlook says future work will keep compressing the hear-understand-respond latency, which concedes there is room to compress without stating today's baseline.

Audio-visual is genuinely harder than audio-only, so coarser disclosure is understandable. But for teams making a technology decision it means **there is currently no public number usable for cross-vendor comparison** — subjective testing in the Doubao App is the only option.

Real-time audio-video agents are difficult to summarize with one number. A useful evaluation stack should separate:

- perception: how often it mishears, missees, or misresolves references;
- timing: interruption, dead air, false stops, and false triggers;
- task execution: tool-call success and recovery;
- safety: privacy notices, sensitive-scene handling, permission control;
- cost: latency, bandwidth, compute, and battery;
- subjective experience: whether users feel the system is natural, controllable, and non-intrusive.

That evaluation infrastructure will become part of the real-time agent stack itself.

## The Official Roadmap Points at an Agent Front End

The launch post closes with four directions, and they say more about where this line is heading than the model description does:

1. **Lower latency and more natural timing** — keep compressing end-to-end hear-understand-respond latency, with the goal of reproducing the micro-rhythms of real conversation (interrupting, jumping in, backchanneling, pausing), not merely being faster.
2. **More proactive perception and decision-making** — move from speaking when appropriate to *acting* when appropriate, judging on its own when to remind and when to add information.
3. **Robustness in complex multi-person scenes** — reliably determine who is speaking, what they are looking at, and who to answer, in noisy rooms with several people in frame.
4. **From "able to converse" to "able to act"** — connect tool calls to the real world so the model can complete lookups, bookings, and tasks.

The fourth deserves its own marker. Tool calling isn't a distant roadmap item: the capability section already states the model can weave tool calls into its responses, and the airport demo has it going online for a baggage-carousel location. In other words, **the destination of this line isn't a better voice assistant but an agent front end that watches a live scene and decides when to act** — the real-time interaction layer is its I/O surface.

The airport clip carries one more easily-missed detail. ByteDance's framing is that a noisy environment is no longer only interference to filter out: key information from bystander chatter is retained and drawn on when needed. That is a stricter requirement than noise robustness — the model has to decide a line shouldn't trigger a reply while still committing it to memory.

## What It Means for Product Teams

If you are building real-time voice, companionship, education, guided tours, customer support, hardware assistants, or desktop agents, SeedRealtime’s direction is clear: do not treat voice as only an input method.

The product questions become:

- What context does the screen or physical environment provide while the user is speaking?
- When should the AI proactively speak, and when should it stay silent?
- How does the system confirm that it was addressed in a multi-person environment?
- Can it stop immediately and reroute after user interruption?
- Do proactive reminders require explicit permission?
- Does tool use require a second confirmation?
- What are the storage, training, and deletion policies for continuous camera and microphone input?

Many teams will begin with “low-latency voice.” Eventually, they will discover that latency is not the only bottleneck. The harder problem is interaction policy: how AI can be useful in a continuously changing scene without over-participating.

## Conclusion

SeedRealtime shows that real-time agent competition is shifting from faster answers to more natural presence.

Audio-visual full duplex means the model no longer slices the world into one utterance, one image, and one request. It continuously understands sound, scene, timing, and social rhythm. It has to decide who is speaking, what they are looking at, when to respond, when to wait, and when it can safely call tools.

This path is still early. Evaluation, privacy, cost, permissions, and false triggers will all be hard problems. But the direction is clear: the next generation of voice agents will not be only a spoken version of chat. They will become the real-time interaction layer that connects physical scenes, screen context, and action.
