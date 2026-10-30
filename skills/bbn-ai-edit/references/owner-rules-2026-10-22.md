# กฎเจ้าของช่อง 2026-10-22 (จากงาน EP239)

ไฟล์นี้คือกฎกลางที่ทุกสกิล BBN อ้างถึง ชนะข้อความเก่าในสกิล/reference/MASTER_PROMPT ที่ขัดกัน ยกเว้นคำสั่งล่าสุดของเจ้าของช่องในงานนั้น

## คำสั่งชื่อรุ่นใหม่โดยตรง — เพิ่ม 2026-10-30

ข้อห้ามสร้าง `_v2`/`_v3` ด้านล่างเป็นค่าเริ่มต้น ห้ามใช้ปฏิเสธคำสั่งล่าสุดที่ผู้ใช้ขอชื่อรุ่นใหม่โดยตรง ให้สร้างรุ่นนั้นครั้งเดียวและอัปทับชื่อ/ID ของรุ่นนั้นในการแก้ต่อไป โดยตรวจ remote และรักษาต้นฉบับเดิม สำหรับ Short แบบ teaser ให้ใช้ [แนวทาง teaser/CTA](../../bbn-ai-short-fullscreen/references/teaser-and-ending-revisions.md) ตามบรีฟล่าสุด

## 1. แก้งาน = อัปทับไฟล์เดิมบนไดรฟ์ ชื่อเดิม ID เดิม

- ทุกรีวิชัน (Long, Short, Package, ปก, Skool, resource.zip) อัปทับไฟล์เดิมใน `BBN-Video/<EP>/` ด้วยชื่อเดิม ห้ามสร้าง `_v2`, `_v3`, `-final`, `(1)` หรือไฟล์ซ้ำบนไดรฟ์ ประวัติรุ่นก่อนเก็บในเครื่องเท่านั้น (`archive/` ของ EP) ไม่อัปขึ้นไดรฟ์
- ใช้ [scripts/drive_replace.sh](../scripts/drive_replace.sh): `drive_replace.sh <ไฟล์ในเครื่อง> <โฟลเดอร์บนไดรฟ์> [ชื่อบนไดรฟ์]` โฟลเดอร์คือ `<EP>` สำหรับวิดีโอ/Package/resource และ `<EP>/Thumbnail` สำหรับปก รีวิชันต้องได้ผล `replaced-in-place` ถ้าได้ `new` แปลว่า path ผิดและเกิดไฟล์ใหม่ ให้แก้ทันที สคริปต์จะ
  1. หา remote: `bbndrive:` ถ้ามีใน `rclone listremotes` (root = BBN-Video) ไม่งั้น `gdrive:`; ส่ง `--drive-root-folder-id 13PTVmiD5YJPVgytx5WLYpJs3M-EvpcwZ` ทุกครั้ง (override ด้วย `BBN_DRIVE_REMOTE` / `BBN_DRIVE_ROOT`)
  2. หยุดถ้ามีไฟล์ชื่อนี้มากกว่า 1 ไฟล์ (ต้อง dedupe ก่อน)
  3. `rclone copyto` ทับชื่อเดิม
  4. ตรวจว่ามีชื่อนี้ไฟล์เดียว file ID ไม่เปลี่ยน และ md5 บนไดรฟ์ = `md5 -q` ในเครื่อง
- ทำเองเมื่อรีวิชันผ่าน QA ไม่ต้องถามยืนยันการอัป

## 2. Package / Description ต้องตรงรูปแบบ EP242

- ตัวอย่างที่ล็อก: [reference-EP242_Package.txt](../../bbn-youtube-description/assets/reference-EP242_Package.txt) (Drive id `1xOhHLwFGUBI2mzyyGc6fU1YQVOLAiAvG`, ดึงใหม่ด้วย `rclone backend copyid <remote> 1xOhHLwFGUBI2mzyyGc6fU1YQVOLAiAvG <dir>`) ทุกหัวข้อ ป้าย บรรทัดว่าง อิโมจิ ลำดับ ต้องเหมือนกัน เปลี่ยนเฉพาะเนื้อหาของ EP
- Timeline ไม่เกิน 10 chapters
- Package ไม่ใส่เครดิตเพลง (ไม่มีบรรทัด 🎵)
- ตัวตรวจ: `bbn-youtube-description/scripts/check_package.py <pkg> --duration <วินาที> [--resource-post <URL>]`

## 3. ปก: bbn-youtube-thumbnail + Codex CLI native เท่านั้น

- สร้างด้วย `codex exec` (native image generation) ผ่านสกิล [bbn-youtube-thumbnail](../../bbn-youtube-thumbnail/SKILL.md) เท่านั้น ไม่ใช้ Phaya, Canva, ปกปัง Studio, image_generate หรือ HTML/CSS-only layout
- หน้าคนใช้ approved face [assets/shared/face/face.png](../assets/shared/face/face.png) เท่านั้น ห้ามใช้เฟรมจากวิดีโอแทนหน้า โลโก้/มาสคอตต้องเป็นไฟล์ของจริง
- ทีมปกคือบอท **น้องปก**: ส่งปกให้รีวิวผ่านเส้นทางของน้องปกที่ตั้งไว้แล้วบนเครื่อง ถ้ายังไม่มีเส้นทางให้รายงาน ห้ามสร้างบอทหรือ token ใหม่

## 4. อินเสิร์ต/เดโม = อัดหน้าจอจริง

- เมื่อคลิปพูดถึงการทำบนจอ (เปิดแอป กดเมนู พิมพ์ prompt ดูผลลัพธ์) แต่ฟุตเทจไม่มีภาพนั้น ให้อัดหน้าจอจริงทำตามที่พูด ไม่ใช้ UI ปลอม/โมชันแทน
- คำสั่ง macOS: `screencapture -v -V <วินาที> -k -x [-R x,y,w,h | -D <display>] <out.mov>` (`-V` จำกัดเวลาให้รันแบบไม่ต้องกดหยุด, `-k` แสดงคลิก, `-x` ปิดเสียงชัตเตอร์) แล้วตัดให้จังหวะภาพตรงกับคำพูดใน cut plan
- ตรวจไฟล์ทุกครั้งด้วย `ffprobe` ถ้า `screencapture` จบ exit 1 และไม่มีไฟล์ แปลว่าโปรเซสที่รัน (Terminal/Claude/Codex) ยังไม่ได้สิทธิ์ Screen Recording: ให้เปิด System Settings → Privacy & Security → Screen & System Audio Recording อนุญาตครั้งเดียวต่อเครื่อง (ข้อ 6) ระหว่างรอ เดโมที่อยู่ในเบราว์เซอร์อัดด้วย ego-browser recorder (แบบ `work/EP237/tools/dotrec.mjs`) ได้ (ทดสอบ 2026-10-22 บนเครื่อง boomvitt: ยังไม่ได้สิทธิ์ ได้ exit 1)
- เบลอข้อมูลส่วนตัว (อีเมล ชื่อบัญชี token แชต ประวัติ) ก่อนส่ง บันทึกช่วงที่อัดลง `footage-ledger.json`

## 5. Resource แจก = resource.zip + โพสต์ชุมชน Kruoop

- ถ้าคลิปพูดถึงไฟล์/เทมเพลต/prompt ที่แจก ให้ทำไฟล์ที่ใช้ได้จริง รวมเป็น `resource.zip` (ชื่อนี้เท่านั้น) ไม่มีเลข EP ในชื่อไฟล์ใด ๆ ใน zip ไม่มี secret
- โพสต์แจกในชุมชน Kruoop ของ BoomBigNose หมวด `📚 แหล่งความรู้` แนบ `resource.zip` ตรงในโพสต์ ห้ามใส่ลิงก์ไดรฟ์ ห้ามมีเลข EP ในหัวข้อ/เนื้อหา/ชื่อไฟล์/เนื้อไฟล์ ใช้ template `kruoop_resource_post.txt` ของสกิล [kruoop-post](../../kruoop-post/SKILL.md) (ไม่ต้องรอ Short หรือคอร์ส)
- เอา URL โพสต์ใส่ Description เป็นบรรทัดลิงก์สำคัญ `- <ชื่อ resource> (แจกฟรีในชุมชน Kruoop) — <URL>` แล้วตรวจด้วย `--resource-post <URL>`
- ลำดับ: ทำโพสต์ resource ก่อนปิด Package ถ้าโพสต์ทีหลัง ให้แก้ Package แล้วอัปทับไฟล์เดิมตามข้อ 1

## 6. ทำเองจนจบ ไม่ถามกลับ

- ทำทุก deliverable ที่สั่งจนจบโดยไม่ถามยืนยันระหว่างทาง ถ้าติด blocker ให้รายงานแล้วทำส่วนอื่นต่อ ไม่หยุดรอ
- สิทธิ์บนเครื่อง (macOS Screen Recording, Accessibility, Claude Code permission) ขอครั้งเดียวแล้วเลือก always allow / เพิ่มใน allowlist ไม่ขอซ้ำทุกงาน
- **ไม่โพสต์/อัปโหลด/ตั้งเวลา YouTube อัตโนมัติ** ยังต้องรอเจ้าของช่องสั่งเฉพาะ EP ส่วนโพสต์ resource ใน Kruoop ตามข้อ 5 ได้รับอนุญาตถาวรแล้ว (คอร์ส Kruoop ยังเก็บเป็น draft)

## 7. Path ไม่ผูกเครื่อง

- เขียน path เป็น `~/` หรือ `$HOME/` หรือ relative ต่อสกิล ห้าม `/Users/<ชื่อ>/` ใช้ได้ทั้ง Mac Studio (user `boombignose`), Mac mini (user `boombignose-server-macmini-001`) และเครื่องอื่น
- runtime ตัดต่อ: `~/.local/share/bbn-ai-cut/` (README, `venvs/mlx`, `venvs/thai`, `models.json`, `checks/`); สกิล: `~/.codex/skills/<name>/`
- path จากเครื่องเก่าที่อาจเหลือในไฟล์ snapshot/หลักฐานเป็นประวัติ ไม่ใช่ path ที่ใช้รันจริง
