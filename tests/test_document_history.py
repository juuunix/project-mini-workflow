import pytest

from mini_workflow.engine import run_graph
from mini_workflow.result import RunStatus
from mini_workflow.search import Collection, Document, DocumentSearch
from mini_workflow.workflows.document_history import (
    FIND_DOCUMENTS_NODE,
    MAX_DOCUMENTS,
    NO_DOCUMENTS_NODE,
    READ_METADATA_NODE,
    WRITE_REPORT_NODE,
    FindDocumentsNode,
    build_document_graph,
    read_metadata,
)


def document_with_header(
    doc_id: str, title: str, collection: Collection, header: str
) -> Document:
    return Document(
        doc_id=doc_id,
        title=title,
        collection=collection,
        text=f"# {title}\n\n{header}\n\n{title} 내용이다.",
    )


def unrelated_documents(collection: Collection) -> list[Document]:
    # BM25는 모든 문서에 있는 단어의 점수를 0으로 매기므로, 주제가 없는 문서를 함께 둔다.
    return [
        document_with_header(
            f"{collection}-leave-{n}",
            f"휴가 안내 {n}",
            collection,
            "- 문서 번호: POL-9\n- 상태: 현행\n- 시행일: 2025-01-01",
        )
        for n in range(2)
    ]


VALID_CURRENT_HEADER = "- 문서 번호: TEC-1\n- 상태: 현행\n- 시행일: 2025-01-01"
BAD_DATE_HEADER = (
    "- 문서 번호: TEC-1\n- 상태: 보관 (개정 전)\n- 시행일: 2020.01.01\n"
    "- 폐지일 또는 개정일: 2024-12-31"
)


def current_document(doc_id: str, title: str) -> Document:
    return Document(
        doc_id=doc_id,
        title=title,
        collection=Collection.CURRENT,
        text=f"# {title}\n{title} 내용이다.",
    )


def test_find_documents_keeps_current_then_archive_documents(
    search: DocumentSearch,
) -> None:
    node = FindDocumentsNode(search)

    update = node({"topic": "배포"})

    assert [doc.doc_id for doc in update["documents"]] == [
        "tech-02-deploy",
        "tech-14-atlas-deploy-tool",
        "tech-11-deploy-2022",
    ]


def test_find_documents_keeps_at_most_max_documents() -> None:
    archive = Document(
        doc_id="old", title="옛 문서", collection=Collection.ARCHIVE, text="# 옛 문서"
    )
    # BM25는 모든 문서에 있는 단어의 점수를 0으로 매기므로, 주제가 없는 문서를 더 많이 둔다.
    matching = [
        current_document(f"deploy-{n}", f"배포 절차 {n}")
        for n in range(MAX_DOCUMENTS + 1)
    ]
    others = [
        current_document(f"other-{n}", f"휴가 안내 {n}")
        for n in range(MAX_DOCUMENTS + 2)
    ]
    node = FindDocumentsNode(DocumentSearch([*matching, *others, archive]))

    update = node({"topic": "배포"})

    assert len(update["documents"]) == MAX_DOCUMENTS


def test_topic_without_documents_goes_find_then_no_documents(
    search: DocumentSearch,
) -> None:
    graph = build_document_graph(search)

    result = run_graph(graph, {"topic": "동호회"})

    assert [record.node for record in result.history] == [
        FIND_DOCUMENTS_NODE,
        NO_DOCUMENTS_NODE,
    ]
    assert result.status is RunStatus.SUCCESS


def test_metadata_is_read_once_per_found_document(search: DocumentSearch) -> None:
    graph = build_document_graph(search)

    result = run_graph(graph, {"topic": "배포"})

    assert [record.node for record in result.history] == [
        FIND_DOCUMENTS_NODE,
        READ_METADATA_NODE,
        READ_METADATA_NODE,
        READ_METADATA_NODE,
        WRITE_REPORT_NODE,
    ]
    assert result.status is RunStatus.SUCCESS


def test_history_report_groups_versions_by_document_number(
    search: DocumentSearch,
) -> None:
    graph = build_document_graph(search)

    result = run_graph(graph, {"topic": "배포"})

    assert result.state["report"] == (
        "'배포' 관련 문서 3건의 이력입니다.\n"
        "\n"
        "[TEC-002] 서비스 배포 절차\n"
        "- 2025-05-01 ~ 현재: 서비스 배포 절차 (tech-02-deploy) · 현행\n"
        "- 2022-03-01 ~ 2025-04-30: 서비스 배포 절차 (2022년판) (tech-11-deploy-2022)"
        " · 보관 (개정 전)\n"
        "\n"
        "[TEC-012] 아틀라스 배포 도구 사용 절차\n"
        "- 2017-11-01 ~ 2022-02-28: 아틀라스 배포 도구 사용 절차"
        " (tech-14-atlas-deploy-tool) · 보관 (폐지)\n"
        "\n"
        "지금 따라야 할 문서: 서비스 배포 절차 (tech-02-deploy)"
    )


def test_report_says_no_document_is_in_force_when_all_are_archived(
    search: DocumentSearch,
) -> None:
    graph = build_document_graph(search)

    result = run_graph(graph, {"topic": "웰니스 포인트"})

    assert result.state["report"].splitlines()[-1] == (
        "지금 유효한 문서가 없습니다. 마지막으로 유효했던 문서는 "
        "웰니스 포인트 운영 규정 (policy-14-wellness-points)이며 "
        "2024-06-30에 효력이 끝났습니다."
    )


@pytest.mark.parametrize(
    ("header", "reason"),
    [
        (
            "- 문서 번호: TEC-1\n- 시행일: 2025-01-01",
            "'상태' 항목이 없습니다.",
        ),
        (
            "- 문서 번호: TEC-1\n- 상태: 현행\n- 시행일: 2025.01.01",
            "'시행일'이 YYYY-MM-DD 형식이 아닙니다: 2025.01.01",
        ),
        (
            "- 문서 번호: TEC-1\n- 상태: 보관 (폐지)\n- 시행일: 2020-01-01",
            "보관 문서인데 '폐지일 또는 개정일' 항목이 없습니다.",
        ),
    ],
)
def test_read_metadata_skips_document_with_malformed_metadata(
    header: str, reason: str
) -> None:
    document = document_with_header("doc", "문서", Collection.ARCHIVE, header)

    update = read_metadata({"topic": "문서", "documents": [document]})

    assert update == {"skipped": [{"doc_id": "doc", "reason": reason}]}


def test_report_lists_skipped_documents_after_history() -> None:
    search = DocumentSearch(
        [
            document_with_header(
                "deploy-new", "배포 절차", Collection.CURRENT, VALID_CURRENT_HEADER
            ),
            document_with_header(
                "deploy-old", "배포 절차 (구판)", Collection.ARCHIVE, BAD_DATE_HEADER
            ),
            *unrelated_documents(Collection.CURRENT),
            *unrelated_documents(Collection.ARCHIVE),
        ]
    )

    result = run_graph(build_document_graph(search), {"topic": "배포"})

    assert result.state["report"] == (
        "'배포' 관련 문서 1건의 이력입니다.\n"
        "\n"
        "[TEC-1] 배포 절차\n"
        "- 2025-01-01 ~ 현재: 배포 절차 (deploy-new) · 현행\n"
        "\n"
        "지금 따라야 할 문서: 배포 절차 (deploy-new)\n"
        "\n"
        "메타데이터를 읽지 못해 제외한 문서\n"
        "- deploy-old: '시행일'이 YYYY-MM-DD 형식이 아닙니다: 2020.01.01"
    )


def test_report_has_no_history_when_every_document_is_skipped() -> None:
    search = DocumentSearch(
        [
            document_with_header(
                "deploy-old", "배포 절차 (구판)", Collection.ARCHIVE, BAD_DATE_HEADER
            ),
            *unrelated_documents(Collection.CURRENT),
            *unrelated_documents(Collection.ARCHIVE),
        ]
    )

    result = run_graph(build_document_graph(search), {"topic": "배포"})

    assert result.status is RunStatus.SUCCESS
    assert result.state["report"] == (
        "'배포' 관련 문서 1건 모두 메타데이터를 읽지 못했습니다.\n"
        "\n"
        "메타데이터를 읽지 못해 제외한 문서\n"
        "- deploy-old: '시행일'이 YYYY-MM-DD 형식이 아닙니다: 2020.01.01"
    )
