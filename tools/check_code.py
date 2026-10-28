"""Check source parity, execute finite examples, and compare actual displayed output."""
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

class Listings(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.programs = []
        self.outputs = []
        self.capture = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'code' and attrs.get('data-file'):
            self.capture = ['code', attrs['data-file'], []]
        elif tag == 'pre' and 'output' in attrs.get('class','').split():
            self.capture = ['output', None, []]
    def handle_data(self, data):
        if self.capture:
            self.capture[2].append(data)
    def handle_endtag(self, tag):
        if self.capture and ((tag == 'code' and self.capture[0]=='code') or
                             (tag == 'pre' and self.capture[0]=='output')):
            kind, name, parts = self.capture
            if kind == 'code': self.programs.append((name, ''.join(parts)))
            else: self.outputs.append(''.join(parts))
            self.capture = None

def main():
    records = []
    bodies = sorted((ROOT/'chapters').glob('ch*.html'))
    bodies += [ROOT/'pages/appendix-concentration.html']
    for body in bodies:
        parser=Listings(); parser.feed(body.read_text(encoding='utf-8'))
        if not parser.programs:
            records.append({'body':str(body.relative_to(ROOT)), 'passed':False,
                            'error':'No standalone program found'})
            continue
        for index,(name,source) in enumerate(parser.programs):
            path=(ROOT/name).resolve()
            if not path.is_relative_to(ROOT/'code') or path.suffix!='.py':
                raise ValueError('Unsafe program path: '+name)
            saved=path.read_text(encoding='utf-8')
            parity=source.strip()==saved.strip()
            result=subprocess.run([sys.executable,'-B','-X','utf8',str(path)],
                cwd=ROOT, capture_output=True,text=True,timeout=30)
            expected=parser.outputs[index] if index<len(parser.outputs) else None
            output_matches=expected is not None and result.stdout.strip()==expected.strip()
            records.append({'body':str(body.relative_to(ROOT)), 'program':name,
                'source_sha256':hashlib.sha256(saved.encode()).hexdigest(),
                'embedded_source_matches':parity,'exit_code':result.returncode,
                'stdout':result.stdout,'stderr':result.stderr,
                'displayed_output_matches':output_matches,
                'passed':parity and result.returncode==0 and output_matches})
    report={'scope':'Finite executable examples; no theorem or empirical-model certification',
            'program_count':len(records),'passed':all(r['passed'] for r in records),
            'records':records}
    (ROOT/'validation/code-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(f"{sum(r['passed'] for r in records)}/{len(records)} program checks passed")
    for r in records:
        if not r['passed']: print(json.dumps(r,indent=2))
    return 0 if report['passed'] else 1

if __name__=='__main__':
    sys.exit(main())
