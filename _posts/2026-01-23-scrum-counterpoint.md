---
title: "Scrum Counterpoint: Agile, Scrum, and the Point‑Perspective Pitfall"
date: 2026-01-23 11:37:00 -0500
categories:
  - sdlc
  - agile
  - scrum
  - architecture
  - software engineering
author: steven
---
# Scrum Counterpoint: Agile, Scrum, and the Point Perspective Pitfall

*By Steven Miers*

> “Everything should be made as simple as possible, but not simpler.” — often attributed to Einstein, and often ignored during sprint planning.

Scrum has become a household name in software development. It’s the framework beloved by consultants and lampooned by developers. But as with any tool, its greatest strength—a lightweight structure with clear ceremonies—can become a weakness when used without an understanding of why those ceremonies exist.

This article offers a counterpoint to the common story-point obsession. Rather than attacking Scrum, it pokes fun at the point perspective—the habit of reducing agility to velocity charts, burn-down graphs, and arithmetic on estimates. Along the way, we revisit the Agile Manifesto to remind ourselves that our highest priority is to satisfy the customer through early and continuous delivery of valuable software, and that individuals and interactions matter more than processes and tools.

---

## Table of Contents

- [Introduction: The Point Perspective](#introduction-the-point-perspective)
- [Agile Values vs. Scrum Rituals](#agile-values-vs-scrum-rituals)
- [Symptoms of Dogmatic Scrum](#symptoms-of-dogmatic-scrum)
- [The Point Perspective Pitfall](#the-point-perspective-pitfall)
    - [Why Points Are Not Additive](#why-points-are-not-additive)
    - [Reframing Points as Uncertainty](#reframing-points-as-uncertainty)
    - [When High Points Signal Decomposition](#when-high-points-signal-decomposition)
- [What Good Scrum Looks Like](#what-good-scrum-looks-like)
- [Reclaiming Agility: Practical Tips](#reclaiming-agility-practical-tips)
- [Conclusion](#conclusion)
- [References](#references)

---

## Introduction: The Point Perspective

In many Scrum teams, the concept of the **story point** has taken on a mythical quality. It’s treated as a currency of productivity, a unit of measurement as precise as a kilowatt-hour. Managers ask, *“How many points will we get this sprint?”* Teams debate whether a task is a three-pointer or a five-pointer with the solemnity of a court proceeding.

Meanwhile, code complexity mounts and customers wait for features that matter.

Why do we obsess over points? Because they are easy to count. They give us charts and metrics that look scientific. They feed our desire for certainty in an uncertain world. Yet the Agile principles remind us that **working software is the primary measure of progress**, and that simplicity—the art of maximizing the amount of work not done—is essential.

Points are a proxy.  
They are not the product.

## Agile Values vs. Scrum Rituals

The Agile Manifesto emphasizes values; Scrum provides a framework. Trouble starts when the framework is treated as the goal.

| Agile Value 🧭 | Healthy Scrum Practice ✅ | Dogmatic Scrum Anti-Pattern ❌ |
|---------------|--------------------------|-------------------------------|
| Individuals & interactions | Conversations that resolve blockers | Stand-ups as interrogations |
| Working software | Demos of real, usable increments | Slide decks and screenshots |
| Customer collaboration | Backlog reshaped by feedback | “Sprint scope is locked” |
| Responding to change | Swapping stories when value shifts | Change treated as failure |

The tension isn’t between Agile and Scrum—it’s between **principles** and **ritualized implementation**.

## Symptoms of Dogmatic Scrum 🚨

You may have fallen into the Point Perspective Pitfall if you notice:

- **Ever-lowering bar** 📉  
  README edits and typo fixes celebrated as sprint wins.

- **Ticket Tetris** 🧩  
  Work chosen for point efficiency, not customer value.

- **Rollover roulette** 🎰  
  Chronic carry-over normalized instead of questioned.

- **Micromanaging Masters** 🕵️  
  Stand-ups used to track people instead of unblock work.

- **Metrics over meaning** 📊  
  Velocity treated as success rather than a signal.

These behaviors are not caused by Scrum—они emerge when Scrum is applied without understanding.

## The Point Perspective Pitfall 🎯

Story points represent **relative effort**, not time, not value, and certainly not productivity. When points become currency, behavior warps:

- **Performance gaming**  
  Easy points beat valuable work.

- **False progress signals**  
  Velocity rises while outcomes stagnate.

- **Technical debt acceleration**  
  “We’ll refactor later” becomes a lie we tell ourselves.

- **Context collapse**  
  Cross-team point comparisons create nonsense and competition.

Points are abstract. Treating them as concrete guarantees disappointment.

### Why Points Are Not Additive ➕≠

A persistent misconception is that points behave like math.

#### Question:
How often is a **5-point story** truly equivalent to **two stories totaling 5 points**?

#### Answer:
Almost never.

#### Numeric Combination Matrix

| + | **1** | **2** | **3** | **5** | **8** |
|---|---|---|---|---|---|
| **1** | 🟩2 | 🟩3 | 🟥4 | 🟥6 | 🟥9 |
| **2** | 🟩3 | 🟩4 | 🟩5 | 🟥7 | 🟥10 |
| **3** | 🟥4 | 🟩5 | 🟥6 | 🟩8 | 🟥11 |
| **5** | 🟥6 | 🟥7 | 🟩8 | 🟥10 | 🟥13 |
| **8** | 🟥9 | 🟥10 | 🟥11 | 🟥13 | 🟥16 |

This matrix shows that only a handful of combinations (highlighted in green) sum to another Fibonacci number: 1+1=2, 1+2=3, 2+3=5, and 3+5=8. Most combinations fall between Fibonacci values (for example, 2+2=4 or 5+8=13) and therefore do not neatly map to a single story point. It illustrates why point arithmetic breaks down—and why downstream calculations (capacity, delivery dates, individual performance) compound the error.

### Reframing Points as Uncertainty 🌫️

A more honest mental model:

> **Story points are a signal of uncertainty.**

| Point Size | What It Often Means | Healthy Response |
|-----------|---------------------|------------------|
| 1–2 🟢 | Well understood | Pull confidently |
| 3–5 🟡 | Some unknowns | Clarify & slice |
| 8+ 🔴 | High uncertainty | Decompose immediately |

High-point stories often tell you: *“You don’t understand this well enough yet.”* That’s not a failure—it’s useful information.

> **Sidebar:** The popular *cone of uncertainty* metaphor visualises how our range of possible outcomes narrows as we learn more.  We won’t dive into that shape here—it deserves its own article—but keep in mind that every story point represents a slice of that cone.  Larger numbers correspond to a wider slice and more room for surprises; smaller numbers reflect a tighter, better understood scope.

### When High Points Signal Decomposition

The larger the point value, the greater the uncertainty and risk involved. Work items above roughly 16 hours or 20 points should be broken down into smaller pieces. This ties into the idea that a high story-point value is often a proxy for unknowns. A 13-point or 20-point item usually hides multiple assumptions, dependencies, or risk factors. Rather than carrying these unknowns forward, treat large estimates as a sign to decompose the work or perform additional discovery.

| Points | Typical complexity | Uncertainty/Risk | Suggested action |
|---|---|---|---|
| **1** | 🟢 low | 🟢 low | Proceed; tasks are well understood |
| **2** | 🟢 low–medium | 🟡 low–medium | Proceed; minor unknowns |
| **3** | 🟡 medium | 🟡 medium | Proceed; verify assumptions |
| **5** | 🟠 medium–high | 🟠 medium–high | Break story into smaller tasks if possible |
| **8** | 🟥 high | 🟥 high | Decompose; perform spike/research |
| **13+** | 🟥🟥 very high | 🟥🟥 very high | Stop: too much uncertainty; refine and split |

### <!-- The Uncertainty Cone section has been intentionally removed -->

## What Good Scrum Looks Like 🌱

Good Scrum feels almost boring—in the best way.

- **Principles over process**  
  Ceremonies evolve or disappear when they stop helping.

- **Self-organizing teams**  
  Scrum Masters facilitate; they do not police.

- **Technical excellence first**  
  Quality is never traded for points.

- **Customer-visible progress**  
  Every sprint answers: *“What’s better for the user?”*

- **Real retrospectives**  
  Reflection leads to change, not checklists.

When Scrum works, you stop talking about Scrum so much.

## Reclaiming Agility: Practical Tips 🔧

- **Rename points as 'uncertainty'.** Don’t treat them as currency. They serve as signals of risk.
- **Adopt Kanban and limit WIP.** Focus on flow and throughput rather than chasing velocity charts.
- **Tighten your Definition of Done.** Include tests, refactoring, and usable increments to prevent hidden debt.
- **Treat backlog grooming as strategy, not admin.** Purge stale items and align work with real user value.
- **Ask “What’s blocking you?”** Stand-ups should eliminate impediments instead of reciting status.
- **Reward refactoring and debt repayment.** Ensure quality isn’t invisible.
- **Experiment with flow-based work.** Try periods without formal sprints to see if rituals help or hinder.
- **Celebrate outcomes, not estimates.** Recognize delivering value, not burning numbers.

Try them. Adapt them. Ignore any that don’t help.

## Conclusion

**Scrum Counterpoint: Agile, Scrum, and the Point Perspective Pitfall** isn’t anti-Scrum. It’s a reminder that tools serve people—not the other way around.

Story points are useful when treated as rough, local, and temporary signals. They become harmful when treated as truth, currency, or contracts. The next time you’re debating whether a ticket is a three-pointer or a five-pointer, pause and ask: *What uncertainty is this number trying to tell us about?* And maybe—just maybe—ask the most Agile question of all: **What’s the point?**

## References

- Manifesto for Agile Software Development  
  <https://agilemanifesto.org/>

- Principles Behind the Agile Manifesto  
  <https://agilemanifesto.org/principles.html>

- *Scrum: The Agile Trap That Keeps on Sprinting*  
  <https://www.linkedin.com/pulse/scrum-agile-trap-keeps-sprinting-steven-miers-1dtpc>
