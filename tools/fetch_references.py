"""Fetch only the pinned reader runtime and primary reference snapshots."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import requests

ROOT = Path(__file__).resolve().parents[1]
ITEMS = [
    ('assets/mathjax-tex-svg-full.js', 'https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg-full.js'),
    ('assets/mathjax-LICENSE', 'https://cdn.jsdelivr.net/npm/mathjax@3.2.2/LICENSE'),
    ('work/references/grinstead-snell.pdf', 'https://math.dartmouth.edu/~prob/prob/prob.pdf'),
    ('work/references/loss-data-analytics.html', 'https://openacttexts.github.io/Loss-Data-Analytics/'),
]


def fetch(item):
    path, url = item
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    (ROOT / path).write_bytes(response.content)
    return {'path': path, 'url': url, 'bytes': len(response.content),
            'sha256': hashlib.sha256(response.content).hexdigest()}


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, ITEMS))
    (ROOT / 'work/references/retrieval.json').write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    text = (ROOT / 'work/references/loss-data-analytics.html').read_text(encoding='utf-8')
    print('\n'.join(dict.fromkeys(re.findall(r'href="([^"]+)"', text))))
