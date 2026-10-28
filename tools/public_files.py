"""The explicit public-package boundary shared by export and publication checks."""
from pathlib import Path


def public_files(root):
    root=Path(root)
    files=[]
    for name in ['assets','chapters','code','pages','tools','validation']:
        files.extend(p for p in (root/name).rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.suffix!='.pyc')
    files.extend(p for p in root.iterdir() if p.is_file() and (
        p.suffix in ['.html','.json','.md'] or p.name in [
        '.gitignore','.gitattributes','.nojekyll','requirements-dev.txt','requirements-source.txt']))
    return sorted(set(p for p in files if p.name!='EDITOR_DOMAIN.md'))
