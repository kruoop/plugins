"""Offline regression tests for the owner-locked Package format; all fixtures are synthetic test data."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1]
TEMPLATE = (SKILL / 'assets/package-template.txt').read_text(encoding='utf-8')
CHECKER = SKILL / 'scripts/check_package.py'


def fixture(**changes):
    fields = dict(episode='EP9999', title_main='ทดสอบรูปแบบตัวหลัก', title_alt1='ทดสอบรูปแบบสำรองหนึ่ง', title_alt2='ทดสอบรูปแบบสำรองสอง', keyword='TEST', ig_main_benefit='ทดสอบตัวหลักให้ครับ ☺️', ig_alt1_benefit='ทดสอบสำรองหนึ่งให้ครับ ☺️', ig_alt2_benefit='ทดสอบสำรองสองให้ครับ ☺️', summary1='ข้อความ fixture ทดสอบหนึ่ง', summary2='ข้อความ fixture ทดสอบสอง', summary3='ข้อความ fixture ทดสอบสาม', disclaimer_block='', resource_lines='- Test resource — https://example.com/tool', timeline='00:00 ทดสอบหนึ่ง\n00:20 ทดสอบสอง\n00:40 ทดสอบสาม', tags='test,format test')
    fields.update(changes)
    return TEMPLATE.format(**fields)


class LockedPackageTests(unittest.TestCase):
    def run_check(self, text, ok, *extra):
        # Hermes TMPDIR is the profile's managed scratch directory, never system temp.
        with tempfile.TemporaryDirectory(prefix='package-format-test-', dir=os.environ.get('TMPDIR')) as temp:
            path = Path(temp) / 'fixture.txt'
            path.write_text(text, encoding='utf-8')
            result = subprocess.run([sys.executable, str(CHECKER), str(path), '--duration', '60', *extra], capture_output=True, text=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertTrue(report['fixed_template'] and report['plain_urls'])
        else:
            self.assertNotEqual(result.returncode, 0, 'Invalid fixture unexpectedly passed')

    def test_locked_default_without_disclaimer(self):
        self.run_check(fixture(), True)

    def test_locked_default_with_required_disclaimer(self):
        self.run_check(fixture(disclaimer_block='⚠️ คำเตือนใน fixture ทดสอบเท่านั้น\n\n'), True)

    def test_reject_url_marker(self):
        self.run_check(fixture().replace('https://example.com/tool', '@url:https://example.com/tool'), False)

    def test_reject_backticks(self):
        self.run_check(fixture().replace('https://example.com/tool', '`https://example.com/tool`'), False)

    def test_reject_contact_change(self):
        self.run_check(fixture().replace('contact@boombignose.org', 'changed@example.com'), False)

    def test_reject_old_kruoop_link(self):
        self.run_check(fixture().replace('https://kruoop.com/about?c=boombignose', 'https://kruoop.com/s/post/old-test-only'), False)

    def test_reject_automatic_hostinger(self):
        self.run_check(fixture().replace('💡 ', '☺️ Hostinger https://example.com/promo\n\n💡 ', 1), False)

    def test_reject_automatic_workshop(self):
        self.run_check(fixture().replace('🌟 ', '📍 Workshop https://example.com/promo\n\n🌟 ', 1), False)

    def test_reject_heading_change(self):
        self.run_check(fixture().replace('💎 ลิงก์สำคัญ', 'Resources'), False)

    def test_reject_emoji_change(self):
        self.run_check(fixture().replace('💡 ', '🔍 ', 1), False)

    def test_reject_repeated_title_drift(self):
        self.run_check(fixture().replace('ทดสอบรูปแบบตัวหลัก', 'ชื่อไม่ตรง', 1), False)

    def test_reject_internal_notes_tail(self):
        self.run_check(fixture() + '\nบันทึกตรวจด้วยโค้ด fixture\n', False)

    def test_reject_overlong_title(self):
        self.run_check(fixture(title_main='ก' * 101), False)

    def test_reject_overlong_summary(self):
        self.run_check(fixture(summary1='ก' * 56), False)

    def test_reject_tags_budget_overflow(self):
        self.run_check(fixture(tags=','.join('test keyword ' + str(i).zfill(15) for i in range(26))), False)

    def test_reject_music_credit(self):
        self.run_check(fixture(resource_lines='- Test resource — https://example.com/tool\n\n🎵 เพลง: Do It — Infraction'), False)

    def test_resource_post_link_required(self):
        url = 'https://kruoop.com/s/post/test-resource'
        self.run_check(fixture(), False, '--resource-post', url)
        self.run_check(fixture(resource_lines=f'- ไฟล์ resource แจกฟรีในชุมชน Kruoop — {url}'), True, '--resource-post', url)

    def test_reject_drive_link_resource(self):
        self.run_check(fixture(resource_lines='- resource — https://drive.google.com/file/d/abc/view'), False)

    def test_ep242_reference_passes(self):
        text = (SKILL / 'assets/reference-EP242_Package.txt').read_text(encoding='utf-8')
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as temp:
            path = Path(temp) / 'EP242_Package.txt'
            path.write_text(text, encoding='utf-8')
            result = subprocess.run([sys.executable, str(CHECKER), str(path), '--duration', '600'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
