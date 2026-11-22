"""Reconstruct the public candidate file, without importing the lab's checker."""
from hashlib import sha256
from pathlib import Path

root = Path(__file__).resolve().parent
representatives = [
    tuple(int(value) for value in row.split())
    for row in (root / "data/L31_orbit_reps.txt").read_text().splitlines()
    if row.strip()
]
elements = set()
for representative in representatives:
    assert len(representative) == 31
    for offset in range(31):
        rotated = representative[offset:] + representative[:offset]
        for sign in (1, -1):
            elements.add(tuple(sign * value for value in rotated))
candidates = sorted(
    tuple(value + 5 for value in element)
    for element in elements
    if sum(element) == -10 and all(-5 <= value <= 10 for value in element)
)
output = "".join(" ".join(map(str, row)) + "\n" for row in candidates).encode()
(root / "data/S31.txt").write_bytes(output)
digest = sha256(output).hexdigest()
assert (len(representatives), len(elements), len(candidates)) == (729, 45198, 21328)
assert digest == "d8847554f4c93355b00b3d6f23510e283f243a2a02d9ceb1bd2d5e7d021f37d7"
print(len(representatives), len(elements), len(candidates), digest)
