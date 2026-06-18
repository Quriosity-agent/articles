# Voice-agent / speech-model benchmark source notes

Use this reference when writing articles from X/Twitter posts announcing TTS, STT, or real-time voice-agent model releases, especially when screenshots cite Artificial Analysis or similar leaderboards.

## Source triangulation pattern

1. Treat the X post as social framing, not the canonical technical source.
2. Preserve meaningful tweet media locally, especially leaderboard screenshots and embedded video thumbnails/frames.
3. Resolve and cite canonical product/docs pages:
   - product landing page for positioning and deployment claims;
   - model docs for supported languages, latency claims, endpoint semantics, API events, and model IDs;
   - benchmark/methodology pages for independent numbers.
4. For Artificial Analysis speech benchmarks, prefer the dedicated article/model/leaderboard pages over screenshots when available.
5. Compare screenshot claims against the current live leaderboard; these boards move. If live rankings differ from the screenshot, write that explicitly instead of presenting the screenshot's “#1” as permanent.

## Artificial Analysis voice-agent details worth extracting

For streaming STT benchmark articles, capture:

- WER metric and whether lower is better;
- whether the number is **First Final Transcription** or **First Partial Transcription**;
- latency definition, usually measured from end-of-speech;
- dataset mix and weights when published;
- top rows with WER and latency, not only the rank;
- notes that no single model may lead on every dataset or every latency/accuracy regime.

For TTS Arena screenshots/pages, capture:

- Elo score and whether higher is better;
- whether the leaderboard is dynamic/live;
- top rows shown in the screenshot;
- current live FAQ/table if accessible;
- the distinction between naturalness/preference ranking and production-readiness factors such as first-audio latency, controllable pronunciation, structured alphanumeric speech, multilingual support, and deployment constraints.

## Article angle

A strong angle for voice-agent launches is usually not “model X is #1,” but:

- STT as an agent control surface: turn.start, turn.update, eager end, resume, turn.end;
- TTS as a production output layer: first-audio latency, pronunciation dictionaries, structured content, multilingual speech;
- end-to-end latency budget across listening, endpointing, LLM reasoning, tool calls, TTS first audio, barge-in, cancellation, and resume;
- observability/tracing per conversation turn.

## Pitfalls

- Do not flatten “#1 in a screenshot” into an evergreen fact; leaderboards change.
- Do not mix non-streaming STT WER with streaming STT WER without labeling the benchmark mode.
- Do not compare TTS quality Elo directly with TTS latency; they answer different questions.
- If the source is an X post with embedded benchmark images, include the images locally in both Chinese and English articles, then ground broad claims in official docs and benchmark methodology pages.