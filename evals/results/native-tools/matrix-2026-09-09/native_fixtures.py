"""Matched native-tool fixtures, with opaque IDs shared by every source record.

This module and its source-criteria mapping are private to the evaluator. Native
sessions receive only materialized Case.files and the ordinary user request.
"""
from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import PurePosixPath
import re

from fixtures import Case, Criterion, cases as original_cases


SEED = 'native-tools-forward-2026-09-09-v1'


def strengthen(case: Case) -> Case:
    """Preserve semantic chains while removing fixture-origin ID shortcuts."""
    stems = sorted({PurePosixPath(p).stem for p in case.files
                    if p.startswith('history/') and PurePosixPath(p).name not in ('brief.md', 'index.md')})
    # Receipt and support identities use the same opaque namespace too; leaving
    # rollout-rev-4000 in the body would still expose the generated ID range.
    identifiers = set(stems)
    for content in case.files.values():
        identifiers.update(value for value in re.findall(r'\b[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+\b', content)
                           if any(character.isdigit() for character in value))
    identities = {stem: 'record-' + hashlib.sha256(f'{SEED}:{case.name}:{stem}'.encode()).hexdigest()[:10]
                  for stem in sorted(identifiers)}
    if len(set(identities.values())) != len(identities):
        raise ValueError('Source identity collision')
    token = re.compile(r'[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*')

    def rename(text: str) -> str:
        def substitute(match: re.Match[str]) -> str:
            value = match.group()
            # Calendar dates are dates, even if an operations file is named for
            # one. Their filename is changed separately, never their provenance.
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                return value
            return identities.get(value, value)
        return token.sub(substitute, text)

    retired = next(p.rsplit('/brief.md', 1)[0] for p in case.files if '/retired/' in p and p.endswith('/brief.md'))
    paths: dict[str, str] = {}
    for path in case.files:
        original = PurePosixPath(path)
        renamed = str(original.with_name(identities[original.stem] + original.suffix)) if original.stem in identities else path
        # Interleave completed/background actions with retained original actions.
        # Their existing dispositions and linked evidence remain unchanged.
        if path.startswith('history/actions/') and re.search(r'-([4-6][0-9]{3})\.md$', path):
            pick = int(hashlib.sha256(path.encode()).hexdigest()[:8], 16)
            if pick % 6 == 0:
                renamed = retired + '/actions/' + PurePosixPath(renamed).name
        paths[path] = renamed
    pattern = re.compile(r'history/[A-Za-z0-9_./-]+')

    def transform(text: str) -> str:
        # Replace complete paths first, protecting them from subsequent ID rewrite.
        placeholders: dict[str, str] = {}
        def path_replacement(match: re.Match[str]) -> str:
            if match.group() not in paths:
                return match.group()
            marker = f'@@SOURCEPATH{len(placeholders)}@@'
            placeholders[marker] = paths[match.group()]
            return marker
        text = rename(pattern.sub(path_replacement, text))
        for marker, path in placeholders.items():
            text = text.replace(marker, path)
        return text

    files = {paths[path]: transform(content) for path, content in case.files.items()}
    criteria = tuple(Criterion(c.key, transform(c.description), tuple(paths[s] for s in c.sources)) for c in case.criteria)
    return replace(case, files=files, request=transform(case.request), criteria=criteria)


def cases() -> tuple[Case, ...]:
    return tuple(strengthen(case) for case in original_cases(record_count=2400))
