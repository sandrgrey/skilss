# Adapter: Telegram Bot

**Enable:** architecture, backend-data, security. Never enable cinematic UI modules by default.

Clarify polling vs webhook, command list, conversational states, persistence needs, target hosting and expected failure handling.

## Design
- Route updates by type (messages, callbacks, commands, edits) and validate all incoming fields.
- Handle duplicate updates, expired callbacks, concurrency and retry-safe side effects.
- Keep `BOT_TOKEN` only in environment/server secrets.
- Use explicit states only when conversation requires it; support cancel/help/start.
- Avoid leaking user private data into logs and sample fixtures.

## Acceptance
Simulate/verify start, help, expected commands, unknown input, callback navigation, validation errors, duplicate updates, recovery after restart and token-missing startup.

Do not report actual messages delivered unless tested with a real bot in an authorized environment.
