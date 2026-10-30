#!/usr/bin/env python3
"""Install this repository's BBN skills, backing up only the replaced skill folders."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]


def inventory(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=Path.home() / '.codex/skills')
    parser.add_argument('--check', action='store_true', help='Check the destination without writing')
    args = parser.parse_args()
    dest = args.destination.expanduser().resolve()
    manifest = json.loads((ROOT / 'plugins/bbn-video-studio/.claude-plugin/plugin.json').read_text())
    names = manifest['metadata']['bundledSkills']
    assert len(names) == len(set(names))
    for name in names:
        assert Path(name).name == name and (ROOT / 'skills' / name / 'SKILL.md').is_file()
    if args.check:
        drift = [n for n in names if inventory(ROOT / 'skills' / n) != inventory(dest / n)]
        if drift:
            raise SystemExit('Installed skills differ: ' + ', '.join(drift))
        print(f'Checked {len(names)} installed skill trees: all paths and SHA-256 hashes match')
        return
    canonical = (ROOT / 'skills').resolve()
    if dest == canonical or canonical in dest.parents or dest in canonical.parents:
        raise SystemExit('Destination must not overlap canonical skills/')
    dest.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup = dest.parent / 'skill-backups' / ('bbn-video-studio-' + stamp)
    for name in names:
        target = dest / name
        saved = backup / name
        if target.exists() or target.is_symlink():
            backup.mkdir(parents=True, exist_ok=True)
            target.rename(saved)
        try:
            shutil.copytree(ROOT / 'skills' / name, target)
        except Exception:
            if target.is_dir():
                shutil.rmtree(target)
            if saved.exists() or saved.is_symlink():
                saved.rename(target)
            raise
    print(f'Installed {len(names)} skills into {dest}; prior folders saved in {backup}')


if __name__ == '__main__':
    main()
