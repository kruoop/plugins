"""Resource limits and cache provenance, exercised without internet services."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from array import array

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from public_clip_sources import bounded_run, fetch_clip, sha256


class AcquisitionTest(unittest.TestCase):
    def test_sidecar_race_rolls_back_new_links_without_touching_collision(self):
        from public_clip_render import publish_artifacts
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); rendered=root/'encoded'; rendered.write_bytes(b'encoded media')
            out=root/'review.mp4'; collision=out.with_suffix('.report.json'); collision.mkdir()
            with self.assertRaises(OSError):
                publish_artifacts(rendered,out,{},'credit',root)
            self.assertTrue(collision.is_dir())
            self.assertFalse(out.exists())
            self.assertFalse(out.with_suffix('.credits.txt').exists())

    def test_narration_duck_has_sample_exact_edges_and_keeps_stereo(self):
        from public_clip_render import duck_filter
        raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                                       'aevalsrc=0.1|0.2:s=48000:d=0.2', '-af',
                                       duck_filter(0.05, 0.1), '-f', 'f32le', '-'])
        samples = array('f', raw)
        for n in [2399, 2400, 4799, 4800, 4801]:
            muted = 2400 <= n < 4800
            self.assertAlmostEqual(samples[n*2], 0 if muted else .1, places=6)
            self.assertAlmostEqual(samples[n*2+1], 0 if muted else .2, places=6)

    def test_resource_watchdog_stops_a_hung_child(self):
        with tempfile.TemporaryDirectory() as folder:
            started = time.monotonic()
            with self.assertRaisesRegex(ValueError, 'timed out'):
                bounded_run([sys.executable, '-c', 'import time; time.sleep(30)'],
                            folder, 1024**2, timeout=0.1, reserve_bytes=0)
            self.assertLess(time.monotonic() - started, 3)

    def test_resource_watchdog_stops_an_oversized_child(self):
        with tempfile.TemporaryDirectory() as folder:
            child = "from pathlib import Path; import time; Path('large').write_bytes(b'x'*4096); time.sleep(30)"
            # Child writes only in this test's temporary directory.
            child = child.replace("Path('large')", f'Path({str(Path(folder)/"large")!r})')
            with self.assertRaisesRegex(ValueError, 'size limit'):
                bounded_run([sys.executable, '-c', child], folder, 1024, timeout=5, reserve_bytes=0)

    def test_cache_reuse_preserves_source_identity_and_hash(self):
        import hashlib
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            cue = {'url': 'https://example.org/public-film', 'start': 10, 'end': 11}
            identity = dict(cue)
            key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:24]
            media = root / f'{key}.mp4'
            media.write_bytes(b'controlled previously verified excerpt')
            manifest = {'source': identity, 'sha256': sha256(media), 'path': str(media),
                        'channel': 'Fixture', 'media': {'duration': 1}}
            (root / f'{key}.json').write_text(json.dumps(manifest))
            asset = fetch_clip(cue, root, {'max_bytes': 1024**2, 'timeout': 5})
            self.assertEqual(asset['source']['start'], 10)
            self.assertEqual(asset['acquisition'], 'verified-excerpt-cache')
            self.assertEqual(asset['sha256'], sha256(media))
            cue['channel'] = 'Corrected creator'
            corrected = fetch_clip(cue, root, {'max_bytes': 1024**2, 'timeout': 5})
            self.assertEqual(corrected['channel'], 'Corrected creator')


if __name__ == '__main__':
    unittest.main()
