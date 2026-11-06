# Sources and Verification

Reviewed November 6, 2026 (Australia/Melbourne). The article folder follows the original Zhihu publication date.

| Source | What it supports |
|---|---|
| [清流Agent, Zhihu](https://zhuanlan.zhihu.com/p/2041861168235536468) | Page displayed May 24, 2026, 14:42. The diary describes the Windows wrapper, processing changes, listening impressions, and upload attempts. These are author reports, not a controlled benchmark. |
| [Audio Separator](https://github.com/nomadkaraoke/python-audio-separator) | Independent Python/CLI project that runs pretrained separation models and documents its FFmpeg dependency. Not the source of the author's WinForms wrapper. |
| [KUIELab-MDX-Net](https://arxiv.org/abs/2111.12203) | Primary research on music demixing. Used for technical context, not as identification or validation of the author's exact checkpoint. |
| [Suno Terms](https://suno.com/terms) | Revision dated August 10, 2026; effective September 3, 2026. Used for the upload rights language at review time, not as a reconstruction of the terms in May. |
| [Suno Community Guidelines](https://suno.com/community-guidelines) | Rules against evasion and unauthorized use, and the appeal route. |
| [Suno Cover help](https://help.suno.com/en/articles/2872257) | Official description of changing the style of a song you created. No current plan limits inferred from the older article. |

The text reader returned 403, but the public article rendered in the browser without signing in. Its readable body did not supply a repository or binary for `Mp3Splitter`. Focused public searches did not identify that version. Direct requests for the page's image assets returned HTTP errors, so no original images are republished. `stereo-difference.svg` is an original figure based on the local calculation below, not a screenshot or a platform result.

## Synthetic Stereo Difference

The following was run locally with Node.js. No third-party audio, codec, neural separator, or network service is involved. The 80 Hz and 440 Hz sine waves are identical in the two input arrays; only the left array contains the 660 Hz sine. The calculation projects the one-second arrays onto each sine wave to recover its amplitude.

```js
const n = 48000;
const terms = [[80, 0.2], [440, 0.3], [660, 0.1]];
const amplitude = (samples, f) => Math.abs(samples.reduce(
  (sum, value, i) => sum + value * Math.sin(2 * Math.PI * f * i / n), 0
) * 2 / n);
const tones = terms.map(([f, a]) => Float64Array.from(
  { length: n }, (_, i) => a * Math.sin(2 * Math.PI * f * i / n)
));
const right = tones[0].map((value, i) => value + tones[1][i]);
const left = right.map((value, i) => value + tones[2][i]);
const difference = left.map((value, i) => value - right[i]);
for (const [f] of terms) {
  console.log(f, ...[left, right, difference].map(x => amplitude(x, f).toFixed(6)));
}
```

| Frequency | Left | Right | Left minus right |
|---|---:|---:|---:|
| 80 Hz | 0.200000 | 0.200000 | 0.000000 |
| 440 Hz | 0.300000 | 0.300000 | 0.000000 |
| 660 Hz | 0.100000 | 0.000000 | 0.100000 |

The author's executable was not obtained or run. No model inference, listening comparison on real songs, upload, generation, or platform-detection test was performed. The numeric example is not a benchmark of any separator or an explanation of Suno's proprietary system.
