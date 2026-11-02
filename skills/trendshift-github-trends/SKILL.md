---
name: trendshift-github-trends
description: Use when you need trending GitHub repos for BoomBigNose content ideas or the daily GitHub giveaway — pulls the live daily/weekly/monthly/yearly ranking from Trendshift.io, verifies stars with the GitHub API, filters by language/stars/AI, and scores content fit. Not for posting anything.
---

# trendshift-github-trends — ดึง repo มาแรงจาก Trendshift.io

เครื่องมือหา repo GitHub ที่กำลังเทรนด์ เพื่อเอาไปคิดคอนเทนต์ BoomBigNose (โพสต์แจก GitHub, Short, คลิปยาว, AI News)
สคริปต์เป็น Python มาตรฐานล้วน ไม่ต้องติดตั้งอะไรเพิ่ม (Python 3.9+)

## ใช้งานเร็ว

```bash
cd skills/trendshift-github-trends
python3 scripts/trendshift_trends.py                          # daily 25 อันดับ (ตาราง Markdown)
python3 scripts/trendshift_trends.py --verify --sort fit       # ตรวจดาวกับ GitHub + เรียงตามความเหมาะกับคอนเทนต์
python3 scripts/trendshift_trends.py --giveaway --exclude-file posted.json   # หา repo แจก GitHub ที่ยังไม่เคยแจก
python3 scripts/trendshift_trends.py --period weekly --ai-only --min-stars 10000 --limit 10 --verify
python3 scripts/trendshift_trends.py --language Python --json -o out.json
```

| ตัวเลือก | ความหมาย |
|---|---|
| `--period daily\|weekly\|monthly\|yearly` | ช่วงเวลาเทรนด์ (ค่าเริ่ม daily) — หน้าละ 25 อันดับ |
| `--limit N` | จำนวนที่แสดง |
| `--language X` | กรองภาษา (Python, TypeScript, Rust…) |
| `--min-stars N` | ดาวขั้นต่ำ (ใช้ดาว GitHub จริงถ้าใส่ `--verify`) |
| `--tag ai-agent` | กรองตาม tag ของ Trendshift (ใส่ซ้ำได้) เช่น ai-coding, ai-memory, llm-inference, browser-automation |
| `--ai-only` | เฉพาะ repo สาย AI (ดูจาก tag + คำในชื่อ/คำอธิบาย) |
| `--verify` | ดึงดาวจริง, เจ้าของเป็นองค์กรไหม, license, archived/fork จาก GitHub API |
| `--giveaway` | เฉพาะที่ผ่านเกณฑ์แจก GitHub ขั้นต้น: AI + ดาว ≥10k + ไม่ใช่ fork/archived (เปิด `--verify` ให้อัตโนมัติ) |
| `--exclude-file F` | ตัด repo ที่เคยใช้แล้ว (ไฟล์ข้อความ/JSON ที่มี `owner/repo`) |
| `--sort rank\|fit\|stars` | เรียงตามอันดับ Trendshift / คะแนนเหมาะกับคอนเทนต์ / ดาว |
| `--json` / `--md` | รูปแบบผลลัพธ์ (ค่าเริ่ม Markdown) · `-o ไฟล์` เพื่อบันทึก |

ฟิลด์ที่ได้ต่อ repo: `rank, full_name, url, trendshift_url, description, language, stars, stars_gained, forks, trend_score, tags, created_at` และถ้า `--verify`: `github_stars, owner_type, license, archived, fork, homepage, github_topics` + `fit` (0–100), `fit_reasons`, `giveaway_ready`

GitHub API แบบไม่ล็อกอินได้ 60 ครั้ง/ชม. (พอสำหรับ 2 รอบเต็ม) ถ้าใช้บ่อยให้ตั้ง `GITHUB_TOKEN` ใน env (ห้าม commit token ลง repo)

## ขั้นตอนหาไอเดียคอนเทนต์

1. รัน `--verify --sort fit` ดูทั้ง daily และ weekly
2. คัดที่เหมาะกับผู้ชม BoomBigNose (คนไทยสาย AI/เทค): ใช้งานได้จริง ฟรี/โอเพนซอร์ส อธิบายง่าย ตัดที่คำอธิบายเป็นจีนล้วนหรือไม่เกี่ยวกับ AI
3. แจก GitHub: ต้องเป็น repo official, ดาว ≥10k, กำลังเทรนด์, มีประโยชน์, ไม่ซ้ำกับ `posted.json` → ใช้ `--giveaway --exclude-file`
4. เขียนหัวข้อคอนเทนต์ภาษาไทย 1 บรรทัดต่อ repo: “ประโยชน์ที่จับต้องได้ + ฟรี/ทำเองได้” ดูตัวอย่างที่ [samples/2026-11-02.md](samples/2026-11-02.md)

## ที่มาของข้อมูล & ข้อตกลงการใช้ (ตรวจเมื่อ 2 พ.ย. 2026)

- อ่านจาก **หน้าเว็บสาธารณะ** `trendshift.io/`, `/weekly`, `/monthly`, `/yearly` — ในหน้ามีข้อมูลอันดับฝังมาเป็น JSON ของ Next.js (`initialData`: rank, score, stars, stars gained, tags) ถ้าอ่านไม่ได้จะใช้ JSON-LD `ItemList` สำรอง (ไม่มีดาว → เติมจาก GitHub API)
- `robots.txt`: `Allow: /` แต่ **ห้าม `/api/`, `/apikeys/`, `/login`, `/signup`** → สคริปต์ไม่แตะ `/api/` เด็ดขาด ไม่มี RSS
- ToS (trendshift.io/tos): ข้อมูล repo มาจาก GitHub สาธารณะ แต่ **อันดับ/คะแนนเทรนด์/การนำเสนอเป็นทรัพย์สินของ Trendshift**; API ทางการ (Trendshift Signal) เป็นแบบเสียเงิน และห้ามเผยแพร่ข้อมูลดิบซ้ำ — insight ที่เราวิเคราะห์เองใช้ได้
- แนวปฏิบัติ: รันวันละไม่กี่ครั้ง (1 คำขอต่อช่วงเวลา) ใช้ User-Agent ระบุตัว, ใช้ข้อมูลเพื่อหาไอเดียภายในทีม **ไม่ก๊อปตารางอันดับทั้งชุดไปโพสต์** ถ้าอ้างอันดับในคอนเทนต์ให้ให้เครดิต Trendshift ถ้าต้องการข้อมูลเยอะ/ถี่ ให้ซื้อ Signal API แทนการ scrape

## ถ้าสคริปต์พัง

- `อ่านข้อมูลจากหน้า Trendshift ไม่ได้` = โครงหน้าเว็บเปลี่ยน → เปิด view-source ของ trendshift.io หา `"initialData":` หรือ `application/ld+json` แล้วแก้ `_parse_initial_data` / `_parse_jsonld`
- ดาว GitHub ว่าง (`github_error: 403`) = rate limit → ตั้ง `GITHUB_TOKEN` แล้วรันใหม่
- กรองภาษาผ่าน URL ไม่ได้ (เว็บกรองฝั่งเบราว์เซอร์) สคริปต์จึงกรองเองหลังดึง 25 อันดับ
