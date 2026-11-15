# System Architecture

## Current MVP topology
- **PWA (Next.js):** responsive farmer UI, auth, soil data capture, report display, Hindi/Kannada report audio controls and static-asset caching.
- **API (FastAPI):** stateless REST endpoints, auth, validation, diagnostics, recommendations and PDF export.
- **PostgreSQL:** users and analysis history; source of truth.
- **Image storage adapter:** local volume for development; replace with private object storage for production.

## Request flow
1. Farmer authenticates and receives a short-lived JWT.
2. Farmer submits soil measurements and optional image.
3. API validates ranges and image bytes, normalizes image and persists an analysis.
4. Diagnostic service applies transparent screening rules and recommendation service returns conservative next steps.
5. Farmer sees result, history and can download PDF. A field trend endpoint summarizes observed health-score direction once three or more assessments exist. If `SARVAM_API_KEY` is configured, a protected voice endpoint translates the report excerpt and returns Hindi/Kannada speech.

## Scale path
Run multiple stateless API replicas behind a load balancer. Move images to private S3-compatible storage and serve through short-lived signed URLs/CDN. Add Redis for caching/rate limiting and a queue-backed worker for expensive inference. Add model registry/versioning, dataset lineage, offline evaluation, calibration and drift monitoring before enabling ML output. Partition large tables only when measured query patterns justify it.

## Explicit non-goals of this MVP
Training utilities for ResNet-50 image classification and a gradient-boosted tabular baseline are included under `backend/`, but no trained weights or live inference integration is included. Hybrid fusion, Grad-CAM, SHAP and regional agronomy validation are not implemented. Image upload is storage only; it does not diagnose nutrients from a photo. Voice output is an optional Sarvam Translate + Bulbul TTS integration and requires a valid provider key; it has not been live-tested here.
