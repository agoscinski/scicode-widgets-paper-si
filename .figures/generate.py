"""Execute the four paper notebooks and write PNGs to figs/ in the working directory."""
import ast
import base64
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from threading import Thread

import nbformat
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from playwright.sync_api import sync_playwright
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from layout import (ADD_SOURCE, CAPTURE_STATE, CLEAN, FIGURE3_STATES, LAYOUT,
                    LAYOUT4, SETUP, SOURCE_PANELS, STYLE, STYLE4)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = Path(__file__).resolve().parent / 'assets'
SIZES = [(1332, 3173), (1612, 3492), (1036, 783), (1606, 3508)]


def source_panels(notebook, number):
    source = '\n\n'.join(c.source for c in notebook.cells if c.cell_type == 'code')
    nodes, lines = ast.parse(source).body, source.splitlines()
    panels = []
    for first, last, x, y, w, h, font in SOURCE_PANELS.get(number, []):
        text = '\n'.join(lines[nodes[first].lineno - 1:nodes[last].end_lineno])
        panels.append(dict(html=highlight(text, PythonLexer(), HtmlFormatter(nowrap=True)),
                           x=x, y=y, w=w, h=h, font=font))
    return panels


def execute(notebook, number, kernels):
    cells = [nbformat.v4.new_code_cell(c.source) for c in notebook.cells if c.cell_type == 'code']
    nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(SETUP)])
    if number == 3:
        source = '\n\n'.join(c.source for c in cells)
        nb.cells.extend(nbformat.v4.new_code_cell(source + '\n' + state + '\ncode_ex')
                        for state in FIGURE3_STATES)
    else:
        nb.cells.extend(cells + [nbformat.v4.new_code_cell(CAPTURE_STATE[number])])
    manager = KernelManager(kernel_name='figures',
                            kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernels)]))
    client = NotebookClient(nb, km=manager, timeout=120,
                            resources={'metadata': {'path': str(ROOT)}})
    try:
        client.execute()
    finally:
        if client.kc:
            client.kc.stop_channels()
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
    return HTMLExporter(template_name='lab', exclude_input=True).from_notebook_node(nb)[0]


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main():
    # Fail before executing notebooks if the matching browser is not installed.
    with sync_playwright() as playwright:
        playwright.chromium.launch().close()
    output = Path.cwd() / 'figs'
    output.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix='paper-figures-') as work:
        work = Path(work)
        os.environ['MPLCONFIGDIR'] = str(work / 'matplotlib')
        kernels = work / 'kernels'
        spec = kernels / 'figures'
        spec.mkdir(parents=True)
        (spec / 'kernel.json').write_text(json.dumps({
            'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
            'display_name': 'Figures', 'language': 'python'}))
        panels = {}
        for number in range(1, 5):
            print(f'Executing figure {number}', flush=True)
            notebook = nbformat.read(ROOT / f'figure-{number}.ipynb', as_version=4)
            panels[number] = source_panels(notebook, number)
            (work / f'{number}.html').write_text(execute(notebook, number, kernels))
        with ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(work))) as server:
            Thread(target=server.serve_forever, daemon=True).start()
            try:
                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch()
                    try:
                        for number, (width, height) in enumerate(SIZES, 1):
                            page = browser.new_page(viewport={'width': width, 'height': height})
                            page.goto(f'http://127.0.0.1:{server.server_port}/{number}.html')
                            page.wait_for_selector('.widget-code-input-body .cm-line', timeout=60000)
                            page.wait_for_timeout(5000)
                            page.evaluate('document.fonts.ready')
                            page.add_style_tag(content=CLEAN)
                            if number == 4:
                                page.evaluate(LAYOUT4)
                                page.add_style_tag(content=STYLE4)
                                page.add_style_tag(content='#publication {transform:scale(3);transform-origin:top left}')
                            else:
                                overlay = (ASSETS / f'figure-{number}-annotations.svg').read_text()
                                page.evaluate(LAYOUT, dict(i=number, w=width, h=height, overlay=overlay))
                                page.add_style_tag(content=STYLE)
                                page.add_style_tag(content=HtmlFormatter().get_style_defs('.notebook-source'))
                                page.evaluate(ADD_SOURCE, panels[number])
                            page.wait_for_timeout(1000)
                            shot = page.context.new_cdp_session(page).send('Page.captureScreenshot', {
                                'format': 'png', 'captureBeyondViewport': True,
                                'clip': dict(x=0, y=0, width=width, height=height, scale=1)})
                            path = output / f'fig{number}.png'
                            path.write_bytes(base64.b64decode(shot['data']))
                            page.close()
                            print(f'Wrote {path}', flush=True)
                    finally:
                        browser.close()
            finally:
                server.shutdown()


if __name__ == '__main__':
    main()
