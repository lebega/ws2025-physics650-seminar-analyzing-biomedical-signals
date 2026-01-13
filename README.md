# Computational Physics Seminar on Analyzing Biomedical Signals
This repository contains the LaTeX and Python code used for creating the presentations and plots used in the seminar talks by Konrad Beck and Leon Galbas (Universität Bonn) in the winter semester 2025/26.

## Requirements
This project requires the TISEAN package to be installed and on your system's PATH. TISEAN can by found under (https://www.mpipks-dresden.mpg.de/tisean/Tisean_3.0.1/index.html).

## Installation
This repository uses the `uv` package manager. An installation guide can be found under (https://docs.astral.sh/uv/). It is most easily installed using
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Once `uv` is installed, inside the project root, run
```
uv sync
```
to install all necessary dependencies. Then, any python file can be run with `uv run`, e.g.
```
uv run project_leon/src/main.py
```




