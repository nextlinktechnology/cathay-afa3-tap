FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

EXPOSE 8080

ENTRYPOINT ["uv", "run", "uvicorn", "agent_a2a_server:a2a_app", "--host", "0.0.0.0", "--port", "8080"]
