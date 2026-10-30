"""Exercise cleanup orchestration without loading a model or doing inference."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import soundfile as sf
from pythainlp import word_tokenize

import voice_engine
from voice_quality import normalized


SETTINGS = {
    'steps': 32, 'guidance': 2.0, 'seed': 42, 'pace_factor': .85,
    'pitch_semitones': -.5, 'pause_phrase': .14, 'pause_sentence': .4,
    'pause_topic': .6, 'pause_paragraph': .75, 'pause_scale': 1.0,
}
REFERENCE_TEXT = 'ซึ่งในวันนี้นะครับ ผมก็จะอธิบายทั้งหมดเลยว่า อีอาร์พีตรงนี้นะครับ'


def transcript(text):
    tokens = word_tokenize(text, engine='newmm', keep_whitespace=True)
    return {'text': text, 'segments': [{'words': [
        {'word': word, 'start': index * .08, 'end': (index + 1) * .08,
         'probability': .99}
        for index, word in enumerate(tokens)
    ]}]}


class FakeModel:
    audio_tokenizer = object()

    def __init__(self):
        self.calls = []

    def generate(self, **kwargs):
        self.calls.append(kwargs)
        audio = .2 * np.sin(np.arange(96000, dtype=np.float32) * (2 * np.pi * 180 / 24000))
        yield SimpleNamespace(audio=audio, sample_rate=24000)


class RepairChunkTests(unittest.TestCase):
    def setUp(self):
        estimator = voice_engine.RuleDurationEstimator()
        self.seconds_per_weight = 5.6 / estimator.calculate_total_weight(REFERENCE_TEXT) * .85

    def test_actual_missing_reading_prefix_is_kept_as_one_child(self):
        source = 'ตรงไหนที่อ่านแล้วรู้สึกว่าไม่ใช่คำที่เราพูดตามปกติ ก็แก้ให้เป็นภาษาของเราได้เลย'
        analysis = {'cleaned_text': normalized('รู้สึกว่าไม่ใช่คำที่เราพูดตามปกติ ก็แก้ให้เป็นภาษาของเราได้เลย')}
        children = voice_engine.repair_chunks(source, analysis, self.seconds_per_weight)
        self.assertEqual(children[0], 'ตรงไหนที่อ่านแล้ว')
        self.assertEqual(children, ['ตรงไหนที่อ่านแล้ว', 'รู้สึกว่าไม่ใช่คำที่เราพูดตามปกติ',
                                    'ก็แก้ให้เป็นภาษาของเราได้เลย'])
        self.assertEqual(normalized(''.join(children)), normalized(source))

    def test_actual_work_prefix_extends_to_complete_clause(self):
        source = 'งานเดิมใช้เวลานานแค่ไหน งานใหม่เร็วขึ้นตรงไหน แล้วมีจุดไหนที่ต้องกลับมาแก้บ่อย'
        analysis = {'cleaned_text': normalized('ใช้เวลานานแค่ไหน งานใหม่เร็วขึ้นตรงไหน แล้วมีจุดไหนที่ต้องกลับมาแก้บ่อย')}
        children = voice_engine.repair_chunks(source, analysis, self.seconds_per_weight)
        self.assertEqual(children[0], 'งานเดิมใช้เวลานานแค่ไหน')
        self.assertEqual(children, ['งานเดิมใช้เวลานานแค่ไหน', 'งานใหม่เร็วขึ้นตรงไหน',
                                    'แล้วมีจุดไหนที่ต้องกลับมาแก้บ่อย'])
        self.assertNotIn('บ่อย', children)
        self.assertEqual(normalized(''.join(children)), normalized(source))

    def test_tiny_trailing_word_merges_with_previous_child(self):
        source = 'แล้วมีจุดไหนที่ต้องกลับมาแก้ บ่อย'
        children = voice_engine.repair_chunks(source, {'cleaned_text': normalized(source)},
                                             self.seconds_per_weight)
        self.assertNotIn('บ่อย', children)
        self.assertEqual(normalized(''.join(children)), normalized(source))

    def test_asr_deletion_inside_word_anchors_complete_source_word(self):
        source = 'วันนี้เราจะจัดระเบียบไฟล์ในคอมพิวเตอร์ แล้วอธิบายขั้นตอนให้เพื่อนเข้าใจ'
        heard = 'เบียบไฟล์ในคอมพิวเตอร์ แล้วอธิบายขั้นตอนให้เพื่อนเข้าใจ'
        children = voice_engine.repair_chunks(source, {'cleaned_text': normalized(heard)},
                                             self.seconds_per_weight)
        self.assertEqual(children[0], 'วันนี้เราจะจัดระเบียบ')
        self.assertEqual(children[1], 'ไฟล์ในคอมพิวเตอร์')
        self.assertEqual(normalized(''.join(children)), normalized(source))

    def test_standalone_repetition_mark_attaches_previous_child(self):
        source = 'เราจะค่อย ๆ พัฒนาโปรเจกต์ด้วยกันครับ'
        children = voice_engine.repair_chunks(source, {'cleaned_text': normalized(source)},
                                             self.seconds_per_weight)
        self.assertNotIn('ๆ', children)
        self.assertTrue(any('ค่อย ๆ' in child for child in children))
        self.assertEqual(normalized(''.join(children)), normalized(source))


class EngineQualityTests(unittest.TestCase):
    def run_engine(self, source, heard):
        model = FakeModel()
        checks = []

        def checker(audio, sample_rate):
            self.assertEqual(sample_rate, 24000)
            self.assertTrue(len(audio))
            text = heard(len(checks), model.calls[-1]['text'])
            checks.append(text)
            return transcript(text)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            model_path = root / 'models' / 'voice'
            model_path.mkdir(parents=True)
            (model_path / 'model.safetensors').write_bytes(b'fake model identity')
            reference = root / 'reference.wav'
            sf.write(reference, np.ones(48000, dtype=np.float32) * .1, 24000)
            output = root / 'output.wav'
            scan = SimpleNamespace(stderr='silence_start: 0.2\nsilence_end: 0.7', returncode=0)
            with patch('mlx_audio.tts.utils.load_model', return_value=model) as load, \
                 patch('mlx_audio.tts.models.omnivoice.utils.create_voice_clone_prompt', return_value=object()), \
                 patch('mlx.core.set_cache_limit'), patch('mlx.core.clear_cache'), \
                 patch('mlx.core.random.seed'), \
                 patch.object(voice_engine, 'ThaiChecker', return_value=checker), \
                 patch.object(voice_engine, 'lower_pitch_file', side_effect=lambda src, dst, _: shutil.copyfile(src, dst)), \
                 patch.object(voice_engine.subprocess, 'run', return_value=scan) as cleanup:
                voice_engine.synthesize(str(reference), REFERENCE_TEXT, source, str(output),
                                        model_path, SETTINGS.copy())
            self.assertEqual(load.call_count, 1)
            cleanup.assert_called_once()
            self.assertIn('silencedetect=noise=-45dB:d=0.15', cleanup.call_args.args[0])
            report = json.loads(output.with_suffix('.json').read_text())
            self.assertTrue(report['quality']['silence_cuts'])
            self.assertTrue(output.is_file())
            return model.calls, checks, report

    def test_missing_prefix_gets_one_repair_and_cleanup(self):
        source = 'ตรงไหนที่อ่านแล้วรู้สึกว่าไม่ใช่คำที่เราพูดตามปกติ'
        calls, checks, report = self.run_engine(
            source, lambda index, requested: 'รู้สึกว่าไม่ใช่คำที่เราพูดตามปกติ' if index == 0 else requested)
        self.assertEqual(len(calls), 3)  # Original plus two checked prefix/body repairs.
        self.assertEqual(len(checks), 3)
        self.assertEqual(len(report['quality']['details'][0]['repairs']), 2)
        self.assertEqual(report['quality']['repair_round_limit'], 1)
        self.assertTrue(report['quality']['details'][0]['initial']['needs_repair'])
        self.assertEqual(report['quality']['details'][0]['selected'], 'repair')
        self.assertEqual(report['quality']['status'], 'passed')
        self.assertFalse(report['quality']['details'][0]['needs_review'])

    def test_persistent_mismatch_stops_after_one_repair_round(self):
        calls, checks, report = self.run_engine(
            'ตรงไหนที่อ่านแล้วรู้สึกว่าไม่ใช่คำที่เราพูดตามปกติ',
            lambda index, requested: 'นา นา นา นา')
        self.assertEqual(len(calls), 2)
        self.assertEqual(len(checks), 2)
        self.assertEqual(report['quality']['status'], 'needs_review')
        self.assertTrue(report['quality']['flags'])
        self.assertTrue(report['quality']['details'][0]['needs_review'])

    def test_requested_filler_is_preserved_while_silence_cleanup_runs(self):
        calls, checks, report = self.run_engine(
            'คำว่า เอ่อ ใช้แสดงความลังเล', lambda index, requested: requested)
        self.assertEqual(len(calls), 1)
        self.assertEqual(len(checks), 1)
        self.assertEqual(report['quality']['details'][0]['initial']['cuts'], [])
        self.assertEqual(report['quality']['status'], 'passed')
        self.assertAlmostEqual(report['duration'], 3.58, places=3)

    def test_repeated_words_in_separate_phrases_are_checked_independently(self):
        calls, checks, report = self.run_engine(
            'ขอบคุณครับ\nครับผมจะทำงานต่อ', lambda index, requested: requested)
        self.assertEqual([call['text'] for call in calls], ['ขอบคุณครับ', 'ครับผมจะทำงานต่อ'])
        self.assertEqual(checks, ['ขอบคุณครับ', 'ครับผมจะทำงานต่อ'])
        self.assertEqual(report['quality']['status'], 'passed')
        self.assertEqual(len(report['quality']['details']), 2)
        for detail in report['quality']['details']:
            self.assertEqual(detail['initial']['cuts'], [])
            self.assertEqual(detail['repairs'], [])


if __name__ == '__main__':
    unittest.main()
