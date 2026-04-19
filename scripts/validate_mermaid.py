#!/usr/bin/env python3
"""Validate Mermaid diagrams embedded in docs-book/source.

This script walks every ``.rst`` file under the Sphinx source tree, extracts all
``.. mermaid::`` directives (including external ``.mmd`` references), renders
them with Mermaid CLI, and reports any parser/render failures with source
locations.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Diagram:
    source_file: Path
    source_line: int
    temp_name: str
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "source",
        help="Path to the Sphinx source directory (default: docs-book/source).",
    )
    parser.add_argument(
        "--mmdc",
        default="mmdc",
        help="Mermaid CLI executable to use (default: mmdc).",
    )
    parser.add_argument(
        "--keep-artifacts",
        action="store_true",
        help="Keep the temporary .mmd/.svg files for manual inspection.",
    )
    return parser.parse_args()


def _normalize_block(lines: list[str]) -> str:
    return "\n".join(lines).strip() + "\n"


def iter_diagrams(source_root: Path) -> list[Diagram]:
    diagrams: list[Diagram] = []
    counter = 0
    for rst_path in sorted(source_root.rglob("*.rst")):
        lines = rst_path.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if not line.startswith(".. mermaid::"):
                i += 1
                continue

            line_no = i + 1
            argument = line[len(".. mermaid::") :].strip()
            if argument.endswith(".mmd"):
                diagram_path = (rst_path.parent / argument).resolve()
                text = diagram_path.read_text(encoding="utf-8")
                temp_name = f"{counter:03d}-{diagram_path.stem}.mmd"
            else:
                i += 1
                while i < len(lines) and (
                    not lines[i].strip() or lines[i].lstrip().startswith(":")
                ):
                    i += 1

                block: list[str] = []
                while i < len(lines):
                    current = lines[i]
                    if current.startswith("   "):
                        block.append(current[3:])
                        i += 1
                    elif current.startswith("\t"):
                        block.append(current[1:])
                        i += 1
                    elif current.strip() == "":
                        block.append("")
                        i += 1
                    else:
                        break

                i -= 1
                text = _normalize_block(block)
                temp_name = f"{counter:03d}-{rst_path.stem}-{line_no}.mmd"

            diagrams.append(
                Diagram(
                    source_file=rst_path,
                    source_line=line_no,
                    temp_name=temp_name,
                    text=text,
                )
            )
            counter += 1
            i += 1
    return diagrams


def render_diagram(diagram: Diagram, out_dir: Path, mmdc: str) -> tuple[bool, str]:
    input_path = out_dir / diagram.temp_name
    output_path = out_dir / f"{Path(diagram.temp_name).stem}.svg"
    input_path.write_text(diagram.text, encoding="utf-8")

    proc = subprocess.run(
        [mmdc, "-i", str(input_path), "-o", str(output_path)],
        capture_output=True,
        text=True,
    )
    message = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, message


def main() -> int:
    args = parse_args()
    diagrams = iter_diagrams(args.source_root)
    if not diagrams:
        print(f"No Mermaid diagrams found under {args.source_root}", file=sys.stderr)
        return 1

    temp_dir = Path(tempfile.mkdtemp(prefix="docs-book-mermaid-"))
    failures: list[tuple[Diagram, str]] = []

    try:
        for diagram in diagrams:
            ok, message = render_diagram(diagram, temp_dir, args.mmdc)
            if not ok:
                failures.append((diagram, message))

        print(f"Validated {len(diagrams)} Mermaid diagrams.")
        if failures:
            print("")
            print("Failures:")
            for diagram, message in failures:
                rel = diagram.source_file.relative_to(args.source_root.parent)
                print(f"- {rel}:{diagram.source_line}")
                if message:
                    print(message)
                print("")
            return 1

        print("All Mermaid diagrams rendered successfully with Mermaid CLI.")
        if args.keep_artifacts:
            print(f"Artifacts kept at: {temp_dir}")
            temp_dir = None  # type: ignore[assignment]
        return 0
    finally:
        if temp_dir is not None and temp_dir.exists() and not args.keep_artifacts:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
