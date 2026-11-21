import argparse
from collections.abc import Sequence
from pathlib import Path

from langchain_core.messages import HumanMessage
from langgraph.types import RetryPolicy

from mini_agent import messages
from mini_agent.engine import run_graph
from mini_agent.fake_llm import FakeLLM
from mini_agent.graph import LLM_RETRY_POLICY, build_graph
from mini_agent.report import format_result
from mini_agent.scenarios import DEMO_NODE_LIMITS, DEMO_QUESTIONS, TIMEOUT_QUESTION
from mini_agent.search import DocumentSearch

DEFAULT_DOCS_DIR = Path("data") / "docs"


def run_demo(docs_dir: Path, llm_retry: RetryPolicy = LLM_RETRY_POLICY) -> list[str]:
    """시연 질문마다 같은 그래프를 실행하고, 실행 결과를 출력할 줄로 돌려준다."""
    llm = FakeLLM(timeout_questions=frozenset({TIMEOUT_QUESTION}))
    graph = build_graph(llm, DocumentSearch.from_directory(docs_dir), llm_retry)

    lines: list[str] = []
    for question in DEMO_QUESTIONS:
        result = run_graph(
            graph,
            {"messages": [HumanMessage(question)]},
            node_limits=DEMO_NODE_LIMITS,
        )
        lines.append(messages.question_line(question))
        lines.extend(format_result(result))
        lines.append("")
    return lines


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="미니 에이전트 시연")
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=DEFAULT_DOCS_DIR,
        help="current, archive 폴더가 있는 문서 디렉터리 (기본값: data/docs)",
    )
    args = parser.parse_args(argv)
    for line in run_demo(args.docs_dir, LLM_RETRY_POLICY):
        print(line)


if __name__ == "__main__":
    main()
