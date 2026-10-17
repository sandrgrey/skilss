# Universal Project Builder — Claude Code instructions

Use the repository and `PROJECT_BRIEF.md` as the project specification. If critical fields in `PROJECT_BRIEF.md` are still `TODO`, ask only for blocking requirements. First inspect files, then choose one adapter and only relevant feature modules under `.ai/`. For multi-step work briefly plan, implement, inspect the actual results, run checks and report honestly. Never delete existing work or execute destructive operations without authorization. Do not invent successful tests, asset rights or external integrations.

@.ai/core/operating.md
@.ai/core/workflow.md
@.ai/core/quality-gates.md

## Module routing (read on demand)

- `.ai/modules/source-fidelity.md` for exact rebuilds and reference-driven work.
- `.ai/modules/architecture.md` for structure, stack and boundaries.
- `.ai/modules/design-system.md` for visual UI; `.ai/modules/cinematic-engine.md` for motion; `.ai/modules/video-engine.md` for video; `.ai/modules/3d-engine.md` for 3D.
- `.ai/modules/backend-data.md` for data/integrations and `.ai/modules/security.md` for threat modeling and secrets.
- `.ai/modules/agent-orchestration.md` only for multi-part tasks needing coordination.
- `.ai/adapters/` contains project-type profiles. Select a fitting one instead of implementing them all.

For planning use `.ai/templates/plan.md`; for acceptance use `.ai/templates/acceptance.md`. Preserve local changes. Distinguish source data from independent engineering guidance.
