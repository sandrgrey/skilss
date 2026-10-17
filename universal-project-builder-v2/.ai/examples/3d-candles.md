# Example brief — Premium candle portfolio

- PROJECT_NAME: Atelier Candles 3D
- MODE: CREATE
- FIDELITY: CUSTOM
- PROJECT_TYPE: 3d-showcase / fullstack
- GOAL_AND_AUDIENCE: premium handmade-candle showcase, leads through social and email
- CORE_USER_JOURNEYS: browse catalog → rotate/zoom GLB model → open details → contact via Telegram/email
- MUST_HAVE: 3D per product, detailed page, admin uploading GLB/photos/prices, safe file validation, contact links, mobile fallback
- OUT_OF_SCOPE: checkout, payment, cart
- DESIGN: graphite #1a1a2e, amber #f0a500, dark premium
- ANIMATION: BASIC with optional cinematic landing hero
- TECH_STACK: Next.js App Router + TypeScript + @react-three/fiber + Supabase
- DATA_AND_INTEGRATIONS: Supabase auth/database/storage for admin; Telegram/email as outgoing contact links
- ENVIRONMENT_AND_DEPLOY: Vercel + Supabase
- ACCEPTANCE_CRITERIA: upload validation; usable mobile catalog; 3D orbit/zoom; permissions; no fake checkout
- EXECUTION_MODE: PLAN_THEN_IMPLEMENT

Select `adapters/fullstack.md`, `modules/design-system.md`, `modules/3d-engine.md`, `modules/backend-data.md`, `modules/security.md`. Add cinematic-engine only when animation is explicitly desired.
