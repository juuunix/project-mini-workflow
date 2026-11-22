from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from langchain_core.messages import HumanMessage

from mini_workflow.workflows.agent.nodes import LLM_NODE, SEARCH_NODE
from mini_workflow.workflows.document_history.nodes import READ_METADATA_NODE


class Workflow(StrEnum):
    AGENT = "agent"
    DOCUMENT_HISTORY = "document_history"


@dataclass(frozen=True)
class Scenario:
    workflow: Workflow
    label: str
    initial_state: dict[str, Any]


def agent_scenario(question: str) -> Scenario:
    return Scenario(Workflow.AGENT, question, {"messages": [HumanMessage(question)]})


def document_history_scenario(topic: str) -> Scenario:
    return Scenario(Workflow.DOCUMENT_HISTORY, topic, {"topic": topic})


# 가짜 LLM이 답변을 만들 때마다 시간 초과로 실패하는 질문. 현행 문서에서 찾아지는 질문이라
# 검색까지는 정상으로 가고, 답변 단계에서 실패해 오류 안내로 간다.
TIMEOUT_QUESTION = "재택근무 운영 지침 찾아줘"

DEMO_QUESTIONS = [
    "안녕하세요",
    "오늘 날짜 알려줘",
    "연차휴가 이월은 최대 며칠까지 가능한지 찾아줘",
    "웰니스 포인트는 언제 폐지됐는지 찾아줘",
    "사내 동호회 가입 방법 찾아줘",
    TIMEOUT_QUESTION,
]

DEMO_TOPICS = ["배포", "동호회"]

DEMO_SCENARIOS = [
    *(agent_scenario(question) for question in DEMO_QUESTIONS),
    *(document_history_scenario(topic) for topic in DEMO_TOPICS),
]

# 정상 절차의 최대 횟수(검색 2번, LLM 3번, 메타데이터 읽기 3번)보다 크게 잡는다.
DEMO_NODE_LIMITS = {SEARCH_NODE: 4, LLM_NODE: 5, READ_METADATA_NODE: 5}
