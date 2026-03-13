from pathlib import Path
from ftfy import fix_text

root = Path(r"C:/Users/yanie/Desktop/articles/2026-03-12")
changed = []
for p in root.glob("*.md"):
    s = p.read_text(encoding="utf-8", errors="replace")
    if any(tok in s for tok in ["ï¼", "æ", "å", "ç", "é", "â€œ", "â€"]):
        t = fix_text(s)
        if t != s:
            p.write_text(t, encoding="utf-8")
            changed.append(p.name)

print("\n".join(changed) if changed else "no changes")
