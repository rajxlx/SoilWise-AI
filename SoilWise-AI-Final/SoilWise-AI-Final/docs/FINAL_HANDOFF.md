# SoilWise AI — engineering handoff

## Changes in this revision
- Replaced unconditional startup schema creation with development-only bootstrap; production startup expects Alembic-managed schema.
- Added an initial Alembic revision and made the Compose API startup apply migrations before Uvicorn.
- Hardened production settings against placeholder JWT secrets and wildcard/empty CORS configuration.
- Normalized image EXIF orientation before JPEG conversion.
- Reworked PDF generation to wrap text, paginate long reports and escape user-provided strings.
- Restricted the service worker to static same-origin assets; authenticated pages, navigations and API responses are not cached.
- Added authenticated Hindi/Kannada report audio endpoint using Sarvam Translate and Bulbul v4 Flash, with provider key kept server-side.
- Added a field history trend summary (observed direction only) and optional ResNet-50 / gradient-boosted training scripts that require reviewed labeled datasets.
- Replaced the metadata-driven initial schema creation with explicit Alembic table/index operations and added pytest import-path configuration.
- Added report-page voice controls and improved frontend API error parsing.
- Added image normalization/rejection and long-report PDF tests.

## Verification performed
- `pytest -q`: 7 passed.
- `python -m compileall -q app migrations`: passed.
- `DATABASE_URL=sqlite:////tmp/soilwise-final-migration.db python -m alembic upgrade head` and `... python -m alembic current`: initial revision applied and reported as head.
- TypeScript build was attempted but dependencies are not installed; package installation could not reach the package registry in this environment.
- Docker is unavailable here; no Docker image build or browser end-to-end run was performed.
- Sarvam endpoint integration is implemented against current official REST contracts but was not live-tested because no API key was supplied.

## Remaining launch blockers
- No trained or validated soil-image CNN/GBM is included; image uploads are stored, not used to infer soil type or nutrient status. Optional training scripts are dataset-dependent and are not wired to production inference.
- No scientific validation of screening thresholds or crop/fertilizer guidance; do not prescribe fertilizer doses from this MVP.
- Full UI translation is not complete; Hindi/Kannada are currently supported for report audio only.
- JWT remains in localStorage in the browser. Move to HttpOnly secure cookies/BFF before public launch.
- Add rate limiting, refresh-token rotation, email verification, password recovery, object storage, malware scanning, observability, backups, load tests and security review.
- Set `SARVAM_API_KEY` and validate the provider account's model access, billing and usage limits before enabling voice for end users.
