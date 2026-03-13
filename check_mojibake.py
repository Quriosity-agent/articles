from pathlib import Path
root=Path(r'C:\Users\yanie\Desktop\articles\2026-03-12')

def cjk(t):
    return sum(1 for ch in t if '\u3400' <= ch <= '\u9fff')

for p in root.glob('*analysis.md'):
    s=p.read_text(encoding='utf-8',errors='replace')
    r=s.encode('latin-1',errors='ignore').decode('utf-8',errors='ignore')
    print(p.name, 'cjk', cjk(s), '->', cjk(r), 'rep', s.count('�'), '->', r.count('�'))
