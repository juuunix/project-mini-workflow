"""mini_workflow 패키지의 로그를 한 줄에 JSON 객체 하나로(JSON Lines) 파일에 남기는 설정.

모든 줄은 같은 바깥 칸(time, level, logger, run, event)을 가지고, 이벤트마다 다른 값은
data 하나에 담는다. data에 무엇이 들어갈지는 이벤트가 정한다(Event의 설명).

각 모듈은 log_event()로 기록만 하고, 프로그램을 시작하는 곳에서 file_logging()으로
파일 기록을 켠다. 켜지 않으면(예: 테스트) 파일이 생기지 않는다.
"""

import json
import logging
import sys
from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from enum import StrEnum
from logging.handlers import RotatingFileHandler
from pathlib import Path

from mini_workflow import messages

LOG_FILE = Path("logs") / "mini-workflow.log"
# 파일이 1MB를 넘으면 예전 파일로 돌려 3개까지 남겨, 로그 전체가 4MB를 넘지 않게 한다.
LOG_MAX_BYTES = 1_000_000
LOG_BACKUP_COUNT = 3
PACKAGE_LOGGER = "mini_workflow"


class Event(StrEnum):
    """로그에 남기는 이벤트와 그 data의 칸."""

    SCENARIO_START = "scenario_start"  # scenario
    SCENARIO_END = "scenario_end"  # status
    SCENARIO_CRASHED = "scenario_crashed"  # scenario, error, traceback
    DOCS_LOAD_FAILED = "docs_load_failed"  # docs_dir, error, traceback
    NODE_START = "node_start"  # node, node_run
    NODE_END = "node_end"  # node, output
    NODE_FAILED = "node_failed"  # node, error, traceback
    ERROR_HANDLED = "error_handled"  # node, output
    RUN_FINISHED = "run_finished"  # steps
    RUN_STOPPED = "run_stopped"  # kind, node, detail
    LLM_ATTEMPT_FAILED = "llm_attempt_failed"  # attempt, error


# 지금 실행 중인 질문의 번호. 시연이 정하고, 그동안 남는 모든 줄에 run으로 붙는다.
# 엔진과 노드는 이 번호를 몰라도 된다.
current_run: ContextVar[int | None] = ContextVar("current_run", default=None)


@contextmanager
def log_run(run: int) -> Generator[None]:
    """with 블록 안에서 남는 로그에 run 번호를 붙인다."""
    token = current_run.set(run)
    try:
        yield
    finally:
        current_run.reset(token)


def log_event(
    logger: logging.Logger,
    level: int,
    event: Event,
    *,
    exc_info: bool = False,
    **data: object,
) -> None:
    """이벤트 하나를 남긴다. 로그는 모두 이 함수로만 남긴다."""
    # stacklevel=2: 기록 위치를 이 함수가 아니라 부른 곳으로 남긴다.
    logger.log(
        level,
        event,
        exc_info=exc_info,
        extra={"event": event, "data": data},
        stacklevel=2,
    )


class JsonLinesFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = dict(getattr(record, "data", {}))
        if record.exc_info:
            data["traceback"] = self.formatException(record.exc_info)
        line = {
            "time": datetime.fromtimestamp(record.created).isoformat(
                timespec="milliseconds"
            ),
            "level": record.levelname,
            "logger": record.name,
            "run": current_run.get(),
            "event": getattr(record, "event", record.getMessage()),
            "data": data,
        }
        return to_log_json(line)


@contextmanager
def file_logging(path: Path = LOG_FILE) -> Generator[None]:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(
            path, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT, encoding="utf-8"
        )
    except OSError as error:
        # 로그를 남길 수 없는 상황이라 logging이 아닌 화면(stderr)으로 알린다.
        print(messages.log_file_unavailable(error), file=sys.stderr)
        yield
        return
    handler.setFormatter(JsonLinesFormatter())
    logger = logging.getLogger(PACKAGE_LOGGER)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    try:
        yield
    finally:
        logger.removeHandler(handler)
        handler.close()


def to_log_json(value: object) -> str:
    """로그에 남길 값을 JSON 한 줄로 바꾼다. 한글은 그대로 둔다.

    로그에 남기는 값은 모두 이 함수를 거친다. 개인정보처럼 가려야 할 값이 생기면 여기서 가린다.
    """
    return json.dumps(value, ensure_ascii=False, default=jsonable)


def jsonable(value: object) -> object:
    """JSON이 모르는 값을 바꾼다.

    LangChain 메시지는 필드를 원본 그대로 꺼내되, 정보가 없는 빈 칸({}, [], null)은 뺀다.
    나머지는 글자로 바꾼다.
    """
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        fields = model_dump()
        return {key: item for key, item in fields.items() if item not in EMPTY_VALUES}
    return str(value)


EMPTY_VALUES: tuple[object, ...] = (None, {}, [])
