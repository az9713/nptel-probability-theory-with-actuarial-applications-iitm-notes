"""Static integrity checks for the actual house markup and generated edition."""
from collections import Counter
from html import unescape
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote,urlsplit,parse_qs

ROOT=Path(__file__).resolve().parents[1]

class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.assets=[];self.exercise_count=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag in ['script','img'] and 'src' in a:self.assets.append(a['src'])
        if tag=='link' and a.get('rel')=='stylesheet':self.assets.append(a.get('href',''))
        if tag=='details' and 'exercise' in a.get('class','').split():self.exercise_count+=1

def main():
    issues=[]; records=[]
    plan=json.loads((ROOT/'book-plan.json').read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/'source-manifest.json').read_text(encoding='utf-8'))
    videos={v['id']:v for v in manifest['recordings']}
    docs={}
    for path in ROOT.glob('*.html'):
        raw=path.read_text(encoding='utf-8'); doc=Document();doc.feed(raw)
        docs[path.name]=(doc,raw)
        duplicate=[k for k,v in Counter(doc.ids).items() if v>1]
        if duplicate:issues.append(f'{path.name}: duplicate IDs {duplicate}')
        for required in ['lang="en"','name="viewport"','id="main"']:
            if required not in raw:issues.append(f'{path.name}: missing {required}')
        for asset in doc.assets:
            p=urlsplit(asset)
            if p.scheme or p.netloc:issues.append(f'{path.name}: remote rendering asset {asset}')
            elif not (ROOT/unquote(p.path)).is_file():issues.append(f'{path.name}: missing asset {asset}')
    for name,(doc,raw) in docs.items():
        for href in doc.links:
            parsed=urlsplit(href)
            if parsed.scheme in ['https','http','mailto']:continue
            if parsed.scheme or parsed.netloc:issues.append(f'{name}: unsafe/unexpected link {href}');continue
            target_name=unquote(parsed.path) or name
            target=(ROOT/target_name).resolve()
            if not target.is_relative_to(ROOT):issues.append(f'{name}: link escapes root {href}');continue
            if not target.exists():issues.append(f'{name}: broken local link {href}');continue
            if parsed.fragment and target_name in docs and unquote(parsed.fragment) not in docs[target_name][0].ids:
                issues.append(f'{name}: missing fragment {href}')
    for c in plan['chapters']:
        body_path=ROOT/c['body'];html_path=ROOT/c['file']
        if not body_path.exists() or not html_path.exists():issues.append(f'Chapter {c["number"]} missing');continue
        body=body_path.read_text(encoding='utf-8');html=html_path.read_text(encoding='utf-8')
        digest=hashlib.sha256(body.encode()).hexdigest()
        parity=f'<!-- BEGIN AUTHORED BODY sha256={digest} -->\n{body}\n<!-- END AUTHORED BODY -->' in html
        if not parity:issues.append(c['file']+': body parity failed')
        for opening,closing in [(r'\(',r'\)'),(r'\[',r'\]')]:
            if body.count(opening)!=body.count(closing):issues.append(c['body']+': unbalanced MathJax delimiters')
        if re.search(r'SOURCE_CH\d+|\[PROOF NEEDED\]|\[CITATION NEEDED|pending source|SOURCE_READ_PENDING',body,re.I):
            issues.append(c['body']+': unresolved author marker')
        doc=Document();doc.feed(body)
        if doc.exercise_count<5:issues.append(c['body']+': fewer than five worked exercises')
        anchors=[]
        for href in doc.links:
            p=urlsplit(href)
            if p.netloc in ['www.youtube.com','youtube.com'] and p.path=='/watch':
                params=parse_qs(p.query)
                if 't' not in params:continue
                video=params.get('v',[''])[0]
                try:seconds=int(params['t'][0].removesuffix('s'))
                except ValueError:issues.append(c['body']+': noninteger timestamp');continue
                anchors.append(video)
                if video not in videos or seconds<0 or seconds>videos[video]['duration']:
                    issues.append(c['body']+': timestamp out of source bounds')
                private=ROOT/'work/sources'/f'{video}.transcript.json'
                if private.exists():
                    observed=json.loads(private.read_text(encoding='utf-8'))['segments']
                    if not any(abs(s['start']-seconds)<1.1 for s in observed):
                        issues.append(c['body']+f': timestamp {video}:{seconds} is not an observed segment start')
        missing=set(c['videos'])-set(anchors)
        if missing:issues.append(c['body']+': missing recording anchors '+str(sorted(missing)))
        records.append({'chapter':c['number'],'body_sha256':digest,'body_parity':parity,
            'exercises':doc.exercise_count,'math_segments':body.count(r'\(')+body.count(r'\['),
            'covered_recordings':sorted(set(anchors))})
    review=json.loads((ROOT/'editorial-review-summary.json').read_text(encoding='utf-8'))
    for item in review.get('reviewed_bodies',[]):
        current=hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()
        if current!=item['sha256']:issues.append(item['path']+': changed since independent acceptance')
    if len(review.get('reviewed_bodies',[]))!=23:issues.append('Incomplete independent review acceptance record')
    summary={'scope':'Static reader/source/code structure, not mathematical certification',
        'html_pages':len(docs),'chapter_count':len(records),'passed':not issues,'issues':issues,'chapters':records}
    (ROOT/'validation/book-checks.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(f'{len(records)} chapters, {len(docs)} pages, {len(issues)} static issues')
    for issue in issues:print(issue)
    return 0 if not issues else 1

if __name__=='__main__':sys.exit(main())
