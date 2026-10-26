# Sound for AI Video: A Six-Source Workflow for Music, Ambience, and Timed Effects

> Source: [3three_AI's X post](https://x.com/3three_AI/status/2114545802211103044), published October 26, 2026. Websites and code checked October 27. Filed under the post date. The six destinations are Pixabay Music, Freesound, Sound Effect Lab, Mixkit, ElevenLabs Sound Effects, and Leonxlnx/earshot.

A character opens a door, but the soundtrack contains only continuous music. The camera moves to another room without an acoustic change. A button finishes moving before its click arrives. A different video-generation model will not necessarily fix these problems.

The six resources make more sense as different sound jobs: music establishes pace and feeling, ambience establishes space, action sounds make events tangible, transitions emphasize selected changes, generators fill gaps, and procedural tools provide adjustable effects and timing evidence. Their capabilities overlap; no video needs all six by default.

![Official earshot demonstration montage with typing, buttons, notes, and moving graphics](imgs/ai-video-six-audio-sources/launch_frames.png)

*This is the official higher-resolution version of the earshot montage used in the post. It is not a film jointly produced by all six services or a production result from this review.*

## 1. What Each Destination Is For

| Resource | Primary role | A useful search approach |
|---|---|---|
| [Pixabay Music](https://pixabay.com/music/) | Existing background music | Search mood, style, and usable section length rather than titles alone |
| [Freesound](https://freesound.org/) | Field recordings, foley, and individual sound assets | Combine object, material, action, distance, and setting |
| [Sound Effect Lab](https://soundeffect-lab.info/) | Categorized everyday, combat, presentation, and interface effects | Narrow results with Japanese categories and action terms |
| [Mixkit Transition](https://mixkit.co/free-sound-effects/transition/) | Whooshes, sweeps, impacts, and editorial accents | Match motion, speed, and weight; avoid repeating one effect on every cut |
| [ElevenLabs Sound Effects](https://elevenlabs.io/sound-effects) | Text-generated effects and ambience | Specify source, action, material, space, and unwanted background |
| [earshot](https://github.com/Leonxlnx/earshot) | Procedural effects, candidate analysis, and synchronization evidence | Turn audio into measurements, then confirm the listening result |

At review time, Pixabay advertised over 300,000 tracks and Freesound displayed 737,948 sounds. These are catalog snapshots, not quality rankings. Sound Effect Lab's Japanese search and categories were confirmed, but the post's claim of more than two thousand assets was not independently counted. Mixkit's transition page listed 42 items; the wider site includes other sound categories. [Pixabay](https://pixabay.com/music/), [Freesound](https://freesound.org/), [Mixkit transitions](https://mixkit.co/free-sound-effects/transition/)

## 2. Search the First Four Libraries by the Event

Pixabay is a useful place to shortlist music, but a score does not replace scene sound. A music-led product film may start from a beat grid; dialogue-led fiction should protect speech and key actions before fitting music around them. This is an editorial recommendation, not a mandatory order imposed by the websites.

Freesound's value is specific recordings. Cinematic is usually too broad a query. A close, gently closing wooden door indoors, or rain on a metal roof with distant passing traffic, describes the actual sound. Check noise, decay, and recording distance before accepting a candidate; its filename alone does not establish suitability.

Sound Effect Lab organizes everyday, mechanical, environmental, and interface sounds clearly. Japanese searches such as `雨` for rain, `足音` for footsteps, and `ドア` for doors can help. Mixkit offers a quick transition shortlist and states that sound effects can be downloaded without signup. An intentionally quiet cut needs no whoosh at all. [Sound Effect Lab](https://soundeffect-lab.info/), [Mixkit sound effects](https://mixkit.co/free-sound-effects/)

## 3. ElevenLabs Fills Gaps; earshot Does a Different Job

Text generation becomes useful when no recording matches a particular material and action. A starting description might specify a heavy metal latch sliding into a lock in a small room, short and dry, with no music or voices. This is an illustrative prompt, not a generation or listening result obtained here.

ElevenLabs supplies a hosted model service. earshot's `sfx` renders packaged code recipes. These are different mechanisms, not interchangeable forms of AI sound generation.

The post mentions 201 earshot sounds. At the inspected 0.4.0 commit, `591fa3e`, four bank JSON files contain **252 unique effect IDs**: 183 existing recipes, 51 additions, 15 fitted entries, and three pluck entries. These are renderable entries, not 252 trained models or necessarily 252 distinct sound categories. [Pinned sound banks](https://github.com/Leonxlnx/earshot/tree/591fa3e028032e6dce56620a20e932e35667e8d8/earshot/forge/bank)

More useful than the count are the parameters and synchronization landmarks. Effects can be adjusted through controls such as duration, peak position, and pitch. A `kit` records role selections and measured onset, peak, and end times for a downstream renderer or mixer to place against cues. The beginning of an audio file is not necessarily the point that should align with a visual event. [Bank implementation](https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/earshot/forge/bank.py), [kit implementation](https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/earshot/forge/kit.py)

![Official earshot analysis sheet with frames, events, spectrum, waveform, loudness, and synchronization markers](imgs/ai-video-six-audio-sources/launch_sheet.png)

*This upstream sheet analyzes the project's own demonstration film. Its numbers and labels are not measurements made for this article, and event labels are not guaranteed human annotations.*

earshot also provides matching, recording searches, timelines, and meters. Its limits document treats mixed-audio event labels as hints and launch-film scoring as a style-specific reference. It cannot establish beauty, brand fit, or licensing. Model-free `sfx` rendering requires no inference or network, but the complete package still has dependencies. Semantic analysis uses audio models; the optional Gemini opinion uploads audio after explicit consent. [Limits](https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/docs/LIMITS.md), [upload boundary](https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/earshot/llm.py)

## 4. Downloading, Commercial Use, and Redistribution Are Different Rights

This table summarizes the official material reviewed, not a substitute for checking an individual asset and intended use.

| Source | Boundary to retain |
|---|---|
| Pixabay | Free use and adaptation without mandatory attribution, subject to restrictions including substantially unchanged standalone sale/distribution and other applicable rights |
| Freesound | Check CC0, CC BY, or CC BY-NC per item; free download does not erase attribution or noncommercial restrictions |
| Sound Effect Lab | Free commercial use without mandatory credit, but restrictions include redistribution, AI training, and rights registration that interferes with others |
| Mixkit | The Sound Effects Free License supports commercial and noncommercial end products, not standalone stock/tool/template redistribution or rights-management registration |
| ElevenLabs | The current sound-effects page distinguishes free noncommercial use from paid-account commercial use; a free test generation is not default client-delivery clearance |
| earshot | MIT code with separate source records for fitted recipes; analyzing or fitting outside assets does not change their licenses |

Sources: [Pixabay summary](https://pixabay.com/service/license-summary/), [Freesound FAQ](https://freesound.org/help/faq/), [Sound Effect Lab terms](https://soundeffect-lab.info/agreement/), [Mixkit sound-effects license](https://mixkit.co/license/modal/sfxFree/), [ElevenLabs sound-effects FAQ](https://elevenlabs.io/sound-effects), [earshot fitted-source credits](https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/docs/CREDITS_FIT.md).

Incorporating an effect into a film is not the same as offering it to other people as stock. Sound Effect Lab explicitly lists default effects inside an editor and sound-distribution packages as redistribution scenarios. Permission for a video does not automatically authorize bundling assets with software, templates, or a public repository.

Freesound also explains that legitimately obtained effects can still trigger platform copyright matching. Keep a project asset record: filename, creator, original page, license, acquisition date, modifications, and final usage. Licensing supports the right to use a sound; it does not guarantee that platform matching will never make a mistake.

## 5. Turn the Resource List into a Reviewable Timeline

The following is a proposed lightweight workflow, not a film produced and tested during this review:

1. **Choose the sound lead.** Prioritize dialogue and actions in speech-led work, or establish rhythm in music-led work. Avoid making every track compete for attention.
2. **Establish space, then action.** Maintain scene continuity with ambience, then align doors, footsteps, and object handling with events. Check whether a scene change needs an acoustic change.
3. **Accent selected changes.** Reserve transitions for meaningful motion or reveals. Ordinary cuts need not all be sounded.
4. **Generate or synthesize missing material.** Try text generation for a specific material/action combination, and procedural recipes for interface or motion-graphics gestures. Choose by the sound task.
5. **Listen and retain evidence.** Check masked dialogue, abrupt tails, loop seams, and audiovisual timing. Measurements locate problems; listening determines whether a fix works.

This review resolved the six links, read site descriptions and relevant terms, and counted earshot's bank entries structurally. It did not bulk-download audio, call paid models, run listening blind tests, or produce a film. Media and evidence are documented in [SOURCES.md](imgs/ai-video-six-audio-sources/SOURCES.md). The earlier [earshot article](../2026-10-16/2026-10-16-earshot-agent-audio-evidence-layer-en.md) provides a deeper technical reading.

The six destinations cover different jobs: music, real spaces, actions, editorial accents, missing assets, and timing or level checks. A successful soundtrack comes from serving the same scene, not from maximizing the number of audio tracks.
