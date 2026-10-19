---
title: "🌈 Autonomy is a spectrum, not a switch"
excerpt: "Right-size the model, right-size the autonomy, and keep the people who can tell the difference."
version: "1.06"
date: 2026-10-15
author: steven
header:
  teaser: https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/autonomy-spectrum-banner.jpg
categories: [architecture, ai]
tags: [ai, ml, llm, software-engineering, hitl, hotl, software-architecture]
toc: true
---

<img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/autonomy-spectrum-banner.jpg" alt="An ordered grid unraveling into noise">

**Right-size the model, right-size the autonomy, and keep the people who can tell the difference.**

*Steven B Miers · October 15, 2026 · v1.06*

## 📝 Introduction

Recently, I watched a team ship a project they'd generated end to end with an AI assistant.
They'd given it an opinionated database schema with full referential integrity, a matching OpenAPI spec, and a written spec of the business rules.

It worked on day one, mostly.
It was also massive, and one big mess.
The request handler reached into everything around it, and as the team tried to make it fully work, every fix tightened the coupling a little more.
Fix one thing and something broke in a seemingly unrelated area.

> It's a simple complex system. That's the technical name for it. Because it's simple, it's prone to cascades, and because it's complex, you can't predict what's going to fail. Or how. It's computationally impossible."
> — James S.A. Corey, Caliban's War, Chapter 17_

It was plausible, it passed, and it was welded together so tightly that nothing could move.

I don't blame the tool. It built what it was asked to build. The spec said what the code should do. Nobody in the loop said how it should be put together, or knew that it mattered.

## 🧭 Where I'm standing

<img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/autonomy-spectrum-portrait.jpg" width="350px" alt="Steven B Miers"/>

I use AI every day: for research, for learning, for keeping my old Land Rover running, for code, and for running half-baked designs past it before I inflict them on humans.
So this is no bash on AI, and I'm not shouting at clouds.
(Not *those* clouds, anyway.)
I've trained and shipped production neural networks since 2007, including a patented behavioral-prediction platform, NLP pipelines with custom-trained language models, and a human-in-the-loop curation system that fed corrections back into training.
More recently it's been LLM-based systems and the agents built on them.
I understand how these things work as math I've had to implement, not as a slogan.

Which is why one current habit worries me: reach for the biggest LLM for every problem, run it as autonomously as the demo allows, and treat the people who can tell good output from plausible output as overhead.

The measurements don't back the habit.
[METR's 2025 randomized trial](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) found experienced developers took **19% longer** with AI on their own codebases, and afterward believed they'd been 20% faster.
[Stack Overflow's 2025 survey](https://survey.stackoverflow.co/2025/ai) put trust in AI accuracy at **29%**, and 66% of developers named answers that are almost right as their top frustration.
In [Anthropic's own trial](https://www.anthropic.com/research/AI-assistance-coding-skills), developers who learned a new library with AI scored **50% versus 67%** on a comprehension quiz taken without it.
I wouldn't hang a policy on any single study, but they all point the same way, and that's what bothers me.

That comprehension gap is how judgment erodes: not in a day, but one accepted answer at a time.

## ⚖️ Judgment

![Fig. 1](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/autonomy-spectrum-fig-1-judgment.jpg)

__Fig. 1: Judgment degrades gradually, then can't be measured.__
As time passes, experienced engineers leave, and the junior pipeline that would have replaced them gets cut.
*Judgment* is the ability to tell a good decision from a merely plausible one, and you only build it by working next to people who hold *the standard*.

## 📜 Coding was never the hard part

Writing code isn't software engineering.
The hard part is knowing what to build, what to leave out, what breaks at 3 a.m., and which requirement the customer forgot to mention.
Programming languages exist because English is a terrible specification language, and a spec complete enough to become correct software *is* the software, in a worse notation.

A good engineer fills the gaps: talks to the principals, trusts a hunch, asks the question nobody wrote down. A model fills gaps too. Sometimes it asks. Sometimes it grows a third arm.

![Fig. 2](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/autonomy-spectrum-fig-2-third-arm.jpg)

__Fig. 2: The third arm.__
A simulation of a poorly implemented AI solution: a 9×5 grid where every node connects to at most four neighbors.
The spec is one clear sentence, and the result still fails three ways at once.
The opening team's request handler is one of the overgrown nodes, reaching into everything around it.
From across the room it looks finished.
Only someone holding the spec, checking node by node, can see what's wrong.

## 🌈 Autonomy is a spectrum, not a switch

None of this is an argument for less AI.
It's an argument for AI with people who understand it in charge.
The question was never "automate or don't."
It's how much judgment the task needs, and who supplies it.

There are three rungs.
*In the loop*, the model proposes and a person decides, every time.
*On the loop*, the model acts and a person watches the aggregate, stepping in when needed.
*Autonomous*, the model acts alone and a person audits now and then.
Here, the loop is the work itself: each task you hand a model.
(The same words describe how ML systems learn; that's [a series of its own](https://git-steven.github.io/architecture/ai/ml/aut-ai-hitl/).)

That's also why hiring matters.
"Uses AI" describes everyone.
Understanding how the model works, and noticing when it's wrong, is the scarce part.
_(Interview tip: ask for a time the model was wrong, then watch their face.)_
The model doesn't remove the work.
It moves it from writing to reviewing, and reviewing takes someone who knows what good looks like.

### 🪜 Pick a rung for every task

To pick a rung, ask three things.
Can you undo it?
How far does a mistake travel?
Can your reviewer tell right from plausible in a minute or less?
Run that opening team's request handler through them and the answer is obvious: the design belonged in the loop, and only the boilerplate had earned a looser leash.

![Fig. 3](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/autonomy-spectrum-fig-3-leash.jpg)

__Fig. 3: The leash.__ Three rungs of autonomy, and what moves a task between them. Where a task sits is a finding, not a preference.

It runs both ways, too. If a task has a bad month, move it back left. That's not failure, that's a Tuesday.

A task moves right only when it has earned it.
"Earned" means measured, over time, on your own work, not on the vendor's benchmark.
Track the numbers vendors don't publish: duplication, churn, coupling and instability (see [📐 The Hidden Geometry of Software Coupling](https://git-steven.github.io/sdlc/architecture/coupling/metrics/geometry-coupling/)), review load.
If AI is helping your codebase, those will say so first, well before the incident report does.
And every human override is labeled training data from your own experts.
Keep it.
It's the most valuable data you own, and it only exists while those experts are still in the room.

## 🛠️ Build better systems with AI

<img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/autonomy-spectrum-build-better-systems.jpg" width="450px" alt="Build better systems"/>

### 🧯 Right-size the model

- **Reach for the algorithm first.**
  If a plain algorithm, or a homegrown, public or purchased ML model, can solve it, an LLM is overkill.
  You get deterministic results, better performance and a smaller bill.
  Save the LLM for when you really need one, like generative work or a chat interface over a customer knowledge base.
- **Right-size the model, and consider on-prem.**
  Most business work doesn't need a genius in a hyperscale data center.
  It needs a clerk who doesn't make things up.
  A small model on a box you own keeps the data home, keeps the bill flat and sips power instead of guzzling it.

### ⌨️ When writing code

Don't forget how to code.
Skills wane, and judgment goes with them.
Generating code *feels* productive right up until something breaks, and then fixing it (or coaxing the model into fixing it) is like chewing rocks.

Use AI as a reference; it's excellent at researching algorithms, libraries, services and where each should run.
Know the fundamentals, like data structures, database design, refactoring and minimal dependencies, because the model knows them too and you need to know when it's wrong.
Learn the design patterns *and* the anti-patterns, and remember the golden hammer from the era when we tried to solve everything with a pattern.

A few principles have outlived every framework fad: separation of concerns; DRY; loose coupling and high cohesion; YAGNI; fail loudly; and make it work, make it right, make it fast, in that order.
None of them is about typing.
That's the point.

### 🤝 Working with agents

An agent is an LLM with tools, a loop and a job description.
I once handed a crew of them a real service, pages of house rules, and instructions to check each other's work.
What came back compiled, passed its own tests, and needed a rewrite.
What's held up since:

- **One agent, one job.**
  Separation of concerns applies here too: a planner, an implementer, a test writer, a reviewer, each with its own instructions, tools and only the context its job needs.
  An agent that designs, builds, tests and judges its own work grades itself, and it's generous.
- **Agent review is a pre-filter, never the review.**
  A reviewer agent with a different brief catches the mechanical stuff: the missing test, the leaked credential, the rule it was told to check.
  It won't catch a wrong boundary, a schema the model quietly worked around, or a third arm.
  Those need someone who holds the standard.
- **Skills over prompts.**
  Put how you do things (the review checklist, the migration recipe, the house style) in versioned skill files the agent loads when the task matches.
  Treat them like code: in the repo, reviewed, tested.
- **Few, concrete, enforced rules.**
  The rules that got ignored said "Always" and "Never."
  The ones that hold are short, specific ("one class per file, one return point," not "write clean code"), stated once where every agent reads them, and checked by something that isn't the model: a linter, a dependency rule, an architecture test, a coverage gate.
  Don't ask an agent to honor DRY; give it the duplication detector that fails when it doesn't.
  And put a human on the cases where "most of the time" isn't good enough.
- **Small tasks, short loops.** One task, one change, reviewed before the next. Drift compounds with context length, and nothing in Fig. 2 happens in a two-hundred-line pull request.

## 🏁 Conclusion

Back to that team.
The code wasn't wrong and the tool wasn't broken.
What was missing was someone standing at the right spot on the spectrum, with enough scar tissue to say "not like that."
We built a machine that produces plausible software faster than anyone can check it, so I'd keep the checkers, and let them decide how long the leash is.

---
Version 1.06 · October 2026
