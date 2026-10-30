# Thai Caption + Inline Emoji Recipe

Use this when a pre-cut 9:16 Short needs only an opening Thai caption and a color emoji, while preserving the source edit.

## Proven composition

1. Lock the pre-cut source: do not change shots, timing, crop, audio, or duration.
2. Render each Thai text line with Pango/HarfBuzz (or CoreText/browser shaping), not Pillow text rendering. A valid Unicode source string does not prove the visible combining marks are correct.
3. Render text to transparent RGBA, crop to the alpha bounds, and add contrast with an alpha-mask outline if needed.
4. Use a canonical color emoji PNG/JPG. Remove only its known background, resize it independently, and composite it after the final punctuation.
5. Measure the second-line text and emoji as one group:
   - `group_width = text_width + gap + emoji_width`
   - center the group, not the text alone;
   - reject or uniformly reduce both line sizes if the group crosses safe margins.
6. Composite the overlay only for the measured opening interval. Set output duration explicitly to the source duration.

## Font resolution and yellow emphasis

1. Resolve the approved family and weight separately with Fontconfig, for example `fc-match -f '%{family}|%{style}|%{file}\n' 'Noto Sans Thai:style=Bold'` when that family is authorized. Inspect the returned family and file: a successful command may silently return a fallback. Do not treat an unstructured family-plus-weight query as proof of font identity.
2. Shape the entire caption in one Pango layout. Escape text for markup, then wrap only the emphasized words in `<span foreground="#ffde3c" underline="single">…</span>` and render using `pango-view --no-display --pixels --markup --foreground=white --background=transparent` with the approved `--font`, `--text` and `--output` values.
3. Preserve that rendered RGBA layer when applying the outline and translucent backing. Do not redraw the highlighted word as a separately cropped image positioned using the prefix width: independent alpha trims and shaping can shift its baseline or detach Thai marks.
4. Measure the whole shaped phrase against safe margins, then inspect the encoded frame at full resolution. Keep the approved font size; split phrases at natural boundaries rather than shrinking individual long captions.

## Literal QA

Inspect both the transparent overlay and a frame extracted from the encoded MP4. Confirm:

- Thai vowels and tone marks are visibly present and attached to the intended consonants;
- brand tokens such as `n8n` are exact;
- punctuation order is exact, e.g. `ในคลิกเดียว!` followed by the emoji;
- emoji is color, not a font fallback, and is not clipped;
- neither caption nor emoji obstructs the host’s eyes or central face;
- the encoded duration, frame size, codecs, and audio match the intended source.

## Delivery semantics

`Make EPxxx_short` means produce and deliver the review MP4. It does not mean create a YouTube Studio draft. If the user requests a Drive link, upload/update only the review artifact, then read back the file ID and size/checksum before returning the link. Publishing still requires separate item-specific approval.
