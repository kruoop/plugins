"""Source-aware cleanup checks; no ASR model or synthesis is required."""
import unittest

import numpy as np

from voice_quality import analyze_phrase, remove_intervals, silence_cuts


def transcript(*words):
    return {
        'text': ''.join(words),
        'segments': [{'words': [
            {'word': word, 'start': index * .25, 'end': (index + 1) * .25,
             'probability': .99}
            for index, word in enumerate(words)
        ]}],
    }


class PhraseQualityTests(unittest.TestCase):
    def test_explicit_filler_is_preserved(self):
        result = analyze_phrase('คำว่า เอ่อ ใช้แสดงความลังเล',
                                transcript('คำว่า ', 'เอ่อ ', 'ใช้', 'แสดง', 'ความลังเล'), 2)
        self.assertEqual(result['cuts'], [])
        self.assertFalse(result['needs_repair'])

    def test_unwanted_filler_is_cut(self):
        result = analyze_phrase('สวัสดีครับทุกคน',
                                transcript('เอ่อ ', 'สวัสดี', 'ครับ', 'ทุกคน'), 2)
        self.assertEqual(len(result['cuts']), 1)
        self.assertEqual(result['cuts'][0]['text'].strip(), 'เอ่อ')
        self.assertEqual(result['cuts'][0]['reason'], 'filler')
        self.assertFalse(result['needs_repair'])

    def test_thai_repetition_mark_preserves_both_spoken_words(self):
        result = analyze_phrase('ค่อย ๆ ทำงาน',
                                transcript('ค่อย ', 'ค่อย ', 'ทำงาน'), 2)
        self.assertEqual(result['cuts'], [])
        self.assertFalse(result['needs_repair'])

    def test_unwanted_adjacent_repeat_is_cut(self):
        result = analyze_phrase('ค่อยทำงานให้เสร็จ',
                                transcript('ค่อย ', 'ค่อย ', 'ทำงาน', 'ให้', 'เสร็จ'), 2)
        self.assertEqual(len(result['cuts']), 1)
        self.assertEqual(result['cuts'][0]['text'].strip(), 'ค่อย')
        self.assertEqual(result['cuts'][0]['reason'], 'repeat')
        self.assertFalse(result['needs_repair'])

    def test_repeated_source_words_across_sentences_are_preserved(self):
        result = analyze_phrase('ครับ. ครับผมจะทำต่อ',
                                transcript('ครับ. ', 'ครับ', 'ผม', 'จะ', 'ทำต่อ'), 2)
        self.assertEqual(result['cuts'], [])
        self.assertFalse(result['needs_repair'])

    def test_source_word_after_matching_suffix_is_preserved(self):
        result = analyze_phrase('ผลงานดูดี ดีพอที่จะใช้ต่อได้',
                                transcript('ผลงาน', 'ดูดี ', 'ดี', 'พอ', 'ที่จะ', 'ใช้ต่อได้'), 2)
        self.assertEqual(result['cuts'], [])
        self.assertFalse(result['needs_repair'])

    def test_missing_prefix_requires_regeneration(self):
        result = analyze_phrase('ตรงไหนที่อ่านแล้วรู้สึกว่าไม่ใช่คำที่เราพูดตามปกติ',
                                transcript('รู้สึก', 'ว่า', 'ไม่ใช่', 'คำ', 'ที่', 'เรา', 'พูด', 'ตามปกติ'), 3)
        self.assertTrue(result['needs_repair'])

    def test_single_character_asr_difference_does_not_require_repair(self):
        result = analyze_phrase('เราจะค่อยพัฒนาโปรเจกต์นี้ให้ดีขึ้นด้วยกันครับ',
                                transcript('เรา', 'จะ', 'คอย', 'พัฒนา', 'โปรเจกต์', 'นี้',
                                           'ให้', 'ดี', 'ขึ้น', 'ด้วยกัน', 'ครับ'), 4)
        self.assertFalse(result['needs_repair'])
        self.assertEqual(result['cuts'], [])

    def test_ai_alias_does_not_require_repair(self):
        result = analyze_phrase('เราจะใช้เอไอช่วยทำงานให้เสร็จ',
                                transcript('เรา', 'จะ', 'ใช้', 'AI', 'ช่วย', 'ทำงาน', 'ให้', 'เสร็จ'), 3)
        self.assertFalse(result['needs_repair'])
        self.assertEqual(result['cuts'], [])

    def test_invalid_word_timestamp_never_produces_destructive_cut(self):
        for start, end in ((0, 10), (-.1, .25), (.5, .25), (float('nan'), .25)):
            with self.subTest(start=start, end=end):
                heard = transcript('เอ่อ ', 'สวัสดี', 'ครับ', 'ทุกคน')
                heard['segments'][0]['words'][0].update(start=start, end=end)
                result = analyze_phrase('สวัสดีครับทุกคน', heard, 2)
                self.assertEqual(result['cuts'], [])
                self.assertTrue(result['needs_repair'])

    def test_empty_asr_requires_repair(self):
        result = analyze_phrase('สวัสดีครับทุกคน', {'text': '', 'segments': []}, 2)
        self.assertTrue(result['needs_repair'])
        self.assertEqual(result['cuts'], [])

    def test_backward_or_overlapping_word_times_require_review(self):
        for first, second in (((.25, .5), (0, .25)), ((0, .25), (.1, .5))):
            with self.subTest(first=first, second=second):
                heard = transcript('เอ่อ ', 'สวัสดี', 'ครับ', 'ทุกคน')
                heard['segments'][0]['words'][0].update(start=first[0], end=first[1])
                heard['segments'][0]['words'][1].update(start=second[0], end=second[1])
                result = analyze_phrase('สวัสดีครับทุกคน', heard, 2)
                self.assertEqual(result['cuts'], [])
                self.assertTrue(result['needs_repair'])

    def test_invalid_probabilities_require_review_without_cuts(self):
        for probability in (float('nan'), float('inf'), -1, 1.1):
            with self.subTest(probability=probability):
                heard = transcript('เอ่อ ', 'สวัสดี', 'ครับ', 'ทุกคน')
                heard['segments'][0]['words'][0]['probability'] = probability
                result = analyze_phrase('สวัสดีครับทุกคน', heard, 2)
                self.assertEqual(result['cuts'], [])
                self.assertTrue(result['needs_repair'])

    def test_uncertain_or_too_short_extra_filler_requires_review(self):
        for probability, end in ((.3, .25), (.99, .04)):
            with self.subTest(probability=probability, end=end):
                heard = transcript('เอ่อ ', 'สวัสดี', 'ครับ', 'ทุกคน')
                heard['segments'][0]['words'][0].update(probability=probability, end=end)
                result = analyze_phrase('สวัสดีครับทุกคน', heard, 2)
                self.assertEqual(result['cuts'], [])
                self.assertTrue(result['needs_repair'])

    def test_repeated_syllable_meltdown_requires_repair(self):
        result = analyze_phrase('งานเดิมใช้เวลานานแค่ไหน',
                                transcript('นา ', 'นา ', 'นา ', 'นา ', 'นา '), 2)
        self.assertTrue(result['needs_repair'])


class AudioEditTests(unittest.TestCase):
    def test_overlapping_cuts_remove_union_once(self):
        audio = np.ones(1000, dtype=np.float32)
        result = remove_intervals(audio, 100, [
            {'start': 1, 'end': 3}, {'start': 2, 'end': 4},
        ])
        self.assertEqual(len(result), 700)
        self.assertTrue(np.isfinite(result).all())

    def test_out_of_bounds_cuts_are_rejected(self):
        audio = np.ones(1000, dtype=np.float32)
        for cut in ({'start': 0, 'end': 11}, {'start': -1, 'end': 1},
                    {'start': 3, 'end': 2}):
            with self.subTest(cut=cut), self.assertRaises(ValueError):
                remove_intervals(audio, 100, [cut])

    def test_long_silence_retains_eighty_milliseconds(self):
        cuts = silence_cuts('silence_start: 1.0\nsilence_end: 1.5', 2)
        self.assertEqual(len(cuts), 1)
        self.assertAlmostEqual(cuts[0]['start'], 1.04)
        self.assertAlmostEqual(cuts[0]['end'], 1.46)
        self.assertAlmostEqual(.5 - (cuts[0]['end'] - cuts[0]['start']), .08)

    def test_short_or_unpaired_silence_is_safe(self):
        self.assertEqual(silence_cuts('silence_start: 1.9', 2), [])
        self.assertEqual(silence_cuts('silence_end: 1.5', 2), [])
        self.assertEqual(silence_cuts('silence_start: 1.0\nsilence_end: 1.1', 2), [])


if __name__ == '__main__':
    unittest.main()
