import json
import logging
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest
from langgraph.graph.state import CompiledStateGraph

from mini_agent.demo import main
from mini_agent.engine import run_graph
from mini_agent.graph import LLM_RETRY_POLICY
from mini_agent.log import LOG_FILE, Event
from mini_agent.report import NOT_RUN
from mini_agent.result import RunResult
from mini_agent.scenarios import DEMO_QUESTIONS

LOG_LINE_KEYS = {"time", "level", "logger", "run", "event", "data"}


@pytest.fixture(autouse=True)
def run_in_tmp_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """시연이 남기는 로그 파일이 저장소가 아닌 임시 폴더에 생기게 한다."""
    monkeypatch.chdir(tmp_path)


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
    docs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
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

    caplog.set_level(logging.INFO, logger="mini_agent")

    main(["--docs-dir", str(docs_dir)])

    output = capsys.readouterr().out
    assert NOT_RUN in output
    assert "고장" in output
    assert DEMO_QUESTIONS[-1] in output
    # 화면에는 한 줄만 보이고, 원인을 찾을 traceback은 로그에 남는다.
    [error] = [r for r in caplog.records if r.levelno == logging.ERROR]
    assert getattr(error, "event") == Event.QUESTION_CRASHED
    assert getattr(error, "data")["question"] == broken_question
    assert error.exc_info is not None


def test_main_writes_log_file(
    docs_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "mini_agent.demo.LLM_RETRY_POLICY",
        LLM_RETRY_POLICY._replace(initial_interval=0),
    )

    main(["--docs-dir", str(docs_dir)])

    log = (tmp_path / LOG_FILE).read_text(encoding="utf-8")
    lines = [json.loads(line) for line in log.splitlines()]
    # 모든 줄이 같은 바깥 칸을 가지고, 질문 번호가 붙는다.
    assert all(line.keys() == LOG_LINE_KEYS for line in lines)
    assert (lines[0]["run"], lines[0]["event"]) == (1, Event.QUESTION_START)
    # 노드 출력이 원본 그대로 남는다. JSON 변환이 깨지면 이 글자가 없다.
    assert "search_documents" in log


def test_main_stops_with_message_when_documents_cannot_be_loaded(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--docs-dir", str(tmp_path)])

    assert exit_info.value.code == 1
    output = capsys.readouterr().out
    assert "문서를 읽지 못해 시연을 시작할 수 없습니다" in output
    assert "Traceback" not in output
