import operator
from typing import Annotated, NoReturn, TypedDict

import pytest
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from mini_agent.engine import run_graph
from mini_agent.result import RecordKind, RunStatus, StopKind


class PathState(TypedDict):
    path: Annotated[list[str], operator.add]


class AppendName:
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, state: PathState) -> dict[str, list[str]]:
        return {"path": [self.name]}


class RaiseError:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error or ValueError("boom")

    def __call__(self, state: PathState) -> dict[str, list[str]]:
        raise self.error


class CountRuns:
    def __init__(self) -> None:
        self.runs = 0

    def __call__(self, state: PathState) -> dict[str, list[str]]:
        self.runs += 1
        return {"path": ["L"]}


def build_chain(nodes: list[tuple[str, AppendName | RaiseError]]) -> CompiledStateGraph:
    builder = StateGraph(PathState)  # ty: ignore[invalid-argument-type]
    previous = START
    for name, node in nodes:
        builder.add_node(name, node)
        builder.add_edge(previous, name)
        previous = name
    builder.add_edge(previous, END)
    return builder.compile()


def build_endless_loop(node: AppendName | CountRuns) -> CompiledStateGraph:
    builder = StateGraph(PathState)  # ty: ignore[invalid-argument-type]
    builder.add_node("L", node)
    builder.add_edge(START, "L")
    builder.add_edge("L", "L")
    return builder.compile()


def test_runs_nodes_in_order_and_succeeds() -> None:
    graph = build_chain(
        [("A", AppendName("A")), ("B", AppendName("B")), ("C", AppendName("C"))]
    )

    result = run_graph(graph, {"path": []})

    assert [record.node for record in result.history] == ["A", "B", "C"]
    assert result.status is RunStatus.SUCCESS
    assert result.history[0].output == {"path": ["A"]}
    assert result.state == {"path": ["A", "B", "C"]}


def test_node_failure_without_handler_stops_with_failure() -> None:
    graph = build_chain(
        [("A", AppendName("A")), ("B", RaiseError()), ("C", AppendName("C"))]
    )

    result = run_graph(graph, {"path": []})

    assert result.status is RunStatus.FAILURE
    assert [record.node for record in result.history] == ["A", "B"]
    assert not result.history[-1].succeeded
    assert result.stop_reason is not None
    assert result.stop_reason.kind is StopKind.NODE_FAILURE
    assert result.stop_reason.node == "B"
    assert "ValueError" in result.stop_reason.detail
    assert result.state == {"path": ["A"]}


def send_to_recover(state: PathState) -> Command:
    return Command(goto="RECOVER")


def test_node_failure_with_handler_records_handling_and_succeeds() -> None:
    builder = StateGraph(PathState)  # ty: ignore[invalid-argument-type]
    builder.add_node("A", AppendName("A"))
    builder.add_node("B", RaiseError(), error_handler=send_to_recover)
    builder.add_node("C", AppendName("C"))
    builder.add_node("RECOVER", AppendName("RECOVER"))
    builder.add_edge(START, "A")
    builder.add_edge("A", "B")
    builder.add_edge("B", "C")
    builder.add_edge("C", END)
    builder.add_edge("RECOVER", END)

    result = run_graph(builder.compile(), {"path": []})

    assert result.status is RunStatus.SUCCESS
    assert result.stop_reason is None
    assert [(record.kind, record.node) for record in result.history] == [
        (RecordKind.NODE, "A"),
        (RecordKind.NODE, "B"),
        (RecordKind.ERROR_HANDLER, "B"),
        (RecordKind.NODE, "RECOVER"),
    ]
    assert not result.history[1].succeeded
    assert result.state == {"path": ["A", "RECOVER"]}


def test_recursion_error_raised_by_node_is_node_failure() -> None:
    # 노드 안에서 난 GraphRecursionError(예: 하위 그래프의 상한 초과)는
    # 바깥 그래프의 단계 수 상한 초과가 아니라 그 노드의 실패다.
    error = GraphRecursionError("하위 그래프의 상한 초과")
    graph = build_chain([("A", RaiseError(error))])

    result = run_graph(graph, {"path": []})

    assert result.stop_reason is not None
    assert result.stop_reason.kind is StopKind.NODE_FAILURE
    assert result.stop_reason.node == "A"


def test_endless_loop_stops_with_step_limit_exceeded() -> None:
    graph = build_endless_loop(AppendName("L"))

    result = run_graph(graph, {"path": []}, recursion_limit=5)

    assert result.status is RunStatus.FAILURE
    assert result.stop_reason is not None
    assert result.stop_reason.kind is StopKind.STEP_LIMIT_EXCEEDED
    assert result.stop_reason.node == "L"
    assert [record.node for record in result.history] == ["L"] * 5


def test_node_over_its_limit_stops_before_running_again() -> None:
    node = CountRuns()

    result = run_graph(build_endless_loop(node), {"path": []}, node_limits={"L": 3})

    assert result.status is RunStatus.FAILURE
    assert result.stop_reason is not None
    assert result.stop_reason.kind is StopKind.NODE_LIMIT_EXCEEDED
    assert result.stop_reason.node == "L"
    assert [record.node for record in result.history] == ["L"] * 3
    assert node.runs == 3


def test_node_counts_start_over_for_each_run() -> None:
    graph = build_endless_loop(CountRuns())

    first = run_graph(graph, {"path": []}, node_limits={"L": 3})
    second = run_graph(graph, {"path": []}, node_limits={"L": 3})

    assert len(first.history) == 3
    assert len(second.history) == 3


def test_error_outside_nodes_is_not_reported_as_node_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    graph = build_chain([("A", AppendName("A"))])

    def broken_stream(*args: object, **kwargs: object) -> NoReturn:
        raise RuntimeError("not a node")

    monkeypatch.setattr(graph, "stream", broken_stream)

    with pytest.raises(RuntimeError, match="not a node"):
        run_graph(graph, {"path": []})
