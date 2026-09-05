# Deployment Guide

This is the runbook for putting Falante on the actual internet. It assumes
you're not ready to do this yet and are reading it to know what's involved —
when you are ready, come back and follow it top to bottom.

**Recommended stack:** [Render](https://render.com) for the backend + a managed
Postgres database, [Vercel](https://vercel.com) for the frontend. Both have
real free tiers, both are common enough that naming them means something on
a resume, and neither requires a credit card for the free tier at time of
writing (worth double-checking when you actually sign up, since platforms
change this).

If you'd rather use Railway, Fly.io, or something else, the backend steps
transfer almost directly (any host that can run a Dockerfile + Postgres
works) — the frontend steps are Vercel-specific but Netlify's flow is
nearly identical.

---

## Before you start

- [ ] Milestone 9 (this one) is merged — rate limiting, the production
      Dockerfile, and Postgres compatibility all need to be in place first.
      Deploying without the rate limit means your OpenAI key is exposed to
      unbounded use by anyone who finds the URL.
- [ ] Your code is pushed to GitHub (it should already be, per the
      day-to-day workflow in the main README).
- [ ] You have your OpenAI API key handy (the same one already in your
      local `backend/.env`).

---

## Part 1 — Backend on Render

### 1. Create the Postgres database first

1. In the Render dashboard: **New → PostgreSQL**.
2. Name it `falante-db`, pick the free tier, create it.
3. Once it's up, copy the **Internal Database URL** shown on its page —
   you'll paste this into the backend service's environment variables in a
   moment. (Internal, not External — the backend and database will live in
   the same Render network, so the internal URL is faster and doesn't count
   against any external-connection limits.)

### 2. Create the backend web service

1. **New → Web Service**, connect your GitHub repo.
2. **Root Directory:** `backend`
3. **Runtime:** Docker (Render will find `backend/Dockerfile` automatically
   given the root directory above)
4. **Instance type:** free tier is fine to start.

### 3. Set environment variables on the backend service

In the service's **Environment** tab, add:

| Key | Value |
|---|---|
| `DATABASE_URL` | the Internal Database URL you copied in step 1 |
| `AI_PROVIDER` | `openai` |
| `AI_API_KEY` | your real OpenAI key |
| `AI_MODEL` | `gpt-4o-mini` |
| `AI_RATE_LIMIT_PER_DAY` | `10` (or whatever you want it to be — see [Adjusting the rate limit](#adjusting-the-rate-limit-later) below) |
| `CORS_ORIGINS` | leave this for now — you'll come back and set it after Part 2, once you know your actual Vercel URL |

Deploy. Render will build the Docker image, run the container's `CMD`
(which applies Alembic migrations against the real Postgres database, then
starts the server), and give you a URL like
`https://falante-backend.onrender.com`.

### 4. Confirm it's actually up

```bash
curl https://falante-backend-xxxx.onrender.com/health
```

Should return `{"status":"ok"}`. If it doesn't, check the service's Logs
tab — most first-deploy issues are a missing/misspelled environment
variable.

---

## Part 2 — Frontend on Vercel

1. In the Vercel dashboard: **Add New → Project**, import the same GitHub repo.
2. **Root Directory:** `frontend`
3. Vercel auto-detects Vite — the default build command (`npm run build`)
   and output directory (`dist`) should already be correct.
4. **Environment Variables:** add
   - `VITE_API_URL` = `https://falante-backend-xxxx.onrender.com/api/v1`
     (your actual Render URL from Part 1, plus `/api/v1`)
5. Deploy. You'll get a URL like `https://falante.vercel.app`.

### Now go back and finish the backend CORS setting

Back in Render, set:

| Key | Value |
|---|---|
| `CORS_ORIGINS` | `https://falante.vercel.app` |

(Comma-separate multiple origins if you ever need to — e.g. a custom domain
alongside the `.vercel.app` one: `https://falante.vercel.app,https://falante.com`.)

Redeploy the backend for this to take effect (env var changes require a
restart, same as locally).

---

## Part 3 — Verify the whole thing end to end

Open the Vercel URL in a browser and actually click through:
- Dashboard loads (confirms frontend ↔ backend ↔ Postgres all connected)
- Add a vocabulary word, review a flashcard
- Ask the Grammar Tutor something (confirms the AI key + CORS are both correct)
- Hit the Tutor or Writing Coach more than your rate limit and confirm you
  get the friendly 429 message, not a raw error

---

## Adjusting the rate limit later

Change `AI_RATE_LIMIT_PER_DAY` in Render's environment variables and
redeploy (or just restart the service — no code change needed). This was
built specifically so tightening or loosening it later doesn't require
touching a single line of code.

---

## Cost expectations

- **Render free tier:** the backend web service spins down after a period
  of inactivity and takes ~30–60 seconds to wake up on the next request.
  Fine for a portfolio demo; annoying if you want it to feel instant for a
  recruiter clicking a link cold. Render's paid tier removes this if it
  ever matters enough to pay for.
- **Render Postgres free tier:** has a storage cap and (last checked) an
  expiration window on the free database itself — worth checking Render's
  current docs when you actually set this up, since free-tier terms change.
- **OpenAI cost:** with `gpt-4o-mini` and a 10/day/visitor cap, cost stays
  predictable even under real traffic — worst case is (visitors) × (10) ×
  (cost per request), which for this model is fractions of a cent per
  request.

---

## Custom domain (optional, later)

Once the free subdomains are live and working, both Vercel and Render
support attaching a custom domain from their dashboards (Vercel: Project →
Settings → Domains; Render: service → Settings → Custom Domains). This is a
separate, low-risk step to do whenever you actually own a domain — it
doesn't require re-deploying anything, just DNS records pointed at each
platform's provided target.
