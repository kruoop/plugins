# ผูกกับเสียงและส่งเข้าไทม์ไลน์

## ขอบเขตและเวลา

สำหรับ Short ใช้ render_mode เป็น upper-half ตามขนาดแผงจริง หลังฮุคคนพร้อมห้องเดิมอยู่ครึ่งล่างโดยไม่ทำ matting Topic bridge และการอธิบายเครื่องมือใช้โมชั่นตามเสียงจริง ไม่ใช้ภาพเว็บทั่วไปแทนแนวคิด หาจุดคืนภาพจริงจากคำชวนดู/เริ่มพาทำร่วมกับ footage และ source→final mapping ไม่รอจบ historical segment ที่ตั้งชื่อว่า teaching/invitation ตัวอย่าง full-frame ด้านล่างเป็นตัวอย่าง clock สำหรับงานทั่วไป ไม่ใช่คำสั่งเปลี่ยน Short ให้เต็มจอ

แบ่งไทม์ไลน์เป็น `explanation` และ `teaching` จากคำพูดร่วมกับภาพจริงก่อนวาง cue สกิลนี้ทำงานเฉพาะ explanation เก็บ `teaching_start_frame` เป็นขอบเขตจบของโมชั่นทั้งหมด รวม hold/exit/transition คืนคลิปอัดหน้าจอในเลย์เอาต์สอนเดิมตั้งแต่เฟรมนั้นตลอดช่วงสอน ไม่รอถึงการคลิกครั้งแรก และไม่แทรก pop-up ระหว่างอธิบายวิธีทำหรือรอโหลดในช่วงสอน หากกลับมาอธิบายแนวคิดแยกต่างหาก จึงเปิด explanation segment ใหม่

ยึด source→final mapping ของ editor หลักและเวลาในคลิปหลังตัด สำหรับงานแก้ภาพใช้ final timeline ที่รับรองแล้ว ถ้าผู้ใช้ระบุ source time ให้แปลงผ่าน mapping ไม่เดา offset

ระบุ FPS เป็นเศษส่วนเมื่อจำเป็น เช่น 30000/1001 เก็บช่วงเป็นจำนวนเต็ม `[start_frame,end_frame)` เริ่ม/จบ = round(seconds × fps) โดยใช้กฎ half-up สำหรับเวลาไม่ติดลบและตรวจขอบเขตกับ editor เดิม ระยะเวลาไฟล์ = `(end_frame-start_frame)/fps` seek เฟรมท้องถิ่น i = `i/fps`; เวลาในคลิปหลัก = `(start_frame+i)/fps`

transcript กับช่วงประโยคใช้กำหนดร่างได้ แต่ timestamp ของคำยึดจังหวะเป็น provisional จนฟัง/ตรวจเสียงจริง ไม่สมมติแบ่งประโยคเท่า ๆ กันตามจำนวนคำ ตรวจรอบคำสำคัญและเฟรมใกล้เคียง ให้ผู้ชมรู้ต้นทางก่อนเคลื่อนและถึงปลายทางในช่วงคำบอกผล เสียงเร็วให้ลดรายละเอียด ไม่เปลี่ยนความเร็วเสียงหรือเพิ่มความยาวคลิปเอง

## Cue manifest

ตัวอย่างร่าง: คลิป 30fps ช่วง source 40–48s ย้ายมา final 12–20s หน้าจอจริงเริ่ม 17.2s จึงจบกราฟิกก่อนเฟรม 516 เวลาเหตุการณ์ย่อยยังไม่ได้ตรวจเสียง:

```json
{
  "fps": { "num": 30, "den": 1 },
  "clock": "final-edited-video",
  "rounding": "half-up",
  "timing_status": "provisional-within-known-segment-bounds",
  "scenes": [
    {
      "id": "sources",
      "final_start_frame": 360,
      "final_end_frame": 432,
      "pattern": "converging-paths",
      "spoken_text": "รับข้อมูลจากฟอร์ม อีเมล และแชตมารวมไว้ที่เดียว",
      "cue_phrase": "รวมไว้ที่เดียว",
      "nodes": ["ฟอร์ม", "อีเมล", "แชต", "ข้อมูลรวม"],
      "action": "สามการ์ดเข้าโหนดข้อมูลรวม",
      "result": "ข้อมูลรวม",
      "render_mode": "full-frame",
      "caption_clearance": "use existing subtitle bounds"
    },
    {
      "id": "checks",
      "final_start_frame": 432,
      "final_end_frame": 516,
      "pattern": "workflow-board",
      "spoken_text": "จากนั้น AI ตรวจสอบ แล้วส่งให้ทีมอนุมัติ",
      "cue_phrase": "ส่งให้ทีมอนุมัติ",
      "nodes": ["ข้อมูลรวม", "AI ตรวจสอบ", "รอทีมอนุมัติ"],
      "action": "การ์ดผ่านขั้นตรวจสอบไปคอลัมน์รอทีม",
      "result": "รออนุมัติ",
      "render_mode": "full-frame",
      "transition_in": "vertical-slide",
      "return_to_real_screen_frame": 516
    }
  ]
}
```

ช่วง transition รวมอยู่ในเฟรมที่จัดสรร ไม่เพิ่มเวลาและเลื่อนเสียงข้างหลัง ถ้าเริ่มก่อนแบ่งฉาก ระบุ overlap/tracks ให้ชัดและเก็บภาพทั้งคู่ในขอบเขตแทรกรวม หน้าจอจริงที่ต้องเห็นเป็นจุดจบตายตัว

บันทึก `transition.start_frame`, `transition.end_frame` และวิธีรักษาภาพ outgoing: snapshot ของเฟรมสุดท้าย หรือ clip ที่ยัง visible จนจบ transition หากใช้ overlap ให้แยกช่วง render/visibility ออกจากช่วงคำพูด ตัวอย่าง transition `[432,444)` ต้องยังเห็น A1 ผ่านเฟรม 443 แม้ประโยค A1 จบที่ 432; อย่าปิด A1 ที่ 432 แล้วเลื่อนภาพว่าง ใช้ tracks ที่รองรับ overlap ตาม contract ของ compositor

ตัวอย่างไฟล์รวมสองฉากมี 156 เฟรม ยาว 5.2s วางที่เฟรม 360; เฟรม 516 กลับภาพจริง เก็บ local offsets ด้วย ไม่ใช้ 12s เป็นเวลาเริ่ม animation ภายในไฟล์ 5.2s

### Cue สำหรับป็อปอัพและการประกอบ UI

บันทึกแต่ละชิ้นใน `events` ของฉาก โดยมี `cue_phrase`, `visual`, `asset_path` หรือ `asset_fallback`, `placement`, `entrance`, `hold`, `exit`, `final_frame` และ `timing_status` ถ้ายังไม่ได้ตรวจเสียง ให้ `final_frame` เป็น null และสถานะ provisional ไม่สร้างเฟรมย่อยที่ดูเหมือนตรวจมาแล้ว

ก่อนเรนเดอร์ แต่ละ event ต้องมี `enter_start_frame`, `enter_end_frame`, `exit_start_frame`, `exit_end_frame`; ช่วง hold คือ `[enter_end_frame,exit_start_frame)` พร้อม `persist_until` สำหรับวัตถุที่ต้องอยู่ข้ามช่วงคำพูดหรือฉาก ทุกค่ามี clock เดียวกับ manifest และผ่าน mapping เป็น local time ของไฟล์กราฟิก ถ้าไม่มีเวลา hold ให้ลดรายละเอียดหรือปรับ choreography ภายในขอบเขตเดิม

ตัวอย่าง: “Claude ช่วยคิดโครง” ใช้ badge/ชื่อ Claude และโครงหน้าเว็บ; “Codex เขียนหน้าเว็บ” เพิ่ม badge/ชื่อ Codex กับโครงเนื้อหา; “เพิ่มปุ่ม การ์ด แล้วก็กราฟ” เพิ่ม component แต่ละชิ้นตรงคำจริง ไม่แบ่งช่วงเสียงเป็นสามส่วนเท่ากันเอง กำหนด hold/exit เพื่อให้ชิ้นที่ยังมีบทบาทอยู่ในภาพ แต่เอาป็อปอัพที่หมดบทบาทออกโดยไม่ทับซับ

ถ้าทั้ง scene ยาว 4s ที่ 30fps ให้เรนเดอร์ 120 เฟรม ป็อปอัพและ build events ต้องอยู่ในช่วงนี้ทั้งหมด ตรวจเสียงก่อนเปลี่ยนสถานะเป็น verified และบันทึกแหล่งเวลาที่ใช้ตรวจใน manifest

## สร้างและส่งไฟล์

ใช้ HTML/CSS/SVG สำหรับการ์ด เส้น และตัวอักษร กับ GSAP paused/registered timeline เมื่อใช้ HyperFrames ทำตาม duration/track contract ของเครื่องมือ ใช้ฟอนต์/asset ที่ตรวจแล้วและ timeline ที่ seek ได้ จำนวนรอบจำกัดตามฉาก ไม่มี setTimeout, Date.now, Math.random หรือ infinite repeat เป็นตัวขับการเคลื่อน

- **ฉากเต็ม:** MP4 พร้อมพื้นหลัง FPS/resolution ตรงคลิป ไม่มีเสียงเมื่อใช้เสียงคลิปเดิม
- **วางทับภาพ:** format ที่มี alpha จริง เช่น ProRes 4444 MOV หรือ PNG sequence ตามที่ compositor รองรับ ตรวจ renderer/encoder ก่อนเลือก format ชื่อ MOV หรือ pix_fmt เพียงอย่างเดียวไม่พิสูจน์ alpha
- **แก้ไขต่อ:** composition source, assets ที่ใช้, ฟอนต์หรือข้อมูลอ้างอิงตามสิทธิ์ใช้งาน และ cue manifest ในโฟลเดอร์งานเดิม

ถ้า alpha export ไม่รองรับโดยตรง ใช้ PNG RGBA sequence และ encoder ที่ตรวจแล้ว ถ้ายังทำไม่ได้เลือกฉากเต็มเมื่อบรีฟอนุญาตหรือแจ้งข้อจำกัด ไม่ใช้ chroma key เป็นค่าเริ่มต้นเพราะขอบตัวอักษร/สีส้มอาจเสีย

ไม่สร้างเสียงพูดใหม่ งานภาพอย่างเดียวไม่เพิ่ม whoosh/click เอง ถ้า editor หลักอนุญาต sound design ใช้เสียงสั้นตาม action ที่มีความหมายและตรวจว่าพูดยังชัด

## QA กับ export จริง

1. ตรวจ hero frame ก่อนโมชั่น: ป้ายไม่ซ้อน ซับ/ใบหน้า/UI มีพื้นที่ อ่านสระและวรรณยุกต์ครบ
2. ดู entrance, 25/50/75% ของทาง, ถึงปลายทาง, hold, กลาง transition และเฟรมติดรอยต่อ เส้นกับการ์ดตรงกัน ผลตรงคำพูด ป็อปอัพใช้ภาพตรงกับสิ่งที่พูดและเข้าตรงคำ UI build เพิ่ม component ตามลำดับคำจริง ไม่มีชิ้นที่ต้องเพิ่มแต่ปรากฏครบตั้งแต่ต้น
3. ใช้ lint/validate/inspect ที่ HyperFrames เวอร์ชันติดตั้งรองรับ แล้วตรวจภาพ encode ด้วย การผ่าน layout check ไม่แทนการดูโมชั่นกับเสียง
4. ตรวจ dimensions, FPS, decoded frame count และ duration เทียบ manifest พร้อม full decode ของ segment ถ้ามี alpha ทดลอง composite เหนือพื้นดำและขาว
5. ดู preview จาก export ที่ประกอบแล้วพร้อมเสียงเดิม คำยึดจังหวะตรง หน้าจอจริงกลับตั้งแต่เริ่มสอนและคงเลย์เอาต์สอนเดิมตลอด teaching ไม่มี pop-up ค้างหรือโผล่ระหว่างสอน กราฟิกไม่ทำให้เข้าใจผิดว่ามีผลสาธิตที่ยังไม่เกิด

งาน patch คลิปที่รับรองแล้วใช้กติกา timing/audio ของ editor หลัก ตรวจขอบเขตที่เปลี่ยน อ้างว่า audio เหมือนเดิมเมื่อมี preservation check จริง ไม่เริ่ม ASR ทั้งเรื่องหรือ normalize เสียงใหม่เพื่อแก้กราฟิกสั้น ๆ

ส่งไฟล์ที่เรนเดอร์จริง ซอร์ส และ cue manifest พร้อมช่วง final ที่แทรกและข้อจำกัด เก็บหลักฐาน/ฟุตเทจ/transcript ของแต่ละตอนในโฟลเดอร์ตอน ไม่คัดลอกลงสกิลส่วนตัวนี้
