#!/usr/bin/env python3
"""Render a Markdown research artefact — or a whole paper folder — to a styled .docx.

    python3 md_to_docx.py <in.md> [out.docx]
    python3 md_to_docx.py --folder <paper> [out.docx] [--title "..."] [--subtitle "..."]

Folder mode is the .docx twin of `md_to_pdf.py --folder`: it takes every .md in the
paper folder in skill order (evidence cards last), reusing that script's ordering and
link-cleaning so the .docx and the dossier .pdf carry the same content in the same
order. It adds a cover page and a Word TOC field, and starts each source file on a
new page. Output defaults to `<paper>/<paper>-dossier.docx`.

Styling is the house style: Calibri 11 / 1.15 line spacing, navy headings, shaded
table headers, 1" margins.

Markdown supported (the subset the templates actually use):
  # / ## / ###      headings          | a | b |        tables (--- separator row)
  *text* on line 2  centred subtitle  - / * / 1.       lists
  **bold** *italic* inline            > quote          --- rule
  `code` inline

Deliberately not a full Markdown implementation. The Markdown stays the source of
truth; this produces the copy that leaves the repo.
"""

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

NAVY = (0x1F, 0x3B, 0x57)
GREY = (0x33, 0x33, 0x33)
HEADER_FILL = "1F3B57"


# --- Document setup ----------------------------------------------------------


def new_document():
    doc = Document()

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = 1.15

    for name, size, colour in (("Heading 1", 15, NAVY),
                               ("Heading 2", 12.5, NAVY),
                               ("Heading 3", 11, GREY)):
        st = doc.styles[name]
        st.font.name = "Calibri"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor(*colour)
        st.paragraph_format.space_before = Pt(14)
        st.paragraph_format.space_after = Pt(6)

    for s in doc.sections:
        s.top_margin = s.bottom_margin = Inches(1)
        s.left_margin = s.right_margin = Inches(1)

    return doc


# --- Primitives (shared helpers) ---------------------------------


def para(doc, text="", style=None, bold=False, italic=False, size=None,
         align=None, space_after=None):
    p = doc.add_paragraph(style=style)
    if text:
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        if size:
            r.font.size = Pt(size)
    if align is not None:
        p.alignment = align
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p


def rich(doc, parts, style=None, space_after=None):
    """parts: list of (text, {bold/italic/size/colour}) tuples."""
    p = doc.add_paragraph(style=style)
    for text, fmt in parts:
        r = p.add_run(text)
        r.bold = fmt.get("bold", False)
        r.italic = fmt.get("italic", False)
        if "size" in fmt:
            r.font.size = Pt(fmt["size"])
        if "colour" in fmt:
            r.font.color.rgb = RGBColor(*fmt["colour"])
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p


def shade(cell, hexcolour):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hexcolour)
    tcPr.append(shd)


def table(doc, headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        emit_inline(p, h, base_bold=True, base_size=10)
        shade(hdr[i], HEADER_FILL)
        for r in p.runs:
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            if i >= len(headers):
                break
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            emit_inline(p, val, base_size=9.5)
    if widths:
        for r_ in t.rows:
            for i, w in enumerate(widths):
                r_.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t


# --- Inline Markdown ---------------------------------------------------------

INLINE = re.compile(r"(\*\*.+?\*\*|__.+?__|\*[^*]+?\*|_[^_]+?_|`[^`]+?`|\[.+?\]\(.+?\))")
LINK = re.compile(r"\[(.+?)\]\((.+?)\)")


def parse_inline(text):
    """Markdown inline -> [(text, fmt), ...]. Links render as their label."""
    parts = []
    for tok in INLINE.split(text):
        if not tok:
            continue
        if (tok.startswith("**") and tok.endswith("**")) or \
           (tok.startswith("__") and tok.endswith("__")):
            parts.append((tok[2:-2], {"bold": True}))
        elif (tok.startswith("*") and tok.endswith("*")) or \
             (tok.startswith("_") and tok.endswith("_")):
            parts.append((tok[1:-1], {"italic": True}))
        elif tok.startswith("`") and tok.endswith("`"):
            parts.append((tok[1:-1], {"colour": GREY}))
        elif LINK.fullmatch(tok):
            parts.append((LINK.fullmatch(tok).group(1), {}))
        else:
            parts.append((tok, {}))
    return parts


def emit_inline(p, text, base_bold=False, base_size=None):
    for chunk, fmt in parse_inline(text):
        r = p.add_run(chunk)
        r.bold = fmt.get("bold", False) or base_bold
        r.italic = fmt.get("italic", False)
        size = fmt.get("size", base_size)
        if size:
            r.font.size = Pt(size)
        if "colour" in fmt:
            r.font.color.rgb = RGBColor(*fmt["colour"])
    return p


# --- Block parsing -----------------------------------------------------------


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_separator(line):
    return bool(re.fullmatch(r"\|?[\s:|-]*-[\s:|-]*\|?", line.strip())) and "-" in line


def heading_levels(lines):
    """Map Markdown heading depth -> Word heading level.

    A document with a single `#` treats it as the title, and `##` sections become
    Word Heading 1 — matching how these reports are read in Word, where the title
    and the numbered sections sit at the same visual level.
    """
    tops = [ln for ln in lines if re.match(r"^#\s+", ln.strip())]
    demote = len(tops) == 1
    return lambda depth, first: 1 if first else max(1, min(depth - 1 if demote else depth, 3))


def render(doc, lines):
    i, n = 0, len(lines)
    seen_heading = False
    level_of = heading_levels(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Horizontal rule
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
            i += 1
            continue

        # Table: a pipe row followed by a separator row
        if stripped.startswith("|") and i + 1 < n and is_separator(lines[i + 1]):
            headers = split_row(stripped)
            rows, j = [], i + 2
            while j < n and lines[j].strip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            table(doc, headers, rows)
            i = j
            continue

        # Heading
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            first = not seen_heading
            level = level_of(len(m.group(1)), first)
            align = WD_ALIGN_PARAGRAPH.CENTER if first else None
            p = doc.add_paragraph(style=f"Heading {level}")
            emit_inline(p, m.group(2))
            if align is not None:
                p.alignment = align
            seen_heading = True
            i += 1
            continue

        # Centred italic subtitle: a fully-italic line immediately after the title
        if seen_heading and len(doc.paragraphs) <= 2 and \
                re.fullmatch(r"\*[^*]+\*", stripped):
            para(doc, stripped[1:-1], italic=True, size=12,
                 align=WD_ALIGN_PARAGRAPH.CENTER)
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            p = doc.add_paragraph()
            emit_inline(p, " ".join(block))
            p.paragraph_format.left_indent = Inches(0.35)
            for r in p.runs:
                r.italic = True
            continue

        # Lists
        m = re.match(r"^\s*([-*+]|\d+[.)])\s+(.*)$", line)
        if m:
            ordered = not m.group(1) in "-*+"
            style = "List Number" if ordered else "List Bullet"
            while i < n:
                mm = re.match(r"^\s*([-*+]|\d+[.)])\s+(.*)$", lines[i])
                if not mm:
                    break
                p = doc.add_paragraph(style=style)
                p.paragraph_format.space_after = Pt(3)
                emit_inline(p, mm.group(2))
                i += 1
            continue

        # Paragraph — join until a blank line or a new block starts
        block = []
        while i < n and lines[i].strip() and not lines[i].strip().startswith(("#", "|", ">")) \
                and not re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]) \
                and not re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", lines[i].strip()):
            block.append(lines[i].strip())
            i += 1
        p = doc.add_paragraph()
        emit_inline(p, " ".join(block))

    return doc


# --- Folder mode -------------------------------------------------------------


def _sibling_pdf_helpers():
    """Borrow md_to_pdf's folder ordering and link-cleaning.

    Single source of truth on purpose: if the two scripts each kept their own copy
    of FOLDER_ORDER, the .docx and the .pdf would silently drift apart in section
    order the first time one was edited.
    """
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    try:
        import md_to_pdf
    except ImportError:
        sys.exit("--folder needs md_to_pdf.py alongside this script")
    return md_to_pdf._resolve_order, md_to_pdf._clean


def add_toc(doc):
    """A real Word TOC field, marked dirty so Word populates it on open.

    Page numbers cannot be computed here — only Word knows where the pages fall —
    so this is a field, not a rendered list.
    """
    p = doc.add_paragraph()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), r'TOC \o "1-3" \h \z \u')
    fld.set(qn("w:dirty"), "true")
    run = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "Right-click and choose Update Field to build the contents."
    run.append(t)
    fld.append(run)
    p._p.append(fld)
    return p


def _navy(p):
    for r in p.runs:
        r.font.color.rgb = RGBColor(*NAVY)
    return p


def build_folder(folder, title, subtitle, toc=True):
    resolve_order, clean = _sibling_pdf_helpers()
    files = resolve_order(folder)
    if not files:
        sys.exit(f"no .md files found in {folder}")

    doc = new_document()

    for _ in range(6):
        doc.add_paragraph()
    _navy(para(doc, title, bold=True, size=21, align=WD_ALIGN_PARAGRAPH.CENTER))
    if subtitle:
        para(doc, subtitle, italic=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, _dt.date.today().strftime("%d %B %Y"), size=10,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    if toc:
        _navy(para(doc, "Contents", bold=True, size=15))
        add_toc(doc)
        doc.add_page_break()

    for i, f in enumerate(files):
        if i:
            doc.add_page_break()
        render(doc, clean(f.read_text(encoding="utf-8")).strip().splitlines())

    return doc, files


# --- CLI ---------------------------------------------------------------------


def main():
    if "--folder" in sys.argv[1:]:
        ap = argparse.ArgumentParser(prog="md_to_docx.py")
        ap.add_argument("output", type=Path, nargs="?")
        ap.add_argument("--folder", type=Path, required=True,
                        help="take every .md in this paper folder, in skill order")
        ap.add_argument("--title", help="cover title (default: folder name)")
        ap.add_argument("--subtitle", default="")
        ap.add_argument("--no-toc", action="store_true")
        args = ap.parse_args()

        folder = args.folder
        out = args.output or folder / f"{folder.resolve().name}-dossier.docx"
        doc, files = build_folder(folder, args.title or folder.resolve().name,
                                  args.subtitle, toc=not args.no_toc)
        doc.save(out)
        print(f"written: {out}")
        print(f"  files: {len(files)}  paragraphs: {len(doc.paragraphs)}  "
              f"tables: {len(doc.tables)}")
        for f in files:
            print(f"    - {f.relative_to(folder)}")
        return

    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".docx")

    text = src.read_text(encoding="utf-8")
    # Strip YAML front matter if present
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            text = text[end + 4:]

    doc = new_document()
    render(doc, text.splitlines())
    doc.save(out)

    print(f"written: {out}")
    print(f"  paragraphs: {len(doc.paragraphs)}  tables: {len(doc.tables)}")


if __name__ == "__main__":
    main()
