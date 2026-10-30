# Web-ready screenshot guide workflow

Use this variant when the user intends to publish the guide on a website.

## Deliverable shape

- Package `index.html` with a relative `assets/` directory; also ship a ZIP containing both.
- Keep CSS and small JavaScript inline unless the user asks for a framework or separate asset pipeline.
- Include semantic headings, alt text, responsive navigation, print styles, and visible source links.
- Preserve original screenshots with stable names; use lazy loading only below the fold.

## Research hierarchy

1. Treat official pages, official FAQs, policies, and downloadable manuals as the authority for eligibility, dates, limits, privacy, quotas, and support contacts.
2. Use reputable secondary reporting only to add practical details (for example, unsupported browser modes or estimated timing).
3. Attribute secondary details explicitly and list all sources in the artifact.
4. If sources disagree on model names or fast-changing figures, cite the official current page or describe the category without choosing an unsupported value.

## Verification

1. Serve the folder over local HTTP rather than testing only with `file://`.
2. Check desktop and a narrow mobile viewport (about 390 px).
3. Assert `document.body.scrollWidth <= innerWidth` on mobile.
4. Scroll through the page so lazy images load, then confirm every `img[src]` has `naturalWidth > 0`.
5. Check all internal `#anchor` links resolve to an existing element.
6. Confirm key external links return successfully where network access permits.
7. Rebuild the ZIP after the final patch, not before.

## Content depth

When a first-pass guide is judged too brief, expand the artifact itself with prerequisites, expected screen states, decisions, privacy/safety notes, troubleshooting, post-registration behavior, FAQs, contact information, and source notes. Do not answer with extra prose while leaving the downloadable artifact unchanged.
