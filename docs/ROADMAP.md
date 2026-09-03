# Roadmap

## Confirmed decisions (from planning discussion)

- **Database:** SQLite for local dev, but the app reads `DATABASE_URL` from environment config everywhere — switching to Postgres later is a one-line `.env` change, no code changes.
- **Dashboard:** pulled forward to Milestone 2, right after the proof of concept.
- **Docker:** added in Milestone 6, dev mode with hot reload — now the primary way the project runs day-to-day. Manual venv/npm setup still works and is what CI uses.
- **AI provider:** OpenAI, confirmed in Milestone 5. Both AI features (Grammar Tutor, Writing Coach) go through the same `AIProvider` abstraction, so adding Claude/Gemini later doesn't touch feature code.
- **Writing Coach (Milestone 7):** corrections come back as a structured, itemized list (original → corrected → explanation, each tagged "grammar" or "wording") rather than freeform prose — via OpenAI JSON mode. Every submission is saved to a `writing_submissions` table. Suggested vocabulary has a one-click "+ Add to my vocabulary" button.
- **Reading Helper (Milestone 8):** fully frontend — "unknown" is determined purely by checking pasted text against the existing Vocabulary Manager list, client-side, no backend changes. No AI, no dictionary API — definitions are manual-entry only, matching the original brief's "no AI required" note for this feature. Already-known words are also clickable, showing a read-only view of what's saved.
- **Verb-form recognition (post-Milestone 8 fix):** a new `POST /verbs/lookup-batch` endpoint reuses the Milestone 4 conjugation engine in reverse — given raw words, it finds which ones are conjugated forms of a known verb. This powers three things: (1) Reading Helper highlighting now treats a conjugated form of an already-known verb as known, not a separate unknown word; (2) saving a recognized verb form saves the infinitive, grouping all conjugated forms under one vocabulary entry instead of creating duplicates; (3) Vocabulary entries that are verbs are now clickable through to the Verb Explorer's conjugation page, which shows a "Back to Vocabulary" link instead of the default "Back to Verb Explorer" when arrived at that way (tracked via React Router `location.state`).

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
| 8 | Reading Helper | Word highlighting (known vs. unknown) + save-to-vocabulary flow, fully client-side | ✅ Done |
| 9 | Progress Analytics | Charts over `flashcard_reviews` + `writing_submissions` data | Next |
| 10 | Polish pass | Dark mode toggle, loading/error states everywhere, accessibility audit, deploy | Planned |

## Future ideas (post-MVP, from the original brief)

Speech pronunciation scoring · speech recognition · conversation practice · adaptive lesson generation · personalized learning paths · AI-generated quizzes · OCR from textbook pages · camera translation · sentence mining · Anki import/export · word frequency analysis · offline mode / PWA · audio pronunciation · gamification & achievements · daily challenges · teacher/classroom mode · mobile app · embeddings for semantic vocabulary search · ML-driven adaptive spaced repetition.

None of these require architectural changes to Milestone 1 — the repository/service split and the `AIService` abstraction are what make adding them later cheap.
