from pathlib import Path

root = Path(r"C:\Users\yanie\Desktop\articles\2026-03-12")

def cjk_count(s: str) -> int:
    return sum(1 for ch in s if '\u3400' <= ch <= '\u9fff')

fixed_any = False
for p in root.glob('*.md'):
    s = p.read_text(encoding='utf-8', errors='replace')
    # Try common reverse: mojibake utf-8 decoded as latin-1 then re-encoded
    try:
        repaired = s.encode('latin-1', errors='ignore').decode('utf-8', errors='ignore')
    except Exception:
        continue
    old_score = cjk_count(s) - s.count('�') * 5
    new_score = cjk_count(repaired) - repaired.count('�') * 5
    if new_score > old_score + 20:
        p.write_text(repaired, encoding='utf-8')
        fixed_any = True
        print(f'fixed {p.name}: {old_score} -> {new_score}')

if not fixed_any:
    print('no files auto-fixed')
