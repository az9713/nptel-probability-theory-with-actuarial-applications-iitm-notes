"""Embed only the two explicitly mapped root-authored programs, with actual stdout."""
from html import escape
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
for body, program, marker in [
    ('chapters/ch22.html', 'code/ch22.py', '<!-- CH22_CODE -->'),
    ('pages/appendix-concentration.html', 'code/appendix_concentration.py', '<!-- APPENDIX_CODE -->'),
]:
    path = ROOT / body
    text = path.read_text(encoding='utf-8')
    if marker not in text:
        continue
    source = (ROOT / program).read_text(encoding='utf-8')
    result = subprocess.run([sys.executable, '-B', '-X', 'utf8', program],
                            cwd=ROOT, capture_output=True, text=True, check=True)
    block = (f'<pre><code class="language-python" data-file="{program}">'
             f'{escape(source)}</code></pre>\n<pre class="output">'
             f'{escape(result.stdout)}</pre>')
    path.write_text(text.replace(marker, block), encoding='utf-8')
    print(body, 'embedded verified source and actual stdout')
