"""Behavior tests use real encoded media; internet access is not required."""
from array import array
import math
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / 'scripts/public_clips.py'


def run(*args):
    return subprocess.run([str(x) for x in args], capture_output=True, text=True)


class PublicClipsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        for name, color, duration, audio in [('base', 'blue', 8, True),
                                              ('excerpt', 'red', 1, True),
                                              ('silent', 'green', 1, False)]:
            args = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                    f'color=c={color}:s=320x180:r=25:d={duration}']
            if audio:
                frequency = 440 if name == 'base' else 880
                args += ['-f', 'lavfi', '-i', f'sine=frequency={frequency}:duration={duration}',
                         '-c:a', 'aac']
            args += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-shortest', cls.root / f'{name}.mp4']
            result = run(*args)
            assert result.returncode == 0, result.stderr

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def plan(self):
        return {'base': 'base.mp4', 'output': 'rendered.mp4', 'timing_reviewed': True,
                'protected': [[0, 1], [6, 8]], 'speech_free': [[4, 5]],
                'cues': [{'mode': 'ref', 'url': 'https://example.org/film',
                          'start': 10, 'end': 11, 'at': 2, 'channel': 'Test channel',
                          'local_excerpt': 'excerpt.mp4', 'audio': 'mute',
                          'rights_note': 'Controlled test media'},
                         {'mode': 'meme', 'url': 'https://example.org/film',
                          'start': 11, 'end': 12, 'at': 3, 'channel': 'Test channel',
                          'local_excerpt': 'silent.mp4', 'audio': 'under',
                          'rights_note': 'Controlled test media'},
                         {'mode': 'gag', 'url': 'https://example.org/film',
                          'start': 12, 'end': 13, 'at': 4, 'channel': 'Test channel',
                          'local_excerpt': 'excerpt.mp4', 'audio': 'replace',
                          'rights_note': 'Controlled test media'}]}

    def invoke(self, plan, action='validate'):
        path = self.root / 'plan.json'
        path.write_text(json.dumps(plan))
        return run('python3', CLI, action, '--plan', path)

    def test_valid_plan_preflight_succeeds_without_fetch(self):
        r = self.invoke(self.plan())
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_protected_instruction_is_rejected_before_download(self):
        p = self.plan()
        p['cues'][0]['at'] = 0.5
        r = self.invoke(p)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('protected', r.stderr)

    def test_source_audio_cannot_replace_active_narration(self):
        p = self.plan()
        p['cues'][0]['audio'] = 'replace'
        r = self.invoke(p)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('speech_free', r.stderr)

    def test_invalid_numbers_overlap_and_end_of_episode_fail(self):
        mutations = [('start', -1), ('end', 10), ('at', 7.5), ('at', float('nan'))]
        for field, value in mutations:
            with self.subTest(field=field, value=value):
                p = self.plan()
                p['cues'][0][field] = value
                self.assertNotEqual(self.invoke(p).returncode, 0)
        p = self.plan()
        p['cues'][1]['at'] = 2.5
        self.assertNotEqual(self.invoke(p).returncode, 0)

    def test_window_timestamps_are_normalized_and_nonfinite_gain_fails(self):
        p = self.plan()
        p['protected'] = [['0', '1'], ['6', '8']]
        r = self.invoke(p)
        self.assertEqual(r.returncode, 0, r.stderr)
        p['cues'][0]['clip_gain_db'] = float('nan')
        self.assertNotEqual(self.invoke(p).returncode, 0)

    def test_ref_box_must_fit_and_protect_presenter(self):
        p = self.plan()
        p['cues'][0]['box'] = [300, 10, 100, 100]
        self.assertNotEqual(self.invoke(p).returncode, 0)

    def test_access_bearing_urls_are_rejected_but_normal_video_ids_work(self):
        for url in ['https://example.org/v?X-Amz-Signature=private',
                    'https://example.org/v?access_token=private',
                    'https://example.org/v#access_token=private']:
            p = self.plan()
            p['cues'][0]['url'] = url
            self.assertNotEqual(self.invoke(p).returncode, 0)
        p = self.plan()
        p['cues'][0]['url'] = 'https://www.youtube.com/watch?v=aqz-KE-bpKQ'
        self.assertEqual(self.invoke(p).returncode, 0)

    def test_local_excerpt_must_be_trimmed_to_requested_duration(self):
        p = self.plan()
        p['cues'][0]['local_excerpt'] = 'base.mp4'
        self.assertNotEqual(self.invoke(p).returncode, 0)

    def test_output_cannot_overwrite_source_or_existing_file(self):
        p = self.plan()
        p['output'] = 'base.mp4'
        self.assertNotEqual(self.invoke(p).returncode, 0)

    def test_existing_sidecar_is_preserved_and_no_movie_is_published(self):
        for suffix in ['.credits.txt', '.report.json']:
            p = self.plan()
            p['output'] = 'collision-' + suffix[1:] + '.mp4'
            out = self.root / p['output']
            side = out.with_suffix(suffix)
            side.write_text('previous review evidence')
            r = self.invoke(p, 'render')
            self.assertNotEqual(r.returncode, 0)
            self.assertEqual(side.read_text(), 'previous review evidence')
            self.assertFalse(out.exists())

    def test_sound_only_gag_retains_picture_and_has_credit(self):
        p = self.plan()
        p['output'] = 'audio-gag.mp4'
        p['cues'] = [p['cues'][2]]
        p['cues'][0]['visual'] = False
        r = self.invoke(p, 'render')
        self.assertEqual(r.returncode, 0, r.stderr)
        pixels = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', '4.5',
                                          '-i', str(self.root / 'audio-gag.mp4'),
                                          '-vf', 'crop=80:20:40:10', '-frames:v', '1',
                                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
        self.assertGreater(sum(pixels[2::3]) / len(pixels[2::3]), 230)
        self.assertLess(sum(pixels[0::3]) / len(pixels[0::3]), 15)

    def test_sixty_fps_insert_reaches_last_scheduled_frame(self):
        p = self.plan()
        base = self.root / 'base60.mp4'
        r = run('ffmpeg', '-v', 'error', '-y', '-i', self.root/'base.mp4',
                '-t', '3', '-r', '60', '-c:v', 'libx264', '-an', base)
        self.assertEqual(r.returncode, 0, r.stderr)
        p.update(base=str(base), output='sixty.mp4', protected=[], speech_free=[])
        p['cues'] = [p['cues'][0]]
        p['cues'][0].update(at=.5, mode='meme')
        r = self.invoke(p, 'render')
        self.assertEqual(r.returncode, 0, r.stderr)
        raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(self.root/'sixty.mp4'),
                                       '-vf', 'crop=2:2:100:10', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
        # Four RGB pixels per frame; frame 89 is 1.4833s, still inside [.5,1.5).
        for frame in [30, 87, 88, 89]:
            self.assertGreater(raw[frame*12], 180, f'missing insert at frame {frame}')
        self.assertLess(raw[90*12], 15)

    def test_sound_gag_after_short_narration_is_not_dropped(self):
        p = self.plan()
        base = self.root/'short-audio.mp4'
        r = run('ffmpeg', '-v', 'error', '-y', '-i', self.root/'base.mp4',
                '-filter_complex', '[0:a]atrim=duration=2[a]', '-map', '0:v', '-map', '[a]',
                '-c:v', 'copy', '-c:a', 'aac', base)
        self.assertEqual(r.returncode, 0, r.stderr)
        p.update(base=str(base), output='tail-gag.mp4', protected=[], speech_free=[[4,5]])
        p['cues']=[p['cues'][2]]
        r=self.invoke(p,'render')
        self.assertEqual(r.returncode, 0, r.stderr)
        raw=subprocess.check_output(['ffmpeg','-v','error','-ss','4.4','-i',
                                     str(self.root/'tail-gag.mp4'),'-t','0.2','-vn',
                                     '-ac','1','-ar','8000','-f','f32le','-'])
        samples=array('f',raw)
        self.assertGreater(len(samples),1000)
        self.assertGreater(sum(v*v for v in samples)/len(samples),0.00001)

    def test_render_three_modes_credits_and_unchanged_teaching_frames(self):
        p = self.plan()
        p['output'] = 'integration.mp4'
        r = self.invoke(p, 'render')
        self.assertEqual(r.returncode, 0, r.stderr)
        out = self.root / 'integration.mp4'
        meta = json.loads(run('ffprobe', '-v', 'error', '-show_format', '-of', 'json', out).stdout)
        self.assertAlmostEqual(float(meta['format']['duration']), 8, delta=0.08)
        credits = out.with_suffix('.credits.txt').read_text()
        self.assertIn('Test channel', credits)
        self.assertIn('https://example.org/film', credits)
        report = json.loads(out.with_suffix('.report.json').read_text())
        self.assertEqual([c['mode'] for c in report['clips']], ['ref', 'meme', 'gag'])
        self.assertEqual(len(report['clips']), 3)
        for t in [0.5, 6.5]:
            pixels = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(out),
                                              '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
            self.assertGreater(sum(pixels[2::3]) / len(pixels[2::3]), 230)
            self.assertLess(sum(pixels[0::3]) / len(pixels[0::3]), 15)
        # Insert content must actually appear, not merely leave the base unchanged.
        pixels = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', '2.5', '-i', str(out),
                                          '-vf', 'crop=80:20:40:10', '-frames:v', '1',
                                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
        self.assertGreater(sum(pixels[0::3]) / len(pixels[0::3]), 180)
        def tone_strength(at, hz):
            raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(at), '-i', str(out),
                                           '-t', '0.2', '-vn', '-ac', '1', '-ar', '8000', '-f', 'f32le', '-'])
            samples = array('f', raw)
            return abs(sum(v * complex(math.cos(2*math.pi*hz*n/8000),
                                       math.sin(2*math.pi*hz*n/8000)) for n, v in enumerate(samples)))
        self.assertGreater(tone_strength(2.4, 440), tone_strength(2.4, 880) * 10)
        self.assertGreater(tone_strength(4.4, 880), tone_strength(4.4, 440) * 10)


if __name__ == '__main__':
    unittest.main()
