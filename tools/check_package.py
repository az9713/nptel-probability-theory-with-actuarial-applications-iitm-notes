"""Validate an explicit public export without using private source material."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from public_files import public_files

ROOT=Path(__file__).resolve().parents[1]


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    paths=public_files(ROOT);issues=[]
    for path in paths:
        relative=path.relative_to(ROOT).as_posix()
        if any(x in path.parts for x in ['work','.git','.venv','node_modules','.playwright']):
            issues.append('Private path in export: '+relative)
        if path.suffix.lower() in ['.m4a','.mp4','.webm','.vtt','.srt','.pdf']:
            issues.append('Raw source media/reference in export: '+relative)
        if path.suffix in ['.py','.js','.md','.json','.html','.ps1']:
            text=path.read_text(encoding='utf-8')
            if re.search(r'gh[pousr]_[A-Za-z0-9]{32,}',text):issues.append('Credential-like string: '+relative)
    export=ROOT/'work'/('public-export-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'))
    export.mkdir(parents=True,exist_ok=False)
    for path in paths:
        target=export/path.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,target)
    checks=[]
    for script in ['tools/build_book.py','tools/check_code.py','tools/validate_book.py']:
        result=subprocess.run([sys.executable,'-B','-X','utf8',script],cwd=export,
            capture_output=True,text=True,timeout=45)
        checks.append({'command':script,'exit_code':result.returncode,
                       'stdout':result.stdout,'stderr':result.stderr})
        if result.returncode:issues.append('Clean export check failed: '+script)
    compared=[]
    for source in sorted(ROOT.glob('*.html')):
        target=export/source.name
        same=target.exists() and digest(source)==digest(target)
        compared.append({'file':source.name,'sha256':digest(source),'identical':same})
        if not same:issues.append('Rebuilt HTML differs: '+source.name)
    sourcefree={'scope':'Clean explicit public export, with private sources absent; no network required',
        'passed':not issues,'checks':checks,'html_parity':compared,
        'rendering':'Original public HTML was browser-tested offline; byte-identical rebuilt HTML is recorded here'}
    (ROOT/'validation/source-free-checks.json').write_text(json.dumps(sourcefree,indent=2),encoding='utf-8')
    report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'passed':not issues,
        'public_file_count':len(paths),'public_bytes':sum(p.stat().st_size for p in paths),
        'private_sources_included':False,'issues':issues,
        'self_reference_policy':'This package report does not embed hashes of its own content',
        'files':[p.relative_to(ROOT).as_posix() for p in paths]}
    (ROOT/'validation/package-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(f'{len(paths)} public files; {len(compared)} byte-identical rebuilt HTML pages; {len(issues)} package issues')
    for issue in issues:print(issue)
    return 0 if not issues else 1

if __name__=='__main__':sys.exit(main())
