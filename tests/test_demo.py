from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest
from langgraph.graph.state import CompiledStateGraph

from mini_agent.demo import main
from mini_agent.engine import run_graph
from mini_agent.graph import LLM_RETRY_POLICY
from mini_agent.report import NOT_RUN
from mini_agent.result import RunResult
from mini_agent.scenarios import DEMO_QUESTIONS


def test_main_prints_demo_and_exits_normally(
    docs_dir: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "mini_agent.demo.LLM_RETRY_POLICY",
        LLM_RETRY_POLICY._replace(initial_interval=0),
    )

    main(["--docs-dir", str(docs_dir)])

    output = capsys.readouterr().out
    assert DEMO_QUESTIONS[0] in output
    assert DEMO_QUESTIONS[-1] in output


def test_unexpected_error_in_one_question_does_not_stop_demo(
    docs_dir: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    broken_question = DEMO_QUESTIONS[1]

    def run_graph_breaking_on_one_question(
        graph: CompiledStateGraph,
        initial_state: dict[str, Any],
        node_limits: Mapping[str, int] | None = None,
    ) -> RunResult:
        if initial_state["messages"][0].text == broken_question:
            raise RuntimeError("고장")
        return run_graph(graph, initial_state, node_limits=node_limits)

    monkeypatch.setattr("mini_agent.demo.run_graph", run_graph_breaking_on_one_question)
    monkeypatch.setattr(
        "mini_agent.demo.LLM_RETRY_POLICY",
        LLM_RETRY_POLICY._replace(initial_interval=0),
    )

    main(["--docs-dir", str(docs_dir)])

    output = capsys.readouterr().out
    assert NOT_RUN in output
    assert "고장" in output
    assert DEMO_QUESTIONS[-1] in output
