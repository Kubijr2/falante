# Falante

An AI-assisted Brazilian Portuguese learning platform — a companion study tool for college students, independent learners, travelers, and heritage speakers.

**Status:** Milestones 1–10 complete — Vocabulary Manager, Flashcards (spaced repetition), Dashboard, Grammar Reference, Verb Conjugation Explorer, an AI Grammar Tutor, an AI Writing Coach, Docker, a Reading Helper (with verb-form recognition), production-readiness, and real accounts via Google Sign-In (with per-user data), all full-stack and tested end to end.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full design plan, [`docs/ROADMAP.md`](docs/ROADMAP.md) for what's done and what's coming next, and [`DEPLOYMENT.md`](DEPLOYMENT.md) for the concrete steps to put this on the actual internet when you're ready.

---

## Stack

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, TanStack Query, React Hook Form + Zod, React Router, react-markdown
- **Backend:** FastAPI, SQLAlchemy, Alembic, Pydantic, SQLite (swappable to Postgres via one env var)
- **Testing:** Pytest (backend), Vitest + React Testing Library (frontend)
- **Dev environment:** Docker Compose (primary) — see below. A manual, no-Docker path also still works; see [Alternative: running without Docker](#alternative-running-without-docker).

---

## Prerequisites

- **Docker Desktop** (includes Docker Compose) — [docker.com](https://www.docker.com/products/docker-desktop/)
- **Git** — check with `git --version`, or get it from [git-scm.com](https://git-scm.com/downloads)

---

## First-time setup

### 1. Copy the env files

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

The defaults just work (SQLite, no AI key). If you have an OpenAI key, put it in `backend/.env` now — see [Where your AI API key goes](#where-your-ai-api-key-goes) below.

### 2. Bring the whole stack up

```bash
docker compose up --build
```

Open `http://localhost:5173` for the app, `http://localhost:8000/docs` for the interactive API docs. Stop with `Ctrl+C` or `docker compose down`.

### 3. Confirm it's actually working

```bash
docker compose exec backend pytest -q
docker compose exec frontend npm test
```

### 4. Getting this onto GitHub (one-time)

1. Create an empty repo named `falante` at [github.com/new](https://github.com/new) (no README/.gitignore there).
2. From the `falante/` root:
   ```bash
   git init
   git add .
   git commit -m "Milestone 1: vocabulary manager + flashcards with spaced repetition"
   git branch -M main
   git remote add origin https://github.com/<your-username>/falante.git
   git push -u origin main
   ```

---

## Day-to-day: applying a new milestone

### 1. Drop the files in

Unzip the milestone zip and copy its `falante/` contents over your existing `falante/` folder.

### 2. Restart the stack

```bash
docker compose up --build
```

`--build` is safe every time. New Alembic migrations apply automatically on backend startup.

**If a milestone added a new Python package**, `--build` alone is enough — the backend has no persistent volume shadowing its installed packages, so a fresh image build picks up the new dependency correctly.

**If a milestone added a new npm package**, `--build` alone is *not* enough — `frontend_node_modules` is a named Docker volume (kept separate from the bind-mounted code specifically so the container's Linux-built packages don't get overwritten by your host's), and that volume's old content persists across rebuilds regardless of what changed in `package.json`. You'll see an error like `Failed to resolve import "..."` for the new package if you skip this. Run:

```bash
docker compose down -v
docker compose up --build
```

`-v` removes that stale volume so npm actually reinstalls. This is safe — it does not touch `backend/falante.db` (a bind-mounted file, not a volume), so no data is lost. I'll call it out explicitly whenever a milestone adds an npm package, but this is the fix any time you see an import-resolution error that shouldn't be there.

### 3. Run the tests

```bash
docker compose exec backend pytest -q
docker compose exec frontend npm test
```

### 4. Commit and push

```bash
git add .
git commit -m "Milestone N: <what it added>"
git push
```

### A note on the `.env` files

`backend/.env` and `frontend/.env` are **not** tracked by git — only `.env.example` is, and `docker-compose.yml` requires `backend/.env` to exist (via `env_file:`).

### A note on the SQLite database and Docker

`backend/falante.db` lives in the bind-mounted `backend/` folder — a real file on your host machine, not trapped in a container. It's the *same* database whether you run via Docker or the manual venv setup, so your data stays consistent either way.

---

## Where your AI API key goes

The Grammar Tutor (on each Grammar Reference topic page) and the Writing Coach both talk to OpenAI. Your key goes in **`backend/.env`** — never in frontend code, never committed to git, never sent to the browser. The backend is the only thing that ever sees it.

`backend/.env.example` has the placeholder:

```bash
AI_PROVIDER=openai
AI_API_KEY=
AI_MODEL=gpt-4o-mini
AI_RATE_LIMIT_PER_DAY=10
```

Paste your real key into `backend/.env` as `AI_API_KEY=sk-...`, then restart (`Ctrl+C` then `docker compose up`) so the container picks it up. If left blank, the app runs completely normally — both AI features show an "AI isn't configured" message instead of crashing, since AI is always optional, never required.

`AI_RATE_LIMIT_PER_DAY` caps how many Tutor + Writing Coach requests a single visitor (by IP) can make per day — this matters once the app is public (see [`DEPLOYMENT.md`](DEPLOYMENT.md)) so a stranger can't run up your OpenAI bill. Locally it barely matters, but it's on by default everywhere so the behavior is the same in dev and production. Change the number and restart to adjust it — no code change needed.

Adding a second provider later (Claude, Gemini) means writing one new file implementing `AIProvider` in `backend/app/services/ai/` and registering it in `factory.py` — nothing else changes, including either AI feature's own code.

---

## Setting up Google Sign-In (Milestone 10, one-time)

Falante uses "Sign in with Google" for accounts — there's no password system to manage. This needs a one-time, free setup in Google Cloud Console to get a **Client ID**, which is what tells Google "this login attempt is for *my* app."

### 1. Create the OAuth consent screen

1. Go to [console.cloud.google.com](https://console.cloud.google.com/) and create a project (or use an existing one) — free, no billing required for this.
2. Go to **APIs & Services → OAuth consent screen**.
3. Choose **External** user type (unless you have a Google Workspace account).
4. Fill in the required fields (app name — "Falante" is fine, your email for support/developer contact). The default scopes (email, profile, openid) are all you need — don't add anything else.
5. Save.

**Important, easy to miss:** a new external app starts in **Testing** mode, which means only email addresses you explicitly add as "test users" can actually sign in — anyone else gets blocked by Google, not by your app. If you want other people (recruiters, friends) to try the live demo, either:
- Add their email addresses individually under **Test users** (works immediately, no review, good for a handful of people), or
- **Publish** the app to Production (Google may ask for a verification review for some scopes, but basic email/profile/openid scopes like this app uses typically don't require one — worth checking Google's current requirements when you get there).

### 2. Create the Client ID

1. Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
2. Application type: **Web application**. Name it "Falante" (or anything).
3. Under **Authorized JavaScript origins**, add:
   - `http://localhost:5173` (local dev)
   - Your real frontend URL once deployed (e.g. `https://falante.vercel.app`) — you can add this later and edit the credential, no need to redo this whole process.
4. Create. Google shows you a **Client ID** that looks like `123456-abc.apps.googleusercontent.com`.

### 3. Put the Client ID in both `.env` files

The *same* Client ID goes in two places — the backend uses it to verify tokens are meant for your app, the frontend uses it to render the actual Google button:

```bash
# backend/.env
GOOGLE_CLIENT_ID=123456-abc.apps.googleusercontent.com

# frontend/.env
VITE_GOOGLE_CLIENT_ID=123456-abc.apps.googleusercontent.com
```

Restart the stack (`docker compose up` again) so both containers pick up the new values. Also set a real `JWT_SECRET_KEY` in `backend/.env` while you're there — see the comment in `.env.example` for how to generate one; the default value is deliberately insecure so you don't forget to change it.

### What's gated behind login

Vocabulary, Flashcards, the Writing Coach, and the Reading Helper all require being logged in — that's your personal data. **The Dashboard is the homepage and is viewable by anyone** — logged out, it shows an intro to the app and an example dashboard with clearly-labeled sample data; logged in, it shows your real stats. Grammar Reference and the Verb Explorer stay fully public and browsable without an account. The Grammar Tutor is a special case: the *article* you're reading stays public, but the chat panel itself shows a "log in to use the tutor" prompt in its place if you're not signed in.

### Troubleshooting sign-in

If clicking the Google button gets you "Couldn't sign you in" or similar, the error message itself now tells you the real reason (as of the latest fix) — check what it actually says first. The most common causes, in order of likelihood:

1. **You edited `.env` but didn't restart the containers.** Both `GOOGLE_CLIENT_ID` and `JWT_SECRET_KEY` are read once when the backend starts — `docker compose up` again (or `Ctrl+C` then back up) after any `.env` change.
2. **The Client ID doesn't match between the two `.env` files.** `backend/.env`'s `GOOGLE_CLIENT_ID` and `frontend/.env`'s `VITE_GOOGLE_CLIENT_ID` must be the exact same value — a typo or copying the Client Secret into one of them by mistake is an easy way to end up with a mismatch.
3. **`CORS_ORIGINS` doesn't include the URL you're actually visiting the frontend from.** If the error says something about not reaching the server at all (rather than a specific rejection reason), check the browser's DevTools → Network tab for a CORS error, and confirm `backend/.env`'s `CORS_ORIGINS` includes that exact origin.
4. **You're not an added test user yet**, if the Google consent screen itself is still in "Testing" mode (see the setup steps above) — this shows as a Google-side error before you even get back to Falante, not the "couldn't sign in" message.

If none of those explain it, check `docker compose logs backend` — unexpected verification failures (including network issues reaching Google from inside the container) are now logged there with the full error, even though the browser only sees a clean summary.

**"Couldn't reach the server" specifically, with the backend container missing entirely from `docker compose ps`:** check `docker compose logs backend` for a crash on startup. Two real causes we hit, both fixed as of the latest update:

- **Any typo in `backend/.env` used to crash the entire backend**, not just fail to use that one setting — a misspelled variable name (even one nothing reads, like an extra `GOOGLE_CLIENT_SECRET` saved "just in case") made the whole app refuse to start with a `pydantic_core.ValidationError: extra_forbidden`. Fixed — `config.py` now explicitly ignores unrecognized `.env` keys instead of rejecting the whole file.
- **The Milestone 10 auth migration used to fail on any database with real pre-existing data**, in two distinct ways depending on exactly which retry you were on: `sqlite3.OperationalError: table users already exists`, a `NOT NULL constraint failed`, or `table _alembic_tmp_flashcard_reviews already exists`. All three come from the same root cause — SQLite's DDL isn't transactional, so a migration that fails partway leaves whatever it already did in place, and a naive retry crashes trying to redo that same step. Fixed — the migration now checks for and cleans up every leftover artifact a real interrupted attempt could produce (an already-created table, an already-added column, or a stale internal scratch table from SQLite's batch-alter process) before doing that step again, so it's safe to retry from any intermediate state. You don't need to manually delete `backend/falante.db` for this migration to succeed, though doing so is also a fine (zero-risk) way to guarantee a clean slate if you'd rather not think about it.

If you're on an older copy of these files, either issue can still show up — updating to the latest versions resolves both.

---

## Project structure

```
falante/
├── README.md                  ← you are here
├── docker-compose.yml         ← one command runs the whole stack
├── docs/                      ← architecture plan + roadmap
├── .github/workflows/ci.yml   ← runs backend + frontend tests on every push (no Docker — plain venv/npm)
├── backend/
│   ├── Dockerfile.dev
│   └── app/
│       ├── core/                config, database setup, seed data
│       ├── models/              SQLAlchemy tables (vocabulary, flashcards, grammar, verbs, writing)
│       ├── schemas/             Pydantic request/response shapes
│       ├── repositories/        raw DB queries, nothing else
│       ├── services/            business logic — SRS scheduling, streak calc, conjugation engine,
│       │                        AI provider abstraction (services/ai/), tutor + writing coach services
│       └── api/v1/              FastAPI routes
└── frontend/
    ├── Dockerfile.dev
    └── src/
        ├── components/ui/           dumb, reusable primitives (Button, Card…)
        ├── components/vocabulary/   Vocabulary + Flashcards feature components
        ├── components/dashboard/    Dashboard feature components
        ├── components/grammar/      Grammar Reference + Tutor feature components
        ├── components/verbs/        Verb Explorer feature components
        ├── components/writing/      Writing Coach feature components
        ├── pages/                   route-level components
        ├── hooks/                   TanStack Query wrappers — all server state
        ├── services/api/            the only files that know the REST endpoints
        └── types/                   shared TypeScript types
```

---

## What's done / what's next

| Milestone | Status |
|---|---|
| 1. Vocabulary Manager + Flashcards (SRS) | ✅ Done |
| 2. Dashboard (streak, stats, recently learned) | ✅ Done |
| 3. Grammar Reference (5 seeded articles) | ✅ Done |
| 4. Verb Conjugation Explorer (85 verbs) | ✅ Done |
| 5. AI abstraction layer + Grammar Tutor (OpenAI) | ✅ Done |
| 6. Docker | ✅ Done |
| 7. AI Writing Coach (structured corrections + vocab suggestions) | ✅ Done |
| 8. Reading Helper (word highlighting, save-to-vocabulary, verb-form recognition) | ✅ Done |
| 9. Production-readiness (rate limiting, prod Docker image, Postgres verified) | ✅ Done |
| 10. Real accounts / login (Google Sign-In, per-user data) | ✅ Done |
| 11. Progress Analytics (5 charts, dedicated page + dashboard customization) | ✅ Done |
| 12. AI Study Assistant | Next |
| 12. AI Study Assistant | Planned |
| 13. Sentence mining | Planned |
| 14. Anki-style import/export | Planned |
| 15. Flashcard UX overhaul (Quizlet-inspired — scope TBD) | Planned |
| — Deployment (Render + Vercel — see [`DEPLOYMENT.md`](DEPLOYMENT.md)) | Whenever ready, not tied to a specific milestone number |

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the full sequence and future ideas beyond the MVP.

---

## Alternative: running without Docker

<details>
<summary>Click to expand the manual setup</summary>

### Prerequisites

- **Python 3.12+**, **Node.js 20+**

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
cp .env.example .env                # skip if you already have one
alembic upgrade head
pytest -q
uvicorn app.main:app --reload
```

Always run these from *inside* `backend/`, venv activated — that's what makes `from app...` imports resolve. This is also exactly how CI runs things (no Docker there).

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npx tsc -b && npm test && npm run lint
npm run dev
```

Both paths read/write the same `backend/falante.db` and `.env` files.

</details>
