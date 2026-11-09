# Figure generation (maintainers)

From the repository root, using Python 3.12:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r .figures/requirements.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python .figures/generate.py
```

Install Chromium again after changing the Playwright version. Each version needs its own browser build; a browser installed by another Python environment or Node project may not match.

The script reads the four current notebooks and writes only `figs/fig1.png` through `figs/fig4.png`, relative to the directory where you run it. Existing PNGs with those names are overwritten. It has no command-line options and does not modify notebooks or save execution artifacts.

`layout.py` holds publication geometry and capture states; `assets/` holds vector annotations, without the original source text or raster screenshots. Source-code panels come from the notebooks, not text replacement rules. Notebook execution uses the same Python environment as the renderer.
