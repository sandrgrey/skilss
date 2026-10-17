# Agent Orchestration (optional)

Use separate sub-tasks only when the environment supports them and work naturally partitions; otherwise follow the same sequence in one agent.

## Roles are responsibilities, not fictional parallel execution
1. Researcher — inspect existing facts, official docs, sources and tradeoffs.
2. Architect — boundaries, data flow, acceptance criteria and delivery stages.
3. Implementer — changes in scoped files and tests.
4. Reviewer — independent review of correctness, security, regressions and user experience.
5. Validator — executes real checks and records evidence.

Do not claim separate agents ran when they did not. A reviewer cannot call code secure solely from a static glance.

## Handoff contract
Each handoff contains goal, relevant paths, constraints, assumptions, known risks, done/not-done, verification output and next precise action. Do not send secrets or unnecessarily duplicate huge documents.

## Guardrails
Limit concurrent edits to overlapping files; merge and test changes; keep a single accountable owner for final acceptance and release. Protect the user's repository state.
