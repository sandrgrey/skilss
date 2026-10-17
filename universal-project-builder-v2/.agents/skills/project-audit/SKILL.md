---
name: project-audit
description: Use when asked to analyze codebases, technical PDFs, incomplete projects, bugs, architecture, security or readiness, and to produce a prioritized repair plan.
---

# Audit an existing project without changing it

1. Do not modify code in AUDIT mode.
2. Inventory the actual source tree, manifests, README, tests, dependencies and configuration; distinguish available materials from missing ones.
3. Compare implementation to `PROJECT_BRIEF.md` and `.ai/core/quality-gates.md`, selecting the relevant adapter.
4. Classify findings as confirmed code defects, plausible runtime risks, or unverified hypotheses. Cite file and line when possible.
5. Prioritize by impact and likelihood, with concrete remediation and verification steps; avoid inventing test results.
6. Recommend an implementable next-step plan; do not begin migration, deployment or deletions without explicit authorization.
