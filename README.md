# Falante

An AI-assisted Brazilian Portuguese learning platform — a companion study tool for college students, independent learners, travelers, and heritage speakers.

**Status:** Milestones 1–6 complete — Vocabulary Manager, Flashcards (spaced repetition), Dashboard, Grammar Reference, Verb Conjugation Explorer, an AI-powered Grammar Tutor (OpenAI), and Docker, all full-stack and tested end to end.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full design plan and [`docs/ROADMAP.md`](docs/ROADMAP.md) for what's done and what's coming next.

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

That's genuinely it for day-to-day work — Docker Compose handles Python and Node inside the containers, so you don't need them installed on your host machine at all anymore. (You'll still want them installed if you ever want to run things outside Docker — see the alternative section.)

---

## First-time setup

### 1. Copy the env files

Docker Compose reads these directly, so they need to exist before the first `docker compose up` (this is the one step Compose can't do for you):

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

The defaults just work (SQLite, no AI key). If you have an OpenAI key for the Grammar Tutor, put it in `backend/.env` now — see [Where your AI API key goes](#where-your-ai-api-key-goes) below.

### 2. Bring the whole stack up

From the `falante/` root folder:

```bash
docker compose up --build
```

First run takes a minute or two (building both images, installing dependencies inside them). Every run after that is fast — Docker caches the dependency-install layer and only reinstalls when `requirements.txt`/`package.json` actually change.

This single command:
- Builds and starts the backend (applies any pending Alembic migrations automatically, then starts FastAPI with hot reload)
- Builds and starts the frontend (Vite dev server with hot reload)
- Leaves both running with logs streaming in your terminal

Open `http://localhost:5173` for the app, `http://localhost:8000/docs` for the interactive API docs.

Stop everything with `Ctrl+C`, or run `docker compose down` from another terminal.

### 3. Confirm it's actually working

In a second terminal, with the stack still running:

```bash
docker compose exec backend pytest -q
docker compose exec frontend npm test
```

Both should pass clean — same as the CI pipeline runs on every push.

### 4. Getting this onto GitHub (one-time)

1. **Create the repo on GitHub first** (don't create a README/`.gitignore` there — we already have ours):
   - Go to [github.com/new](https://github.com/new)
   - Name it `falante`
   - Leave it empty (no README, no .gitignore, no license — we already have those)
   - Click **Create repository**
   - Copy the repo URL it shows you (something like `https://github.com/<your-username>/falante.git`)

2. **Initialize git locally and make your first commit**, from the `falante/` root folder:

   ```bash
   cd falante
   git init
   git add .
   git commit -m "Milestone 1: vocabulary manager + flashcards with spaced repetition"
   ```

3. **Connect your local repo to GitHub and push:**

   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/falante.git
   git push -u origin main
   ```

   Refresh the GitHub page — your code should be there.

---

## Day-to-day: applying a new milestone

Each time I hand you a new milestone's files, you're just dropping updated/new files into a project that's already fully set up. Here's the actual loop:

### 1. Drop the files in

Unzip the milestone zip and copy its `falante/` contents over your existing `falante/` folder. It'll only touch the files that are new or changed for that milestone.

### 2. Restart the stack

```bash
docker compose up --build
```

`--build` is safe to run every time — Docker skips rebuilding anything that hasn't changed, so this is fast unless a milestone actually added a new dependency (I'll always call that out when it happens). New Alembic migrations get applied automatically on backend startup, same as before. Code changes hot-reload without needing this command at all if the stack's already running — `--build` is really only for picking up new dependencies.

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

That's the whole loop.

### A note on the `.env` files

`backend/.env` and `frontend/.env` are **not** tracked by git (see `.gitignore`) — only `.env.example` is, and `docker-compose.yml` specifically requires `backend/.env` to exist (via `env_file:`) — that's why it's a first-time setup step rather than something Compose creates for you. Secrets like your AI API key should never be committed, which is exactly what keeping them out of git accomplishes.

### A note on the SQLite database and Docker

`backend/falante.db` lives in the bind-mounted `backend/` folder, which means it's a real file on your host machine — not something trapped inside a container. It survives `docker compose down` and `docker compose up` automatically, no separate Docker volume needed. It's also the *same* database file whether you run the backend via Docker or via the manual venv setup below, so your data stays consistent no matter which way you run things.

---

## Where your AI API key goes

The Grammar Tutor (embedded on each Grammar Reference topic page) talks to OpenAI. Your key goes in **`backend/.env`** — never in frontend code, never committed to git, and never sent to the browser. The backend is the only thing that ever sees it; the frontend just calls your own `/api/v1/tutor/ask` endpoint, which calls OpenAI on the backend's behalf.

`backend/.env.example` has the placeholder:

```bash
AI_PROVIDER=openai
AI_API_KEY=
AI_MODEL=gpt-4o-mini
```

Paste your real key into `backend/.env` (not `.env.example`) as `AI_API_KEY=sk-...`. If the stack is already running via Docker Compose, restart it (`Ctrl+C` then `docker compose up`) so the container picks up the new value — `env_file` values are only read at container start. If `AI_API_KEY` is left blank, the app runs completely normally; the tutor just shows an "AI isn't configured" message instead of a chat box, per the original requirement that AI is always optional, never required.

Adding a second provider later (Claude, Gemini) means writing one new file implementing `AIProvider` in `backend/app/services/ai/` and registering it in `factory.py` — nothing else in the app needs to change, including the frontend.

---

## Project structure

```
falante/
├── README.md                  ← you are here
├── docker-compose.yml         ← one command runs the whole stack
├── docs/                      ← architecture plan + roadmap
├── .github/workflows/ci.yml   ← runs backend + frontend tests on every push (no Docker — plain venv/npm, see below)
├── backend/
│   ├── Dockerfile.dev
│   └── app/
│       ├── core/                config, database setup, seed data
│       ├── models/              SQLAlchemy tables (vocabulary, flashcards, grammar, verbs)
│       ├── schemas/             Pydantic request/response shapes
│       ├── repositories/        raw DB queries, nothing else
│       ├── services/            business logic (SRS scheduling, streak calc, conjugation engine, AI provider abstraction)
│       └── api/v1/              FastAPI routes
└── frontend/
    ├── Dockerfile.dev
    └── src/
        ├── components/ui/           dumb, reusable primitives (Button, Card…)
        ├── components/vocabulary/   Vocabulary + Flashcards feature components
        ├── components/dashboard/    Dashboard feature components
        ├── components/grammar/      Grammar Reference + Tutor feature components
        ├── components/verbs/        Verb Explorer feature components
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
| 7. AI Writing Coach | Next |

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the full sequence and future ideas beyond the MVP. Each milestone follows the same pattern: new model → schema → repository → service → route on the backend, new type → api service → hook → components → page on the frontend.

---

## Alternative: running without Docker

Docker is the recommended day-to-day path now, but the manual setup still works — useful if Docker itself is ever unavailable, or if you want to poke around with a debugger attached directly rather than through a container.

<details>
<summary>Click to expand the manual setup</summary>

### Prerequisites

- **Python 3.12+** — check with `python3 --version`, get it from [python.org](https://www.python.org/downloads/)
- **Node.js 20+** — check with `node --version`, get it from [nodejs.org](https://nodejs.org/) (LTS version)

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
cp .env.example .env                # skip if you already have one from the Docker setup
alembic upgrade head
pytest -q
uvicorn app.main:app --reload
```

**Important:** always run backend commands (`alembic`, `pytest`, `uvicorn`) from *inside* the `backend/` folder, with the venv activated. That's what makes `from app...` imports resolve correctly — `backend/` is the Python source root, not the repo root. This is also exactly how the CI pipeline (`.github/workflows/ci.yml`) runs things — no Docker there, just plain venv/npm, which is why it's worth keeping this path working even with Docker as the daily default.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env                # skip if you already have one from the Docker setup
npx tsc -b && npm test && npm run lint   # optional, confirms everything's healthy
npm run dev
```

Both paths read/write the exact same `backend/falante.db` and the exact same `.env` files, so you can freely switch between Docker and manual on the same machine without losing data or reconfiguring anything.

</details>
