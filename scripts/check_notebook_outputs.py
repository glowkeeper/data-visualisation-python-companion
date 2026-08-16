#!/usr/bin/env python3
"""Reject staged notebooks that still carry executed output.

The Markdown files are the source of truth in this repository; the .ipynb
files are generated with jupytext and should be committed clean. Stored
outputs bloat the repository (a single Plotly notebook once reached 140 KB
against ~21 KB clean) and produce noisy, unreviewable diffs.

Installed as .git/hooks/pre-commit. Run directly to check the whole tree:

    python scripts/check_notebook_outputs.py --all
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def staged_notebooks() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [p for p in result.stdout.splitlines() if p.endswith(".ipynb")]


def staged_content(path: str) -> str:
    """Read the version git would commit, not the working copy."""
    result = subprocess.run(
        ["git", "show", f":{path}"], capture_output=True, text=True, check=True
    )
    return result.stdout


def dirty_cells(text: str) -> tuple[int, int]:
    """Return (cells with outputs, cells with an execution count)."""
    try:
        notebook = json.loads(text)
    except json.JSONDecodeError:
        return (0, 0)

    outputs = 0
    counts = 0

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs"):
            outputs += 1
        if cell.get("execution_count") is not None:
            counts += 1

    return (outputs, counts)


def main() -> int:
    check_all = "--all" in sys.argv

    if check_all:
        paths = sorted(str(p) for p in Path("notebooks").rglob("*.ipynb"))
        read = lambda p: Path(p).read_text(encoding="utf-8")  # noqa: E731
    else:
        paths = staged_notebooks()
        read = staged_content

    offenders = []

    for path in paths:
        outputs, counts = dirty_cells(read(path))
        if outputs or counts:
            offenders.append((path, outputs, counts))

    if not offenders:
        return 0

    print("\nBlocked: notebook output must not be committed.\n", file=sys.stderr)

    for path, outputs, counts in offenders:
        print(
            f"  {path}\n"
            f"    {outputs} cell(s) with stored output, "
            f"{counts} with an execution count",
            file=sys.stderr,
        )

    first = offenders[0][0]
    source = first[:-6] + ".md"

    print(
        "\nRegenerate the notebook from its Markdown source, for example:\n"
        f"    python -m jupytext --to notebook --output {first} {source}\n"
        "\nThen stage it again. To check the whole tree:\n"
        "    python scripts/check_notebook_outputs.py --all\n",
        file=sys.stderr,
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
