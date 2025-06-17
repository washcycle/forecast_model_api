FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /build

COPY pyproject.toml pyproject.toml
COPY --from=ghcr.io/astral-sh/uv:0.7.12 /uv /uvx /bin/

# add lightgbm system dependency
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

RUN uv sync

FROM python:3.12-slim AS runtime

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libgomp.so.1

COPY model/lgbm_model.txt /app/lgbm_model.txt

RUN adduser --disabled-password --gecos '' app 

COPY --chown=app:app src/app.py /app/app.py

RUN chown root:app /app/.venv/bin/uvicorn && chmod 750 /app/.venv/bin/uvicorn

USER app

# tried uvicorn but it's missing some system depdencies
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]