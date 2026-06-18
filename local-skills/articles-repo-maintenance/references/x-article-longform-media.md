# X Articles / Longform Posts with Many Embedded Media

Use this reference when Peter asks to write an article from an X/Twitter Article or longform post that contains many inline screenshots, tutorial frames, or a video thumbnail.

## Extraction pattern

1. Open the X URL in the browser even if the page shows login/signup overlays.
2. Use DOM extraction on `article` rather than relying on the compact accessibility snapshot:
   ```js
   [...document.querySelectorAll('article')].map(a => ({
     text: a.innerText,
     links: [...a.querySelectorAll('a')].map(l => ({text: l.innerText, href: l.href})),
     imgs: [...a.querySelectorAll('img')].map(img => ({
       src: img.currentSrc || img.src,
       alt: img.alt,
       w: img.naturalWidth,
       h: img.naturalHeight
     }))
   }))
   ```
3. Download meaningful `pbs.twimg.com/media/...` images as `name=orig` where possible. Keep the original source frames in the article asset folder for traceability.
4. If there are many tutorial images, create 2–4 compact contact sheets (`contact-sheet-1.webp`, etc.) for embedding in both Chinese and English articles. Keep source frames too, but embed contact sheets unless individual frames are essential.
5. Inspect contact sheets with vision before embedding: verify they are readable enough and describe a coherent workflow.
6. Scan text for promotional contact details or ad-like personal acquisition snippets from the social post (for example “加 V / +V / WeChat handle”) and avoid copying them into the article unless editorially necessary. Keep the source URL attribution instead.
7. Verify every relative image link exists before staging.

## Example contact-sheet generator

```python
from PIL import Image, ImageDraw
from pathlib import Path

D = Path('YYYY-MM-DD/imgs/<slug>')
files = sorted(D.glob('source-*.jpg'))
thumbs = []
for p in files:
    im = Image.open(p).convert('RGB')
    im.thumbnail((320, 220))
    canvas = Image.new('RGB', (320, 245), 'white')
    canvas.paste(im, ((320 - im.width) // 2, 0))
    dr = ImageDraw.Draw(canvas)
    dr.rectangle([0, 222, 319, 244], fill=(20, 20, 20))
    dr.text((8, 226), f'{p.stem.replace("source-", "")}  {Image.open(p).size}', fill='white')
    thumbs.append(canvas)

for sheet_idx in range((len(thumbs) + 8) // 9):
    subset = thumbs[sheet_idx*9:(sheet_idx+1)*9]
    sheet = Image.new('RGB', (3*320, 3*245), 'white')
    for i, t in enumerate(subset):
        sheet.paste(t, ((i % 3) * 320, (i // 3) * 245))
    sheet.save(D / f'contact-sheet-{sheet_idx+1}.webp', 'WEBP', quality=82, method=6)
```

## Article angle

For tutorial-style X Articles, write a practical workflow analysis rather than a simple transcript. Useful structure:

- The production problem the tutorial solves.
- The tool/workflow abstraction behind the screenshots.
- A step-by-step operational breakdown.
- Recommended SOP for creators.
- Product implications for AI-video / creative tools.

For AI-video director-stage/tutorial sources specifically, emphasize the shift from prompt-only generation toward production engineering: spatial plan, camera/shot planning, reference assets, generation, and editing iteration.
