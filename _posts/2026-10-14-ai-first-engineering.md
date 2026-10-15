---
title: "🤖 AI-first “engineering”"
excerpt: "A giant leap forward in the devolution of building software."
version: "7.05"
date: 2026-10-14
author: steven
header:
  teaser: https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-banner.jpg
categories: [architecture, ai]
tags: [ai, llm, software-engineering, hitl, data-centers]
toc: true
published: false
---

<img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-banner.jpg" alt="Engineering First">

**A giant leap forward in the devolution of building software.**

## 📝 Introduction

Steven B Miers · October 14, 2026 · v7.05

Last month I handed a frontier model a real task — a service with state, concurrency, and a database that already had a schema and full referential integrity. I gave it pages of house rules — explicit, consistent, none in conflict with another — and a crew of differently defined agents working together and checking each other's work. The rules used words like "Always" and "Never." At least a third of them were ignored. What came back compiled, passed its own tests, *and needed a total rewrite*. The software equivalent of an AI image with three arms.

The industry is laying off the engineers who can see the third arm, and hiring for people who can't. That is not efficiency. That is the first wave of the AI plague — people getting dumber, and then dumber-er — and software is only where it shows up first.

## 🧭 Where the author stands

<img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-portrait.jpg" width="350px" alt="Steven B Miers"/>

This is not a bash on AI. I use it every day — for research, for learning, for keeping my old Land Rover running, even for code, and for running nebulous designs past it before I inflict them on humans.

So you know which kind of skeptic you are reading: I have trained and shipped production neural networks since 2007 — a patented behavioral-prediction platform, CNN and RNN models, NLP pipelines with custom-trained language models for named-entity recognition and list/series detection, and a human-in-the-loop curation system that fed corrections back into training. More recently, generative AI: LLM-based systems and the agents built on them.

I understand how neural networks and LLMs work — as math I have implemented, not as a slogan. Interviewers find that "interesting." Not a qualification; they want AI *users*, not people who can build the models. Hold that thought.

![Fig. 1](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-fig-1-devolution.png)

__Fig. 1 — Judgment degrades gradually, then cannot be measured.__ Read left to right as time: experienced engineers leave, and the junior pipeline that would have replaced them is cut. *Judgment* is the ability to tell a good decision from a merely plausible one; it is built by working alongside people who hold *the standard*.

### Marks

Each mark is one engineering decision: a design call, a review comment, a rejected change.

- **Horizontal, white** — checked by someone who knows the standard.
- **Tilted** — drifted, and nobody caught it.
- **Light blue** — accepted on the model's say-so.
- **Gap** — a decision nobody made at all; the model filled it.

### Lines

- **Gold, along the bottom** — the standard: what correct looks like here — the review bar, the architecture rules, the reasons behind the conventions; mostly unwritten, and held by the people who learned it doing the work. It thins and fades as those people leave.
- **Purple diagonal** — entropy: disorder, increasing the whole way.

### Phases, left to right

- **Judgment retained (green)** — people who know the standard check every decision against it.
- **Judgment fades (orange)** — they leave and are not replaced; the standard is applied less and less, and drift begins to pass unnoticed.
- **Judgment lost (red)** — nobody left knows the standard, so drift can no longer be seen as drift.

## 🎓 AI is a poor engineer

It does fine with algorithms. I have yet to receive anything complex that did not need a rewrite. That is not one architect's anecdote:

- **Experienced developers got slower.** METR's 2025 randomized trial — 16 seasoned developers, 246 real tasks in their own repos — found they took **19% longer** with AI, and afterward *still believed* they had been 20% faster.
- **Nearly half the code is insecure.** Veracode, 100+ models, 80+ tasks: OWASP Top 10 vulnerabilities **45% of the time**, 72% in Java. Newer, larger models were no better.
- **"Almost right" is the product.** Stack Overflow 2025: 84% of developers use AI; trust in its accuracy fell to **29%**; the top frustration (66%) is solutions that are almost right but not quite.
- **It copies instead of refactoring.** GitClear, 211 million changed lines: duplicate blocks up ~8x in a year; refactored code down from ~24% to 3.8%.
- **The work moved downstream.** Faros AI, 22,000 developers across 4,000 teams: PRs merged with no human review up **76%**, time in QA up 300%, monthly incidents up 125%. Google's DORA still finds AI adoption correlates negatively with delivery stability.

Would you hire an engineer who hallucinated several times a day? Who invented an API that does not exist, cited a library version that was never released, and then passed the tests they wrote for their own code — all with complete confidence? That is the colleague being hired at scale. The person who would have caught it is the one being shown the door.

The model does not remove the work. It moves it — from writing to reviewing. And reviewing requires someone who knows what good looks like. How do you build quality software if you don't know what that is?

## 📜 Coding was never the hard part

*"Using this technology, anyone can write software."* We've heard this before. **Six** times:

![Fig. 2](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-fig-2-timeline.png)

__Fig. 2 — Sixty-five years of the same promise.__ Each dot is a technology sold, at launch, as the end of programmers. Time runs left to right.

### 🧾 The six promises

- **1959 — COBOL.** English-like syntax so managers could write programs. Programmers wrote COBOL for the next sixty-five years.
- **1980s — 4GLs and CASE tools.** Declare the result; the tool generates the system. The output was unmaintainable; developers rewrote it.
- **2001 — UML / MDA.** Draw the model, generate the code. Programmers drew the models and fixed the code.
- **2006 — BDD / Cucumber.** Stakeholders write executable `Given / When / Then` specs. Developers wrote the specs.
- **2014 — Low-code / no-code.** "Citizen developers" drag-and-drop their own apps. It works until the first requirement the components didn't anticipate; then a developer finishes the app — or inherits it.
- **2024 — LLMs (orange).** "Nobody has to program" (Jensen Huang, Nvidia, Feb 2024). "AI writes 90% of code in six months, essentially all of it in a year" (Dario Amodei, Anthropic, Mar 2025).

The gaps between promises are shrinking. The outcome has not changed.

Same promise every time: describe what you want in something close to English and the programmers become optional. Every time, programmers wrote it anyway.

BDD is the exact rehearsal for today. Dan North coined it in 2006; Cucumber promised product owners would write `Given / When / Then` scenarios and the software would follow. Very few non-programmers could write a scenario that meant anything, so developers wrote them — in a stilted dialect of English slower to produce than the code it described. The industry noticed and quietly moved on.

The lesson has nothing to do with the tool: **writing code ≠ software engineering.** Coding isn't the hard part. It never was. The hard part is knowing what to build, what to leave out, what breaks at 3 a.m., and which requirement the customer forgot to mention. Programming languages exist because English is a terrible specification language; a spec complete enough to become correct software *is* the software, in a worse notation.

A good engineer fills the gaps — talks to the principals, applies intuition, asks the question nobody wrote down. A model fills gaps too. Sometimes it asks. Sometimes it grows a third arm.

![Fig. 3](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-fig-3-extra-arms.png)

__Fig. 3 — Plausible everywhere, wrong where only a reviewer would look.__ The spec was simple: a 9×5 lattice, every node connected to at most four neighbors. __Green dot:__ asked for and received. __Red square:__ asked for and never delivered — three nodes are missing, and the dashed red lines are the connections that went with them. __Light blue:__ structure the model generated that nothing asked for — six to ten extra limbs on each of five nodes (ringed in blue). __Orange ×:__ where each of those limbs ends — a dead end, structure that goes nowhere and does nothing. __Red circle:__ a node the model invented outright — three of them — attached to nothing that was specified, two of them sprouting dead ends of their own. Thirty-seven of forty-five specified nodes are exactly right, and at a glance the figure looks finished. That is the shape of "almost right": the model fails in every direction at once — it quietly leaves out part of what was asked for, adds to what it did deliver, and invents things that were never on the drawing — and none of it is visible unless you are holding the spec.

## 🧠 Dumber, then dumber-er

Future programmers, we are told, will be technicians who consult a model and set the software's parameters in English. Fine. Who teaches them what good looks like?

- **The pipeline is being cut.** Stanford, payroll data on 25 million workers: employment of software developers aged 22–25 is down **~20% since late 2022**.
- **Learning with AI teaches less.** Anthropic's own randomized trial (January 2026): developers who learned a new library with AI wrote better code in the session, then scored **50% versus 67%** on a comprehension quiz without it. The vendor published that against its own interest.
- **Confidence replaces thinking.** Microsoft Research and Carnegie Mellon, 319 knowledge workers: the more someone trusted the AI, the less critical thinking they applied.

Read those three together and the word is not "productivity." The word is atrophy. Critical thinking is a muscle, and the measurements show it going slack in real time: the more people trust the model, the less they think; the less they think, the less able they are to notice when the model is wrong; and the less they notice, the more they trust it. That loop runs in one direction, and nothing inside it ever calls for a human who knows better. We are not augmenting judgment. We are training people out of the habit of having any.

Senior judgment is made out of junior work. Cut the junior work and in ten years nobody in the room knows what the model got wrong — including the model. And this will not stay in software. It is coming for anything technical, and anything creative.

## 😶 The grief nobody names

It is a strange time to work in tech. People who spent ten, twenty, thirty years getting excellent at a craft are being told it no longer matters. That is not a small thing. That is an identity crisis at scale, and companies are making it worse — laying off people they deem "not AI native" and hiring from scratch, instead of investing in the ones who already have the judgment, the taste, and the institutional knowledge that cannot be taught quickly. Those are the hardest things to find. They are being thrown away.

<img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-cartoon.jpg" alt="Exit interview" width="350"/>

__Exit interview.__ Greg could see the third arm. That was the problem.

- **The body count is official.** Challenger, Gray & Christmas counted **54,836** US layoffs blamed on AI in 2025; by spring 2026 AI was the most-cited reason of all — and companies have started *not* saying so, because it spooks the survivors.
- **The big names aren't shy.** Amazon shed ~30,000 corporate roles in two rounds, citing "the most transformative technology we've seen since the Internet." Salesforce took support from 9,000 heads to 5,000 and thanked its AI agent. Shopify now makes teams prove AI *can't* do a job before they may hire a human for it.
- **Then comes the sheepish rehire.** Klarna swapped 700 agents' worth of work for AI, found it "lower quality, and that's not sustainable," and is hiring humans again. Orgvue asked 1,163 senior leaders about their AI layoffs: **55% call it the wrong decision**, and a third have already rehired. Forrester expects half of all AI-attributed layoffs to be quietly reversed — often offshore, or at lower pay.

This is not only happening to juniors. AI is putting exceptional engineers out of work — including the ones who embraced it. I have thirty years as an architect and engineer who still writes code, uses these tools daily, and understands how they work under the hood. I have been told the last part is interesting — but what they are hiring for is "AI-first engineering," which turns out to require no AI knowledge beyond a subscription to Claude or ChatGPT. If the only qualification is "uses AI," you have described everyone. The judgment above the tool is what is scarce, and it is what is being discarded.

### 🔥 The bill nobody itemizes

The replacement for that judgment is a data center. Several hundred of them — and the vendors' own reports say what they cost.

- **The grid.** The IEA expects data centers to more than double their electricity by 2030 — **~945 TWh**, more than Japan uses today — with 15–27 GW of on-site gas plants built to feed them, mostly in the US. AI-focused data centers grew 50% in 2025 alone. Lawrence Berkeley National Laboratory puts US data centers at 4.4% of the nation's electricity in 2023 and **6.7–12% by 2028**.
- **The water.** US data centers drank 17 billion gallons for cooling in 2023; LBNL projects 38–73 billion by 2028. Google alone swallowed **10.9 billion gallons** in 2025 — up 34% in a year, more than double 2021.
- **The vendors' own report cards.** Google's 2026 environmental report: emissions up **18% in a year** — its biggest jump ever — and **81% above the 2019 baseline** it had pledged to halve by 2030; electricity use up 37%. Microsoft's FY2025 report: **20 million tonnes** of CO₂e, up 25% in a year and up from 13 million in 2020, the baseline for its carbon-negative pledge. Named culprit, both times: the AI buildout.
- **Downwind.** xAI ran its Memphis cluster on 35+ unpermitted methane turbines — 400+ MW, 2,000+ tons of nitrogen oxides a year — next to a neighborhood whose cancer risk was already four times the national average.
- **And the pedal is down.** OpenAI's $500B Stargate, Anthropic's $50B of US data centers, big-tech capital spending past $400B in 2025 and climbing. Claude, ChatGPT, Gemini — every one of them lives in this bill.

None of this appears on the invoice for a seat license. It is paid by whoever lives downwind, and billed to a decade no one in the room will be around to answer for.

## 🧭 What I would do instead

<img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-build-better-systems.jpg" width="450px" alt="Build better systems">

None of this argues for less AI. It argues for AI with people who understand it in charge.

### 🎯 Hire for judgment

"Understands how the model works" is not interesting. It is the qualification.

### 🎚️ Autonomy is a spectrum, not a switch

Human-in-the-loop where judgment is load-bearing; human-on-the-loop where supervision is enough; fully autonomous only where the evidence has earned it. Every human override is labeled training data from your own experts — keep it.

### 🧯 Don't overuse the LLM

**In the software**

- **Reach for the algorithm first.** If a problem can be solved algorithmically — or with a homegrown, public, or purchased ML model — an LLM is overkill. You get deterministic results, better performance, and a smaller bill, including the [hidden costs](#the-bill-nobody-itemizes) the vendors never itemize. *Do* use an LLM when you actually need one: generative work, or a chat interface over a customer knowledge base.
- **Right-size the model, and consider on-prem.** Most business work doesn't need a genius in a hyperscale data center — it needs a clerk who doesn't make things up. A small model on a box you own keeps the data home, keeps the bill flat, and sips power instead of guzzling it.

**When writing code**

- **Don't forget how to code.** Skills wane, and engineering judgment goes with them. Writing code is [the easy part](#coding-was-never-the-hard-part); generating it *feels* productive right up until something breaks, and then fixing it — or coaxing the model into fixing it — is like chewing rocks.
- **Use AI as a reference.** It is excellent at researching problems, algorithms, and architecture: which libraries, which services, where each should run, how the concerns should be separated.
- **Know the fundamentals.** Variables, loops, conditionals, data structures, algorithms, visibility, database design, refactoring, minimizing dependencies. The model knows them too; you need to know when it's wrong.
- **Learn the [anti-patterns](https://a.co/d/0bVOAzCe) and never do them.** Learn the [design patterns](https://a.co/d/05eTZMg7) and when to apply them — and remember the [golden hammer](https://en.wikipedia.org/wiki/Law_of_the_instrument#Computer_programming), from the era when engineers tried to solve every problem with a pattern.

**Software engineering principles**

A few that have outlived every framework fad:

- **Separation of concerns** — one thing does one job. The code that bills the customer shouldn't also be the code that emails them.
- **Don't repeat yourself** — [copy-and-paste programming](https://en.wikipedia.org/wiki/Copy-and-paste_programming) is how one bug becomes twelve, and then more, as the copies get fixed in some places and not others. Every duplicate raises the entropy, and the project slowly morphs from a brick building into a shack on sand.
- **Loose coupling, high cohesion** — modules should be good neighbors, not roommates who share a toothbrush.
- **YAGNI** — don't build it until you actually need it. Most "we'll need this later" code is a monument to optimism.
- **Fail loudly** — a crash you can see beats a wrong answer you can't.
- **Make it work, make it right, make it fast** — in that order. Nobody has ever regretted skipping premature optimization.

None of these is about typing. That's the point.

### 📏 Measure what vendors don't publish

Duplication, churn, coupling, stability, review load. If AI is helping your codebase, those numbers will say so first.

Software engineers are expensive for a reason, and the reason has not changed. What changed is that we built a machine that produces plausible software faster than anyone can check it — and then started laying off the checkers.

## 📚 References

- METR — Becker, Rush, Barnes & Rein, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*, July 10, 2025. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- Veracode, *2025 GenAI Code Security Report*, July 30, 2025 (updated Oct 2025). https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/
- Stack Overflow, *2025 Developer Survey — AI*. https://survey.stackoverflow.co/2025/ai
- GitClear, *AI Copilot Code Quality: 2025 Data Suggests 4x Growth in Code Clones* (Feb 2025) and *The Maintainability Gap: 2026 AI Code Quality Research*. https://www.gitclear.com/ai_assistant_code_quality_2025_research · https://www.gitclear.com/the_ai_code_quality_maintainability_gap
- Faros AI, *AI Engineering Report Q3 2026: The Speed Trap*, Sept 18, 2026. https://www.faros.ai/blog/ai-speed-trap-takeaways
- Google Cloud / DORA, *2024 Accelerate State of DevOps* and *2025 State of AI-Assisted Software Development*. https://dora.dev/research/
- Shen & Tamkin (Anthropic), *How AI assistance impacts the formation of coding skills*, Jan 29, 2026. https://www.anthropic.com/research/AI-assistance-coding-skills
- Lee et al. (Microsoft Research / Carnegie Mellon), *The Impact of Generative AI on Critical Thinking*, CHI 2025. https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/
- Brynjolfsson, Chandar & Chen (Stanford Digital Economy Lab), *Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence*, Aug 2025, rev. 2026. https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/
- Dan North, *Introducing BDD*, Better Software, March 2006. https://dannorth.net/introducing-bdd/
- Challenger, Gray & Christmas, *2025 Year-End Challenger Report* and 2026 monthly reports. https://www.challengergray.com/blog/2025-year-end-challenger-report-highest-q4-layoffs-since-2008-lowest-ytd-hiring-since-2010/
- Amazon (Beth Galetti memo, Oct 28, 2025; Jan 2026 cuts) and Salesforce (Benioff, *The Logan Bartlett Show*, Aug 2025) as reported by CNBC and The Register. https://www.theregister.com/2025/09/02/salesforce_4000_jobs_ai
- Shopify (Tobi Lütke memo, Apr 2025) as reported by Fortune, Apr 8, 2025. https://fortune.com/2025/04/08/shopify-ceo-ai-automation-no-new-hires-tech-jobs/
- Klarna reversal — Forbes / Bloomberg, May 18, 2025. https://www.forbes.com/sites/quickerbettertech/2025/05/18/
- Orgvue, *55% of businesses admit wrong decisions in making employees redundant when bringing AI into the workforce*, Apr 29, 2025; follow-up Mar 12, 2026. https://www.orgvue.com/news/55-of-businesses-admit-wrong-decisions-in-making-employees-redundant-when-bringing-ai-into-the-workforce/
- Forrester, *Predictions 2026: The Future of Work*, Oct 2025, as reported by The Register, Oct 29, 2025. https://www.theregister.com/software/2025/10/29/ai-layoffs-to-backfire-half-quietly-rehired-at-lower-pay/937713
- IEA, *Energy and AI* (Apr 2025) and *Key Questions on Energy and AI* (2026). https://www.iea.org/reports/energy-and-ai · https://www.iea.org/reports/key-questions-on-energy-and-ai
- Shehabi et al. (Lawrence Berkeley National Laboratory), *2024 United States Data Center Energy Usage Report*, Dec 2024. https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers
- Google, *2026 Environmental Report*, July 2, 2026 (as reported by Axios and ESG Dive). https://www.esgdive.com/news/googles-emissions-continue-to-climb-due-to-ai-buildout/824373/
- Microsoft, *2026 Environmental Sustainability Report* (FY2025), July 10, 2026 (as reported by The Register and DCD). https://www.theregister.com/on-prem/2026/07/10/ai-driven-datacenter-builds-drive-microsofts-emissions-up-a-quarter-in-one-year/5269924
- Southern Environmental Law Center / NAACP, Clean Air Act notice of intent to sue xAI, June 2025. https://www.selc.org/news/xai-built-an-illegal-power-plant-to-power-its-data-center/

---
Version 7.05 · October 2026
