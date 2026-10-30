# Kruoop Plugins & Skills

คลังใหญ่สำหรับปลั๊กอินและสกิลของ Kruoop (Claude Code plugins & skills marketplace)

## ติดตั้ง marketplace

```
/plugin marketplace add kruoop/plugins
```

## โครงสร้าง

- `plugins/` — ปลั๊กอินของ Kruoop
- `skills/` — agent skills ของ Kruoop
- `.claude-plugin/marketplace.json` — manifest ของ marketplace

## ลิงก์

- เว็บไซต์: https://kruoop.com
- GitHub: https://github.com/kruoop/plugins

## BBN-AI-Edit / BBN Video Studio

ชุดสกิล BBN ล่าสุดทั้ง 48 ตัวอยู่ใน [`skills/`](skills/README.md) และแพ็กติดตั้งผ่าน marketplace อยู่ที่ [`plugins/bbn-video-studio/`](plugins/bbn-video-studio/README.md)

```text
/plugin marketplace add kruoop/plugins
/plugin install bbn-video-studio@kruoop-plugins
```

สำหรับ Codex ให้ clone repo นี้แล้วรัน:

```bash
python3 scripts/install_bbn_skills.py
python3 scripts/install_bbn_skills.py --check
```

ตัวติดตั้งสำรองสกิลที่มีชื่อซ้ำก่อนแทน ไม่แก้สกิลอื่น จากนั้นเรียก `$bbn-ai-edit` ใน Codex

ต้นฉบับอยู่ใน `skills/` เมื่อแก้แล้วให้รัน `python3 scripts/sync_bbn_plugin.py` เพื่ออัปเดตชุดแจกในปลั๊กอิน และ `python3 scripts/sync_bbn_plugin.py --check` เพื่อตรวจชื่อไฟล์และ SHA-256 ทุกไฟล์

การแก้สกิลครั้งนี้รวม Short แบบ teaser, เพลงใน assets และ final mix, การแก้ CTA เฉพาะภาพ และการใช้ชื่อ v2 ตามคำสั่งผู้ใช้ โดยไม่เริ่มตัดหรือเผยแพร่คลิปจากการติดตั้ง
