# Roadmap

## Confirmed decisions (from planning discussion)

- **Database:** SQLite for local dev, but the app reads `DATABASE_URL` from environment config everywhere — switching to Postgres later is a one-line `.env` change, no code changes.
- **Dashboard:** pulled forward to Milestone 2, right after the proof of concept.
- **Docker:** added in Milestone 6, dev mode with hot reload — now the primary way the project runs day-to-day. Manual venv/npm setup still works and is what CI uses.

## Milestone sequence

| # | Milestone | Adds | Status |
|---|---|---|---|
| 1 | Proof of concept | Backend skeleton, DB, Vocabulary CRUD, Flashcards + SRS, minimal frontend, CI, tests | ✅ Done |
| 2 | Dashboard | Study streak, stats, recently learned — one new aggregation endpoint over existing tables | ✅ Done |
| 3 | Grammar Reference | New `grammar_topics` table + seeded content + search | ✅ Done |
| 4 | Verb Conjugation Explorer | New `verbs` table/seeded dataset + search UI | ✅ Done |
| 5 | AI abstraction layer | `AIService` interface + one provider (your key), used first for AI Grammar Tutor | ✅ Done |
| 6 | Docker | Dockerfiles + docker-compose for backend + frontend, so the whole stack runs with one command | ✅ Done |
| 7 | AI Writing Coach | Builds on the AI layer from Milestone 5 | Next |
| 8 | Reading Helper | Word highlighting + save-to-vocabulary flow | Planned |
| 9 | Progress Analytics | Charts over `flashcard_reviews` + study session data | Planned |
| 10 | Polish pass | Dark mode toggle, loading/error states everywhere, accessibility audit, deploy | Planned |

## Future ideas (post-MVP, from the original brief)

Speech pronunciation scoring · speech recognition · conversation practice · adaptive lesson generation · personalized learning paths · AI-generated quizzes · OCR from textbook pages · camera translation · sentence mining · Anki import/export · word frequency analysis · offline mode / PWA · audio pronunciation · gamification & achievements · daily challenges · teacher/classroom mode · mobile app · embeddings for semantic vocabulary search · ML-driven adaptive spaced repetition.

None of these require architectural changes to Milestone 1 — the repository/service split and the `AIService` abstraction (Milestone 5) are what make adding them later cheap.
