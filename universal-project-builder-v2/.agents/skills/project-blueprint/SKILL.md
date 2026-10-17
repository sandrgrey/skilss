---
name: project-blueprint
description: Use when starting a new code project, planning substantial changes, translating a PDF/mocks into architecture, or reviewing an ambiguous project brief.
---

# Project blueprint from a brief

1. Read `PROJECT_BRIEF.md` and inspect real repository state.
2. Read `.ai/core/operating.md`, `.ai/core/workflow.md`, and `.ai/modules/architecture.md` from repository root.
3. Select one adapter under `.ai/adapters/` and only necessary modules; justify choices.
4. Produce a plan using `.ai/templates/plan.md` with verifiable acceptance criteria, assumptions, source/asset inventory, risks and rollback.
5. If execution is authorized, implement in milestones and verify results with `.ai/core/quality-gates.md`.
6. For exact reference rebuilds add `.ai/modules/source-fidelity.md`; differentiate verified values from estimates.
