# Roadmap

## Confirmed decisions (from planning discussion)

- **Database:** SQLite for local dev, but the app reads `DATABASE_URL` from environment config everywhere — switching to Postgres later is a one-line `.env` change, no code changes.
- **Dashboard:** pulled forward to Milestone 2, right after the proof of concept.
- **Docker:** added in Milestone 6, dev mode with hot reload — now the primary way the project runs day-to-day. Manual venv/npm setup still works and is what CI uses.
- **AI provider:** OpenAI, confirmed in Milestone 5. Both AI features (Grammar Tutor, Writing Coach) go through the same `AIProvider` abstraction, so adding Claude/Gemini later doesn't touch feature code.
- **Writing Coach (Milestone 7):** corrections come back as a structured, itemized list (original → corrected → explanation, each tagged "grammar" or "wording") rather than freeform prose — via OpenAI JSON mode. Every submission is saved to a `writing_submissions` table. Suggested vocabulary has a one-click "+ Add to my vocabulary" button.
- **Reading Helper (Milestone 8):** fully frontend — "unknown" is determined purely by checking pasted text against the existing Vocabulary Manager list, client-side, no backend changes. No AI, no dictionary API — definitions are manual-entry only, matching the original brief's "no AI required" note for this feature. Already-known words are also clickable, showing a read-only view of what's saved.
- **Verb-form recognition (post-Milestone 8 fix):** a new `POST /verbs/lookup-batch` endpoint reuses the Milestone 4 conjugation engine in reverse — given raw words, it finds which ones are conjugated forms of a known verb. This powers three things: (1) Reading Helper highlighting now treats a conjugated form of an already-known verb as known, not a separate unknown word; (2) saving a recognized verb form saves the infinitive, grouping all conjugated forms under one vocabulary entry instead of creating duplicates; (3) Vocabulary entries that are verbs are now clickable through to the Verb Explorer's conjugation page, which shows a "Back to Vocabulary" link instead of the default "Back to Verb Explorer" when arrived at that way (tracked via React Router `location.state`).
- **Production-readiness (Milestone 9):** the deploy target is Render (backend + managed Postgres) + Vercel (frontend), chosen for real free tiers and name recognition. AI rate limit set to 10 requests/day/visitor (identified by IP, no login system) — deliberately conservative for the first deploy, and built as a per-request env var read (not baked in at import time) specifically so it's a one-line change with no code touch later.
- **CORS config fix (post-Milestone 9):** `cors_origins` had to be changed from a `list[str]` field to a plain `str` field with the parsed list exposed via a property. Pydantic-settings tries to JSON-decode any list-typed field's raw env value before any custom validator runs, so a plain comma-separated value (valid per our own docs) crashed the app at startup. Root-caused and fixed; all four input shapes (comma-separated, JSON list, multiple origins, unset/default) verified working.
- **Deployment decoupled from the milestone sequence:** more features first, deploy "whenever ready" rather than as a fixed next step — see `DEPLOYMENT.md` for the runbook when that time comes.
- **Post-Milestone-9 feature order:** Real Accounts/Login moved to be first among the remaining features (originally 3rd in initial preference) — Progress Analytics, Sentence Mining, and Anki export all touch Vocabulary/review data that should be scoped per-user once login exists, so building auth first avoids retrofitting user-scoping into each of them afterward.

## Milestone sequence

| # | Milestone | Adds | Status |
|---|---|---|---|
| 1 | Proof of concept | Backend skeleton, DB, Vocabulary CRUD, Flashcards + SRS, minimal frontend, CI, tests | ✅ Done |
| 2 | Dashboard | Study streak, stats, recently learned | ✅ Done |
| 3 | Grammar Reference | New `grammar_topics` table + seeded content + search | ✅ Done |
| 4 | Verb Conjugation Explorer | New `verbs` table/seeded dataset + search UI | ✅ Done |
| 5 | AI abstraction layer | `AIService` interface + OpenAI, used first for AI Grammar Tutor | ✅ Done |
| 6 | Docker | Dockerfiles + docker-compose, one command runs the whole stack | ✅ Done |
| 7 | AI Writing Coach | Structured grammar/wording corrections + vocabulary suggestions, saved history, Vocabulary Manager integration | ✅ Done |
| 8 | Reading Helper | Word highlighting (known vs. unknown) + save-to-vocabulary flow, fully client-side. Later extended with verb-form recognition (`POST /verbs/lookup-batch`): conjugated forms of known verbs highlight as known, saving one groups under the infinitive, and Vocabulary verb entries link through to the Verb Explorer with context-aware back-navigation. | ✅ Done |
| 9 | Production-readiness | AI rate limiting (10/day/visitor by default, env-configurable), a production Dockerfile (multi-stage, non-root, no dev deps), Postgres compatibility verified end-to-end against a real Postgres 16 instance, comma-friendly `CORS_ORIGINS` parsing (fixed post-ship — see decisions above), a CI job that builds the production image on every push, and `DEPLOYMENT.md` with concrete Render + Vercel steps | ✅ Done |
| 10 | Real accounts / login | Actual user accounts, replacing the current single-shared-vocabulary model with per-user data. The foundation everything below builds on. | Next |
| 11 | Progress Analytics | Charts over `flashcard_reviews` + `writing_submissions` data, scoped per-user | Planned |
| 12 | AI Study Assistant | A general chat (separate from the topic-scoped Grammar Tutor) that gives hints and asks follow-up questions rather than answers outright — reuses the existing `AIProvider` abstraction | Planned |
| 13 | Sentence mining | Save a full highlighted sentence from Reading Helper as a vocabulary entry's example sentence, not just the single word | Planned |
| 14 | Anki-style import/export | Import a CSV (or `.apkg`) into Vocabulary; export your vocabulary back out | Planned |
| 15 | Flashcard UX overhaul | Reworking the flashcard study flow to feel more like Quizlet's — exact scope still to be discussed | Planned |
| — | Deployment | Stand up Render (backend + Postgres) and Vercel (frontend) per `DEPLOYMENT.md`. Not tied to a specific milestone number — pursued whenever ready, after however many of the above are done | Whenever ready |
| — | Polish pass | Dark mode toggle, loading/error states everywhere, accessibility audit | Planned, unscheduled |

## Future ideas (post-MVP, from the original brief)

Speech pronunciation scoring · speech recognition · conversation practice · adaptive lesson generation · personalized learning paths · AI-generated quizzes · OCR from textbook pages · camera translation · word frequency analysis · offline mode / PWA · audio pronunciation · gamification & achievements · daily challenges · teacher/classroom mode · mobile app · embeddings for semantic vocabulary search · ML-driven adaptive spaced repetition.

(Sentence mining and Anki import/export were promoted from this list to Milestones 13–14 above.)

None of these require architectural changes to Milestone 1 — the repository/service split and the `AIService` abstraction are what make adding them later cheap.
