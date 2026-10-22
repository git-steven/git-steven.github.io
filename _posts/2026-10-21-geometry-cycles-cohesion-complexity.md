---
title: "📐 The Hidden Geometry of Software, Part 2"
date: 2026-10-21 11:11:11 -0500
tagline: "Dependency Cycles, Coupling Between Objects, Cohesion (LCOM4), Cyclomatic and Cognitive Complexity"
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

<!-- 🚀 banner: Part 1 opens with an illustrated banner (coupling-metrics-md.png). Add coupling-pt2-banner.png here. -->

## 📃 Introduction

In [Part 1: The Hidden Geometry of Software Coupling](https://git-steven.github.io/sdlc/architecture/coupling/metrics/geometry-coupling/), we measured packages from the **outside**:
* `𝐶ₐ` and `𝐶ₑ`: who depends on you, and who you depend on
* `I`: which way the dependencies point
* `A` and `D`: how far a package has drifted from the Main Sequence

Those numbers told us **where** the pain was. They did not tell us **what kind** of pain it was.
* Is this package welded to its neighbors in a loop? 🔁
* Is this class one class, or three classes sharing a name? 🧱
* Is this method hard to test, or just hard to read? 🔬

Part 2 opens the box. We zoom in four times, from the package graph down to a single method. Every metric below is still just **counting things on a graph**.

![Fig. 1: Four zoom levels](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig1-zoom-levels.png)

### 🧭 What made the cut (and what didn't)

There are dozens of structural metrics. Four of them earn a full section here, and two get a sidebar.

| Metric                          | Zoom level    | Verdict     | Why                                                                                      |
|---------------------------------|---------------|-------------|------------------------------------------------------------------------------------------|
| Package cycles (ADP)            | Package graph | **Feature** | The missing third of Martin's package principles. Part 1's metrics need it to be true.    |
| CBO                             | Class graph   | **Feature** | Part 1's `𝐶ₐ` and `𝐶ₑ`, one level down. The most consistently useful class metric.        |
| LCOM4                           | Class         | **Feature** | One of the few metrics whose value is also a refactoring instruction.                     |
| Cyclomatic + Cognitive          | Method        | **Feature** | Already in your linter. Worth knowing what it really measures.                           |
| WMC                             | Class         | Sidebar     | No fixed definition, and it mostly re-measures class size.                               |
| DIT                             | Class graph   | Sidebar     | Weak, contradictory evidence. One useful idea survives.                                  |

The test for each was simple:
* Does it connect to Part 1's `𝐶ₐ`, `𝐶ₑ` and `I`?
* When it fires, does it tell you **what to do**?
* Does the research hold up?
* Can you run it on Python code today?

---

## 🔁 Package Graph: Dependency Cycles

### 📜 The Acyclic Dependencies Principle

Part 1 covered the **Stable Dependencies Principle**. It has an older sibling. Robert C. Martin stated it in 1996, in capital letters:

> THE DEPENDENCY STRUCTURE BETWEEN PACKAGES MUST BE A DIRECTED ACYCLIC GRAPH (DAG). THAT IS, THERE MUST BE NO CYCLES IN THE DEPENDENCY STRUCTURE. -- _Robert C. Martin, "Granularity" (C++ Report, 1996)_

His argument was about building and shipping, not about elegance. He called it **"the morning after syndrome"**: you leave working code at night and come back to find it broken, because somebody else stayed later than you.

With one back edge in the graph, Martin's example packages could no longer be released separately:
> They have, in effect, become one large package.

### ⛓️ Why one back edge matters

```text
orders ──▶ billing ──▶ notifications
  ▲                         │
  └──── needs order data ───┘
```

Those three packages now form a **strongly connected component** (SCC): every member depends, directly or indirectly, on every other member.
* Change one, and you retest and release all three 🔥
* You can't unit test one in isolation from the other two
* Everything that depends on _any_ of them now depends on _all_ of them

### 🧮 The bridge to Part 1: SDP can't hold inside a cycle

This is the strongest reason to care, and it takes one line of algebra.

The Stable Dependencies Principle says `I` should **decrease** along every dependency arrow. Walk around the cycle:

```text
I(orders) > I(billing) > I(notifications) > I(orders)
```

That's impossible. **Every cycle contains at least one SDP violation.**

Worse, Part 1's per-package numbers quietly lie inside a cycle. Each member counts its cycle-mates in `𝐶ₐ` and `𝐶ₑ`, so a package can look balanced on the Main Sequence while it is welded to an unstable partner.

The fix is to check in order:
1. **Acyclic first**: no cycles between packages (ADP)
2. **Then direction**: dependencies point toward stability (SDP)
3. **Then balance**: distance from the Main Sequence (`D`)

If you must compute `I`, `A` and `D` on a graph that still has cycles, collapse each SCC into a single node first.

### 🧲 Breaking the cycle

Martin offered two cures, and both still work:
* **Invert the dependency**: introduce an interface that the _depending_ package owns, and let the other package implement it
* **Extract a new package**: move the shared piece somewhere both can depend on

The detail that makes inversion work is **who owns the interface**:
> Interfaces are very often included in the package that uses them, rather than in the package that implements them. -- _Robert C. Martin, "Design Principles and Design Patterns" (2000)_

Put the interface in the implementer's package, and the cycle survives. Put it in its own `order_ports` package (a port, in ports-and-adapters terms) and the loop becomes a ladder:

![Fig. 2: Breaking a dependency cycle](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig2-cycle-break.png)

### 📏 Measuring cycles: from yes/no to "how bad"

A simple yes/no is the right **gate**. For a codebase that already has cycles, you need a sense of **severity**:

| Measure                           | Question it answers                         |
|-----------------------------------|---------------------------------------------|
| Is it a DAG?                      | Do we have any cycles at all?                |
| Number of non-trivial SCCs        | How many tangles?                            |
| Size of the largest SCC           | How much of the system is welded together?   |
| Minimum feedback set              | How many edges would we have to cut?         |

Sonargraph's **Relative Cyclicity** shows why size matters more than count. Fifty files caught in one 50-file cycle score **100%**, the worst possible. The same fifty files arranged as twenty-five 2-file cycles score **20%**. Every file is in a cycle either way, but one big tangle is far worse than many small ones.

Skip counting individual cycles. Inside one SCC the number of distinct loops explodes combinatorially, which is why ArchUnit caps its detector at 100 by default.

### 🔬 What the research says

The evidence is real, but correlational and mostly from Java:
* Across six applications, Oyetoyan, Cruzes and Conradi found that "most defects and defective components are concentrated in cyclic-dependent components."
* Components that **move into** cycles between releases become more defect-prone.
* Cycles also raise the change-proneness of nearby classes.

The counterpoint comes from the same field. Al-Mutawa et al. found that most package cycles in Java are **"package local"** (tangles between siblings under one parent), which may not be critical. Nobody has shown that _breaking_ cycles causes fewer defects.

The honest summary: **cycles are a risk marker, and bigger tangles are worse.**

### 🛠️ Enforcing it

**Go** makes the ADP a compile error:
> It is illegal for a package to import itself, directly or indirectly. -- _The Go Programming Language Specification_

**Python** tolerates circular imports until one blows up with `ImportError: cannot import name ... from partially initialized module`. A `TYPE_CHECKING` import or a function-level import makes that error go away, but the **design** dependency is still there.

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

Notice that it picked `orders → billing`, not the `notifications → orders` back edge we inverted. The tool finds the _cheapest_ cut. Choosing which arrow to flip is still a **design decision**. After adding `order_ports`, the contract passes.

| Ecosystem | Tool                                                           | Checks             |
|-----------|----------------------------------------------------------------|--------------------|
| Python    | import-linter `acyclic_siblings`                               | Packages           |
| Python    | grimp `nominate_cycle_breakers`                                | Suggests edges to cut |
| Python    | tach `forbid_circular_dependencies`                            | Modules (off by default) |
| Python    | pylint `cyclic-import` (R0401), `pydeps --show-cycles`         | Modules            |
| JVM       | ArchUnit `slices()...should().beFreeOfCycles()`, JDepend       | Packages           |
| JS / TS   | `madge --circular`, dependency-cruiser `no-circular`, `import/no-cycle` | Files      |

Granularity matters: a codebase can be acyclic **file by file** and still cyclic **package by package**. Martin meant packages.

---

## 🧩 Class Graph: Coupling Between Objects (CBO)

### 🔢 Part 1's numbers, one level down

In 1994, Chidamber and Kemerer published the best-known set of object-oriented class metrics. **CBO** is the one that matters most here:

```text
CBO(c) = number of other classes that c uses, or that use c
```

Sound familiar? It's Part 1's `𝐶ₐ` and `𝐶ₑ`, at class level, **with the arrows erased**:

```text
CBO = |dependents ∪ dependencies| = 𝐶ₐ + 𝐶ₑ − (classes in both)
```

### 🧮 A small example

`Invoice` uses `Customer`, `TaxTable` and `Ledger`. It is used by `Ledger` and `ReportBuilder`.

| Metric | Value                                     |
|--------|-------------------------------------------|
| `𝐶ₑ`   | 3 (Customer, TaxTable, Ledger)             |
| `𝐶ₐ`   | 2 (Ledger, ReportBuilder)                  |
| CBO    | 4 = 3 + 2 − 1 (`Ledger` is counted once)   |
| `I`    | 3 / 5 = 0.6                                |

Two lessons hide in that table:
* **CBO tells you how entangled a class is.** `I` tells you **which way** the entanglement points, which is exactly what CBO throws away.
* The `Invoice ↔ Ledger` overlap that CBO quietly de-duplicates is itself a **cycle**, just at class level. 🔁

### 🔬 What the research says

CBO has the best track record of the classic class metrics:
* Basili, Briand and Melo found it significant for fault-proneness (p = 0.0000 for UI classes).
* In a 2013 review of 106 studies, Radjenović et al. concluded that "the best metrics from the CK metrics suite are CBO, WMC and RFC."

There is a catch that applies to **every** class metric in this article. El Emam et al. found that once you control for class size, "all of these associations disappear." Big classes have more of everything, including bugs. Keep that in mind before treating any single number as a verdict.

### ⚠️ "CBO" isn't one number

Tools disagree on what to count:
* **ckjm** reports CBO as outgoing only (effectively `𝐶ₑ`), with `𝐶ₐ` in a separate column.
* **CK** (Aniche) counts outgoing by default, and offers "CBO Modified" for both directions.
* **NDepend** skips CBO entirely and reports `TypeCa` and `TypeCe`.
* **Python** has no mainstream CK tool. Module-level `𝐶ₐ`/`𝐶ₑ` from an import graph (grimp, pydeps) is the practical stand-in.

A threshold tuned on one tool's CBO means nothing on another's.

### 📏 Where the thresholds come from

| Threshold   | Source                                           | Kind                         |
|-------------|--------------------------------------------------|------------------------------|
| CBO > 14    | Sahraoui et al. (2000)                            | Expert opinion               |
| CBO > 9     | Shatnawi (2010), fitted on Eclipse                | Empirical, one system        |
| "NASA" values | Conflicting secondary citations                 | Folklore                     |

That last row deserves a footnote. Linda Rosenberg's own NASA paper says there is "insufficient statistical data" to set good or bad values, and recommends reviewing outliers instead. Good advice that never made it into the slide decks.

### 🌳 Sidebar: Depth of Inheritance Tree (DIT)

DIT counts the steps from a class up to the root of its inheritance tree. It is easy to compute and hard to interpret:
* Tools disagree on whether the root counts (DIT 0 or 1 for the same class).
* The research contradicts itself. One study found deeper classes more fault-prone, another found the opposite, and a third found the worst classes in the **middle** of the hierarchy.
* The "≤ 5" or "≤ 6" thresholds are vendor guidance, not findings.

One idea survives, and it connects straight back to Part 1: **inheritance is the strongest efferent dependency there is.** A subclass depends on its parent's _implementation_, not just its interface. Inheriting from a concrete class deep in a tree is a dependency on something concrete and stable, which is Part 1's Zone of Pain.

In Python, mixins make depth misleading. `len(cls.__mro__) - 1` counts total ancestors, and pylint's `too-many-ancestors` (R0901) flags classes past 7 by default.

> Favor object composition over class inheritance. -- _Gamma, Helm, Johnson & Vlissides, "Design Patterns" (1994)_

---

## 🧱 Class: Lack of Cohesion (LCOM4)

### 🏝️ Count the islands

Coupling is about the edges **between** classes. Cohesion is about the edges **inside** one.

Hitz and Montazeri's **LCOM4** builds a small graph for each class:
* Each **method** is a node
* Connect two methods if they **share a field**, or if one **calls** the other
* `LCOM4` = the number of **connected components** ("islands")

```text
LCOM4 = 1   → cohesive
LCOM4 = N   → N classes sharing one name; split along the islands
LCOM4 = 0   → no methods
```

![Fig. 3: LCOM4 islands](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig3-lcom4-islands.png)

The `User` class above has two islands: one about credentials, one about billing. Nothing connects them except the class name. That's two classes, and LCOM4 says so.

### 🐞 Why not plain "LCOM"?

The original 1994 definition counts method pairs that share no fields (`P`) and pairs that do (`Q`), then reports `P − Q`, floored at zero. The floor is fatal. Give three methods the field `x` and a fourth method only `y`:

```text
P = 3, Q = 3   →   LCOM = 0   ("perfectly cohesive")
LCOM4 = 2                     (the 4th method and y are a separate class)
```

Basili's team found the original LCOM "insignificant in all cases." The naming hasn't helped either: different papers and tools number the variants differently. **Always define cohesion metrics by formula, not by name.**

### ☎️ One call changes the answer

The call edges are what make LCOM4 useful. Take an `Order` class whose methods split into `{add_item, total, apply_discount}` and `{send_receipt, email_domain}`. That's LCOM4 = 2.

Now `send_receipt` prints the order total by calling `self.total()`. The islands merge, and **LCOM4 = 1**. The class went from "split this" to "cohesive" because one method genuinely needs the other.

### 🐍 LCOM4 for Python, in 40 lines

No maintained Python tool computes LCOM4 (radon does no class metrics), so here is one using only the standard library:

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

### 🧪 Pointed at a real codebase

Run across pip 26.2's internals, 82 of the 183 classes with methods score LCOM4 > 1. Read the top of that list, though, and a pattern appears:
* **Interfaces and abstract bases** (`Candidate`, `Requirement`): every abstract stub is its own island, because stubs share no state.
* **Callback hooks** (a resolver reporter whose seven hook methods each stand alone)
* **Alternate constructors** (`from_directory`, `from_wheel`, …), which build a new instance instead of touching the current one

None of those should be split. LCOM4 assumes a class is **state plus behavior**. Abstract classes have no state, which in Part 1's terms means high `A`. **Read LCOM4 on concrete classes, and skip the abstract ones.**

### 🔬 What the research says

Honestly? Cohesion metrics have a weaker predictive record than coupling metrics. SonarQube once computed LCOM4, along with RFC, DIT and NOC, then dropped them because, in their words, "very few people knew what to do with them."

LCOM4 earns its place for a different reason: when it fires on a concrete class, it hands you the refactoring. Split along the islands, and each new class usually depends on **fewer** things, so `𝐶ₑ` drops too.

---

## 🔬 Method: Cyclomatic and Cognitive Complexity

### 🧮 Cyclomatic complexity: counting test paths

Thomas McCabe defined it in 1976 on a method's control-flow graph:

```text
V(G) = E − N + 2P        (edges, nodes, connected components)
     = decisions + 1     (for structured code)
```

Every `if`, `for`, `while`, `case`, `except`, and each `and`/`or` adds one.

`V(G)` is the number of **independent paths** through the method, which is the size of a basis set of tests. That's what it measures accurately: **how many tests you need**.

### 📏 The "not magical" 10

The famous limit came from McCabe himself:
> The particular upper bound that has been used for cyclomatic complexity is 10 which seems like a reasonable, but not magical, upper limit. -- _Thomas McCabe, "A Complexity Measure" (1976)_

He also exempted large `case` statements. "Not magical" is the most ignored phrase in software metrics.

### 📊 Complexity lives in the tail

Here is real data from pip 26.2's internals (1,549 functions), measured with radon:

![Fig. 4: Complexity distribution in pip](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig4-complexity-tail.png)

* **86%** of functions get radon's grade A (`V(G)` ≤ 5).
* The **4%** at grade C or worse (`V(G)` > 10) hold **23%** of all the branching.

You don't need to fix the codebase. You need to look at the tail.

### 🤔 What it doesn't measure

Two long-standing criticisms:
* **It's mostly size.** Shepperd (1988) called it "no more than a proxy for, and in many cases is outperformed by, lines of code." Across roughly 1.2 million source files, Jay et al. (2009) found that lines of code explained about 90% of its variation.
* **It's blind to nesting.** A flat 10-way `match` and three loops nested inside each other can score the same, but they don't read the same.

Cyclomatic complexity counts **tests**, not **confusion**.

### 🧠 Cognitive Complexity: charging for nesting

SonarSource's **Cognitive Complexity** (G. Ann Campbell) drops the graph math and scores **reading effort** instead:
* +1 for each break in linear flow (`if`, loops, `except`, ternaries)
* **+1 more for each level of nesting** it sits inside
* A whole `switch`/`match` costs +1, not +1 per case
* A run of the same boolean operator (`a and b and c`) costs +1
* `try`, early returns and null-coalescing are free

Here is one Python function, scored both ways:

```python
def shipping_cost(order, rates) -> float:
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

Same function, four different answers. **"Complexity 8" means nothing without the tool's name.**

The `switch` debate in miniature: a 3-case `match` and the equivalent `if/elif/elif` chain both have CC 4. Cognitive Complexity scores the `match` 1 and the chain 3.

### 📏 Where *its* threshold comes from

Cognitive Complexity's default limit is 15. Campbell was refreshingly candid about where that came from: they started with McCabe's 10, found it "noisy," and raised it until the results felt right.
> I guess you're hoping for some scientific formula. I can't give you one. -- _G. Ann Campbell, SonarSource Community (2024)_

It has some validation. A 2020 meta-analysis of ~24,000 human evaluations found a moderate correlation (r = 0.54) between Cognitive Complexity and how long people took to understand code. That's real, and it's also not a defect predictor.

### ⚖️ Sidebar: Weighted Methods per Class (WMC)

```text
WMC = Σ complexity(method)   over all methods in a class
```

Chidamber and Kemerer deliberately left "complexity" undefined, so tools fill it in differently. Some count methods; others sum cyclomatic complexity. Two "WMC" numbers from two tools are two different metrics.

It also mostly measures size. El Emam et al. found WMC correlated with lines of code at ρ = 0.88, and its link to faults vanished once size was controlled. Radjenović's review put it bluntly: WMC "is not really an OO metric."

WMC is most useful **in combination**. PMD's `GodClass` rule fires only when high WMC meets low cohesion and heavy use of other classes' data. That combination is the next chart.

---

## 🗺️ Putting It Together: The Class Map

Part 1 plotted packages on `A` vs `I`. At class level, the useful picture is **size** (WMC) against **entanglement** (CBO), with cohesion (LCOM4) as bubble size:

![Fig. 5: The class map](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/coupling-pt2-fig5-class-map.png)

| Zone          | Meaning                       | Typical move                                         |
|---------------|-------------------------------|------------------------------------------------------|
| Healthy core  | Small, loosely coupled         | Leave it alone                                       |
| Brain class   | Big, but self-contained        | Extract methods; watch Cognitive Complexity          |
| Hub           | Small, but leans on many       | Check `I`: is it pointing toward stability?          |
| God class     | Big **and** entangled          | Split along the LCOM4 islands first                  |

The threshold lines are Shatnawi's Eclipse-derived values (CBO 9, WMC 20). Treat them as a starting point, not a law. Your own baseline is a better line.

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

The numbers that hold up best aren't statistical at all. **Zero cycles** and **one island** follow from what the graph means, not from a regression.

Two findings should keep us all humble:
* After controlling for class size, El Emam et al. found that "none of the metrics we studied were associated with fault-proneness anymore."
* Radjenović's review found that **process metrics** (churn, who touched what, how often) predict post-release faults better than any static code metric.

So use these numbers as a **flashlight**, not a **verdict**:
* Name the tool alongside the number
* Ratchet against your own baseline, not someone else's blog post (including this one)
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

The cycle check is a **gate**. The other two are **reports**: they tell you where to look, and a human decides what to do.

## 🗝 Key Takeaways

* Every metric here is **counting on a graph** 🕸️: loops in the package graph, neighbors in the class graph, islands inside a class, paths inside a method.
* **Cycles come first.** Inside a loop, Part 1's `I` and `D` stop describing anything real 🔁.
* **CBO** is `𝐶ₐ` plus `𝐶ₑ` with the arrows erased. Use `I` to get the direction back 🧭.
* **LCOM4** is the rare metric that hands you the refactoring. Split along the islands ✂️.
* **Cyclomatic complexity** counts tests. **Cognitive complexity** counts confusion 🧠.
* Most thresholds are **somebody's judgment**. The structural ones (zero cycles, one island) are the ones to enforce 📏.

The shape of the system changes. The math still doesn't.

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
- Tools: [import-linter](https://import-linter.readthedocs.io/en/stable/contract_types/), [grimp](https://github.com/python-grimp/grimp), [radon](https://radon.readthedocs.io/), [ruff C901](https://docs.astral.sh/ruff/rules/complex-structure/), [ArchUnit](https://www.archunit.org/userguide/html/000_Index.html), [dependency-cruiser](https://github.com/sverweij/dependency-cruiser)
