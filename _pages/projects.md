---
layout: single
author_profile: true
title: "Projects"
permalink: /projects/
---

## Recent projects (Python)

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