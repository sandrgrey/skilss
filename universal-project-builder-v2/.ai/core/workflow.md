# 02 — Workflow and LoopGuard

## State machine

1. **DISCOVERY** — inspect brief, tree, package manifest, existing tests, assets, git status, constraints. For an empty repo, record that it is empty.
2. **BLUEPRINT** — choose a single primary adapter, relevant modules, core architecture, user journeys, dependencies, tradeoffs and acceptance criteria. For high-effort work keep a living plan per `.ai/templates/plan.md`.
3. **BUILD** — implement in small, reversible steps. Keep UI, state, services and integration boundaries clear. Do not overwrite unrelated files.
4. **REVIEW** — examine correctness, tests, accessibility where applicable, security, performance and regressions.
5. **VALIDATE** — run executable checks available in the repository; inspect actual app if tools exist. Fix verified defects and repeat checks.
6. **DELIVER** — list what changed, evidence, commands, blockers, residual risks, and next concrete steps.

## LoopGuard: failure discipline

If an action fails twice with substantially the same error, STOP identical retries and:
1. Quote the exact failure signature and command.
2. Identify 2–3 plausible causes and inspect evidence to discriminate.
3. Change one meaningful variable and test the smallest possible hypothesis.
4. Reevaluate architecture/permissions/available tooling if still failing.
5. After a third materially distinct failed attempt, report BLOCKED with diagnostics instead of looping forever.

Do not apply blind package upgrades, mass rewrites, security-disabling workarounds or deletion of lockfiles as a substitute for diagnosis.

## Plans
- For tiny tasks: one or two actions, skip ceremony.
- For multi-file implementation: brief work plan, progress on milestones, revisions when discoveries invalidate assumptions.
- For costly or destructive actions: request explicit authorization.
