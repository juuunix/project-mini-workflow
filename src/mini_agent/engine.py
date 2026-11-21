import logging
import traceback
from collections import Counter
from collections.abc import Mapping
from typing import Any

from langgraph.errors import GraphRecursionError
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import TaskResultPayload

from mini_agent import messages
from mini_agent.log import Event, log_event
from mini_agent.result import (
    ExecutionRecord,
    RecordKind,
    RunResult,
    StopKind,
    StopReason,
)

# LangGraph가 노드 B의 오류 처리기를 "__error_handler__B"라는 이름으로 실행한다.
ERROR_HANDLER_PREFIX = "__error_handler__"


DEFAULT_RECURSION_LIMIT = 20

logger = logging.getLogger(__name__)


def run_graph(
    graph: CompiledStateGraph,
    initial_state: dict[str, Any],
    recursion_limit: int = DEFAULT_RECURSION_LIMIT,
    node_limits: Mapping[str, int] | None = None,
) -> RunResult:
    history: list[ExecutionRecord] = []
    state: dict[str, Any] = initial_state
    # 그래프 밖으로 올라온 예외가 노드가 던진 것인지 가리려고, 종료 이벤트의 예외를 기억해 둔다.
    failed_node: str | None = None
    node_error: object = None
    limits = node_limits or {}
    run_counts: Counter[str] = Counter()

    try:
        for part in graph.stream(
            initial_state,
            {"recursion_limit": recursion_limit},
            stream_mode=["tasks", "values"],
            version="v2",
        ):
            if part["type"] == "values":
                state = part["data"]
            elif part["type"] == "tasks":
                event = part["data"]
                if "input" in event:
                    # 시작 이벤트는 노드 본문보다 먼저 오므로, 여기서 멈추면 넘친 실행은 일어나지 않는다.
                    name = event["name"]
                    run_counts[name] += 1
                    limit = limits.get(name)
                    if limit is not None and run_counts[name] > limit:
                        stop_reason = StopReason(
                            kind=StopKind.NODE_LIMIT_EXCEEDED,
                            node=name,
                            detail=messages.node_limit_detail(limit),
                        )
                        return stopped(history, state, stop_reason)
                    log_event(
                        logger,
                        logging.INFO,
                        Event.NODE_START,
                        node=name,
                        node_run=run_counts[name],
                    )
                else:
                    record = to_record(event)
                    if event["error"] is not None:
                        failed_node, node_error = record.node, event["error"]
                    log_record(record, event["error"])
                    history.append(record)
    except Exception as caught:
        if failed_node is not None and caught is node_error:
            # 노드가 던진 예외는 종류와 상관없이 그 노드의 실패다.
            # 노드 안의 하위 그래프가 던진 GraphRecursionError도 여기에 해당한다.
            stop_reason = StopReason(
                kind=StopKind.NODE_FAILURE,
                node=failed_node,
                detail=describe_error(caught),
            )
        elif isinstance(caught, GraphRecursionError):
            # 노드가 던지지 않은 GraphRecursionError는 이 그래프의 단계 수 상한 초과다.
            stop_reason = StopReason(
                kind=StopKind.STEP_LIMIT_EXCEEDED,
                node=history[-1].node if history else "",
                detail=messages.step_limit_detail(recursion_limit),
            )
        else:
            # 노드 밖에서 발생한 오류는 기록하지 않고 다시 던진다. 받는 쪽이 traceback과 함께 기록한다.
            raise
        return stopped(history, state, stop_reason)

    log_event(logger, logging.INFO, Event.RUN_FINISHED, steps=len(history))
    return RunResult(history=history, state=state)


def stopped(
    history: list[ExecutionRecord], state: dict[str, Any], stop_reason: StopReason
) -> RunResult:
    log_event(
        logger,
        logging.WARNING,
        Event.RUN_STOPPED,
        kind=stop_reason.kind,
        node=stop_reason.node,
        detail=stop_reason.detail,
    )
    return RunResult(history=history, state=state, stop_reason=stop_reason)


def log_record(record: ExecutionRecord, error: BaseException | str | None) -> None:
    """실행 기록 하나를 로그로 남긴다. 실패는 오류 처리기의 실패까지 같은 이벤트로 남긴다."""
    if record.error is not None:
        # 예상하지 못한 버그도 위치를 찾을 수 있도록 traceback을 함께 남긴다.
        log_event(
            logger,
            logging.WARNING,
            Event.NODE_FAILED,
            node=record.node,
            error=record.error,
            traceback=traceback_of(error),
        )
        return
    # 노드의 입력은 앞 노드들의 출력이 쌓인 것이라, 출력만 원본 그대로 남긴다.
    if record.kind is RecordKind.ERROR_HANDLER:
        event = Event.ERROR_HANDLED
    else:
        event = Event.NODE_END
    log_event(logger, logging.INFO, event, node=record.node, output=record.output)


def traceback_of(error: BaseException | str | None) -> str | None:
    if isinstance(error, BaseException):
        return "".join(traceback.format_exception(error))
    return None


def to_record(event: TaskResultPayload) -> ExecutionRecord:
    name = event["name"]
    if name.startswith(ERROR_HANDLER_PREFIX):
        kind, node = RecordKind.ERROR_HANDLER, name.removeprefix(ERROR_HANDLER_PREFIX)
    else:
        kind, node = RecordKind.NODE, name
    error = event["error"]
    return ExecutionRecord(
        kind=kind,
        node=node,
        output=event["result"],
        error=None if error is None else describe_error(error),
    )


def describe_error(error: BaseException | str) -> str:
    """LangGraph는 종료 이벤트의 error를 문자열로 선언하지만 실제로는 예외 객체를 넣는다."""
    if isinstance(error, BaseException):
        return messages.error_reason(error)
    return error
