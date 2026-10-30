# BBN Video Studio 0.4.0

ชุด BBN-AI-Edit ทั้ง 48 สกิล สำหรับ Claude Code และ Codex รวม Long, Short, motion, เสียง, thumbnail และชุดข้อความ YouTube

ติดตั้งใน Claude Code:

```text
/plugin marketplace add kruoop/plugins
/plugin install bbn-video-studio@kruoop-plugins
```

เรียกสกิลหลักด้วย `/bbn-video-studio:bbn-ai-edit` แล้วระบุ EP และงานที่ต้องการ

Codex ติดตั้งจาก checkout ของ repo นี้ด้วย `python3 scripts/install_bbn_skills.py` ที่ root ของ repo แล้วเรียก `$bbn-ai-edit` สคริปต์สำรองชุดเดิมก่อนแทน และไม่แก้สกิลอื่น

อัปเดต 2026-10-30: Short แบบ teaser เน้นชวนดู Long, เพลงต้องอยู่ใน assets และเสียง export, CTA ตามข้อความที่สั่ง, การแก้ข้อความท้ายรักษาเสียง/เวลาเดิมและปรับ editable project ให้ตรงกัน สร้าง v2 ได้เมื่อผู้ใช้ขอโดยตรง แล้วอัปทับชื่อ/ID ของ v2 เดิมในการแก้ต่อไป ไม่ใช้คำว่า Gemini หรือความยาว 45 วินาทีเป็นค่าบังคับทุก EP

ต้นฉบับสกิลอยู่ที่ `skills/` ระดับ root ของ repo ส่วน `skills/` ในปลั๊กอินนี้สร้างด้วย `python3 scripts/sync_bbn_plugin.py` เพื่อให้ติดตั้งเป็นแพ็กที่มีไฟล์ครบโดยไม่อ้างพาธนอกปลั๊กอิน ตรวจความตรงกันด้วย `--check`

แพ็กมี instructions, scripts, templates และ shared assets รวมเพลง แต่ runtime, model weights, FFmpeg/rclone/HyperFrames, fonts และการเชื่อมต่อบัญชีต้องตรวจบนเครื่องปลายทาง การติดตั้งไม่เริ่มตัด EP, watcher, การแจ้งเตือนหรือเผยแพร่คลิป
