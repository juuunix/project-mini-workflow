import argparse
import logging
from collections.abc import Sequence
from pathlib import Path

from langgraph.graph.state import CompiledStateGraph
from langgraph.types import RetryPolicy
from rich.console import Console
from rich.text import Text

from mini_agent import messages
from mini_agent.document_history import build_document_graph
from mini_agent.engine import run_graph
from mini_agent.fake_llm import FakeLLM
from mini_agent.graph import LLM_RETRY_POLICY, build_agent_graph
from mini_agent.log import Event, file_logging, log_event, log_run
from mini_agent.report import not_run_report, run_report
from mini_agent.result import RunResult
from mini_agent.scenarios import (
    DEMO_NODE_LIMITS,
    DEMO_SCENARIOS,
    TIMEOUT_QUESTION,
    Scenario,
    Workflow,
)
from mini_agent.search import DocumentLoadError, DocumentSearch

DEFAULT_DOCS_DIR = Path("data") / "docs"

logger = logging.getLogger(__name__)


def run_demo(
    console: Console, docs_dir: Path, llm_retry: RetryPolicy = LLM_RETRY_POLICY
) -> None:
    """시나리오마다 그 워크플로우의 그래프를 실행하고, 모든 실행이 끝난 뒤 결과를 한꺼번에 출력한다.

    실행하는 대로 출력하면 재시도로 기다리는 시나리오만 늦게 나타나 멈춘 것처럼 보인다.
    """
    llm = FakeLLM(timeout_questions=frozenset({TIMEOUT_QUESTION}))
    search = DocumentSearch.from_directory(docs_dir)
    graphs = {
        Workflow.AGENT: build_agent_graph(llm, search, llm_retry),
        Workflow.DOCUMENT_HISTORY: build_document_graph(search),
    }

    results = [
        run_scenario(graphs[scenario.workflow], number, scenario)
        for number, scenario in enumerate(DEMO_SCENARIOS, start=1)
    ]
    for number, (scenario, result) in enumerate(
        zip(DEMO_SCENARIOS, results, strict=True), start=1
    ):
        console.rule(Text(f"[{number}/{len(results)}]"))
        if isinstance(result, RunResult):
            console.print(run_report(result))
        else:
            console.print(not_run_report(scenario.label, result))
        console.print()


def run_scenario(
    graph: CompiledStateGraph, number: int, scenario: Scenario
) -> RunResult | Exception:
    with log_run(number):
        log_event(logger, logging.INFO, Event.QUESTION_START, question=scenario.label)
        try:
            result = run_graph(
                graph, scenario.initial_state, node_limits=DEMO_NODE_LIMITS
            )
        except Exception as error:
            log_event(
                logger,
                logging.ERROR,
                Event.QUESTION_CRASHED,
                exc_info=True,
                question=scenario.label,
                error=messages.error_reason(error),
            )
            return error
        log_event(logger, logging.INFO, Event.QUESTION_END, status=result.status)
        return result


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="미니 에이전트 시연")
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=DEFAULT_DOCS_DIR,
        help="current, archive 폴더가 있는 문서 디렉터리 (기본값: data/docs)",
    )
    args = parser.parse_args(argv)
    console = Console()

    with file_logging():
        try:
            run_demo(console, args.docs_dir, LLM_RETRY_POLICY)
        except DocumentLoadError as error:
            log_event(
                logger,
                logging.ERROR,
                Event.DOCS_LOAD_FAILED,
                exc_info=True,
                docs_dir=args.docs_dir,
                error=str(error),
            )
            console.print(Text(messages.demo_not_started(str(error))))
            raise SystemExit(1) from error


if __name__ == "__main__":
    main()
