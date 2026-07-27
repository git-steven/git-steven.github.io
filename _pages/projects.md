---
layout: single
author_profile: true
title: "Projects"
permalink: /projects/
---

## Recent projects (Python)

### [Freyja](https://github.com/terracoil/freyja)
**_Zero-config CLIs from your Python classes_**
![](/assets/images/freyja_sm.jpg)


A Python library that builds a complete command-line interface from one or more functions (or typed class methods) using introspection. With zero configuration and no runtime dependencies, Freyja turns type annotations and docstrings into professional CLIs — complete with type-safe argument parsing, automatic help generation, and shell completion for Bash, Zsh, Fish, and PowerShell. Available on [PyPI](https://pypi.org/project/freyja).

### [Idunn](https://github.com/terracoil/idunn)
**_A tiny constructor-time dependency inversion toolkit_**
![](/assets/images/idunn_sm.png)


A minimal dependency injection / IoC toolkit built around just three decorators — `@Port` (defines a contract), `@Adapter` (binds an implementation), and `@Invert` (injects dependencies). Idunn focuses exclusively on constructor-time injection, with auto-discovery, environment-based implementation selection (dev/test/prod), keyed adapters, and transient or singleton lifecycles. Named for Iðunn, the Norse keeper of the apples of youth — a nod to keeping code fresh through clean, explicit wiring. Available on [PyPI](https://pypi.org/project/idunn).

### [Modgud](https://github.com/terracoil/modgud)
**_Expression-oriented programming for Python_**
![](/assets/images/modgud_sm.jpg)


Brings expression-oriented programming to Python 3.11+ through guard clause decorators and implicit returns, eliminating defensive-coding clutter while preserving a single-return-point architecture. Declarative guards (`not_none`, `positive`, `in_range`, `type_check`, `matches_pattern`, `not_empty`, plus a custom guard registry) validate inputs before a function runs, so bodies focus on business logic instead of validation boilerplate. Zero runtime dependencies and mypy-friendly. Named for Móðguðr, the Norse bridge guardian who demands identification before passage. Available on [PyPI](https://pypi.org/project/modgud).

### [CSV Batcher](https://github.com/tangledpath/csv-batcher)
**_Scaling vertically with CSVs and/or Pandas_**
![](</assets/images/csv_batcher_sm.png>)


A lightweight, python-based, multi-process CSV batcher suitable for use with Pandas dataframes, as a standalone tool, or other tools that deal with large CSV files (or files that require timely processing).

### [Python Arango Object Graph Model](https://github.com/tangledpath/python-arango-ogm)
![](/assets/images/pao_sm.png)


This is built on top of [python-arango]([url](https://github.com/arangodb/python-arango/)).  Capabilities include model-like access to graph objects, and a migration mechanism that generates migrations from your defined models; similar to how Django builds its migrations. This is somewhat a work-in-progress as I integrate it back into the closed-source project from which it was extracted.


### [Python Bunny MQ](https://github.com/tangledpath/python-bunny-mq)
![](/assets/images/bunny-sm.png)


Python-based package that implements a no-dependency, ultra-lightweight intra-process message queue.  This works inside a single process.  This is useful when you need a lightweight pub-sub system.  For example, the author is using it in development to send message to local handlers.  These handlers are ultimately deployed to AWS and are invoked as a lambda function via SQS, so the dev-time "bunny-mq" will not be used.
## Previous Projects
### [Ruby-Fann](https://github.com/tangledpath/ruby-fann)
![](/assets/images/ruby-fann.png)


RubyFann, or "ruby-fann" is a Ruby Gem (no Rails required) that binds natively to FANN (Fast Artificial Neural Network) from within a ruby/rails environment. FANN is a is a free native open source neural network library, which implements multilayer artificial neural networks, supporting both fully-connected and sparsely-connected networks. It is easy to use, versatile, well documented, and fast. RubyFann makes working with neural networks a breeze using ruby, with the added benefit that most of the heavy lifting is done natively.

### [PathMaster](https://github.com/tangledpath/pathmaster)

[A★](https://en.wikipedia.org/wiki/A*_search_algorithm)


![](/assets/images/a_star.png)


[A★](https://en.wikipedia.org/wiki/A*_search_algorithm)
pathfinding in Unity 3D via AutoWaypoints. This was part of a Unity game that didn't make it to market. Since Unity now has pathfinding built-in, we are open-sourcing this for posterity.

# Other
See other open-source; some now defunct/deprecated, on [github](https://github.com/tangledpath).