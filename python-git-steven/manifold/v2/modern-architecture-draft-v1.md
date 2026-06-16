---
title: "🌌 Modern Software Architecture and the Structure of the Universe"
excerpt: "The Shape of Architecture — software runs in another universe, and here's what we know about its laws: they are not the same as ours."
categories:
  - architecture
  - philosophy
tags:
  - architecture
  - distributed systems
  - ai
  - cost
toc: true
---

**The Shape of Architecture** — software runs in another universe, and here's what we know about its laws: they are not the same as ours.

> *"The eternal mystery of the world is its comprehensibility."*
> — **Albert Einstein**, *Physics and Reality* (1936)

*Draw an architecture diagram and you've sketched a little universe.*

I don't reach for that line lightly. A box-and-arrow picture is a poor model of a running system; a semi-directed, cyclic graph of a thought is a better one. There is no actual universe where architecture comes alive as software. But there might as well be — and I've been calling it **the Manifold** for longer than the robots have been writing code. It has laws. They are not the laws of *our* universe. And like ours, some of them can be broken — for a while. 🌌

## 🌌 Welcome to the Manifold

Carl Sagan liked to say that to make an apple pie from scratch, you must first invent the universe. Shipping a system is the same trick: before the first request is served, you've quietly invented the universe it runs in — its objects, its time, its causes and effects, its notion of *failure*. You aren't only writing code. You're **legislating physics**.

If you want a picture for the Manifold, borrow the strangest one physics has: a **Calabi–Yau manifold**. In string theory, our universe's extra dimensions are thought to curl up into one of these intricate, folded shapes — and here's the part that matters: *the shape of the manifold determines the laws of physics* that fall out of it, which particles can exist and how forces behave. Change the folds, change the universe. That is the exact bargain you make as an architect. The shape of your system — its boundaries, its couplings, the paths your data is allowed to take — fixes the laws everything downstream must obey. It's why two teams with the same requirements and different architectures end up living in different worlds. **The Shape of Architecture, made literal.**

And the physics you legislate is strange. In some ways the Manifold is **stricter** than our own:

- A type error is more absolute than friction — there's no "close enough."
- A null pointer is more final than death.
- A crash isn't local. The whole cosmos blinks out at once.

In other ways it is far **stranger** — looser than anything our physics permits:

- You can **add a dimension** any time you draw a new boundary.
- You can **replay time**, querying the world as it was at 3:02 a.m.
- You can **teleport** a fact across the planet and copy it a million times for free.

| Our universe | The Manifold |
|---|---|
| Laws are **discovered** | Laws are **authored** — by you |
| Light-speed caps everything | Latency caps everything, and you can't bribe it |
| One arrow of time | Replay the log; query the past |
| Matter is conserved | Data is copied, forked, duplicated for free |
| Failure is local and rare | Partial failure is constant and normal |
| You can't add a dimension | You add one every time you draw a boundary |

That last row is the whole story of how we got here.

## 📡 The Coefficient of Separation

The history of software architecture is one number climbing: **how far apart the pieces are allowed to be.** We started with everything fused into a single process and spent fifty years prying it apart — pulling concerns away from each other until the separation stopped being conceptual and became *physical*. Every time we added distance, the Manifold answered with a new law.

| Era | What got separated | The new law of the Manifold |
|---|---|---|
| **One process** | nothing — one address space, one clock | Determinism is absolute; a crash is total |
| **Linked libraries** — DLL / `.so` / `.dylib` | your code from everyone else's | Versions are physics; mismatched laws = "DLL hell" |
| **IPC & the network** — pipes → sockets → CORBA → SOAP → REST → queues → gRPC | functions, by a boundary | Distance, latency, and partial failure become real |
| **Independent services** | concerns, *physically* | Scale each piece alone; failure is normal, not rare |
| **Cloud-native** — S3, Kinesis, Lambda | compute from storage from state | There is no single *now* — no global clock |
| **AI-written code** | authorship from understanding | Someone human still has to own the structure |

Read it top to bottom and you can watch a developer's daydream — *separate the concerns, almost physically* — become literally true. **Every new distance came with a new law.** None of those laws were free.

## 💸 The Tangible Cost of Progress

Here's the part nobody draws on the architecture diagram: **every new power in the Manifold arrives with a bill, and most of the bills are hidden.** The architect's real job is less "can we build this" and more "what does this actually cost, and who pays it."

### 🪙 When distribution got expensive

Microservices were sold as the shape of the future. Then the pendulum swung. In 2023, Amazon's own Prime Video team folded a sprawling, serverless monitoring service back into a single process and cut its cost by about **90%**. Martin Fowler had named the trap years earlier — the *"microservice premium,"* the standing tax you pay in latency, ops, and coordination for the privilege of being distributed.

The lesson isn't "monoliths won." It's that **microservices were never a law of the Manifold — they were local weather.** The law underneath is coupling, and coupling doesn't care which decade you're in.

### 🤖 "I'm not going to whine because a robot took my job"

I'm not. These tools amaze me daily — a force multiplier, a tireless research assistant, a generator of images and diagrams I'd never have the patience to draw by hand. Kent Beck calls the good version **"augmented coding"** (as opposed to "vibe coding"), and he's right that it rewrites the math of the craft: *"90% of my skills just went to \$0, and 10% went up 1000×."* The surviving 10% — vision, design, holding complexity in your head — is the architect's job, exactly. Beck also describes an AI agent as an **"unpredictable genie."** Keep that image handy.

Because here's the failure mode. A team reaches for a large language model on the 80% case that **a few lines of code would have settled** — using a genie to merge two lists. It feels like progress. It bills like progress. It is, in fact, the most expensive way to compute something you already knew how to compute.

### 🎯 The right-sized tool

The subtle version is worse, and more interesting. Sometimes a job genuinely *needs* a frontier model… at first. Then someone reads the logs. They notice the inputs are **predictably shaped**, that months of saved prompts and responses are sitting right there — cleanable, filterable, normalizable — and they train a plain, unglamorous neural network to do the same job for a rounding error of the cost. The model bill falls off a cliff.

This isn't folklore; it's the recommended pattern now. NVIDIA's research group argues that small, specialized models are **10–30× cheaper to serve** than generalist LLMs, and spells out the playbook: *map the task with a big model, then replace the hot spots with small ones.*

> **Don't fire a nuke when a slingshot will do.** The entire discipline of cost architecture lives in that sentence.

### 🧾 Receipts, not honking

None of this is a vibe. Google's **DORA** research found that a 25% rise in AI adoption tracked with roughly **1.5% lower delivery throughput and 7.2% lower stability** — the productivity you feel as an individual quietly leaks out of the system when the fundamentals aren't there. The 2025 report reframes AI as an **amplifier**: it magnifies whatever discipline, or chaos, you already had. **Gartner** expects a meaningful share of agentic-AI projects to be **cancelled by 2027**, with operating cost the reason given. And the oldest rule in the book still holds — *YAGNI*, and "use the simplest thing that works."

There's a colder cost too, and I won't pretend otherwise. An industry that staffs **armies of engineers to feed and grade its models** is paying a bill it mostly keeps off the books. The most expensive system you can build is one whose hidden cost is **the people quietly feeding it**. A good architect counts that line, too.

## 🪐 The Rules That Don't Change

Some laws of the Manifold can be broken — for a while. Skip the tests, smear the boundaries, let the genie write code that no one reads. The system keeps running. It feels fast. And then comes what a professor of mine used to warn about — he was paraphrasing **Gerald Weinberg**:

> *"If builders built buildings the way programmers wrote programs, then the first woodpecker that came along would destroy civilization."*
> — **Gerald Weinberg**

The woodpecker always comes. What it tests are the laws that never actually changed, across any era in that table above:

- **Boundaries and coupling.** The load-bearing one. *(I measured it in [The Hidden Geometry of Software Coupling](https://git-steven.github.io/sdlc/architecture/coupling/metrics/geometry-coupling/) — the shape of the system changes; the math does not.)*
- **You cannot cheat latency or partial failure.** You can only choose where to feel them.
- **Immutability and derivation.** Keep the facts; derive the rest. (It's why an event log and a raw data lake are the same idea in different clothes.)
- **Every abstraction is a new universe you now own.** Dijkstra's point: abstraction isn't vagueness — it's a new level on which you get to be precise, and responsible.

So are there still rules, now that the robots are writing the code? Of course. The robot writes the code; **a human still owns the structure** — reads it, shapes it, signs it. That was always the part that wasn't about typing.

> **You don't discover the laws of your software universe. You author them — and then you live in the world you built.**

## 🗝️ Key Takeaways

- Every architecture is a small universe — **the Manifold** — and you author its physics.
- Its laws are **stricter** than ours in some ways, **stranger** in others.
- The march from one process to the cloud is one rising number: **separation**. Each new distance brought a new law.
- **Every new power arrives with a bill, mostly hidden.** Distribution, and now AI, teach the same lesson by way of the invoice.
- **Don't fire a nuke when a slingshot will do** — right-size the tool, and count the human cost, not only the compute.
- The deepest laws — **boundaries, latency, immutability, ownership** — never changed. The woodpecker still comes for the ones you broke.

## 📚 References

- Albert Einstein — *"Physics and Reality," Journal of the Franklin Institute* (1936)
- Carl Sagan — *Cosmos* (1980)
- Brian Greene — *The Elegant Universe* (1999) — string theory and Calabi–Yau compactification
- Gerald Weinberg — *The Psychology of Computer Programming* / "Weinberg's Law" (1971)
- Amazon — Prime Video Tech Blog, *"Scaling up the Prime Video monitoring service and reducing costs by 90%"* (2023)
- Martin Fowler — *"MicroservicePremium,"* martinfowler.com
- Kent Beck — *"90% of My Skills Are Now Worth \$0"* (2023); *"augmented coding,"* Tidy First? (2025)
- Belcak et al. — *"Small Language Models are the Future of Agentic AI,"* NVIDIA Research, arXiv:2506.02153 (2025)
- Google / DORA — *Accelerate State of DevOps Report* (2024, 2025)
- Edsger W. Dijkstra — on abstraction as a new level of precision
