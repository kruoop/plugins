"""Breath cleanup and best-take helpers; synthetic audio only, no models."""
import tempfile
import unittest
from pathlib import Path

import numpy as np

from best_take import added_particles, read_lines, strip_asr_loop, too_long, without_terms
from voice_quality import breath_spans, clean_breaths

SR = 24000
rng = np.random.default_rng(1)


def vowel(seconds):
    t = np.arange(int(seconds * SR)) / SR
    return (.5 * np.sin(2 * np.pi * 150 * t) * np.hanning(len(t))).astype(np.float32)


def inhale(seconds):
    noise = rng.standard_normal(int(seconds * SR)).astype(np.float32)
    # broadband hiss weighted to 1.5–5 kHz like a measured inhale (flatness ~.2, centroid ~3.5 kHz), quiet
    spectrum = np.fft.rfft(noise)
    freqs = np.fft.rfftfreq(len(noise), 1 / SR)
    spectrum *= np.where(freqs < 1500, .15, np.where(freqs <= 5000, 1, .4))
    hiss = np.fft.irfft(spectrum, len(noise))
    return (.05 * hiss / np.std(hiss)).astype(np.float32)


class BreathTests(unittest.TestCase):
    def test_inner_inhale_is_muted_and_voice_kept(self):
        audio = np.concatenate([vowel(.6), inhale(.3), vowel(.6)])
        out, info = clean_breaths(audio, SR, drop_lead=False)
        self.assertEqual(len(out), len(audio))
        self.assertEqual(len(info['breaths_muted']), 1)
        span = info['breaths_muted'][0]
        self.assertTrue(.5 <= span['start'] <= .7 and .8 <= span['end'] <= 1.0, span)
        self.assertLess(np.abs(out[int(.75 * SR):int(.85 * SR)]).max(), 1e-6)
        self.assertGreater(np.abs(out[int(.2 * SR):int(.4 * SR)]).max(), .3)

    def test_leading_filler_and_inhale_are_dropped(self):
        audio = np.concatenate([vowel(.2), inhale(.25), vowel(.6)])
        out, info = clean_breaths(audio, SR)
        self.assertTrue(.35 <= info['lead_cut'] <= .6, info)
        self.assertEqual(len(out), len(audio) - round(info['lead_cut'] * SR))

    def test_short_aspiration_survives(self):
        audio = np.concatenate([vowel(.5), inhale(.06), vowel(.5)])
        self.assertEqual(breath_spans(audio, SR), [])

    def test_short_word_then_plain_pause_is_kept(self):
        audio = np.concatenate([vowel(.3), np.zeros(int(.2 * SR), np.float32), vowel(.5)])
        self.assertEqual(clean_breaths(audio, SR)[1]['lead_cut'], 0)

    def test_line_start_word_is_kept_without_inhale(self):
        audio = np.concatenate([vowel(.3), vowel(.5)])
        self.assertEqual(clean_breaths(audio, SR)[1]['lead_cut'], 0)


class TakeHelperTests(unittest.TestCase):
    def test_added_particles(self):
        self.assertEqual(added_particles('กฎสำคัญควรเขียนไว้', 'กฎสำคัญควรเขียนไว้นะครับ'), ['นะครับ'])
        self.assertEqual(added_particles('ถามเราก่อน', 'ถามเราก่อนเนี่ยครับ'), ['ครับ', 'เนี่ย'])
        self.assertEqual(added_particles('สวัสดีครับ', 'สวัสดีครับ'), [])
        self.assertEqual(added_particles('ใส่เข้าไป', 'ใส่เข้าไปค่ะ'), ['ค่ะ'])

    def test_runaway_take_is_too_long(self):
        self.assertFalse(too_long('กฎสำคัญเลยควรเขียนไว้', 2.6))
        self.assertTrue(too_long('กฎสำคัญเลยควรเขียนไว้', 12.0))

    def test_asr_loop_is_cut(self):
        pieces = ['กฎ', ' cross', '.md', 'สิน', 'ค้า', ' สิน', 'ค้า', ' สิน', 'ค้า', ' สิน', 'ค้า']
        loop = {'text': ''.join(pieces), 'segments': [{'words': [{'word': w} for w in pieces]}]}
        out = strip_asr_loop(loop)
        self.assertEqual(out['text'], 'กฎ cross.md')
        self.assertEqual(len(out['segments'][0]['words']), 3)
        keep = {'text': 'ไปเรื่อย เรื่อย อ่านไฟล์', 'segments': [{'words': [{'word': 'ไปเรื่อย'}]}]}
        self.assertIs(strip_asr_loop(keep), keep)

    def test_ignored_terms_leave_both_sides(self):
        pieces = ['กฎ', 'สำคัญ', ' cross', '.md']
        text, out = without_terms('กฎสำคัญ คล็อดดอตเอ็มดี', {'text': '', 'segments': [{'words': [{'word': w} for w in pieces]}]}, ['คล็อดดอตเอ็มดี'])
        self.assertEqual(text, 'กฎสำคัญ')
        self.assertEqual(out['text'], 'กฎสำคัญ')

    def test_read_lines_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'l.txt'
            path.write_text('hook-1|เอไอ แค่ทายคำ\n\nบรรทัดสอง\n', encoding='utf-8')
            self.assertEqual(read_lines(path), [('hook-1', 'เอไอ แค่ทายคำ'), ('line-002', 'บรรทัดสอง')])


if __name__ == '__main__':
    unittest.main()
