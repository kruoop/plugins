---
name: visual-procedural-guides
description: "Use when creating screenshot-led step-by-step guides."
---


## Host integration

Resolve sibling skills from this bundle first. For browser control, read the sibling ego-browser skill (or its installed user-wide copy) and use ego-browser CLI with TaskSpace. Map tool names to the tools actually available in Claude Code or Codex; examples do not grant permissions. Resolve runtime paths on the current host rather than treating imported paths as proof of installation. Preserve current user authorization for external writes; installing this bundle starts no generation, upload, post, watcher or episode.

# Visual Procedural Guides

Create polished, verifiable step-by-step guides whose screenshots are part of the deliverable rather than incidental evidence. This skill governs guides for registration, onboarding, setup, and other UI workflows.

## Trigger

Use when the user asks for a manual, walkthrough, onboarding document, or registration guide—especially when they request screenshots, screen captures, PDF/Word delivery, or localized text.

## Core Workflow

1. **Inspect the authoritative source.** Confirm the official URL, eligibility, prerequisites, dates, limits, support contacts, and any downloadable official manual. Cite official pages in the artifact.
2. **Map the workflow before capturing.** List the user-visible stages and decide which require a live screenshot. Capture the landing page, entry point, and every public stage that materially helps the reader.
3. **Save each capture immediately.** Copy every screenshot to a stable, descriptive filename before taking the next capture; temporary screenshot paths are commonly reused or overwritten.
4. **Respect identity boundaries.** Do not perform or claim completion of login, password, OTP, consent, payment, or identity-verification steps on the user's behalf unless explicitly authorized and safely supported. For inaccessible later stages, use screenshots from official documentation and label them as official examples.
5. **Write for action.** For each step include: what to click, what the user should see, what information is required, and the next expected state. Keep screenshots adjacent to the relevant instruction and add captions.
6. **Deliver editable and distribution formats.** Prefer DOCX plus PDF when the user has not specified one. Preserve source screenshots and the official manual alongside the outputs when useful.
7. **Verify the files.** Validate DOCX package health and structure. Check PDF metadata/page count, rasterize every page, and visually inspect legibility, clipping, page breaks, captions, and screenshot scale.
8. **Report scope honestly.** State whether you produced a guide, completed a registration, or stopped before a protected step. Never blur those outcomes.

## Screenshot Standards

- Use one stable filename per state, such as `01-home.png`, `02-sign-in.png`, and `03-consent.png`.
- Capture the full page or viewport for context; add a crop only as a supplementary close-up.
- Distinguish captions: `ภาพหน้าจอจริง` for live captures and `ตัวอย่างจากคู่มือทางการ` for official-document images.
- Avoid screenshots containing passwords, OTPs, personal identifiers, or unrelated windows.
- If a cookie panel obscures an important control, capture again after handling only the non-sensitive cookie choice allowed by the task.

## Complex-Script PDF Rule

For Thai and other shaping-sensitive scripts, prefer browser-rendered HTML/CSS to direct ReportLab text rendering. A font containing the glyphs is not sufficient: combining marks can still be misplaced or rendered as dotted circles. Follow `references/non-latin-pdf-and-screen-capture.md`.

## Artifact Quality Checklist

- [ ] All requested screenshots are actually embedded in the final artifact.
- [ ] Live captures and official examples are labeled distinctly.
- [ ] Prerequisites, dates, limitations, and support contacts match the authoritative source.
- [ ] No credentials, OTPs, or personal identifiers appear in screenshots.
- [ ] DOCX opens and passes structural validation.
- [ ] Every PDF page has been rasterized and visually reviewed.
- [ ] Thai/complex-script combining marks render correctly.
- [ ] Final message links every requested file and describes what was—and was not—completed.

## Pitfalls

- **Writing the guide before capturing screens.** The user may specifically expect visual evidence; capture first and build around it.
- **Reusing a temporary screenshot path.** Later captures overwrite earlier ones. Save distinct copies immediately.
- **Using live screenshots for protected stages.** Login and identity verification belong to the account owner; use official examples when needed.
- **Assuming text extraction proves visual correctness.** A PDF can extract correct Thai text while displaying broken marks. Rasterize and inspect.
- **Treating a generated artifact as verified.** Validate package structure and inspect rendered pages before delivery.
- **Saying “registered” when only a guide exists.** Report the actual side effect precisely.

## Supporting Material

- `references/non-latin-pdf-and-screen-capture.md` — validated HTML-to-PDF path, screen-capture provenance, and visual verification steps.
