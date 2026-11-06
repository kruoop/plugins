#!/usr/bin/env python3
"""Insert credited public-video excerpts on the final EP clock (KAN-93)."""
import argparse
import json
import math
from pathlib import Path
import shutil
import sys
from urllib.parse import urlsplit, parse_qsl

from public_clip_sources import probe

VERSION = '1.0.0'


def number(value):
    if isinstance(value, bool):
        raise ValueError('Times must be finite non-negative numbers')
    v = float(value)
    if not math.isfinite(v) or v < 0:
        raise ValueError('Times must be finite non-negative numbers')
    return v


def public_url(value):
    p = urlsplit(value)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('Use a public http(s) URL without credentials')
    sensitive = {'token', 'access_token', 'auth', 'authorization', 'signature', 'sig',
                 'policy', 'key-pair-id', 'credential', 'password', 'api_key', 'apikey', 'jwt'}
    keys = [k.lower() for k, _ in parse_qsl(p.query) + parse_qsl(p.fragment)]
    if any(k in sensitive or k.startswith(('x-amz-', 'x-goog-')) for k in keys):
        raise ValueError('Use a stable public source page, not a signed/token-bearing URL')
    return value


def load_plan(path):
    path = Path(path).expanduser().resolve()
    p = json.loads(path.read_text())
    def resolve(value):
        f = Path(value).expanduser()
        return str((path.parent / f).resolve())
    p['base'], p['output'] = resolve(p['base']), resolve(p['output'])
    if p.get('font'):
        p['font'] = resolve(p['font'])
    output = Path(p['output'])
    if any(f.exists() or f.is_symlink() for f in
           [output, output.with_suffix('.credits.txt'), output.with_suffix('.report.json')]):
        raise ValueError('Output or review sidecar exists; choose a new review output')
    if p['output'] == p['base']:
        raise ValueError('Output is the source; choose a new review output')
    if not Path(p['output']).parent.is_dir():
        raise ValueError('Output parent directory must already exist')
    p['base_media'] = probe(p['base'])
    duration = p['base_media']['duration']
    if p.get('timing_reviewed') is not True or not isinstance(p.get('protected'), list):
        raise ValueError('Review final transcript/teaching windows; set timing_reviewed and protected')
    for key in ('protected', 'speech_free'):
        windows = p.setdefault(key, [])
        for window in windows:
            if len(window) != 2 or not 0 <= number(window[0]) < number(window[1]) <= duration:
                raise ValueError(f'Invalid {key} window')
        p[key] = [[number(a), number(b)] for a, b in windows]
    cues = p.get('cues', [])
    if not cues or len(cues) > 50:
        raise ValueError('Supply between 1 and 50 cues')
    w, h = p['base_media']['width'], p['base_media']['height']
    previous_end = 0
    for cue in sorted(cues, key=lambda c: number(c['at'])):
        for key in ('start', 'end', 'at'):
            cue[key] = number(cue[key])
        length = cue['end'] - cue['start']
        stop = cue['at'] + length
        if not 0 < length <= 30 or stop > duration + 0.001:
            raise ValueError('Excerpt must be 0–30 seconds and fit the EP duration')
        if cue['at'] < previous_end - 0.00001:
            raise ValueError('Overlapping cues are not supported')
        previous_end = stop
        if any(cue['at'] < b and stop > a for a, b in p['protected']):
            raise ValueError('Cue overlaps a protected teaching window')
        if cue['mode'] not in ('ref', 'meme', 'gag'):
            raise ValueError('mode must be ref, meme or gag')
        if not isinstance(cue.get('visual', True), bool) or (cue.get('visual') is False and cue['mode'] != 'gag'):
            raise ValueError('visual:false is supported only for sound-only gag')
        cue['url'] = public_url(cue['url'])
        cue['credit_url'] = public_url(cue.get('credit_url', cue['url']))
        cue['audio'] = cue.get('audio', 'mute')
        if cue['audio'] not in ('mute', 'under', 'replace'):
            raise ValueError('audio must be mute, under or replace')
        if cue['audio'] == 'replace' and not any(
                cue['at'] >= a and stop <= b for a, b in p['speech_free']):
            raise ValueError('replace audio needs a reviewed speech_free window')
        cue['clip_gain_db'] = float(cue.get('clip_gain_db', -20))
        if not math.isfinite(cue['clip_gain_db']) or not -60 <= cue['clip_gain_db'] <= -12:
            raise ValueError('Under-speech clip gain must be between -60 and -12 dB')
        if cue.get('local_excerpt'):
            cue['local_excerpt'] = resolve(cue['local_excerpt'])
            meta = probe(cue['local_excerpt'])
            if abs(meta['duration'] - length) > max(0.12, 2 / meta['fps']):
                raise ValueError('local_excerpt must already be trimmed to the source range')
            if not cue.get('channel'):
                raise ValueError('local_excerpt requires a channel credit')
        if cue['mode'] == 'ref':
            cue['box'] = cue.get('box', [int(w * .025), int(h * .04),
                                       int(w * .55) // 2 * 2, int(h * .53) // 2 * 2])
            box = cue['box']
            if len(box) != 4 or any(isinstance(v, bool) or not isinstance(v, int) for v in box):
                raise ValueError('box must be integer [x,y,width,height]')
            x, y, bw, bh = box
            if min(x, y) < 0 or min(bw, bh) < 64 or x + bw > w or y + bh > h:
                raise ValueError('Reference box must fit the canvas')
        cue['rights_note'] = cue.get('rights_note', 'Rights not verified; review Content ID risk')
    p['cues'] = sorted(cues, key=lambda c: c['at'])
    p['cache'] = resolve(p.get('cache', '.public-clips-cache'))
    limits = p.setdefault('limits', {})
    limits['max_bytes'] = int(number(limits.get('max_clip_mb', 128)) * 1024**2)
    limits['timeout'] = int(number(limits.get('download_timeout_seconds', 180)))
    if not 1 <= limits['max_bytes'] <= 512 * 1024**2 or not 1 <= limits['timeout'] <= 600:
        raise ValueError('Invalid download size/time limits')
    if shutil.disk_usage(Path(p['output']).parent).free < 1024**3:
        raise ValueError('Keep at least 1 GiB free before rendering')
    return p


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'render'])
    parser.add_argument('--plan', required=True, type=Path)
    args = parser.parse_args()
    try:
        plan = load_plan(args.plan)
        if args.action == 'render':
            from public_clip_render import render_plan
            print(render_plan(plan, args.plan))
        else:
            print(f"Valid: {len(plan['cues'])} cues on {plan['base_media']['duration']:.3f}s final EP")
    except (ValueError, TypeError, OverflowError, KeyError, OSError, ImportError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
