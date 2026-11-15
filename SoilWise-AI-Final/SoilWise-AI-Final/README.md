# SoilWise AI — hardened MVP

A mobile-first soil analytics platform built with Next.js, FastAPI and PostgreSQL. This repository is a runnable software MVP foundation, not a validated agricultural diagnostic product.

## Quick start
1. Install Docker Desktop.
2. Copy `.env.example` to `.env`.
3. Change `POSTGRES_PASSWORD` and `JWT_SECRET` before sharing the environment. For production, set `APP_ENV=production`, configure explicit `CORS_ORIGINS`, and use a unique random JWT secret of at least 32 characters.
4. Optional voice: set `SARVAM_API_KEY` on the backend. The key must remain server-side.
5. Run `docker compose up --build`.
6. Open http://localhost:3000; API docs are at http://localhost:8000/docs in development.

The API container runs `alembic upgrade head` before starting. Development startup retains `create_all` as a local convenience; production startup does not create tables automatically.

## Included
- Next.js PWA with registration, login, dashboard, soil readings, optional camera/file image upload and PDF report download.
- FastAPI backend with JWT authentication, PostgreSQL persistence, owner-scoped history and PDF export.
- Alembic initial schema migration and production migration workflow.
- Image validation, EXIF orientation correction, resizing and local development storage.
- Paginated analysis history, field-level historical score trend summary (requires at least three records), and bounded upload validation.
- Paginated PDF report generation with wrapped and escaped user-supplied text.
- Optional Sarvam Translate + Bulbul v4 Flash Hindi/Kannada report audio. Requires a valid `SARVAM_API_KEY` and provider credits; live integration has not been verified in this environment.
- Optional ResNet-50 image and gradient-boosted tabular model training scripts under `backend/`; they require a separately collected, consented, expert-labeled dataset and are not connected to live inference.
- Service worker caches only same-origin static assets; it does not cache navigations, authenticated pages or API responses.
- Docker Compose, architecture/API/database documentation and automated tests.

## Scientific limitation
The current diagnostics are transparent rule-based screening, not an agronomically validated model. Thresholds assume N/P/K mg/kg and must be calibrated to the exact laboratory extraction methods, soil type, crop and regional guidance. The soil photograph is stored but is not used to predict nutrient status. No trained CNN, gradient-boosting model, Grad-CAM or SHAP model is included. Do not use this MVP to prescribe fertilizer quantities.

## Tests
From `backend/`:
```bash
pip install -r requirements.txt
pytest -q
python -m alembic upgrade head
```
The local test suite currently contains seven tests covering diagnostic thresholds, historical trend summaries, image validation/normalization and PDF generation. Run `cd backend && pytest -q`; the included `pytest.ini` configures the import path.

## Before public production
- Replace local image storage with private S3-compatible storage and short-lived signed URLs.
- Move bearer-token storage from localStorage to secure HttpOnly cookies via a BFF/session design.
- Add rate limiting, refresh-token rotation, password reset, email verification, account lockout controls and audit logging.
- Complete full Hindi/Kannada UI localization, accessibility testing and Android camera QA.
- Train and independently validate models on labeled regional data using the optional scripts in `backend/`; integrate inference, Grad-CAM/SHAP, calibrated confidence and human-reviewed agronomy content before enabling ML predictions.
- Add structured logs, metrics, tracing, backups and disaster recovery tests.
- Run full Docker/frontend builds, browser E2E tests, security testing and load tests. These were not run in the current environment because Docker is unavailable and frontend dependencies are not installed.

## Fastest way to run
Install and start Docker Desktop, extract the ZIP, then run `setup-and-run.ps1` on Windows or `./setup-and-run.sh` on macOS/Linux. The script creates a local `.env` and starts the full stack with `docker compose up --build`. Open http://localhost:3000 when the build completes. See `START_HERE.md` for full steps.
