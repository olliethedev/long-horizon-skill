#!/usr/bin/env python3
"""Preserve reviewed simulation evidence with compact raw trace storage."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
from analyze import analyze


def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}


def archive(root,target):
    if target.exists():
        raise ValueError('Archive destination already exists')
    manifest=json.loads((root/'manifest.json').read_text())
    analysis=analyze(root)
    if manifest['status']=='running':
        raise ValueError('Do not archive while a runner is writing')
    target.mkdir(parents=True)
    for file in root.glob('*.json'):
        shutil.copy2(file,target/file.name)
    source=Path(__file__).resolve().parent
    code=target/'code'
    code.mkdir()
    for file in source.glob('*.py'):
        shutil.copy2(file,code/file.name)
    shutil.copytree(source/'skill',code/'skill')
    for name in ['REVIEW.md','README.md']:
        shutil.copy2(source/name,code/name)
    for ident,case in manifest['cases'].items():
        out=target/'cases'/ident
        out.mkdir(parents=True)
        trial=Path(case['path'])
        for name in ['brief.md','task.md','API.md']:
            shutil.copy2(trial/name,out/name)
        if (trial/'evidence').exists():
            shutil.copytree(trial/'evidence',out/'evidence')
        shutil.copy2(root/'states'/f'{ident}.json',out/'service-final.json')
        for epoch in case['epochs']:
            folder=root/'snapshots'/ident/f"epoch-{epoch['epoch']}"
            # Readable decisions and their cited source files, plus exact pre-run memories.
            shutil.copytree(folder,out/f"epoch-{epoch['epoch']}")
    raw_paths=[]
    for folder in ['harness','traces','sources','states']:
        if (root/folder).exists():
            raw_paths.extend(p for p in (root/folder).rglob('*') if p.is_file())
    # Recheck fixtures can refer to a prior matrix instead of duplicating sources.
    # Preserve their actual read-only histories so the archive stands alone.
    if not (root/'sources').exists():
        for case in manifest['cases'].values():
            raw_paths.extend(p for p in (Path(case['path'])/'history').rglob('*') if p.is_file())
    with tarfile.open(target/'raw-evidence.tar.gz','w:gz') as tar:
        for file in sorted(raw_paths):
            tar.add(file,arcname=str(file.relative_to(root)),recursive=False)
    provenance={'raw_file_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(raw_paths)},
        'archive_file_sha256':hashes(target),'attempted_sessions':analysis['attempted_sessions'],
        'notes':'Raw command traces and generated background histories are compressed; case snapshots remain readable. Paths in traces are the original evaluated paths.'}
    (target/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print(json.dumps({'archive':str(target),'attempted_sessions':analysis['attempted_sessions'],'raw_files':len(raw_paths),'files':len(provenance['archive_file_sha256'])},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('root',type=Path)
    p.add_argument('destination',type=Path)
    a=p.parse_args()
    archive(a.root,a.destination)
