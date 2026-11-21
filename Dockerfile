FROM ghcr.io/astral-sh/uv:0.11.29-python3.13-alpine

# TZ: 날짜 조회 노드가 한국 날짜를 돌려주도록 시간대를 맞춘다. 시간대 정보는 기본 이미지에 들어 있다.
ENV TZ=Asia/Seoul \
    PYTHONUTF8=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-default-groups --group test

COPY src ./src
COPY data ./data
COPY tests ./tests
RUN uv sync --frozen --no-default-groups --group test

CMD ["mini-agent-demo"]
