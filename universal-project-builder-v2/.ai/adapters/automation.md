# Adapter: Automation / CLI / Scripts

**Enable:** architecture, security. Add backend-data only if persistent storage/integrations needed.

Determine inputs, outputs, exact side effects, idempotency, scheduling, permissions and safe defaults. Provide `--help`, dry-run mode for risky operations, exit codes and useful diagnostics where platform-appropriate.

Test invalid arguments, missing files, repeated execution, partial failure and interruption; handle both Windows and Unix path differences if cross-platform support is claimed.

No hidden network calls or destructive filesystem changes. Require confirmation for deletion, payments, force-push or production changes.
