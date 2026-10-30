#!/usr/bin/env python3
"""Build/check the marketplace's self-contained BBN bundle from canonical skills/."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'bbn-video-studio'


def inventory(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Report drift without writing files')
    args = parser.parse_args()
    manifest = json.loads((PLUGIN / '.claude-plugin/plugin.json').read_text())
    names = manifest['metadata']['bundledSkills']
    if len(names) != len(set(names)):
        raise ValueError('Duplicate bundled skill names')
    for name in names:
        if Path(name).name != name or not (ROOT / 'skills' / name / 'SKILL.md').is_file():
            raise ValueError(f'Invalid/missing canonical skill: {name}')
    dest = PLUGIN / 'skills'
    if args.check:
        errors = []
        actual_names = {p.name for p in dest.iterdir()} if dest.exists() else set()
        if actual_names != set(names):
            errors.append('Bundled skill directory membership differs from manifest')
        for name in names:
            if inventory(ROOT / 'skills' / name) != inventory(dest / name):
                errors.append(f'{name}: missing, extra or changed files')
        if errors:
            print('\n'.join(errors), file=sys.stderr)
            return 1
        print(f'Checked {len(names)} skill trees: all bundle paths and SHA-256 hashes match skills/')
    else:
        # This subtree is generated exclusively by this script; canonical skills stay intact.
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        for name in names:
            shutil.copytree(ROOT / 'skills' / name, dest / name)
        print(f'Built {len(names)} self-contained skill trees in {dest.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
