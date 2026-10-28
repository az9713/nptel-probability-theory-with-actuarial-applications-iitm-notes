"""Check served public-file integrity; deliberately exclude this report's own hash."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.parse import quote
from urllib.request import Request,urlopen
from public_files import public_files

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'publication-validation.json'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',required=True)
    parser.add_argument('--commit',required=True)
    args=parser.parse_args()
    base=args.base.rstrip('/')+'/'
    paths=[p for p in public_files(ROOT) if p!=REPORT and not p.name.startswith('.')]
    def check(path):
        relative=path.relative_to(ROOT).as_posix()
        expected=hashlib.sha256(path.read_bytes()).hexdigest()
        url=base+quote(relative,safe='/')+'?verify='+args.commit[:12]
        error=None
        for attempt in range(3):
            try:
                request=Request(url,headers={'User-Agent':'Independent-lecture-notes-integrity-check'})
                with urlopen(request,timeout=25) as response:
                    actual=hashlib.sha256(response.read()).hexdigest()
                    return {'file':relative,'expected_sha256':expected,'served_sha256':actual,
                            'status':response.status,'matches':actual==expected}
            except Exception as exc:
                error=type(exc).__name__+': '+str(exc)
                if attempt<2:time.sleep(2)
        return {'file':relative,'expected_sha256':expected,'matches':False,'error':error}
    with ThreadPoolExecutor(max_workers=6) as pool:records=list(pool.map(check,paths))
    result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'base_url':base,
        'edition_commit':args.commit,'passed':all(r['matches'] for r in records),
        'checked_files':len(records),'matched_files':sum(r['matches'] for r in records),
        'scope':'Served-file byte integrity; no additional scientific/content acceptance implied',
        'excluded':[{'file':'publication-validation.json','reason':'Self-hashing is structurally unverifiable; report excluded from its own hash set'},
                    {'file':'dotfiles','reason':'Repository/build configuration; not reader assets'}],
        'records':records}
    REPORT.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(f'{result["matched_files"]}/{len(records)} served files match the reviewed public edition')
    for row in records:
        if not row['matches']:print(json.dumps(row))
    return 0 if result['passed'] else 1

if __name__=='__main__':sys.exit(main())
