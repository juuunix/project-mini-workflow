import re
from typing import TypedDict

from mini_workflow import messages
from mini_workflow.search import Document

CURRENT_STATUS = "현행"
END_DATE_KEY = "폐지일 또는 개정일"
DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")


class DocumentMetadata(TypedDict):
    doc_id: str
    title: str
    number: str
    status: str
    effective: str
    ended: str | None


def parse_metadata(document: Document) -> DocumentMetadata:
    fields: dict[str, str] = {}
    for line in document.text.splitlines()[1:]:
        if not line.strip() and not fields:
            continue
        if not line.startswith("- "):
            break
        key, _, value = line[2:].partition(": ")
        fields[key] = value.strip()

    def required(key: str) -> str:
        if key not in fields:
            raise ValueError(messages.missing_metadata(key))
        return fields[key]

    def date_of(key: str, value: str) -> str:
        if not DATE_PATTERN.fullmatch(value):
            raise ValueError(messages.invalid_date(key, value))
        return value

    number = required("문서 번호")
    status = required("상태")
    effective = date_of("시행일", required("시행일"))
    ended = fields.get(END_DATE_KEY)
    if ended is not None:
        ended = date_of(END_DATE_KEY, ended)
    elif status != CURRENT_STATUS:
        raise ValueError(messages.missing_end_date(END_DATE_KEY))
    return {
        "doc_id": document.doc_id,
        "title": document.title,
        "number": number,
        "status": status,
        "effective": effective,
        "ended": ended,
    }
