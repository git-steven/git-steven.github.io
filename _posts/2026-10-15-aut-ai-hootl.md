---
title: "🪜Semi and Fully Autonomous AI Systems"
tagline: "Part 3: HOOTL (Human-Out-Of-The-Loop)"
excerpt: "Part 3: HOOTL (Human-Out-Of-The-Loop)."
author: steven
categories:
  - ai
date: 2026-10-15 09:00:00 -0500
description:
  Earning autonomy; a model earns it one decision class at a time — and loses it the same way.
published: true
tags: [ai, ml, hitl, hotl, calibration, selective-classification, governance, software-architecture]
toc: true

---

## 👥 Part 3 Introduction
**Part 3** of a series on autonomous AI architecture, and the sequel to [Part 1: HITL](https://git-steven.github.io/ai/aut-ai-hitl/) and [Part 2: HOTL](https://git-steven.github.io/ai/aut-ai-hotl/) and [Part 3: HOOTL](https://git-steven.github.io/ai/aut-ai-hootl/). 
Human-on-the-Loop (HOTL) systems take the human gates out of the learning loop and replace them with automated validation, automated promotion, circuit breakers, and asynchronous human oversight. HITL systems fail by starvation; HOTL systems fail by poisoning. Using search ranking and recommendation as the problem domain, we compare the two, name "Alignment Risk," 
lay out seven rules for watching the loop, and decide when to use which.


![Part 3 Banner](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-banner-li.png)

### See also
* [🧬 Semi and Fully Autonomous AI Systems — Part 1: HITL (Human-In-The-Loop)](https://git-steven.github.io/ai/aut-ai-hitl/)
* [🧬 Semi and Fully Autonomous AI Systems — Part 2: HOTL (Human-On-The-Loop)](https://git-steven.github.io/ai/aut-ai-hotl/)
* [🪜 Semi and Fully Autonomous AI Systems — Part 3: HOOTL (Human-Out-Of-The-Loop)](https://git-steven.github.io/ai/aut-ai-hootl/)

**Earning autonomy: a model earns it one [decision class](#lexicon) at a time — and loses it the same way.**

> *On Optimum Recognition Error and Reject Tradeoff.*
>
> — C. K. Chow, the title of a 1970 paper [1]

## 🧾 The letter

In 2018 a tenant-screening company paid $3 million to settle [FTC](#lexicon) charges over the records it attached to applicants: an exact match on the last name, "soft" matches on first name, middle name and date of birth, and people denied housing over someone else's record [6].

That system was a matching rule. Put a model in its place and the stakes don't change; the questions do. Six months after a report goes out, a letter comes back disputing one line. Under the [Fair Credit Reporting Act](#lexicon) the clock is thirty days, and the person can ask how the line was checked [4]. So reconstruct it. Which model, which version, trained on what? How sure was it? Which rule turned its answer into a line on a report? Did a person look, and who?

If the answer is a shrug, the system was never autonomous. It was unsupervised.

_This is `Part 3` of a series._ 
* [Part 1 -- HITL](https://git-steven.github.io/ai/aut-ai-hitl/) put a human in the loop as gatekeeper.
* [Part 2 -- HOTL](https://git-steven.github.io/ai/aut-ai-hotl/) moved the human onto the loop as watchdog ([HOTL](#lexicon)), and promises to soon take the watchdog away. 
* [Part 3 -- HOOTL: this article](#lexicon) This part keeps the promise: _human out of the loop, one decision class at a time._

### See also
* [🧬 Semi and Fully Autonomous AI Systems — Part 1: HITL (Human-In-The-Loop)](https://git-steven.github.io/ai/aut-ai-hitl/)
* [⭕ Semi and Fully Autonomous AI Systems — Part 2: HOTL (Human-On-The-Loop)](https://git-steven.github.io/ai/aut-ai-hotl/)

## 📖 Lexicon

Terms used below, in plain words. Each one links back here where it first appears.

* **Argmax:** the label with the highest score; the model's actual answer.
* **Benchmarks (CIFAR-10, CIFAR-100, ImageNet, 20 Newsgroups):** standard public datasets researchers use to compare models. The first three are image sets with 10, 100 and 1,000 classes; 20 Newsgroups is text.
* **BERT:** a widely used pretrained language model, commonly fine-tuned to classify text.
* **Calibration:** whether a model's confidence matches reality. A model that says 0.9 should be right nine times in ten.
* **Calibration error (ECE):** the average gap between how sure a model says it is and how often it's actually right. 0% is perfect.
* **CFPB, EEOC, FTC:** U.S. federal regulators: the Consumer Financial Protection Bureau, the Equal Employment Opportunity Commission and the Federal Trade Commission.
* **Coverage:** the share of traffic the model decides on its own, above τ. A person takes the rest.
* **Data manifest:** a versioned list of exactly which data a model was trained on.
* **Decision class:** one kind of decision the system makes, such as one category of record. Autonomy is granted class by class, never to the whole system at once.
* **Drift (in-domain, out-of-domain):** production inputs moving away from what the model learned on, like new vocabulary or a new format. In-domain inputs look like the training data; out-of-domain inputs don't.
* **Error budget:** the most error you'll accept among the decisions the model makes alone. 1% in this article.
* **FCRA:** the Fair Credit Reporting Act, the U.S. law governing background and credit reports: accuracy, disputes, and how long items may be reported.
* **Fine-tuning:** further training a pretrained model on your own data.
* **HITL, HOTL, HOOTL:** human *in*, *on* and *out of* the loop, the three rungs of the autonomy ladder. In: a person approves each decision. On: the model decides while a person watches and can step in. Out: the model decides alone, and nobody watches each decision as it happens.
* **Input hash:** a short fingerprint of the exact input, so a decision can be found and replayed later.
* **LeNet, ResNet:** neural-network designs for image classification, from 1998 and 2016. ResNet-110 is a 110-layer ResNet.
* **Logits:** a model's raw score for each label, before they're turned into confidences.
* **Medicare Advantage:** U.S. Medicare plans run by private insurers.
* **Policy engine:** versioned, human-written rules that turn a classifier's label into a decision, and record which rule fired.
* **Prior authorization:** an insurer approving a treatment before it's given.
* **Reject option:** letting a classifier say *I don't know* and hand the item to a person. Also called abstention.
* **Risk–coverage curve:** error among the decided items, plotted against coverage. Read it at your error budget to see how much traffic the model may handle alone.
* **Selective classification:** classification with a reject option: the model answers only when it's confident enough.
* **τ (tau):** the confidence cutoff, between 0 and 1. At τ = 0.9, the model acts alone only on items it's at least 90% sure of. Raise τ and the model decides fewer items but gets more of them right; lower it and the model takes more traffic and makes more mistakes.
* **Temperature scaling (*T*):** a calibration fix. Divide the logits by one number, *T*, fitted on data held out from training. Confidence becomes honest; the answers don't change.
* **Weights, gradient:** weights are the learned numbers inside a model; training nudges them along the gradient to reduce error. Changing "by gradient" means changing by retraining.

---

## 🪜 Where Parts 1 and 2 left us

Part 1 found the labels inside the loop: every expert correction is a training example. Part 2 took the gates out and put people on the rail, and ended on deciding **per gate, not per system**. The third rung is **HOOTL**. Out of the loop is not out of the building. The person still owns the rules, audits the record, and takes every class that hasn't earned the rung. Both parts left one question open: what evidence moves a decision up the ladder, HITL → HOTL → HOOTL, and what moves it back down? [Autonomy is a spectrum](https://git-steven.github.io/architecture/ai/autonomy-is-a-spectrum/) answered it for tasks: "earned" means measured, on your own work. Here is the measurement for a model's decisions.

---

## 📏 Accuracy is the wrong dial

Headline accuracy is one number for the whole system, averaged over lopsided traffic. A rare, high-harm class can score near zero while the average looks fine. Autonomy is granted per class, so accuracy can't tell you which decisions to hand over.

Worse, the training that buys accuracy spends something else. Guo and colleagues put a 1998 [LeNet](#lexicon) next to a 2016 [ResNet](#lexicon): the old network was less accurate and its confidence matched its accuracy; the new one was more accurate and "substantially" surer than it had any right to be [2]. The dial that matters first is [**calibration**](#lexicon).

[**Temperature scaling**](#lexicon) fixes it with one number, *T*, and confidence starts meaning what it says. Their ResNet-110 went from 16.5% [calibration error](#lexicon) to 1.3%, and the fix "does not affect the model's accuracy": the [argmax](#lexicon) doesn't move [2]. The number gets honest, which is what lets a threshold on it mean something.

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-reliability.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-reliability.png" alt="Reliability diagrams before and after temperature scaling: before, the bars sit well below the perfect-calibration diagonal (ECE 16.5%); after, they sit on it (ECE 1.3%), with the same decisions" width="1000px"/>
</a>

One caveat that matters for anything that reads text: text classifiers calibrate less cleanly. On [20 Newsgroups](#lexicon) the same fix only got from 8.0% to 4.1% [2]. Calibrate, then measure. Don't assume.

---

## 🎛️ The abstention threshold is the autonomy dial

Chow priced the trade in 1957 and again in 1970: a classifier allowed to say *I don't know* makes fewer mistakes on what it does decide, at the price of deciding less [1]. The [reject option](#lexicon) is older than almost everyone now rediscovering it. [**Selective classification**](#lexicon) brings it to deep networks [3]: pick a threshold [**τ**](#lexicon) on calibrated confidence. Above τ the model decides; below it, a person does.

Every τ trades error for [coverage](#lexicon), and the trade traces a [**risk–coverage curve**](#lexicon). Draw the [error budget](#lexicon) across it, 1% here, and the curve reads off how much traffic the model may handle alone.

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-risk-coverage.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-risk-coverage.png" alt="Risk–coverage curves from published selective-classification results: at a 1% error budget a CIFAR-10 model decides 78.6% of inputs alone, while a CIFAR-100 model at 2% decides only 21.3%; the same CIFAR-10 model at full coverage errs 6.5%" width="1000px"/>
</a>

The published numbers make the point. A [CIFAR-10](#lexicon) model that errs 6.5% at full coverage keeps error under 1% on the 78.6% of inputs it is surest about. Give the method 100 classes instead of 10, and at a 2% budget it decides 21.3% of the traffic; a person takes the rest [3].

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-coverage-at-budget.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-coverage-at-budget.png" alt="Table: coverage at budget on published benchmarks, with each row placed on a rung — CIFAR-10 at 1%: 78.6%, on the loop; at 5%: 96%, autonomous; CIFAR-100 at 2%: 21.3%, in the loop; ImageNet top-5 at 1%: 38.1%, in the loop; at 5%: 88.5%, on the loop" width="1000px"/>
</a>

Now do it **per class**. Each class gets its own τ, the lowest one that keeps it inside the budget, and its coverage at that τ is its evidence. That number puts it on a rung. The rungs are a proposal: a class reaches HOOTL at 95% coverage inside the budget, held on later data; it moves onto the loop (HOTL) at 50%; below that, a person decides (HITL).

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-autonomy-ladder.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-autonomy-ladder.png" alt="The autonomy ladder: decision classes placed on three rungs (in the loop, on the loop, autonomous) by their coverage at a 1% error budget and sized by traffic share; one class climbs after calibration and retraining, one drops a rung after a drift alarm, one never qualifies" width="1000px"/>
</a>

Some classes never qualify. When the same free-text line turns up with different labels in the record, no model reading only that line can be right 99 times in 100 on it, and no τ will get it there. That isn't a tuning problem. It's a data problem, and the honest answer is a person, until the record carries more signal.

---

## ⚖️ Rules are not weights

Not everything belongs in the model. What a category *means* for the decision (how far back to look, which outcomes are excluded, what gets reported) is a lookup a person writes, versions and signs. Rules change by statute and by client, not by [gradient](#lexicon). **And whoever writes the letter is owed the rule that fired, not a [logit](#lexicon).**

The law is written the same way. The FCRA requires "reasonable procedures to assure maximum possible accuracy" [4], and its reporting-period limits cap most adverse items at seven years while leaving convictions out of the limit: a look-back window and an exclusion, written by Congress. Employment decisions weigh the *Green* factors, offense, time since, and job, which courts have applied since 1975 and which outlive the [EEOC](#lexicon)'s 2012 guidance now headed for rescission [5]. The [CFPB](#lexicon) withdrew its advisory opinions on name-only matching and background screening in May 2025 [7]. *The guidance was withdrawn; the duty was not.* And when Medicare regulators were asked about algorithms in coverage decisions, they gave this section in one sentence: "artificial intelligence cannot be used to shift the coverage criteria over time" [9].

---

## 🧾 The audit record

Every decision emits one record: **[input hash](#lexicon) · model version · [data-manifest](#lexicon) id · calibration version (T and the τ table) · labels and confidences · policy version · rule fired · decision · reviewer, if it was routed.** Nine fields, none exotic; most systems log half of them in four different places. The EU's AI Act asks for the same thing of high-risk systems: "automatic recording of events (logs) over the lifetime of the system" [10].

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-where-the-model-sits.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-where-the-model-sits.png" alt="Where the model sits: a record feeds a classifier; a τ gate passes confident answers to a versioned rules engine and drops the rest to a human review lane; reviewer overrides flow back to the classifier as training labels; an audit record captures input hash, model version, data-manifest id, calibration version, labels and confidences, policy version, rule fired, decision and reviewer" width="1000px"/>
</a>

Three slots and a lane. The classifier reads the free text and emits a label with a calibrated confidence. The τ gate, one dial per class, passes what the class has earned and drops the rest to a person. The [policy engine](#lexicon) reads the coded fields through versioned rules and emits the decision with the rule that fired. And the loudest arrow on the page runs backward: a reviewer's override comes home as a label. Part 1's thesis, still working.

Back to the letter. Look up the input hash; read off the model, the confidence, the rule, the reviewer. Replay it. The thirty-day clock becomes an afternoon, and if the line was wrong, the correction goes back as a label like any other override.

_Same loop as Parts 1 and 2, one rung further out. The **τ gate** sits on the loop, the **policy engine** turns its answers into decisions, and the one orange arrow now runs the other way: the loop hands people what falls below τ._

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-infographic.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-infographic.png" alt="HOOTL architecture infographic: the loop from Parts 1 and 2 with a τ gate after model prediction and a policy engine after the gate; a drift alarm demotes a class one rung; humans sit outside the loop, own the rules and audit a nine-field audit record, and the loop routes what falls below τ to them" width="1000px"/>
</a>

---

## 🚨 The loop closes — and the alarm

Overrides return as labels. Retraining runs on a trigger, not a calendar, behind the automated evaluation Part 2 put in place of the governance meeting. And the [drift](#lexicon) alarm watches one number first: **coverage at a fixed τ**.

**Coverage falls before accuracy does.** Accuracy needs labels, and labels arrive late: after a review, a dispute, a quarter. Coverage needs nothing. When inputs turn unfamiliar, confidence drops below τ and more traffic routes to people. The queue grows before anyone can measure the error rate.

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-drift-alarm.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-drift-alarm.png" alt="Table: BERT fine-tuned in one domain and tested in another — accuracy, calibration error and the temperature it needs all move with the shift; the fitted temperature rises from about 1.0–1.3 in-domain to 1.4–3.6 out of domain" width="1000px"/>
</a>

The published record supports the alarm and bounds it. [Fine-tune](#lexicon) [BERT](#lexicon) on one dataset, test it on a shifted one, and the temperature it needs rises with the shift, from about 1.0 to as much as 3.6 [11]: the dial moving before anyone has labels. But a model calibrated at home stays too sure abroad. In a question-answering study, an answer given at confidence 0.6 was right 80% of the time [in-domain](#lexicon) and 45% out of it [12]. It abstained more. It did not abstain enough.

So the alarm is two-sided: coverage leaving its band at a fixed τ, *and* the inputs themselves changing, a vocabulary the model hasn't seen, a new jurisdiction's format. Either one moves a class back down a rung. That's not a failure. That's the system working.

---

## 🌐 Same shape, other domains

[Prior authorization](#lexicon), benefits, content moderation: the ladder, the rules layer and the audit record carry over; only the taxonomy and the budget change. A [Medicare Advantage](#lexicon) insurer is defending a suit alleging its coverage algorithm's denials were reversed about 90% of the time on appeal; the contract claims survived because the insurer's own documents say clinicians decide [13]. The Dutch government fell in January 2021 over a benefits-fraud model whose "use, workings and effect" were hidden from the public [14]: the shrug, at national scale. Meta's Oversight Board, reviewing a handful of the hundreds of thousands of appeals it receives, overturned the company 90% of the time in 2023 [15]. Every one of those is the letter by another name.

---

## ✨ Key Takeaways

* **Autonomy is granted per decision class, on evidence — and revoked the same way.** Nothing starts at HOOTL.
* **The evidence is calibrated confidence and error among the decisions the model takes alone, under a budget.** Headline accuracy can't see it.
* **τ is the autonomy dial.** Coverage at budget places a class on the ladder; a class whose text carries mixed labels never qualifies, and that's a data problem.
* **Rules are not weights.** Versioned, signed, outside the model, so the disputant gets the rule that fired.
* **Coverage at a fixed τ is the early alarm, not the whole alarm.** It falls before accuracy can be measured, and not by enough, so watch the inputs too.

_This is **Part 3** of a series: [Part 1: HITL](https://git-steven.github.io/ai/aut-ai-hitl/) · [Part 2: HOTL](https://git-steven.github.io/ai/aut-ai-hotl/)._

---

## 📊 Data behind the figures

* **Reliability:** bin shapes are schematic; the ECE figures are Guo et al., ICML 2017, Table 1 (ResNet-110 on CIFAR-100, 16.53% → 1.26%).
* **Risk–coverage and coverage at budget:** test risk and coverage from Geifman & El-Yaniv, NeurIPS 2017, Tables 1, 2, 5 and 6.
* **Drift alarm:** Desai & Durrett, EMNLP 2020, Tables 2 and 4 (BERT, out of the box).
* **Ladder and banner:** illustrative placements; rung thresholds (≥50% → HOTL, ≥95% → HOOTL at a 1% budget) are the article's proposal.
* **Where the model sits and the infographic:** schematic; no data.

---

## 📚 References

1. Chow, C. K. "An Optimum Character Recognition System Using Decision Functions." *IRE Transactions on Electronic Computers* EC-6(4), 1957; and "On Optimum Recognition Error and Reject Tradeoff." *IEEE Transactions on Information Theory* 16(1), 1970.

2. Guo, Chuan, et al. "On Calibration of Modern Neural Networks." *ICML 2017*. Figure 1; Table 1; Section 4.2.

3. Geifman, Yonatan, and Ran El-Yaniv. "Selective Classification for Deep Neural Networks." *NeurIPS 2017*. Tables 1, 2, 5 and 6.

4. Fair Credit Reporting Act: 15 U.S.C. § 1681e(b) (accuracy); § 1681c(a), FCRA § 605(a) (reporting-period limits); § 1681i(a) (30-day reinvestigation; description of the procedure on request).

5. *Green v. Missouri Pacific Railroad Co.*, 523 F.2d 1290 (8th Cir. 1975); U.S. Equal Employment Opportunity Commission, *Enforcement Guidance on the Consideration of Arrest and Conviction Records in Employment Decisions under Title VII*, No. 915.002, 25 April 2012 (draft rescission under OMB review as of October 2026).

6. Federal Trade Commission. "Texas Company Will Pay $3 Million to Settle FTC Charges That It Failed to Meet Accuracy Requirements for Its Tenant Screening Reports," 16 October 2018 (RealPage, Inc.).

7. Consumer Financial Protection Bureau. "Interpretive Rules, Policy Statements, and Advisory Opinions; Withdrawal." 90 Fed. Reg. 20084, 12 May 2025.

8. Miers, Steven. *Semi and Fully Autonomous AI Systems*, [Part 1: HITL](https://git-steven.github.io/ai/aut-ai-hitl/), [Part 2: HOTL](https://git-steven.github.io/ai/aut-ai-hotl/) and [Part 3: HOOTL](https://git-steven.github.io/ai/aut-ai-hootl/), 2026.

9. Centers for Medicare & Medicaid Services. *Frequently Asked Questions related to Coverage Criteria and Utilization Management Requirements in CMS Final Rule (CMS-4201-F)*, 6 February 2024.

10. Regulation (EU) 2024/1689 (the AI Act), Article 12(1) (record-keeping) and Article 14 (human oversight).

11. Desai, Shrey, and Greg Durrett. "Calibration of Pre-trained Transformers." *EMNLP 2020*. Tables 2 and 4.

12. Kamath, Amita, Robin Jia, and Percy Liang. "Selective Question Answering under Domain Shift." *ACL 2020*. Section 5.3.

13. *Estate of Lokken v. UnitedHealth Group*, No. 0:23-cv-03514 (D. Minn.): complaint filed 14 November 2023 (the 90% figure is the plaintiffs' allegation); order on the motion to dismiss, 13 February 2025.

14. Amnesty International. *Xenophobic Machines: Discrimination through Unregulated Use of Algorithms in the Dutch Childcare Benefits Scandal*, EUR 35/4686/2021, 25 October 2021.

15. Oversight Board. *2023 Annual Report*, 2024 (53 decisions; 398,597 appeals received).

---

*Steven Miers — [git-steven.github.io](https://git-steven.github.io)*
