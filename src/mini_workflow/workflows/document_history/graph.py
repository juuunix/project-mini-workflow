from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from mini_workflow.search import DocumentSearch
from mini_workflow.workflows.document_history.nodes import (
    FIND_DOCUMENTS_NODE,
    NO_DOCUMENTS_NODE,
    READ_METADATA_NODE,
    WRITE_REPORT_NODE,
    DocumentState,
    FindDocumentsNode,
    no_documents,
    read_count,
    read_metadata,
    write_report,
)


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
