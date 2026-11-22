def no_documents_found(topic: str) -> str:
    return f"현행 문서와 보관 문서에서 '{topic}' 주제의 문서를 찾지 못했습니다."


def invalid_max_documents(max_documents: int) -> str:
    return f"문서 수 상한은 1 이상이어야 합니다: {max_documents}"


def missing_metadata(key: str) -> str:
    return f"'{key}' 항목이 없습니다."


def invalid_date(key: str, value: str) -> str:
    return f"'{key}'이 YYYY-MM-DD 형식이 아닙니다: {value}"


def missing_end_date(key: str) -> str:
    return f"보관 문서인데 '{key}' 항목이 없습니다."


def history_heading(topic: str, count: int) -> str:
    return f"'{topic}' 관련 문서 {count}건의 이력입니다."


def all_documents_skipped(topic: str, count: int) -> str:
    return f"'{topic}' 관련 문서 {count}건 모두 메타데이터를 읽지 못했습니다."


def omitted_section(documents: list[str]) -> str:
    return "\n".join(
        ["문서 수 상한을 넘어 제외한 문서", *(f"- {doc}" for doc in documents)]
    )


def skipped_section(entries: list[str]) -> str:
    return "\n".join(["메타데이터를 읽지 못해 제외한 문서", *entries])


def skipped_entry(doc_id: str, reason: str) -> str:
    return f"- {doc_id}: {reason}"


def history_section(number: str, title: str, entries: list[str]) -> str:
    return "\n".join([f"[{number}] {title}", *entries])


def history_entry(
    effective: str, ended: str | None, title: str, doc_id: str, status: str
) -> str:
    return f"- {effective} ~ {ended or '현재'}: {title} ({doc_id}) · {status}"


def documents_to_follow(documents: list[str]) -> str:
    return f"지금 따라야 할 문서: {', '.join(documents)}"


def no_document_in_force(last_document: str, ended: str) -> str:
    return (
        f"지금 유효한 문서가 없습니다. 마지막으로 유효했던 문서는 {last_document}이며 "
        f"{ended}에 효력이 끝났습니다."
    )


def document_label(title: str, doc_id: str) -> str:
    return f"{title} ({doc_id})"
