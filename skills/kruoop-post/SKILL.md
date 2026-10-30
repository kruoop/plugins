---
name: kruoop-post
description: "Write and post Kruoop items for a finished episode: the course (draft; publish on a yes), the resource.zip giveaway post, the community post (only when asked) and the Short's social promo caption (stage 7 of kruoop-content). Use for โพสต์ลง Kruoop, ลงคอร์ส Kruoop, แจก resource, แคปชั่นโปรโมต Short (Facebook/Reels/TikTok). Not video editing, YouTube text or thumbnails."
---


## Host integration

Resolve sibling skills from this bundle first. For browser control, read the sibling ego-browser skill (or its installed user-wide copy) and use ego-browser CLI with TaskSpace. Map tool names to the tools actually available in Claude Code or Codex; examples do not grant permissions. Resolve runtime paths on the current host rather than treating imported paths as proof of installation. Preserve current user authorization for external writes; installing this bundle starts no generation, upload, post, watcher or episode.

# Kruoop post

Turns a finished episode into Kruoop items: a **course** (full video; creating the draft is fine, publishing needs a clear yes) and a **community post** (short video, links to the course). Write `kruoop_post.txt` always, but **post it only when the owner asks** (owner rule: course only, no feed post unless asked). Output is text files in the episode's `publish/` folder, then optionally filled in through the browser.

## Owner rules 2026-10-22 (EP239) — resource giveaway

These override anything below ([full rules](../bbn-ai-edit/references/owner-rules-2026-10-22.md); its Drive "overwrite in place" rule is for `BBN-Video/<EP>` deliveries only, and Kruoop course episodes upload new files, see `kruoop-content`):

- When the clip mentions a file, template, prompt or workflow to hand out, build it so it **actually works** (open/import/run it once), zip it as exactly `resource.zip`, and strip secrets.
- Post it in the **BoomBigNose** community on Kruoop, category **📚 แหล่งความรู้**, with `resource.zip` **attached directly to the post**. No Drive links, no "in the first comment".
- **No EP number anywhere**: not in the post title, body, zip name, file names or file contents inside the zip. Check before posting (all three must print nothing; the pattern catches EP239/EP 239/EP-239/EP_239/ตอนที่ 239 but skips "Step 1"):
  `P='(^|[^a-z])ep[ ._-]?[0-9]|ตอน(ที่)? ?[0-9]'`
  `unzip -Z1 resource.zip | grep -iE "$P"`
  `zipgrep -iE "$P" resource.zip`  (every file's contents; binary matches also count)
  `sed -n '/^หัวข้อ:/,/^---$/p' publish/kruoop_resource_post.txt | grep -iE "$P"`
- The resource post uses its **own template** (`publish/kruoop_resource_post.txt`, below), not the clip/course announcement: it does not need the Short or the course URL, so it can go out before the Package.
- This resource post is **pre-authorized**: post it without asking, then save the live URL at the end of `kruoop_resource_post.txt` and hand it to `bbn-youtube-description` (`--resource-post <URL>`). The clip/course announcement post and course publishing keep their approval step; YouTube is never posted automatically.

### `publish/kruoop_resource_post.txt`

```
หัวข้อ:
<what the resource is + what it does for the member, no EP number>

เนื้อหา:
<2–3 friendly ครับ sentences: what's in resource.zip, who it's for, how to use it (open/import/run steps)>

ในไฟล์มีอะไรบ้าง
• <file 1 — what it is>
• <file 2 — what it is>

📎 แนบ resource.zip ไว้ในโพสต์นี้แล้ว โหลดไปใช้ได้เลยครับ
---
ชุมชน: BoomBigNose · หมวดหมู่: 📚 แหล่งความรู้ · แนบไฟล์: resource.zip
URL โพสต์: <fill after posting>
```

Only the text between `หัวข้อ:` and `---` is published.
- A revised resource replaces the attachment on the same post (edit the post, same URL), not a new post.

## Inputs

Read these from the episode before writing; never invent facts, prices, credits or node names:
- Final long MP4 (course lesson) and short/vertical MP4 (post media) — note duration and size.
- Thumbnail (`publish/thumbnail_final.png` if it exists) — course cover.
- YouTube title/description from `bbn-youtube-title` / `bbn-youtube-description` if already made — reuse the facts, don't copy the YouTube link block.
- `resource.zip` (workflow JSON, prompts, templates, README) if the episode has downloadable files.

## Files to write

### `publish/kruoop_course.txt`

```
ชุมชน: Kruoop Community · สิทธิ์ดู: ทุกคน · เลเวล: ไม่กำหนด · การเผยแพร่: เก็บเป็นฉบับร่าง
รูปปก: <thumbnail file>

ชื่อคอร์ส:
<short Thai title, same promise as the YouTube title, no emoji>

คำอธิบาย:
<2–3 sentence hook: what the viewer starts with → what they end up with, tools named>

เรียนจบได้ <concrete outcome + files they get>

หมายเหตุ: <costs/credits as estimates, "เสียงบรรยายเป็นเสียงโคลนของผู้สอนเอง" when the cloned voice is used, AI-generated people are not real>

โมดูล 1: <module title>
บทเรียน 1 (วิดีโอ, <N> นาที): <lesson title> (คลิปเต็ม)
วิดีโอ: <path> (<size>, อัปโหลดจากเครื่อง)
สรุปสั้น:
<one paragraph: the steps covered in order, troubleshooting tips shown, where attachments are>
สิ่งแนบ: resource.zip (<size>: <contents>)
```

Drop the `หมายเหตุ` line items that don't apply; drop `สิ่งแนบ` if there is no attachment.

### `publish/kruoop_post.txt`

```
หัวข้อ:
🚀 คลิปใหม่: <course title>

เนื้อหา:
<2–3 sentences, friendly ครับ tone: what the clip does + who it's for>

ในคลิปนี้มีอะไรบ้าง
• <point 1>
• <point 2>
• <point 3>

📎 <what's in resource.zip> แนบไฟล์ไว้ในโพสต์นี้แล้ว โหลดไปใช้ได้เลยครับ

ดูคลิปเต็มในคลาสเรียนได้เลยครับ 👇
<course URL — fill after the course exists; leave <COURSE_URL> until then>

ชุมชน: BoomBigNose · หมวดหมู่: 📚 แหล่งความรู้ · ส่งอีเมล: <เปิด/ปิด> · แชร์สู่เครือข่าย: ปิด
สื่อในโพสต์: <short MP4 path> (<size>)
ไฟล์แนบในโพสต์: resource.zip
```

Omit the 📎 line and `ไฟล์แนบในโพสต์` when there's nothing to attach. Never put an EP number in `หัวข้อ` or `เนื้อหา`.

### `publish/social_captions.txt` (Short promo: Facebook, Reels, TikTok, YouTube Shorts)

The 3D Short is promo material for the course: it is posted on social media, and it is not swapped into the Kruoop
course unless the owner says so. Its spoken CTA is a comment gate, so the caption repeats the same keyword and gives no
URL to the resource. Proven format (LineAI-n8n, 2026-10):

```
ชื่อคลิป (Shorts / Reels / TikTok)
<hook title, ≤ 60 chars, + 1 hashtag>

แคปชัน
<one-line hook with one emoji>
<emoji> <concrete thing it does 1>
<emoji> <concrete thing it does 2>
<emoji> <concrete thing it does 3>
<one line: how simple it is / what tool>

อยากได้<คลิปเต็ม + คู่มือ> คอมเมนต์คำว่า "<KEYWORD>" ไว้ เดี๋ยวผมส่งให้ครับ 👇

#<tool> #<topic> #AI #<Thai tag> … (5–8)

หมายเหตุ
- เสียงบรรยายเป็นเสียงโคลนของผู้สอนเอง
- <sample data is fictional, when it is>
- ภาพ 3D ทำด้วย Blender + three.js · โลโก้ <brands> เป็นเครื่องหมายการค้าของเจ้าของ
```

The keyword must be exactly the one spoken at the end of the Short. If the owner wants a version that links to the
course instead (no comment gate), write it as a second block, `แคปชัน (ลิงก์คอร์ส)`, ending with the course URL. A
Kruoop community post that uses the Short links to the course directly. Its outro says "คอมเมนต์…", so add a note
(the gate is meant for YouTube, TikTok and Facebook; trim or swap the outro for a Kruoop-only upload). Posting to
Facebook or anywhere else needs the owner's clear yes. By default, hand them the file and the caption.

## Rules

- Thai, plain, one promise per item. Exactly 3 bullets in the post.
- No comment-gate lines ("คอมเมนต์ว่า…เดี๋ยวส่งให้") in `kruoop_course.txt` or `kruoop_post.txt`; Kruoop posts link straight to the course. The gate belongs only in `social_captions.txt` (the Short).
- No Hostinger/Workshop/Skool promos unless the owner asks for them in this episode.
- Never put secrets in attachments: strip API keys, tokens and credentials from workflow JSON before zipping (`grep -iE 'key|token|secret|bearer'`).
- Course order: create the course first (draft), copy its URL into the post, then post.

## Posting through the browser

Use `ego-browser` (the user's logged-in Kruoop session). Open `https://kruoop.com/feed/enter?c=kruoop` first: if another community is active, the course edit page shows "ไม่พบหน้านี้". Fill the course form from `kruoop_course.txt` and **leave it as a draft**. The resource post (BoomBigNose, 📚 แหล่งความรู้, `resource.zip` attached) is pre-authorized and is posted without asking. Publishing a course or turning on community email still needs a clear yes from the owner. After posting, save a screenshot as `publish/kruoop_post_live.png` and write the live URLs back into the two text files.

## Example

A finished pair from the n8n Chinese-drama episode (2026-10-20) lives in that episode's `publish/kruoop_course.txt` and `kruoop_post.txt` (episode folder location differs per machine).
