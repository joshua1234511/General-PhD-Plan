% Research Paper Manager — How to Use
% A Claude Code skill for research students
% Share freely

## What it does
Takes one paper from a half-formed idea to a submitted manuscript and a reviewer
response, leaving a linked Markdown trail in the paper's own folder.

The thing it exists to prevent is **a fabricated or drifted citation reaching a
submitted manuscript**. Everything else is scaffolding around that.

| | Workflow | Say this | You get |
|---|---|---|---|
| 🔍 | **Citation integrity check** | *"check my citations"* | every reference verified against the publisher record, every claim checked against what the source actually says |
| 💬 | **Reviewer response** | *"I got reviewer comments"* | a revision roadmap, then a point-by-point response letter |
| 📄 | **Start a paper** | *"new paper on X"* | folder scaffold, strategy note, paper plan |
| 📚 | **Literature pass** | *"find papers on X"*, *"lit scan"* | a literature matrix, evidence cards, a scan report |
| 🎭 | **Pre-submission review** | *"review this before I submit"* | 5 reviewer personas plus a devil's-advocate pass |
| 📤 | **Venue attempt** | *"submitting to NMJI"* | venue subfolder, cover letter, submission checklist |
| ⚖️ | **AI-use disclosure** | *"AI disclosure for X"* | a disclosure written against that venue's actual policy |

The two worth having even if you use nothing else are **citation integrity check** and
**reviewer response**.

## Install (once, ~1 minute)
1. Get the `research-paper-manager/` folder (or unzip `research-paper-manager.zip`).
2. Copy it into your Claude Code skills directory:
   - All your projects: `~/.claude/skills/research-paper-manager/`
   - One repo only: `<repo>/.claude/skills/research-paper-manager/`
3. Start a new Claude Code session. Done — it auto-registers.

Not using Claude Code? See **research-paper-manager-install.md** — it covers Cursor,
GitHub Copilot and ChatGPT, and you can hand that file straight to an AI assistant and
let it do the install for you.

## The rules it enforces
These are the point of the skill. It will push back on you.

1. **Gray zone = FAIL.** A reference you cannot independently confirm exists does not go
   in the paper. It is never marked "uncertain".
2. **No vibe citing.** Never assemble a reference out of remembered fragments of two or
   three real papers. This is the hardest fabrication to detect and the most damaging
   when caught.
3. **Every claim carries a citation**, or is explicitly marked as your own contribution.
4. **Contradicting evidence gets reported**, with a comparison of evidence quality — not
   quietly dropped.
5. **Every paper has an explicit limitations section.**
6. **Source tier discipline.** Peer-reviewed > preprint > grey literature, never
   flattened. Grading is relative to the field: a qualitative study meeting its own
   discipline's gold standard rates highly.
7. **The search strategy is documented** — databases, Boolean strings, date ranges,
   inclusion and exclusion criteria — so someone else can reproduce it.
8. **Devil's advocate before submission.** One pass whose only job is to find the
   strongest argument against your paper.

## Set up your first paper
Make a `research/` folder. Then just say *"new paper on <your topic>"* and it scaffolds
the rest: a strategy note, a paper plan, a bibliography, and the folders for evidence,
data and figures. Templates for every artefact live in the skill's `templates/` folder if
you would rather start one by hand.

Name each folder after the paper, not the venue — a paper usually outlives its first
venue, and the skill keeps one subfolder per venue attempt underneath.

## Word and PDF
It ships two small Python scripts that turn your Markdown into a styled `.docx` or a
single-file `.pdf` — for supervisors who want Word, and for journals that want a PDF.
They need `pandoc` installed; the PDF path also needs `typst`. Both are one `brew install`
away on a Mac.

## Handy to know
- It reads Word, Excel and PDF that you give it. It uploads nothing on its own.
- Verification means real lookups against publisher records — expect it to be slower and
  more sceptical than a chatbot. That is the feature.
- Keep your paper folder private if the work is unpublished.

*Made by a fellow scholar — improve it and pass it on.*
