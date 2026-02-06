# Introducing GPT-5.3-Codex

> Source: https://openai.com/index/introducing-gpt-5-3-codex/

![Benchmark Chart](images/benchmark-chart.webp)

We're introducing a new model that unlocks even more of what Codex can do: GPT‑5.3-Codex, the most capable agentic coding model to date. The model advances both the frontier coding performance of GPT‑5.2-Codex and the reasoning and professional knowledge capabilities of GPT‑5.2, together in one model, which is also 25% faster. This enables it to take on long-running tasks that involve research, tool use, and complex execution. Much like a colleague, you can steer and interact with GPT‑5.3-Codex while it's working, without losing context.

GPT‑5.3‑Codex is our first model that was instrumental in creating itself. The Codex team used early versions to debug its own training, manage its own deployment, and diagnose test results and evaluations—our team was blown away by how much Codex was able to accelerate its own development.

With GPT‑5.3-Codex, Codex goes from an agent that can write and review code to an agent that can do nearly anything developers and professionals can do on a computer.

## Frontier agentic capabilities

GPT‑5.3-Codex sets a new industry high on SWE-Bench Pro and Terminal-Bench, and shows strong performance on OSWorld and GDPval, four benchmarks we use to measure coding, agentic and real-world capabilities.

GPT‑5.3-Codex achieves state-of-the-art performance on SWE-Bench Pro, a rigorous evaluation of real-world software engineering. Where SWE‑bench Verified only tests Python, SWE‑Bench Pro spans four languages and is more contamination‑resistant, challenging, diverse and industry-relevant. It also far exceeds the previous state-of-the-art performance on Terminal-Bench 2.0, which measures the terminal skills a coding agent like Codex needs. Notably, GPT‑5.3‑Codex does so with fewer tokens than any prior model, letting users build more.

Combining frontier coding capabilities, improvements in aesthetics, and compaction results in a model that can do striking work, building highly functional complex games and apps from scratch over the course of days. To test the model's web development and long-running agentic capabilities, we asked GPT‑5.3‑Codex to build us two games: version two of the racing game from the [Codex app launch](https://openai.com/index/introducing-the-codex-app/), and a diving game. Using the develop web game skill and preselected, generic follow-up prompts like "fix the bug" or "improve the game", GPT‑5.3-Codex iterated on the games autonomously over millions of tokens.

GPT‑5.3-Codex also better understands your intent when you ask it to make day-to-day websites, compared to GPT‑5.2-Codex. Simple or underspecified prompts now default to sites with more functionality and sensible defaults, giving you a stronger starting canvas to bring your ideas to life.

For example, we asked GPT‑5.3-Codex and GPT‑5.2-Codex to build two landing pages below. GPT‑5.3-Codex automatically showed the yearly plan as a discounted monthly price, making the discount feel clear and intentional, instead of multiplying the yearly total. It also made an automatically transitioning testimonial carousel with three distinct user quotes rather than one, resulting in a page that feels more complete and production-ready by default.

Software engineers, designers, product managers, and data scientists do far more than generate code. GPT‑5.3‑Codex is built to support all of the work in the software lifecycle—debugging, deploying, monitoring, writing PRDs, editing copy, user research, tests, metrics, and more. Its agentic capabilities go beyond software, helping you build whatever you want to build—whether it's slide decks or analyzing data in sheets.

With custom skills similar to those used for our previous GDPval results, GPT‑5.3‑Codex also shows strong performance on professional knowledge work as measured by [GDPval](https://openai.com/index/gdpval/), matching GPT‑5.2. GDPval is an evaluation OpenAI released in 2025 that measures a model's performance on well‑specified knowledge‑work tasks across 44 occupations. These tasks include things like making presentations, spreadsheets, and other work products.

OSWorld is an agentic computer-use benchmark where the agent has to complete productivity tasks in a visual desktop computer environment. GPT‑5.3-Codex demonstrates far stronger computer use capabilities than previous GPT models.

Together, these results across coding, frontend, and computer-use and real-world tasks show that GPT‑5.3-Codex isn't just better at individual tasks, but marks a step change toward a single, general-purpose agent that can reason, build, and execute across the full spectrum of real-world technical work.

## An interactive collaborator

As model capabilities become more powerful, the gap shifts from what agents are capable of doing to how easily humans can interact with, direct and supervise many of them working in parallel. The Codex app makes managing and directing agents much easier, and now with GPT‑5.3-Codex it's more interactive. With the new model, Codex provides frequent updates so you stay appraised of key decisions and progress as it works. Instead of waiting for a final output, you can interact in real time—ask questions, discuss approaches, and steer toward the solution. GPT‑5.3-Codex talks through what it's doing, responds to feedback, and keeps you in the loop from start to finish.

Enable steering while the model works in the app in Settings > General > Follow-up behavior.

## How we used Codex to train and deploy GPT‑5.3-Codex

The recent rapid Codex improvements build on the fruit of research projects spanning months or years across all of OpenAI. These research projects are being accelerated by Codex, with many researchers and engineers at OpenAI describing their job today as being fundamentally different from what it was just two months ago. Even early versions of GPT‑5.3-Codex demonstrated exceptional capabilities, allowing our team to work with those earlier versions to improve training and support the deployment of later versions.

Codex is useful for a very broad range of tasks, making it difficult to fully enumerate the ways in which it helps our teams. As some examples, the research team used Codex to monitor and debug the training run for this release. It accelerated research beyond debugging infrastructure problems: it helped track patterns throughout the course of training, provided a deep analysis on interaction quality, proposed fixes and built rich applications for human researchers to precisely understand how the model's behavior differed compared to prior models.

The engineering team used Codex to optimize and adapt the harness for GPT‑5.3-Codex. When we started seeing strange edge cases impacting users, team members used Codex to identify context rendering bugs, and root cause low cache hit rates. GPT‑5.3-Codex is continuing to help the team throughout the launch by dynamically scaling GPU clusters to adjust to traffic surges and keeping latency stable.

During alpha testing, one researcher wanted to understand how much additional work GPT‑5.3-Codex was getting done per turn and the associated difference in productivity. GPT‑5.3-Codex came up with several simple regex classifiers to estimate frequency of clarifications, positive and negative user responses, progress on the task, and then ran them scalably over all session logs and produced a report with its conclusion. People building with Codex were happier as the agent was better understanding their intent and made more progress per turn, with fewer clarifying questions.

Due to GPT‑5.3-Codex being so different from its predecessors, the data from alpha testing exhibited numerous unusual and counter-intuitive results. A data scientist on the team worked with GPT‑5.3-Codex to build new data pipelines and visualize the results much more richly than our standard dashboarding tools enabled. The results were co-analyzed with Codex, which concisely summarized key insights over thousands of data points in under three minutes.

Individually, all of these tasks are interesting examples of how Codex can help researchers and product builders. Taken together, we found that these new capabilities resulted in powerful acceleration of our research, engineering, and product teams.

## Securing the cyber frontier

Over recent months, we've seen meaningful gains in model performance on cybersecurity tasks, benefiting both developers and security professionals. In parallel, we've been [preparing strengthened cyber safeguards](https://openai.com/index/strengthening-cyber-resilience/) to support defensive use and broader ecosystem resilience.

GPT‑5.3-Codex is the first model we classify as [High capability](https://openai.com/index/gpt-5-3-codex-system-card/) for cybersecurity-related tasks under our [Preparedness Framework](https://openai.com/index/updating-our-preparedness-framework/), and the first we've directly trained to identify software vulnerabilities. While we don't have definitive evidence it can automate cyber attacks end-to-end, we're taking a precautionary approach and deploying our most comprehensive cybersecurity safety stack to date. Our mitigations include safety training, automated monitoring, trusted access for advanced capabilities, and enforcement pipelines including threat intelligence.

Because cybersecurity is inherently dual-use, we're taking an evidence-based, iterative approach that accelerates defenders' ability to find and fix vulnerabilities while slowing misuse. As part of this, we're launching [Trusted Access for Cyber](https://openai.com/index/trusted-access-for-cyber/), a pilot program to accelerate cyber defense research.

We're investing in ecosystem safeguards such as expanding the private beta of [Aardvark](https://openai.com/index/introducing-aardvark/), our security research agent, as the first offering in our suite of Codex Security products and tools, and partnering with open-source maintainers to provide free codebase scanning for widely used projects such as Next.js—where a security researcher used Codex to find vulnerabilities [disclosed](https://vercel.com/changelog/summaries-of-cve-2025-59471-and-cve-2025-59472) last week.

Building on our $1M Cybersecurity Grant Program launched in 2023, we're also committing $10M in API credits to accelerate cyber defense with our most capable models, especially for open source software and critical infrastructure systems. Organizations engaged in good-faith security research can apply for API credits and support through our [Cybersecurity Grant Program](https://openai.com/index/openai-cybersecurity-grant-program/).

## Availability & details

GPT‑5.3-Codex is available with paid ChatGPT plans, everywhere you can use Codex: the app, CLI, IDE extension and web. We are working to safely enable API access soon.

With this update, we are also now running GPT‑5.3-Codex 25% faster for Codex users, thanks to improvements in our infrastructure and inference stack, resulting in faster interactions and faster results.

GPT‑5.3-Codex was co-designed for, trained with, and served on NVIDIA GB200 NVL72 systems. We are grateful to NVIDIA for their partnership.

## What's next

With GPT‑5.3-Codex, Codex is moving beyond writing code to using it as a tool to operate a computer and complete work end to end. By pushing the frontier of what a coding agent can do, we're also unlocking a broader class of knowledge work—from building and deploying software to researching, analyzing, and executing complex tasks. What started as a focus on being the best coding agent has become the foundation for a more general collaborator on the computer, expanding both who can build and what's possible with Codex.

## Related Images

![System Card Art](images/system-card-art.webp)

![Codex Landing Page](images/codex-landing-page.webp)

![GPT-5.2 Codex Art Card](images/gpt-5.2-codex-artcard.webp)

## Benchmark Results

| Model | SWE-Bench Pro (Public) | Terminal-Bench 2.0 | OSWorld-Verified | GDPval (wins or ties) | Cybersecurity CTF | SWE-Lancer IC Diamond |
|-------|------------------------|-------------------|------------------|----------------------|-------------------|----------------------|
| GPT-5.3-Codex (xhigh) | 56.8% | 77.3% | 64.7% | 70.9% | 77.6% | 81.4% |
| GPT-5.2-Codex (xhigh) | 56.4% | 64.0% | 38.2% | - | 67.4% | 76.0% |
| GPT-5.2 (xhigh) | 55.6% | 62.2% | 37.9% | 70.9% (high) | 67.7% | 74.6% |
