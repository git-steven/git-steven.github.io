---
title: "Drain the Data Swamp, Dig the Data Lake Right"
author: steven
description: '"We''ll Add Structure Later" — a Eulogy and a Resurrection'
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
published: true
toc: true
---

## "We'll Add Structure Later"
_— a Eulogy and a Resurrection_


![A data lake: metadata gives the water a shape](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/datalake/data-lake.png)

> "It was on display in the bottom of a locked filing cabinet stuck in a disused lavatory with a sign on the door saying 'Beware of the Leopard.'"
>
> _**— Douglas Adams, The Hitchhiker's Guide to the Galaxy (1979)**_

## 🎣 The Lake That Wasn't

*You need a number from the 2019 cohort — something Finance swears got loaded "back when we set up the lake."* Forty minutes and a lot of `aws s3 ls` later, you're spelunking through `raw/2019/`, and here's the haul:

- `events.csv`
- `events_final.csv`
- `events_final_v2_REAL.csv`

Three files. No trustworthy timestamps, no record of which job wrote which, no idea whether the schema drifted between them. Whoever named the third one left the company in 2021. **The lake your team spent two years filling isn't a lake. It's a swamp.** 🦠

![A data swamp: no metadata, no shape — just question marks](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/datalake/data-swamp.png)

"Data lake" was always a slightly optimistic name. A lake is clear, contained, *swimmable*. A swamp is where things wander in, sink, and are never reliably seen again. And here's the uncomfortable bit: the difference between the two **isn't the water**. Same files, same bucket, same Parquet, same monthly bill. It's whether anything gives the water a **shape**.

That shape has a name: an **open table format** — Apache Iceberg, Delta Lake, or Apache Hudi. One metadata layer is the whole difference between the two pictures above.

> *A data lake without a table format is a swamp. A data lake with one is a warehouse that forgot it was supposed to be expensive.*

So that's the tour: how that layer works, what it hands back to you, and the handful of times you're honestly fine without it.

## 🧊 The Missing Spine: Open Table Formats

The whole thing turns on one sentence: *a pile of Parquet files isn't a table.* It's a pile of files that happen to share columns and a vague hope.

What turns that pile *into* a table is a **metadata layer** sitting over the files, keeping receipts on:

- 📍 which files belong to which **version** of the table
- 🧬 the **schema** at each version
- 🗂️ how the thing is **partitioned**
- 🗑️ what's been **deleted**, and when

That layer is the table format. It's the spine the lake was always missing — the thing that finally gives the water a shape.

![The full picture: same water, different shape — one metadata layer is the whole difference](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/datalake/data-lake-vs-swamp.png)

Dijkstra said it best in his 1972 Turing Award lecture: the purpose of abstracting "is not to be vague, but to create a new semantic level in which one can be absolutely precise." A table format does exactly that for a heap of files: it's the level at which "the table" becomes a real, queryable thing instead of a rumor.

![Iceberg cross-section: data files above the waterline, the metadata layer below](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/datalake/iceberg-cross-section.png)

## 🗂️ A Quick Taxonomy

Four terms get used interchangeably in every architecture meeting. They are not interchangeable:

- **Data Lake** — one store for *all* your data, structured or not, sitting in cheap object storage and open file formats, queried by whatever engine you point at it. Schema deferred to read time. *The pitch: dump now, structure later.*
- **Data Swamp** — what a lake becomes when nothing tracks structure, versioning, or provenance. Same files, same storage, same invoice — but no way to know what's in there, who wrote it, or whether you'd stake the quarterly number on it. *A lake nobody can swim in.*
- **Data Warehouse** — the governed, transactional thing the lake was rebelling against: schemas enforced on write, fast SQL, correctness baked in. You pay for all of it in money, rigidity, and lock-in.
- **Table Format / Lakehouse** — the spine above, and the name for a lake that has one. *More on the lakehouse shortly.* 🧊

## 🏛️ Why Not Just Use a Data Warehouse?

*Somebody always asks this right about here, usually the person who signs the invoice.*

A warehouse — Snowflake, BigQuery, Redshift — already hands you schemas, transactions, and fast SQL. If structure is the goal, why build a lake at all?

Three reasons teams keep reaching *past* the warehouse:

- 💸 **Cost & coupling** — Classic warehouses weld storage to compute and charge a premium for both. A lake pries them apart: data sits in cheap object storage, and *any* engine — Spark, Trino, Athena, DuckDB — can read it.
- 🧩 **Shape of the data** — Warehouses want tidy rows and columns, thank you. Lakes happily swallow JSON, Parquet, images, audio, log dumps — the messy, semi-structured stuff modern ML actually runs on.
- 🔓 **Open formats** — Your data is plain files you can read with anything, today or in ten years. No vendor's proprietary internals holding your history hostage.

So no, the lake wasn't a mistake. It exists for genuinely good reasons.

### ⚖️ The Catch

Here's what nobody puts on the slide: **a warehouse was quietly doing four jobs for you** — enforcing schemas, running transactions, tracking what changed when, and keeping one version of the truth. Dump raw files into S3 and all four jobs simply… stop getting done. Nobody sends a notice.

You kept the cheap, open, flexible part. You threw out the part that kept everyone sane.

> Table formats are how you get that part back — **without giving up the lake**. But first: how did we all end up in the swamp?

## 🏞️ The Promise

> "A beginning is the time for taking the most delicate care that the balances are correct."
>
> _**— Frank Herbert, Dune (1965)**_

*Rewind to the pitch. It was intoxicating.*

**The Solution**: _"Schema-on-Read"_. Stop arguing about column types in a two-hour planning meeting. Stop sizing clusters. Land the data *now*, in whatever shape it arrives, and defer all that fussy structure until query time. Storage is cheap, flexibility is infinite, and nobody has to model anything up front.

For a glorious while, it works exactly as advertised. Then "later" arrives.

### 🦠 The Reality

*"Later," it turns out, is where lakes go to die.* With nothing tracking the *state* of your data, the bill comes due all at once — four capabilities you quietly lost:

- ❌ **No ACID** — Two jobs write the same table at once; a reader catches it mid-write and sees a table that never logically existed.
- ❌ **No schema evolution** — Adding one column means rewriting every file, or silently shipping mismatched schemas that break readers downstream.
- ❌ **No time travel** — Overwrite a file and the prior version is *gone*. No "what did this look like last Tuesday."
- ❌ **No safe deletes** — A single GDPR request turns into rewriting whole partitions by hand.

…and a fifth wound running underneath all four:

- ❌ **No provenance** — No record of which job wrote which file, when. `events_final_v2_REAL.csv` is a provenance problem wearing a costume.

**These aren't bugs you fix. They're capabilities the lake never had** — and they're exactly what the metadata spine restores.

## ⚙️ The Four Superpowers

> "Life itself was a grand chemical improvisation... it grew and collapsed and grew again. Catastrophe was just one part of what always happened. It was a prelude to what came next."
>
> _**— James S.A. Corey, Caliban's War (2012)**_

*Add that metadata layer, and four capabilities you thought required a warehouse come flooding back.*

### ⚛️ ACID Transactions
Snapshot isolation, finally. Writers stop corrupting each other, and readers *always* see a complete, consistent version of the table — even mid-write. "The report ran during the load" stops being a root cause.

### 🔧 Schema Evolution
Add, drop, or rename columns without rewriting a single data file; old rows return `null` for new columns. **The schema lives in the metadata, not in the bytes** — so evolving it is a bookkeeping change, not a migration you schedule around a long weekend.

### 🔭 Time Travel
Query the table as of any past snapshot or timestamp. Old versions don't vanish — they're just earlier entries in the log. (This one earns a whole section of its own below.)

### ✏️ Safe Upserts & Deletes
`MERGE` and `DELETE` that touch only what they must, instead of bulldozing whole partitions. That GDPR request? One statement.

### 🧩 The Mechanics
*All four fall out of one design choice, and it's almost boringly simple.* Every write appends a new **snapshot** pointing at a set of **manifests**, which list the **data files** for that version. Nothing is ever mutated in place — you only ever *append*. Readers pin to a snapshot and stay consistent; writers never stomp on them. It's `git` for your table: commits, history, and all.

The bonus fifth capability comes free with the receipts. That append-only log *is* **provenance** — a standing record of which write produced which files, and when. `events_final_v2_REAL.csv` never happens again, because nobody ever needs to invent it.

![Format enforcement: schema checked on write, snapshots appended, readers always consistent](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/datalake/table-format-enforcement.png)

## 📜 Schema-on-Read Was a False Choice

*Remember "The Solution" from a few sections back?* Time to come clean about it.

We were sold a binary:

- **Schema-on-write** — rigid, governed, correct. The warehouse.
- **Schema-on-read** — flexible, chaotic, cheap. The lake.

Pick your poison and live with the tradeoff.

**Except it was a false binary the whole time.** Table formats quietly introduced a third option — **schema-in-metadata**: the schema is enforced on write and lives in the metadata, but the files stay open and the compute stays decoupled. Schema-on-write *governance* with schema-on-read *flexibility*. You were never actually choosing between rigid and chaotic. You were choosing between having metadata and not having it.

## 🆚 Iceberg vs Delta vs Hudi

*Three formats, same mission, three very different personalities.*

| Format | Origin | Strength | Watch out for |
|---|---|---|---|
| **Apache Iceberg** | Netflix (2017; open-sourced 2018) | Vendor-neutral; read by Athena, Spark, Trino, Snowflake, BigQuery, DuckDB; strong schema & partition evolution | Some tooling still maturing; metadata needs periodic compaction |
| **Delta Lake** | Databricks (open-sourced 2019) | Mature; superb inside Databricks/Spark; strong ML tooling | Historically Spark-centric |
| **Apache Hudi** | Uber (2016) | Built for high-frequency upserts & CDC; record-level indexing | More operational complexity |

Pick one in thirty seconds:

- 🧭 Want vendor neutrality and the broadest engine support → **Iceberg**.
- 🧱 Already living inside Databricks → **Delta**, and don't overthink it.
- 🌊 Drowning in high-frequency upserts or CDC → **Hudi** earns its complexity.

### 🏠 The Lakehouse
Put any of these on top of your lake and you've built what Databricks popularized as the **lakehouse** — a lake that behaves like a database. Cheap, open storage *plus* warehouse-grade correctness. The name is marketing; the capability is real.

## 🔭 The Time-Travel Party Trick

*Time travel sounds like a gimmick — until the Tuesday it saves your job.*

- 📉 A dashboard number looks wrong → diff today's snapshot against yesterday's.
- 🔍 An auditor asks what a table held on some date in 2023 → query it *as of* that timestamp.
- 💥 A bad batch job lands at 3am → roll back to the snapshot before it ran.
- 🧪 A model needs reproducible training data → pin it to a snapshot ID.

None of this required planning ahead. **The format was keeping the history whether you asked it to or not.**

## ⚖️ When You Don't Need a Spine

*Honest moment: a table format isn't free.* Metadata needs occasional compaction, there's a learning curve, and you've added one more layer to reason about at 2am. Sometimes plain Parquet in a folder really is the *right* answer:

- the data is **clean on arrival**, **read once**, by a **single consumer**
- it's a throwaway export, a one-off analysis, a staging hop
- nobody will *ever* ask "what did this look like last month" — and be honest with yourself about *ever*

> *The eternal mystery of the world is its comprehensibility.* — Einstein, *Physics and Reality* (1936)

The spine earns its keep the moment you have **messy input** *or* **more than one consumer**. Below that bar, it's just ceremony.

## 🗝️ Key Takeaways

- 🌊 A data lake is just cheap object storage with excellent PR — what makes it *trustworthy* is a **table format** layered on top.
- 🦠 Lakes silt into swamps because raw files have **no ACID, no schema history, no time travel, no safe deletes** — plus **no provenance**. A table format gives all four back, and provenance for free.
- 📜 "Schema-on-read vs schema-on-write" was a **false binary** — **schema-in-metadata** is the third option: governed *and* flexible.
- 🆚 **Iceberg** for vendor-neutral breadth, **Delta** inside Databricks, **Hudi** for high-frequency upserts/CDC.
- ⚖️ Skip the spine only when data is clean-on-arrival, read once, by a single consumer. Everything else earns it.

> "We can only see a short distance ahead, but we can see plenty there that needs to be done."
>
> _**— Alan Turing, Computing Machinery and Intelligence (1950)**_

> 🔜 *Next in the series:* once your lake has a spine, the **🥇Medallion Pattern** is how you organize *trust* on top of it.

## 📚 References

- James Dixon (Pentaho) — credited with coining *data lake* (2010)
- Ryan Blue & Dan Weeks (Netflix) — *Apache Iceberg* (2017; open-sourced 2018)
- Databricks — *Delta Lake* (open-sourced 2019) and the *lakehouse* framing
- Uber — *Apache Hudi* (2016)
- Edsger W. Dijkstra — *The Humble Programmer*, ACM Turing Award lecture (1972)
- Maxime Beauchemin — *Functional Data Engineering* (2018)
- Pat Helland — *Immutability Changes Everything* (CIDR 2015)
- Martin Kleppmann — *Designing Data-Intensive Applications* (2017)
- Douglas Adams — *The Hitchhiker's Guide to the Galaxy* (1979)
- Frank Herbert — *Dune* (1965)
- James S.A. Corey — *Caliban's War* (The Expanse, 2012)
- Albert Einstein — *Physics and Reality* (1936)
- Alan Turing — *Computing Machinery and Intelligence* (1950)
