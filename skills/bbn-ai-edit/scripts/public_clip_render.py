"""FFmpeg composites plus credit cards; no changes to the final EP clock."""
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime, timezone

from public_clip_sources import bounded_run, fetch_clip, probe, sha256


def duck_filter(start, end):
    # aeval evaluates every sample/channel; volume's enable evaluates audio frames.
    # Integer sample ordinals avoid floating-point t=0.049999999 at a 0.05s edge.
    first, last = round(start * 48000), round(end * 48000)
    return f"aeval=exprs='if(gte(n,{first})*lt(n,{last}),0,val(ch))':c=same"


def publish_artifacts(rendered, out, report, credits, temp):
    """Publish evidence first and movie last; collision/failure rolls back our own links."""
    credit_file = Path(temp) / 'credits.txt'
    report_file = Path(temp) / 'report.json'
    credit_file.write_text(credits)
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    pairs = [(credit_file, out.with_suffix('.credits.txt')),
             (report_file, out.with_suffix('.report.json')), (rendered, out)]
    created = []
    try:
        for source, target in pairs:
            os.link(source, target)  # fails on files, directories and even dangling symlinks
            created.append((source, target))
    except OSError:
        for source, target in reversed(created):
            if target.exists() and os.path.samefile(source, target):
                target.unlink()
        raise


def font_path(plan):
    if plan.get('font'):
        f = Path(plan['font']).expanduser()
        if f.is_file():
            return f
        raise ValueError('Configured font does not exist')
    for name in ('Sarabun-Regular.ttf', 'IBMPlexSansThai-Regular.ttf'):
        f = Path.home() / 'Library/Fonts' / name
        if f.is_file():
            return f
    raise ValueError('Install a Thai-capable font or set font in the plan')


def card(cue, channel, width, folder, index, font):
    from PIL import Image, ImageDraw, ImageFont, features
    if not features.check('raqm'):
        raise ValueError('Pillow needs RAQM support for Thai credit shaping')
    size = max(10, round(width * .026))
    body = ImageFont.truetype(str(font), size)
    title = ImageFont.truetype(str(font), round(size * 1.1))
    pad = max(8, width // 60)
    image = Image.new('RGBA', (width, width), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    # Wrap by measured glyph width, including URLs without spaces; never truncate attribution.
    def wrap(text, ft, available):
        lines, line = [], ''
        for char in str(text).replace('\n', ' '):
            if d.textlength(line + char, font=ft) > available and line:
                lines.append(line)
                line = ''
            line += char
        return lines + [line]
    label = {'ref': 'REFERENCE', 'meme': 'MEME', 'gag': 'GAG'}[cue['mode']]
    lines = [(f'{label}  |  {channel}', title), (cue['credit_url'], body)]
    wrapped = [(line, ft) for text, ft in lines for line in wrap(text, ft, width - pad * 2 - size * 2)]
    if len(wrapped) > 8:
        raise ValueError('Credit is too long to read; supply a shorter canonical credit_url')
    row = round(size * 1.65)
    height = pad * 2 + len(wrapped) * row
    image = image.crop((0, 0, width, height))
    d = ImageDraw.Draw(image)
    d.rectangle((0, 0, width, height), fill=(6, 13, 27, 242))
    d.rectangle((0, 0, max(3, width // 180), height), fill=(255, 136, 51, 255))
    # Original geometric icon, drawn here rather than using an emoji/font glyph.
    ix, iy, s = pad, pad + size // 2, size
    if cue['mode'] == 'ref':
        d.rectangle((ix, iy, ix + s, iy + s), outline='#ff8833', width=2)
    elif cue['mode'] == 'meme':
        d.polygon([(ix, iy), (ix + s, iy + s // 2), (ix, iy + s)], fill='#ff8833')
    else:
        d.line([(ix, iy + s // 2), (ix + s // 3, iy), (ix + s // 2, iy + s),
                (ix + s, iy + s // 2)], fill='#ff8833', width=2)
    for n, (text, ft) in enumerate(wrapped):
        d.text((pad + size * 2, pad + n * row), text, font=ft, fill='white')
    p = Path(folder) / f'credit-{index}.png'
    image.save(p)
    return p, height


def render_plan(plan, plan_path):
    base, out = Path(plan['base']), Path(plan['output'])
    font = font_path(plan)
    clips = [fetch_clip(c, plan['cache'], plan['limits']) for c in plan['cues']]
    meta = plan['base_media']
    w, h, fps, duration = meta['width'], meta['height'], meta['fps'], meta['duration']
    with tempfile.TemporaryDirectory(prefix='public-clips-', dir=out.parent) as temp:
        args = ['ffmpeg', '-v', 'error', '-nostdin', '-filter_complex_threads', '2', '-i', base]
        graph = [f'[0:v]setpts=PTS-STARTPTS,setsar=1[v0]']
        audio = []
        if meta['audio']:
            graph += [f'[0:a]aresample=48000,asetpts=PTS-STARTPTS,apad,'
                      f'atrim=duration={duration}[baseaudio]']
        else:
            graph += [f'anullsrc=r=48000:cl=stereo,atrim=duration={duration}[baseaudio]']
        previous_audio = 'baseaudio'
        for index, (cue, clip) in enumerate(zip(plan['cues'], clips)):
            src, png = index * 2 + 1, index * 2 + 2
            at, length = cue['at'], cue['end'] - cue['start']
            stop = at + length
            args += ['-i', clip['path']]
            if cue['mode'] == 'ref':
                x, y, bw, bh = cue['box']
            else:
                x, y, bw, bh = 0, 0, w, h
            credit, ch = card(cue, clip['channel'], bw, temp, index, font)
            if ch >= bh * .65:
                raise ValueError('Credit card leaves too little space for video; enlarge box')
            args += ['-loop', '1', '-framerate', str(fps), '-i', credit]
            # Credit area belongs to the insert's rectangle, never floats over another teaching area.
            if cue.get('visual', True):
                graph += [f'[{src}:v]trim=duration={length},setpts=PTS-STARTPTS,fps={fps},'
                          f'scale={bw}:{bh-ch}:force_original_aspect_ratio=decrease,'
                          f'pad={bw}:{bh-ch}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1[clip{index}]',
                          f'[{png}:v]format=rgba,trim=duration={length},setpts=PTS-STARTPTS[card{index}]',
                          f'[clip{index}]pad={bw}:{bh}:0:0:color=black[padded{index}]',
                          f'[padded{index}][card{index}]overlay=0:{bh-ch}:shortest=1,'
                          f'setpts=PTS-STARTPTS+{at}/TB[insert{index}]']
            else:
                y = h - ch
                graph += [f'[{png}:v]format=rgba,trim=duration={length},'
                          f'setpts=PTS-STARTPTS+{at}/TB[insert{index}]']
            graph += [f'[v{index}][insert{index}]overlay={x}:{y}:eof_action=pass:repeatlast=0:'
                      f"enable='gte(t,{at})*lt(t,{stop})'[v{index+1}]"]
            if cue['audio'] != 'mute' and clip['media']['audio']:
                gain = cue['clip_gain_db'] if cue['audio'] == 'under' else 0
                graph += [f'[{src}:a]atrim=duration={length},asetpts=PTS-STARTPTS,aresample=48000,'
                          f'loudnorm=I=-20:TP=-3:LRA=7,volume={gain}dB,'
                          f'afade=t=in:d=0.015,afade=t=out:st={max(0,length-.025)}:d=0.025,'
                          f'adelay={round(at*1000)}:all=1[a{index}]']
                audio.append(f'[a{index}]')
                if cue['audio'] == 'replace':
                    graph += [f'[{previous_audio}]{duck_filter(at,stop)}[duck{index}]']
                    previous_audio = f'duck{index}'
        inputs = f'[{previous_audio}]' + ''.join(audio)
        graph += [f'{inputs}amix=inputs={len(audio)+1}:duration=first:normalize=0,'
                  'alimiter=limit=0.891:level=false:latency=true[aout]']
        script = Path(temp) / 'filters.txt'
        script.write_text(';\n'.join(graph))
        rendered = Path(temp) / 'render.mp4'
        args += ['-filter_complex', script.read_text(), '-map', f"[v{len(clips)}]", '-map', '[aout]',
                 '-t', str(duration), '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
                 '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', rendered]
        bounded_run(args, temp, max(512*1024**2, int(duration * w * h * fps / 40)),
                    timeout=max(180, int(duration * 20)))
        actual = probe(rendered)
        if abs(actual['duration'] - duration) > max(.12, 2 / fps):
            raise ValueError('Encoded output changed EP duration')
        report_clips = [{**c, **{k: v for k, v in asset.items() if k != 'path'}}
                        for c, asset in zip(plan['cues'], clips)]
        credits = ['Public clip sources / เครดิตคลิปประกอบ', '']
        for cue, clip in zip(plan['cues'], clips):
            credits += [f"EP {cue['at']:.3f}s | {cue['mode']} | {clip['channel']}",
                        clip.get('title') or 'Supplied excerpt', cue['credit_url'],
                        f"Source {cue['start']:.3f}–{cue['end']:.3f}s; excerpt edited for this EP",
                        cue['rights_note'], '']
        report = {'version': '1.0.0', 'created': datetime.now(timezone.utc).isoformat(),
              'plan': str(Path(plan_path).resolve()), 'base_sha256': sha256(base),
              'output_sha256': sha256(rendered), 'output_media': actual, 'clips': report_clips,
              'protected': plan['protected'], 'speech_free': plan['speech_free'],
              'qa': {'duration_pass': True, 'visual_review': 'pending', 'realtime_listening': False,
                     'patsinee_approval': 'pending'},
              'risk': 'Public availability and credits do not verify rights. Review source rights, '
                      'music and Content ID risk before publication.'}
        publish_artifacts(rendered, out, report, '\n'.join(credits), temp)
    return out
