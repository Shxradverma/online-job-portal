# OnlineJobPortal

Django job portal with a public job search, candidate and recruiter dashboards, private PDF resumes, applications, messages, interviews, and recent activity.

## Current delivery status

Core functionality has been implemented in source. 32 backend regression tests pass using Django 6.1 from the uploaded development environment and SQLite. Django system checks and migration consistency checks pass. Python, JavaScript (including inline scripts), and shell syntax checks pass.

**This is not yet a verified production deployment.** Installation of production dependencies could not run in the editing environment. Production pins resolve to a patched Django 6.1 release; that exact installed stack, PostgreSQL, WhiteNoise, Gunicorn, SMTP, and browser interactions still need validation. No live deployment or GitHub push has been performed.

See `AUDIT.md` for the original gaps, changes, and remaining launch work.

## Local setup

Use Python 3.12 or newer and a fresh environment. The uploaded Windows virtual environment is deliberately not included in this deliverable.

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows, copy `.env.example` to `.env` using the file explorer or `Copy-Item`. Replace the placeholder `DJANGO_SECRET_KEY` with a long random value. Keep `DEBUG=True` only for local work.

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. Create candidate and recruiter accounts at `/register/`. Recruiters add their company, then publish a job through `/dashboard/`. Candidates add profile details and upload a PDF through `/profile/`, then view and apply to a published job. Applications connect both users to a private conversation and interviews.

This is a source-only package. Keep your original ZIP/database/media backup: the original database, media uploads, local environment, and Git internals are not copied into this distribution. There are no shipped default credentials or fake production jobs. Existing databases are upgraded through migrations; take a backup before applying them.

## Checks

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test api --settings=config.test_settings
python manage.py collectstatic --noinput
```

`config.test_settings` is for tests only: it uses an in-memory database, in-memory uploads, and a fast password hasher. Never use it for deployment. Production runs with `config.settings`. GitHub Actions runs checks after the source is pushed.

## Deployment

The existing repository reference in the uploaded ZIP is:
`https://github.com/Shxradverma/online-job-portal`

Connect GitHub and Render to continue deployment from ChatGPT. The provided `render.yaml` describes a Python web service, PostgreSQL database, and persistent disk for private resumes. **It uses paid resource plans; review the actual current cost before provisioning.** No paid resources have been created.

1. Apply these changes to the existing repository on a review branch, keeping the repository's history. Do not upload a virtual environment, `.env`, database, or user media.
2. Run the CI checks with the fresh production dependency installation. Resolve failures before merging/deploying.
3. Create the Render Blueprint from this repository. The build runs `bash build.sh`; startup runs migrations and Gunicorn through `bash start.sh`.
4. Set `CSRF_TRUSTED_ORIGINS` to the actual HTTPS site origin. Render's hostname is automatically added to `ALLOWED_HOSTS`. For a custom domain, add it to `ALLOWED_HOSTS` too.
5. Configure SMTP: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, and `DEFAULT_FROM_EMAIL`. Password-reset email cannot be delivered until SMTP works.
6. Create the initial administrator in the service shell with `python manage.py createsuperuser`. Never commit admin passwords.
7. Verify public search, signup/login, profile/resume upload and private download, job publication, applications, messages, interview scheduling, password-reset email, and persistence after a restart.
8. Check HTTPS/proxy handling and run `python manage.py check --deploy`. Enable HSTS after confirming HTTPS works. Configure backups for both PostgreSQL and private resume files.

A Dockerfile is also included for a Python-capable host. Mount persistent storage at `/var/data`, set `MEDIA_ROOT=/var/data/media`, and configure `DATABASE_URL`, hosts, HTTPS, and email. Do not serve `/media/` publicly: resumes require authenticated download endpoints.

Official hosting references:
- https://render.com/docs/deploy-django
- https://render.com/docs/disks
- https://render.com/docs/blueprint-spec
- https://www.djangoproject.com/download/

## Behavior and boundaries

- Registration supports CANDIDATE and RECRUITER only; administrators are created separately.
- Each recruiter owns their companies and jobs. Joining an existing company, invitations, and manual recruiter verification are not implemented.
- Resumes accept PDF files up to 5 MB, with extension and header checks. This is not antivirus/content scanning. Only the owner and recruiters receiving that resume through an application can download it.
- Candidates cannot set hiring status, attach another user's resume, or rewrite a job through withdrawal. Recruiter notes stay private to recruiters/admins.
- Messages and interviews are tied to an application. Interview times display in each browser's local timezone. Notifications are an in-app recent activity feed, refreshed on demand; no push/email interview notifications or unread counters are implemented.
- Matching is a deterministic comparison of comma-separated skills, not an LLM or semantic AI ranking service.
- Email verification is an existing model/admin flag, not an implemented self-service verification flow.
- Basic request throttling uses Django's local-memory cache. A shared cache and edge rate limits are needed for coordinated multi-worker protection.
- Candidate profile photos/company logo delivery, advanced reporting, resume parsing, payment plans, social login, and video calling are outside this delivery.
