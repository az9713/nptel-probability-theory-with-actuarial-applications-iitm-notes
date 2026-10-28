"""Offline deterministic reader builder. Source bodies are copied verbatim and hashed."""
import hashlib
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data)


def plain(text):
    parser = PlainText()
    parser.feed(text)
    return ' '.join(' '.join(parser.parts).split())


def shell(title, body, plan, current=None, previous=None, following=None):
    nav = ''.join(f'<li><a href="{c["file"]}"'
        + (' aria-current="page"' if c['number'] == current else '')
        + f'><span class="chapter-number">{c["number"]:02d}</span>{escape(c["title"])}</a></li>'
        for c in plan['chapters'])
    pages = ''
    if previous or following:
        pages = '<nav class="page-nav" aria-label="Chapter navigation">'
        pages += (f'<a rel="prev" href="{previous["file"]}">← {escape(previous["title"])}</a>'
                  if previous else '<span></span>')
        pages += (f'<a rel="next" href="{following["file"]}">{escape(following["title"])} →</a>'
                  if following else '<a href="index.html">Return to contents →</a>')
        pages += '</nav>'
    toolbar = '<div class="toolbar" aria-label="Reader controls"><button id="theme" aria-pressed="false">Light / dark</button><button data-font="-1" aria-label="Decrease text size">A−</button><button data-font="1" aria-label="Increase text size">A+</button><button id="solutions" aria-pressed="false">Show solutions</button><button id="print">Print / PDF</button><label for="search">Search</label><input id="search" type="search" placeholder="Search the book" autocomplete="off"></div><div class="search-panel" id="search-results" role="region" aria-label="Search results" aria-live="polite" hidden></div>'
    return f'''<!doctype html>
<html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Independent expanded lecture notes: probability theory with actuarial applications, IIT Madras NPTEL."><title>{escape(title)} · Probability &amp; Actuarial Applications</title><link rel="stylesheet" href="assets/book.css"><script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']]}},svg:{{fontCache:'local'}},options:{{renderActions:{{addMenu:[]}}}},startup:{{pageReady:()=>MathJax.startup.defaultPageReady().then(()=>{{document.querySelectorAll('mjx-container[display="true"]').forEach(el=>{{const d=document.createElement('div');d.className='math-scroll';el.before(d);d.append(el)}});document.documentElement.dataset.mathReady='true'}})}}}};</script><script defer src="assets/mathjax-tex-svg-full.js"></script><script defer src="assets/search-index.js"></script><script defer src="assets/book.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="masthead"><a href="index.html">Probability / Actuarial Applications</a><nav aria-label="Primary"><a href="index.html">Contents</a><a href="source-map.html">Recordings</a><a href="numerical-lab.html">Laboratory</a><a href="references.html">References</a></nav></header><div class="layout"><aside class="sidebar"><details open><summary>Chapters / 01–22</summary><ol>{nav}</ol><a href="appendix-concentration.html">Appendix · Concentration and LLN</a><br><a href="study-guide.html">Study guide and notation</a></details></aside><main id="main"><div class="eyebrow">IIT Madras · NPTEL · Independent study edition</div>{toolbar}{body}{pages}</main></div><footer class="footer"><a href="WORKFLOW.md">Production workflow</a><a href="source-validation-summary.json">Source record</a><a href="editorial-review-summary.json">Editorial review</a><a href="validation/book-checks.json">Validation</a><a href="https://github.com/az9713/nptel-probability-theory-with-actuarial-applications-iitm-notes">GitHub repository</a><br>Independent educational rewrite. Course recordings and cited works remain attributed to their creators. Educational models use stated assumptions; numerical examples are synthetic.</footer></body></html>'''


def main():
    plan = json.loads((ROOT / 'book-plan.json').read_text(encoding='utf-8'))
    manifest = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))
    videos = {v['id']: v for v in manifest['recordings']}
    inventory, search = [], []
    for i, chapter in enumerate(plan['chapters']):
        path = ROOT / chapter['body']
        if not path.exists():
            continue
        body = path.read_text(encoding='utf-8')
        digest = hashlib.sha256(body.encode()).hexdigest()
        text = plain(body)
        words = len(plain(re.sub(r'<pre\b.*?</pre>', '', body, flags=re.S | re.I)).split())
        exercises = len(re.findall(r'<details\b[^>]*class=["\'][^"\']*exercise', body))
        programs = re.findall(r'data-file=["\']([^"\']+)', body)
        anchors = re.findall(r'https://www\.youtube\.com/watch\?v=([\w-]+)(?:&amp;|&)t=(\d+)', body)
        item = {**chapter, 'body_sha256': digest,
                'authored_file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'body_hash_convention': 'body_sha256 hashes UTF-8 text with LF-normalized newlines; authored_file_sha256 binds exact reviewed file bytes',
                'words': words,
                'exercises': exercises, 'programs': programs,
                'timestamp_anchors': [{'id': v, 'seconds': int(t)} for v, t in anchors]}
        inventory.append(item)
        links = ' · '.join(f'<a href="{videos[v]["url"]}">{escape(videos[v]["title"])}</a>' for v in chapter['videos'])
        heading = f'<h1>{escape(chapter["title"])}</h1><div class="meta">Chapter {chapter["number"]:02d} · Week {chapter["week"]} · {words:,} words · {exercises} worked exercises<br>{links}</div>'
        heading += '<p class="source-note">The recordings determine the topic sequence. Derivations, examples, code and exercises are independently authored expansions; timestamp links identify related lecture discussions. Machine transcripts can misrecognize spoken notation.</p>'
        body_marked = f'<!-- BEGIN AUTHORED BODY sha256={digest} -->\n{body}\n<!-- END AUTHORED BODY -->'
        html = shell(chapter['title'], heading + body_marked, plan,
                     chapter['number'], plan['chapters'][i-1] if i else None,
                     plan['chapters'][i+1] if i+1 < len(plan['chapters']) else None)
        (ROOT / chapter['file']).write_text(html, encoding='utf-8')
        (ROOT / chapter['file'].replace('.html', '.meta.json')).write_text(json.dumps(item, indent=2), encoding='utf-8')
        search.append({'title': chapter['title'], 'file': chapter['file'], 'text': text})
    (ROOT / 'completion.json').write_text(json.dumps({'chapters': inventory,
        'chapter_count': len(inventory), 'planned_chapter_count': len(plan['chapters']),
        'words': sum(c['words'] for c in inventory),
        'worked_exercises': sum(c['exercises'] for c in inventory),
        'programs': sum(len(c['programs']) for c in inventory),
        'assigned_recordings': len({v for c in inventory for v in c['videos']})}, indent=2), encoding='utf-8')
    (ROOT / 'assets/search-index.js').write_text('window.BOOK_SEARCH='+json.dumps(search, ensure_ascii=False)+';', encoding='utf-8')
    for path in sorted((ROOT / 'pages').glob('*.html')):
        body = path.read_text(encoding='utf-8')
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
        title = plain(title_match[1]) if title_match else path.stem
        (ROOT / path.name).write_text(shell(title, body, plan), encoding='utf-8')
    generate_contents(plan, manifest, inventory)
    print(f'Built {len(inventory)}/{len(plan["chapters"])} chapters; '
          f'{sum(c["words"] for c in inventory):,} words')


def generate_contents(plan, manifest, inventory):
    by_number = {c['number']: c for c in inventory}
    words = sum(c['words'] for c in inventory)
    exercises = sum(c['exercises'] for c in inventory)
    rows = ''.join(f'<li><span class="num">{c["number"]:02d}</span><div><a href="{c["file"]}">{escape(c["title"])}</a><small>Week {c["week"]} · {len(c["videos"])} recordings · {by_number.get(c["number"], {}).get("words", 0):,} words</small></div></li>' for c in plan['chapters'])
    home = f'''<div class="hero-rule"></div><h1>Probability Theory<br>with Actuarial Applications</h1><p class="lede">From the language of risk to the mathematics of insurance payments. A substantial, independently authored study edition built around Prof. Neelesh S. Upadhye’s IIT Madras NPTEL recordings.</p><div class="stats"><div><strong>{len(inventory)}</strong><span>Topic chapters</span></div><div><strong>56</strong><span>Lecture uploads</span></div><div><strong>{words:,}</strong><span>Words</span></div><div><strong>{exercises}</strong><span>Worked exercises</span></div></div><p>Begin with events and counting, build conditional and distributional reasoning, then derive the payment rules and aggregate-loss formulas used throughout elementary actuarial probability. Every topic includes explanations, worked calculations, executable checks, and exercises with full solutions.</p><p><a href="{plan['chapters'][0]['file']}">Begin chapter 1 →</a> &nbsp; <a href="study-guide.html">Choose a study path</a></p><div class="source-note"><strong>Source boundary.</strong> The supplied playlist lists 58 entries: an introduction, 56 available lecture uploads, and one unavailable entry. The lectures have 55 distinct week/lesson labels because Week 11 Lesson 1 has two uploads. Week 8 is absent. The recording map preserves these facts. The concentration appendix is an original supplement, not a reconstruction of missing recordings.</div><h2 id="contents">The reading sequence</h2><ol class="chapter-list">{rows}</ol><h2 id="beyond">Beyond the recordings</h2><p>The added proofs make assumptions explicit; the original examples separate gross loss from insurer payment; the numerical laboratory checks finite cases against exact calculations. The <a href="appendix-concentration.html">concentration appendix</a> supplies an independently authored bridge to approximation theory. Research and source notes distinguish these additions from lecture statements.</p><p>The reader works offline with bundled mathematics, search, text controls, code copying and printable solutions. Recordings and external references require an internet connection.</p>'''
    (ROOT / 'index.html').write_text(shell('Probability Theory with Actuarial Applications', home, plan), encoding='utf-8')
    records = []
    for v in manifest['recordings']:
        linked = ', '.join(f'<a href="{plan["chapters"][n-1]["file"]}">Chapter {n}</a>' for n in v['chapters'])
        status = 'Unavailable; content not inferred' if v['status']=='unavailable' else ('Introduction; course context' if not v['chapters'] else 'Included')
        records.append(f'<tr><td>{v["playlist_position"]}</td><td><a href="{v["url"]}">{escape(v["title"])}</a><br><code>{v["id"]}</code></td><td>{linked or status}</td><td>{status}</td></tr>')
    source = '<h1>Recording and source map</h1><p class="lede">Every listed entry retains its original identity and position. The textbook follows the teaching labels rather than the irregular upload order.</p><p><a href="'+escape(plan['playlist'])+'">Original YouTube playlist</a> · <a href="source-manifest.json">Machine-readable manifest</a> · <a href="source-validation-summary.json">Acquisition and coverage evidence</a></p><div class="source-note">No Week 8 recordings occur in this playlist snapshot. One unavailable entry has no recoverable title. The two Week 11 Lesson 1 uploads remain separate source identities. All available lecture recordings are assigned; missing material is never inferred from a title.</div><table><thead><tr><th>Playlist position</th><th>Recording</th><th>Textbook location</th><th>Coverage</th></tr></thead><tbody>'+''.join(records)+'</tbody></table>'
    (ROOT / 'source-map.html').write_text(shell('Recording and source map', source, plan), encoding='utf-8')


if __name__ == '__main__':
    main()
