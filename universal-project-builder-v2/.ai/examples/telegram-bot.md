# Example brief — Telegram bot

- PROJECT_NAME: Study Companion Bot
- MODE: CREATE
- FIDELITY: CUSTOM
- PROJECT_TYPE: telegram-bot
- GOAL_AND_AUDIENCE: users practicing question-and-answer flashcards
- CORE_USER_JOURNEYS: /start → choose topic → show question → answer → result and progress
- MUST_HAVE: commands, structured state, persistence, validation, help and cancel, no change to original verified question/answer wording
- OUT_OF_SCOPE: website, animations, paid subscription
- TECH_STACK: Python + aiogram or Node + grammY, choose only after brief clarifies environment
- DATA_AND_INTEGRATIONS: Telegram Bot API and SQLite to start
- ENVIRONMENT_AND_DEPLOY: local during development, VPS for hosting
- ACCEPTANCE_CRITERIA: unknown commands, duplicate callback, invalid state, persistence and restart all verified
- EXECUTION_MODE: PLAN_THEN_IMPLEMENT

Select `adapters/telegram-bot.md`, `modules/backend-data.md`, `modules/security.md`. Don't select design, cinematic, video or 3D modules.
