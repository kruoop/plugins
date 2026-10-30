# Reference-led overlay revisions

Use this when a user supplies a screenshot and names one overlay element to correct.

## 1. Freeze the accepted state

Record the current accepted values for:

- source cut, duration, crop, and audio;
- caption copy and punctuation;
- font family, weight, nominal size, outline, horizontal scale, and line positions;
- emoji asset, size, order, and position;
- overlay appearance interval.

Only fields explicitly named in the correction become editable.

## BBN reference discovery before rebuilding an overlay

Inspect an actual encoded prior Short and its renderer before applying the BBN template; a logo-only derivative rejected by the owner is not the accepted reference. For the established EP205/EP213 composition, local reference files are `Desktop/FB-AutoPost/artifacts/EP205-short/qa/EP205_short_readback_final.mp4`, its `build_overlay.py`, and `Desktop/youtube/EP213/short_overlay_review/render_short.py`. Verify these remain available and inspect real frames rather than trusting these paths alone. The measured treatment uses 350px upper logo boxes at y=170, Pango-rendered Noto Sans Thai SemiBold 110 with dark outline, caption lines at y=755/895, and an opening interval ending at 6.5s. These are reference values, not permission to override a newer user correction. When two large logos and a caption are explicitly requested, preserve the caption treatment and center the combined logo group; do not substitute tiny middle-of-frame logos or omit the caption.

## Explicit full-face opening → half-layout correction

When the owner explicitly asks to open half/half so the usual text + icon can fit, reframe the actual synchronized opening host into the lower half and restore the established large centered upper icon plus headline/emoji. Do not fall back to a small corner logo or treat the earlier full-face framing as immutable after this correction. Inspect actual prior encoded references and reuse their renderer; end the revised opening at its original cut, not the reference's unrelated duration. Preserve baked spoken subtitles at readable native size (retain their original strip when cropping would remove them), distinguish a replaced static title from spoken captions, and inspect encoded first/late-opening/both-cut-boundary frames. Never generate a face or stretch the host to fill the region.

## Official asset retrieval when the channel library has no match

Inventory the channel's logo folder first. If the needed mark is absent, retrieve the brand's canonical logo page and use the actual linked asset, not an image-search recreation. For Blender, `https://www.blender.org/about/logo/` links to the branding kit and `https://download.blender.org/branding/blender_logo_socket.png`; the socket variant retains its official white backing. Preserve that supplied backing and aspect ratio when the owner requests the original-background treatment.

If a Python HTTP request is rejected, retry the same public canonical page with native `curl -fL --max-time 30 -A 'Mozilla/5.0' URL -o FILE`, then extract its linked assets locally. Inspect the downloaded image before composing and record the canonical asset URL in the existing review record. A wide wordmark needs a proportional width-based box, not stretching into the previous square icon's dimensions.

## Evidence-preserving preflight for a new episode

1. Reuse the accepted renderer's shaping, outline and emoji functions, but probe the current source for its own duration/frame count and inspect its opening before copying coordinates. Treat episode paths, source hashes, logo identity, caption text, timing and expected media properties as explicit per-item values; check them together before running a copied script.
2. Inspect full-resolution frames throughout the proposed opening interval. Mark the bounds of baked demonstration/model labels and section captions, not just the face and subtitles; small lower-corner labels can be hidden by an otherwise clean headline.
3. Composite a preview over those source frames before the full encode. Keep new headline/emoji alpha bounds outside the marked regions and keep the original logo background/aspect ratio. For a newly composed opener, move or compact only the new overlay within the permitted design scope; do not shrink locked typography to conceal a collision.
4. End the overlay before tables or other dense evidence appear. Preserve all source chart labels, values, footnotes and spoken caveats; neutral comparison copy is preferable to an unsupported winner claim.
5. Inspect an actual encoded opening and both sides of the overlay boundary. If a collision requires a rerender, archive the prior local candidate and its QA frames together so the final evidence cannot accidentally refer to the rejected layout. Repeat frame-count, duration, full-decode and copied-audio-hash checks on the final file.

## 2. Measure the named element

For a two-logo row, measure against the visible video canvas rather than the screenshot's outer border:

- combined row width as a percentage of canvas width;
- each logo box width/height;
- gap between logos;
- group center X;
- row Y and the vertical gap to the first caption line.

Compute placement as one group:

```text
group_width = logo_a_width + gap + logo_b_width
group_x = (canvas_width - group_width) / 2
logo_a_x = group_x
logo_b_x = group_x + logo_a_width + gap
```

Do not center each logo independently. Preserve each asset's aspect ratio and official appearance.

## 3. Typography correction rule

Thai combining-mark failure is a shaping problem, not a font-size problem. Keep the accepted font/style locked and render with Pango/HarfBuzz, CoreText, or browser text shaping. Inspect the rasterized word and an encoded video frame at full resolution. For inline punctuation plus a composited emoji, verify literal order such as `เดียว!` followed by the emoji asset.

## Transparent-icon replacement without typography drift

1. Inspect the latest owner-supplied icon and rejected encoded frame first. Distinguish exterior white matte from intentional interior white artwork and a colored rounded-square backing. For exterior-border removal, preserve that exact variant rather than choosing a different bare transparent mark from the library. Use an existing transparent asset only if its artwork matches the supplied icon. Check alpha extrema and composite over contrasting backgrounds and the actual video; alpha alone does not rule out a white halo.
   - When no exact transparent asset exists, reuse an edge-connected flood-fill matte remover: seed the image perimeter, make only connected exterior-background pixels transparent, and preserve enclosed white symbols. Never globally remove all white pixels. Inspect JPEG/antialiased boundary pixels and tune the background criterion to this asset; a near-white-only threshold can leave a visible pale fringe, while a copied aggressive threshold can eat light brand colors. Assert transparent outside corners and unchanged opaque interior artwork, then inspect the encoded edge at full resolution. Keep the original file and save a derivative.
2. Reuse the latest overlay raster and replace only its verified logo rectangle when that rectangle does not intersect captions or other graphics. Otherwise rebuild only the separate logo layer. Preserve the headline and emoji rasters rather than rerendering text for a logo-only request.
3. Assert equality of RGBA pixels outside the changed logo rectangle. Keep the existing logo box, centering and appearance interval unless the owner also requested placement or size changes; resize the new asset proportionally without adding a backing tile or outline.
4. Render from the verified source with the same composition settings, stream-copy the unchanged AAC, and compare its extracted hash with the previous review. Inspect the encoded icon for white edges and carry forward any listening/motion checks still pending; byte-identical audio is not a new listening review.

## 4. QA the narrow revision

Compare before/after frames and verify:

- only the requested element changed;
- combined logo group is centered and matches reference scale;
- no logo clipping, caption overlap, face obstruction, or platform-UI conflict;
- caption typography, punctuation, emoji, crop, timing, and audio remain unchanged;
- encoded MP4 passes full decode and retains expected dimensions/duration;
- remote review file is read back with matching size/checksum before reporting the link.
