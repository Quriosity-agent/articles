# Tencent Docs source articles

Use this when the user asks to write an article from a public `docs.qq.com/doc/...` Tencent Docs link.

## Extraction pattern

Tencent Docs may render only the title, outline, and word count in `document.body.innerText`, while the actual document text is embedded in a JSONP script loaded from `/dop-api/opendoc`.

1. Open the shared doc in the browser and inspect `document.scripts` for a URL like:
   `https://docs.qq.com/dop-api/opendoc?...&id=<DOC_ID>&...&callback=clientVarsCallback...`
2. Fetch that URL through an authenticated browser session when required, using a normal browser `User-Agent` / `Referer`. Do not store or commit cookies, tokens, or session headers.
3. Strip the wrapper: `clientVarsCallback(<json>)`.
4. Parse JSON and read:
   `clientVars.collab_client_vars.initialAttributedText.text[0]`
5. Base64-decode that string. The decoded bytes are protobuf-like, but the document's plain UTF-8 text is usually embedded directly inside it.
6. Decode with `utf-8` using `errors='ignore'`, convert `\r` to newlines, remove control bytes, and trim from the first real title/heading if there is binary/protobuf prefix noise.
7. Stop at the real document content before metadata/protobuf residue begins. In practice, outline headings and the visible word count help verify completeness.

Example Python sketch:

```python
import base64, json, re
raw_js = response_text
payload = json.loads(re.match(r'clientVarsCallback\\((.*)\\)\\s*$', raw_js, re.S).group(1))
b64 = payload['clientVars']['collab_client_vars']['initialAttributedText']['text'][0]
text = base64.b64decode(b64).decode('utf-8', 'ignore')
text = text.replace('\r', '\n')
text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]+', '', text)
```

## Article-writing angle

For prompt collections or shared notes, do not simply mirror the prompt dump. Turn it into an analytical article:

- identify the reusable workflow or pattern behind the notes;
- quote/describe representative prompts only as evidence;
- group examples into categories;
- extract a reusable formula/checklist;
- connect the pattern to relevant product work when appropriate (for example article automation or AI-video production graphs).

## Verification

- Compare extracted headings against the Tencent Docs outline visible in the browser.
- Use the visible word count as a rough completeness check.
- If the source has no meaningful body images, proceed text-only and state that no local assets were needed.
- Preserve the canonical `https://docs.qq.com/doc/<id>` URL in frontmatter; query parameters from IM/app wrappers can usually be dropped.
