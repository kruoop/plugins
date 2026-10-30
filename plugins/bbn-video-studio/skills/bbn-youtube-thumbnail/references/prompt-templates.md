# Editable thumbnail prompts

Resolve variables and attach inspected images before each call. Produce one image per prompt. These templates create new work for the current topic; Claude/Ponytail are only the bundled style example.

## Variables

| Variable | Fill with |
| --- | --- |
| `TOPIC` | Current video topic and supported takeaway |
| `HEADLINE_1`, `HEADLINE_2` | Exact short Thai headline lines readable in 3 seconds (line 1 topic, line 2 benefit ~3–5 words); example: โค้ดน้อยลง / งานยังครบ only when supported |
| `ALT_HEADLINE_1`, `ALT_HEADLINE_2` | A second truthful hook, or reuse the same headline for a layout comparison |
| `BRAND_A`, `BRAND_B` | Exact current product names; use one brand if the topic needs only one |
| `LOGO_A`, `LOGO_B` | Inspected genuine attached logos, with source recorded locally |
| `PORTRAIT` | User-selected real portrait for variants that include a presenter |
| `STYLE_REFERENCE` | Bundled assets/style-reference-no-presenter.png, style/layout only |
| `RELATION` | Relationship actually supported by the video, such as “+”; do not imply a partnership |
| `OUTPUT_SIZE` | Requested landscape size, normally 1920 × 1080; verify actual output afterward |
| `ALT_PRESENTER_RULE` | Either “Use attached PORTRAIT as a smaller lower-right presenter, preserving identity and natural skin” or “Include no presenter photography” |

If a logo or portrait is omitted, remove its instructions and rebalance the layout before generation. Do not leave unresolved variables or request nonexistent attachments. Real input examples can be a user-supplied `Claude.png` and, for a Ponytail topic, the official repository asset at https://github.com/DietrichGebert/ponytail/raw/main/assets/logo-dark.png; inspect the current file before use. These are examples, not mandatory brands or bundled logo sources for every task.

## 1. Presenter and logos

```text
Create ONE finished YouTube thumbnail for TOPIC, requested OUTPUT_SIZE, landscape 16:9. Use the attached STYLE_REFERENCE only for its premium dark graphite mood, dimensional tiles and bold Thai hierarchy. Make an original composition for this topic; replace all reference brands and wording.

Use attached PORTRAIT as the real presenter on the right, with a large recognizable face, natural skin color, authentic facial proportions and a clean silhouette. Preserve identity and a natural confident expression; avoid yellow skin or a generic invented face. Place genuine LOGO_A and LOGO_B as large recognizable dimensional dark tiles across the upper-left/middle, preserving the exact logo artwork and proportions. Add the supported RELATION between them and small correctly spelled labels BRAND_A and BRAND_B. If only one logo is supplied, make that single logo the hero without inventing a second brand.

Set exactly two large Thai headline lines below the tiles, clear of the face:
HEADLINE_1
HEADLINE_2
Use clean bold white for the first line and vivid flat yellow emphasis on the second with a single yellow underline. Preserve all Thai vowels and tone marks. Dark graphite background, restrained relevant code texture, subtle tile edge lighting, readable separation and breathing room. Tile depth may be dimensional; typography stays modern, not gold or ornate.

The image should communicate the supported takeaway immediately at small thumbnail size. No unverified numbers, fake benchmark UI, extra slogans, watermarks or unrelated decoration. Keep all important content inside the canvas. Produce one thumbnail, not a grid or a comparison sheet.
```

## 2. Matching version without presenter photography

```text
Create ONE finished YouTube thumbnail for TOPIC, requested OUTPUT_SIZE, landscape 16:9. It is the matching no-presenter-photo version of the dark premium concept. Use attached STYLE_REFERENCE for mood and hierarchy only; replace its brands and text with this topic. Do not include a photographic person, human body, presenter cutout or substitute avatar. A human-faced illustration already present in a required genuine logo must remain intact: it is brand artwork.

Make attached genuine LOGO_A and LOGO_B the large central heroes on dimensional dark graphite tiles, with subtle controlled edge lighting and a supported RELATION between them. Preserve exact logo identity and aspect ratios. Put small correctly spelled labels BRAND_A and BRAND_B below the corresponding tiles. If only one genuine logo is supplied, center it and remove the extra tile and relation.

Set the exact two-line Thai headline prominently below the logo pair:
HEADLINE_1
HEADLINE_2
The first line is bold white; the second uses flat vivid yellow emphasis with one yellow underline. Maintain correct Thai combining marks, generous margins and very high small-size readability. Rebalance the space freed by removing the presenter; do not leave an empty portrait-shaped gap.

Keep a premium dark graphite background with faint relevant code/tech texture and clean separation. Use an original composition inspired by the reference, not a replica. No unverified percentages, fabricated proof, extra text, watermarks or unrelated objects. Do not use a light background. Produce one complete thumbnail, not multiple panels.
```

## 3. Alternate hook or layout, same dark family

```text
Create ONE alternate YouTube thumbnail for TOPIC, requested OUTPUT_SIZE, landscape 16:9. Retain the premium dark graphite, dimensional logo tiles and white/yellow Thai typography of attached STYLE_REFERENCE. Create a clearly different original layout, not a light-background variation. Replace every example brand and phrase with this topic's supplied assets and text.

Use a strong diagonal visual flow: place genuine LOGO_A and LOGO_B in two large staggered tiles on the right, preserving exact artwork, proportions and recognizable brand colors. Use the supported RELATION only if needed; small labels must read BRAND_A and BRAND_B accurately. With one supplied logo, use a single large tile. Place the alternate headline as the main block on the left, exactly:
ALT_HEADLINE_1
ALT_HEADLINE_2
Use bold clean white supporting type, flat yellow emphasis and a single energetic yellow underline. Keep all Thai glyphs intact. Leave adequate space between the headline and logos.

ALT_PRESENTER_RULE. If a presenter is included, keep the original person's facial proportions and natural neutral skin tone, clear of text and logos; never replace the subject with an invented person. If omitted, preserve any required illustrated logo face.

Subtle relevant tech texture and restrained depth should support a single clear takeaway. Avoid gold ornate lettering, busy decoration, fake results, unverified numeric claims, extra text and watermarks. Keep the alternate hook faithful to the supplied facts. Produce one finished thumbnail with safe margins and readable small-size hierarchy.
```

The generator's returned dimensions may differ from OUTPUT_SIZE. Inspect the saved file and report its actual size, then review text, logos, portrait and layout before delivery.

## 4. Conditional hero logo and result screens

Use this alternative when the current brief calls for a result-led hero composition or explicitly adopts the supplied **Design King** direction. It replaces the layout of a requested variant; it does not add an unrequested fourth thumbnail or change the saved portrait/count defaults. It can use one short headline rather than forcing the two-line templates above.

The user-supplied reference inspected on 2026-09-10 has an oversized white “Design King” headline at the top, a central tilted orange Claude tile with a crown, and four angled website screenshots receding around it on a near-black background. Overlap, perspective, shadow and small warm impact highlights create depth. These are observed composition features, not evidence that the displayed sites are the current episode's results. The crown, sparks and exact arrangement are optional motifs; do not copy the reference's wording, websites or artwork into unrelated work. Its **16:13** badge, rounded screenshot frame and white outer margin are YouTube/screenshot chrome and must be excluded.

Resolve these extra inputs: `SHORT_HEADLINE` (one truthful brief phrase), `HERO_LOGO` (genuine inspected product artwork), `RESULT_SCREENS` (a small set of actual current-project results, with source frames/files recorded), and `PRESENTER_RULE` (the requested real portrait treatment or no presenter). If real result screenshots are unavailable, use a different supported layout; do not invent evidence. Attach each screen as a real-content input, not a style reference. Crop to the useful result and omit browser/player chrome unless a relevant application control is part of the result itself.

```text
Create ONE original YouTube thumbnail for TOPIC, requested OUTPUT_SIZE, landscape 16:9. Use the supplied Design King reference only for hierarchy and depth: a very short oversized headline above a central hero and a few receding result screens. Retain the BBN premium dark graphite/near-black family and clean white type with restrained flat yellow emphasis. The exact headline is:
SHORT_HEADLINE
Make it readable at small size; preserve Thai tone marks and vowels. Do not add the words Design King unless they are explicitly the current chosen headline.

Make attached HERO_LOGO the clear central focal point, preserving the genuine mark, colors and proportions. Build dimensional separation with a restrained supporting surface, shadow and light; do not redraw the mark or invent a 3D replacement logo. If a standalone transparent Claude mark is requested, use that exact alpha PNG without an opaque app tile, white rectangle or fake transparency pattern. Keep its silhouette readable against the dark background.

Arrange the attached real RESULT_SCREENS around and behind the hero in a balanced shallow perspective. Use overlap, scale, soft shadow and edge lighting for depth, while retaining enough of each genuine screen to recognize the supported outcome. Do not synthesize different results, fake interface text or copy the reference's example websites. Let the hero and short headline dominate; keep screens secondary and avoid a collage of tiny unreadable claims.

PRESENTER_RULE. Preserve the exact real portrait identity and natural skin if included. If polished supporting 3D AI imagery is specifically requested, keep it secondary and cohesive in material, lighting and scale, clearly illustrating the idea; it must not replace genuine logos, actual UI evidence or the selected person. Avoid childish flat emoji mixtures and unrelated toys. A crown or impact spark is optional only if it supports the chosen concept; no ornate gold lettering or gratuitous debris.

Keep safe margins, readable separation and an original arrangement. No YouTube duration badge, play icon, progress bar, player controls, white screenshot margins, copied rounded screenshot border, watermarks or extra slogans. Produce one finished thumbnail, not a contact sheet.
```

Inspect the actual output at full and thumbnail size for headline dominance, genuine logo fidelity, source-screen integrity, real portrait identity when requested, and absence of player chrome. A rendered background that looks transparent is not an alpha asset; separately verify the supplied standalone PNG's alpha before composition.

