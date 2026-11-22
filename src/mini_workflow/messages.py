from pathlib import Path


def error_reason(error: BaseException) -> str:
    return f"{type(error).__name__}: {error}"


def step_limit_detail(limit: int) -> str:
    return f"상한 {limit}단계"


def node_limit_detail(limit: int) -> str:
    return f"상한 {limit}회"


COLLECTION_LABELS = {"current": "현행", "archive": "보관"}
WORKFLOW_LABELS = {"agent": "에이전트", "document_history": "문서 이력"}


def scenario_heading(workflow: str, number: int, total: int) -> str:
    return f"{WORKFLOW_LABELS[workflow]} [{number}/{total}]"


def no_documents(collection: str) -> str:
    return f"{COLLECTION_LABELS[collection]}({collection}) 문서가 하나도 없습니다."


def empty_document(path: Path) -> str:
    return f"빈 문서입니다: {path}"


def not_utf8_document(path: Path) -> str:
    return f"UTF-8로 읽을 수 없는 문서입니다: {path}"


def unreadable_document(path: Path, error: OSError) -> str:
    return f"열 수 없는 문서입니다: {path} ({error.strerror})"


def log_file_unavailable(error: OSError) -> str:
    return f"로그 파일을 열 수 없어 로그 없이 실행합니다: {error}"


def demo_not_started(reason: str) -> str:
    return f"문서를 읽지 못해 시연을 시작할 수 없습니다: {reason}"
