# 03 — Quality gates and verification ledger

## Definition of Done
Project work is DONE only if (a) stated acceptance criteria are met, (b) relevant checks actually passed, (c) critical defects are resolved or explicitly accepted, and (d) user can understand how to run and maintain the result.

Every gate must be marked **PASS / FAIL / NOT RUN / NOT APPLICABLE**, never inferred from file creation.

| Gate | What counts as evidence |
|---|---|
| Requirements | mapping from brief and acceptance criteria to feature/files/observed behavior |
| Static checks | exact commands, exit status, tool output |
| Lint/format | separate tooling; `tsc --noEmit` alone is **not** lint |
| Build/package | production build/package command succeeds |
| Automated tests | tests run with reported pass/fail counts |
| Runtime behavior | app invoked and important flows exercised |
| Responsive/visual | snapshots or manual inspection at target widths, record browser/device |
| Accessibility | keyboard, semantics, contrast, reduced motion if relevant |
| Security | dependencies, authz, secrets, input validation and relevant threat scenarios |
| Asset audit | local resources exist, licenses understood, appropriate image/video sizes |

## Visual web minimum
- Inspect representative widths: 390, 768, 1024, 1440 px when environment permits.
- Check initial hero, transitions, final state, footer, hover/focus, errors, reduced motion.
- For exact reference work, compare against user-provided frames. Pixel equivalence cannot be claimed without actual comparison.

## Reporting
Summarize four groups: **implemented**, **verified**, **unverified**, **known issues**. If the environment lacks browsers, browsers are NOT RUN, not PASS. Never claim backend forms work when no actual request was made.
