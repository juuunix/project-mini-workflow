"""v1: compare judges that decide found documents by score alone."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))  # Shared modules live one folder up.

from judges import JUDGES  # noqa: E402
from runner import run  # noqa: E402

if __name__ == "__main__":
    run(JUDGES, HERE / "results")
