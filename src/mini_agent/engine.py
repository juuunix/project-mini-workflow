from typing import Any

from langgraph.graph.state import CompiledStateGraph

from mini_agent.result import ExecutionRecord, RecordKind, RunResult


def run_graph(graph: CompiledStateGraph, initial_state: dict[str, Any]) -> RunResult:
    history: list[ExecutionRecord] = []
    state: dict[str, Any] = initial_state

    for part in graph.stream(
        initial_state, stream_mode=["tasks", "values"], version="v2"
    ):
        if part["type"] == "values":
            state = part["data"]
        elif part["type"] == "tasks" and "result" in part["data"]:
            history.append(
                ExecutionRecord(
                    kind=RecordKind.NODE,
                    node=part["data"]["name"],
                    summary=str(part["data"]["result"]),
                )
            )

    return RunResult(history=history, state=state)
