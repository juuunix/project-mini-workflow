import operator
import re
from typing import Annotated, NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from mini_agent import messages
from mini_agent.search import Collection, Document, DocumentSearch

FIND_DOCUMENTS_NODE = "find_documents"
NO_DOCUMENTS_NODE = "no_documents"
READ_METADATA_NODE = "read_metadata"
WRITE_REPORT_NODE = "write_report"

MAX_DOCUMENTS = 3

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


class SkippedDocument(TypedDict):
    doc_id: str
    reason: str


class DocumentState(TypedDict):
    topic: str
    documents: NotRequired[list[Document]]
    metadata: NotRequired[Annotated[list[DocumentMetadata], operator.add]]
    skipped: NotRequired[Annotated[list[SkippedDocument], operator.add]]
    report: NotRequired[str]


class DocumentsUpdate(TypedDict):
    documents: list[Document]


class MetadataUpdate(TypedDict, total=False):
    metadata: list[DocumentMetadata]
    skipped: list[SkippedDocument]


class ReportUpdate(TypedDict):
    report: str


class FindDocumentsNode:
    def __init__(self, search: DocumentSearch) -> None:
        self._search = search

    def __call__(self, state: DocumentState) -> DocumentsUpdate:
        hits = [
            hit
            for collection in Collection
            for hit in self._search.search(state["topic"], collection)
        ]
        return {"documents": [hit.document for hit in hits[:MAX_DOCUMENTS]]}


def read_metadata(state: DocumentState) -> MetadataUpdate:
    document = state["documents"][read_count(state)]
    try:
        metadata = parse_metadata(document)
    except ValueError as error:
        return {"skipped": [{"doc_id": document.doc_id, "reason": str(error)}]}
    return {"metadata": [metadata]}


def read_count(state: DocumentState) -> int:
    return len(state.get("metadata", [])) + len(state.get("skipped", []))


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


def write_report(state: DocumentState) -> ReportUpdate:
    metadata = state.get("metadata", [])
    skipped = state.get("skipped", [])
    if metadata:
        heading = messages.history_heading(state["topic"], len(metadata))
        parts = [heading, *history_sections(metadata), in_force_line(metadata)]
    else:
        parts = [messages.all_documents_skipped(state["topic"], len(skipped))]
    if skipped:
        parts.append(
            messages.skipped_section(
                [
                    messages.skipped_entry(doc["doc_id"], doc["reason"])
                    for doc in skipped
                ]
            )
        )
    return {"report": "\n\n".join(parts)}


def history_sections(metadata: list[DocumentMetadata]) -> list[str]:
    newest_first = sorted(metadata, key=lambda meta: meta["effective"], reverse=True)
    versions: dict[str, list[DocumentMetadata]] = {}
    for meta in newest_first:
        versions.setdefault(meta["number"], []).append(meta)

    return [
        messages.history_section(
            number,
            metas[0]["title"],
            [
                messages.history_entry(
                    meta["effective"],
                    meta["ended"],
                    meta["title"],
                    meta["doc_id"],
                    meta["status"],
                )
                for meta in metas
            ],
        )
        for number, metas in versions.items()
    ]


def in_force_line(metadata: list[DocumentMetadata]) -> str:
    in_force = [meta for meta in metadata if meta["status"] == CURRENT_STATUS]
    if in_force:
        return messages.documents_to_follow(
            [
                messages.document_label(meta["title"], meta["doc_id"])
                for meta in in_force
            ]
        )
    last = max(metadata, key=lambda meta: meta["ended"] or "")
    return messages.no_document_in_force(
        messages.document_label(last["title"], last["doc_id"]), last["ended"] or ""
    )


def no_documents(state: DocumentState) -> ReportUpdate:
    return {"report": messages.no_documents_found(state["topic"])}


def build_document_graph(search: DocumentSearch) -> CompiledStateGraph:
    builder = StateGraph(DocumentState)  # ty: ignore[invalid-argument-type]
    builder.add_node(FIND_DOCUMENTS_NODE, FindDocumentsNode(search))
    builder.add_node(NO_DOCUMENTS_NODE, no_documents)
    builder.add_node(READ_METADATA_NODE, read_metadata)
    builder.add_node(WRITE_REPORT_NODE, write_report)

    builder.add_edge(START, FIND_DOCUMENTS_NODE)
    builder.add_conditional_edges(
        FIND_DOCUMENTS_NODE, route_after_find, [NO_DOCUMENTS_NODE, READ_METADATA_NODE]
    )
    builder.add_conditional_edges(
        READ_METADATA_NODE, route_after_read, [READ_METADATA_NODE, WRITE_REPORT_NODE]
    )
    builder.add_edge(WRITE_REPORT_NODE, END)
    builder.add_edge(NO_DOCUMENTS_NODE, END)
    return builder.compile()


def route_after_find(state: DocumentState) -> str:
    if not state["documents"]:
        return NO_DOCUMENTS_NODE
    return READ_METADATA_NODE


def route_after_read(state: DocumentState) -> str:
    if read_count(state) < len(state["documents"]):
        return READ_METADATA_NODE
    return WRITE_REPORT_NODE
