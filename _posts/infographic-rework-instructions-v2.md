# Infographic Rework Instructions: HITL + HOTL

> **Goal:** Strip loop-area boxes to **icon + title + subtitle only**. Move all
> explanatory text to the right panel. The right panel becomes the
> "component guide" — not a legend, but a readable reference that
> explains each piece with tone matching the articles. The loop area
> becomes clean, scannable, and small enough to shrink the canvas.
>
> Both diagrams should be **domain-generic** — no mention of matching,
> crypto, dispatch, or any specific case study. The articles provide
> the domain context; the diagrams provide the architecture.

## Font Reference

All loop-area box text uses **Architects Daughter**:

- **Title:** 20pt — the icon + component name
- **Subtitle:** 18pt, italic — the short functional descriptor

HTML previews in the tables below show the intended rendering. In
draw.io, set the font to `Architects Daughter`, size as noted, and
toggle italic for subtitles.

---

# Part A: HITL Infographic

## A1. Loop Area — Strip to Title + Subtitle

Strip each box to its **title line** (icon + label, 20pt) and a new
**subtitle** (18pt italic). Remove all sub-bullets, descriptions,
parenthetical notes, and technology references.

<table>
<thead>
<tr>
<th>Box (current)</th>
<th>Title (20pt)</th>
<th>Subtitle (18pt italic)</th>
<th>Delete</th>
</tr>
</thead>
<tbody>
<tr>
<td>🧮 MODEL PREDICTION SERVICE · real-time results (classification/inference)</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🧮 MODEL PREDICTION SERVICE</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Real-Time Inference</span></td>
<td>All current sub-text</td>
</tr>
<tr>
<td>🖼️ PRODUCT UI · surfaces predictions · stores session results · Some users are also expert users...</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🖼️ PRODUCT UI</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Predictions & User Feedback</span></td>
<td>All 3 bullets</td>
</tr>
<tr>
<td>📑 DATA / OUTCOME · PostgreSQL · Neo4j</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">📑 DATA / OUTCOME</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Outcome & Feedback Storage</span></td>
<td><code>PostgreSQL · Neo4j</code></td>
</tr>
<tr>
<td>👥 SESSION CURATION · to review, select and discard: · session data · expert user feedback · selects/discard</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt; color:#BB7C4B">👥 SESSION CURATION</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic; color:#BB7C4B">Governance · Select & Filter</span></td>
<td>All 4 bullets</td>
</tr>
<tr>
<td>🌀 DATA PIPELINE "Data-Wrangling" · discover · clean · validate · normalize · enrich · transform</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🌀 DATA PIPELINE</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Data-Wrangling</span></td>
<td>All 6 sub-items (subtitle already exists — keep as-is)</td>
</tr>
<tr>
<td>🧑‍💻 DEVELOPER TRAINING · Initial development of model · Manually improve data wrangling/pipeline... · Bypass upon subsequent... · Manual intervention if needed</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🧑‍💻 DEVELOPER TRAINING</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Bootstrap & Manual Intervention</span></td>
<td>All 5 bullets</td>
</tr>
<tr>
<td>🧬 MODEL TRAINING SERVICE · batch retraining · hyperparameter tuning · reinforcement learning · ensembling</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🧬 MODEL TRAINING SERVICE</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Batch Retraining & Tuning</span></td>
<td>All 4 bullets</td>
</tr>
<tr>
<td>👥 MODEL GOVERNANCE · validates · approves release</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt; color:#BB7C4B">👥 MODEL GOVERNANCE</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic; color:#BB7C4B">Governance · Validate & Approve</span></td>
<td><code>validates · approves release</code></td>
</tr>
</tbody>
</table>

> **Note:** The two governance boxes (Session Curation, Model Governance) are shown
> in <span style="color:#BB7C4B">**orange (#BB7C4B)**</span> to match the existing
> governance color system. All others use their current fill colors.

**Also strip these free-floating text labels from the loop area:**
- `Curate session data and expert user feedback` (near Data/Outcome → Session Curation arrow)
- `Curated Data; add to DB / Pipeline` (near Session Curation → Data Pipeline arrow)
- `PROVIDE DATASET(S) AND INITIAL HYPERPARAMETERS` (near Developer Training)
- `Manually, Tune Data Wrangling...normalize/augmentation etc.` (diagonal text near Developer Training bypass)
- `Bypasses developer training after bootstrapping...` (curved bypass label)

**Keep these flow labels** (they help the reader follow the ring):
- `PREDICTIONS`
- `SESSION RESULTS & EXPERT USER FEEDBACK`
- `SUBMIT MODEL`
- `RELEASE MODEL PACKAGE`

---

## A2. Right Panel — New Component Guide

Replace the current right-panel legend entries with a unified
**Component Guide**. Keep the line-type legend at the top (Governance
Routing, Governance Boundary, Main Loop, Sub Loop, Potential Bypass).
Below it, add the component guide with this structure. Each entry gets
the icon, the label in bold, and 1-2 sentences max.

**Recommended layout:** Stack vertically, same rounded-rectangle style
as current legend entries but slightly wider. Group by category with
a small category header.

---

### 🔒 GOVERNANCE (breaks the loop)

**👥 SESSION CURATION**
Reviews incoming data and user feedback. Decides what's trustworthy
enough to enter the training pipeline — and what gets thrown out.
This is the first gate that prevents the loop from closing.

**👥 MODEL GOVERNANCE**
QA checkpoint for trained models. Validates performance, checks for
drift or bias, and approves (or rejects) releases. No model reaches
production without human sign-off. This is the second gate.

---

### ⚙️ LOOP COMPONENTS

**🧮 MODEL PREDICTION SERVICE**
Serves real-time inference results (classification, ranking, scoring)
from the currently approved model. The starting point of every loop
iteration.

**🖼️ PRODUCT UI**
Where predictions meet users. Surfaces results, collects interaction
data, and captures expert feedback (ratings, tags, corrections). Some
users are also domain experts whose signal feeds the learning loop.

**📑 DATA / OUTCOME**
Stores interaction outcomes and expert user feedback. The raw material
the curation team will review — not yet filtered, not yet trusted.

**🌀 DATA PIPELINE** *(Data-Wrangling)*
Ingests curated data and prepares it for training: discovery,
validation, cleaning, normalization, enrichment, transformation.
In HITL, this runs in batch — not streaming.

**🧬 MODEL TRAINING SERVICE**
Batch retraining, hyperparameter tuning, ensembling, and reinforcement
learning. Produces candidate models that must pass governance review
before deployment.

**🧑‍💻 DEVELOPER TRAINING**
Initial model development and manual pipeline tuning. Active during
bootstrap; bypassed in subsequent loops unless manual intervention is
needed. The "break glass" path for humans to directly adjust the
system.

---

## A3. Other HITL Recommendations

**Center label:** Keep `HITL System (Human-In-The-Loop) semi-supervised
learning` — no change needed.

**Bottom caption:** Keep as-is. It's the thesis statement of Part 1.

**"Closing the Loop" text box:** The HITL diagram should NOT have one.
That concept belongs to HOTL. If currently present, remove it.

**Domain-specific text:** Remove any mention of PostgreSQL, Neo4j, or
specific technologies from box labels. The right-panel entries above
are intentionally technology-neutral.

**Paper size:** With stripped boxes, you should be able to reduce canvas
width by ~20-25%. The right panel width stays the same; the loop area
compresses.

---

---

# Part B: HOTL Infographic

## B1. Loop Area — Strip to Title + Subtitle

Same principle. Strip to title (20pt) + subtitle (18pt italic).
Remove all sub-bullets.

<table>
<thead>
<tr>
<th>Box (current)</th>
<th>Title (20pt)</th>
<th>Subtitle (18pt italic)</th>
<th>Delete</th>
</tr>
</thead>
<tbody>
<tr>
<td>🧮 MODEL PREDICTION SERVICE · real-time results · (classification/inference)</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🧮 MODEL PREDICTION SERVICE</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Real-Time Inference</span></td>
<td>Both bullet lines</td>
</tr>
<tr>
<td>🖼️ PRODUCT UI/API · surfaces predictions · stores session results · expert users can rate...</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🖼️ PRODUCT UI / API</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Predictions & User Signal</span></td>
<td>All 3 bullets</td>
</tr>
<tr>
<td>📋 DATA · Store: session outcome · feedback</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">📋 DATA</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Outcome & Signal Storage</span></td>
<td><code>Store: session outcome · feedback</code></td>
</tr>
<tr>
<td>🤖 AUTOMATED VALIDATION · anomaly detection · schema enforcement · statistical filters · Curate session data...</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🤖 AUTOMATED VALIDATION</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Replaces Session Curation</span></td>
<td>All 4 bullets</td>
</tr>
<tr>
<td>🌀 DATA PIPELINE "Data-Wrangling" · Streaming · continuous ingestion · validate · clean · transform</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🌀 DATA PIPELINE</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Streaming Data-Wrangling</span></td>
<td>All 5 sub-items</td>
</tr>
<tr>
<td>🧬 MODEL TRAINING SERVICE · continuous retraining · rolling RL · automated ensembling</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🧬 MODEL TRAINING SERVICE</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Continuous Retraining & RL</span></td>
<td>All 3 bullets</td>
</tr>
<tr>
<td>🚀 AUTO-DEPLOY · thresholds · canary · shadow deploy · automated rollback · no human gate</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🚀 AUTO-DEPLOY</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Replaces Model Governance</span></td>
<td>All 5 bullets</td>
</tr>
<tr>
<td>⚡ CIRCUIT BREAKER(S) · auto-halt on: · metric degradation · erroneous model · data drift · kill switch · New in HOTL</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">⚡ CIRCUIT BREAKER(S)</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Auto-Halt & Kill Switch</span></td>
<td>All sub-text</td>
</tr>
<tr>
<td>👥 HUMAN MONITOR(S) · dashboard · alerts · anomaly · flags · observes without gating</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">👥 HUMAN MONITOR(S)</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Observes Without Gating</span></td>
<td>All sub-text</td>
</tr>
<tr>
<td>🧑‍💻 EMERGENCY DEV INTERVENTION · manual developer override · emergency retraining · bypasses automated gates</td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:20pt">🧑‍💻 EMERGENCY DEV INTERVENTION</span></td>
<td><span style="font-family:'Architects Daughter',cursive; font-size:18pt; font-style:italic">Exceptional Use Only</span></td>
<td>All 3 bullets</td>
</tr>
</tbody>
</table>

> **Subtitle design note for HOTL:** The two components that replace HITL
> governance gates use `Replaces [X]` as their subtitle. This does double
> duty — it's a functional descriptor *and* a visual diff from HITL. No
> need for separate `← NEW IN HOTL` markers on the loop boxes when the
> subtitle already says it.

**Also strip these free-floating text labels:**
- `replaces Model Governance` (near Human Monitor — now covered by Auto-Deploy subtitle)
- `intervenes (exceptional case only)` (near Emergency Dev Intervention — now in subtitle)
- `VALIDATED DATA (streaming)` (near Automated Validation → Pipeline arrow)
- `WRANGLED DATASET(S)` (near Pipeline → Training arrow)
- `MODEL PACKAGES` (near Training → Auto-Deploy arrow)
- `VERIFIED MODELS` (near Auto-Deploy → Prediction Service arrow)

**Keep these flow labels:**
- `PREDICTIONS`
- `SESSION RESULTS / USER SIGNAL`
- `USER SIGNAL`
- `observes` (on observation lines — structurally important)

**Strip the "Closing the Loop" text box from the loop center.**
Move its content to the right panel (see below).

---

## B2. Right Panel — New Component Guide

Same structure as HITL, but with HOTL-specific entries and callouts
for what changed. Use a small inline marker `← NEW` or `← REPLACES [X]`
in a contrasting color (orange or teal) in the right panel entries
where the loop subtitle alone doesn't tell the full story.

Keep the line-type legend at top (Main HOTL closed loop, Humans *on*
the loop, Observation, Emergency Intervention).

---

### 🔓 CLOSING THE LOOP

*(This replaces the center text box — give it prominence at the top
of the component guide, before the component entries.)*

**HITL:** Humans gate the loop (approve/reject before proceeding).
**HOTL:** Humans observe the loop (monitor, alert, intervene if
needed). The loop closes. The gatekeeper becomes a watchdog.

---

### 👁️ HUMANS ON THE LOOP (outer ring)

**⚡ CIRCUIT BREAKER(S)** ← NEW IN HOTL
Auto-halts on metric degradation, data drift, or erroneous model
behavior. Triggers rollback or full stop without waiting for a human.
The automated first responder — buys time for humans to diagnose.
Includes kill switch capability.

**👥 HUMAN MONITOR(S)** ← REPLACES MODEL GOVERNANCE
Dashboards, alerts, anomaly flags. Watches the closed loop from
outside — observes without gating. The human no longer approves each
model; they watch for the system learning the wrong thing.

**🧑‍💻 EMERGENCY DEV INTERVENTION**
Manual override when automated recovery fails. Emergency retraining,
pipeline bypass, direct model rollback. Not an operational path —
it's the fire extinguisher behind glass.

---

### 🤖 AUTOMATED LOOP (inner ring)

**🧮 MODEL PREDICTION SERVICE**
Real-time inference (classification, ranking, scoring) from the
currently deployed model. Unchanged from HITL.

**🖼️ PRODUCT UI / API**
Surfaces predictions, stores results, captures user signal. Expert
feedback flows directly into the data layer — no curation meeting
required.

**📋 DATA**
Stores outcomes and user feedback. In HOTL, this is the raw
firehose — filtering happens downstream at Automated Validation,
not upstream at a human curation desk.

**🤖 AUTOMATED VALIDATION** ← REPLACES SESSION CURATION
Anomaly detection, schema enforcement, statistical filters. Decides
programmatically what's clean enough for training. No human gate —
just automated rejection of garbage.

**🌀 DATA PIPELINE** *(Streaming Data-Wrangling)*
Streaming continuous ingestion — not batch jobs. Validates, cleans,
and transforms data in near-real-time. Same operations as HITL,
different cadence.

**🧬 MODEL TRAINING SERVICE**
Continuous retraining, rolling RL, automated ensembling. Models
improve on a streaming cadence, not a weekly schedule.

**🚀 AUTO-DEPLOY** ← REPLACES MODEL GOVERNANCE GATE
Canary and shadow deployments, performance thresholds, automated
rollback. Ships when metrics pass — no human sign-off required.

---

## B3. Other HOTL Recommendations

**Center label:** Keep `HOTL System (Human-On-The-Loop) closed-loop
learning` — with "Closing the Loop" box removed, the center breathes.

**Outer arc label:** Keep `Humans-On-The-Loop (asynchronous oversight)`.

**Bottom caption:** Keep as-is.

**Paper size:** With stripped boxes and center text removed, reduce
canvas width by ~25-30%. The right panel becomes the primary reading
surface; the loop becomes the scannable architecture reference.

---

---

# Part C: General Recommendations (both diagrams)

## C1. Subtitle Design Principles

The subtitles serve three functions simultaneously:
1. **Functional descriptor** — what this component *does* in 2-4 words
2. **HITL↔HOTL diff** (HOTL only) — `Replaces [X]` subtitles let
   readers see the architectural evolution without a side-by-side
3. **Visual rhythm** — the italic 18pt under the bold 20pt creates a
   consistent two-line cadence across all boxes

## C2. Matching Subtitles Across Diagrams

Where possible, HITL and HOTL subtitles should rhyme — similar structure,
different content — so the delta is obvious:

| Component | HITL Subtitle | HOTL Subtitle |
|---|---|---|
| Data Pipeline | *Data-Wrangling* | *Streaming Data-Wrangling* |
| Model Training | *Batch Retraining & Tuning* | *Continuous Retraining & RL* |
| Session Curation / Automated Validation | *Governance · Select & Filter* | *Replaces Session Curation* |
| Model Governance / Auto-Deploy | *Governance · Validate & Approve* | *Replaces Model Governance* |
| Developer Training / Emergency Intervention | *Bootstrap & Manual Intervention* | *Exceptional Use Only* |

## C3. Visual Hierarchy

The reader should scan the diagram in this order:
1. **Title + subtitle** — which article, which architecture
2. **Loop area** — scan the ring, read labels + subtitles, follow arrows
3. **Right panel** — deep-dive on any component that caught their eye

Stripping bullets from the loop makes this work: loop = shape + labels,
right panel = words.

## C4. Box Sizing

Post-strip, all boxes within a category should be the same size — two
lines of text (title + subtitle) creates natural uniformity. This makes
the ring feel intentional rather than organic.

## C5. Right Panel Width

~35-40% of total canvas width. It's now the primary reading surface.
Loop area gets 60-65%.

## C6. Right Panel Font

Consider a slightly smaller font for the right panel descriptions
than for the loop labels. Loop labels need readability at small embed;
right panel is only read at full zoom.

## C7. Side-by-Side Publishing

If both diagrams reach the same canvas size post-rework, consider
publishing them stacked (HITL on top, HOTL below) in a single image
for the Part 2 article. The visual diff between "broken ring with
governance gates" and "closed ring with outer monitoring arc" becomes
immediately apparent.

## C8. Domain Neutrality Check

After rework, search both diagrams for remaining domain-specific
language and replace:

| Remove | Replace with |
|---|---|
| PostgreSQL · Neo4j | *(remove — no tech stack in labels)* |
| expert user | user / domain expert |
| session | interaction / outcome |
| matching | *(remove — articles provide context)* |

The right panel entries and subtitles above are already domain-neutral.
