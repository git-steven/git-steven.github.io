---
title: "🎚️ Autonomy is a spectrum, not a switch"
excerpt: "Right-size the model, right-size the autonomy, and keep the people who can tell the difference."
version: "1.00"
date: 2026-10-15
author: steven
header:
  teaser: https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-banner.jpg
categories: [architecture, ai]
tags: [ai, llm, software-engineering, hitl, hotl]
toc: true
---

<img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-banner.jpg" alt="Engineering First">

**Right-size the model, right-size the autonomy, and keep the people who can tell the difference.**

## 📝 Introduction

Steven B Miers · October 15, 2026 · v1.00

Earlier this year I watched a team ship a feature they had generated end to end with an AI assistant. It worked on the first day. It was also, in effect, one object: the request handler parsed the input, validated it, queried the database, built the response, and sent the notification, and every piece reached into the internals of every other piece to do it. The first change request — a second notification channel — could not be made without touching all of it. The generated tests, which tested the implementation rather than the behavior, all broke with it. In the end the feature was rewritten by hand, by the one person on the team who could see why. The code had never been wrong. It was plausible, it passed, and it was coupled so tightly that nothing in it could be changed.

That is the failure I keep seeing, and it is not the tool's fault. The tool did what it was asked. Nobody in the loop knew what to ask for — or that it mattered.

## 🧭 Where I'm standing

<img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-portrait.jpg" width="350px" alt="Steven B Miers"/>

I use AI every day — for research, for learning, for keeping my old Land Rover running, for code, and for running nebulous designs past it before I inflict them on humans. This is not a bash on AI.

It is a position from someone who has built the models. I have trained and shipped production neural networks since 2007 — a patented behavioral-prediction platform, CNN and RNN models, NLP pipelines with custom-trained language models for named-entity recognition and list/series detection, and a human-in-the-loop curation system that fed corrections back into training. More recently, LLM-based systems and the agents built on them. I understand how neural networks and LLMs work — as math I have implemented, not as a slogan.

![Fig. 1](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-fig-1-devolution.png)

__Fig. 1 — Judgment degrades gradually, then cannot be measured.__ Read left to right as time: experienced engineers leave, and the junior pipeline that would have replaced them is cut. *Judgment* is the ability to tell a good decision from a merely plausible one; it is built by working alongside people who hold *the standard*.

That is why the current reflex worries me: reach for the largest LLM for every problem, run it as autonomously as the demo allows, and treat the people who can tell good output from plausible output as overhead. The measurements do not support it. METR's 2025 randomized trial found experienced developers took **19% longer** with AI on their own codebases — and believed afterward they had been 20% faster. Stack Overflow's 2025 survey: trust in AI accuracy down to **29%**, and the top frustration, for 66% of developers, is answers that are almost right. Anthropic's own trial: developers who learned a new library with AI then scored **50% versus 67%** on a comprehension quiz without it. The vendor published that against its own interest.

## 📜 Coding was never the hard part

The lesson has nothing to do with the tool: **writing code ≠ software engineering.** Coding isn't the hard part. It never was. The hard part is knowing what to build, what to leave out, what breaks at 3 a.m., and which requirement the customer forgot to mention. Programming languages exist because English is a terrible specification language; a spec complete enough to become correct software *is* the software, in a worse notation.

A good engineer fills the gaps — talks to the principals, applies intuition, asks the question nobody wrote down. A model fills gaps too. Sometimes it asks. Sometimes it grows a third arm.

![Fig. 2](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-fig-3-extra-arms.png)

__Fig. 2 — The third arm: a simple grid the model was asked to draw, and what came back.__ The spec: a 9×5 lattice, every node connected to at most four neighbors. __Green:__ asked for and received. __Red squares and dashed lines:__ three nodes, and their connections, never delivered. __Light blue:__ six to ten extra limbs on each of five nodes that nothing asked for, each ending in an __orange ×__ — a dead end. __Red circles:__ three nodes invented outright. Thirty-seven of forty-five specified nodes are exactly right, and at a glance the figure looks finished. That is the shape of "almost right," and none of it is visible unless you are holding the spec.

## 🛠️ Build better systems with AI

<img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/ai-1st-eng-build-better-systems.jpg" width="450px" alt="Build better systems"/>

None of this argues for less AI. It argues for AI with people who understand it in charge.

### 🎚️ Autonomy is a spectrum, not a switch

The question is never "automate or don't." It is how much judgment the task needs, and who supplies it.

- **Human-in-the-loop** where judgment is load-bearing: the model proposes, a person who knows the standard decides.
- **Human-on-the-loop** where supervision is enough: the model acts, a person watches the aggregate and steps in.
- **Fully autonomous** only where the evidence has earned it — measured, over time, on your own work, not on the vendor's benchmark.

Move along that spectrum as the record justifies, and no faster. And every human override is labeled training data from your own experts — keep it. It is the most valuable data you own, and it only exists while those experts are still in the room.

### 🎯 Hire for judgment

"Understands how the model works" is not a nice-to-have. It is the qualification. "Uses AI" describes everyone; the judgment above the tool is what is scarce.

The model does not remove the work. It moves it — from writing to reviewing — and reviewing requires someone who knows what good looks like.

### 🧯 Right-size the model

**In the software**

- **Reach for the algorithm first.** If a problem can be solved algorithmically — or with a homegrown, public, or purchased ML model — an LLM is overkill. You get deterministic results, better performance, and a smaller bill. *Do* use an LLM when you actually need one: generative work, or a chat interface over a customer knowledge base.
- **Right-size the model, and consider on-prem.** Most business work doesn't need a genius in a hyperscale data center — it needs a clerk who doesn't make things up. A small model on a box you own keeps the data home, keeps the bill flat, and sips power instead of guzzling it.

**When writing code**

- **Don't forget how to code.** Skills wane, and engineering judgment goes with them. Generating code *feels* productive right up until something breaks, and then fixing it — or coaxing the model into fixing it — is like chewing rocks.
- **Use AI as a reference.** It is excellent at researching problems, algorithms, and architecture: which libraries, which services, where each should run, how the concerns should be separated.
- **Know the fundamentals.** Data structures, algorithms, database design, refactoring, minimizing dependencies. The model knows them too; you need to know when it's wrong.
- **Learn the anti-patterns and never do them.** Learn the design patterns and when to apply them — and remember the golden hammer, from the era when engineers tried to solve every problem with a pattern.

**Software engineering principles**

A few that have outlived every framework fad: separation of concerns; don't repeat yourself; loose coupling, high cohesion; YAGNI; fail loudly; make it work, make it right, make it fast — in that order. None of these is about typing. That's the point.

### 🤝 Working with agents

An agent is an LLM with tools, a loop, and a job description. I have run the experiment of handing a crew of them a real service, pages of house rules, and instructions to check each other's work: what came back compiled, passed its own tests, and needed a rewrite. What has held up since:

- **One agent, one job.** Separation of concerns applies to agents too. A planner, an implementer, a test writer, a reviewer — each with its own instructions, its own tools, and only the context its job needs. An agent asked to design, build, test, and judge its own work grades itself, and it is generous.
- **Let agents review agents — and know what that buys you.** A reviewer agent with a different brief catches the mechanical things: the missing test, the leaked credential, the rule it was explicitly told to check. It does not catch a wrong boundary, a schema the model quietly worked around, or a third arm — those need someone who holds the standard. Treat agent review as a pre-filter on the human reviewer's time, never as the review.
- **Skills over prompts.** Put how you do things — the review checklist, the migration recipe, the house style — in reusable, versioned skill files the agent loads when the task matches, instead of retyping it every session. Treat them like code: in the repo, reviewed, tested.
- **House rules: few, concrete, enforced.** The rules that got ignored said "Always" and "Never." The rules that hold are short (a page, not pages), concrete ("one class per file, one return point," not "write clean code"), stated once in the repository's agent-instructions file where every agent reads them, and checked by something that is not the model — a linter, a test, a CI gate. A rule nothing can check is a rule the model follows most of the time; put a human on the cases where most is not enough.
- **Make the principles executable.** Don't ask an agent to honor separation of concerns, DRY, loose coupling, or YAGNI — give it the test that fails when it doesn't: a duplication detector, a dependency rule, an architecture test, a coverage gate. The agent will make it pass, and the number becomes the record.
- **Small tasks, short loops.** One task, one change, reviewed before the next. Drift compounds with context length; nothing in Fig. 1 happens in a two-hundred-line pull request.
- **Feed the overrides back.** Every change a reviewer rejects, and why, goes into the rules and the skills. That is the loop that improves the crew — and it only runs while the reviewer is in the room.

### 📏 Measure what vendors don't publish

Duplication, churn, coupling, stability, review load. If AI is helping your codebase, those numbers will say so first — and they will say so before the incident report does.

Software engineers are expensive for a reason, and the reason has not changed. What changed is that we built a machine that produces plausible software faster than anyone can check it. The fix is not less of the machine. It is keeping the checkers, and putting them in charge of how far it runs.

---
Version 1.00 · October 2026
