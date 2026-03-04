# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python workspace for Jupyter notebooks that accompany blog posts on the parent Jekyll site (`git-steven.github.io`). Notebooks cover data visualization, PySpark, scikit-learn feature engineering, coupling metrics analysis, and architectural proposals (IoC/DI patterns, DIKW frameworks).

This directory lives inside the parent Jekyll repo but has its own Python toolchain (Poetry, `.venv`, pyproject.toml).

## Common Commands

```bash
# Install dependencies (uses Poetry with pyproject.toml)
poetry install

# Start JupyterLab
bin/start                    # or: poetry run jupyter lab

# Run tests
poetry run pytest

# Run a single test file
poetry run pytest tests/test_foo.py

# Run a single test
poetry run pytest tests/test_foo.py::test_bar

# Lint
poetry run ruff check .

# Build Spark Docker image (for PySpark notebooks)
./build-spark.sh

# Start Spark cluster
docker compose up

# Shell into Spark container
./docker-sh.sh
```

## Architecture

### Notebook-Centric Layout
This is not a traditional Python application. Content is organized as standalone Jupyter notebooks at the root level, each supporting a blog post topic:
- `pyspark01.ipynb` / `pyspark02.ipynb` - PySpark tutorials using Harry Potter datasets
- `sklearn-feature-engineering*.ipynb` - scikit-learn feature engineering
- `coupling-metrics-*.ipynb` - Software coupling metrics analysis and visualization
- `fast-api-sqs-labmda.ipynb` - FastAPI + SQS + Lambda patterns
- `dikw.ipynb` - DIKW pyramid visualization
- `ioc_proposal_notebook.ipynb` - IoC/dependency injection proposal

### Key Dependencies (from pyproject.toml)
- **Python 3.13.7** (Poetry-managed)
- **JupyterLab** for notebook development
- **Plotly** for interactive visualizations
- **Pandas / NumPy / Matplotlib** for data analysis
- **NetworkX** for graph analysis
- **Freyja** for additional utilities
- Pytest config references `--cov=modgud` (coverage target from a related project; may need updating for local use)

### Spark Infrastructure
PySpark notebooks use a Dockerized Spark cluster:
- `Dockerfile` builds `terracoil/spark` image (bitnami/spark + graphframes)
- `docker-compose.yml` defines master/worker topology
- `conf/` and `spark-defaults.conf` for Spark configuration
- `data/` contains CSV datasets (Harry Potter scripts/characters, Medium search data, Game of Thrones scripts)

### Other Artifacts
- `terracoil/` - Python package stub (empty `__init__.py`)
- `ioc_proposal_one_class_per_file.md` - Detailed IoC design document
- `dikw.md` - DIKW framework writeup
- `coupling-metrics-complete.drawio` - draw.io diagram for coupling metrics article

## Pytest Configuration Notes

The `pyproject.toml` pytest config targets `--cov=modgud` and `testpaths = ["tests"]`. There is currently no `tests/` directory or `modgud` package in this workspace; these settings carry over from a sibling project. When adding tests here, update `addopts` to match the correct package name or remove the coverage flag.
