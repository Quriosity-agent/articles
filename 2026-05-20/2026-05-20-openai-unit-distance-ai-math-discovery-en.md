# OpenAI’s Discrete Geometry Breakthrough: When AI Independently Refuted Erdős’s Unit Distance Conjecture

> Original: [An OpenAI model has disproved a central conjecture in discrete geometry](https://openai.com/index/model-disproves-discrete-geometry-conjecture/)  
> Proof: [Planar Point Sets with Many Unit Distances](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf)  
> Companion remarks: [Remarks on the Disproof of the Unit Distance Conjecture](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf)  
> CoT summary: [Rewritten Chain of Thought for the Solution to the Unit Distance Problem](https://cdn.openai.com/pdf/1625eff6-5ac1-40d8-b1db-5d5cf925de8b/unit-distance-cot.pdf)  
> Source: OpenAI  
> Author: OpenAI  
> Published: 2026-05-20  
> Article date: 2026-05-20  
> Tags: OpenAI / AI for Math / Discrete Geometry / Unit Distance Problem / Erdős / Algebraic Number Theory / Research Automation

![OpenAI Unit Distance Problem cover](imgs/openai-unit-distance-ai-math-discovery/og-polynomial-construction.png)

OpenAI’s new announcement is not a benchmark, a product feature, or another “AI solves contest math” demo. It is historically heavier: an internal general-purpose reasoning model produced a counterexample to the planar unit distance conjecture, refuting a long-standing belief around one of the central problems in discrete geometry.

The problem is easy to state: if you place $n$ points in the plane, how many pairs can be exactly distance 1 apart? Paul Erdős raised the question in 1946, and it has remained one of the best-known, easiest-to-explain, and hardest-to-move problems in combinatorial geometry.

The important part is not merely that “AI solved a hard problem.” OpenAI says the proof came from a new general-purpose reasoning model, not from a system specially trained for this problem, scaffolded around unit-distance search, or hand-designed to explore this particular conjecture. The proof was then checked by external mathematicians, and a companion paper was written by Noga Alon, Thomas Bloom, W. T. Gowers, Daniel Litt, Will Sawin, Arul Shankar, Jacob Tsimerman, Victor Wang, and Melanie Matchett Wood.

This article focuses on three questions:

1. What exactly was refuted?
2. Why does algebraic number theory suddenly appear in a planar geometry problem?
3. Why is this a deeper signal for AI research automation than another math medal or puzzle result?

---

## 1. The refuted belief was near-linearity, not the existence of any upper bound

Let $u(n)$ denote the maximum number of unit-distance pairs among $n$ points in the plane.

A few scales help frame the result:

| Construction / bound | Meaning |
|---|---|
| $n$ equally spaced points on a line | About $n-1$ unit distances, linear scale |
| Square-grid constructions and rescalings | About $n^{1+C/\log\log n}$, slightly superlinear |
| Spencer–Szemerédi–Trotter upper bound | $O(n^{4/3})$, the best general upper-bound scale known |
| Erdős conjectural direction | Essentially, $u(n)$ should not significantly exceed $n^{1+o(1)}$ |
| OpenAI model’s counterexample | For infinitely many $n$, at least $n^{1+\delta}$ unit-distance pairs |

So the proof does not improve the upper bound from $n^{4/3}$ to some smaller exponent. It refutes the long-held belief that the optimal construction is only barely superlinear. The new construction gives a fixed polynomial improvement.

OpenAI notes that the original AI proof did not make $\delta$ explicit. A forthcoming refinement by Princeton mathematician Will Sawin shows that one can take $\delta=0.014$. The number is small, but the qualitative shift is large: the gain in the exponent is no longer tending to zero.

---

## 2. Why the square grid used to look close to optimal

The classical Erdős lower bound is powered by the square grid.

In an $m \times m$ integer grid, the number of points is $n=m^2$. If an integer $k$ can be written as $a^2+b^2$, then difference vectors like $(a,b)$ and their symmetries create many edges of length $\sqrt{k}$. Rescale the whole configuration by $1/\sqrt{k}$, and those edges become unit distances.

In algebraic language, this is connected to the Gaussian integers $\mathbb{Z}[i]$: numbers of the form $a+bi$ turn “sum of two squares” into a norm problem. If $k$ has many prime factors congruent to $1 \pmod 4$, it has many representations as a sum of two squares, and the grid gains many same-length directions.

But this mechanism has a ceiling. It yields a scale like $n^{1+C/\log\log n}$, where the extra exponent tends to zero. It is powerful, but not powerful enough to produce $n^{1+\delta}$.

For decades, the natural belief was that grid-like constructions had already captured the essence of the problem. OpenAI’s model found a construction outside that intuition.

![Classical grid/unit-distance structure](imgs/openai-unit-distance-ai-math-discovery/unit-distance-grid.svg)

---

## 3. The new construction jumps from Gaussian integers to deeper algebraic number theory

The proof does not simply draw a cleverer planar pattern. It first moves into high-dimensional algebraic structure, then projects back down to the plane.

The proof abstract gives the route:

1. Build an infinite unramified tower of totally real number fields;
2. Ensure these extensions have growing 3-power Galois groups and a fixed set of rational primes splitting completely;
3. Adjoin $i$ to obtain the corresponding CM fields;
4. Use the embeddings of those fields to build high-dimensional lattices;
5. Find many elements whose images under every complex embedding have absolute value 1;
6. Project a suitable lattice window back to one complex coordinate, producing planar point sets with many unit distances.

This is not the usual toolbox for an elementary-looking Euclidean geometry problem. The companion remarks explicitly connect the argument to ideas associated with Ellenberg–Venkatesh, Golod–Shafarevich, and Hajir–Maire–Ramakrishna. Golod–Shafarevich theory is used to ensure the required infinite tower exists, even after a quotient step that makes prescribed Frobenius classes trivial.

The conceptual jump is that “unit-length differences” in the plane become “algebraic numbers whose complex embeddings all have absolute value 1.” The problem is rerouted through class field towers, class numbers, discriminants, and splitting primes.

That is why mathematicians find the result surprising: the tools were familiar in algebraic number theory, but few expected them to decide a basic-looking question about distances in the Euclidean plane.

---

## 4. Why this is an AI-math milestone, not just another solving demo

OpenAI’s strongest claim is that this is the first time an AI system has autonomously resolved a prominent open problem central to a mathematical subfield.

That should be separated from several weaker achievements:

- not merely producing a polished proof fragment;
- not merely reaching human level on known contest-style problems;
- not merely helping a mathematician check, organize, or complete a proof;
- but proposing a construction strong enough to refute a long-held conjecture, then surviving external mathematical scrutiny and human digestion.

The companion remarks carry unusual weight. Tim Gowers writes that if a human had written the paper and submitted it to the Annals of Mathematics, he would have recommended acceptance without hesitation. Arul Shankar observes that much of the model’s chain of thought tries to construct a counterexample to the widely believed upper bound, rather than prove it; to him, this suggests mathematical intuition, willingness to try a long-shot approach, and the ability to carry an original idea through.

That is different from brute-force proof search. The interesting behavior is that the model chose to challenge the community’s default belief: instead of proving $n^{1+o(1)}$, it suspected a loophole and pursued a counterexample.

![OpenAI visual material for the model/math investigation](imgs/openai-unit-distance-ai-math-discovery/model-success-chart.webp)

---

## 5. Human mathematicians did not disappear; their role became more important

It is easy to misread the announcement as “AI replaces mathematicians.” The public record suggests a better description: AI generated a high-value original proof, while human mathematicians verified, digested, simplified, contextualized, and interpreted it.

The companion remarks describe themselves as a “short, digested, human-verified” version of the OpenAI-generated counterexample. In other words, the original proof may contain the key ideas, but community absorption requires humans to place it in the literature, clarify attribution, identify reusable structure, and assess implications for neighboring problems.

Thomas Bloom proposes a useful criterion: when judging an AI-generated proof, ask whether it teaches us something new about the problem. For this result, his answer is a moderated yes. It reveals that number-theoretic constructions may have much more to say about discrete geometry than expected, and that the required number theory can be very deep.

That is the more important pattern for AI for science:

- models can connect tools across fields;
- experts decide whether the connection is real, meaningful, and generalizable;
- the community turns a result into a new research direction.

---

## 6. The real signal for AI research automation

The significance for AI is not “math was a final fortress and now it has fallen.” The more practical signal is that models are beginning to show a bundle of capabilities that research automation needs.

### 6.1 Long-chain coherence

A mathematical proof is not a normal Q&A task. A long argument only works if every definition, quantifier, boundary condition, and estimate stays aligned. This construction must travel from number fields to planar point-set counts; a loose step anywhere can break the result.

### 6.2 Cross-domain recoding

The surface problem belongs to discrete geometry, but the key machinery comes from algebraic number theory. The model did not merely apply a local trick. It recoded the problem in a different mathematical language.

### 6.3 Exploration against consensus

The community broadly believed the near-linear conjecture. The model pursued the opposite direction: maybe there is a counterexample. That matters for automated research, because many breakthroughs come from exposing hidden weaknesses in consensus rather than tightening consensus proofs.

### 6.4 Verifiable artifacts

Mathematics gives AI a clear verification surface. A proof either checks or it does not. Compared with biology, materials science, or medicine, this makes math an unusually clean testbed for advanced reasoning systems.

---

## 7. Stay calm: this does not mean models can do all mathematics now

The result is strong, but its boundaries matter:

1. **The model identity and training details are not public.** OpenAI describes it as an internal model; the capability should not be projected onto all public models.
2. **The result was human-verified and rewritten.** The community-readable version is not a raw model transcript dropped directly into publication.
3. **A breakthrough is not a production line.** Solving one open problem does not imply stable performance across arbitrary frontier problems.
4. **Mathematical verification is unusually clean.** Transferring the pattern to experimental science requires more complex real-world feedback loops.

A more reasonable conclusion is that this is a phase-change signal. AI is no longer only a proof assistant in every case; in some frontier settings, it can enter the zone of proposing original, verifiable constructions.

---

## 8. What product builders should take from this

For people building AI-agent products, the lesson is not just “models got stronger.” The breakthrough came from the combination of model capability, problem selection, verification surface, and expert review.

Abstracted as an agent workflow, it looks like this:

```text
high-value open problem
  → clear verifiable target
  → model proposes candidate construction/proof
  → external experts verify
  → humans digest and rewrite
  → community absorbs it as a new research direction
```

That is a more realistic picture of research automation than “let the agent run forever.” The point is not to remove humans entirely, but to move humans to higher-leverage roles: choosing problems, defining evaluations, reviewing artifacts, and interpreting significance.

The same pattern will matter in software engineering, video generation, scientific computing, and materials search. Useful agents will not merely execute commands; they will produce verifiable artifacts that experts can quickly decide to accept, reject, or develop further.

---

## 9. Conclusion: AI is entering the hard zone of creative research

OpenAI’s unit-distance result matters because several conditions line up at once:

- the problem is old, simple to state, and well known;
- the conjecture was not marginal folklore but a core belief in combinatorial geometry;
- the counterexample is an infinite family, not a small brute-force configuration;
- the bridge uses unexpectedly deep mathematics;
- the result was verified, digested, and publicly discussed by external mathematicians.

That makes it different from most AI-math headlines. It is a signal that when models can sustain long-chain reasoning, recode problems across fields, and propose checkable new constructions, their role in research can shift from assistant to candidate discoverer.

But candidate discoverers still need human mathematicians. Scientific progress is not complete at the moment a model outputs a proof. It becomes progress through expert verification, conceptual rewriting, community understanding, and follow-on work.

Perhaps that is the most important lesson: AI does not make mathematics less human. It makes human judgment, taste, and interpretation more valuable.
