import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

from mini_agent.engine import run_graph
from mini_agent.result import RunStatus


class PathState(TypedDict):
    path: Annotated[list[str], operator.add]


class AppendName:
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, state: PathState) -> dict[str, list[str]]:
        return {"path": [self.name]}


def test_runs_nodes_in_order_and_succeeds() -> None:
    builder = StateGraph(PathState)  # ty: ignore[invalid-argument-type]
    for name in ["A", "B", "C"]:
        builder.add_node(name, AppendName(name))
    builder.add_edge(START, "A")
    builder.add_edge("A", "B")
    builder.add_edge("B", "C")
    builder.add_edge("C", END)

    result = run_graph(builder.compile(), {"path": []})

    assert [record.node for record in result.history] == ["A", "B", "C"]
    assert result.status is RunStatus.SUCCESS
    assert result.state == {"path": ["A", "B", "C"]}
