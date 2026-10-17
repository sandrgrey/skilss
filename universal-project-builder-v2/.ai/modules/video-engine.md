# Video and Media Engine

## Inventory and rights
List files, origin, role, dimensions, codec, duration, filesize, poster and license/permission. Download only user-authorized assets. Serve assets locally or from a controlled CDN; never make an author's private asset archive your production hotlink.

## Scroll-scrubbing video
Translate scene progress into target media time. Video `currentTime` seeking is asynchronous and dependent on keyframe interval, decoding and browser/device constraints. Avoid assuming that every `requestAnimationFrame` can decode a new video frame.

- Wait for `loadedmetadata` and a finite positive duration.
- Clamp seek targets; skip tiny/no-op seeks; avoid huge seek backlogs.
- For interactive scrub, consider quick-seeking/keyframe-optimized assets or image sequences; evaluate costs empirically.
- Control preload policy and decode memory; pause or suspend processing when offscreen.
- Handle failure, unseekable streams, reduced motion, mobile bandwidth constraints and fallback poster.
- Clean up animation frames, listeners, observers and references.

## Multi-clip seams
Maintain clip-independent seek mapping and a single global progress value. For `seam=0.5`, clip A maps `p/seam`, B maps `(p-seam)/(1-seam)`; clamp both to 0…1.

Crossfade over a narrow band where corresponding frames visually align. `crossfadeMix(progress, seam, halfWidth)` computes the B opacity. A crossfade is **not** a guaranteed seamless join; inspect actual frames at and near seam and reverse scrolling.

## Validation
Cold load, delayed media, error fallback, fast scroll, fast reverse scroll, pause/tab background, mobile, reduced motion; record evidence, not assumptions.
