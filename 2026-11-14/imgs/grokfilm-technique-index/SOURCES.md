# Sources and Verification

Reviewed November 14, 2026, Australia/Melbourne. This is a live-site snapshot, not an announcement date.

- [Public index](https://grokfilm.app/#index): browser-rendered catalogue, filters, detail overlays, copyright and attribution. The static web reader showed zero-count placeholders before JavaScript execution; the rendered browser showed 300 entries, eight categories.
- [Page HTML](https://grokfilm.app/), SHA-256 `f5f96681cc88d838923e34bf9a05392c45f8e8ffab1299217f1f6d5b120ad9e1`: inspected the `buildPrompt`, `grokBtn`, `copyBtn`, and `buildBtn` handlers. The clipboard and Grok handoff are source-review findings; neither was clicked. No Grok prompt prefill, generation, settings, billing, or cross-model performance was tested.
- [Public catalogue data](https://grokfilm.app/data.js), SHA-256 `04ceb38532faf8b7ee6cc74153291b9f04c646cd5401532cef522cd3e10b8a5f`: parsed the JSON array inside the `const TECHNIQUES` declaration without executing the script. Counted 300 records, 300 unique slugs, eight categories, and 29 truthy `video` fields. Field presence does not establish asset availability or fidelity.

| Local image | Source and scope |
|---|---|
| `rack-focus.jpg` | Browser capture after searching `rack focus` and opening the one returned entry. The accessibility tree additionally showed the reel placeholder. |
| `studio.jpg` | Browser capture after clicking Build your GrokFilm; Coming Soon / Under Construction visible. |
| `dolly-contact.jpg` | Frames 0, 72, and 144 of the [site's Dolly Shot reel](https://grokfilm.app/media/dolly-shot.mp4), each resized to 376 × 208 and tiled left to right. |

The UI and demonstration material are attributed to GrokFilm/Tetsuo Corp.; the site labels the reel as rendered in Grok Imagine. Limited editorial illustrations, not an assertion of asset reuse rights. The source MP4 is not redistributed here.

## Sample Reel Check

- Browser loaded the Dolly Shot video with `readyState=4`. The file SHA-256 was `6c63b33418d6e0439f479968bfbcacf7267fe2dadbd03be5f9098aa6f891ec98`.
- FFprobe reported a 6.041667-second container and a main H.264 stream at 752 × 416, 24 fps, 145 frames. The AAC audio track and main video decoded through EOF without errors. No audio quality judgment was made. The file also carries a separate MJPEG stream.
- Visual comments refer to the extracted frames only. We did not independently verify the model, the original prompt, a real-world camera path, or the other linked videos.

```sh
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames dolly-shot.mp4
ffmpeg -v error -xerror -i dolly-shot.mp4 -map 0:v:0 -map 0:a:0 -f null -
ffmpeg -v error -i dolly-shot.mp4 \
  -vf "select='eq(n,0)+eq(n,72)+eq(n,144)',scale=376:208,tile=3x1" \
  -frames:v 1 dolly-contact.jpg
```
