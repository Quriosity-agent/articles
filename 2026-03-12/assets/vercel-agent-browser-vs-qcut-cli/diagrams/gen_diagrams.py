from PIL import Image, ImageDraw, ImageFont
import os, math
base=r'C:\Users\yanie\Desktop\articles\2026-03-12\assets\vercel-agent-browser-vs-qcut-cli\diagrams'
os.makedirs(base,exist_ok=True)

def font(sz=22):
    try:
        return ImageFont.truetype('arial.ttf',sz)
    except:
        return ImageFont.load_default()

def box(draw,xy,text,fill='#f3f6ff',outline='#4a67d6'):
    draw.rounded_rectangle(xy, radius=16, fill=fill, outline=outline, width=3)
    x1,y1,x2,y2=xy
    bb=draw.multiline_textbbox((0,0),text,font=font(20),spacing=6)
    w,h=bb[2]-bb[0],bb[3]-bb[1]
    draw.multiline_text((x1+(x2-x1-w)/2,y1+(y2-y1-h)/2),text,fill='black',font=font(20),align='center',spacing=6)

def arrow(draw,a,b,text=None):
    draw.line([a,b],fill='#2b2b2b',width=3)
    ang=math.atan2(b[1]-a[1],b[0]-a[0]); L=12
    p1=(b[0]-L*math.cos(ang-0.4),b[1]-L*math.sin(ang-0.4)); p2=(b[0]-L*math.cos(ang+0.4),b[1]-L*math.sin(ang+0.4))
    draw.polygon([b,p1,p2],fill='#2b2b2b')
    if text:
        mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
        draw.text((mx+8,my-22),text,fill='#333',font=font(16))

img=Image.new('RGB',(1800,1100),'white'); d=ImageDraw.Draw(img)
d.text((40,25),'agent-browser Architecture (Node + Native)',fill='black',font=font(36))
box(d,(80,140,420,250),'LLM Agent / Script')
box(d,(520,140,980,250),'agent-browser CLI\n(Rust binary + JS wrapper)')
box(d,(1120,80,1700,250),'Daemon Layer\nNode daemon (Playwright) OR\nNative daemon (Rust/CDP)')
box(d,(1120,330,1700,500),'Browser Backends\nChrome/Chromium CDP\nSafari/WebDriver\nCloud providers (Browserbase/Kernel/Browser Use)')
box(d,(80,390,980,560),'Safety Controls\nAction Policy • Confirm Actions • Domain Allowlist\nContent Boundaries • Max Output • Encrypted Auth Vault')
box(d,(80,650,980,860),'Interaction Model\nopen → snapshot (refs @eN) → act (click/fill/get) → resnapshot\nOptional: annotated screenshot, diff, record, streaming WS')
box(d,(1120,650,1700,860),'State & Session\n--session / --profile / --session-name\nencrypted cookies + storage persistence\nJSON response for orchestrators')
arrow(d,(420,195),(520,195),'command'); arrow(d,(980,195),(1120,165),'IPC'); arrow(d,(1410,250),(1410,330),'CDP/WebDriver'); arrow(d,(800,250),(800,390),'guardrails'); arrow(d,(1410,500),(1410,650),'state/events'); arrow(d,(980,755),(1120,755),'responses')
img.save(os.path.join(base,'agent-browser-architecture.png'))

img=Image.new('RGB',(1800,1150),'white'); d=ImageDraw.Draw(img)
d.text((40,20),'QCut CLI Integration Map with agent-browser',fill='black',font=font(36))
box(d,(80,120,760,270),'QCut CLI Today\nPipeline-oriented TypeScript CLI\n(video gen / analysis / transcription / YAML workflows)')
box(d,(1040,120,1720,270),'agent-browser Capability\nDeterministic browser ops for AI agents\n(snapshot refs, safety, sessions, CDP/native)')
box(d,(80,360,560,520),'Borrow NOW\n1) snapshot+ref abstraction\n2) domain allowlist + output boundaries\n3) session persistence layer')
box(d,(650,360,1150,520),'Borrow NEXT\n4) stream websocket for human-in-loop\n5) diff snapshot/screenshot for QA\n6) action confirmation gating')
box(d,(1240,360,1720,520),'Borrow LATER\n7) pure native runtime slices (Rust)\n8) cloud browser provider adapters\n9) iOS/Safari backend parity')
box(d,(80,620,1720,760),'Adoption constraint: QCut cannot "drop-in replace" with agent-browser.\nBest path = sidecar module (qcut web-runner) and unify command schema progressively.')
box(d,(80,840,1720,1060),'Recommended Architecture\nQCut Orchestrator → Browser Adapter Interface\n→ Adapter A: agent-browser subprocess (immediate)\n→ Adapter B: future native bridge\nKeep QCut pipeline contracts stable; expose browser state as artifacts for downstream video workflows.')
arrow(d,(760,195),(1040,195),'gap'); arrow(d,(300,270),(300,360)); arrow(d,(900,270),(900,360)); arrow(d,(1500,270),(1500,360)); arrow(d,(300,520),(300,620)); arrow(d,(900,520),(900,620)); arrow(d,(1500,520),(1500,620)); arrow(d,(900,760),(900,840),'implementation path')
img.save(os.path.join(base,'qcut-agent-browser-integration-map.png'))
print('done')