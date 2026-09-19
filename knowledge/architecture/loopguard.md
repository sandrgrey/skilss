---
tags: [architecture, loopguard, debugging]
summary: LoopGuard fingerprints failed operations and escalates repeated identical failures from warning to strategy reset to audit.
---
# LoopGuard

LoopGuard hashes the operation type, command family, exit code, and normalized error output. The same failed fingerprint repeated twice produces a warning, three times requires a strategy reset, and four times reaches the independent-audit boundary. A successful operation resets the streak.
