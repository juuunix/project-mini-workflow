import operator
from typing import Annotated, NotRequired, TypedDict

from mini_workflow import messages
from mini_workflow.search import Collection, Document, DocumentSearch
from mini_workflow.workflows.document_history.metadata import (
    CURRENT_STATUS,
    DocumentMetadata,
    parse_metadata,
)

FIND_DOCUMENTS_NODE = "find_documents"
NO_DOCUMENTS_NODE = "no_documents"
READ_METADATA_NODE = "read_metadata"
WRITE_REPORT_NODE = "write_report"

MAX_DOCUMENTS = 3


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
