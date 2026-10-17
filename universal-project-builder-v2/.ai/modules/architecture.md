# Architecture & Research

## Before choosing a stack
Check type of product, environment/hosting, interactive complexity, team knowledge, data lifespan, expected scale, user constraints, existing repo and availability of supported dependencies.

Compare two practical choices if undecided; record why the selected stack better meets the brief. Do not choose a language from a cinematic reference for a Telegram bot or backend-only service.

## Boundaries
UI/presentation → application state/use-cases → domain → infrastructure/adapters. A small app may combine layers; preserve conceptual boundaries even without many files.

Centralize configuration and constants. Type/validate all external inputs. Model errors explicitly. Avoid shared mutable global state unless justified.

## Reproducibility
Pin versions or commit a valid lockfile; document runtime version and package manager. Test migrations, install, build, and start commands. Never label caret ranges (`^`) as exact pins.

## Performance budget
Define meaningful budgets based on device, connection and application type rather than one-size-fits-all values. Profile or measure before complex optimization.
