FROM python:3.12.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.11.33 /uv /uvx /bin/
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"
WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY backend ./backend
COPY db ./db
COPY scripts/seed_demo.py ./scripts/seed_demo.py
COPY scripts/start_backend.py ./scripts/start_backend.py
RUN uv sync --frozen --no-dev --no-editable \
    && groupadd --gid 10001 omnimed \
    && useradd --uid 10001 --gid omnimed --no-create-home omnimed \
    && chown -R omnimed:omnimed /app
USER omnimed
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=8s --start-period=10s --retries=5 \
  CMD ["python", "-c", "import urllib.request; from scripts.start_backend import runtime_port; urllib.request.urlopen(f'http://127.0.0.1:{runtime_port()}/api/health/ready', timeout=7)"]
CMD ["python", "scripts/start_backend.py"]
