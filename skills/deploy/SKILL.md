---
name: deploy
description: Plan or execute deployment/configuration changes with validation, exact backups, atomic writes, and rollback.
---
# Deploy

Use transaction discipline for mutable configuration:

1. Capture the exact pre-change state.
2. Create an operation-scoped backup.
3. Build a candidate without mutating the live file when possible.
4. Validate the candidate.
5. Atomically replace the live file.
6. Run post-change health checks.
7. Restore the exact operation backup on failure.

Never choose a rollback file merely because it is the newest backup in a directory.
