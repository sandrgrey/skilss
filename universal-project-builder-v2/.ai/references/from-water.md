# Water.pdf / Marlin — source-derived principles and limitations

**Source:** uploaded Water.pdf, 29 pages, “Marlin — Scroll-Choreographed Jetski Site Rebuild Prompt.” This file records what the provided document states and what UPB v2.0 independently recommends. It does **not** include the original source files or video assets.

## Confirmed from the PDF's written source

1. **Purpose** (pp. 1–2): one-page electric jetski promo: scroll drives a scene rather than conventional page movement. The source features hero headline, moving content groups, four cards, two 10-second videos and a footer.
2. **Stack** (pp. 2–5): React 19, Vite 6, TypeScript, Tailwind v4 plugin, `motion/react`, Anybody and Manrope fonts. The PDF says 'pinned versions' but package.json uses caret (`^`) semver ranges: these are not exact locks.
3. **Media** (pp. 3–4): seven external assets — 2 videos, 4 card stills, 1 poster. The archive is not part of the PDF. License/availability should not be assumed. Its URL is intentionally not copied into this kit.
4. **Artboard** (pp. 1–2 and 7–10): 1440×810 fixed stage; elements positioned in design pixels; scale = viewportWidth / 1440; anchored top-left. Sticky frame height = max(100vw × 810/1440, 100vh); viewport chrome outside stage.
5. **Scroll clock** (pp. 21–23): TOTAL_MS=20000; SCROLL_VH=620; phases represented as fractions of TOTAL_MS. Source describes 19 interactions; key phase constants in JSON preset.
6. **Three group offsets** (pp. 21–23): g53 186→−774, g54 1050→105→−1115, g55 1400→740→144. Separate vertical moves produce parallax filmstrip.
7. **Easing** (pp. 22–23): `ramp` linear, `span` cubic ease-out `1 − (1 − t)^3`, and linear interpolation `lerp`.
8. **Video seam** (pp. 7–10, 21–23): `VIDEO_SEAM=0.5`, crossfade 0.02 progress each side. Video A/B targets seek toward wanted time every requestAnimationFrame using 0.26 easing factor, threshold 0.012 seconds; nudge to 0.01 after metadata.
9. **Content** (pp. 13–19): staggered heading/body, animated percentage stats, four cards, deep-water scene. `Footer.tsx` (pp. 23–28) is in normal responsive flow, unlike fixed artboard.
10. **Source design** (pp. 19–21): near-black #0b1016, volt #d8f24a. Anybody substitutes commercial PP Monument Extended; Manrope substitutes Quatro.

## Not source-derived: UPB v2 engineering recommendations

- Use a mobile-specific layout when width scaling renders body text unreadable. Source's width-lock is deliberate, not universally responsive.
- Fix source's inline `display: 'flex'` overriding `.nav-links { display: none }` at ≤640px.
- Implement actual actions for decorative nav/CTA elements, form submission logic, and error states. These are not in the reference site code.
- Avoid continuous dual-video seeking where profiling shows decoding stalls; consider keyframe/image sequence alternatives and visibility management.
- Maintain modular architecture, source trust rules, security checks and explicit test evidence.

## Fidelity caveats

The PDF claims “byte-identical rebuild” and “pixel-for-pixel the original” while internally describing modified layout choices (e.g., underwater text repositioned to prevent clipping, pp. 18–19) and font substitutions. Treat these as claims in a prompt, **not evidence of verified identity**. The full site has not been reconstructed or browser-tested by this kit.

## Preset mapping

Read `.ai/references/marlin-timeline.json` for reusable numeric reference. Import `.ai/references/motion-core.mjs` for portable progress math. Neither is a substitute for obtaining licensed videos or for an actual site implementation.
