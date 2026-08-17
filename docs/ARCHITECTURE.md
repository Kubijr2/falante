# Falante — Architecture & Roadmap Plan

**Status:** Draft for approval — no code yet
**Approach:** Proof-of-concept first, then layer on features milestone by milestone

---

## 1. What We're Actually Building First

Full scope (all 7 core features + 3 AI features) is the *end state*, not the starting point. We're going to build a **thin vertical slice** first — a real, working, deployable app with a narrow feature set — then widen it.

**Proof-of-concept (Milestone 1) includes:**
- Vocabulary Manager (add/edit/delete/categorize words)
- Flashcards with flip animation + basic spaced repetition
- A working FastAPI backend + SQLite database + React frontend talking to each other over a real REST API

That's it. No Dashboard, no AI, no Grammar Reference yet. This is intentional — it proves the entire stack end-to-end (DB → API → frontend → UI) on the smallest surface area possible, which is exactly what makes it easy to build onto.

Everything after that is additive: new tables, new routers, new pages, new components — never a rewrite.

---

## 2. Tech Stack Justification

| Choice | Why |
|---|---|
| **React + TypeScript + Vite** | Type safety catches bugs before runtime; Vite gives instant HMR, standard for modern SWE roles |
| **Tailwind CSS** | Fast, consistent styling without a CSS-file sprawl; easy dark mode |
| **TanStack Query** | Proper server-state caching/invalidation instead of manual `useEffect` fetch spaghetti — this alone is a strong signal to reviewers |
| **React Hook Form + Zod** | Type-safe form validation shared logically between frontend and backend Pydantic schemas |
| **FastAPI** | Async, auto-generates OpenAPI docs, Pydantic-native — reads as "knows modern backend practice" |
| **SQLAlchemy + Alembic** | Real migrations from day one, not `db.create_all()` — shows you understand schema evolution |
| **SQLite → Postgres-ready** | SQLite for zero-friction local dev; schema designed so swapping to Postgres later is a config change, not a rewrite |
| **Pytest / Vitest** | Industry-standard, both ecosystems |
| **Docker** | One command to run the whole stack — this is what makes it demo-able in an interview |

---

## 3. Folder Structure (Milestone 1 scope, full tree pre-planned)

```
falante/
├── README.md
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── ARCHITECTURE.md          (this doc, checked into the repo)
│   ├── API.md
│   └── ROADMAP.md
├── scripts/
│   └── setup.sh
├── backend/
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── alembic/
│   │   └── versions/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── vocabulary.py
│   │   │   └── flashcard.py
│   │   ├── schemas/
│   │   │   ├── vocabulary.py
│   │   │   └── flashcard.py
│   │   ├── repositories/
│   │   │   ├── vocabulary_repository.py
│   │   │   └── flashcard_repository.py
│   │   ├── services/
│   │   │   ├── vocabulary_service.py
│   │   │   └── srs_service.py          (spaced repetition logic, isolated)
│   │   └── api/
│   │       └── v1/
│   │           ├── vocabulary.py
│   │           └── flashcards.py
│   └── tests/
│       ├── test_vocabulary.py
│       └── test_srs_service.py
└── frontend/
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.ts
    ├── Dockerfile
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── components/
        │   ├── ui/                     (Button, Card, Badge — dumb/reusable)
        │   └── vocabulary/
        │       ├── VocabularyList.tsx
        │       ├── VocabularyForm.tsx
        │       └── FlashcardDeck.tsx
        ├── pages/
        │   ├── VocabularyPage.tsx
        │   └── FlashcardsPage.tsx
        ├── hooks/
        │   ├── useVocabulary.ts        (wraps TanStack Query)
        │   └── useFlashcardSession.ts
        ├── services/
        │   └── api/
        │       ├── client.ts           (Axios instance)
        │       └── vocabulary.ts
        ├── types/
        │   └── vocabulary.ts
        └── utils/
            └── srs.ts                  (client-side display helpers only — real SRS logic lives on backend)
```

Everything under `grammar/`, `dashboard/`, `ai/`, `analytics/` gets added as its own vertical slice (backend model → schema → repo → service → route, frontend type → api service → hook → components → page) in later milestones — same pattern each time, so it becomes a repeatable rhythm rather than new architecture every time.

---

## 4. Database Schema (Milestone 1)

**`vocabulary`**
| column | type | notes |
|---|---|---|
| id | int, PK | |
| portuguese | str | |
| english | str | |
| example_sentence | str, nullable | |
| notes | str, nullable | |
| category | str, nullable | e.g. "food", "travel" |
| tags | str (JSON-encoded list), nullable | |
| difficulty | enum: easy/medium/hard | |
| mastery_level | int (0–5) | drives SRS interval |
| next_review_at | datetime | |
| created_at | datetime | |
| updated_at | datetime | |

**`flashcard_reviews`**
| column | type | notes |
|---|---|---|
| id | int, PK | |
| vocabulary_id | int, FK → vocabulary.id | |
| reviewed_at | datetime | |
| result | enum: again/hard/medium/easy | |
| interval_days_before | int | |
| interval_days_after | int | |

This gives us a real review history table from day one — later "Progress Analytics" just queries this table instead of needing a new one.

Full future schema (Users, GrammarTopics, StudySessions, VerbBookmarks, Settings, APIKeys) is documented in `docs/ROADMAP.md` but **not created yet** — no empty unused tables in migration 1.

---

## 5. API Routes (Milestone 1)

```
GET    /api/v1/vocabulary              list (supports ?category=&tag=&search=)
POST   /api/v1/vocabulary              create
GET    /api/v1/vocabulary/{id}         detail
PATCH  /api/v1/vocabulary/{id}         update
DELETE /api/v1/vocabulary/{id}         delete

GET    /api/v1/flashcards/due          words due for review today
POST   /api/v1/flashcards/{vocab_id}/review   submit a review result (again/hard/medium/easy) → SRS service recalculates next_review_at
```

Auto-generated OpenAPI docs live at `/docs` via FastAPI — free interview-demo material.

---

## 6. UI Wireframes (text)

**Vocabulary Page**
```
┌─────────────────────────────────────────┐
│ Falante          [Vocabulary] [Flashcards]│
├─────────────────────────────────────────┤
│  [+ Add Word]         [search] [filter▾] │
│                                           │
│  ┌───────────────┐  ┌───────────────┐    │
│  │ falar          │  │ saudade        │   │
│  │ to speak       │  │ longing        │   │
│  │ 🏷 verbs       │  │ 🏷 culture     │   │
│  │ ●●●○○ mastery  │  │ ●○○○○ mastery  │   │
│  └───────────────┘  └───────────────┘    │
└─────────────────────────────────────────┘
```

**Flashcards Page**
```
┌─────────────────────────────────────────┐
│              12 cards due today          │
│                                           │
│           ┌─────────────────┐            │
│           │                 │            │
│           │     saudade     │  (tap to   │
│           │                 │   flip)    │
│           └─────────────────┘            │
│                                           │
│   [Again]  [Hard]  [Medium]  [Easy]      │
└─────────────────────────────────────────┘
```

---

## 7. Component Hierarchy (Milestone 1)

```
App
├── Layout (nav + shell)
│   ├── VocabularyPage
│   │   ├── VocabularyForm       (add/edit — controlled by RHF+Zod)
│   │   └── VocabularyList
│   │       └── VocabularyCard (× n)
│   └── FlashcardsPage
│       └── FlashcardDeck
│           └── Flashcard (flip animation, isolated component)
└── ui/ (Button, Card, Badge, Input, Modal — shared, no business logic)
```

Rule carried through the whole project: **page components fetch data via hooks and pass props down; presentational components never call the API directly.**

---

## 8. State Management Plan

- **Server state** (vocabulary, flashcards, review history): TanStack Query exclusively — no Redux/Zustand needed at this scale. Query keys namespaced (`['vocabulary', filters]`) so cache invalidation stays predictable as features grow.
- **Local/UI state** (form inputs, modal open/closed, current flashcard index): plain `useState`/`useReducer` inside the component that owns it.
- **No global client state store** until/unless a real cross-cutting need appears (e.g. AI chat session state in a later milestone) — avoids over-engineering the POC.

---

## 9. Roadmap & Milestones

Each milestone is independently buildable, testable, and committable — matching your rule of never generating everything at once.

| # | Milestone | Adds |
|---|---|---|
| **1** | **Proof of concept** | Backend skeleton, DB, Vocabulary CRUD, Flashcards + SRS, minimal frontend, Docker, CI skeleton, tests |
| 2 | Dashboard | Study streak, stats, recently learned — reads from existing tables, no new backend needed beyond one aggregation endpoint |
| 3 | Grammar Reference | New `grammar_topics` table + static seeded content + search |
| 4 | Verb Conjugation Explorer | New `verbs` table or seeded JSON dataset + search UI |
| 5 | AI abstraction layer | `AIService` interface, one concrete provider (your key), used first for AI Grammar Tutor (lowest-risk AI feature) |
| 6 | AI Writing Coach | Builds on the AI layer from M5 |
| 7 | Reading Helper | Word highlighting + save-to-vocabulary flow |
| 8 | Progress Analytics | Charts over `flashcard_reviews` + study session data |
| 9 | Polish pass | Dark mode, loading/error states, skeletons, accessibility audit, deploy |

This ordering is deliberately picked so the **resume-worthy full-stack proof (M1)** exists fast, and every milestone after it is a self-contained, demo-able increment you can commit and even screenshot for a resume/portfolio update as you go.

---

## 10. What I Need From You Before We Start Coding

1. Do you want the DB to stay SQLite for the whole semester, or should I set up the config so switching to Postgres later is trivial (I'd default to "yes, make it swappable" — costs nothing now)?
2. Any objection to the milestone order above, or something you'd rather pull forward (e.g. Dashboard before Flashcards)?
3. Once you approve, I'll walk you through local setup step-by-step (Python/Node versions, Docker or no Docker, running migrations) as part of Milestone 1 delivery — want Docker included in M1, or plain local Python/Node venv first and Docker added later as its own milestone?
