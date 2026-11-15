# SoilWise AI — one-time setup

## What you need to install first

Install **Docker Desktop** for Windows or macOS (or Docker Engine + the Docker Compose plugin on Linux). Start Docker and wait until it reports that it is running. You do not need to install Python, Node.js, PostgreSQL, or the project libraries separately: Docker builds the API and frontend images and downloads their dependencies for you.

## Windows

1. Extract `SoilWise-AI-Final.zip`.
2. Open the extracted `SoilWise-AI-Final` folder.
3. Right-click `setup-and-run.ps1` and choose **Run with PowerShell**. If Windows blocks scripts, open PowerShell in this folder and run:
   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\setup-and-run.ps1
   ```
4. Wait for the first build to finish, then open **http://localhost:3000**.

## macOS / Linux

1. Extract the ZIP and open a terminal in `SoilWise-AI-Final`.
2. Run:
   ```bash
   ./setup-and-run.sh
   ```
3. Wait for the first build to finish, then open **http://localhost:3000**.

## Use the application

1. Select **Register** and create your account.
2. Sign in.
3. Open **New analysis**, enter the soil laboratory readings, and optionally attach a soil photograph.
4. Submit the analysis, review the screening results, and download the PDF report.
5. Hindi/Kannada speech is optional. Add a valid `SARVAM_API_KEY` to `.env`, then restart with `docker compose up -d --force-recreate api`.

## Stop / start later

- Stop: press `Ctrl+C` in the terminal, then run `docker compose down`.
- Start again: run `docker compose up` from this folder.
- Keep database and uploaded files: do **not** run `docker compose down -v` (that deletes the persistent volumes).

## Important project boundaries

- The current nutrient assessment is illustrative, rule-based screening; it is not laboratory-validated and must not be used to calculate fertilizer doses.
- Uploaded soil photos are validated, normalized and stored. The current application does not infer nutrient levels or soil type from photos.
- CNN and tabular model training scripts are included, but training requires a properly labeled dataset. No trained model or measured accuracy is supplied.
- Historical trend summaries describe recorded observations; they are not future degradation predictions.
- Sarvam speech requires your own API key. Without it, the rest of the application can still run.
- Local camera capture works only in supported browser contexts. For phone access over a network, deploy behind HTTPS.

This is a runnable educational MVP foundation, not a scientifically validated agricultural diagnostic product or a hardened public production service. Review `docs/FINAL_HANDOFF.md` before any real-world deployment.
