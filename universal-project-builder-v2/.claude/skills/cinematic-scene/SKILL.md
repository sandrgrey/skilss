---
name: cinematic-scene
description: Use when implementing animation timelines, scroll-driven videos, parallax groups, multi-clip seams, or immersive animated landing pages from a design reference.
---

# Build and verify scroll-driven cinematic scenes

1. Read `.ai/modules/cinematic-engine.md`, `.ai/modules/video-engine.md`, and `.ai/modules/design-system.md` from repository root.
2. For Marlin references, examine `.ai/references/from-water.md`, `.ai/references/marlin-timeline.json`; never assume its values are universal defaults.
3. Define a motion specification using `.ai/templates/motion-spec.md`; keep timeline, assets and design coordinates centralized.
4. Use independent pure math helpers (`.ai/references/motion-core.mjs`) or port to the project's stack; test boundaries and progress both directions.
5. Verify at timeline landmarks, desktop and mobile, video loading/failure, reduced-motion, and fast reverse scroll. A crossfade is not automatically seamless.
6. If visual comparison tools are available, fill `.ai/templates/visual-comparison.md`. Clearly disclose unverified media/assets.
