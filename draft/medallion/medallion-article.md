---
title: "🦴 The Lake Needed a Spine: A Field Guide to the Medallion Pattern"
categories:
  - dataengineering
  - architecture
  - datalake
  - medallion
tags:
  - medallion
  - data lake
  - iceberg
  - event sourcing
  - etl
toc: true
---

## 📃 Introduction

A data lake is just a swamp with better marketing — right up until you give it a skeleton.

Dump enough raw files into cheap object storage and you don't get a lake; you get a murky basin where data sinks to the bottom and is never reliably seen again. The fix isn't a fancier query engine or a more expensive warehouse. It's a discipline with a slightly silly name — **bronze, silver, gold** — (reminiscent of the Olympics) and at its heart sits one stubborn rule it quietly borrowed from a corner of software most data engineers never visit:

> 🪨 **Never change what already happened.**

Let's talk about how the medallion pattern actually works, how to build each layer, and why — if you've ever written an event-sourced system — the whole thing is going to feel suspiciously familiar.

## 🐊 The Lake That Became a Swamp

The data lake pitch was intoxicating:

- 💸 Storage is cheap — dump everything in
- 🤸 Schema-on-read — figure out structure *later*
- ♾️ Infinite scale — never size a cluster again

For about six months, it feels like freedom. Then the silt sets in.

- 🌫️ Nobody remembers what's in `s3://data/raw/2019/`
- 🔗 A vendor adds a column and six downstream jobs break — *silently*
- 💥 Two writers hit the same table and leave it half-written
- 🧟 Someone asks *"what did this look like in Q2?"* and the room goes quiet

Phil Karlton quipped that the two hardest problems in computing are cache invalidation and naming things; a swamp is what happens when *finding* and *trusting* your data becomes the third. None of this is exotic — it's the **predictable** result of storing data with no shape.

*(The shift from ETL to ELT — load raw first, transform later — didn't create the swamp, but it did remove the bouncer at the door.)*

The lesson isn't *"go back to rigid warehouses."* It's that **a lake needs a spine.**

![Swamp vs Lake-with-a-spine](/assets/images/lake-vs-swamp.svg)

> 🖼️ **[TEMP — IMAGE DESCRIPTION, DELETE BEFORE PUBLISH]** *(exists: `lake-vs-swamp.svg` / `.drawio`)*
> *Two side-by-side panels under the header "Same water. The difference is whether anything gives it a shape."*
> *• **LEFT — "🐊 The Swamp":** scattered, tilted file icons labeled `final_v2`, `final_REAL`, `copy(3)`, `??.csv` — visual chaos, no structure. Footer: "No ACID · no schema · no time travel" and "'what did Q2 look like?' → silence."*
> *• **RIGHT — "🦴 Lake With a Spine":** an ordered vertical mini-stack — 🪨 Bronze → 🪙 Silver → 🏆 Gold — with connecting arrows. Footer: "ACID · schema evolution · time travel" and "'what did Q2 look like?' → one query."*

## 🦴 The Spine: Three Layers of Trust

The medallion pattern gives the lake a skeleton: three layers, each more refined than the last.

![Bronze, Silver, Gold — the medallion stack](/assets/images/medallion-stack.svg)

> 🖼️ **[TEMP — IMAGE DESCRIPTION, DELETE BEFORE PUBLISH]** *(exists: `medallion-stack.svg` / `.drawio`)*
> *A vertical stack of three rounded boxes joined by downward arrows. Top hint: "raw data in ↓".*
> *• 🪨 **BRONZE** (amber): "Raw · Immutable · Append-only · Iceberg on S3 · partitioned by event_date" — captioned "the insurance policy."*
> *• arrow labeled "dbt + quality gates" →*
> *• 🪙 **SILVER** (gray): "Cleaned · deduped · type-cast · schema-enforced · PII tokenized" — captioned "the contract."*
> *• arrow labeled "dbt + contracts" →*
> *• 🏆 **GOLD** (gold): "Business marts · aggregations · definitions" — captioned "the product."*
> *Bottom hint: "business value out ↓".*

The names borrow from the Olympic podium, and the metaphor is doing real work — each layer is a *higher grade of the same underlying thing*. Here's the part most explainers miss:

> 💡 **ETL/ELT is a data-*movement* strategy. Medallion is a data-*trust* strategy.** One answers *how does data get from A to B?* The other answers *how confident am I in the data at each stage?* They're not competitors. They're answering different questions.

If the progression feels familiar, it should. It's Kent Beck's old mantra wearing a data hat:

> *"Make it work, make it right, make it fast."* — **Kent Beck**

Bronze makes it **exist**. Silver makes it **right**. Gold makes it **useful**. Same discipline, different domain.

## 🪨 Bronze: The Immutable Floor

**What it is:** every record exactly as it arrived, never modified.

**How it's actually built:**

- 🧊 **An open table format on object storage** *(example: Apache Iceberg on S3; alternatives: Delta Lake, Apache Hudi)* — not loose Parquet files, but a table layer that gives you ACID transactions, schema evolution, and time travel over cheap object storage
- ➕ **Append-only** — ingestion writes here and *only* here; nothing updates or deletes
- 📅 **Partitioned by event date** — so a correction to old data touches one partition, not the whole table
- 🔁 **Idempotent ingest** — the same file or event landing twice resolves to one record (dedup on a natural key)

Bronze is the layer you're tempted to skip and the one you'll be most grateful for — your **insurance policy**. Anything downstream can be rebuilt from it, because it never lies and never forgets.

## 🪙 Silver: The Contract

**What it is:** cleaned, conformed, trustworthy data with a stable shape.

**How it's actually built:**

- 🛠️ **dbt models** transform bronze → silver as version-controlled, tested SQL
- 🧹 **Deduplication** on natural keys; **type-casting**; **normalization** of vendor quirks
- ✅ **Great Expectations** gates — distributional checks, not just "is it null"; bad data fails *here*, loudly, instead of leaking into a dashboard
- 🔐 **PII tokenization confirmed** — identifiers swapped for tokens, identity held in a separate service

Silver is the **contract layer**. When a vendor changes their feed, only bronze-to-silver breaks. Everything downstream keeps running against the contract silver promises. That isolation — vendor chaos on one side, business logic on the other — is the whole point.

## 🏆 Gold: The Product

**What it is:** business-ready marts shaped for the people and systems that consume them.

**How it's actually built:**

- 📊 **dbt-published marts** — aggregations, joins, and business definitions ("active customer," "attributed conversion") live here
- 🎯 **Shaped per consumer** — BI tools, ML feature pipelines, and reverse-ETL all read gold
- 🏷️ **Contract-versioned** — a change to a business definition is a reviewed event, not a surprise

Gold is the **product**. When the business redefines "active customer," only silver-to-gold changes — silver stays stable for everyone else.

## 🔁 Wait — Isn't This Just an Event Database?

If you've built a CQRS or event-sourced system, a bell has been ringing for several paragraphs. Let it ring. Fowler describes event sourcing as storing every state change as a sequence of events you never edit, then deriving current state by replaying them. Sound like anyone you know?

| Event Sourcing | Medallion |
|---|---|
| Append-only event log | Immutable bronze |
| Events are facts, never edited | Raw records never overwritten |
| Projections derived from the log | Silver / gold derived from bronze |
| Rebuild state by replaying events | Re-derive marts by reprocessing bronze |
| Temporal query ("state as of T") | Table-format time-travel, e.g. Iceberg ("data as of T") |
| Corrective events (never delete) | Version-2 records (never delete) |

> 💡 **Bronze is an event log for your analytics. The medallion pattern is event sourcing that wandered into the data warehouse and decided to stay.**

But — and this is the part worth saying out loud, because it keeps you honest — they are **analogous, not identical**:

- 🎯 Event sourcing usually replays in **strict order**, per aggregate, to reconstruct an exact object's state
- 🌊 Medallion reprocessing is usually **set-based and idempotent** — re-derive the whole partition, order be damned, as long as the result is deterministic

The shared DNA is **immutability + derivation**; the replay *mechanics* differ. Name the resemblance, then name the seam.

## 🩹 The Payoff: Restatement Without Tears

Here's where the spine earns its keep. The dreaded request:

> *"Can you re-run last March, but with the corrected numbers?"*

In a swamp, that sentence ruins a week. In a medallion lake:

1. The correction lands in **bronze** as a new, versioned record — the original is untouched
2. A **dbt incremental** model re-derives silver and gold from a watermark — just the affected partitions
3. **The table format's time-travel** *(example: Iceberg)* answers *"what did we report on March 1st?"* from the same table

A retroactive correction stops being archaeology and becomes a Tuesday — not a feature you bolt on later, but a property that *falls out of* never overwriting bronze.

> 🖼️ **[TEMP — OPTIONAL IMAGE SLOT, DELETE BEFORE PUBLISH]** *(does not exist yet)*
> *A small left-to-right flow would land well here: a correction enters **Bronze** as a new versioned record → **dbt incremental** re-derives Silver & Gold from a watermark → **time-travel query** answers "as of March 1." Say the word and I'll build it (`restatement-flow.svg` / `.drawio`); otherwise delete this note.*

## ⚖️ When Your Lake Doesn't Need a Spine

Three layers aren't free. Each is more pipeline, more orchestration, more places to break at 2 a.m. Silver earns its keep only when **input is messy** *or* **multiple consumers** need the same cleaned data. Knock out both — clean-on-arrival data, one consumer — and silver becomes an elaborate `SELECT *`.

In that world, collapse to two tiers (raw → curated) and don't apologize.

> *"Everything should be made as simple as possible, but no simpler."* — **Einstein** (give or take a paraphrase)

The value was never the bronze/silver/gold vocabulary. It's the **separation of concerns** — keeping raw, cleaned, and business-ready apart so a vendor change can't ripple into a dashboard. Three boxes are a convenient default, not a commandment.

## 🧰 The Toolbox

The pattern is tool-agnostic, but here's the slate I reached for above — by job, with the trade-offs. The biggest decision is the **open table format**; the rest are fairly settled defaults.

| Tool | Type | Pros | Cons |
|---|---|---|---|
| **Apache Iceberg** | Open table format | Vendor-neutral; read by Athena, Spark, Trino, Snowflake, BigQuery; strong schema & partition evolution | Some ecosystem tooling still maturing; metadata needs periodic compaction |
| **Delta Lake** | Open table format | Mature; best-in-class on Databricks/Spark; strong ML tooling | Historically Spark-centric; shines most inside Databricks' orbit |
| **Apache Hudi** | Open table format | Excellent for high-frequency upserts & CDC; record-level indexing | More operational complexity; steeper learning curve |
| **Amazon S3** | Object storage | Cheap, durable, ubiquitous; deep AWS integration | AWS-coupled; egress costs *(alts: GCS, Azure Blob — same trade per cloud)* |
| **dbt** | Transformation | SQL-native; version-controlled; tested; strong lineage & community | SQL-centric for heavy non-SQL work; needs a separate orchestrator |
| **Great Expectations** | Data quality | Rich distributional checks; docs-as-tests; Python-native | Setup overhead; verbose for trivial checks |

> 💡 **The one real choice here is the table format.** Default to Iceberg for vendor neutrality; pick Delta if you live in Databricks; reach for Hudi if your world is high-frequency upserts. Everything else — object storage, dbt, a quality framework — is a near-default for an AWS-shaped lake.

## 🗝️ Key Takeaways

- 🐊 A data lake without structure is a swamp; the medallion pattern is its spine
- 🪨 **Bronze** = immutable raw (insurance); **silver** = cleaned contract; **gold** = business product
- 🧊 An open table format on object storage *(example: Iceberg on S3)* is what makes immutable bronze, schema evolution, and time-travel real
- 🔁 It's event sourcing in a trenchcoat — same immutability-plus-derivation DNA, different replay mechanics
- 🩹 Restatement becomes trivial *because* you never overwrite bronze
- ⚖️ Use the layers the forces demand; collapse to two when silver does nothing

> 🦴 A lake doesn't become trustworthy by getting bigger. It becomes trustworthy by getting a **shape**.

## 📚 References

- Databricks — *medallion architecture* terminology and lakehouse guidance (~2019–2020)
- Ryan Blue et al. — *Apache Iceberg* (originated at Netflix, ~2017–2018)
- Ralph Kimball — *The Data Warehouse Toolkit* (1996); staging → presentation layering
- Maxime Beauchemin — *Functional Data Engineering* (2018); immutable raw + idempotent transforms
- Martin Fowler — *Event Sourcing* (martinfowler.com, 2005)
- Pat Helland — *Immutability Changes Everything* (CIDR 2015 / ACM Queue)
- James Dixon — credited with coining *data lake* (~2010)
