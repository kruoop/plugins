---
name: boombignose-episode-package
description: "สร้างชุดรีวิว YouTube และ Skool ต่อหนึ่ง EP."
---


## Host integration

Resolve sibling skills from this bundle first. For browser control, read the sibling ego-browser skill (or its installed user-wide copy) and use ego-browser CLI with TaskSpace. Map tool names to the tools actually available in Claude Code or Codex; examples do not grant permissions. Resolve runtime paths on the current host rather than treating imported paths as proof of installation. Preserve current user authorization for external writes; installing this bundle starts no generation, upload, post, watcher or episode.

# BoomBigNose Episode Package Skill

สร้างชุดไฟล์ต่อหนึ่ง EP สำหรับช่อง BoomBigNose จากวิดีโอ คำบรรยาย และไฟล์จริงใน Google Drive โดยยึดหลักฐานที่ตรวจสอบได้ ไม่เผยแพร่ อัปโหลด ตั้งเวลา หรือทำให้เนื้อหาเป็นสาธารณะจนกว่าจะได้รับอนุมัติเฉพาะรายการจากผู้ใช้

กติกาและรูปแบบฉบับเต็มอยู่ใน `references/MASTER_PROMPT.md` และถือเป็นข้อกำหนดของงาน หากขัดกับ approval gate หรือคำสั่งระบบ ให้ยึด approval gate และคำสั่งระบบก่อนเสมอ

## YouTube Package — owner-locked default

อ่าน [references/MASTER_PROMPT.md](references/MASTER_PROMPT.md) ก่อนผลิต EP และใช้เทมเพลต/ตัวตรวจของ `bbn-youtube-description` เป็นรูปแบบ Package ปัจจุบัน ยึดรูปแบบ EP242 (`../bbn-youtube-description/assets/reference-EP242_Package.txt`) เป็น default ทุกงาน ห้ามเปลี่ยนรูปแบบเองหรือย้อนกลับ EP214/EP224 เว้นแต่เจ้าของช่องสั่งเปลี่ยนโดยตรง

- บรรทัดแรกตรงตัว: 🌟 เรียนรู้และติดตาม Skill บน Kruoop 👉 https://kruoop.com/about?c=boombignose
- ลำดับ Description: Kruoop → สรุป 3 บรรทัด 💡 / ✨ / 🌐 → 💎 ลิงก์สำคัญ → 👨‍💼 ติดต่องาน / Workshop องค์กร → ⏰ Timeline; disclaimer ที่จำเป็นอยู่ระหว่างสรุปกับลิงก์สำคัญ
- Contact ตรงตัวคนละบรรทัด: 👨‍💼 ติดต่องาน / Workshop องค์กร; ✉️ contact@boombignose.org; 📱 https://lin.ee/SJ1m7ix
- URL ทุกส่วนเป็น https:// ธรรมดา ไม่เติม @url: ไม่ครอบ backtick ไม่ใช้ Markdown link labels; ลิงก์สำคัญใช้ `- ชื่อ — URL` แม้ตัวอย่างในแชทมี wrapper ให้ดึงเฉพาะ URL จริง
- ไม่เติมโปรโมต Hostinger, สมัคร Workshop, Skool หรือลิงก์ Kruoop TH เก่าอัตโนมัติ การใส่โปรโมตเพิ่มต้องมีคำสั่งเจ้าของช่องเฉพาะงาน
- เปลี่ยนเฉพาะเนื้อหา/ชื่อ/Keyword/ลิงก์เครื่องมือที่ตรวจจริง/Timeline/Tags ตาม EP ไม่ยกเนื้อหา REA หรือ Grok Bot ไปใช้กับ EP อื่น ไม่แก้ EP เก่าย้อนหลัง และไม่เปลี่ยน Approval Gate

## Package file scope — explicit owner format

When the owner asks for `EPxxx_Package.txt`, load `bbn-youtube-description` and use its linked fixed Package template: Title (main + 2 alternatives), long caption (main + 2), short caption (main + 2), IG short caption (main + 2), YouTube Description with Timeline, then Tags. Preserve the template's exact headings, labels and blank lines; do not add horizontal rules or substitute the older EP214/EP224 layout. Do not mix render logs, QA, hashes, source investigation, hook, guide, Skool lessons or internal status into this file. Keep technical evidence internally and report counts/limitations in the delivery message. Revise the existing local and authorized working-Drive file, preserving its Drive ID and verifying content hashes. This explicit package request is distinct from automatic broader EP deliverables; do not infer that it requests a course or thumbnail.

## Delivery convention — สร้าง → ลง Drive → แจ้ง

เมื่อเจ้าของช่องสั่งสร้างหรือแก้ deliverable ให้บันทึกไฟล์ที่เสร็จลงโฟลเดอร์ EP เดิมใน BBN-Video ตามขอบเขตงาน แล้วอ่านกลับยืนยันก่อนแจ้ง Telegram พร้อมลิงก์ Drive โดยไม่รอให้สั่งอัปโหลด Drive ซ้ำ การรอตรวจหมายถึงก่อนลงแพลตฟอร์มหรือเผยแพร่ ไม่ใช่ก่อนส่งไฟล์เข้า working Drive; คงสิทธิ์แชร์เดิมและไม่แตะ source root

## Current Skool format — plain text .txt

งาน Skool ที่สร้างหลังคำสั่งนี้ให้ส่ง `EPxxx_skool.txt` แบบ UTF-8 เป็นไฟล์หลักเพียงไฟล์เดียว แทน `.md`; งานไม่มีเลข EP ใช้ `<ชื่อ>_skool.txt` ไม่สร้าง .md คู่กัน ไม่เพียงเปลี่ยนนามสกุลแต่ต้องเขียน plain text จริง: หัวข้อใช้ชื่อกับ emoji และบรรทัดว่าง รายการใช้ • หรือลำดับเลข ไม่ใช้ Markdown heading #, ตัวหนา **, เส้นคั่น ---, code fences หรือ backtick ตกแต่ง ลิงก์ใช้ชื่อ — URL ธรรมดา ไม่ใช้ @url: หรือ Markdown link syntax คงเนื้อหา 4 แท็บ คู่มือ Prompt และหมายเหตุเจ้าของช่องแยกท้ายไฟล์ตามกฎเดิม Prompt/Code ที่ต้องคัดลอกให้แยกด้วยชื่อหัวข้อและบรรทัดว่าง แต่รักษาอักขระที่มีความหมายจริงใน Code/Prompt/URL ห้าม strip # หรือ * แบบเหมารวมจนโค้ดเสีย หากนำเข้า Skool ให้จัด Rich Text ผ่าน editor ไม่วาง Markdown ดิบ ไฟล์เก่าไม่แปลง/ลบโดยไม่มีคำสั่ง รูปแบบล่าสุดนี้ชนะข้อกำหนด .md และเครื่องหมาย Markdown ในขั้นตอนเก่าด้านล่าง

## Current deliverable scope — หยุด Title/Description และ Guide แยกไฟล์

เจ้าของช่องสั่งหยุดสร้าง `EPxxx_title_description.md` และ `EPxxx_guide.md` ในแพ็กเกจ EP ตั้งแต่นี้ จนกว่าจะสั่งกลับมาทำโดยตรง ข้ามการผลิต Title/Caption/Keyword/YouTube Description/Timeline/Tags อัตโนมัติ ไม่ย้ายชุดงานนี้ไปสร้างในไฟล์อื่นแทน และไม่สร้างหรืออัปเดตสองไฟล์ดังกล่าวอัตโนมัติ เก็บไฟล์เดิมไว้ไม่ลบ คู่มือ ขั้นตอน และ Prompt ที่จำเป็นต่อการเรียนให้เขียนตรงใน `EPxxx_skool.md` (🍀 ขั้นตอน/การทดสอบ/ข้อควรระวัง; 💎 Prompt/Code เต็ม) โดยไม่ต้องมี guide เป็น prerequisite ยังคงตรวจความปลอดภัยและรายงานในหมายเหตุเจ้าของช่องนอกบทเรียน Skool คำบรรยาย SRT ยังคงทำตามเงื่อนไขเดิม; งานปกยังพักตามหัวข้อถัดไป ขอบเขตล่าสุดนี้ชนะรายการ deliverable และขั้นตอนผลิตเดิมด้านล่าง ไม่เปิด Watcher หรือเผยแพร่เองจากการเปลี่ยนขอบเขตนี้

## ปก — กฎเจ้าของช่อง 2026-10-22 (แทนข้อพักปก / ปกปัง Studio / Phaya / Canva ทั้งหมด)

ปกทุกงานใช้สกิล `bbn-youtube-thumbnail` + Codex CLI `codex exec` (native image generation) เท่านั้น ใช้ approved face `../bbn-ai-edit/assets/shared/face/face.png` (ห้ามเฟรมวิดีโอ ห้าม `face/image.webp` ที่ถูกปฏิเสธ) โลโก้/มาสคอตของจริง ห้าม HTML-only layout ทีมปกคือบอท **น้องปก** ไฟล์ปก: `Thumbnail/<EP>_Cover.png`, `thumbnail-2.png`, `thumbnail-3.png` แก้แล้วอัปทับชื่อเดิม

## กฎเจ้าของช่อง 2026-10-22 (EP239) — ชนะข้อความเก่าในไฟล์นี้

ดู [owner-rules-2026-10-22.md](../bbn-ai-edit/references/owner-rules-2026-10-22.md):
1. แก้งานแล้วอัปทับไฟล์เดิมบนไดรฟ์ ชื่อเดิม ID เดิม (`../bbn-ai-edit/scripts/drive_replace.sh`, rclone `copyto`, ตรวจ md5) ห้ามมี `_v3`/ไฟล์ซ้ำ
2. Package ตรงรูปแบบ EP242 (`../bbn-youtube-description/assets/reference-EP242_Package.txt`) Timeline ≤ 10 ไม่ใส่เครดิตเพลง
3. ปกตามหัวข้อด้านบน
4. เดโมที่พูดถึงบนจอ = อัดหน้าจอจริง ตรงจังหวะเสียง เบลอข้อมูลส่วนตัว
5. Resource ที่คลิปพูดถึง → `resource.zip` ที่ใช้ได้จริง โพสต์ชุมชน Kruoop BoomBigNose หมวด 📚 แหล่งความรู้ แนบไฟล์ในโพสต์ ห้ามลิงก์ไดรฟ์ ห้ามเลข EP แล้วใส่ลิงก์โพสต์ใน Description (สกิล `kruoop-post`)
6. ทำเองจนจบไม่ถามกลับ สิทธิ์เครื่องขอครั้งเดียว always allow **ไม่โพสต์ YouTube อัตโนมัติ** (Approval Gate ด้านล่างยังใช้กับ YouTube/โซเชียล; โพสต์ resource ใน Kruoop ตามข้อ 5 ได้รับอนุญาตถาวรแล้ว)
7. path ใช้ `~/` หรือ relative เท่านั้น

## When to Use

- ผู้ใช้ขอทำแพ็กเกจ YouTube, ปก, คู่มือ หรือ Skool สำหรับ EP ของ BoomBigNose
- ผู้ใช้ระบุเลข EP หรือโฟลเดอร์ Google Drive ที่มีวิดีโอต้นฉบับ
- งานรันตามกำหนดเพื่อเตรียม candidate ให้ผู้ใช้ตรวจและอนุมัติ

อย่าใช้สำหรับการเผยแพร่ทั่วไปที่ไม่ใช่ BoomBigNose หรือเมื่อผู้ใช้ต้องการเพียงสรุปวิดีโอแบบสั้น

## Prerequisites

1. ต้องมีเลข EP และตำแหน่งโฟลเดอร์ต้นทาง หากหาได้จากโฟลเดอร์ปัจจุบันหรือ Google Drive ให้ค้นเองก่อนถาม
2. แยก Drive อย่างเคร่งครัด:
   - `BoomBigNose Video` root `1ZpXuUP54cPM78xskh8ICyJRYU1bmLzQA` เป็น source แบบ **read-only** ห้ามสร้าง อัปโหลด ย้าย เปลี่ยนชื่อ ลบ หรือสร้าง `_backup` ทุกกรณี
   - `BBN-Video` root `13PTVmiD5YJPVgytx5WLYpJs3M-EvpcwZ` เป็น working/output Drive; ไฟล์ `.md` และ thumbnail ทั้งหมดต้องอยู่ในโฟลเดอร์ EP เดิมบน Drive นี้ เช่น `EP 197/` ห้ามสร้างโฟลเดอร์คู่ขนานหรือ `_backup` เอง
   - ไฟล์ใหม่หรือไฟล์ที่ถูกแก้ใน `BBN-Video` คือ Trigger ของ Watcher และต้องส่งแจ้งเตือนทันที แม้ EP นั้นจะมี Deliverables อยู่แล้ว; ห้ามตอบ `[SILENT]` ในรอบที่ตรวจพบการเปลี่ยนแปลงใหม่
   - ก่อนสร้างหรือแก้เนื้อหา EP ใด ต้องจับคู่เลข EP แล้วอ่านเอกสารที่มีทั้งหมดจาก `BoomBigNose Video > EPxxx` แบบ read-only ร่วมกับคลิปตัดใน `BBN-Video > EP xxx`; อย่าใช้ metadata หรือไฟล์ `.md` ฝั่ง BBN แทนการตรวจคลิปจริง หากค้น source Doc/ไฟล์แจกแล้วไม่พบ ให้ปฏิบัติตาม MASTER STEP 0 และ STEP 5 กติกาไฟล์แจก: แจ้งไฟล์ที่ขาด ใช้คลิปเต็มกับ caption/local ASR และเฟรมเป็นหลักฐาน แล้วเขียนเทมเพลตใหม่จาก workflow โดยติดป้ายชัดว่าไม่ใช่ Prompt/Skill ต้นฉบับ ห้ามแต่งลิงก์หรืออ้างว่าอ่านไฟล์ที่ไม่มี การขาด Doc ไม่ใช่เหตุหยุดแพ็กเกจเนื้อหาทั้งชุด
   - Review Package ที่เกิดจาก Trigger ต้องเตรียมเนื้อหาสำหรับทั้ง `YouTube Studio Draft` และ `Skool Draft` ให้ตรวจ แต่ห้ามเขียนลงแพลตฟอร์มจนกว่าจะมีคำอนุมัติแยกต่อ EP/เวอร์ชัน/แพลตฟอร์ม
3. ใช้ Chrome session ที่ลงชื่อเข้า Google Drive ไว้แล้วบนเครื่องนี้เป็นค่าเริ่มต้น ห้ามตั้ง Google Cloud OAuth/MCP ใหม่ถ้าไม่จำเป็น
4. **แหล่ง Caption/Title ของ Short ต้องแยกตามแพลตฟอร์ม:** จับคู่เลข EP กับ `EPxxx_title_description.md` ในโฟลเดอร์เดียวกันก่อนทุกครั้ง แล้วอ่านหัวข้อจริงก่อนสร้าง payload ห้ามใช้ Caption ของแพลตฟอร์มหนึ่งแทนอีกแพลตฟอร์ม
   - Facebook Short ใช้เฉพาะ `### 📣 แคปชันโพสต์ short video`
   - Instagram Reel ใช้เฉพาะตัวหลักใต้ `### 📣 แคปชันโพสต์ short video IG`
   - TikTok ใช้หัวข้อที่เจ้าของช่องกำหนดสำหรับ TikTok; ถ้ายังไม่มีหัวข้อเฉพาะ ห้ามเดาหรือคัดลอกจาก Facebook/IG ให้ถามครั้งเดียวก่อนโพสต์
   - ห้ามดึงข้าม EP ห้ามใช้ Title จากเอกสารต้นฉบับฝั่ง `BoomBigNose Video` แทน และห้ามแต่ง Caption ใหม่เอง ถ้าหัวข้อที่ต้องใช้หายหรือว่างให้หยุดและรายงาน blocker
   - **ManyChat DM link button:** เมื่อเปลี่ยนลิงก์ DM ของ EP ใหม่ ต้องเปลี่ยน Button label ด้วยทุกครั้ง รูปแบบ `📍<ชื่อ AI ที่ใช้สอนใน EP>` เช่น `📍n8n + Hermes`, `📍ChatGPT Work`, `📍Claude` — อิโมจิปักหมุดเสมอ ลิมิต label 20 ตัวอักษร
   - **ManyChat Facebook ต้องผูกกับโพสต์ปกใหม่ของ EP นั้น:** เจ้าของช่องจะโพสต์ภาพปกใหม่ (แคปชันแนว `ฟรี! พิมพ์ "KEYWORD" ...`) ใกล้เวลาเผยแพร่ EP ห้ามผูก trigger กับโพสต์ปกเก่าของ EP ก่อนหน้า (อายุหลายชั่วโมง/ข้ามวัน) เด็ดขาด ตรวจ caption+อายุโพสต์ใน picker ก่อนเลือกทุกครั้ง ถ้าโพสต์ปกใหม่ยังไม่ขึ้นให้รอ/รายงาน ห้ามผูกโพสต์เก่าแทน
5. **Facebook Short:** ลงเฉพาะ Caption จากหัวข้อดังกล่าว ห้ามใส่ First Comment เอง เจ้าของช่องจะให้คนมาแสดงความคิดเห็นเพื่อเข้า ManyChat และระบบทำหน้าที่ตอบกลับเท่านั้น
6. **Postiz read-back:** หลัง Postiz รับงาน ให้ตรวจ record เดิมด้วย Postiz API หนึ่งรอบจนได้ terminal state และเก็บ `postId/releaseId/releaseURL`; ถ้า URL รายคลิปยังไม่มี ให้รายงาน `published_unverified_url` ตรง ๆ ห้ามยิงซ้ำ ห้ามสร้างโพสต์ใหม่ และห้ามวนเช็กหลาย browser profile หรือหลาย scraper โดยไม่มีหลักฐานว่าจะให้ข้อมูลเพิ่ม
6. ตรวจโฟลเดอร์หาไฟล์วิดีโอยาว วิดีโอชื่อมี `TK` สำหรับแนวตั้ง, `captions.sbv` หรือ `.srt`, โลโก้, รูปโฮสต์ และไฟล์แจกจริง โดยใช้คลิปตัดแล้วชื่อ `งานบีท EPxxx` จาก BBN-Video เป็นตัวอ่านเนื้อหา
5. ตรวจโฟลเดอร์หาไฟล์วิดีโอยาว วิดีโอชื่อมี `TK` สำหรับแนวตั้ง, `captions.sbv` หรือ `.srt`, โลโก้, รูปโฮสต์ และไฟล์แจกจริง โดยใช้คลิปตัดแล้วชื่อ `งานบีท EPxxx` จาก BBN-Video เป็นตัวอ่านเนื้อหา
6. ปกต้องมี Codex CLI ที่ล็อกอินแล้วและรองรับ native image generation (ดู `bbn-youtube-thumbnail`)
7. งานนี้ผูกกับ macOS เพราะ fallback วิเคราะห์วิดีโอใช้ `swiftc`, AVFoundation, Vision, `afinfo` และ `sips`

## Remote browser fallback

OAuth ให้เจ้าของช่องเลือกบัญชีและอนุมัติบนเครื่องที่กำลังใช้งานอยู่เป็นค่าเริ่มต้น ไม่ใช่ส่งไปกดหน้า Mac mini ตรวจ flow ที่บริการรองรับก่อน: ใช้ device authorization หรือ remote-compatible redirect ที่รองรับจริง; localhost callback ต้องกลับถึง process ที่เริ่ม OAuth จึงห้ามส่งลิงก์ไปอีกเครื่องแล้วอ้างว่าใช้ได้ทันที ไม่ขอ token, OTP หรือ callback ที่มี code ผ่านแชต และไม่คัดลอก browser session ข้ามเครื่อง OAuth ของ API/MCP ไม่เท่ากับการล็อกอิน YouTube Studio หรือสิทธิ์ Chrome remote debugging ต้องตรวจแต่ละส่วนแยกกัน ถ้า flow ไม่รองรับข้ามเครื่องให้แจ้งข้อจำกัดก่อนเริ่ม ไม่สัญญาว่าทำได้ทุกบริการ

เจ้าของช่องสั่งงานจากระยะไกลและไม่สามารถไปกดอนุญาตที่ Mac mini ได้ หาก Chrome ที่เลือกติด consent ให้หยุดเส้นทางนั้นและตรวจเบราว์เซอร์/โปรไฟล์/เครื่องอื่นที่ได้รับอนุญาตไว้แล้วก่อนรายงาน blocker ไม่วนขอให้เจ้าของช่องไปหน้าเครื่องเป็นวิธีหลัก การเปลี่ยน browser ไม่ใช่การข้าม consent: ห้ามกดอนุญาตแทน ปิดระบบป้องกัน คัดลอก cookies/credentials หรือใช้เส้นทางใหม่เพื่อเลี่ยงสิทธิ์ที่ถูกปฏิเสธ ต้องตรวจว่าเส้นทางสำรองได้รับสิทธิ์และล็อกอินช่อง BoomBigNose จริงก่อนใช้ หากทุกทางยังต้อง Login/2FA/OS approval ให้รายงานข้อจำกัดตรง ๆ และเสนอขั้นตอนที่ผู้ใช้ทำจากระยะไกลได้เท่านั้น เมื่อเชื่อมต่อที่อนุญาตแล้วให้รักษา connection เดียวตลอดงานเพื่อลด consent ซ้ำ ไม่เปิด process ใหม่ทุก action

## Approval Gate

- เก็บขั้นตอนการออกแบบทั้งหมดใน skill นี้ไว้ครบ และต้องสร้าง Title, Description/แคปชัน, ปก และ deliverables ตามสเปกให้เสร็จก่อน
- รอบแรกมีสถานะ `content_review` และต้องส่งสิ่งที่สร้างจริงให้ผู้ใช้ตรวจทาง Telegram ก่อน ห้ามนำข้อมูลไปใส่ YouTube ในรอบนี้
- แก้ไขตาม feedback และส่งเวอร์ชันใหม่กลับทาง Telegram วนซ้ำจนผู้ใช้อนุมัติเวอร์ชันนั้นอย่างชัดเจน การชมงาน การถามต่อ หรือคำว่า “โอเค” ที่ไม่ผูกกับ EP/เวอร์ชัน ห้ามตีความเป็นอนุมัติ
- คำอนุมัติลักษณะ `อนุมัติให้ทำดราฟ EPxxx เวอร์ชัน x` อนุญาตเฉพาะการนำ Title, Description/แคปชัน, Tags, Caption และปกของเวอร์ชันที่อนุมัติไปใส่ในขั้นตอนอัปโหลดของ YouTube Studio พร้อมเลือก **Playlist ที่ตรงกับเนื้อหา EP** (ถ้ามีรายการที่เข้ากันชัดเจน; ถ้ากำกวมให้ถามเจ้าของช่องก่อน) จากนั้นตั้งค่า **Monetization = On** และตอบแบบประเมินความเหมาะสมต่อโฆษณา (Ad suitability / Self-certification) ตามเนื้อหาวิดีโอจริงเท่านั้น ห้ามเดาคำตอบหรือปกปิดเนื้อหาอ่อนไหว; ถ้าจัดหมวดไม่ได้อย่างมั่นใจให้หยุดถามเจ้าของช่องก่อนบันทึก จากนั้นปิด/ออกจากขั้นตอนเพื่อให้ YouTube เก็บเป็น `Draft` เอง
- ตอนทำ YouTube Draft ให้ตั้ง `AI use = No` ตามกฎของช่องสำหรับคลิปสอนหน้าจอทั่วไป ห้ามเลือก `Yes` เพียงเพราะเนื้อหาพูดถึงหรือใช้เครื่องมือ AI; หากภาพหรือเสียงเข้าข่ายเกณฑ์ disclosure ที่ YouTube แสดงจริง เช่น ทำให้บุคคลจริงพูด/ทำสิ่งที่ไม่ได้ทำ, ดัดแปลงเหตุการณ์จริง หรือสร้างฉากสมจริงที่ไม่เคยเกิด ให้หยุดแจ้งเจ้าของช่องก่อน ห้ามเดา
- **Thumbnail A/B testing:** เจ้าของช่องเป็นผู้ใส่ไฟล์ภาพปก 2 ไว้ในโฟลเดอร์ EP เอง เมื่อสั่งทำ YouTube Draft และพบปกที่ตรง EP จำนวน 2 ไฟล์ ให้ใช้ฟีเจอร์ `Test & compare` ของ YouTube Studio และเลือกใช้ทั้งสองปกเป็น A/B test; ห้ามสร้างปกที่สามในขั้น YouTube Draft นี้ (ไม่เกี่ยวกับการทำปก 3 ใบตอนผลิตงาน) ห้ามเลือกแทนเหลือใบเดียว และต้องตรวจชื่อไฟล์/EP/ภาพจริงก่อนอัปโหลด หากหาไม่ครบ 2 ไฟล์หรือจับคู่ไม่ได้ให้รายงาน blockerแทนการเดา
- เพิ่ม End screen ทุกคลิปเสมอเป็น `Subscribe: BoomBigNose` 1 รายการ + `Video: Best for viewer` 1 รายการ วางในช่วงท้ายที่ Studio อนุญาต แล้วอ่านกลับให้เห็นทั้งสอง element ก่อนจบงาน
- หลังทำ YouTube Draft เสร็จ ต้องเปิดหน้า Content อ่านกลับให้เห็นรายการนั้นเป็น `Draft` ตรวจว่า metadata/ปก/Caption/Playlist/End screen ที่อนุมัติถูกต้อง, `AI use = No` และค่าการสร้างรายได้ถูกตั้งตามที่ทำได้จริง แล้วแจ้งเจ้าของช่องทันทีพร้อมผลตรวจ; ห้ามรอรอบ Watcher ถัดไป
- **ห้ามเลือก Private, Unlisted, Public หรือ Schedule ตอนทำ Draft** และห้ามใช้ YouTube Data API อัปโหลด เพราะ API บังคับสร้าง video record พร้อม visibility ซึ่งอาจเริ่มนับเวลาบนแพลตฟอร์ม
- หลังปิดขั้นตอนอัปโหลด ต้องเปิดรายการ Content ใน YouTube Studio และอ่านกลับให้เห็นสถานะ `Draft` ของรายการที่ผูกกับ EP นั้นก่อนรายงาน `youtube_draft_verified`; ถ้าแสดง visibility ใด ๆ หรือยืนยัน Draft ไม่ได้ ให้หยุดและรายงาน blocker
- การทำ Preliminary Draft เพื่อรอ Caption ต้องได้รับคำอนุมัติเฉพาะ EP เช่นกัน ใช้วิธี YouTube Studio แบบไม่เลือก visibility แล้วตรวจกลับว่าเป็น `Draft`; การอนุมัตินี้ไม่ครอบคลุม metadata/ปกฉบับจริง
- หลัง YouTube สร้างคำบรรยายแล้ว ให้ดาวน์โหลด `.sbv` เก็บเป็น `caption.sbv` ในโฟลเดอร์ EP แล้วสร้าง `captions.srt` และ `captions_fixed.srt`; ย้อนกลับไปแก้ Timeline และคู่มือให้ตรงวินาที
- ถ้าแก้แพ็กเกจหลังอนุมัติ ต้องกลับไปสถานะ `content_review` ส่ง Telegram ให้ตรวจ และขออนุมัติทำดราฟใหม่สำหรับเวอร์ชันแก้ไข
- `scripts/youtube_private_upload.py` ใช้ได้เฉพาะ `--dry-run` เพื่อตรวจแพ็กเกจเท่านั้น การอัปโหลดจริงผ่าน API ถูกปิดตามนโยบายช่อง
- สำหรับ Skool หลังได้รับคำสั่งเฉพาะ `อนุมัติทำดราฟ Skool EPxxx เวอร์ชัน x` ให้สร้าง Course เป็น Draft/ซ่อนจากสมาชิกก่อนเสมอ ส่วนเนื้อหา 4 หน้า/Modules ภายในตั้งเป็น Public/Active ได้ เพราะ Course แม่ยังเป็น Draft; หลังเขียนทุกครั้งต้องอ่านกลับและยืนยันว่า Course แม่ยังเป็น Draft หากสถานะเปลี่ยนหรือยืนยันไม่ได้ให้หยุดทันที ห้ามเผยแพร่ Course เอง
- เวลาสร้าง Skool Course ใหม่ ให้ไปหน้าสุดท้ายของ Classroom แล้วใช้การ์ด `New course` เป็นค่าเริ่มต้น ห้าม Duplicate คอร์สเดิมเพื่อประหยัดการลาก เพราะเนื้อหา/ปก/การตั้งค่าเดิมอาจตกค้างและตรวจไม่หมด ใช้ Duplicate เฉพาะเมื่อผู้ใช้สั่งให้ทำสำเนาคอร์สนั้นโดยตรง
- **YouTube Automation จบที่ Studio Draft ที่ยังไม่เลือก visibility เท่านั้นตลอด Workflow**: หลังใส่ Title, Description, Tags, Caption และปกที่อนุมัติแล้วให้ปิดขั้นตอนอัปโหลด ตรวจรายการ Content ว่าเป็น `Draft` แล้วหยุด ห้ามเลือก Private, Unlisted, Public หรือ Schedule เจ้าของช่องเป็นผู้กลับไปตั้งค่าต่อเองภายหลัง
- การเผยแพร่ Skool Course ต้องได้รับคำสั่งแยกที่ชัดเจนสำหรับหนึ่งรายการเท่านั้น และต้องอ่านกลับจากแพลตฟอร์มก่อนตั้งสถานะ `published_verified`
- **Instagram pre-publish review:** ก่อนลง IG Reel ทุกครั้ง ต้องส่งวิดีโอ/เลข EP พร้อม Caption IG ตัวเต็มให้วาตรวจใน Telegram และรอคำอนุมัติที่ระบุ IG ของรายการนั้น เช่น `ลง IG EPxxx` ก่อน Publish เสมอ แม้ Facebook/TikTok ของ EP เดียวกันได้รับอนุมัติแล้วก็ห้ามถือว่าอนุมัติ IG ไปด้วย การอนุมัติครั้งหนึ่งใช้ได้เฉพาะ Caption/วิดีโอเวอร์ชันที่ส่งตรวจเท่านั้น; ถ้าแก้ Caption ต้องส่งตรวจและขออนุมัติใหม่
- งาน cron ที่ไม่มี candidate คุณภาพพอให้ตอบ `[SILENT]`

## Procedure

### 0. ทำ preliminary Studio Draft เพื่อดึง caption (เมื่อยังไม่มี caption)

1. ถ้าโฟลเดอร์ EP มี `caption.sbv`, `captions.sbv` หรือ `.srt` ที่ตรงกับวิดีโอเวอร์ชันล่าสุดอยู่แล้ว ให้ข้ามขั้นนี้
2. ถ้ายังไม่มี ให้ขออนุมัติเฉพาะ EP ว่า `อนุมัติให้ทำ Draft EPxxx เพื่อดึง caption` แล้วเปิดขั้นตอนอัปโหลดใน YouTube Studio พร้อม metadata ชั่วคราว `TEMP — EPxxx รอตรวจเนื้อหา`
3. ใส่วิดีโอแล้วปิด/ออกจากขั้นตอนอัปโหลดโดยไม่เลือก Private, Unlisted, Public หรือ Schedule จากนั้นอ่านรายการ Content กลับให้เห็น `Draft`
4. รอให้ YouTube ประมวลผล auto-caption โดยไม่เดาเวลาที่เสร็จ และห้ามกำหนด visibility
5. เมื่อพร้อม ให้ดาวน์โหลดเป็น `.sbv` เก็บชื่อ `caption.sbv` ในโฟลเดอร์ EP จากนั้นทำขั้นตอนแปลง `.srt` และใช้ timestamp จากไฟล์นี้กับ Description และคู่มือ
6. ขั้นนี้อนุมัติเฉพาะ Studio Draft เพื่อสร้าง caption ไม่รวมการอนุมัติ metadata/ปกฉบับจริงหรือการเผยแพร่

### 1. สำรวจและเลือก source of truth

1. อ่านรายชื่อไฟล์ทั้งหมดในโฟลเดอร์ EP และ Google Drive ด้วยเครื่องมือที่เข้าถึงแหล่งจริง
2. เลือกวิดีโอเวอร์ชันล่าสุดที่ไม่มีลายน้ำ ตรวจความยาวเทียบเวอร์ชันเก่า และแยกไฟล์ `TK`
3. ถ้ามี `captions.sbv` หรือ `.srt` ให้ใช้เป็นแหล่งเวลาและคำพูดหลัก
4. ถ้าไม่มี caption ให้ใช้ `terminal` คอมไพล์ Swift CLI ด้วย `swiftc -parse-as-library`, อ่าน duration ด้วย `afinfo`, ดึงเฟรมทุก 30 วินาทีด้วย `AVAssetImageGenerator` แล้วดึงถี่ขึ้นเฉพาะรอบรอยต่อบทหรือจุดที่ OCR/ภาพยังไม่ชัด ระบุ timestamp ว่าแม่นประมาณ ±10 วินาที
5. ห้ามสแกนทั้งคลิปทุก 10 วินาทีเป็นรอบที่สอง เพราะทำให้ Telegram ค้างนานและสร้างไฟล์เกินจำเป็น ให้ดึงช่วง 10 วินาทีแบบเจาะจงไม่เกิน 12 ช่วงก่อน หากยังไม่พอค่อยเพิ่มเฉพาะช่วงที่มีเหตุผลชัดเจน
6. เมื่อ caption ขัดกับภาพ ให้ดึงเฟรมช่วงนั้นและยึดภาพหน้าจอเป็นหลัก

### Telegram latency mode

- เมื่อรับงาน EP เต็มชุดจาก Telegram ให้ตอบรับภายใน 30 วินาทีว่ารับงานแล้วและกำลังประมวลผล จากนั้นย้ายงานยาวไป `delegate_task` หรือ `terminal(background=true, notify_on_complete=true)` เพื่อไม่ให้ DM ถูกบล็อก
- หลีกเลี่ยง `computer_use` สำหรับการดาวน์โหลดหรืออ่าน Drive เมื่อมีลิงก์ตรง, MCP, ไฟล์ซิงก์ หรือไฟล์ในโฟลเดอร์ EP อยู่แล้ว หาก `computer_use` ไม่มีผลลัพธ์ภายใน 60 วินาทีให้หยุดและเปลี่ยนวิธี ห้ามปล่อยรอเกิน 5 นาที
- พรีวิวข้างแชตใช้สำหรับ login/OAuth และตรวจหน้า Drive บนเครื่องผู้ใช้ แต่ปุ่ม Download ในพรีวิวอาจดาวน์โหลดลงเครื่องผู้ใช้ ไม่ใช่ Mac mini ที่ประมวลผล ห้ามถือว่าดาวน์โหลดสำเร็จจนกว่าจะพบไฟล์จริงใน workspace
- ถ้า Drive MCP ไม่มี OAuth แต่โฟลเดอร์ถูกแชร์แบบเปิดอ่านได้ ให้ fetch URL โฟลเดอร์จาก Mac mini, parse ชื่อไฟล์กับ Drive file ID จาก HTML แล้วดาวน์โหลดด้วย `https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t`; ตรวจขนาดและ duration หลังดาวน์โหลด หากโฟลเดอร์ไม่เปิดสาธารณะให้ขอผู้ใช้อนุญาต/ซิงก์ ห้ามพยายามข้ามสิทธิ์
- อย่าลองติดตั้ง/เรียกหลาย fallback ต่อเนื่อง (`gdown`, `cv2`, path ของ `ffmpeg`) ระหว่างงานจริงโดยไม่มี prerequisite check ให้เลือกเส้นทางที่มีอยู่จริงก่อน และรายงาน blocker หากเส้นทางหลักใช้ไม่ได้
- งานปกและงานวิเคราะห์วิดีโอทำขนานกันได้เมื่ออินพุตพร้อม อย่ารอทีละสายงานโดยไม่จำเป็น

เสร็จเมื่อรู้ไฟล์ต้นฉบับที่เลือก, duration, สถานะ caption, โครงเรื่อง, ไฟล์แจก และความเสี่ยงที่เห็นบนจอ

### 2. สร้างไฟล์ Title และ Description

เขียน `EP<เลข>_title_description.md` ไฟล์เดียว โดยเรียงหัวข้อ:

1. `### 🎯 Title` — ตัวหลัก 1 และสำรอง 2; นับด้วยโค้ดและทุกชื่อไม่เกิน 100 ตัวอักษร
2. `### 📣 แคปชันโพสต์ long video` — `ฟรี! พิมพ์ "KEYWORD" ผมส่งเนื้อหาทั้งหมดให้ครับ ☺️ : <Title ตัวหลัก>`
3. `### 📣 แคปชันโพสต์ short video` — Title ตัวหลักเท่านั้น
4. `### 📝 Description` — ใช้โครง, ลิงก์, contact และหัวข้อคงที่ตาม reference; timeline 10 ช่วงและมี `Skool - BoomBigNose+` ตรงช่วงโปรโมต
5. `### 🏷️ Tags` — สตริงจุลภาคเดียว; นับด้วยโค้ดไม่เกิน 500 ตัวอักษร; แต่ละแท็กไม่ควรเกิน 30
6. `### 📌 หมายเหตุก่อนอัปโหลด` — เวอร์ชันไฟล์, ลายน้ำ, ข้อมูลส่วนตัว, disclaimer, จุดที่ต้องเบลอ และข้อสังเกตทั้งหมด
7. เพิ่ม source link และ publication time สำหรับข้อเท็จจริงที่อ้างจากภายนอกทุกข้อ
8. ใน YouTube Description หัวข้อ `💎 ลิงก์สำคัญ` ทุกบรรทัดต้องใช้ `- <ชื่อ> — <URL>` โดยเป็น URL ธรรมดา ห้ามใส่ `@url:` และห้ามครอบ URL ด้วย backtick; ถ้าเนื้อหามาจาก Doc ให้ใช้เฉพาะ URL ที่อยู่ในเนื้อหา Doc จริง ห้ามเพิ่มลิงก์ Doc/โฟลเดอร์ Drive และห้ามใส่ Hostinger หรือลิงก์พันธมิตรซ้ำเมื่อมีบรรทัดโปรโมตด้านบนแล้ว
9. หลัง Timeline ห้ามเติมย่อหน้าข้อมูลหรือ Source note เพิ่มเอง เว้นแต่เจ้าของช่องให้ข้อความนั้นมาโดยตรง; Source/เวลาเผยแพร่เก็บในส่วน Review หรือหมายเหตุนอก Description ที่นำไปวางใน Studio
10. ห้ามสร้างไฟล์ HTML/DOCX companion เพื่อทำปุ่ม Copy หรืออ้างว่าปุ่ม Copy ใช้งานได้ เพราะ Hermes file WebView อาจแสดงปุ่มและสถานะ ✓ แต่ไม่เขียน Clipboard จริง. ส่งเฉพาะไฟล์ deliverable มาตรฐานตามสเปกและภาพปก; หากผู้ใช้ต้องการคัดลอก ให้แสดงข้อความในรูปแบบที่ผู้ใช้สั่ง ณ ตอนนั้นโดยไม่เพิ่มไฟล์ชนิดใหม่เอง (กฎนี้ไม่เปลี่ยนข้อห้าม code block ของเนื้อหา Skool)

#### แคปชันโพสต์ short video IG — Keyword สั้นและพิมพ์ง่าย

เพิ่มหัวข้อ `### 📣 แคปชันโพสต์ short video IG` ถัดจากแคปชัน short video และก่อน Description ในไฟล์ `EP<เลข>_title_description.md` เดิม ใช้รูปแบบ `✨ ฟรี! พิมพ์ "KEYWORD" เดี๋ยวผมส่งลิงก์วิดีโอสอน<หัวข้อสั้น ๆ> ให้ทั้งหมดเลยครับ` โดยหัวข้อสั้นจบในบรรทัดเดียว เสนอตัวหลัก 1 และสำรอง 2 ตาม MASTER_PROMPT.md

- Keyword ต้องเป็นคำเดียวสั้น ๆ คุ้นตา จำง่าย พิมพ์ง่ายบนมือถือ และตรงแก่นเนื้อหา ไม่สร้างรหัสจากชื่อหัวข้อทั้งประโยค
- ตัวอย่าง: Hermes ใช้ `hermes` หรือ `VPS` เมื่อเน้นการติดตั้งบน VPS; AI Agent 3D World ใช้ `3D`; n8n ใช้ `n8n`
- ห้ามใช้คำผสมหรือรหัสยาว/สะกดยาก เช่น `claudemv`, `hostonger`, `agentworld` และห้ามสะกดชื่อเครื่องมือผิดเพื่อทำ Keyword
- ถ้าคำสั้นชนกับ Keyword ที่ใช้อยู่ ให้เลือกคำสั้นอื่นที่ตรงเนื้อหา ไม่เติมคำต่อท้ายจนยาว
- ในแพ็กเกจใหม่ ใช้ Keyword สั้นเดียวกันทั้ง IG และ long video ตามกฎเดิม; ไม่เปลี่ยนโพสต์เก่าหรือระบบตอบกลับที่ใช้งานอยู่เองโดยไม่มีคำสั่ง

เสร็จเมื่อผ่านลิมิต Title 100, Description 5,000, Tags 500, Keyword IG สั้นพิมพ์ง่าย และ timeline อิงหลักฐาน

### 3. แปลงและแก้คำบรรยาย

ทำเฉพาะเมื่อมี `captions.sbv`:

1. สร้าง `captions.srt` โดยแปลงเวลาและข้อความตรง ๆ
2. สร้าง `captions_fixed.srt` โดยรวมคำไทยที่ถูกตัดกลางคำ, เว้นไทย–อังกฤษ, และแก้ชื่อแบรนด์/เครื่องมือที่ตรวจยืนยันได้
3. รายงานรายการแก้ไขทุกคำ ห้ามเปลี่ยนใจความหรือเติมคำพูดที่ไม่มีในต้นฉบับ

เสร็จเมื่อทั้งสองไฟล์ parse ได้ ลำดับเวลาไม่ย้อน และเนื้อหาตัวตรงยังคงเดิม

### 4. สร้างคู่มือ

เขียน `EP<เลข>_guide.md` ให้ทำตามได้จริง ประกอบด้วย:

- คลิปทำอะไรและ prerequisites
- ขั้นตอนเรียงตาม timeline
- Prompt/คำสั่งที่เห็นในคลิปแบบตรงตัว; หากภาพกับ caption ขัดกันต้องยึดเฟรม
- เทคนิค ข้อจำกัด ความปลอดภัย และ Prompt ชุดเต็ม
- หากเสริมความรู้นอกคลิป ให้ติดป้ายและสรุปท้ายงานว่าเสริมตรงไหน

เสร็จเมื่อผู้อ่านที่ไม่ใช่สายเทคทำตามได้โดยไม่ต้องเดาค่าหรือขั้นตอนสำคัญ

### 5. เตรียมและตรวจภาพปก

ทำตามสกิล `bbn-youtube-thumbnail` ทั้งหมด (Codex CLI native generation, approved face `../bbn-ai-edit/assets/shared/face/face.png`, โลโก้จริง, 3 ใบ: `Thumbnail/<EP>_Cover.png`, `thumbnail-2.png`, `thumbnail-3.png`) ส่งรีวิวผ่านบอทน้องปก ขั้นตอน Phaya/Canva/plate/`face/image.webp` เดิมถูกยกเลิกแล้ว (สำเนาเดิมอยู่ใน backup `backups/skills-2026-10-22/`)

### 6. สร้างเนื้อหา Skool

คู่มือและ Prompt จริงใน `EP<เลข>_guide.md` ต้องถูกนำมาใช้ในเนื้อหา `EP<เลข>_skool.md` ไม่ใช่ทำเป็นเอกสารแยกแล้วให้สมาชิกไปอ่านเอง: นำเหตุผล ขั้นตอน การตั้งค่า การทดสอบ และข้อควรระวังไปเรียบเรียงในแท็บ 🍀; นำ Prompt/Code จริงแบบเต็มที่ต้องคัดลอกไปไว้แท็บ 💎; ใช้แท็บ 🔥 เฉพาะเนื้อหาต่อยอด ไม่ทำคู่มือเดิมซ้ำ เมื่อแก้ขั้นตอนหรือ Prompt ในคู่มือต้องปรับส่วนที่เกี่ยวข้องใน Skool ให้ตรงกันด้วย โดยคงรูปแบบ Skool และไม่ใส่ timestamp ในบทเรียน ไฟล์ guide เดิมยังคงไว้เป็นต้นฉบับ ไม่ลบหรือเปลี่ยนโครงไฟล์เอง

เขียน `EP<เลข>_skool.md` ไฟล์เดียว:

1. ชื่อคอร์ส 3 ตัวเลือก
2. Course description ไม่เกิน 480 ตัวอักษร ตรวจด้วยโค้ดจนผ่าน
3. สี่แท็บ: `🌟 วิดิโอประกอบการเรียนรู้`, แท็บ `🍀` ที่ตั้งชื่อใหม่ตาม EP, `🔥 ต่อยอด Exclusive`, `💎 Source Code เทมเพลต`
4. ไฟล์ต้องเป็นต้นฉบับพร้อมคัดลอกลง Skool จริง: ห้ามปนสถานะงาน, blocker, character count, เหตุผลการเลือก, รายงานแหล่งข้อมูล, ข้อความ “รออนุมัติ/เติมภายหลัง” หรือหมายเหตุของ Agent ภายในเนื้อหา 4 แท็บ ให้ย้ายทั้งหมดไปท้ายไฟล์ใต้ `หมายเหตุสำหรับเจ้าของช่อง — ไม่นำไปวางใน Skool`
5. รักษาขอบเขต: 🍀 อธิบาย/ติดตั้ง/วิธีใช้, 🔥 ต่อยอดที่ลึกกว่า YouTube, 💎 ลิงก์จริงและ Prompt/เทมเพลตเท่านั้น
6. ตอนนำเนื้อหาเข้า Skool ต้องจัดด้วย Rich Text จริง ไม่ใช่วาง Markdown/ข้อความยาวเป็นก้อน: ใช้ Heading, Bullet, Numbered list, Blockquote และ Code block ให้เห็นลำดับชั้นชัดเจนบนมือถือ
   - แต่ละย่อหน้า 1–3 ประโยค, ลิสต์ไม่เกิน 7 ข้อต่อชุด และหัวข้อซ้อนไม่เกิน 2 ระดับ
   - 🌟 เรียง `คอร์สทำอะไร → ก่อนเริ่ม → ลำดับการเรียน → วิดีโอ`
   - 🍀 เรียง `ทำไม → Workflow → เครื่องมือ → ติดตั้ง → ทดสอบ → ความปลอดภัย/ข้อเสีย`
   - 🔥 ห้ามซ้ำกับ 🍀; ใช้ `ผลลัพธ์ที่จับต้องได้ → ระบบสถานะ/แนวทางต่อยอด → ความเสี่ยง → มุมธุรกิจ`
   - 💎 ต้องเป็นจุดรับของแบบสั้น: `ไฟล์จริง → Code/Prompt ที่ก๊อป → เช็กก่อนรัน → ลิงก์` ห้ามเทคู่มือยาวลงหน้านี้
7. ใช้ตาราง Markdown ได้เมื่อช่วยเปรียบเทียบข้อมูล แต่ต้องกระชับและอ่านบนมือถือได้; ยังห้าม timestamp, คำว่า `Page 1/2/3` และ `PlayBook สรุปเนื้อหา`
8. กล่องโค้ดใช้เฉพาะ Prompt/Code/คำสั่งที่ต้องก๊อปทั้งก้อน ห้ามใช้กับรายการเครื่องมือ ตาราง Markdown ตารางอ้างอิง หรือผังขั้นตอน; ใช้ลิสต์ `- **ชื่อ** — รายละเอียด`, ตาราง Markdown ปกติ หรือลิสต์เลขตามเนื้อหา
9. อ่านไฟล์แจกจาก Google Drive จริง ข้าม `._*`, `~$*`, และ `.mov`; ในรายการลิงก์ให้ใช้เฉพาะ URL ที่ปรากฏอยู่ในเนื้อหา Doc/ไฟล์ต้นฉบับจริง ใช้รูปแบบ `- <ชื่อ> — @url:` แล้วครอบ URL ด้วย backtick ชื่อไม่ต้องมีวงเล็บ ห้ามใส่ลิงก์ Doc หรือโฟลเดอร์ Drive เป็น Resource และห้ามใส่ลิงก์พันธมิตรซ้ำถ้ามีอยู่ด้านบนแล้ว
   - ก่อนเขียนแท็บ 💎 ต้องไล่รายการไฟล์ใน `BoomBigNose Video > EPxxx` แบบ read-only ทุกครั้ง แล้วอ่านเนื้อหาจากไฟล์ text, DOCX, JSON หรือ Workflow จริง ไม่ใช่อ้างเฉพาะ `EPxxx_skool.md`
   - ถ้ามี Workflow/Source Code แนบอยู่ใน Drive ให้ใส่ลิงก์หรือ Resource ของไฟล์จริงใน Skool และดึงรายละเอียดที่ตรวจยืนยันจากข้อความในไฟล์มาเขียนด้วย ห้ามแทนด้วยตัวอย่างที่แต่งขึ้นเอง
8. ถ้าไฟล์หาย ให้แจ้งตรง ๆ และแจก Prompt/เทมเพลตที่สร้างจากขั้นตอนในคลิปแทน
9. ถ้ามี n8n JSON ให้แกะโครงสร้างจริงและทำ workflow diagram ที่อ่านบนมือถือได้

เสร็จเมื่อ description ผ่าน 480 ตัวอักษร, ไม่มี placeholder, ทุกลิงก์มาจากไฟล์จริง และเนื้อหาไม่ซ้ำข้ามแท็บ

### 7. ตรวจความปลอดภัยและส่ง review package

ตรวจชื่อ/ภาพคนจริง, อีเมล, เบอร์, เลขบัญชี, รหัสผ่าน, OTP, เลขบัตร และคำเคลมด้านแพทย์ การเงิน กฎหมาย ระบุเวลาที่ต้องเบลอและ disclaimer ที่ต้องใช้ ห้ามนำบุคคลจริงหรือคำเคลมอ่อนไหวไปใส่ Title/thumbnail

ส่ง review package ทาง Telegram แบบกระชับ โดยแนบสิ่งที่สร้างจริงทุกครั้ง:

- **ทันทีที่สร้างหรือแก้ไฟล์เนื้อหา หรือปก Candidate สำเร็จ ต้องส่ง Review และแนบไฟล์จริงเข้า AutoYT_Bot/Telegram ทันที ห้ามเก็บไว้บนเครื่องหรือ Drive เงียบ ๆ**
- ทำและส่งทีละ EP; ถ้ามีหลาย EP ให้ส่ง EP แรกแล้วหยุดรอ feedback ห้ามทำหรือส่งหลาย EP รวดเดียว
- หลังส่งให้หยุดที่ `awaiting_content_review` ห้ามทำ YouTube Draft หรือ Skool Draft จนกว่าจะได้รับคำสั่งเฉพาะ EP/เวอร์ชันว่า “สร้างดราฟ”
- ถ้า Delivery ล้มเหลว ห้ามถือว่าส่งสำเร็จ ต้อง retry ผ่าน `bot-chat:auto-post-youtube` และรายงาน failure ที่ตรวจได้
- Title options โดยแนะนำตัวที่แข็งแรงที่สุดและเหตุผลหนึ่งบรรทัด
- Description พร้อม timestamp และ source links
- Tags/keywords
- Thumbnail direction และไฟล์ภาพปกจริงที่ผ่านการตรวจแล้ว
- Hook 5–10 วินาที
- Source link พร้อม publication time
- Status: `content_review`
- ระบุเลข EP และเวอร์ชันของแพ็กเกจให้ชัด เพื่อผูก feedback/approval กับงานที่ถูกต้อง
- รายการไฟล์ที่เสร็จ, blocker, สิ่งที่ผู้ใช้ต้องเติม และส่วนที่เสริมนอกคลิป
- รับ feedback แล้วแก้เฉพาะที่สั่ง ส่งแพ็กเกจเวอร์ชันใหม่ทาง Telegram และทำซ้ำจนผู้ใช้พอใจ
- เมื่อผู้ใช้ต้องการให้ลงข้อมูลใน YouTube ให้ขอคำอนุมัติชัดเจนว่า `อนุมัติให้ทำดราฟ EPxxx เวอร์ชัน x` โดยยังไม่เผยแพร่

## Pitfalls

- For Hermes Desktop/VPS lessons, compare the recorded authentication flow with the current official Desktop security guidance before recommending deployment. A filmed username/password sign-in is not approval to expose basic auth publicly; distinguish trusted-network/VPN use from the supported public OAuth route. A visible game window is not proof every bot tested it, and a missing Docker socket is an access limitation, not proof the target service is down. Treat image manifests as image resources, not executable source bundles.

- For Skool course titles, count UTF-16 code units as well as Unicode code points and keep every option within 50 UI units; omit EP numbers when the owner's latest preference requires it. A public demo repository may have changed after recording: compare the current README with final-video UI and explicitly distinguish the downloadable version from the recorded demo. If YouTube oEmbed fails, inspect the exact watch-page playability status; LOGIN_REQUIRED/private is not a verified title and must not be replaced with another episode or a guessed publication date.

- When a linked live demo or repository has evolved after recording, compare it with the actual final-video frames before writing lessons. Keep the filmed behavior separate from the current README/site; do not silently teach a new phone-directory implementation as the original booking demo. Explain version drift in owner notes, and teach Pages source selection from the branch containing reviewed files rather than blindly repeating a slide's main branch. Source Doc URLs remain the member-resource allowlist unless the owner explicitly requests expanded resources.

- Do not label an ffmpeg `fps=1/30` contact sheet as exact 0, 30, 60-second samples without checking selected source timestamps; filter rounding can select midpoint frames. For source/privacy evidence, seek each requested timestamp explicitly, label it from the actual extraction request, and include a final near-end frame. Contact-sheet cell index alone is not timestamp evidence.

- Skool course-cover crop Save starts an asynchronous upload: wait until the crop dialog and PROCESSING state disappear and the course preview updates before saving Edit course. Otherwise the course can save without the new cover. For classroom reordering, use the target card's Move ← menu, wait for the position change and recheck Draft after every write; when crossing pagination, reload the destination page to avoid stale cached ordering. Count unique cards and verify pagination ranges during before/after inventories, then compare unrelated-course relative order. During Move ← animations, wait for the target title to reappear at the expected adjacent index together with its Draft badge; transient missing cards are not a confirmed pagination crossing. When reopening a lesson, wait for both the Title input and Published/Draft editor control, not merely a `.tiptap` node: the read-only renderer also uses that class. Stop at the actual first card, not a locally decremented page counter.

- During authenticated Skool imports, bind browser automation to the exact tab/window rather than the active tab; concurrent user activity can silently redirect actions. If the permitted Chrome Apple Events JavaScript bridge is already enabled, it can drive visible UI controls and paste HTML through the editor clipboard event without accessing cookies or internal APIs. Do not enable it to bypass a refusal. Verify each saved page by reopening its editor and comparing the full text, then cancel without another write. Background tabs may defer the read-only rich-text renderer, so absent rendered content alone is not evidence of data loss. Use real `<pre><code>` blocks only when the live editor supports Code block and read back all prompt text. Capture the exact native window and ensure the intended tab is visible before accepting screenshot evidence.

- For multi-tool demos, verify the named repository's actual role from its primary documentation before turning a spoken instruction into installation guidance. A decision/classification model is not automatically a UI operator, an MCP configuration check is not a successful video render, and a post-list screenshot is not proof that the same automation published the intended item. Label newly authored practice prompts and separate production approval from publication approval.

- For Blender/AI episodes, inspect the actual demo bundle's script, prompt record and action log before writing lessons. Prompt text in a Python Console is not proof of a natural-language add-on; an image opened in Blender is not proof of editable 3D geometry. Separate native renders, previously generated images, and reference-video attempts that only reached a billing quote. Preserve original prompt wording while explaining actual script parameters when they differ. Search scoped `Desktop/BBN AI Edit/EPxxx` checkpoints before retranscribing or broadly scanning Desktop; bind reused review assets to an identical final-video hash.

- When the working-Drive final video differs in hash from saved local edits, review the actual Drive final even if durations match. New labels or inserts may invalidate earlier visual evidence. Reuse local ASR only after proving the relevant media/timing equivalence; otherwise transcribe the actual final locally. If source Docs and original prompts are absent, distinguish overview lessons and newly authored practice templates from installation instructions or verbatim prompts, and keep the missing-video-URL blocker only in owner notes.

- When a compact package targets a re-edited video, map saved original ASR segment intersections through the canonical source/output frame plan; do not copy original timestamps or old insert narration. Audio-only revisions may reuse picture timing only after packet/timing equality is established. Keep chapter rounding and non-word-aligned caption limitations outside the package. Verify a Drive text delivery by reading back exact bytes and comparing SHA-256, plus provider MD5 when available; metadata size alone is insufficient.

- ข้อความต้นฉบับที่ว่า “พร้อมอัปโหลดและแปะ Skool” หมายถึงเตรียมให้พร้อมตรวจ ไม่ใช่อนุญาตเผยแพร่
- อย่าคาดเดา timestamp, Prompt บนหน้าจอ, ชื่อไฟล์ Drive, URL, คำพูด หรือสถิติ
- หากใช้โมเดลถอดเสียงที่ติดตั้งในเครื่องแล้ว ให้ตรวจข้อความช่วงต้นกับภาพก่อนใช้ทั้งชุด; ถ้าพบ numerical warnings ร่วมกับข้อความหลายภาษาผิดบริบท ให้หยุดและไม่สร้าง SRT จากผลนั้น ใช้ fallback อ่านเฟรมพร้อมระบุเวลาประมาณและข้อจำกัด ห้ามแก้ข้อความมั่วให้ดูเหมือน transcript ที่ยืนยันแล้ว
- เมื่อ local faster-whisper มี numerical warnings ให้ตรวจเครื่องมือที่ติดตั้งจริงก่อนเพิ่ม dependency: `whisper-cli` กับ multilingual `~/.cache/hyperframes/whisper/models/ggml-small.bin` เป็นทางเลือกที่ทดสอบได้บน Mac; ใช้ ffmpeg สกัด PCM mono 16 kHz แล้วรัน `whisper-cli -m <model> -f <audio.wav> -l th -d 60000 -oj -of <sample>` เทียบใจความกับภาพก่อนถอดทั้งคลิปโดยตัด `-d` ออก หากช่วงท้ายสำคัญให้ใช้ `-ot <milliseconds> -d <milliseconds>` ตรวจซ้ำแยก อย่าใช้โมเดล `.en` กับเสียงไทยหรือถือว่า ASR ที่ไม่เตือนเท่ากับถอดชื่อ/ตัวเลขถูก ต้องยืนยัน model, prompt, stock และค่าต่าง ๆ จาก UI; ไม่ส่ง audio ไป Apple/external ASR เอง
- แยกความสำเร็จสามระดับเมื่ออ่านคลิป automation: execution สำเร็จ, Tool คืนข้อมูล, และคำตอบถูกตรง source เป็นคนละ assertion; ข้อความ stock ใน Hosted Chat หรือ Succeeded สีเขียวไม่พิสูจน์จำนวนคงเหลือ หากไม่มีแถว/Tool output รอบเดียวกันให้ระบุว่าเป็นคำตอบที่เห็นแต่ยังยืนยันข้อมูลจริงไม่ได้
- ตัวตรวจ Skool ต้องแยกเส้นคั่นเดี่ยว `---` ออกจากแถวคั่นหัวตาราง Markdown `|---|---|`; ตารางที่ MASTER อนุญาตไม่ควรถูกนับเป็นเส้นคั่นต้องห้าม
- ตัวตรวจข้อความหลังบ้านใน Skool ต้องแยก prose ออกจาก Prompt: คำสั่งให้ผู้ช่วย “รออนุมัติก่อนส่ง” ภายใน Prompt เป็น approval gate ที่ต้องเก็บ ไม่ใช่สถานะ content_review ที่หลุดเข้าบทเรียน ห้ามลบข้อป้องกันเพื่อให้ regex ผ่าน
- งาน Exclusive ที่ไม่มีเลข EP และผู้ใช้สั่ง Skool-only ให้ใช้ชื่อโฟลเดอร์จริงและ canonical `<ชื่อ>_skool.md` เดียว ไม่แต่งเลข EP ไม่สร้าง guide/title companion; หากไม่มี URL วิดีโอที่ยืนยันได้และผู้ใช้ห้าม placeholder ให้คงแท็บวิดีโอโดยไม่มี URL สมมติ แล้วระบุการผูกวิดีโอจริงเป็น blocker เฉพาะหมายเหตุเจ้าของช่อง
- เทียบเวลาจบ caption กับ duration ของคลิปตัดต่อที่เลือกก่อนอ้าง timestamp แม้อยู่โฟลเดอร์เดียวกันก็อาจเป็นคนละเวอร์ชัน; ถ้าไม่ตรงให้เก็บข้อจำกัดในหมายเหตุเจ้าของช่อง และใช้เวลาเฟรมของไฟล์จริงสำหรับจุดตรวจความปลอดภัย ห้ามอ้างว่าคำบรรยายตรงทุกวินาทีโดยยังไม่ตรวจ alignment
- อย่าใช้ caption เป็นหลักเมื่อภาพหน้าจอแสดงค่าหรือคำสั่งต่างออกไป
- อย่าใช้ thumbnail ที่หน้าโฮสต์คล้ายแต่ไม่ใช่คนเดียวกัน
- อย่าเขียน 💎 เป็นบทความยาวหรือคัดลอกเนื้อหาจาก 🍀
- อย่าใช้ shell utilities แทน Hermes tools เมื่อมี `read_file`, `search_files`, `write_file`, `patch`
- ถ้า Codex/Drive/Kruoop ติด login, OAuth, 2FA หรือ permission ให้รายงาน blocker แล้วทำ deliverable อื่นต่อ (ไม่ถามกลับระหว่างทาง) ห้ามวาง API key หรือ callback URL ลงในแชต

## Verification

- [ ] ตรวจ source จริงและเวอร์ชันวิดีโอแล้ว
- [ ] caption/timestamp มีระดับความแม่นยำระบุชัด
- [ ] ไฟล์ deliverable ครบตามเงื่อนไขใน reference
- [ ] Title, Description, Tags และ Skool description ผ่านการนับด้วยโค้ด
- [ ] Prompt ในคู่มือตรงกับเฟรมหรือ caption ที่ยืนยันแล้ว
- [ ] ลิงก์ Drive ทุกตัวอ่านจากไฟล์จริงและไม่มี placeholder
- [ ] thumbnail ผ่าน identity, Thai marks, pipeline order, 1280×720 และต่ำกว่า 2 MB
- [ ] ประเด็น privacy/safety/disclaimer ถูกแจ้ง
- [ ] ทุกข้อเท็จจริงภายนอกมี source และ publication time
- [ ] สถานะเป็น `content_review`; ยังไม่มีการเผยแพร่หรืออัปโหลดต่อสาธารณะ
