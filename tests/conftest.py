from pathlib import Path

import pytest

from mini_workflow.search import DocumentSearch


@pytest.fixture(scope="session")
def docs_dir() -> Path:
    return Path(__file__).parents[1] / "data" / "docs"


@pytest.fixture(scope="session")
def search(docs_dir: Path) -> DocumentSearch:
    return DocumentSearch.from_directory(docs_dir)
