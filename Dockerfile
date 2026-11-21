FROM ghcr.io/astral-sh/uv:0.11.29-python3.13-trixie-slim

# 날짜 조회 노드가 한국 날짜를 돌려주도록 시간대를 맞춘다. slim 이미지에는 시간대 정보가 없다.
RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Seoul \
    PYTHONUTF8=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY src ./src
COPY data ./data
COPY tests ./tests
RUN uv sync --frozen

CMD ["mini-agent-demo"]
