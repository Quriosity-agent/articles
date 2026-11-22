# Sources and local verification

Reviewed November 23, 2026 (Australia/Melbourne). The root article date is the website-review date; individual research notes were published earlier.

- [Home](https://generalised.si/), [Approach](https://generalised.si/approach), and [Contact](https://generalised.si/contact): positioning, proposed workflow, and preview access. No preview registration, credentials, paid service, or full discovery-system run.
- [Research index](https://generalised.si/research): public counts, mixed evidence levels and scope.
- [GSI-R-0018](https://generalised.si/research/solver-compiler-and-factory): declared classes, prebuilt solvers, internal evaluation and explicit lack of demonstrated automatic solver generation.
- [GSI-R-0007](https://generalised.si/research/williamson-good-order-75): distinct timing baselines and missing search-completeness certificate. No performance replication.
- [GSI-R-0004](https://generalised.si/research/cyclic-difference-set-465): finite checker, data and assumptions. No independent review of the reduction theorems, historical priority or entire non-existence proof.

The two local WebP images are editorial screenshots of the public website captured in an isolated Chromium session at 1360×1000. They are not screenshots of a logged-in research preview.

## Reproduce the finite check

The accompanying [rebuild_candidates.py](rebuild_candidates.py) is a small local reconstruction script following the published recipe. It imports no code from the lab's checker. It is not a separate proof of the mathematics. Run from this notes directory:

```sh
out="$(mktemp -d)"
cp rebuild_candidates.py "$out/"
mkdir -p "$out/data" "$out/aux"
base=https://generalised.si/files/cyclic-difference-set-465
for f in check.py SHA256SUMS data/L31_orbit_reps.txt aux/lajolla_smallest.py aux/lajolla_smallest.out; do
  curl -fsSL "$base/$f" -o "$out/$f"
done
python3 "$out/rebuild_candidates.py"
(cd "$out" && shasum -a 256 -c SHA256SUMS)
python3 "$out/check.py"
```

Inspect downloaded code before execution. It uses the Python standard library and local files; it does not run a cloud agent. The two auxiliary files are included to satisfy the hash manifest; their La Jolla database audit was not rerun.

Local result on macOS with Python 3.15.1:

- 729 orbit representatives expand to 45,198 elements and 21,328 candidates.
- Candidate SHA-256: `d8847554f4c93355b00b3d6f23510e283f243a2a02d9ceb1bd2d5e7d021f37d7`.
- Downloaded checker SHA-256: `eb74acfd6fe06f8e77388b52fe250f846a1fa682a1cff73f0a53517b6bd63e22`.
- Orbit-representative file SHA-256: `9976eff808078ed0e1c502b89ebb594fec37863ec836895bdf725e85b4813a28`.
- All five manifest checks passed. The upstream checker reported zero surviving candidates and accepted 7,812 positive controls, then printed `ALL CHECKS PASSED` and exited 0 (3.7 seconds reported by that run).

That single runtime is a reproduction observation, not a speed benchmark. The site explicitly distinguishes the finite checks from the cited mathematical reduction and notes that no full machine-checked proof or external-lab review is established. The upstream checker/data are fetched from their public source for reproduction, not redistributed in this article.
