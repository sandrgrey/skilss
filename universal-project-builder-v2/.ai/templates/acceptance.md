# Acceptance checklist — select only relevant items

## Requirements
- [ ] Every MUST_HAVE item has evidence of implementation.
- [ ] Explicit OUT_OF_SCOPE items were not silently added.
- [ ] Reference divergence is documented (EXACT/INSPIRED).

## Engineering
- [ ] Dependencies are justified; installation is reproducible.
- [ ] Static checks and actual lint run separately where applicable.
- [ ] Build and meaningful tests succeed, or blockers are clearly declared.
- [ ] Error/loading/empty states verified.
- [ ] Credentials are not committed or exposed.

## Interface (if applicable)
- [ ] 390/768/1024/1440 px, plus unusual aspect ratios as relevant.
- [ ] Text remains readable; interactive elements work with touch/keyboard.
- [ ] Reduced motion and media failure fallbacks work.
- [ ] Navigation, forms and CTAs are functional; no mock success.
- [ ] Images/video have provenance, correct paths and budgets.

## Release
- [ ] Setup, run, build and test commands documented.
- [ ] No unauthorized deployment, destructive operations or pushes.
- [ ] Unverified claims and known issues are explicit.
