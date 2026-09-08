# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The public website for Dra. Viviana Romero Nossa's pediatric cardiology practice, built on the **Medilab** HTML template from BootstrapMade (free tier, v4.9.1). The front end (`index.html`, `inner-page.html`, `assets/`) is still plain HTML/CSS/JS with no build step — but it is now served by a small **FastAPI** app (`app/`), packaged as a Docker image, instead of a raw static file server or PHP.

There used to be PHP form handlers (`forms/contact.php`, `forms/appointment.php`); they never worked (they depended on a paid-tier library not present in the repo) and have been removed in favor of FastAPI endpoints — see "Forms" below.

## Commands

- Run locally with Docker (recommended — matches production): `docker compose up --build`, then visit `http://localhost:8000`. Requires a `.env` file (`cp .env.example .env` and fill in SMTP values) — `docker compose` will refuse to start without one.
- Run without Docker: `uv sync`, export the variables from `.env.example`, then `uv run uvicorn app.main:app --reload --port 8000`.
- Update dependencies / regenerate the lockfile: `uv lock` (add `--native-tls` if `uv` can't validate PyPI's TLS chain on this network).
- No test suite exists yet.

## Architecture

- `app/main.py` — the FastAPI app. Mounts the form router at `/api`, exposes `GET /healthz`, and mounts `StaticFiles(directory="www", html=True)` at `/` **last**, so it doesn't shadow the `/api/*` routes. Any new `.html` file dropped into `www/` (i.e. copied there by the Dockerfile) is served automatically — no route needs to be added.
- `app/forms.py` — `POST /api/contact` and `POST /api/appointment`. Both build an `email.message.EmailMessage` and send it via stdlib `smtplib` (no extra dependency), run through `run_in_threadpool` since `smtplib` is blocking. `From` is the authenticated SMTP account; `Reply-To` is set to the visitor's email so replies go straight to them. On success they return `PlainTextResponse("OK")`; on failure, `PlainTextResponse(<message>, status_code=500)`.
  - **This response contract is dictated by `assets/vendor/php-email-form/validate.js`** (kept from the original template, has no PHP dependency itself): it POSTs the form as `multipart/form-data` and expects the literal text `"OK"` on success or any other text as an error message to display. Don't change the contract without also updating `validate.js` and the form markup (`.loading` / `.error-message` / `.sent-message` divs).
  - Config is read directly from environment variables (`os.environ`) — `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`, `CONTACT_TO_EMAIL`, `APPOINTMENT_TO_EMAIL`. See `.env.example`.
- `Dockerfile` — multi-stage, `python:3.13-slim` (matches `.python-version`), uses `uv` to install into a venv in the builder stage, then copies only `.venv/`, `app/`, and the web assets (`index.html`, `inner-page.html`, `assets/`, copied into `www/`) into the final image. Runs as a non-root user. `reporte*.html` and other repo files are deliberately **not** copied into the image (see below).
- `docker-compose.yml` — the production shape: pulls the image from GHCR, no published ports (Traefik on the VPS reaches it over the compose network via labels), `env_file: .env`. This is the exact file deployed to the VPS.
- `docker-compose.override.yml` — local-dev-only, auto-merged by `docker compose`: builds from the local `Dockerfile` and publishes port 8000.
- `.github/workflows/deploy.yml` — on push to `master`: builds the image, pushes to `ghcr.io/<owner>/<repo>` (lowercased, tagged `latest` and the commit SHA), then SSHes into the VPS and runs `docker compose pull && docker compose up -d` in the project's directory. Needs `VPS_SSH_HOST`, `VPS_SSH_USER`, `VPS_SSH_PRIVATE_KEY` as GitHub secrets.
- **Deployment target**: a Hostinger VPS already running Traefik (Docker provider, `network_mode: host`, Let's Encrypt via HTTP-01) as one of several projects on that box. This site is routed via `Host(\`cardiologia.futurehealthlabmx.io\`)` — a subdomain of `futurehealthlabmx.io` used until a permanent domain is set up. Because Traefik already terminates TLS and handles the HTTP→HTTPS redirect at the entrypoint level, the app container itself only needs the Traefik labels in `docker-compose.yml`, not its own port publishing or TLS handling.

## Structure

- `index.html` — the main/home page (single-page layout with anchor-linked sections: hero, about, services, doctors, appointment, contact, etc.)
- `inner-page.html` — a generic inner-page template from the original theme (not linked from the live nav; useful as a starting point for new subpages). Served, but not linked.
- `reporte.html`, `reporte 2.html`, `reporte 3.html` — standalone, uncommitted working pages that reuse the same head/vendor includes as `index.html`; treat these as drafts/scratch pages, not part of the established site structure. They are intentionally excluded from the Docker image until their fate is decided (see `CONTROL_SESIONES.md`).
- `assets/css/style.css` — the template's custom stylesheet (hand-edited on top of the theme)
- `assets/scss/` — Sass source counterpart (currently only a `Readme.txt`; no compiled Sass pipeline is wired up in this repo)
- `assets/vendor/` — third-party front-end libraries bundled with the theme (Bootstrap, Bootstrap Icons, Boxicons, Font Awesome, GLightbox, Remixicon, Swiper, animate.css, and `php-email-form/validate.js`). Treat as vendored/third-party — don't hand-edit these files; update by replacing the vendor folder if a library needs upgrading.
- `assets/js/main.js` — the template's JS (nav toggling, scroll behavior, GLightbox/Swiper init, etc.)
- `assets/img/` — site images, including `assets/img/testimonials/` and `assets/img/doctors/`

## Working with the HTML pages

- All top-level HTML pages (`index.html`, `reporte*.html`, `inner-page.html`) repeat the same `<head>` block (Google Fonts + vendor CSS links) and the same vendor `<script>` includes near the end of `<body>`. When adding a new page, copy this boilerplate from `index.html` rather than reinventing it, and keep asset paths relative to the repo root (`assets/...`) consistent with the existing pages. If the page should be publicly served, also add it to the `COPY` step in the `Dockerfile`.
- Content/contact info (emails, phone numbers) lives inline in the HTML (e.g., the topbar in `index.html`) — there's no templating or shared partials, so contact details must be updated in every page that repeats them.
- The form `<select>` option values (department/city in the appointment form) must match their visible labels — they're sent as-is in the notification email.
- The site language is a mix: template scaffolding/comments are in English, real page content is in Spanish.
