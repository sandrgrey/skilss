# Backend, Data & Integrations

Model business rules before choosing a database. Define data ownership, API contracts, schema, validation, roles/permissions, retention and recovery requirements.

## Integration rules
- Keep keys on server or in secure runtime configuration, not client bundles or git.
- Apply validation to every untrusted payload, including webhook messages and imported files.
- Design idempotency and retries for external side effects.
- Handle timeouts, partial failures, duplicate events and rate limits.
- Authorization must be enforced server-side and tested by role.
- Never report a mock submission as a completed production operation.

## Data changes
Migration first, reversible where practical, tested against representative data. Destructive schema/data changes require explicit authorization and backup plan.

## Operational baseline
Health/readiness as applicable, structured logs without secrets, limited permissions, monitoring and runbook for common incidents. Keep implementation proportional to scale.
