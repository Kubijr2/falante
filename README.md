# Falante

An AI-assisted Brazilian Portuguese learning platform — a companion study tool for college students, independent learners, travelers, and heritage speakers.

**Status:** Milestones 1–8 complete — Vocabulary Manager, Flashcards (spaced repetition), Dashboard, Grammar Reference, Verb Conjugation Explorer, an AI Grammar Tutor, an AI Writing Coach, Docker, and a Reading Helper, all full-stack and tested end to end.

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

`--build` is safe every time — Docker skips rebuilding anything unchanged. New Alembic migrations apply automatically on backend startup.

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
```

Paste your real key into `backend/.env` as `AI_API_KEY=sk-...`, then restart (`Ctrl+C` then `docker compose up`) so the container picks it up. If left blank, the app runs completely normally — both AI features show an "AI isn't configured" message instead of crashing, since AI is always optional, never required.

Adding a second provider later (Claude, Gemini) means writing one new file implementing `AIProvider` in `backend/app/services/ai/` and registering it in `factory.py` — nothing else changes, including either AI feature's own code.

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
| 8. Reading Helper (word highlighting, save-to-vocabulary) | ✅ Done |
| 9. Progress Analytics | Next |

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
