---
title: "🧬 Semi and Fully Autonomous AI Systems"
date: 2026-05-29 03:33:33 -0500
categories:
  - architecture
  - ai
  - ml
author: steven
description: 
  Part 1 of a series on autonomous AI architecture. Most production AI that looks autonomous is actually Human-in-the-Loop (HITL): a loop-shaped but not closed-loop system. Using an annotated architecture diagram, we show that it isn't the presence of humans that breaks the loop — it's the data curation and model governance gates. Covers HITL signatures, human gates as architectural control surfaces, semi-supervised learning, and "Autonomy Debt."
---

# Part 1: HITL (Human-In-The-Loop)

<div style="align-self: center">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hitl-redux-sm.png" width=600>
</div>

**Your AI _Looks_ autonomous. It's _probably_ not. Here's an Architecture Diagram to Prove It. **

_Most production AI deployments exhibit loop-like behavior, but they stop short of being true `closed-loop systems`. Human feedback, policy enforcement, and operational oversight introduce delays and control boundaries that shape system outputs and maintain accountability, limiting autonomous operation._

---

## ⭕ The Illusion of the Closed Loop

Your platform performs specialized matching for clients. An ML model scores candidates, ranks them, and serves predictions through an API. The product team calls it "AI-powered." The sales deck says "autonomous matching engine." The investors nod approvingly.

Then you look at the actual architecture and notice:
* A human reviews every session before feedback enters the training set
* A governance team approves every model before it touches production
* The "real-time learning" happens in a batch job that runs Tuesday nights

**Congratulations. You've built a very sophisticated suggestion box with a neural network attached.**
* This isn't a criticism — it's a *classification*. Most production AI systems that look autonomous are actually **Human-in-the-Loop (HITL)** systems. They're adaptive, useful, and often excellent. But they are not closed-loop.
* Understanding *why* matters, because the architecture you choose determines what your system can and cannot learn, how fast it can learn it, and who's liable when it gets something wrong.
* And here's the first non-obvious thing: it's not the *presence of humans* that makes these systems non-autonomous. It's the specific role those humans play. More on that after the diagram.

---

## 👥 What Makes a System HITL?

A HITL system is one where humans are structurally embedded in the feedback and control pathways of the AI. Not as end users consuming predictions, but as **active mediators** of what the system learns and how it evolves.

The key structural signatures are:

| Signature                   | What It Means                                                                                        |
|-----------------------------|------------------------------------------------------------------------------------------------------|
| **Human-mediated feedback** | Expert users rate, tag, or correct predictions — but the signal is filtered before reaching training |
| **Delayed learning**        | Models retrain on curated batches, not streaming feedback                                            |
| **Filtered signal**         | A curation team selects which feedback enters the training pipeline                                  |
| **Controlled deployment**   | A governance team validates and approves model releases                                              |

If your system has *any* of these, it's HITL. If it has *all four*, it's what I'd call **fully-mediated HITL** — the human isn't just in the loop, they *are* the loop's bottleneck.

---

## 🏛️ The Architecture: HITL Loop and Human Gates

_The **infographic** below maps **HITL** architecture as an elliptical loop. The two orange hexagons — `Data Curation` and `Model Governance` — are the **human gates**: humans must approve before the loop can continue past them._
<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hitl-redux.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hitl-redux.png" alt="🧬HITL Architecture Infographic" width="1000px"/>
</a>
### ⬭ The HITL System

This is the main human-in-the-loop.  Predictions flow to users, users react, reactions get stored.

It is **NOT** a closed loop: two orange hexagonal nodes — <span style="color: #BB7C4B; font-family: monospace;"><strong>Data Curation</strong></span> and <span style="color: #BB7C4B; font-family: monospace;"><strong>Model Governance</strong></span> — sit inline on the loop and require human approval before downstream steps run.

![Infographic Legend](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hitl-redux-legend.png)

* **🧮 MODEL PREDICTION SERVICE:** _real-time results (classification/inference)_
* **🖼️ PRODUCT INTERFACE:** _Automated predictions combined with actual session info and expert user feedback_
* **🌀 DATA SERVICE:** _Storage of session outcome and expert user feedback_
  * **👥 DATA CURATION** <span style="color: #BB7C4B; font-family: monospace;"><strong>(HUMAN GATE):</strong></span>
    * Evaluates user session data and feedback from expert user
    * Select for inclusion or exclusion (or include with changes)
    * Sanity-check
  * **🌀 DATA PIPELINE:** (_Data-Wrangling_)
    * Discover
    * Validate
    * Clean
    * Normalize
    * Enrich/Augment/Transform
* **🧑‍💻 DEVELOPER**
  * Initial development of model
  * Bypassed in subsequent loops
  * Can be done again for manual intervention, to change wrangling parameters, for normalization, augmentation, etc.
* **🧬 MODEL TRAINING**
  * batch retraining
  * model tuning/ensembling
  * RL (reinforcement learning)
* **👥 MODEL GOVERNANCE** <span style="color: #BB7C4B; font-family: monospace;"><strong>(HUMAN GATE):</strong></span>
  * QA of new model
  * Sanity check

### 👥 Human Gates: The Architectural Control Surfaces
At nearly opposite ends of the loop sit the two orange hexagons — `Data Curation` and `Model Governance`. They live *inside* the loop, but they break it semantically by requiring human sign-off:

* **Data Service → Data Curation → Data Pipeline**: A curation team reviews session data and selects which signals are trustworthy enough for training. This prevents noisy or adversarial feedback from corrupting the model.
* **Model Training → Model Governance → Model Prediction Service**: A governance team validates model performance, checks for bias, and approves releases. No model reaches production without human sign-off.

These aren't bureaucratic overhead. They're **architectural control surfaces**. Remove them, and your "AI-powered" system is one bad training batch away from recommending your worst matches for your best client.

---

### 🔍 Wait — It's Not the "Human" That Breaks the Loop

This is the part that tends to reframe the whole diagram:

**The human users in this system don't make it non-autonomous. The curation and governance teams do.**

Think about it: a fully autonomous AI — say, a large language model trained via **Reinforcement Learning from Human Feedback** [3] — still has humans all over it. Millions of them. Users rating outputs, flagging errors, generating the signal the model learns from. Those humans are *in the loop*. And yet the system is autonomous, because that feedback flows directly back into training without a mandatory human checkpoint deciding what's trustworthy enough to keep.

What breaks *our* loop is structural, not incidental. For this example (see [Problem Domain](#the-problem-domain-matching) below for details), it's two governance gates:

* The **Data Curation** gate, which decides which feedback signals are trustworthy enough to enter the training pipeline
* The **Model Governance** gate, which decides which trained models are ready to deploy

Remove those two gates and the rest of the system — expert users rating matches, session outcomes accumulating, the pipeline ingesting data — could, in principle, run continuously. Add them back, and you have two asynchronous, human-bandwidth-constrained chokepoints that batch and gate everything downstream.

>The "Human" in Human-in-the-Loop doesn't mean *end* _users_.
>It means **gatekeepers**.
>And it's the _gatekeepers_ — not the _users_ — who keep this loop from closing.

---

## The Problem Domain: Matching
This architecture isn't theoretical. It maps to production systems in the professional services space — platforms where the cost of a bad match is measured in lost contracts, not lost clicks.

Matching requires:
* **📐 Precision**: The difference between "knows about derivatives" and "structured credit derivatives at a bulge-bracket bank during the 2008 crisis" is the difference between a usable match and a wasted hour.
* **🧭 Context**: The same match might be perfect for a diligence call and terrible for a survey. Context isn't just *who* — it's *why, when, and for whom (and even where)*.
* **♻️ Continuous improvement**: Match availability, knowledge of end-users and expert users, and client preferences all drift. A static model degrades visibly within weeks.

This combination — high precision, rich context, continuous drift — naturally produces semi-supervised systems. You can't label everything (too expensive), you can't leave everything unlabeled (too noisy), so you build a system where humans and models collaborate. That's HITL.

---

## 🤖 Why It's Not Autonomous (And Why That's Fine)

_A truly autonomous system would:_
1. Ingest feedback directly into the learning loop without human curation
2. Retrain continuously (or near-continuously) on streaming data
3. Deploy updated models automatically based on performance thresholds
4. Self-correct without human intervention when predictions degrade

Our **HITL** system does *none of these*. Every feedback signal passes through at least one human filter. Retraining is batched. Deployment is gated. Correction requires a human to notice the problem, diagnose it, and intervene.

### 🏦 Autonomy Debt
**And that's _often_ the right call.** Fully autonomous systems can fail fast and fail weird. **HITL** systems fail slow and fail in ways humans can understand and fix. In a domain where a single catastrophic match can lose a client relationship worth millions, a **HITL** system may be a better choice than a closed-loop system.

The tradeoff is what I'll call **"Autonomy Debt"** (with a nod to Sculley et al. [5]): the gap between what your system *could* learn if it were fully autonomous and what it *actually* learns given human bandwidth constraints.

#### 🚰 Bottleneck
As your network of matchable items scales from hundreds to tens of thousands, the curation team becomes the bottleneck. The governance review becomes the deployment blocker. The humans who make the system trustworthy also make it slow.

Managing that debt — knowing when to automate a gate, when to keep a human in the loop, and when to add more humans — is the central architectural challenge of HITL systems.

---

## 🧠 Semi-Supervised Learning in Practice

The HITL architecture naturally implements a semi-supervised learning pattern. Here's how it breaks down:

| Component                       | Supervised Signal                                    | Unsupervised Signal                                                                    |
|---------------------------------|------------------------------------------------------|----------------------------------------------------------------------------------------|
| Expert user Ratings and Tagging | Explicit tagging and evaluation on matches           | —                                                                                      |
| User Session outcomes           | —                                                    | Engagement metrics (attempts, total time to find match, sequence in result list, etc.) |
| Data Curation                   | Curated training labels and data to improve matching | —                                                                                      |
| Model Curation                  | Evaluated and approved models for use in inference   | —                                                                                      |

The supervised signal is expensive (human-generated) and sparse. The unsupervised signal is cheap and abundant. The semi-supervised architecture lets you use the abundant signal to expand coverage while using the expensive signal to maintain quality.

This is *exactly* the pattern described in Zhu & Goldberg's foundational work on semi-supervised learning — using a small amount of labeled data to guide learning from a large amount of unlabeled data. In a HITL system, the "labeling" happens through the operational loop, and the "guidance" happens through the human gates.

---

## 🗝️ Key Takeaways

**Many production AI systems are loop-shaped, but not closed-loop.** Human feedback, curation, and governance introduce delay due to selecting/rejecting/cleaning, and control boundaries that prevent true autonomy.

_This is **Part 1** of a series._ 
In **Part 2**, we'll look at what happens when you start removing those human gates  and the entirely different failure modes that emerge when the loop actually closes.  
* Will it cause the AI uprising?
* Will it make everybody's lives better?

_...Find out in **Part 2** (coming soon with enhanced infographic diagrams!)_

---

## 📖 References

1. Zhu, Xiaojin & Goldberg, Andrew B. *Introduction to Semi-Supervised Learning*. Morgan & Claypool, 2009. — Foundational framework for combining labeled and unlabeled data.

2. Monarch, Robert. *Human-in-the-Loop Machine Learning*. Manning Publications, 2021. — Comprehensive treatment of HITL patterns in production ML systems.

3. Christiano, Paul, et al. "Deep Reinforcement Learning from Human Preferences." *NeurIPS*, 2017. — The RLHF paradigm that underpins modern HITL training loops.

4. Amershi, Saleema, et al. "Software Engineering for Machine Learning: A Case Study." *ICSE-SEIP*, 2019. — Microsoft's production ML lifecycle patterns, including human oversight gates.

5. Sculley, D., et al. "Hidden Technical Debt in Machine Learning Systems." *NeurIPS*, 2015. — The foundational paper on ML systems debt, directly relevant to Autonomy Debt.

---

*Steven Miers — [git-steven.github.io](https://git-steven.github.io)*
