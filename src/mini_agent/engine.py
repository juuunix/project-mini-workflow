from collections import Counter
from collections.abc import Mapping
from typing import Any

from langgraph.errors import GraphRecursionError
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import TaskResultPayload

from mini_agent import messages
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
                        return RunResult(
                            history=history, state=state, stop_reason=stop_reason
                        )
                else:
                    if event["error"] is not None:
                        failed_node, node_error = event["name"], event["error"]
                    history.append(to_record(event))
    except GraphRecursionError:
        stop_reason = StopReason(
            kind=StopKind.STEP_LIMIT_EXCEEDED,
            node=history[-1].node if history else "",
            detail=messages.step_limit_detail(recursion_limit),
        )
        return RunResult(history=history, state=state, stop_reason=stop_reason)
    except Exception as caught:
        if failed_node is None or caught is not node_error:
            raise
        stop_reason = StopReason(
            kind=StopKind.NODE_FAILURE,
            node=failed_node,
            detail=describe_error(caught),
        )
        return RunResult(history=history, state=state, stop_reason=stop_reason)

    return RunResult(history=history, state=state)


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
        summary=str(event["result"]),
        error=None if error is None else describe_error(error),
    )


def describe_error(error: BaseException | str) -> str:
    """LangGraph는 종료 이벤트의 error를 문자열로 선언하지만 실제로는 예외 객체를 넣는다."""
    if isinstance(error, BaseException):
        return messages.error_reason(error)
    return error
