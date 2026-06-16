---
title: "Drain the Data Swamp, Dig the Data Lake Right"
description: "We'll Add Structure Later" — a Eulogy and a Resurrection
categories:
  - data-engineering
  - architecture
tags:
  - data-lake
  - data-swamp
  - apache-iceberg
  - delta-lake
  - apache-hudi
  - table-formats
  - lakehouse
  - schema-evolution
published: false
toc: true
---

## "We'll Add Structure Later" 
_— a Eulogy and a Resurrection_

![Data Lake turning into Swamp](./data-lake-swamp-header.png)

> "Data is a precious thing and will last longer than the systems themselves."
> 
> _**— Tim Berners-Lee**_

## 🎣 The Lake That Wasn't

*You need a number from the 2019 cohort — something Finance swears got loaded "back when we set up the lake."* Forty minutes later you're spelunking through `raw/2019/`, and here's the haul:

- `events.csv`
- `events_final.csv`
- `events_final_v2_REAL.csv`

Three files. No trustworthy timestamps, no record of which job wrote which, no idea whether the schema drifted between them. **The lake your team spent two years filling isn't a lake. It's a swamp.** 🐊

"Data lake" was always a slightly optimistic name. A lake is clear, contained, *swimmable*. A swamp is where things wander in, sink, and are never reliably seen again. And here's the thing — the difference between the two **isn't the water**. It's whether anything gives the water a **shape**.

![A lake and a swamp hold the same water — the difference is the shape](./data-lake-vs-swamp.svg)

That shape has a name. But before we drain anything, let's get our terms straight.

## 🗂️ A Quick Taxonomy

- **Data Lake** — one store for *all* your data, structured or not, in cheap object storage and open file formats, queried by whatever engine you point at it. Schema deferred to read time. *The promise: dump now, structure later.*
- **Data Swamp** — what a lake becomes when nothing tracks structure, versioning, or provenance. Same files, same storage — but no way to know what's in there, who wrote it, or whether you can trust it. *A lake nobody can swim in.*
- **Data Warehouse** — the governed, transactional alternative the lake was reacting against: schemas enforced on write, fast SQL, correctness baked in — at the cost of price, rigidity, and lock-in.
- **Table Format / Lakehouse** — the plot twist. *We'll get there.* 🧊

## 🏛️ Why Not Just Use a Data Warehouse?

*Fair question — and it deserves a straight answer before we go any further.*

A warehouse — Snowflake, BigQuery, Redshift — already hands you schemas, transactions, and fast SQL. If structure is the goal, why build a lake at all?

Three reasons teams reach *past* the warehouse:

- 💸 **Cost & coupling** — Classic warehouses bind storage to compute and bill a premium for both. A lake decouples them: data sits in cheap object storage, and *any* engine — Spark, Trino, Athena, DuckDB — can read it.
- 🧩 **Shape of the data** — Warehouses want tidy rows and columns. Lakes happily swallow JSON, Parquet, images, audio, log dumps — the messy, semi-structured stuff modern ML actually runs on.
- 🔓 **Open formats** — Your data is plain files you can read with anything, today or in ten years. No vendor's proprietary internals holding it hostage.

So the lake exists for *good* reasons.

### ⚖️ The Catch

Here's what nobody puts on the slide: **a warehouse was quietly doing four jobs for you** — enforcing schemas, running transactions, tracking what changed when, and keeping one version of the truth. Dump raw files into S3 and all four jobs simply… stop getting done.

You kept the cheap, open, flexible part. You threw out the part that kept everyone sane.

> The rest of this piece is about getting that part back — **without giving up the lake**.

## 🏞️ The Promise

*Rewind to the pitch. It was intoxicating.*

**The Solution**: _"Schema-on-Read"_. Stop arguing about column types in a planning meeting. Stop sizing clusters. Land the data *now*, in whatever shape it arrives, and defer all that fussy structure until query time. Storage is cheap, flexibility is infinite, and nobody has to model anything up front.

For a glorious while, it works exactly as advertised. Then "later" arrives.

### 🐊 The Reality

*"Later," it turns out, is where lakes go to die.* With nothing tracking the *state* of your data, the bill comes due all at once:

- ❌ **No ACID** — Two jobs write the same table at once; a reader catches it mid-write and sees a table that never logically existed.
- ❌ **No schema evolution** — Adding one column means rewriting every file, or silently shipping mismatched schemas that break readers downstream.
- ❌ **No time travel** — Overwrite a file and the prior version is *gone*. No "what did this look like last Tuesday."
- ❌ **No safe deletes** — A single GDPR request turns into rewriting whole partitions by hand.
- ❌ **No provenance** — No record of which job wrote which file, when. `events_final_v2_REAL.csv` is a provenance problem wearing a costume.

**These aren't bugs you fix. They're capabilities the lake never had.** Which brings us to the thing it was missing.

## 🧊 The Missing Spine: Open Table Formats

Here's the reframe that changes everything: *a pile of Parquet files isn't a table.* It's a pile of files that happen to share columns and a vague hope.

What turns that pile *into* a table is a **metadata layer** sitting over the files, tracking:

- 📍 which files compose which **version** of the table
- 🧬 the **schema** at each version
- 🗂️ the **partitioning** scheme
- 🗑️ what's been **deleted**

That layer is an **open table format** — Apache Iceberg, Delta Lake, or Apache Hudi. It's the spine the lake was always missing — the thing that finally gives the water a shape.

As Dijkstra argued, a good abstraction doesn't exist to make things *vaguer* — it creates a level where you can finally be *precise*. A table format does exactly that for a heap of files: it's the level at which "the table" becomes a real, queryable thing instead of a folkloric one.

![Iceberg cross-section: data files above the waterline, the metadata layer below](./iceberg-cross-section.svg)

## ⚙️ The Four Superpowers

*Add that metadata layer, and four capabilities you thought required a warehouse come flooding back.*

### ⚛️ ACID Transactions
Snapshot isolation, finally. Writers stop corrupting each other, and readers *always* see a complete, consistent version of the table — even mid-write. No more half-written messes.

### 🔧 Schema Evolution
Add, drop, or rename columns without rewriting a single data file; old rows return `null` for new columns. **The schema lives in the metadata, not in the bytes** — so evolving it is a bookkeeping change, not a migration.

### 🔭 Time Travel
Query the table as of any past snapshot or timestamp. Old versions don't vanish — they're just earlier entries in the log. (More on why that's quietly a superpower below.)

### ✏️ Safe Upserts & Deletes
`MERGE` and `DELETE` that touch only what they must, instead of bulldozing whole partitions. That GDPR request? One statement.

### 🧩 The Mechanics
*One design choice unlocks all four at once.* Every write appends a new **snapshot** pointing at a set of **manifests**, which list the **data files** for that version. Nothing is ever mutated in place — you only ever *append*. Reads pin to a snapshot, so they stay consistent; writes never stomp on readers.

![Format enforcement: schema checked on write, snapshots appended, readers always consistent](./table-format-enforcement.svg)

## 📜 Schema-on-Read Was a False Choice

*Remember "The Solution" from a few sections back?* Time to come clean about it.

We were sold a binary:

- **Schema-on-write** — rigid, governed, correct. The warehouse.
- **Schema-on-read** — flexible, chaotic, cheap. The lake.

Pick your poison and live with the tradeoff.

**Except it was a false binary the whole time.** Table formats quietly introduced a third option — **schema-full storage**: the schema is enforced on write and lives in the metadata, but the files stay open and the compute stays decoupled. Schema-on-write *governance* with schema-on-read *flexibility*. You were never actually choosing between rigid and chaotic.

> *A data lake without a table format is a swamp. A data lake with one is a warehouse that forgot it was supposed to be expensive.*

## 🆚 Iceberg vs Delta vs Hudi

*Three formats, same mission, different centers of gravity.*

| Format | Origin | Strength | Watch out for |
|---|---|---|---|
| **Apache Iceberg** | Netflix (~2017–18) | Vendor-neutral; read by Athena, Spark, Trino, Snowflake, BigQuery, DuckDB; strong schema & partition evolution | Some tooling still maturing; metadata needs periodic compaction |
| **Delta Lake** | Databricks | Mature; superb inside Databricks/Spark; strong ML tooling | Historically Spark-centric |
| **Apache Hudi** | Uber | Built for high-frequency upserts & CDC; record-level indexing | More operational complexity |

Short take:

- 🧭 Want vendor neutrality and the broadest engine support → **Iceberg**.
- 🧱 Living inside Databricks → **Delta**.
- 🌊 Drowning in high-frequency upserts or CDC → **Hudi** earns its complexity.

### 🏠 The Lakehouse
Put any of these on top of your lake and you've built what Databricks named a **lakehouse** — a lake that behaves like a database. Cheap, open storage *plus* warehouse-grade correctness. The name is marketing; the capability is real.

## 🔭 The Time-Travel Party Trick

*Time travel sounds like a gimmick — until the Tuesday it saves your job.*

- 📉 A dashboard number looks wrong → diff today's snapshot against yesterday's.
- 🔍 An auditor asks what a table held on a date → query it *as of* that timestamp.
- 💥 A bad batch job lands → roll back to the snapshot before it ran.
- 🧪 A model needs reproducible training data → pin it to a snapshot ID.

None of this required planning ahead. **The format was keeping the history whether you asked it to or not.**

## ⚖️ When You Don't Need a Spine

*Honest moment: a table format isn't free.* Metadata needs occasional compaction, there's a learning curve, and you've added one more layer to reason about. Sometimes plain Parquet in a folder is the *right* answer:

- the data is **clean on arrival**, **read once**, by a **single consumer**
- it's a throwaway export, a one-off analysis, a staging hop
- nobody will *ever* ask "what did this look like last month"

> *Everything should be made as simple as possible, but no simpler.* — Einstein (paraphrase)

The spine earns its keep the moment you have **messy input** *or* **more than one consumer**. Below that bar, it's just ceremony.

## 🗝️ Key Takeaways

- 🌊 A data lake is just cheap object storage — what makes it *trustworthy* is a **table format** layered on top.
- 🐊 Lakes silt into swamps because raw files have **no ACID, no schema history, no provenance, no time travel**. A table format gives all four back.
- 📜 "Schema-on-read vs schema-on-write" was a **false binary** — **schema-full storage** is the third option: governed *and* flexible.
- 🆚 **Iceberg** for vendor-neutral breadth, **Delta** inside Databricks, **Hudi** for high-frequency upserts/CDC.
- ⚖️ Skip the spine only when data is clean-on-arrival, read once, by a single consumer.

> 🔜 *Next in the series:* once your lake has a spine, the **medallion pattern** is how you organize *trust* on top of it.

## 📚 References

- James Dixon — credited with coining *data lake* (~2010)
- Ryan Blue et al. (Netflix) — *Apache Iceberg* (~2017–2018)
- Databricks — *Delta Lake* and the *lakehouse* framing (~2019–2020)
- Uber — *Apache Hudi*
- Maxime Beauchemin — *Functional Data Engineering* (2018)
- Pat Helland — *Immutability Changes Everything* (CIDR 2015)
- Martin Kleppmann — *Designing Data-Intensive Applications* (2017)
