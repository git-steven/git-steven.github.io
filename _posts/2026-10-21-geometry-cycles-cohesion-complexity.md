---
title: "📐 The Hidden Geometry of Software, Part 2"
date: 2026-10-21 11:11:11 -0500
tagline: "Dependency Cycles, Coupling Between Objects, Cohesion, Cyclomatic and Cognitive Complexity"
excerpt: "Part 2 of The Hidden Geometry of Software. Part 1 measured packages from the outside. Part 2 opens the box: dependency cycles, class coupling, cohesion and complexity, with honest notes on where the thresholds come from."
header:
  teaser: https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig1-zoom-levels.png
categories:
  - sdlc
  - architecture
  - coupling
  - metrics
tags: [architecture, metrics, coupling, cohesion, complexity, python, static-analysis]
author: steven
toc: true
published: false
---
## Part 2
_Dependency Cycles, Coupling Between Objects, Cohesion, Cyclomatic and Cognitive Complexity_

![Coupling Metrics]({{"/assets/images/coupling-metrics-md.png" | relative_url}})
<!-- 🚀 banner: Part 1 opens with an illustrated banner (coupling-metrics-md.png). Add coupling-pt2-banner.png here. -->

## 📃 Introduction

In [Part 1: The Hidden Geometry of Software Coupling](https://git-steven.github.io/sdlc/architecture/coupling/metrics/geometry-coupling/), we measured packages from the **outside**:
* `𝐶ₐ` and `𝐶ₑ`: who depends on you, and who you depend on
* `I`: which way the dependencies point
* `A` and `D`: how far a package has drifted from the Main Sequence

That was the satellite photo. It told us **where** the pain was. It didn't tell us **what kind** of pain it was, any more than a satellite photo tells you the house has termites.
* Is this package welded to its neighbors in a loop? 🔁
* Is this class one class, or three classes in a trench coat? 🧱
* Is this method hard to test, or just hard to read? 🔬

So Part 2 is the home inspection: the person who opens every cabinet, taps on the walls, and says "hmm" a lot. We zoom in from the package graph all the way down to a single method. The good news hasn't changed since Part 1: every metric below is still just **counting things on a graph**. No machine learning. No consultants. Barely any division.

![Fig. 1: Four zoom levels](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig1-zoom-levels.png)

---

## 📦 Package-level metrics

Part 1 already did most of the package-level work: `𝐶ₐ`, `𝐶ₑ`, `I`, `A` and `D`. There's one big thing it left out, and it's the one that quietly breaks all the others.

### 🔁 Dependency Cycles (the Acyclic Dependencies Principle)

#### 📜 The principle

Part 1 covered the **Stable Dependencies Principle**. It has an older, crankier sibling. Robert C. Martin stated it in 1996, and he stated it in capital letters, so you know he meant it:

> THE DEPENDENCY STRUCTURE BETWEEN PACKAGES MUST BE A DIRECTED ACYCLIC GRAPH (DAG). THAT IS, THERE MUST BE NO CYCLES IN THE DEPENDENCY STRUCTURE. -- _Robert C. Martin, "Granularity" (C++ Report, 1996)_

His argument wasn't about elegance. It was about building and shipping. He called the problem **"the morning after syndrome"**: you go home with working code, and you come back the next morning to find it broken, because somebody stayed later than you did. (If you've worked on a team, you've been both people.)

With a single back edge in the graph, Martin's example packages could no longer be released separately:
> They have, in effect, become one large package.

#### ⛓️ Why one back edge matters

```text
orders ──▶ billing ──▶ notifications
  ▲                         │
  └──── needs order data ───┘
```

It always starts innocently. Somebody in `notifications` just needs one little thing from `orders`. Now those three packages form a **strongly connected component** (SCC): every member depends, directly or indirectly, on every other member. It's a group project where nobody can turn in their part alone.
* Change one, and you retest and release all three 🔥
* You can't unit test one in isolation from the other two
* Everything that depends on _any_ of them now depends on _all_ of them

#### 📏 Measuring cycles: from "yes/no" to "how bad?"

A simple yes/no is the right **gate**. But if you've inherited a codebase that already has cycles (and statistically, you have), you need a sense of **severity**:

| Measure                           | Question it answers                         |
|-----------------------------------|---------------------------------------------|
| Is it a DAG?                      | Do we have any cycles at all?                |
| Number of non-trivial SCCs        | How many tangles?                            |
| Size of the largest SCC           | How much of the system is welded together?   |
| Minimum feedback set              | How many edges would we have to cut?         |

Sonargraph's **Relative Cyclicity** shows why size matters more than count. Fifty files caught in one 50-file cycle score **100%**, the worst possible. The same fifty files arranged as twenty-five 2-file cycles score **20%**. Every file is in a cycle either way, but twenty-five small knots are a weekend. One giant knot is a career.

Don't bother counting individual cycles. Inside one SCC the number of distinct loops explodes combinatorially, which is why ArchUnit gives up at 100 by default. Even the tools know when to stop looking.

#### 📖 Reading cycle results

**Measures:** whether you can follow import arrows out of a package and end up back where you started, and if so, how much of the system is caught in the loop.

| Result              | Rating          | Meaning                                                      | Change Strategy                                  |
|---------------------|-----------------|--------------------------------------------------------------|--------------------------------------------------|
| No cycles (a DAG)   | Healthy         | Every package can be built, tested and released on its own   | _Gate it in CI so it stays that way_             |
| A few small tangles | Local tangle    | A handful of packages that are really one package            | _Invert one import, or merge them_               |
| One large SCC       | Big ball of mud | A big slice of the system has to change, test and ship together | _Cut the cheapest edges first; shrink the largest SCC_ |

**Threshold:** **zero** cycles. This one isn't statistical, it's structural: it falls straight out of the principle. The Go compiler enforces it, and NDepend's default rule complains at any count above 0.

**In human terms:** a cycle says _"you can't safely change one of these without the others."_ The largest SCC is the biggest chunk of the system somebody has to keep in their head (and retest) for any change inside it.

#### 🧮 The bridge to Part 1: the SDP can't survive a cycle

Here's the best reason to care, and it takes exactly one line of algebra. I promise it's a short line.

The Stable Dependencies Principle says `I` should **decrease** along every dependency arrow. Walk around the cycle:

```text
I(orders) > I(billing) > I(notifications) > I(orders)
```

That's an M.C. Escher staircase. It looks reasonable one step at a time, and it's impossible as a whole. **Every cycle contains at least one SDP violation.**

It gets worse. Part 1's per-package numbers quietly lie inside a cycle. Each member counts its cycle-mates in `𝐶ₐ` and `𝐶ₑ`, so a package can sit pretty on the Main Sequence while it's welded to an unstable partner. It's a lovely house built on a sinkhole.

So check things in this order:
1. **Acyclic first**: no cycles between packages (ADP)
2. **Then direction**: dependencies point toward stability (SDP)
3. **Then balance**: distance from the Main Sequence (`D`)

If you must compute `I`, `A` and `D` on a graph that still has cycles, collapse each SCC into a single node first. Treat the tangle as what it really is: one package with several names.

#### 🧲 Breaking the cycle

Martin offered two cures, and both have aged better than most 1996 advice:
* **Invert the dependency**: introduce an interface that the _depending_ package owns, and let the other package implement it
* **Extract a new package**: move the shared piece somewhere both can depend on

The detail that makes inversion work is **who owns the interface**:
> Interfaces are very often included in the package that uses them, rather than in the package that implements them. -- _Robert C. Martin, "Design Principles and Design Patterns" (2000)_

Put the interface in the implementer's package, and congratulations, you've added a file and kept the cycle. Put it in its own `order_ports` package (a port, in ports-and-adapters terms) and the loop becomes a ladder:

![Fig. 2: Breaking a dependency cycle](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig2-cycle-break.png)

#### 🔬 What the research says

The evidence is real, but correlational and mostly from Java:
* Across six applications, Oyetoyan, Cruzes and Conradi found that "most defects and defective components are concentrated in cyclic-dependent components."
* Components that **move into** cycles between releases become more defect-prone.
* Cycles also raise the change-proneness of the classes around them. Bad neighborhoods lower property values.

The counterpoint comes from the same field. Al-Mutawa et al. found that most package cycles in Java are **"package local"** (tangles between siblings under one parent), which may not be critical. And nobody has shown that _breaking_ cycles causes fewer defects.

The short version: **cycles are a risk marker, and bigger tangles are worse.** That's less exciting than "cycles cause bugs," but it has the advantage of being true.

#### 🛠️ Enforcing it

**Go** doesn't negotiate. It makes the ADP a compile error:
> It is illegal for a package to import itself, directly or indirectly. -- _The Go Programming Language Specification_

**Python** is more of a "we'll see" language. It tolerates circular imports right up until one blows up with `ImportError: cannot import name ... from partially initialized module`. A `TYPE_CHECKING` import or a function-level import makes the error go away, but the **design** dependency is still there. You've unplugged the smoke detector, not put out the fire.

Since late 2025, **import-linter** can enforce the ADP directly with an `acyclic_siblings` contract:

```ini
[importlinter]
root_package = shop

[importlinter:contract:no-package-cycles]
name = Packages under shop form a DAG
type = acyclic_siblings
ancestors =
    shop
```

Run against the cycle from Fig. 2, it fails and suggests a cut:
```text
Packages under shop form a DAG BROKEN

No cycles are allowed in shop.
It could be made acyclic by removing 1 dependency:

- .orders -> .billing (1 import)
```

Notice that it picked `orders → billing`, not the `notifications → orders` back edge we inverted. The tool finds the _cheapest_ cut, not the _right_ one. Choosing which arrow to flip is still a **design decision**, which is a polite way of saying it's still your job. After adding `order_ports`, the contract passes.

| Ecosystem | Tool                                                           | Checks             |
|-----------|----------------------------------------------------------------|--------------------|
| Python    | import-linter `acyclic_siblings`                               | Packages           |
| Python    | grimp `nominate_cycle_breakers`                                | Suggests edges to cut |
| Python    | tach `forbid_circular_dependencies`                            | Modules (off by default) |
| Python    | pylint `cyclic-import` (R0401), `pydeps --show-cycles`         | Modules            |
| JVM       | ArchUnit `slices()...should().beFreeOfCycles()`, JDepend       | Packages           |
| JS / TS   | `madge --circular`, dependency-cruiser `no-circular`, `import/no-cycle` | Files      |

One gotcha: a codebase can be acyclic **file by file** and still cyclic **package by package**. Martin meant packages. Your linter may not.

---

## 🧩 Class-level metrics

Now we lift the lid off a package and look at the classes inside. There are two kinds of question here:
* **Between classes** (the class graph): who do you lean on (**CBO**), and who are you descended from (**DIT**)?
* **Inside a class**: does it hang together (**LCOM4**), and how much is crammed into it (**WMC**)?

Most of these come from Chidamber and Kemerer's 1994 suite, the best-known set of object-oriented metrics, and also the most argued-about. Academics have been writing "Yes, but…" papers about it for thirty years.

### 🔗 Coupling Between Objects (CBO)

#### 🔢 Part 1's numbers, one level down

```text
CBO(c) = number of other classes that c uses, or that use c
```

Sound familiar? It's Part 1's `𝐶ₐ` and `𝐶ₑ`, at class level, **with the arrows erased**:

```text
CBO = |dependents ∪ dependencies| = 𝐶ₐ + 𝐶ₑ − (classes in both)
```

Think of it as your class's contact list. CBO doesn't care whether you call them or they call you. It just counts how many people you'd have to warn before you change your phone number.

#### 🧮 A small example

`Invoice` uses `Customer`, `TaxTable` and `Ledger`. It is used by `Ledger` and `ReportBuilder`.

| Metric | Value                                     |
|--------|-------------------------------------------|
| `𝐶ₑ`   | 3 (Customer, TaxTable, Ledger)             |
| `𝐶ₐ`   | 2 (Ledger, ReportBuilder)                  |
| CBO    | 4 = 3 + 2 − 1 (`Ledger` is counted once)   |
| `I`    | 3 / 5 = 0.6                                |

Two lessons hide in that table:
* **CBO tells you how entangled a class is.** `I` tells you **which way** the entanglement points, which is exactly the part CBO throws away.
* `Ledger` shows up on both sides. The `Invoice ↔ Ledger` overlap that CBO politely de-duplicates is a **cycle**, just at class level. Cycles are like glitter; once they're in the codebase, you find them everywhere. 🔁

#### 📖 Reading CBO

**Measures:** how many other classes this class is tied to, in either direction.

| CBO     | Rating   | Meaning                                                   | Change Strategy                                   |
|---------|----------|-----------------------------------------------------------|---------------------------------------------------|
| `0`     | Isolated | Uses nothing, and nothing uses it: a standalone value type, or dead code | _Check that it's actually used_     |
| `1–9`   | Typical  | Under the empirical line                                  | _Normal dev pace_                                 |
| `10–14` | Elevated | Past the empirical line, under the expert one             | _Monitor; check `I` to see which way it leans_    |
| `> 14`  | High     | Past both published lines; changes here ripple widely     | _Look for a missing abstraction, or a split_      |

**Threshold:** **9** comes from Shatnawi (2010), fitted on Eclipse (empirical, but one system). **14** comes from Sahraoui et al. (2000), and is expert opinion. The "NASA" values floating around slide decks contradict each other. Linda Rosenberg's own NASA paper says there is "insufficient statistical data" to set good or bad values, and recommends reviewing the outliers instead. Sensible advice that, naturally, never made it into the slide decks.

**In human terms:** CBO is the number of other classes you may have to open, understand or retest when you change this one.

Those bands assume CK's original, both-directions CBO. Which brings us to the fun part.

#### ⚠️ "CBO" isn't one number

Ask four tools for CBO and you'll get four answers, each delivered with total confidence:
* **ckjm** reports CBO as outgoing only (effectively `𝐶ₑ`), with `𝐶ₐ` in a separate column.
* **CK** (Aniche) counts outgoing by default, and offers "CBO Modified" for both directions.
* **NDepend** skips CBO entirely and reports `TypeCa` and `TypeCe`.
* **Python** has no mainstream CK tool at all. Module-level `𝐶ₐ`/`𝐶ₑ` from an import graph (grimp, pydeps) is the practical stand-in.

A threshold tuned on one tool's CBO means nothing on another's. Outgoing-only counts run lower for heavily used classes, so recalibrate before you borrow anyone's numbers. Including mine.

#### 🔬 What the research says

CBO has the best track record of the classic class metrics:
* Basili, Briand and Melo found it significant for fault-proneness (p = 0.0000 for UI classes).
* In a 2013 review of 106 studies, Radjenović et al. concluded that "the best metrics from the CK metrics suite are CBO, WMC and RFC."

Now the bucket of cold water, and it applies to **every** class metric in this article. El Emam et al. found that once you control for class size, "all of these associations disappear." Big classes have more of everything: more coupling, more methods, more bugs, more people afraid to touch them. Keep that in mind before you treat any single number as a verdict.

### 🌳 Depth of Inheritance Tree (DIT)

#### 🪜 Counting the steps

CBO asks who you **use**. DIT asks who you **are**, or at least who your parents were.

```text
DIT(c) = length of the longest path from c up to the root of its hierarchy
```

```python
class Model: ...         # DIT 0 (1 if your tool counts `object`)
class User(Model): ...   # DIT 1
class Admin(User): ...   # DIT 2
```

Easy to compute, surprisingly hard to interpret:
* Tools disagree on whether the root counts, so the same class can be DIT 0 or DIT 1. Off-by-one errors: now available as a metric.
* Under multiple inheritance the hierarchy is a graph, not a tree. Some tools report the longest path, others the number of ancestors.

#### 📖 Reading DIT

**Measures:** how many layers of inherited behavior sit above a class.

| DIT   | Rating    | Meaning                                                | Change Strategy                                          |
|-------|-----------|--------------------------------------------------------|----------------------------------------------------------|
| `0–1` | Flat      | Stands alone, or extends a single base                 | _Normal dev pace_                                        |
| `2–4` | Layered   | Behavior is spread across a few classes                | _Check that each level earns its place_                  |
| `5–6` | Deep      | At the Visual Studio (5) and NDepend (6) guidance      | _Add new behavior by composition, not another subclass_ |
| `7+`  | Very deep | Reading one method can mean reading the whole chain    | _Flatten, or replace inheritance with delegation_       |

**Threshold:** **5** (Visual Studio) or **6** (NDepend: "might be hard to maintain," though "this isn't a strict rule"). Both are vendor guidance, not research findings. Frameworks also run up the score before you've written a line: NDepend notes that classes deriving from WinForms `Control` average a DIT of 5.3. You're born deep.

**In human terms:** DIT is roughly how many class definitions you may have to read to find out what one method call on this class actually does. Inheriting grandpa's watch is nice. Inheriting his 40 overridden methods, less so.

#### 🔬 What the research says

The research can't make up its mind. One study found deeper classes more fault-prone, another found the opposite, and a third found the worst classes in the **middle** of the hierarchy, which is the kind of result that makes researchers quietly change topics. Later reviews rank DIT well below CBO and WMC as a predictor.

#### 🧲 The idea that survives

One idea does hold up, and it ties straight back to Part 1: **inheritance is the strongest efferent dependency there is.** A subclass depends on its parent's _implementation_, not just its interface. Inheriting from a concrete class deep in a tree is a dependency on something concrete and stable, which is a short walk to Part 1's Zone of Pain.

In Python, mixins make depth misleading. `len(cls.__mro__) - 1` counts total ancestors, and pylint's `too-many-ancestors` (R0901) flags classes past 7 by default.

The Gang of Four settled this one before most of us had a job:
> Favor object composition over class inheritance. -- _Gamma, Helm, Johnson & Vlissides, "Design Patterns" (1994)_

### 🧱 Lack of Cohesion of Methods (LCOM4)

#### 🏝️ Count the islands

Coupling is about the edges **between** classes. Cohesion is about the edges **inside** one.

Hitz and Montazeri's **LCOM4** builds a little graph for each class:
* Each **method** is a node
* Connect two methods if they **share a field**, or if one **calls** the other
* `LCOM4` = the number of **connected components** ("islands")

![Fig. 3: LCOM4 islands](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig3-lcom4-islands.png)

The `User` class above has two islands: one about credentials, one about billing. They live together like roommates who share a mailbox and nothing else. That's two classes, and LCOM4 says so out loud. We've all written this class. Most of us have written it more than once.

#### 📖 Reading LCOM4

**Measures:** how many unrelated groups of methods live in one class.

| LCOM4 | Rating       | Meaning                                                              | Change Strategy                              |
|-------|--------------|----------------------------------------------------------------------|----------------------------------------------|
| `0`   | Nothing to measure | No methods besides `__init__` and static methods: a plain record | _Skip it_                                    |
| `1`   | Cohesive     | Every method connects to every other, through fields or calls        | _Leave it alone_                             |
| `2`   | Two jobs     | Two groups of methods that never touch each other's data             | _Split along the islands_                    |
| `3+`  | Several jobs | Several classes sharing one name                                     | _Split, starting with the largest island_    |

**Threshold:** **1**. This one is structural: by definition, a class with more than one island can be split without cutting a single connection. The exception is abstract classes, interfaces and protocols, which score high by design (more on that below).

**In human terms:** LCOM4 is the number of separate jobs a class is doing. Each extra island is a class waiting to be extracted, and it's been waiting patiently.

#### 🐞 Why not plain "LCOM"?

The original 1994 definition counts method pairs that share no fields (`P`) and pairs that do (`Q`), then reports `P − Q`, floored at zero. That floor is fatal. Give three methods the field `x` and a fourth method only `y`:

```text
P = 3, Q = 3   →   LCOM = 0   ("perfectly cohesive")
LCOM4 = 2                     (the 4th method and y are a separate class)
```

A metric that calls an obviously split class "perfectly cohesive" is a smoke detector that only goes off when you open the window. Basili's team found the original LCOM "insignificant in all cases." The naming hasn't helped either: different papers and tools number the variants differently, so "LCOM3" in one tool is somebody else's "LCOM2." **Always define cohesion metrics by formula, not by name.**

#### ☎️ One call changes the answer

The call edges are what make LCOM4 useful. Take an `Order` class whose methods split into `{add_item, total, apply_discount}` and `{send_receipt, email_domain}`. That's LCOM4 = 2.

Now `send_receipt` prints the order total by calling `self.total()`. The islands merge, and **LCOM4 = 1**. The class went from "split this" to "cohesive" because one method genuinely needs the other. One phone call, and the roommates are a family.

#### 🐍 LCOM4 for Python, in 40 lines

No maintained Python tool computes LCOM4 (radon does no class metrics), so here's one using only the standard library:

```python
from __future__ import annotations

import ast
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Lcom4:
  """LCOM4 (Hitz & Montazeri, 1995): the number of connected components in a class's method graph."""

  cls: ast.ClassDef

  def methods(self) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Methods with a receiver (``self``/``cls``), minus ``__init__``, which touches every field."""
    return {node.name: node for node in self.cls.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name != "__init__"
            and node.args.args and not any(getattr(d, "id", None) == "staticmethod" for d in node.decorator_list)}

  @staticmethod
  def touches(method: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Every ``self.<name>`` (or ``cls.<name>``) a method reads, writes or calls."""
    receiver: str = method.args.args[0].arg
    return {node.attr for node in ast.walk(method)
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == receiver}

  def islands(self) -> list[set[str]]:
    """Group methods that share a field or call one another."""
    methods: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = self.methods()
    groups: list[set[str]] = []
    for name, method in methods.items():
      # A method's reach is itself plus every field and method it touches; overlapping reaches merge.
      reach: set[str] = self.touches(method) | {name}
      groups = [g for g in groups if not g & reach] + [reach.union(*(g for g in groups if g & reach))]
    return [g & methods.keys() for g in groups]


class Lcom4Report:
  """Command line: print LCOM4 for every class in a Python file."""

  @staticmethod
  def run(path: str) -> None:
    """Parse ``path`` and report each class's islands."""
    with open(path) as fh:
      tree: ast.Module = ast.parse(fh.read())
    for cls in (node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)):
      islands: list[set[str]] = Lcom4(cls).islands()
      print(f"{cls.name}: LCOM4 = {len(islands)}  {[sorted(i) for i in islands]}")


if __name__ == "__main__":
  Lcom4Report.run(sys.argv[1])
```

```text
$ python lcom4.py order.py
Order: LCOM4 = 2  [['add_item', 'apply_discount', 'total'], ['email_domain', 'send_receipt']]
```

#### 🧪 Pointed at a real codebase

Run across pip 26.2's internals, 82 of the 183 classes with methods score LCOM4 > 1. That sounds like an indictment of pip. It isn't. Read the top of the list and a pattern appears:
* **Interfaces and abstract bases** (`Candidate`, `Requirement`): every abstract stub is its own island, because stubs share no state.
* **Callback hooks** (a resolver reporter whose seven hook methods each stand alone)
* **Alternate constructors** (`from_directory`, `from_wheel`, …), which build a new instance instead of touching the current one

None of those should be split. LCOM4 assumes a class is **state plus behavior**. Abstract classes have no state, which in Part 1's terms means high `A`. **Read LCOM4 on concrete classes, and skip the abstract ones.** The metric isn't wrong; it's just answering a question nobody asked about interfaces.

#### 🔬 What the research says

Cohesion metrics have a weaker predictive record than coupling metrics. SonarQube once computed LCOM4, along with RFC, DIT and NOC, then dropped them because, in their words, "very few people knew what to do with them." Which is honest, and a little sad.

LCOM4 is still worth running for a different reason: when it fires on a concrete class, it hands you the refactoring. Split along the islands, and each new class usually depends on **fewer** things, so `𝐶ₑ` drops too. Most metrics tell you something's wrong. This one draws you the dotted line.

### ⚖️ Weighted Methods per Class (WMC)

#### ➕ Summing the methods

WMC is the bathroom scale of class metrics:

```text
WMC = Σ complexity(method)   over all methods in a class
```

Here's the catch: Chidamber and Kemerer deliberately left "complexity" undefined. So tools fill it in however they like. Some count methods (every method weighs 1); others sum each method's cyclomatic complexity (see the method-level section below). Two "WMC" numbers from two tools are two different metrics wearing the same name tag.

#### 📖 Reading WMC

**Measures:** how much logic lives in one class.

| WMC    | Rating  | Meaning                                              | Change Strategy                              |
|--------|---------|------------------------------------------------------|----------------------------------------------|
| `≤ 20` | Typical | Under Shatnawi's Eclipse-fitted line                 | _Normal dev pace_                            |
| `> 20` | Heavy   | A lot of logic in one place; usually a big class     | _Check LCOM4 and CBO before acting on it_    |

**Threshold:** **20**, from Shatnawi (2010) on Eclipse: empirical, but one system. Other published values (40, 50, 100) are all over the map, and none of them has a primary derivation I could find. Always state the weighting: 20 methods and a total complexity of 20 describe very different classes.

**In human terms:** WMC is how much logic lives in the class. In practice, that's mostly how big it is.

#### 🔬 What the research says

WMC mostly measures size, and it isn't subtle about it. El Emam et al. found WMC correlated with lines of code at ρ = 0.88, and its link to faults vanished once size was controlled. Radjenović's review put it bluntly: WMC "is not really an OO metric."

A bathroom scale won't tell you whether you're muscle or doughnuts, but it's still useful next to other measurements. PMD's `GodClass` rule only fires when high WMC meets low cohesion **and** heavy use of other classes' data. Hold that thought; it's the class map below.

---

## 🔬 Method-level metrics

Last zoom. We're inside a single function now, where the actual `if` statements live.

### 🧮 Cyclomatic Complexity

#### 🧭 Counting test paths

Thomas McCabe defined it in 1976 on a method's control-flow graph:

```text
V(G) = E − N + 2P        (edges, nodes, connected components)
     = decisions + 1     (for structured code)
```

You don't need the graph theory. Start at 1, then add one for every `if`, `for`, `while`, `case`, `except`, and each `and`/`or`.

`V(G)` is the number of **independent paths** through the method, which is the size of a basis set of tests. That's what it measures, and it measures it well: **how many tests you owe**.

#### 📖 Reading cyclomatic complexity

**Measures:** how many independent paths run through a function. The bands below are radon's ranks, with radon's own descriptions.

| V(G)    | Rank | Rating                                         | Change Strategy                          |
|---------|------|------------------------------------------------|------------------------------------------|
| `1–5`   | A    | Low risk: simple block                         | _Normal dev pace_                        |
| `6–10`  | B    | Low risk: well structured and stable           | _Fine; still within McCabe's 10_         |
| `11–20` | C    | Moderate risk: slightly complex                | _Review it; split it if it keeps growing_ |
| `21–30` | D    | More than moderate risk: more complex          | _Refactor before adding to it_           |
| `31–40` | E    | High risk: complex, alarming                   | _Add tests first, then refactor_         |
| `41+`   | F    | Very high risk: error-prone, unstable          | _Add tests first, then refactor_         |

(Radon's word for E is "alarming." Respect a tool that doesn't sugarcoat.)

**Threshold:** **10**, McCabe's own judgment (more on that next). Tool defaults wander: ruff and mccabe use 10 once you turn the rule on, lizard uses 15, and ESLint uses 20, for reasons nobody seems to have written down.

**In human terms:** `V(G)` is the minimum number of test cases it takes to exercise every independent path. A function scoring 12 needs at least 12 tests before all its basis paths are covered. If that function has 2 tests, you now know exactly how much you owe.

#### 📏 The "not magical" 10

The famous limit came from McCabe himself, and he hedged it beautifully:
> The particular upper bound that has been used for cyclomatic complexity is 10 which seems like a reasonable, but not magical, upper limit. -- _Thomas McCabe, "A Complexity Measure" (1976)_

He also exempted large `case` statements. Twenty years later, NIST SP 500-235 (co-written by McCabe) kept 10 as the default and allowed up to 15 only for teams with "experienced staff, formal design… code walkthroughs, and a comprehensive test plan." Every team believes it's that team. "Not magical" remains the most ignored phrase in software metrics.

#### 📊 Complexity lives in the tail

Here's real data from pip 26.2's internals (1,549 functions), measured with radon:

![Fig. 4: Complexity distribution in pip](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig4-complexity-tail.png)

* **86%** of functions get radon's grade A (`V(G)` ≤ 5).
* The **4%** at grade C or worse (`V(G)` > 10) hold **23%** of all the branching.

You don't need to fix the whole codebase. You need to go look at the tail, where the dragons are.

#### 🤔 What it doesn't measure

Two long-standing criticisms, both fair:
* **It's mostly size.** Shepperd (1988) called it "no more than a proxy for, and in many cases is outperformed by, lines of code." Across roughly 1.2 million source files, Jay et al. (2009) found that lines of code explained about 90% of its variation. Ouch.
* **It's blind to nesting.** A flat 10-way `match` and three loops nested inside each other can score the same. Nobody who has read both believes they're the same.

Cyclomatic complexity counts **tests**, not **confusion**. For confusion, we need a different tool.

### 🧠 Cognitive Complexity

#### 🌀 Charging for nesting

SonarSource's **Cognitive Complexity** (G. Ann Campbell) skips the graph math and scores **reading effort** instead. Roughly: how many browser tabs your brain has open at the deepest point of the function.
* +1 for each break in linear flow (`if`, loops, `except`, ternaries)
* **+1 more for each level of nesting** it sits inside
* A whole `switch`/`match` costs +1, not +1 per case
* A run of the same boolean operator (`a and b and c`) costs +1
* `try`, early returns and null-coalescing are free

Here's one Python function, scored both ways:

```python
def shipping_cost(order: Order | None, rates: RateCard) -> float:
  total: float = 0.0
  if order is not None and order.items:          # CC +2 | Cog +1 (if) +1 (and)
    for item in order.items:                     # CC +1 | Cog +2 (nested once)
      if item.weight > 50 and item.fragile:      # CC +2 | Cog +3 (nested twice) +1 (and)
        total += rates.freight
      elif item.weight > 10:                     # CC +1 | Cog +1
        total += rates.heavy
      else:                                      # CC +0 | Cog +1
        total += rates.standard
    try:
      total = rates.discount(total, order.coupon)
    except KeyError:                             # CC +1 | Cog +2 (nested once)
      pass
  return total
```

| Tool                 | Score  | Why it differs                         |
|----------------------|--------|----------------------------------------|
| radon, lizard        | CC 8   | Counts each `and`, matching McCabe     |
| mccabe (flake8 C901) | CC 7   | Ignores `and`/`or`; charges +2 for `try/except` |
| ruff C901            | CC 6   | Ignores `and`/`or`                     |
| Cognitive (by spec)  | **12** | Charges for the nesting                |

Same function, four different answers, zero tools admitting doubt. **"Complexity 8" means nothing without the tool's name.**

The `switch` debate in miniature: a 3-case `match` and the equivalent `if/elif/elif` chain both have CC 4. Cognitive Complexity scores the `match` 1 and the chain 3. People have argued about this on the internet for years, so I'll just leave it here and back away slowly.

#### 📖 Reading cognitive complexity

**Measures:** how hard a function is to follow when you read it top to bottom.

| Score    | Rating         | Meaning                                      | Change Strategy                                              |
|----------|----------------|----------------------------------------------|--------------------------------------------------------------|
| `0`      | Linear         | No breaks in flow; it reads straight through | _Nothing to do. Enjoy it._                                   |
| `1–15`   | Within default | Under SonarQube's and PMD's default limit    | _Normal dev pace_                                            |
| `> 15`   | Flagged        | SonarQube rule S3776 fires                   | _Flatten the nesting: extract the inner loop, invert conditions_ |

**Threshold:** **15** (SonarQube uses 25 for C, C++ and Objective-C, which tells you something about C). It was tuned to cut noise, not derived from data; details next.

**In human terms:** Cognitive Complexity estimates how much a reader has to hold in their head to follow the function, and each extra level of nesting costs more than the last. It's the metric for "I had to read that three times."

#### 📏 Where *its* threshold comes from

The default limit is 15. Campbell was refreshingly candid about where that came from: they started with McCabe's 10, found it "noisy," and nudged it up until the results felt right.
> I guess you're hoping for some scientific formula. I can't give you one. -- _G. Ann Campbell, SonarSource Community (2024)_

I love this quote. It's the most honest sentence ever written about a software metric threshold, and it applies to most of the others too.

It does have some validation. A 2020 meta-analysis of ~24,000 human evaluations found a moderate correlation (r = 0.54) between Cognitive Complexity and how long people took to understand code. That's real. It's also not a defect predictor, so don't sell it as one.

---

## 🗺️ Putting It Together: The Class Map

Part 1 plotted packages on `A` vs `I`. At class level, the useful picture is **size** (WMC) against **entanglement** (CBO), with cohesion (LCOM4) as bubble size:

![Fig. 5: The class map](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig5-class-map.png)

| Zone          | Meaning                       | Typical move                                         |
|---------------|-------------------------------|------------------------------------------------------|
| Healthy core  | Small, loosely coupled         | Leave it alone. Seriously.                           |
| Brain class   | Big, but self-contained        | Extract methods; watch Cognitive Complexity          |
| Hub           | Small, but leans on many       | Check `I`: is it pointing toward stability?          |
| God class     | Big **and** entangled          | Split along the LCOM4 islands first                  |

The threshold lines are Shatnawi's Eclipse-derived values (CBO 9, WMC 20). Treat them as a starting point, not a law. Your own codebase's baseline is a better line than anything fitted on Eclipse in 2010.

---

## 📏 Where the Thresholds Really Come From

Put every threshold in this article side by side, and a pattern jumps out:

| Threshold              | Origin                                              | Kind                        |
|------------------------|-----------------------------------------------------|-----------------------------|
| CC ≤ 10                | McCabe's own projects: "reasonable, but not magical" | Practitioner judgment       |
| Cognitive ≤ 15         | Raised from 10 until it stopped being noisy          | Tuned for noise             |
| ESLint CC 20, lizard 15 | No published rationale found                        | Unknown                     |
| CBO > 14               | Sahraoui et al. (2000)                               | Expert opinion              |
| CBO 9, WMC 20          | Shatnawi (2010), Eclipse only                        | Empirical, one system       |
| DIT ≤ 5 or 6           | Visual Studio and NDepend guidance                   | Vendor guidance             |
| LCOM4 = 1              | The definition: more than one island can be split    | **Structural**              |
| Zero package cycles    | The ADP; the Go compiler enforces it                 | **Structural**              |

Most of these numbers were chosen the way you choose a thermostat setting: somebody tried a few, and one felt right. The numbers that hold up best aren't statistical at all. **Zero cycles** and **one island** follow from what the graph means, not from a regression.

Two findings should keep us all humble (me very much included):
* After controlling for class size, El Emam et al. found that "none of the metrics we studied were associated with fault-proneness anymore."
* Radjenović's review found that **process metrics** (churn, who touched what, how often) predict post-release faults better than any static code metric. Your git log knows more about your bugs than your linter does.

So use these numbers as a **flashlight**, not a **verdict**:
* Name the tool alongside the number
* Ratchet against your own baseline, not someone else's blog post (yes, including this one)
* Gate on the structural ones; investigate the statistical ones

## 🛠️ A Small CI Recipe (Python)

```toml
# pyproject.toml: flag methods past McCabe's 10
[tool.ruff.lint]
extend-select = ["C901"]

[tool.ruff.lint.mccabe]
max-complexity = 10
```

```bash
lint-imports                      # ADP gate: fails on any package cycle (.importlinter above)
radon cc -s -n C src/             # list the complexity tail: grade C and worse
python lcom4.py src/app/models.py # cohesion check on concrete classes
```

The cycle check is a **gate**. The other two are **reports**: they tell you where to look, and a human decides what to do. Metrics are great at pointing. They're terrible at deciding.

## 🗝 Key Takeaways

* Every metric here is **counting on a graph** 🕸️: loops in the package graph, neighbors in the class graph, islands inside a class, paths inside a method.
* **Cycles come first.** Inside a loop, Part 1's `I` and `D` stop describing anything real 🔁.
* **CBO** is `𝐶ₐ` plus `𝐶ₑ` with the arrows erased. Use `I` to get the direction back 🧭.
* **DIT** is shaky as a predictor, but every level of inheritance is a dependency on someone else's implementation 🌳.
* **LCOM4** is the rare metric that hands you the refactoring. Split along the islands ✂️.
* **WMC** is mostly class size. Read it next to CBO and LCOM4, never alone ⚖️.
* **Cyclomatic complexity** counts tests. **Cognitive complexity** counts confusion 🧠.
* Most thresholds are **somebody's educated guess**. The structural ones (zero cycles, one island) are the ones to enforce 📏.

The shape of the system changes. The math still doesn't. And the math, thankfully, is still mostly counting.

## 📚 References

- Martin, R. C. (1996). "Granularity." *C++ Report*, Engineering Notebook column. [PDF](https://staff.cs.utu.fi/~jounsmed/doos_06/material/Granularity.pdf)
- Martin, R. C. (2000). *Design Principles and Design Patterns.* [PDF](https://staff.cs.utu.fi/~jounsmed/doos_06/material/DesignPrinciplesAndPatterns.pdf)
- Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design.* Prentice Hall.
- Lakos, J. (1996). *Large-Scale C++ Software Design.* Addison-Wesley.
- Tarjan, R. (1972). "Depth-First Search and Linear Graph Algorithms." *SIAM Journal on Computing*, 1(2). [doi:10.1137/0201010](https://doi.org/10.1137/0201010)
- Oyetoyan, T. D., Cruzes, D. S., & Conradi, R. (2013). "A study of cyclic dependencies on defect profile of software components." *Journal of Systems and Software.* [doi:10.1016/j.jss.2013.07.039](https://doi.org/10.1016/j.jss.2013.07.039)
- Al-Mutawa, H. A., Dietrich, J., Marsland, S., & McCartin, C. (2014). "On the Shape of Circular Dependencies in Java Programs." *ASWEC.* [doi:10.1109/aswec.2014.15](https://doi.org/10.1109/aswec.2014.15)
- hello2morrow (2025). "Designing a metric to detect big balls of mud." [Blog](https://blog.hello2morrow.com/2025/06/designing-a-metric-to-detect-big-balls-of-mud/)
- Chidamber, S. R. & Kemerer, C. F. (1994). "A Metrics Suite for Object Oriented Design." *IEEE TSE*, 20(6). [doi:10.1109/32.295895](https://doi.org/10.1109/32.295895)
- Basili, V. R., Briand, L. C., & Melo, W. L. (1996). "A Validation of Object-Oriented Design Metrics as Quality Indicators." *IEEE TSE*, 22(10). [doi:10.1109/32.544352](https://doi.org/10.1109/32.544352)
- Briand, L. C., Daly, J. W., & Wüst, J. K. (1998). "A Unified Framework for Cohesion Measurement in Object-Oriented Systems." *Empirical Software Engineering*, 3(1).
- Hitz, M. & Montazeri, B. (1995). "Measuring Coupling and Cohesion in Object-Oriented Systems." *Proc. Int. Symposium on Applied Corporate Computing.*
- El Emam, K., Benlarbi, S., Goel, N., & Rai, S. N. (2001). "The Confounding Effect of Class Size on the Validity of Object-Oriented Metrics." *IEEE TSE*, 27(7). [doi:10.1109/32.935855](https://doi.org/10.1109/32.935855)
- Radjenović, D., Heričko, M., Torkar, R., & Živkovič, A. (2013). "Software fault prediction metrics: A systematic literature review." *Information and Software Technology*, 55(8). [doi:10.1016/j.infsof.2013.02.009](https://doi.org/10.1016/j.infsof.2013.02.009)
- Shatnawi, R. (2010). "A Quantitative Investigation of the Acceptable Risk Levels of Object-Oriented Metrics in Open-Source Systems." *IEEE TSE*, 36(2).
- Rosenberg, L. H. (1998). "Applying and Interpreting Object Oriented Metrics." NASA SATC. [Summary](https://www.cs.purdue.edu/homes/apm/courses/BITSC461-fall03_SoftwareEngineering/metrics-slides/nasa-rosenberg-study.html)
- McCabe, T. J. (1976). "A Complexity Measure." *IEEE TSE*, SE-2(4). [PDF](http://www.literateprogramming.com/mccabe.pdf)
- Watson, A. H. & McCabe, T. J. (1996). *Structured Testing: A Testing Methodology Using the Cyclomatic Complexity Metric.* NIST SP 500-235. [PDF](https://www.mccabe.com/pdf/mccabe-nist235r.pdf)
- Shepperd, M. (1988). "A critique of cyclomatic complexity as a software metric." *Software Engineering Journal*, 3(2). [doi:10.1049/sej.1988.0003](https://doi.org/10.1049/sej.1988.0003)
- Jay, G., Hale, J. E., Smith, R. K., Hale, D., Kraft, N. A., & Ward, C. (2009). "Cyclomatic Complexity and Lines of Code: Empirical Evidence of a Stable Linear Relationship." *JSEA*, 2(3). [doi:10.4236/jsea.2009.23020](https://doi.org/10.4236/jsea.2009.23020)
- Campbell, G. A. (2023). *Cognitive Complexity: A new way of measuring understandability.* SonarSource. [PDF](https://www.sonarsource.com/docs/CognitiveComplexity.pdf)
- Muñoz Barón, M., Wyrich, M., & Wagner, S. (2020). "An Empirical Validation of Cognitive Complexity as a Measure of Source Code Understandability." *ESEM.* [arXiv:2007.12520](https://arxiv.org/abs/2007.12520)
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software.* Addison-Wesley.
- NDepend. "Code Metrics." [Docs](https://www.ndepend.com/docs/code-metrics)
- Tools: [import-linter](https://import-linter.readthedocs.io/en/stable/contract_types/), [grimp](https://github.com/python-grimp/grimp), [radon](https://radon.readthedocs.io/), [ruff C901](https://docs.astral.sh/ruff/rules/complex-structure/), [ArchUnit](https://www.archunit.org/userguide/html/000_Index.html), [dependency-cruiser](https://github.com/sverweij/dependency-cruiser)
