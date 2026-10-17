# Cinematic Engine — normalized timelines and scroll choreography

Use only when the brief calls for immersive scenes, motion references, or video-driven narratives. **Never require it for every app.**

## Common clock
Represent visual progress as `p ∈ [0,1]`. Its origin may be normalized page scroll, a playback clock, a gesture or app state. Each animation uses explicit phase windows and easing independent of UI framework.

Core helpers: `clamp`, `lerp`, `ramp`, `span`, `staggerWindow`, `crossfadeMix` in `.ai/references/motion-core.mjs`. These reference helpers work without React; port or import according to the project's bundler/platform. They are tested with Node's built-in test runner.

### Metadata-first scene model
For every scene capture:
- id, source evidence, start/end progress, layers, dimensions and safe area;
- per-layer transforms `{x,y,scale,rotate,opacity}` and independent easing;
- entry/exit and interactions (including reverse-scroll behavior);
- reduced-motion alternative;
- mobile composition rules and validation frames.

Use `.ai/templates/motion-spec.md` rather than burying timing inside JSX. For multi-scene work define all windows centrally; avoid separate magic numbers in components.

## Source-specific Marlin reference (not mandatory defaults)
Water.pdf supplies a **20,000ms virtual prototype** and `SCROLL_VH=620`, with two video clips joined at `VIDEO_SEAM=0.5`. Three groups travel vertically using per-group offsets, rather than as a single filmstrip. `span` uses cubic ease-out; `ramp` is linear. See `.ai/references/marlin-timeline.json` for extracted parameters.

These numbers are **only** a measured/reported reference preset from the PDF. Do not inject them into unrelated projects. 19 source interactions are reported, but only the windows represented in the supplied code are encoded here; do not claim this preset reproduces all 19 as separate verified events.

## Runtime strategy
- Prefer transform and opacity for compositor-friendly effects.
- Derive state from one progress source; avoid rerendering heavyweight components unnecessarily.
- Use `requestAnimationFrame` only as needed, clean it up on unmount, handle visibility/reduced-motion where appropriate.
- Smooth position changes judiciously; smoothing affects exact frame-to-scroll correspondence and should be adjustable or disabled.
- Test scroll both ways, resizing, boundary values and snap/seam frames.
