"""Check Skool plain text, source-only resource links and the waiting video line."""
import argparse, json, re
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('file', type=Path)
parser.add_argument('--forbid-video-url', action='append', default=[])
args = parser.parse_args()
text = args.file.read_text(encoding='utf-8')
member = text.split('หมายเหตุสำหรับเจ้าของช่อง — ไม่นำไปวางใน Skool', 1)[0]
assert not any(c in member for c in '#*"\'`“”‘’'), 'Publication copy contains markup or quotes'
assert member.startswith('1) ชื่อคอร์ส 3 ตัวเลือก\n'), 'Missing course-title heading'
titles = re.findall(r'^\d\. (.+)$', member.split('2) Course description')[0], re.M)
length = lambda value: len(value.encode('utf-16-le')) // 2
assert len(titles) == 3 and all(length(t) <= 50 and not re.search(r'EP\s*\d', t, re.I) for t in titles), 'Invalid course titles'
desc = member.split('2) Course description\n\n', 1)[1].split('\n\n🌟 ', 1)[0]
assert length(desc) < 480, 'Course description too long'
tabs = [line for line in member.splitlines() if line.startswith(('🌟', '🍀', '🔥', '💎'))]
assert len(tabs) == 4 and [line[0] for line in tabs] == ['🌟', '🍀', '🔥', '💎'], 'Invalid four-tab order'
first = member.split('🌟 ', 1)[1].split('\n🍀 ', 1)[0]
body, source = member.split('\n💎 Source Code เทมเพลต\n', 1)
assert not any(phrase in member for phrase in ('การบ้าน', 'แบบฝึกหัด', 'โจทย์ให้ฝึกต่อ', 'โจทย์ฝึกต่อ')), 'Homework framing instead of Exclusive teaching'
assert not re.search(r'https?://|www\.', body, re.I), 'Links outside Source Code'
assert 'ลิงก์วิดีโอ: รอส่งลิงก์' in first, 'Missing waiting video link'
assert not any(url in member for url in args.forbid_video_url), 'Episode review link leaked into Skool copy'
assert not re.search(r'https?://(?:www\.)?(?:youtube\.com|youtu\.be|vimeo\.com)/|(?:วิดีโอหลัก|ลิงก์คลิป)\s*:', source), 'Video link in Source Code'
assert all(heading in member for heading in ('ทำไมต้องทำแบบนี้', 'Workflow', 'เครื่องมือ', 'ลิงก์สำคัญ')), 'Missing reference sections'
print(json.dumps({'titles_utf16': [length(t) for t in titles], 'description_utf16': length(desc), 'four_tabs': True, 'video_placeholder': True, 'links_only_in_source_code': True, 'source_code_without_video_links': True}, ensure_ascii=False))
