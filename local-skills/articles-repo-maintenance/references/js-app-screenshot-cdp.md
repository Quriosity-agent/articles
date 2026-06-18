# JS/WebGL app screenshots via Chrome DevTools Protocol

Use this when an article source is an interactive product app (Vite/React/WebGL/canvas) and a plain headless `--screenshot` captures only an empty/default state or misses the loaded sample scene.

## Pattern

1. Start Chrome with remote debugging and an isolated profile:
   ```bash
   '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
     --headless=new \
     --remote-debugging-port=9223 \
     --remote-allow-origins='*' \
     --user-data-dir=/tmp/article-cdp-profile \
     --disable-gpu \
     --window-size=1440,900 \
     about:blank
   ```
   - `--remote-allow-origins='*'` avoids Chrome rejecting the local WebSocket handshake.
   - Use Hermes background process management for the Chrome process and kill it when done.

2. Use CDP to open the product URL, wait for app text, click UI controls, then capture the page screenshot. Minimal Python shape:
   ```python
   import base64, json, os, time, urllib.request, websocket

   req = urllib.request.Request(
       'http://127.0.0.1:9223/json/new?https://example.app/',
       method='PUT',
   )
   info = json.load(urllib.request.urlopen(req, timeout=10))
   ws = websocket.create_connection(
       info['webSocketDebuggerUrl'],
       timeout=10,
       origin='http://127.0.0.1:9223',
   )

   seq = 0
   def cmd(method, params=None):
       global seq
       seq += 1
       ws.send(json.dumps({'id': seq, 'method': method, 'params': params or {}}))
       while True:
           msg = json.loads(ws.recv())
           if msg.get('id') == seq:
               if 'error' in msg:
                   raise RuntimeError(msg['error'])
               return msg.get('result', {})

   cmd('Page.enable'); cmd('Runtime.enable')
   for _ in range(80):
       text = cmd('Runtime.evaluate', {
           'expression': 'document.body.innerText',
           'returnByValue': True,
       })['result'].get('value', '')
       if 'Expected App Text' in text:
           break
       time.sleep(0.25)

   # Example: open a menu and load a bundled sample project before screenshotting.
   cmd('Runtime.evaluate', {'expression': "[...document.querySelectorAll('button')].find(b=>b.innerText.includes('File'))?.click()"})
   time.sleep(0.5)
   cmd('Runtime.evaluate', {'expression': "[...document.querySelectorAll('button')].find(b=>b.innerText.includes('Load Sample Project'))?.click()"})
   time.sleep(2)

   shot = cmd('Page.captureScreenshot', {
       'format': 'png',
       'captureBeyondViewport': False,
   })['data']
   open('/tmp/app-ui.png', 'wb').write(base64.b64decode(shot))
   ws.close()
   ```

3. Convert large PNG screenshots to WebP before committing:
   ```python
   from PIL import Image
   im = Image.open('/tmp/app-ui.png').convert('RGB')
   im.save('/tmp/app-ui.webp', quality=88, method=6)
   ```

4. Verify with vision before embedding. Keep the screenshot only if it shows meaningful UI state: menus/panels/outliner/camera preview/sample data. If WebGL content is dark/blank but the surrounding UI still proves the product workflow, caption it carefully and do not overclaim visible 3D content.

## Pitfalls

- Plain `chrome --headless --screenshot URL` may load a fresh empty project instead of a useful sample state; interact with the app first through CDP.
- `/json/new?...` on modern Chrome may require HTTP `PUT`, not `GET`.
- Canvas `toDataURL()` can return a tiny/default canvas when the useful view is composited elsewhere or not drawn in headless mode; prefer full-page CDP screenshot plus vision verification.
- Do not leave the remote-debugging Chrome process running after capture.
