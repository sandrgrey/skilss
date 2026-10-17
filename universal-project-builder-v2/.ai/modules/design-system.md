# Design System & Responsive Composition

## Tokens
Use named tokens for surface, text, accents, radii, spacing, elevation, typography, motion durations and easing. Preserve reference tokens in EXACT mode; invent new tokens only for custom/adapted modes.

## Three layout modes
- **FLUID** — semantic document flow, Grid/Flex, intrinsic sizing; default for shops, SaaS, dashboards and documentation.
- **FIXED_STAGE** — artboard with absolute positions scaled by explicit policy; only for precisely designed scenes. Keep the UI's navigational controls outside scaling where necessary.
- **HYBRID** — fixed/scaled cinematic hero with responsive content below; default for Marlin-style promotional work needing readable content.

For FIXED_STAGE record `STAGE_W`, `STAGE_H`, `scale_policy` (`width_lock`, `contain`, `cover`) and overflow-safe zone. Width lock guarantees matching width, **not** readable text or full height. Don't confuse contain/cover. Never apply fixed-stage scaling to an entire information-heavy interface without explicit approval.

## Responsive acceptance
Check min readable font size, tap target sizes, cutoffs, dynamic content, extra-tall mobile aspect ratios, orientation changes, desktop zoom, scrollbar effects and `100vh`/viewport semantics. Use dedicated mobile choreography where a scaled desktop scene breaks.

## Interaction
Clickable items are links/buttons with focus states. Decorative ornaments must not masquerade as navigation. Support screen reader names and prefers-reduced-motion. Render loading/error/empty states for interactive features.

## Source lesson
Water.pdf puts a nav bar outside artboard and hides links at 640px; avoid inline `display: flex` which overrides a non-`!important` media query's `display: none`.
