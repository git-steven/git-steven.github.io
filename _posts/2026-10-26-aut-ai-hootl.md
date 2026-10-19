---
title: "🪜 Semi and Fully Autonomous AI Systems"
tagline: "Part 3: HOOTL (Human-Out-Of-The-Loop)"
date: 2026-10-26 09:00:00 -0500
categories:
  - architecture
  - ai
  - ml
author: steven
tags: [ai, ml, hitl, hotl, calibration, selective-classification, governance, software-architecture]
description:
  Part 3 of a series on autonomous AI architecture, and the sequel to Parts 1 (HITL) and 2 (HOTL). HOOTL, Human-Out-Of-The-Loop, is the rung a model has to earn, one decision class at a time. The evidence is calibrated confidence and the error it makes among the decisions it takes alone, under a stated budget, not headline accuracy. Covers the abstention threshold as the autonomy dial, why the rules stay out of the weights, the audit record every decision emits, and the drift alarm that moves a class back down a rung.
published: false
header:
  teaser: https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-banner-li.jpg
toc: true
---

![Part 3 Banner](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-banner-li.png)

# 🪜 Part 3: HOOTL (Human-Out-Of-The-Loop)

**Earning autonomy: a model earns it one decision class at a time — and loses it the same way.**

> *On Optimum Recognition Error and Reject Tradeoff.*
>
> — C. K. Chow, the title of a 1970 paper [1]

## 🧾 The letter

In 2018 a tenant-screening company paid $3 million to settle FTC charges over the records it attached to applicants: an exact match on the last name, "soft" matches on first name, middle name and date of birth, and people denied housing over someone else's record [6].

That system was a matching rule. Put a model in its place and the stakes don't change; the questions do. Six months after a report goes out, a letter comes back disputing one line. Under the Fair Credit Reporting Act the clock is thirty days, and the person can ask how the line was checked [4]. So reconstruct it. Which model, which version, trained on what? How sure was it? Which rule turned its answer into a line on a report? Did a person look, and who?

If the answer is a shrug, the system was never autonomous. It was unsupervised.

_This is Part 3 of a series. [Part 1](https://git-steven.github.io/architecture/ai/ml/aut-ai-hitl/) put a human in the loop as gatekeeper (HITL); [Part 2](https://git-steven.github.io/architecture/ai/ml/aut-ai-hotl/) moved the human onto the loop as watchdog (HOTL), and promised to take the watchdog away too [8]. This part keeps the promise: HOOTL, human out of the loop, one decision class at a time._

### See also
* [🧬 Semi and Fully Autonomous AI Systems — Part 1: HITL (Human-In-The-Loop)](https://git-steven.github.io/architecture/ai/ml/aut-ai-hitl/)
* [⭕ Semi and Fully Autonomous AI Systems — Part 2: HOTL (Human-On-The-Loop)](https://git-steven.github.io/architecture/ai/ml/aut-ai-hotl/)

---

## 🪜 Where Parts 1 and 2 left us

Part 1 found the labels inside the loop: every expert correction is a training example. Part 2 took the gates out and put people on the rail, and ended on deciding **per gate, not per system**. The third rung is **HOOTL**: the model decides alone and nobody watches the decision as it happens. Out of the loop is not out of the building. The person still owns the rules, audits the record, and takes every class that hasn't earned the rung. Both parts left one question open: what evidence moves a decision up the ladder, HITL → HOTL → HOOTL, and what moves it back down? [Autonomy is a spectrum](https://git-steven.github.io/architecture/ai/autonomy-is-a-spectrum/) answered it for tasks: "earned" means measured, on your own work [9]. Here is the measurement for a model's decisions.

---

## 📏 Accuracy is the wrong dial

Headline accuracy is one number for the whole system, averaged over lopsided traffic. A rare, high-harm class can score near zero while the average looks fine. Autonomy is granted per class, so accuracy can't tell you which decisions to hand over.

Worse, the training that buys accuracy spends something else. Guo and colleagues put a 1998 LeNet next to a 2016 ResNet: the old network was less accurate and its confidence matched its accuracy; the new one was more accurate and "substantially" surer than it had any right to be [2]. The dial that matters first is **calibration**: a model that says 0.9 should be right nine times in ten.

**Temperature scaling** fixes it with one scalar *T* fitted on held-out data: divide the logits by *T* and confidence starts meaning what it says. Their ResNet-110 went from 16.5% calibration error to 1.3%, and the fix "does not affect the model's accuracy": the argmax doesn't move [2]. The number gets honest, which is what lets a threshold on it mean something.

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-reliability.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-reliability.png" alt="Reliability diagrams before and after temperature scaling: before, the bars sit well below the perfect-calibration diagonal (ECE 16.5%); after, they sit on it (ECE 1.3%), with the same decisions" width="1000px"/>
</a>

One caveat that matters for anything that reads text: text classifiers calibrate less cleanly. On 20 Newsgroups the same fix only got from 8.0% to 4.1% [2]. Calibrate, then measure. Don't assume.

---

## 🎛️ The abstention threshold is the autonomy dial

Chow priced the trade in 1957 and again in 1970: a classifier allowed to say *I don't know* buys lower error with lower coverage [1]. The reject option is older than almost everyone now rediscovering it. **Selective classification** brings it to deep networks [3]: pick a threshold **τ** on calibrated confidence. Above τ the model decides; below it, a person does.

Plot error among the decided items against the share decided and you get a **risk–coverage curve**. Draw the error budget across it, 1% here, and the curve reads off how much traffic the model may handle alone.

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-risk-coverage.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-risk-coverage.png" alt="Risk–coverage curves from published selective-classification results: at a 1% error budget a CIFAR-10 model decides 78.6% of inputs alone, while a CIFAR-100 model at 2% decides only 21.3%; the same CIFAR-10 model at full coverage errs 6.5%" width="1000px"/>
</a>

The published numbers make the point. A CIFAR-10 model that errs 6.5% at full coverage keeps error under 1% on the 78.6% of inputs it is surest about. Give the method 100 classes instead of 10, and at a 2% budget it decides 21.3% of the traffic; a person takes the rest [3].

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

Not everything belongs in the model. What a category *means* for the decision (how far back to look, which outcomes are excluded, what gets reported) is a lookup a person writes, versions and signs. Rules change by statute and by client, not by gradient. **And whoever writes the letter is owed the rule that fired, not a logit.**

The law is written the same way. The FCRA requires "reasonable procedures to assure maximum possible accuracy" [4], and its reporting-period limits cap most adverse items at seven years while leaving convictions out of the limit: a look-back window and an exclusion, written by Congress. Employment decisions weigh the *Green* factors, offense, time since, and job, which courts have applied since 1975 and which outlive the EEOC's 2012 guidance now headed for rescission [5]. The CFPB withdrew its advisory opinions on name-only matching and background screening in May 2025 [7]. *The guidance was withdrawn; the duty was not.* And when Medicare regulators were asked about algorithms in coverage decisions, they gave this section in one sentence: "artificial intelligence cannot be used to shift the coverage criteria over time" [10].

---

## 🧾 The audit record

Every decision emits one record: **input hash · model version · data-manifest id · calibration version (T and the τ table) · labels and confidences · policy version · rule fired · decision · reviewer, if it was routed.** Nine fields, none exotic; most systems log half of them in four different places. The EU's AI Act asks for the same thing of high-risk systems: "automatic recording of events (logs) over the lifetime of the system" [11].

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-where-the-model-sits.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-where-the-model-sits.png" alt="Where the model sits: a record feeds a classifier; a τ gate passes confident answers to a versioned rules engine and drops the rest to a human review lane; reviewer overrides flow back to the classifier as training labels; an audit record captures input hash, model version, data-manifest id, calibration version, labels and confidences, policy version, rule fired, decision and reviewer" width="1000px"/>
</a>

Three slots and a lane. The classifier reads the free text and emits a label with a calibrated confidence. The τ gate, one dial per class, passes what the class has earned and drops the rest to a person. The policy engine reads the coded fields through versioned rules and emits the decision with the rule that fired. And the loudest arrow on the page runs backward: a reviewer's override comes home as a label. Part 1's thesis, still working.

Back to the letter. Look up the input hash; read off the model, the confidence, the rule, the reviewer. Replay it. The thirty-day clock becomes an afternoon, and if the line was wrong, the correction goes back as a label like any other override.

---

## 🚨 The loop closes — and the alarm

Overrides return as labels. Retraining runs on a trigger, not a calendar, behind the automated evaluation Part 2 put in place of the governance meeting. And the drift alarm watches one number first: **coverage at a fixed τ**.

**Coverage falls before accuracy does.** Accuracy needs labels, and labels arrive late: after a review, a dispute, a quarter. Coverage needs nothing. When inputs turn unfamiliar, confidence drops below τ and more traffic routes to people. The queue grows before anyone can measure the error rate.

<a href="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-drift-alarm.png">
    <img src="https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/hootl-drift-alarm.png" alt="Table: BERT fine-tuned in one domain and tested in another — accuracy, calibration error and the temperature it needs all move with the shift; the fitted temperature rises from about 1.0–1.3 in-domain to 1.4–3.6 out of domain" width="1000px"/>
</a>

The published record supports the alarm and bounds it. Fine-tune BERT on one dataset, test it on a shifted one, and the temperature it needs rises with the shift, from about 1.0 to as much as 3.6 [12]: the dial moving before anyone has labels. But a model calibrated at home stays too sure abroad. In a question-answering study, an answer given at confidence 0.6 was right 80% of the time in-domain and 45% out of it [13]. It abstained more. It did not abstain enough.

So the alarm is two-sided: coverage leaving its band at a fixed τ, *and* the inputs themselves changing, a vocabulary the model hasn't seen, a new jurisdiction's format. Either one moves a class back down a rung. That's not a failure. That's the system working.

---

## 🌐 Same shape, other domains

Prior authorization, benefits, content moderation: the ladder, the rules layer and the audit record carry over; only the taxonomy and the budget change. A Medicare Advantage insurer is defending a suit alleging its coverage algorithm's denials were reversed about 90% of the time on appeal; the contract claims survived because the insurer's own documents say clinicians decide [14]. The Dutch government fell in January 2021 over a benefits-fraud model whose "use, workings and effect" were hidden from the public [15]: the shrug, at national scale. Meta's Oversight Board, reviewing a handful of the hundreds of thousands of appeals it receives, overturned the company 90% of the time in 2023 [16]. Every one of those is the letter by another name.

---

## ✨ Key Takeaways

* **Autonomy is granted per decision class, on evidence — and revoked the same way.** Nothing starts at HOOTL.
* **The evidence is calibrated confidence and error among the decisions the model takes alone, under a budget.** Headline accuracy can't see it.
* **τ is the autonomy dial.** Coverage at budget places a class on the ladder; a class whose text carries mixed labels never qualifies, and that's a data problem.
* **Rules are not weights.** Versioned, signed, outside the model, so the disputant gets the rule that fired.
* **Coverage at a fixed τ is the early alarm, not the whole alarm.** It falls before accuracy can be measured, and not by enough, so watch the inputs too.

_This is **Part 3** of a series: [Part 1: HITL](https://git-steven.github.io/architecture/ai/ml/aut-ai-hitl/) · [Part 2: HOTL](https://git-steven.github.io/architecture/ai/ml/aut-ai-hotl/)._

---

## 📖 References

1. Chow, C. K. "An Optimum Character Recognition System Using Decision Functions." *IRE Transactions on Electronic Computers* EC-6(4), 1957; and "On Optimum Recognition Error and Reject Tradeoff." *IEEE Transactions on Information Theory* 16(1), 1970.

2. Guo, Chuan, et al. "On Calibration of Modern Neural Networks." *ICML 2017*. Figure 1; Table 1; Section 4.2.

3. Geifman, Yonatan, and Ran El-Yaniv. "Selective Classification for Deep Neural Networks." *NeurIPS 2017*. Tables 1, 2, 5 and 6.

4. Fair Credit Reporting Act: 15 U.S.C. § 1681e(b) (accuracy); § 1681c(a), FCRA § 605(a) (reporting-period limits); § 1681i(a) (30-day reinvestigation; description of the procedure on request).

5. *Green v. Missouri Pacific Railroad Co.*, 523 F.2d 1290 (8th Cir. 1975); U.S. Equal Employment Opportunity Commission, *Enforcement Guidance on the Consideration of Arrest and Conviction Records in Employment Decisions under Title VII*, No. 915.002, 25 April 2012 (draft rescission under OMB review as of October 2026).

6. Federal Trade Commission. "Texas Company Will Pay $3 Million to Settle FTC Charges That It Failed to Meet Accuracy Requirements for Its Tenant Screening Reports," 16 October 2018 (RealPage, Inc.).

7. Consumer Financial Protection Bureau. "Interpretive Rules, Policy Statements, and Advisory Opinions; Withdrawal." 90 Fed. Reg. 20084, 12 May 2025.

8. Miers, Steven. *Semi and Fully Autonomous AI Systems*, [Part 1: HITL](https://git-steven.github.io/architecture/ai/ml/aut-ai-hitl/) and [Part 2: HOTL](https://git-steven.github.io/architecture/ai/ml/aut-ai-hotl/), 2026.

9. Miers, Steven. [*Autonomy is a spectrum, not a switch*](https://git-steven.github.io/architecture/ai/autonomy-is-a-spectrum/), 2026.

10. Centers for Medicare & Medicaid Services. *Frequently Asked Questions related to Coverage Criteria and Utilization Management Requirements in CMS Final Rule (CMS-4201-F)*, 6 February 2024.

11. Regulation (EU) 2024/1689 (the AI Act), Article 12(1) (record-keeping) and Article 14 (human oversight).

12. Desai, Shrey, and Greg Durrett. "Calibration of Pre-trained Transformers." *EMNLP 2020*. Tables 2 and 4.

13. Kamath, Amita, Robin Jia, and Percy Liang. "Selective Question Answering under Domain Shift." *ACL 2020*. Section 5.3.

14. *Estate of Lokken v. UnitedHealth Group*, No. 0:23-cv-03514 (D. Minn.): complaint filed 14 November 2023 (the 90% figure is the plaintiffs' allegation); order on the motion to dismiss, 13 February 2025.

15. Amnesty International. *Xenophobic Machines: Discrimination through Unregulated Use of Algorithms in the Dutch Childcare Benefits Scandal*, EUR 35/4686/2021, 25 October 2021.

16. Oversight Board. *2023 Annual Report*, 2024 (53 decisions; 398,597 appeals received).

---

*Steven Miers — [git-steven.github.io](https://git-steven.github.io)*
