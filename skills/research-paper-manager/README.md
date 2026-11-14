# Research Paper Manager — a Claude Code skill

Take an academic paper from a half-formed idea through a verified literature base, a clean
citation record, a hostile pre-submission read, a venue submission, and a reviewer response.
Leaves a linked Markdown trail in the paper's folder, and a styled `.docx` or a single-file `.pdf` whenever something has
to leave the repo.

The thing this skill exists to prevent is a fabricated or drifted citation reaching a submitted
manuscript. Everything else is scaffolding around that.

**What it does**

| | Workflow | Trigger | Output |
|---|---|---|---|
| 🔍 | **Citation integrity check** | *"check my citations"* | `citation-audit.md` — every reference verified against the publisher record, every claim against what the source actually says |
| 💬 | **Reviewer response** | *"I got reviewer comments"* | `revision-roadmap.md` → `response-to-reviewers.md` |
| 📄 | **Start a paper** | *"new paper on X"* | folder scaffold + `00-strategy.md` + `paper-plan-<slug>.md` |
| 📚 | **Literature pass** | *"find papers on X"*, *"lit scan"* | `literature-matrix.md` + evidence cards + a lit-scan report |
| 🎭 | **Pre-submission review** | *"review this before I submit"* | `review-report.md` — 5 reviewer personas + a devil's-advocate pass |
| 📤 | **Venue attempt** | *"submitting to NMJI"* | `<venue>/` + cover letter + submission checklist |
| ⚖️ | **AI-use disclosure** | *"AI disclosure for X"* | disclosure written against the venue's actual policy |

## The rules it enforces

1. **Gray zone = FAIL.** A reference that cannot be independently confirmed does not go in.
   There is no "uncertain" verdict.
2. **No vibe citing** — never assemble a reference from remembered fragments of several papers.
3. **Every claim carries a citation**, or is flagged as the author's own contribution.
4. **Contradicting evidence is reported**, with a comparison of evidence quality.
5. **Source tiers are never flattened** — and are graded against each discipline's own standard.
6. **The search strategy is documented before searching**, not reconstructed after.
7. **A devil's-advocate pass runs before submission.**

## Install

1. Copy the whole `research-paper-manager/` folder into your Claude Code skills directory:
   - **Per user (all your projects):** `~/.claude/skills/research-paper-manager/`
   - **Per project (one repo):** `<repo>/.claude/skills/research-paper-manager/`
2. Start a new session. The skill auto-registers from its `SKILL.md`.

> **Developing the skill rather than just using it?** Symlink instead of copying, so edits go
> live without a re-install step:
> `ln -s <repo>/skills/research-paper-manager ~/.claude/skills/research-paper-manager`
> Copy is right for distribution; symlink is right for the machine you edit on.

## Use it

Ask in plain language — the skill loads itself:

- *"Find research papers on <topic>"* / `/deep-research`
- *"Check my citations in `manuscript-ises.tex`"*
- *"Review this before I submit to <venue>"*
- *"I got reviewer comments — here they are: …"*
- *"Start a new paper on <topic>, targeting <venue>"*

Or invoke it explicitly: `/research-paper-manager`.

## Word deliverables

Anything leaving the repo gets rendered **from the Markdown** — the Markdown stays the source of
truth:

```
python3 scripts/md_to_docx.py lit-scan-topic.md          # -> lit-scan-topic.docx
python3 scripts/md_to_docx.py report.md out.docx
python3 scripts/md_to_docx.py --folder <paper>           # -> <paper>/<paper>-dossier.docx
python3 scripts/md_to_pdf.py paper-dossier.pdf --folder <paper> --title "<Paper title>"
```

Both `--folder` modes take every `.md` in the paper folder in skill order, evidence cards last,
so the `.docx` and the `.pdf` stay in step — regenerate them together.

Calibri 11 / 1.15 spacing, navy headings, shaded table headers, 1" margins. Requires
`python-docx`. `pandoc file.md -o file.docx` is the quick alternative when styling doesn't matter.
`md_to_pdf.py` needs `pandoc` (>= 3.0) and `typst` — `brew install pandoc typst`; no LaTeX required.

## Templates

Copy from [`templates/`](templates/) — one per artefact the workflows produce:
`00-strategy.md`, `paper-plan.md`, `literature-matrix.md`, `evidence-card.md`,
`lit-scan-report.md`, `citation-audit.md`, `review-report.md`, `revision-roadmap.md`,
`response-to-reviewers.md`, `venue-checklist.md`, `ai-disclosure.md`.

## Scope

**In:** the lifecycle of one paper, plan → submission → reviewer response.
**Out:** coursework and PhD-plan year tracking.

## Privacy note

This skill organises files you give it and searches the public web for literature. It does not
upload your manuscript anywhere. Keep unpublished work in a private repo.

---
*Distils checklists and integrity gates from established academic-writing practice.*
