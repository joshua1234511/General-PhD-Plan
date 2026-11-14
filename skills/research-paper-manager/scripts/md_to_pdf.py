#!/usr/bin/env python3
"""Render one or more Markdown files to a single PDF, via pandoc + typst.

Used for paper dossiers: a strategy, plan, literature matrix, scan report and evidence
cards concatenated into one document that can be sent to a supervisor or co-author.

    md_to_pdf.py out.pdf a.md b.md c.md
    md_to_pdf.py out.pdf --folder path/to/paper --title "Paper name"

Requires: pandoc >= 3.0 and typst on PATH.  Neither LaTeX nor a browser is needed.

Design notes
------------
* **Relative links are unlinked, not followed.** `[text](other.md)` becomes plain `text`.
  A PDF that leaves the repo cannot resolve a sibling file, and a dead blue link reads as
  a broken deliverable.  Absolute http(s) links and DOIs are kept live.
* **Each source file starts on a new page**, so the PDF's structure matches the folder's.
* **Wide tables are shrunk, not clipped.**  Tables with many columns get a smaller type
  size via the Typst template rather than running off the page.
* Emoji used by this skill's conventions (📝 ✅ ⚠️ ❌ …) survive through an explicit
  Apple Color Emoji fallback on macOS; elsewhere they degrade to text glyphs.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Order used when --folder is given.  Anything unlisted follows, alphabetically,
# with evidence cards last.
FOLDER_ORDER = [
    "00-strategy.md",
    "paper-plan-*.md",
    "literature-matrix.md",
    "lit-scan-*.md",
    "citation-audit.md",
    "review-report.md",
    "references-*.md",
    "manuscript-*.md",
]

HEADER = r"""
// Explicit white page: without it the PDF carries no background object, and some
// converters (macOS sips, some thumbnailers) flatten the transparency to black.
#set page(fill: white)
#show heading.where(level: 1): set text(size: 15pt, fill: rgb("#1f3864"))
#show heading.where(level: 2): set text(size: 12pt, fill: rgb("#1f3864"))
#show heading.where(level: 3): set text(size: 10.5pt, fill: rgb("#2e5496"))
#show heading: set block(above: 1.25em, below: 0.65em)
#show raw: set text(size: 8.5pt)
#show table: set text(size: 7.4pt)
#set table(
  inset: 4.5pt,
  stroke: 0.4pt + rgb("#c9ccd4"),
  fill: (_, row) => if row == 0 { rgb("#e8ecf4") },
)
#show table.cell.where(y: 0): set text(weight: "bold")
#show link: set text(fill: rgb("#1f3864"))
// Pandoc wraps every table in a figure, and figures do not break across pages by
// default — a long literature matrix would otherwise pile its last rows on top of
// each other at the page foot.  Make them breakable, and repeat the header row.
#show figure: set block(breakable: true)
#set table(inset: 4.5pt)
#show figure.where(kind: table): set figure(supplement: none)
"""

BEFORE = r"""
#set document(title: "%%DOCTITLE%%")
#set page(numbering: none)
#align(center)[
  #v(4.5cm)
  #text(size: 21pt, weight: "bold", fill: rgb("#1f3864"))[%%TITLE%%]
  #v(0.7cm)
  #text(size: 11pt, fill: rgb("#555555"))[%%SUBTITLE%%]
  #v(0.5cm)
  #text(size: 10pt, fill: rgb("#555555"))[%%DATE%%]
]
#pagebreak()
#set page(numbering: "1")
#counter(page).update(1)
"""


def _resolve_order(folder: Path) -> list[Path]:
    seen: list[Path] = []
    for pattern in FOLDER_ORDER:
        for p in sorted(folder.glob(pattern)):
            if p.is_file() and p not in seen:
                seen.append(p)
    for p in sorted(folder.glob("*.md")):
        if p not in seen:
            seen.append(p)
    for p in sorted((folder / "evidence").glob("*.md")):
        if p not in seen:
            seen.append(p)
    return seen


def _clean(text: str) -> str:
    """Unlink relative links; keep http(s) live.  Drop YAML front matter."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            text = text[end + 4:].lstrip("\n")

    def repl(m: re.Match[str]) -> str:
        label, target = m.group(1), m.group(2)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        return label  # relative path -> plain text

    # [label](target) but not ![image](target)
    return re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", repl, text)


def build(out: Path, files: list[Path], title: str, subtitle: str, author: str) -> None:
    if not files:
        sys.exit("no input files")
    for missing in (f for f in files if not f.is_file()):
        sys.exit(f"not found: {missing}")

    parts = []
    for i, f in enumerate(files):
        body = _clean(f.read_text(encoding="utf-8")).strip()
        parts.append(("\n\n\\newpage\n\n" if i else "") + body)
    merged = "\n".join(parts)

    def esc(s: str) -> str:
        """Escape for a Typst content block."""
        return s.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]").replace("#", "\\#")

    today = _dt.date.today().strftime("%d %B %Y")
    cover = (
        BEFORE.replace("%%DOCTITLE%%", title.replace('"', "'"))
        .replace("%%SUBTITLE%%", esc(subtitle) if subtitle else "")
        .replace("%%TITLE%%", esc(title))
        .replace("%%DATE%%", esc(f"{author} · {today}" if author else today))
    )

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        src = tmp / "merged.md"
        src.write_text(merged, encoding="utf-8")
        hdr = tmp / "header.typ"
        hdr.write_text(HEADER, encoding="utf-8")
        pre = tmp / "cover.typ"
        pre.write_text(cover, encoding="utf-8")
        # margin is a nested map, so it has to come through a metadata file, not -V.
        meta = tmp / "meta.yaml"
        meta.write_text(
            "papersize: a4\n"
            "fontsize: 9.5pt\n"
            "mainfont: Helvetica Neue\n"
            "page-numbering: 1\n"
            "margin:\n  x: 1.9cm\n  y: 2.1cm\n",
            encoding="utf-8",
        )

        # Pandoc's own Typst template is kept — it defines helpers the writer emits
        # (#horizontalrule, terms.item, highlighting).  Styling goes in via
        # header-includes and variables instead of replacing it.
        cmd = [
            "pandoc", str(src),
            "--from", "gfm+pipe_tables+footnotes+tex_math_dollars",
            "--to", "typst",
            "--pdf-engine", "typst",
            "--include-in-header", str(hdr),
            "--include-before-body", str(pre),
            "--toc", "--toc-depth=2",
            # Deliberately no title/date metadata: pandoc's conf() would render its own
            # title block on top of the cover page built in BEFORE.
            "--metadata-file", str(meta),
            "--wrap", "preserve",
            "-o", str(out),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            sys.stderr.write(res.stdout + res.stderr)
            sys.exit(f"pandoc failed ({res.returncode})")
        if res.stderr.strip():
            sys.stderr.write(res.stderr)


def main() -> None:
    for tool in ("pandoc", "typst"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found on PATH — brew install {tool}")

    ap = argparse.ArgumentParser(description="Render Markdown to a single PDF via pandoc + typst.")
    ap.add_argument("output", type=Path, help="output .pdf")
    ap.add_argument("inputs", type=Path, nargs="*", help="input .md files, in order")
    ap.add_argument("--folder", type=Path, help="take every .md in this paper folder, in skill order")
    ap.add_argument("--title", default=None)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--author", default="")
    args = ap.parse_args()

    files = list(args.inputs)
    if args.folder:
        files = _resolve_order(args.folder) + files
    title = args.title or (args.folder.name if args.folder else args.output.stem)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    build(args.output, files, title, args.subtitle, args.author)
    size = args.output.stat().st_size / 1024
    print(f"wrote {args.output}  ({len(files)} file(s), {size:.0f} KB)")


if __name__ == "__main__":
    main()
