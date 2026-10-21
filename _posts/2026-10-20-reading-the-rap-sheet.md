---
title: "🧾 Reading the Rap Sheet"
tagline: "Teaching a small model to read charge text — and knowing when it shouldn't decide"
excerpt: "A small model reads the charge. A versioned lookup reads the outcome. A threshold decides who gets to decide."
date: 2026-10-14 09:00:00 -0500
categories:
  - architecture
  - ai
  - ml
tags: [ai, ml, calibration, selective-classification, hitl, open-data]
author: steven
published: false
toc: true
---

## 📝 Introduction
**A small model reads the charge. A versioned lookup reads the outcome. A threshold decides who gets to decide.**

![Reading the Rap Sheet banner](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/rapsheet-banner.jpg)
> *Finding Not Not Guilty.*
>
> — a real disposition string, 2,437 times

Steven B Miers · October 21, 2026 · v1.01

Three strings in one public court table mean the same thing: `FNG`, `Verdict-Not Guilty`, and, 2,437 times, `Finding Not Not Guilty`. Read literally, *not not guilty* means **guilty**. Nobody meant that. It's what **noisy data** looks like up close: one fact recorded three ways, one of which says the opposite of what it means. A human decodes it in half a second; a regex never will. Above all three sits `Nolle Prosecution` at 714,681 rows, two-thirds of the table. Thirty-six outcome strings in all, and three appear exactly once, which is a lonely way to be a category.

Here's what I built, in plain English. A court record has two text fields that matter: the **charge** (what someone was accused of) and the **disposition** (what the court did about it). A small model reads the charge, sorts it into one of the prosecutor's 77 offense categories, and says *how sure* it is, and means it. Below a certain confidence it doesn't decide; a person does. The disposition gets no model at all. It gets a lookup table a human wrote, versioned, and can defend.

Two fields, two problems, and the mistake most AI-for-records products make is solving both with the same hammer. Thirty-six strings is a *lookup*. Thirteen hundred charge titles, with new ones every year, is a *model*. (Spoiler: the transformer ties the statute book on accuracy, beats it on the rare categories once I stopped starving them, and earns the right to decide alone on three categories out of 68. That last part turns out to be the interesting one.)

Everything is public: the [package and notebook](https://github.com/terracoil/rapsheet), the [data snapshot](https://huggingface.co/datasets/terracoil/rapsheet-charge-titles), the [model](https://huggingface.co/terracoil/rapsheet-legal-bert-small), and every number below, each traced to a run manifest. It's a reference implementation of a methodology, not a screening tool, and nothing in it tries to work out who a record belongs to.

_This is the worked example for [Part 3](https://git-steven.github.io/ai/aut-ai-hootl/) of *Semi and Fully Autonomous AI Systems*: a model earning autonomy one decision class at a time, with real data and real numbers._

## 🧠 Part 1: Concepts

### 🔤 Two vocabularies, one record

**The disposition is a closed vocabulary, and a noisy one.** Thirty-six strings for five outcomes: convicted, acquitted, not prosecuted, vacated, not final. Some of the differences are real procedure (a dismissal isn't a nolle); plenty are noise, the same outcome spelled by different clerks in different decades. A person can read them all in ten minutes, decide each one once, and write the decisions down with a version number. That's `disposition_map.yaml`. `Finding Not Not Guilty` maps to *acquitted*, with a note saying why, so the next engineer doesn't have to rediscover that the clerk meant well. When someone disputes a line on their record, the answer is a rule with a version on it, not a logit. A model would have to *learn* that a double negative is a typo, and could quietly unlearn it at the next retrain.

**The charge title is an open vocabulary, mostly.** There are 1,365 distinct titles, abbreviated by clerks over decades (`RET THEFT/DISP MERCH/<$300/PRECONV`, where `<$300` is the part that matters). We *could* hand-write that lookup, and it would be stale by spring: new statutes add titles, and the legacy case system spelled the old ones differently. A lookup memorizes. A model has a chance at the title it has never seen and, if it's calibrated, the decency to admit when it isn't sure.

The label column isn't innocent either. One of its 78 values, `PROMIS Conversion` (nearly ten thousand rows), isn't an offense; it marks records migrated from the old case system. Same disease as the disposition column: noise that looks like data. (It has a quieter strain, too, which Part 3 runs into head first.)

**Rules are not weights.** The closed vocabulary goes in a lookup a human owns. The open one goes in a model a human supervises.

### 🌡️ What calibration buys us

A softmax output is a score, not a probability, until we make it one. Fine-tuned transformers are often overconfident: the "92%" bucket is right 80% of the time, like a weather app that has never once doubted itself. **Temperature scaling** (Guo et al., 2017) fits one number *T* on held-out data and divides the logits by it. The top answer never changes; only the confidence gets honest, and honest confidence is what the next step spends as a *budget*. (Mine turned out to be honest already. Part 3 has the receipts.)

### 🚦 What abstention buys us

With honest confidence we can set a threshold τ: *below τ, a person decides.* That's **selective classification** (Chow, 1970; Geifman & El-Yaniv, 2017), reported as a risk–coverage curve: for each share of the traffic the model handles alone, what error rate are we accepting? This piece uses a 0.5% budget, applied **per class**. A category earns its threshold only if its validation error stays inside the budget with 95% confidence (the upper end of a Wilson interval), because zero mistakes in thirty rows doesn't prove a half-percent error rate; it proves we looked at thirty rows. What comes out is a table of the categories the model has *earned* the right to decide alone: Part 3's per-gate question, with a number on each gate. (At my budget, it's a short table.)

### 🏛️ Where the model sits

![D1: a record feeds a classifier (category + confidence) and a policy engine (disposition_map v1, look-back, non-conviction exclusion → report / do_not_report / needs_review + the rule that fired); a human-review lane receives low-confidence and needs_review items and sends overrides back as labels; an audit record captures input hash, model version, confidence, policy version, rule fired and reviewer](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/rapsheet-d1-where-the-model-sits.jpg)

Three slots and a lane. The **classifier** emits a category and a calibrated confidence. The **policy engine** reads the disposition through `disposition_map v1`, applies the look-back window and the non-conviction exclusion, and emits `report`, `do_not_report` or `needs_review`, *with the rule that fired*. The **human lane** gets everything below τ and everything the policy flagged, and a reviewer's override comes back as a training label. The **audit record** keeps enough to replay any decision. The baselines are deliberately absent: this is the architecture, not the benchmark.

### 🗃️ The data, in three sentences

One county's public-domain prosecutions table: about 1.08 million charge-level rows, de-identified by the publisher and pulled by query from a SODA open-data portal. The publisher stopped maintaining it in December 2024, but the portal's row timestamps moved as late as April 2026, so every number here traces to a run manifest (query, counts, source timestamp, seeds, git SHA), and the splits are published as a snapshot without identifiers. `race`, `gender`, `age_at_incident`, `judge`, `incident_city`, `law_enforcement_agency` and `unit` are never pulled, nor is `offense_category` (the pre-update label, which would leak the answer), and the loader refuses any frame that carries one.

## 🏗️ Part 2: Build

### 🗺️ The whole pipeline

![D2: three lanes. Data: open-data portal → SodaClient → DispositionsDataset → DatasetSplits → HubSnapshot. Models: majority, title lookup, statute rules, TF-IDF and the encoder all implement one Classifier protocol and are scored by HeadlineMetrics. Decide: LogitStore → TemperatureCalibrator → SelectiveEvaluator → policy engine. A receipts bar: RunManifest.](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/rapsheet-d2-the-whole-pipeline.jpg)

Three lanes, one protocol, and a receipt for everything:

| Component | Job | Why it's here |
|---|---|---|
| 🎣 **SodaClient** | portal → parquet + manifest | A query is a recipe anyone can rerun; a CSV is a snapshot of somebody's afternoon |
| 🛡️ **DispositionsDataset** | refuse, clean, set PROMIS aside | "We never request them" is a promise; the error is a check |
| ⛓️‍💥 **DatasetSplits** | train / val / test / 2023+ | No case straddles the test line, and 2023+ is "the world moved" |
| 📊 **Majority** | always *Narcotics* | The floor: 37%, and embarrassingly hard to beat on a bad day |
| 📖 **Title lookup** | the title's usual label | The dictionary. Can't beat it? Remembering, not reading |
| 📜 **Statute rules** | chapter, act, section → label | The rule a lawyer could write down |
| 🧮 **TF-IDF + LR** | word and character n-grams | A long record of embarrassing transformers on short, stylized text |
| 🧬 **Encoder** | `title [SEP] 720 ILCS 5/24-1.6` → 68 logits | `legal-bert-small` (Chalkidis et al., 2020): a 6-layer BERT, 35M parameters, one new 68-way head, every weight fine-tuned on class-tempered draws |
| 🌡️ **TemperatureCalibrator** | validation logits → *T* | Makes "92%" mean 92% |
| 🚦 **SelectiveEvaluator** | probabilities → τ per class | Decides what the model may decide alone |
| 📍 **RunManifest** | everything → JSON | If a number is in this article, it was in the manifest first |

Every model implements the same three methods (`name`, `fit`, `predict_proba`) and is scored by the same function. Nothing gets graded on a curve.

### 🎣 Pull by query, not by download

```python
params = {'$select': ','.join(COLS.used), '$limit': 50_000, '$offset': offset, '$order': ':id'}
```

`$order=:id` keeps the paging stable, so page 14 means the same rows every time, and the protected columns never appear in `$select`: it's hard to leak what was never downloaded. Rows reported and rows received both say 1,080,014.

### ⛓️‍💥 Split by case, then by time

```python
StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42).split(X, labels, groups=case_ids)
```

Charges in one case share titles, dates and wording. Let them straddle train and test and the model gets graded on homework it has already seen. Everything received from 2023 on is held out entirely.

### 📜 The policy is a file

```yaml
acquitted: [FNG, Verdict-Not Guilty, Finding Not Not Guilty, FNG Reason Insanity]
```

Thirty-six strings, five outcomes, a version number, and a loader that reports what it doesn't recognize instead of guessing. A lookup that guesses is a model with worse documentation.

### 🧩 The transformer

The transformer is the reader, not the decider. `legal-bert-small` (Chalkidis et al., 2020) is a six-layer BERT encoder with a 512-wide hidden state, 35M parameters, pre-trained by masked-language modelling on legislation, contracts and case law. It was never asked to classify anything. Loading it as a sequence classifier does three things: keeps every encoder weight, throws away the masked-language-model head it was pre-trained with, and bolts on one new linear layer from the `[CLS]` vector to 68 logits: 512 × 68 weights drawn from N(0, 0.02²) and 68 zero-initialized biases, about 35k parameters that start from nothing on top of 35M that don't. The head is the only new piece. No new vocabulary, no adapters, no frozen layers, no distillation; the whole network trains end to end, and the head's bias quietly learns roughly the log of how often each class shows up.

**In:** a sentence pair. Segment A is the title exactly as the county spells it, `AGG UUW/VEH/PREV CONVICTION`; segment B is the citation, `720 ILCS 5/24-1.6`. The uncased WordPiece tokenizer lowercases and keeps punctuation, which matters when `<$300` and `>$300` are different charges. Sixty-four tokens is plenty. Nothing else goes in: no disposition, no date, and never a protected column.

**Out:** 68 logits in a fixed label order, 67 named categories plus one fold bucket for anything under 20 training rows. Softmax turns them into a probability per category; the top one is the prediction, and its probability is the confidence Part 3 spends. Everything downstream (the logit adjustment, the temperature, the thresholds) lives in a JSON file next to the weights, not inside them. Load the checkpoint with plain `transformers` and you get a working classifier with none of the policy; load it with `rapsheet` and you get all of it.

### 🧬 The training loop

The 266,439 training rows hold only 1,726 distinct (title, citation) inputs, so the loop encodes each one once and draws them in proportion to how often they occur. Same distribution as drawing rows, at coffee-break prices:

```python
draws = torch.multinomial(weights / weights.sum(), steps * batch_size, replacement=True)
for batch in draws.split(batch_size):
  loss = F.cross_entropy(model(**inputs_at(batch)).logits, targets[batch])
  loss.backward(); optimizer.step(); scheduler.step(); optimizer.zero_grad()
```

No `Trainer`: the weighted draw is the whole trick, and thirty lines of torch show it plainly. The epoch with the lowest validation *negative log-likelihood* wins, because calibration rewards honest probabilities over confident ones. Three epochs took about ten minutes on an Apple-silicon GPU, and a rerun reproduced every number to the last decimal. (Hold on to "in proportion to how often they occur." It comes back to bite.)

## 📊 Part 3: Evaluation

### 📏 The headline table

Four baselines and two runs of the encoder: the first run, and the rerun after I found out what the first one was doing wrong. Two test sets: the stratified test split (33,305 rows) and everything received from 2023 on (19,973). *Rare-class recall* averages the 35 categories with fewer than 500 training rows; *rare-title accuracy* covers titles seen fewer than five times in training.

| Model | Test acc | 2023+ acc | Macro-F1 | Rare-class recall | Rare-title acc |
|---|---|---|---|---|---|
| 📊 Majority (floor) | 37.5% | 31.0% | 0.008 | 0.0% | 5.8% |
| 📖 Title lookup | 95.2% | 94.3% | 0.826 | 74.8% | 59.5% |
| 📜 Statute rules | **96.4%** | **96.0%** | 0.861 | 78.0% | 63.7% |
| 🧮 TF-IDF + LR | 95.3% | 94.3% | 0.823 | 75.2% | **69.0%** |
| 🧬 legal-bert-small, first run | 96.1% | 95.5% | 0.688 | 49.4% | 60.5% |
| 🧬 legal-bert-small, class-tempered | **96.4%** | 95.8% | **0.880** | **85.2%** | 64.7% |

On accuracy, the statute book and the transformer tie: 96.4% each, seven test rows apart, and the rules a fifth of a point ahead on 2023+. Everywhere the small categories count, the transformer wins: macro-F1 0.88 against 0.86, rare-class recall 85% against 78%. Getting there took a rerun, and the honest paragraphs are about why.

**Everyone is fighting over the last point and a half.** Even a perfect memorizer of every (title, citation) pair tops out around 96.7%, because the same input carries different labels on different rows. The category describes the *case*; the title describes the *charge*. A `THEFT` charge gets filed under *Burglary* often enough that no amount of reading will settle it. That's the quieter strain of noise from Part 1.

**The first run starved its small categories.** "In proportion to how often they occur" gives a 25-row category about 14 looks in three epochs. Under 100 training rows, the first run's recall was 17% against the rules' 76%, and 15 named categories never got predicted at all. The fix: draw each category in proportion to the *square root* of its size (that 25-row category now gets about 280 looks), then subtract the tilt back out of the logits so the probabilities still answer for the real class frequencies (Menon et al., 2021). The correction is one number per class, log(real share) − log(tempered share), which is exactly the error the head's bias learned; it lives next to the weights, not inside them, so it can be read, checked and removed. The rerun gets 80% on those small categories, leaves none unpredicted, lifts macro-F1 from 0.69 to 0.88, and *gains* three-tenths of a point of accuracy. I picked which run to feature on validation, by a rule written before looking at test: lower validation NLL *and* higher validation rare-class recall. It won both (0.163 against 0.182; 88% against 49%).

**The legacy dialect.** Half the set-aside `PROMIS Conversion` rows use titles the labeled data never does (`MANUE/DEL 01-15 GR COCAINE/ANLG` is cocaine delivery, spelled the old way). No labels, but confidence still talks. Mean top-class confidence on those rows: title lookup 0.38, statute rules 0.41, TF-IDF 0.72, **the encoder 0.85** (the first run: 0.81). Fixing the small categories made the transformer *more* sure of itself on text it has never seen, which is why the next two sections exist.

### 🌡️ Calibration: the boring choices did the work

![F1: reliability diagram for the test and 2023+ splits; accuracy per confidence bin tracks the diagonal, and about 91% of rows sit above 0.9 confidence](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/rapsheet-f1-reliability.jpg)

**T = 1.00.** Temperature scaling found nothing to fix: calibration error is 0.5% on test and 0.9% on 2023+, before and after. (The first run's *T* was 0.96, a hair underconfident.) Two boring choices had already done the job: picking the epoch by validation NLL, and putting the real prior back with the logit adjustment. The zigzag below 0.6 is small counts: under 3% of rows live there. Two caveats keep this from being a victory lap. Calibrated on familiar data says nothing about a dialect with no labels to check against, and calibrated *on average* isn't calibrated *per class*, which is what the thresholds ask.

### 🚦 Earned autonomy, at a 0.5% budget

**3 of 68 classes** earn a threshold:

| Category | τ | Test: decided alone | Wrong | 2023+: decided alone | Wrong |
|---|---|---|---|---|---|
| Narcotics | 0.9968 | 927 of 12,535 | 3 | 37 of 6,198 | 0 |
| Retail Theft | 0.9931 | 1,782 of 1,925 | 7 | 811 of 904 | 7 |
| Aggravated DUI | 0.6362 | 2,002 of 2,013 | 5 | 536 of 548 | 13 |

Everything else goes to a person. On test, the model decides **14.2%** of rows alone at **0.32%** error. The rerun fixed the small categories and didn't change who earns autonomy: those categories still have far too few validation rows to prove half a percent. Better recall improves what goes to people, not how much the model decides alone. Narcotics, a third of the data and almost always right, earns it on only 927 of its 12,535 test calls: even at the top of the confidence scale its error sits just under the line, and the 95% bound won't round in its favor.

![F2: risk–coverage curves for test and 2023+ with the 0.5% budget line; the per-class policy decides 14% of test rows alone at 0.3% error and 7% of 2023+ rows at 1.5% error](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/rapsheet-f2-risk-coverage.jpg)

The 2023+ column is the one I'd frame. Thresholds earned on cases from before 2023 decide **6.9%** of later cases alone at **1.45%** error, almost three times the budget, mostly plain DUI charges in cases the office filed under something else. The model didn't change; the world did. Thresholds need an owner and a review date, not just a value. On the legacy dialect, the same thresholds would let the model decide 3.9% of rows alone, every one of them as Aggravated DUI.

One global threshold looks better (54% of test rows alone, at 0.45%) until we look inside it: Narcotics runs over budget on test, and four categories run over on 2023+. A global threshold lets the big categories vouch for everybody.

### ⚖️ The budget is a policy decision

![F4: coverage and realized error against the error budget, per-class versus global thresholds, for test and 2023+](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/rapsheet-f4-budget-sweep.jpg)

Half a percent is a number I picked, and it sits far below the roughly 3.3% of rows where the labels disagree with themselves. It asks the model to be more consistent than the people who wrote the labels. Relax it and per-class coverage on test climbs: 14% at 0.5%, 57% at 1%, 74% at 2%, 87% at 5%. From 1% up, per-class error stays under the budget on both test sets, while the global threshold runs over it on 2023+ at five of the eight budgets. Choosing the budget is a person's decision. The sweep makes the trade visible.

### 🔬 Where it's wrong

![F3: the ten most common mistakes on test, led by Burglary → Theft (90), Aggravated Battery → Aggravated Battery Police Officer (68) and Other Offense → Aggravated Battery Police Officer (67)](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/rapsheet-f3-top-confusions.jpg)

Two kinds of mistake: neighboring categories (*Armed Robbery* and *Robbery*) and case-level labels on charge-level text (`THEFT` filed as *Burglary*). 91% of the encoder's test errors fall on inputs that already carried more than one label in training, and in 85% of them the model picked the label that input usually gets. Most of its mistakes are the labels disagreeing with themselves.

### 🌍 The test this data can't run

One county. Every records system spells charges its own way, and the next county's format is the test this dataset can't run; the legacy dialect is a small taste of it. Next: a domain model trained from scratch on this data, and a real cross-jurisdiction test.

## ✨ Key Takeaways

- **Rules are not weights.** Thirty-six noisy strings belong in a versioned lookup a person signs. `Finding Not Not Guilty` is a typo to fix once, not a pattern to learn.
- **Beat the dictionary before we celebrate.** A statute lookup ties a fine-tuned transformer at 96.4%, under a ceiling of about 96.7% set by labels that describe cases, not charges. The transformer's edge is the small categories, and it only showed up after the rerun.
- **Check how sampling is done before we blame the model.** Proportional draws starved the small categories (17% recall); square-root draws plus a logit adjustment took them to 80% at no cost in accuracy, and calibration came along for free (T = 1.00).
- **Autonomy is earned per class, and it expires.** Three of 68 categories earned it at 0.5%; on 2023+ cases their error ran nearly three times the budget.
- **Make the budget visible.** A sweep turns a hidden policy choice into a table a person can sign.

## 📖 References

1. Cook County State's Attorney. *Dispositions* (dataset [`apwk-dzx8`](https://datacatalog.cookcountyil.gov/d/apwk-dzx8), Cook County open-data portal), public domain; no longer maintained as of 30 December 2024. Retrieved 20 October 2026 (1,080,014 rows). Snapshot: [`terracoil/rapsheet-charge-titles`](https://huggingface.co/datasets/terracoil/rapsheet-charge-titles).
2. Guo, Chuan, et al. "On Calibration of Modern Neural Networks." *ICML 2017*.
3. Geifman, Yonatan, and Ran El-Yaniv. "Selective Classification for Deep Neural Networks." *NeurIPS 2017*.
4. Chow, C. K. "On Optimum Recognition Error and Reject Tradeoff." *IEEE Transactions on Information Theory* 16(1), 1970.
5. Chalkidis, Ilias, et al. "LEGAL-BERT: The Muppets straight out of Law School." *Findings of EMNLP 2020*.
6. Wilson, Edwin B. "Probable Inference, the Law of Succession, and Statistical Inference." *Journal of the American Statistical Association* 22(158), 1927.
7. Menon, Aditya Krishna, et al. "Long-tail learning via logit adjustment." *ICLR 2021*.
8. Fair Credit Reporting Act, 15 U.S.C. § 1681c(a) (FCRA § 605(a)): reporting-period limits on adverse information (the look-back window in D1).
9. Miers, Steven. *Semi and Fully Autonomous AI Systems*, [Part 1: HITL](https://git-steven.github.io/ai/aut-ai-hitl/), [Part 2: HOTL](https://git-steven.github.io/ai/aut-ai-hotl/) and [Part 3: HOOTL](https://git-steven.github.io/ai/aut-ai-hootl/), 2026.
10. Miers, Steven. [`rapsheet`](https://github.com/terracoil/rapsheet): package and [notebook](https://github.com/terracoil/rapsheet/blob/HEAD/notebooks/reading_the_rap_sheet.ipynb), 2026. Model: [`terracoil/rapsheet-legal-bert-small`](https://huggingface.co/terracoil/rapsheet-legal-bert-small).

---

*Steven Miers — [git-steven.github.io](https://git-steven.github.io)*
