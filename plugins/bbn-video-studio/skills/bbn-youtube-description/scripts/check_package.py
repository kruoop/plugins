"""Validate the owner's literal template, repeated title copy and export chapters."""
import argparse
import json
import re
import string
import unicodedata
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('package', type=Path)
parser.add_argument('--duration', type=float, required=True)
parser.add_argument('--resource-post', help='Kruoop resource-post URL that must appear as a resource line')
parser.add_argument('--omit-workshop', action='store_true', help='Deprecated compatibility no-op; locked default already excludes Workshop promotions')
args = parser.parse_args()
template = (Path(__file__).resolve().parent.parent / 'assets/package-template.txt').read_text(encoding='utf-8')
text = args.package.read_text(encoding='utf-8')
assert len(text) < 100000, 'Unexpected package size'
assert '@url' not in text and '`' not in text, 'Package URLs must be plain, without @url or backticks'
assert not re.search(r'(?m)^(?:หมายเหตุสำหรับเจ้าของช่อง|บันทึกตรวจด้วยโค้ด|บันทึกแก้ตามเจ้าของช่อง|รายการรีวิวที่ส่ง|Source และเวลาที่มา|ทิศทางปกและ Prompt ที่ใช้)(?:\s|$)', text), 'Owner notes and internal reports do not belong in Package'
assert re.fullmatch(r'[^\n]+\n?', text.split('\nTags\n', 1)[-1]), 'Package must end after its single Tags line'
pattern, seen = [], set()
for literal, field, _, _ in string.Formatter().parse(template):
    pattern.append(re.escape(literal))
    if field:
        pattern.append(f'(?P={field})' if field in seen else f'(?P<{field}>{".*?" if field == "disclaimer_block" else ".+?"})')
        seen.add(field)
match = re.fullmatch(''.join(pattern), text, flags=re.DOTALL)
assert match, 'Package differs from the fixed template, or repeated title/caption copy differs'
fields = match.groupdict()
assert re.fullmatch(r'EP\d+', fields['episode']), 'Invalid episode label'
assert all(fields[key].endswith('ให้ครับ ☺️') for key in ('ig_main_benefit', 'ig_alt1_benefit', 'ig_alt2_benefit')), 'Invalid IG closing copy'
assert not re.search(r'\{[a-z][a-z0-9_]*\}', text), 'Unfilled template field'
for key, value in fields.items():
    if key not in ('resource_lines', 'timeline', 'disclaimer_block'):
        assert '\n' not in value, f'{key} must occupy one line'
assert not fields['disclaimer_block'] or re.fullmatch(r'(?:⚠️ [^\n]+\n\n)+', fields['disclaimer_block']), 'Disclaimers must be warning paragraphs before resources'
assert not re.search(r'(?m)^\s*🎵', text), 'No music credit in Package: remove the 🎵 line'
assert not args.resource_post or f' — {args.resource_post}' in fields['resource_lines'], 'Kruoop resource post link missing from resource lines'
assert not re.search(r'drive\.google\.com|docs\.google\.com/.*/d/', fields['resource_lines']), 'No Drive links in Description resources'
titles = [fields[key] for key in ('title_main', 'title_alt1', 'title_alt2')]
assert all(len(title.encode('utf-16-le')) // 2 <= 100 and '<' not in title and '>' not in title for title in titles), 'Invalid or overlong Title'
assert all(len(prefix + fields[key]) <= 55 for prefix, key in [('💡 ', 'summary1'), ('✨ ', 'summary2'), ('🌐 ', 'summary3')]), 'Summary exceeds 55 characters'
assert all(re.fullmatch(r'- .+ — https://\S+', line) for line in fields['resource_lines'].splitlines()), 'Invalid resource line'
chapters = []
for line in fields['timeline'].splitlines():
    chapter = re.fullmatch(r'(\d+):([0-5]\d) (.+)', line)
    assert chapter, f'Invalid chapter: {line}'
    chapters.append(int(chapter[1]) * 60 + int(chapter[2]))
assert 3 <= len(chapters) <= 10 and chapters[0] == 0, 'Use 3–10 chapters starting at 0:00'
assert all(b - a >= 10 for a, b in zip(chapters, chapters[1:])), 'Chapter spacing below 10s'
assert args.duration - chapters[-1] >= 10, 'Final chapter extends past the current export'
tags = [tag.strip() for tag in fields['tags'].split(',')]
assert tags and all(tags), 'Empty YouTube tag'
assert not any(tag.startswith('#') for tag in tags), 'Use Tags-field keywords, not hashtags'
assert all(len(tag) <= 30 for tag in tags), 'Individual tag exceeds the channel limit of 30 characters'
normalized_tags = [unicodedata.normalize('NFKC', tag).casefold() for tag in tags]
assert len(set(normalized_tags)) == len(tags), 'Duplicate YouTube tags'
youtube_count = sum(len(tag) + (2 if ' ' in tag else 0) for tag in tags) + len(tags) - 1
assert youtube_count <= 500, 'Tags exceed 500 characters including quotation overhead'
assert not any(re.fullmatch(r'BoomBigNose|บูมบิ๊กโน้ส|EP\s*\d+', tag.strip(), re.IGNORECASE) for tag in tags), 'Disallowed channel/episode tag'
description = text.split('📝 YouTube Description\n\n', 1)[1].split('\n\n\nTags\n', 1)[0]
assert len(description.encode('utf-16-le')) // 2 <= 5000, 'Description exceeds 5000 UTF-16 units'
print(json.dumps({'episode': fields['episode'], 'fixed_template': True, 'plain_urls': True, 'matching_title_and_short_copy': True, 'title_characters': [len(title) for title in titles], 'title_limit': 100, 'description_characters': len(description), 'description_limit': 5000, 'chapters': len(chapters), 'duration': args.duration, 'youtube_tags': len(tags), 'tags_characters': len(fields['tags']), 'youtube_tags_budget_count': youtube_count, 'tags_limit': 500}, ensure_ascii=False))
