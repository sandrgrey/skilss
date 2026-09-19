---
name: debugger
description: Diagnose a bug by reproducing it, locating the first divergence, testing hypotheses, and avoiding retry loops.
---
# Debugger

1. Reproduce the exact symptom when possible.
2. Capture the smallest relevant logs, inputs, state, and diff.
3. Separate facts from hypotheses.
4. Pick one discriminating check that can falsify the leading hypothesis.
5. Make the smallest fix consistent with evidence.
6. Run the closest regression test.

If the same failure fingerprint repeats, obey LoopGuard: warning -> strategy reset -> read-only audit.
