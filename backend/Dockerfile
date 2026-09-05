# ---- Build stage: install dependencies into an isolated location ----
FROM python:3.12-slim AS builder

WORKDIR /app

# Only the runtime dependencies — no pytest/httpx/etc from requirements-dev.txt.
COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Runtime stage: copy only what's needed to actually run the app ----
FROM python:3.12-slim

WORKDIR /app

# Non-root user — a container running as root is a bigger blast radius if
# anything in the dependency chain is ever compromised, for no benefit here.
RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN chown -R appuser:appuser /app

USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Applies any pending migrations, then starts the server — no --reload,
# no bind-mounted code, just the image as built.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
