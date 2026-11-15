# API Reference

All application routes use `/api/v1`. Protected routes require `Authorization: Bearer <JWT>`.

## Auth
- `POST /auth/register` JSON `{email,password,full_name,preferred_language}`
- `POST /auth/login` form fields `username` (email), `password`
- `GET /auth/me`

## Analyses
- `POST /analyses` multipart: `nitrogen`, `phosphorus`, `potassium`, `ph`, `organic_matter`, `moisture`, optional `field_name`, optional `image` (JPEG/PNG/WebP, max configured MB)
- `GET /analyses?limit=20&offset=0` (limit 1–100)
- `GET /analyses/{analysis_id}`
- `GET /analyses/trends/summary?field_name=North%20field` returns up to 100 historical score observations and a simple observed direction after at least three records; it is not a future degradation prediction.
- `GET /analyses/{analysis_id}/report` PDF

## Voice
- `POST /voice/speech` JSON `{ "text": "English report excerpt", "language": "hi-IN" | "kn-IN" }`
- Returns `audio/wav`; requires an authenticated user and `SARVAM_API_KEY` configured on the server.
- Server translates the bounded English excerpt with Sarvam Translate and synthesizes speech with Bulbul v4 Flash. The key is never sent to the browser.
- Upstream timeouts and rate limits are returned as controlled API errors. Voice generation incurs provider usage/credits.

## System
- `GET /health` checks API and database connectivity.

NPK values are assumed mg/kg; organic matter and moisture are percentages. Validate against the lab report and regional reference ranges. The screening rules are illustrative and do not prescribe fertilizer quantities.
