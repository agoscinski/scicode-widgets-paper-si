This repository contains the figures of the _scicode-widgets_ paper. The package repository is https://github.com/osscar-org/scicode-widgets.

## Environment

Use Python 3.12 and install the pinned dependencies in an isolated environment:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

`requirements.txt` contains the notebook dependencies. It pins direct dependencies, not the complete transitive dependency tree.
