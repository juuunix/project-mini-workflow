from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class RunStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"


class RecordKind(StrEnum):
    NODE = "node"
    ERROR_HANDLER = "error_handler"


class StopKind(StrEnum):
    NODE_FAILURE = "node_failure"
    NODE_LIMIT_EXCEEDED = "node_limit_exceeded"
    STEP_LIMIT_EXCEEDED = "step_limit_exceeded"


@dataclass(frozen=True)
class ExecutionRecord:
    kind: RecordKind
    node: str
    summary: str
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class StopReason:
    kind: StopKind
    node: str
    detail: str


@dataclass(frozen=True)
class RunResult:
    history: list[ExecutionRecord]
    state: dict[str, Any]
    stop_reason: StopReason | None = None

    @property
    def status(self) -> RunStatus:
        if self.stop_reason is None:
            return RunStatus.SUCCESS
        return RunStatus.FAILURE
