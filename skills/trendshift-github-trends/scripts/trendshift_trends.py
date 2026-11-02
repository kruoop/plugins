#!/usr/bin/env python3
"""ดึง repo ที่กำลังเทรนด์จาก Trendshift.io (หน้าเว็บสาธารณะ) + ตรวจดาวกับ GitHub API

ใช้ Python มาตรฐานล้วน (ไม่ต้อง pip install)

ตัวอย่าง:
  python3 trendshift_trends.py                       # daily 25 อันดับ ตาราง markdown
  python3 trendshift_trends.py --period weekly --min-stars 10000 --ai-only --verify
  python3 trendshift_trends.py --language Python --limit 10 --json > out.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta

BASE = "https://trendshift.io"
PERIOD_PATH = {"daily": "/", "weekly": "/weekly", "monthly": "/monthly", "yearly": "/yearly"}
UA = "BoomBigNose-trendshift-skill/1.0 (+https://github.com/kruoop/plugins; content research)"
BKK = timezone(timedelta(hours=7))

AI_TAGS = {"ai-agent", "ai-coding", "ai-chat", "ai-memory", "ai-skills", "llm-inference",
           "agent-sandbox", "browser-automation", "rag", "mcp", "ai-image", "ai-video", "ai-audio"}
AI_WORDS = re.compile(r"\b(ai|llm|llms|agent|agents|agentic|gpt|claude|codex|gemini|deepseek|qwen|"
                      r"mcp|rag|model|models|diffusion|whisper|tts|copilot|prompt|inference|"
                      r"vision|chatbot|ml|neural)\b", re.I)


def http_get(url: str, headers: dict | None = None, timeout: int = 30) -> tuple[int, bytes, dict]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read() or b"", dict(e.headers or {})


# ---------------------------------------------------------------- Trendshift
def _rsc_payload(html: str) -> str:
    """รวมก้อนข้อมูล Next.js (self.__next_f.push) ที่ฝังอยู่ในหน้า"""
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)', html)
    return "".join(json.loads(f'"{c}"') for c in chunks)


def _parse_initial_data(html: str) -> list[dict]:
    s = _rsc_payload(html)
    dec = json.JSONDecoder()
    for m in re.finditer(r'"initialData":', s):
        try:
            data, _ = dec.raw_decode(s[m.end():])
        except ValueError:
            continue
        if isinstance(data, list) and data and isinstance(data[0], dict) and "full_name" in data[0]:
            return data
    return []


def _parse_jsonld(html: str) -> list[dict]:
    """สำรอง: ใช้ JSON-LD ItemList (ไม่มีจำนวนดาว ต้องเติมจาก GitHub)"""
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S):
        try:
            d = json.loads(m.group(1))
        except ValueError:
            continue
        if isinstance(d, dict) and d.get("@type") == "ItemList":
            out = []
            for el in d.get("itemListElement", []):
                it = el.get("item", {})
                out.append({
                    "rank": el.get("position"), "full_name": it.get("name"),
                    "repository_description": it.get("description"),
                    "repository_language": it.get("programmingLanguage"),
                    "repository_stars": None, "repository_stars_gained": None, "score": None,
                    "tags": [{"slug": k.lower().replace(" ", "-"), "display_name": k} for k in it.get("keywords", [])],
                    "trendshift_url": el.get("url"),
                })
            return out
    return []


def fetch_trendshift(period: str) -> tuple[list[dict], str]:
    url = BASE + PERIOD_PATH[period]
    status, body, _ = http_get(url)
    if status != 200:
        raise SystemExit(f"Trendshift ตอบ HTTP {status} สำหรับ {url}")
    html = body.decode("utf-8", "replace")
    raw = _parse_initial_data(html)
    source = "rsc"
    if not raw:
        raw, source = _parse_jsonld(html), "jsonld"
    if not raw:
        raise SystemExit("อ่านข้อมูลจากหน้า Trendshift ไม่ได้ (โครงหน้าเว็บอาจเปลี่ยน) — ดูหัวข้อ 'ถ้าสคริปต์พัง' ใน SKILL.md")
    repos = []
    for r in raw:
        fn = r.get("full_name")
        repos.append({
            "rank": r.get("rank"),
            "full_name": fn,
            "url": f"https://github.com/{fn}",
            "trendshift_url": r.get("trendshift_url") or (f"{BASE}/repositories/{r['repository_id']}" if r.get("repository_id") else None),
            "description": (r.get("repository_description") or "").strip(),
            "language": r.get("repository_language") or r.get("language"),
            "stars": r.get("repository_stars"),
            "stars_gained": r.get("repository_stars_gained"),
            "forks": r.get("repository_forks"),
            "trend_score": r.get("score"),
            "tags": [t.get("slug") or t.get("name") for t in (r.get("tags") or [])],
            "created_at": r.get("repository_created_at"),
            "mentions": r.get("social_mention_platforms") or [],
        })
    return repos, source


# ---------------------------------------------------------------- GitHub
def verify_github(repos: list[dict], pause: float = 0.2) -> None:
    """เติม/ตรวจดาวจริงจาก GitHub REST API (ใช้ GITHUB_TOKEN ถ้ามี; ไม่มีก็ได้ 60 ครั้ง/ชม.)"""
    headers = {"Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    for r in repos:
        status, body, hdr = http_get(f"https://api.github.com/repos/{r['full_name']}", headers)
        if status == 200:
            g = json.loads(body)
            r["github_stars"] = g.get("stargazers_count")
            r["owner_type"] = (g.get("owner") or {}).get("type")
            r["license"] = ((g.get("license") or {}).get("spdx_id"))
            r["archived"] = g.get("archived")
            r["fork"] = g.get("fork")
            r["homepage"] = g.get("homepage") or None
            r["github_topics"] = g.get("topics") or []
            if r.get("stars") is None:
                r["stars"] = r["github_stars"]
            if g.get("full_name") and g["full_name"] != r["full_name"]:
                r["renamed_to"] = g["full_name"]
        else:
            r["github_error"] = status
            if status in (403, 429) and hdr.get("X-RateLimit-Remaining") == "0":
                print("⚠️ GitHub API rate limit เต็ม — ตั้ง GITHUB_TOKEN แล้วรันใหม่", file=sys.stderr)
                break
        time.sleep(pause)


# ---------------------------------------------------------------- scoring
def is_ai(r: dict) -> bool:
    if AI_TAGS.intersection(r.get("tags") or []) or AI_TAGS.intersection(r.get("github_topics") or []):
        return True
    return bool(AI_WORDS.search(f"{r['full_name']} {r.get('description', '')}"))


def content_fit(r: dict) -> tuple[int, list[str]]:
    """คะแนนความเหมาะกับคอนเทนต์ BoomBigNose (0-100) + เหตุผลสั้นๆ"""
    score, why = 0, []
    stars = r.get("github_stars") or r.get("stars") or 0
    if is_ai(r):
        score += 35; why.append("AI/เครื่องมือ AI")
    if stars >= 10_000:
        score += 30; why.append("ดาว ≥10k")
    elif stars >= 3_000:
        score += 15; why.append("ดาว ≥3k")
    if r.get("owner_type") == "Organization":
        score += 15; why.append("เจ้าของเป็นองค์กร")
    if r.get("license") and r["license"] not in ("NOASSERTION",):
        score += 10; why.append(f"license {r['license']}")
    if (r.get("stars_gained") or 0) >= 1000:
        score += 10; why.append("ดาวพุ่งแรง")
    if r.get("archived") or r.get("fork"):
        score -= 40; why.append("archived/fork")
    if re.search(r"[\u4e00-\u9fff]", r.get("description", "")) and not is_ai(r):
        score -= 10
    return max(0, min(100, score)), why


def giveaway_ready(r: dict) -> bool:
    stars = r.get("github_stars") or r.get("stars") or 0
    return stars >= 10_000 and is_ai(r) and not r.get("archived") and not r.get("fork")


# ---------------------------------------------------------------- output
def fmt_n(n) -> str:
    return "-" if n is None else f"{n:,}"


def to_markdown(repos: list[dict], period: str, fetched: str, source: str) -> str:
    out = [f"# Trendshift {period} — ดึงเมื่อ {fetched} (เวลาไทย)", "",
           f"แหล่ง: {BASE}{PERIOD_PATH[period]} (อ่านจากหน้าเว็บสาธารณะ, parser={source}); ดาวตรวจกับ GitHub API ถ้ามีคอลัมน์ GitHub ⭐", "",
           "| # | Repo | ภาษา | ⭐ Trendshift | GitHub ⭐ | +⭐ ช่วงนี้ | Fit | แจก GitHub? | คำอธิบาย |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in repos:
        desc = (r.get("description") or "").replace("|", "/")[:110]
        out.append(f"| {r['rank']} | [{r['full_name']}]({r['url']}) | {r.get('language') or '-'} | {fmt_n(r.get('stars'))} | "
                   f"{fmt_n(r.get('github_stars'))} | {fmt_n(r.get('stars_gained'))} | {r['fit']} | {'✅' if r['giveaway_ready'] else '—'} | {desc} |")
    out += ["", "Fit = คะแนนความเหมาะกับคอนเทนต์ BoomBigNose (AI +35, ดาว≥10k +30, องค์กร +15, มี license +10, ดาวพุ่ง +10)",
            "แจก GitHub? ✅ = ผ่านเกณฑ์ขั้นต้น (AI + ดาว ≥10k + ไม่ใช่ fork/archived) — ยังต้องเช็กว่าเป็น official และไม่ซ้ำกับที่เคยแจก"]
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="ดึง repo ที่กำลังเทรนด์จาก Trendshift.io สำหรับหาไอเดียคอนเทนต์")
    ap.add_argument("--period", choices=PERIOD_PATH, default="daily", help="daily (ค่าเริ่ม) / weekly / monthly / yearly")
    ap.add_argument("--limit", type=int, default=25, help="จำนวนสูงสุดที่แสดง (Trendshift ให้ 25 ต่อหน้า)")
    ap.add_argument("--language", help="กรองภาษา เช่น Python, TypeScript (ไม่สนตัวพิมพ์)")
    ap.add_argument("--min-stars", type=int, default=0, help="ดาวขั้นต่ำ (ใช้ดาว GitHub ถ้า --verify)")
    ap.add_argument("--tag", action="append", help="กรอง tag ของ Trendshift เช่น ai-agent (ใส่ซ้ำได้)")
    ap.add_argument("--ai-only", action="store_true", help="เอาเฉพาะ repo สาย AI")
    ap.add_argument("--giveaway", action="store_true", help="เอาเฉพาะที่ผ่านเกณฑ์แจก GitHub ขั้นต้น (บังคับ --verify)")
    ap.add_argument("--exclude-file", help="ไฟล์รายชื่อ owner/repo ที่เคยใช้แล้ว (บรรทัดละ 1 หรือ JSON) เพื่อตัดซ้ำ")
    ap.add_argument("--verify", action="store_true", help="ตรวจดาว/เจ้าของ/license กับ GitHub API")
    ap.add_argument("--sort", choices=["rank", "fit", "stars"], default="rank")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--json", action="store_true", help="พิมพ์ JSON")
    g.add_argument("--md", action="store_true", help="พิมพ์ตาราง Markdown (ค่าเริ่ม)")
    ap.add_argument("-o", "--output", help="บันทึกลงไฟล์แทน stdout")
    a = ap.parse_args(argv)

    if a.giveaway:
        a.verify = True
    fetched = datetime.now(BKK).strftime("%Y-%m-%d %H:%M")
    repos, source = fetch_trendshift(a.period)

    if a.exclude_file:
        txt = open(a.exclude_file, encoding="utf-8").read()
        used = {m.lower() for m in re.findall(r"[\w.-]+/[\w.-]+", txt)}
        repos = [r for r in repos if r["full_name"].lower() not in used]
    if a.language:
        repos = [r for r in repos if (r.get("language") or "").lower() == a.language.lower()]
    if a.tag:
        want = {t.lower() for t in a.tag}
        repos = [r for r in repos if want.intersection(r.get("tags") or [])]
    if a.ai_only:
        repos = [r for r in repos if is_ai(r)]
    if a.verify or source == "jsonld":
        verify_github(repos)
    if a.min_stars:
        repos = [r for r in repos if (r.get("github_stars") or r.get("stars") or 0) >= a.min_stars]
    for r in repos:
        r["fit"], r["fit_reasons"] = content_fit(r)
        r["giveaway_ready"] = giveaway_ready(r)
    if a.giveaway:
        repos = [r for r in repos if r["giveaway_ready"]]
    if a.sort == "fit":
        repos.sort(key=lambda r: (-r["fit"], r["rank"] or 999))
    elif a.sort == "stars":
        repos.sort(key=lambda r: -(r.get("github_stars") or r.get("stars") or 0))
    repos = repos[: a.limit]

    if a.json:
        text = json.dumps({"source": BASE + PERIOD_PATH[a.period], "period": a.period, "parser": source,
                           "fetched_at_bkk": fetched, "count": len(repos), "repos": repos},
                          ensure_ascii=False, indent=2) + "\n"
    else:
        text = to_markdown(repos, a.period, fetched, source)
    if a.output:
        with open(a.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"บันทึก {len(repos)} repo → {a.output}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
