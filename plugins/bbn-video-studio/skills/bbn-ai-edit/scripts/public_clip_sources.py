"""Bounded excerpt acquisition. No full-video download fallback or account cookies."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                        '-of', 'json', str(path)], capture_output=True, text=True, timeout=30)
    if r.returncode:
        raise ValueError(f'Cannot probe media: {Path(path).name}')
    data = json.loads(r.stdout)
    videos = [s for s in data['streams'] if s['codec_type'] == 'video']
    if not videos:
        raise ValueError('Media has no video stream')
    v = videos[0]
    rate = v.get('avg_frame_rate', '0/1').split('/')
    fps = float(rate[0]) / (float(rate[1]) or 1)
    return {'duration': float(data['format']['duration']), 'width': v['width'],
            'height': v['height'], 'fps': fps or 30,
            'audio': any(s['codec_type'] == 'audio' for s in data['streams'])}


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def bounded_run(args, folder, max_bytes, timeout=180, reserve_bytes=1024**3):
    """Kill the whole process group if disk/time limits are exceeded."""
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        proc = subprocess.Popen([str(a) for a in args], stdout=stdout, stderr=stderr,
                                start_new_session=True)
        started = time.monotonic()
        try:
            while proc.poll() is None:
                size = sum(p.stat().st_size for p in Path(folder).rglob('*') if p.is_file())
                if size > max_bytes or shutil.disk_usage(folder).free < reserve_bytes:
                    raise ValueError('Media operation stopped at disk/size limit')
                if time.monotonic() - started > timeout:
                    raise ValueError('Media operation timed out; no full-download fallback')
                time.sleep(0.2)
            if proc.returncode:
                # Upstream stderr may contain signed media URLs. Keep it out of reports/chat.
                raise ValueError(f'{Path(str(args[0])).name} failed (exit {proc.returncode}); '
                                 'source may require login, be unavailable, or not support partial retrieval')
            stdout.seek(0)
            return stdout.read().decode('utf-8', errors='replace')
        finally:
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()


def fetch_clip(cue, cache, limits):
    length = cue['end'] - cue['start']
    identity = {k: cue[k] for k in ('url', 'start', 'end')}
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:24]
    cache = Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    media, manifest = cache / f'{key}.mp4', cache / f'{key}.json'
    if cue.get('local_excerpt'):
        p = Path(cue['local_excerpt'])
        return {'path': str(p), 'sha256': sha256(p), 'acquisition': 'supplied-trimmed-excerpt',
                'channel': cue['channel'], 'source': identity, 'media': probe(p)}
    if media.exists() and manifest.exists():
        saved = json.loads(manifest.read_text())
        if saved.get('source') == identity and saved.get('sha256') == sha256(media):
            saved['acquisition'] = 'verified-excerpt-cache'
            saved['path'] = str(media.resolve())
            saved['channel'] = cue.get('channel') or saved.get('source_channel') or saved['channel']
            return saved
    with tempfile.TemporaryDirectory(prefix='fetch-', dir=cache) as temp:
        installed = Path(sys.executable).parent / 'yt-dlp'
        downloader = str(installed) if installed.is_file() else 'yt-dlp'
        common = [downloader, '--ignore-config', '--no-playlist', '--no-warnings',
                  '--socket-timeout', '20', '--retries', '1', '--fragment-retries', '1']
        info = json.loads(bounded_run(common + ['--dump-single-json', '--skip-download', cue['url']],
                                     temp, limits['max_bytes'], timeout=90))
        if info.get('is_live') or info.get('has_drm'):
            raise ValueError('Live/DRM sources are not supported')
        if info.get('duration') and cue['end'] > float(info['duration']):
            raise ValueError('Source excerpt exceeds source duration')
        source_channel = info.get('channel') or info.get('uploader')
        channel = cue.get('channel') or source_channel
        if not channel:
            raise ValueError('Source has no channel credit; supply channel in the plan')
        # Force FFmpeg section seeking; never retry with ordinary whole-file download.
        command = common + ['--download-sections', f"*{cue['start']}-{cue['end']}",
                            '--downloader', 'ffmpeg', '--force-keyframes-at-cuts',
                            '-f', 'bv*[height<=1080]+ba/b[height<=1080]/b',
                            '--merge-output-format', 'mp4', '--max-filesize',
                            str(limits['max_bytes']), '-o', str(Path(temp) / 'section.%(ext)s'),
                            cue['url']]
        bounded_run(command, temp, limits['max_bytes'], timeout=limits['timeout'])
        candidates = [p for p in Path(temp).glob('section.*')
                      if p.suffix not in ('.part', '.ytdl', '.json')]
        if len(candidates) != 1:
            raise ValueError('Section downloader did not produce exactly one media file')
        source = candidates[0]
        meta = probe(source)
        if abs(meta['duration'] - length) > max(0.12, 2 / meta['fps']):
            raise ValueError('Downloaded section duration differs from requested range')
        if source.stat().st_size > limits['max_bytes']:
            raise ValueError('Downloaded section exceeds size budget')
        # Keep the original container extension (FFmpeg probes it, independent of .mp4 name).
        saved = {'path': str(media), 'sha256': sha256(source), 'source': identity,
                 'channel': channel, 'source_channel': source_channel,
                 'title': info.get('title'), 'license': info.get('license'),
                 'acquisition': 'yt-dlp-ffmpeg-section', 'media': meta,
                 'bytes': source.stat().st_size}
        os.replace(source, media)
        manifest.write_text(json.dumps(saved, ensure_ascii=False, indent=2))
        return saved
