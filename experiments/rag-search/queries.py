"""Test questions with expected answers.

Each topic has three phrasings: polite question, casual, and keywords only.
`expected_doc` is None when no document should be found in either collection.
"""

from dataclasses import dataclass
from typing import Literal

Collection = Literal["current", "archive"]


@dataclass(frozen=True)
class Query:
    topic: int
    kind: str  # A: revised, B: current only, C: retired, D: trap, E: none
    style: str  # polite, casual, keywords
    text: str
    expected_collection: Collection | None
    expected_doc: str | None


_TOPICS: list[tuple[str, Collection | None, str | None, tuple[str, str, str]]] = [
    ("A", "current", "policy-01-leave", (
        "연차휴가 이월은 최대 며칠까지 가능한가요?",
        "연차 이월 며칠까지 돼?",
        "연차휴가 이월 일수",
    )),
    ("A", "current", "customer-02-refund", (
        "연간 결제를 환불하면 위약금이 있나요?",
        "연간 결제 환불하면 위약금 내?",
        "연간 결제 환불 위약금",
    )),
    ("A", "current", "policy-02-remote", (
        "재택근무는 일주일에 며칠 할 수 있나요?",
        "재택 일주일에 며칠 돼?",
        "재택근무 주간 최대 일수",
    )),
    ("A", "current", "tech-02-deploy", (
        "배포 후 롤백 기준은 무엇인가요?",
        "배포하고 롤백은 언제 해?",
        "배포 롤백 기준",
    )),
    ("A", "current", "tech-03-incident", (
        "장애 등급은 어떻게 나뉘나요?",
        "장애 등급 어떻게 나눠?",
        "장애 등급 구분",
    )),
    ("B", "current", "policy-03-education", (
        "교육비 지원 한도는 얼마인가요?",
        "교육비 얼마까지 지원돼?",
        "교육비 지원 한도",
    )),
    ("B", "current", "policy-04-expense", (
        "해외 출장비 기준을 알려주세요.",
        "해외 출장 가면 출장비 얼마 나와?",
        "해외 출장비 기준",
    )),
    ("B", "current", "tech-04-backup", (
        "백업 보존 기간은 얼마인가요?",
        "백업 얼마나 보관해?",
        "백업 보존 기간",
    )),
    ("B", "current", "tech-05-access", (
        "운영 환경 임시 권한은 어떻게 신청하나요?",
        "운영 서버 임시 권한 어떻게 받아?",
        "운영 환경 임시 권한 신청",
    )),
    ("B", "current", "policy-05-flextime", (
        "선택적 근로시간제는 어떻게 운영되나요?",
        "선택근무제 어떻게 돌아가?",
        "선택적 근로시간제 운영",
    )),
    ("C", "archive", "customer-14-freepass", (
        "프리패스 이용권 잔여 쿠폰은 어떻게 관리하나요?",
        "프리패스 쿠폰 남은 거 어떻게 해?",
        "프리패스 잔여 쿠폰",
    )),
    ("C", "archive", "customer-13-edu-plan", (
        "에듀 플랜 가입 자격은 무엇인가요?",
        "에듀 플랜 누가 가입할 수 있어?",
        "에듀 플랜 가입 자격",
    )),
    ("C", "archive", "policy-15-refresh-sabbatical", (
        "리프레시 안식월은 누가 쓸 수 있나요?",
        "안식월 누가 쓸 수 있어?",
        "리프레시 안식월 사용 자격",
    )),
    ("C", "archive", "policy-13-onboarding-buddy", (
        "온보딩 버디 활동비는 얼마인가요?",
        "버디 활동비 얼마 나와?",
        "온보딩 버디 활동비",
    )),
    ("D", "archive", "tech-13-hermes-api", (
        "헤르메스 API 호출 한도는 얼마인가요?",
        "헤르메스 API 호출 몇 번까지 돼?",
        "헤르메스 API 호출 한도",
    )),
    ("D", "archive", "tech-14-atlas-deploy-tool", (
        "아틀라스 배포 도구로 롤백하는 방법은?",
        "아틀라스로 롤백 어떻게 해?",
        "아틀라스 배포 도구 롤백",
    )),
    ("D", "archive", "policy-14-wellness-points", (
        "웰니스 포인트는 이월되나요?",
        "웰니스 포인트 이월 돼?",
        "웰니스 포인트 이월",
    )),
    ("D", "archive", "tech-15-orion-monitoring-console", (
        "오리온 모니터링 콘솔의 경보 단계는?",
        "오리온 경보 단계 뭐 있어?",
        "오리온 모니터링 경보 단계",
    )),
    ("E", None, None, (
        "사내 주차 지원은 어떻게 받나요?",
        "주차 지원 받을 수 있어?",
        "사내 주차 지원",
    )),
    ("E", None, None, (
        "안녕하세요",
        "안녕",
        "인사",
    )),
]

_STYLES = ("polite", "casual", "keywords")

QUERIES: list[Query] = [
    Query(topic, kind, style, text, collection, doc)
    for topic, (kind, collection, doc, texts) in enumerate(_TOPICS, start=1)
    for style, text in zip(_STYLES, texts, strict=True)
]
