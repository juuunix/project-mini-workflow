from pathlib import Path

import pytest

from mini_agent.demo import main
from mini_agent.graph import LLM_RETRY_POLICY
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
