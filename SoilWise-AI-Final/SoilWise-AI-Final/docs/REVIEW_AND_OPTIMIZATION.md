# Four-role engineering handoff

## Architect
- Chose a modular monolith: Next.js PWA + stateless FastAPI + PostgreSQL + object-storage boundary.
- Kept inference behind a service boundary so future CNN/GBM inference can move to a worker without changing the farmer-facing contract.
- Avoided premature microservices; horizontal API scaling and later queue-based inference are the intended growth path.

## Engineer — implemented
- Registration/login, JWT-protected endpoints, soil analysis creation, paginated history, report retrieval and PDF download.
- Optional JPEG/PNG/WebP upload with MIME allowlist, bounded read, decode verification, pixel cap and normalized JPEG output.
- Rule-based diagnostic engine, conservative next-step recommendations, crop suggestions and PWA shell caching.
- Docker Compose development environment, Alembic schema migration, historical trend summary, optional ML training utilities and API documentation.

## Reviewer — findings and resolutions
| Finding | Severity | Resolution |
|---|---|---|
| Image upload originally read unbounded bytes | High | Read limited to configured size + 1 byte; reject oversized files |
| MIME header alone was trusted | High | Decode/verify image bytes and enforce pixel cap |
| Non-finite numeric values were not explicitly rejected | Medium | Added finite-value validation |
| Analysis history had fixed 100-row response | Medium | Added bounded limit/offset pagination |
| Database transaction failure could leave an orphan upload | Medium | Roll back and remove uploaded local file on persistence failure |
| Production JWT secret could remain a known default | High | Production settings reject short/default secret |
| DB health endpoint only reported process liveness | Medium | Health route executes `SELECT 1` |
| NPK units were unclear in the UI | High | UI and validation now state assumed mg/kg |
| Thresholds could be mistaken for validated agronomy | High | Explicit MVP/illustrative disclaimer and calibration requirement |
| Docs described tables/features not fully implemented | Medium | Documentation now reflects actual MVP scope |

## Optimizer — improvements
- SQLAlchemy engine uses pre-ping, bounded connection pooling and connection recycling.
- History queries use SQLAlchemy `select()` and server-side pagination.
- Image thumbnailing reduces storage and future transfer cost.
- Service worker caches only same-origin GET shell/assets; API requests are never cached.
- Kept the app as a modular monolith to minimize operational overhead until measured scale warrants extraction.

## Remaining production blockers
1. Alembic migration workflow is now included; production startup no longer runs `create_all`. Keep schema changes migration-owned.
2. Use private object storage, not container-local uploads, for multi-instance deployment.
3. Add rate limiting, refresh-token rotation, password reset, email verification and account lockout controls.
4. Add CI with type-check, lint, unit/integration tests, dependency and container scans.
5. Train and independently validate models on labeled regional data; implement calibrated confidence and human-reviewed agronomy content.
6. Complete full UI localization (the current interface is primarily English), accessibility testing and Android camera QA. Sarvam Hindi/Kannada translation + TTS endpoint and report controls are integrated but require a live API key test.
7. Run load tests and define SLOs, backups, alerting and incident procedures.
8. Move bearer-token storage from localStorage to a secure HttpOnly-cookie/BFF design; localStorage is vulnerable to token theft if an XSS defect is introduced.

## Verification status
The backend diagnostic, trend, upload and PDF test suite passes seven tests (`pytest -q`); Python compilation and an SQLite execution of the initial Alembic migration were also checked. A full Docker build, browser E2E run, live Sarvam API call, cloud deployment, security penetration test and agronomic validation have not been executed in this environment. Package installation was blocked by unavailable network access in this execution environment. Do not interpret this review as certification for production launch.
