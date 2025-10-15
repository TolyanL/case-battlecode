FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set uv environment variables
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /code

# Install project dependencies.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy source code and virtual environment from the builder stage
COPY . /code

# Synchronize the virtual environment
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.12-slim-bookworm

# Create a new user and group
RUN addgroup --system app && adduser --system --group app

WORKDIR /code

# Copy the virtual environment from the builder stage
COPY --from=builder --chown=app:app /code /code

# Copy the entrypoint script
COPY --chown=app:app entrypoint.sh /entrypoint.sh

ENV PATH="/code/.venv/bin:$PATH"

USER app

WORKDIR /code/battlecode

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "battlecode.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=4", "--log-file=-" , "--access-logfile=-", "--worker-tmp-dir=/dev/shm"]
