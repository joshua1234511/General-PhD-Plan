---
name: research-paper-manager
description: Manage an academic paper from plan to submission to reviewer response, as clean Markdown plus Word and PDF deliverables. Use when starting a new paper, running a literature scan or evidence-verified lit review, auditing every citation in a manuscript against what the sources actually say, running a simulated pre-submission peer review, preparing a submission for a specific journal or conference, parsing reviewer comments into a revision roadmap and rebuttal, or writing an AI-use disclosure against a venue's actual policy. Triggers include "new paper on X", "export this paper as a PDF", "make a dossier PDF", "find research papers on X", "deep research", "lit scan", "literature review for X", "literature matrix", "check my citations", "citation audit", "verify these references", "review this before I submit", "devil's advocate pass", "submitting to <venue>", "cover letter for <venue>", "submission checklist", "I got reviewer comments", "respond to reviewers", "revision roadmap", "AI disclosure for X".
---

# Research Paper Manager

Take a paper from a half-formed idea through a verified literature base, a clean citation
record, a hostile pre-submission read, a venue submission, and a reviewer response — leaving a
linked Markdown trail in the paper's folder, plus a styled `.docx` or a single-file `.pdf`
whenever something has to leave the repo.

The thing this skill exists to prevent is a fabricated or drifted citation reaching a submitted
manuscript. Everything else is scaffolding around that.

## When to use

- The user says **"new paper on X"** → scaffold the folder, write strategy and plan (**A**).
- The user says **"find papers on X"**, **"lit scan"**, **"/deep-research"** → verified
  literature pass (**B**).
- The user says **"check my citations"** before a submission → citation audit (**C**).
- The user says **"review this before I submit"** → 5-persona review + devil's advocate (**D**).
- The user says **"submitting to <venue>"** → venue attempt folder + checklist (**E**).
- The user pastes **raw reviewer comments** → revision roadmap, then rebuttal (**F**).
- The user says **"AI disclosure for <venue>"** → disclosure against that venue's policy (**G**).

Out of scope: coursework and PhD-plan year tracking.

## Folder convention

One folder per paper, under a `research/` directory you create. Name each folder after the
paper, not the venue — a paper often outlives its first venue. Follow this layout; do not
invent a new one.

```
<paper-slug>/
  00-strategy.md               # why this paper, target venues in tier order, status
  paper-plan-<slug>.md         # RQ, contribution, structure, word budget
  references-<slug>.md         # working bibliography
  manuscript-<slug>.tex|md     # the draft
  literature-matrix.md         # source × theme + the search strategy
  evidence/<author-year>.md    # one evidence card per source that carries weight
  citation-audit.md            # verification verdicts
  data/                        # + README.md describing each dataset
  figures/                     # + make_figures.py that regenerates every one
  ethics/                      # IRB / consent, where the study needs it

  <venue-slug>/                # one folder per submission attempt
    README-<venue>.md          # deadline, status, what was sent, what came back
    cover-letter.md
    title-page.md
    submission-checklist.md
    reviews.md                 # raw reviewer comments, verbatim as received
    revision-roadmap.md        # parsed, classified, prioritised
    response-to-reviewers.md
    apply_<venue>_format.py    # if the venue needs a specific format

  <slug>-dossier.pdf          # whole folder rendered to one PDF, for sharing
  slides.md  linkedin.md  op-ed.md  email-<audience>.md  outreach/
```

Templates for every Markdown file above are in [`templates/`](templates/) — copy and fill.
`<paper-slug>` and `<venue-slug>` are short kebab-case.

**Never auto-fill author identity.** Leave `Author`, `Authors`, `Prepared for`, affiliation, roll
number and contact fields as `*TBC*` unless the user states, in this conversation, who the
authors of *this* paper are. Do not carry a name, institution, student ID or ORCID over from
another paper, from memory, or from the environment — authorship differs per paper, and a
pre-filled name is wrong more often than it is right. The same applies to programme context:
write "a wider research programme", not a specific named thesis, unless the user ties this paper
to one. Identity goes in at submission time (Workflow E `title-page.md`), from what the user
tells you then.

**Every paper folder is self-contained.** Never write a `../` link from one paper folder into
another — no "builds on", no "see the related paper", no shared reference file. Papers get
submitted, zipped, shared with co-authors and moved; a cross-folder link breaks the moment the
folder travels, and it leaks one venue's material into another's submission bundle. If a paper
genuinely stands on earlier work, **cite it as a published reference** in
`references-<slug>.md`, or restate the relevant fact in prose inside this folder. Links *within*
a paper folder are encouraged — cross-link strategy ↔ plan ↔ matrix ↔ audit ↔ venue folders
freely. The only file that may point across folders is a top-level dashboard that lives outside
them all.

## Conventions

- **Venue attempt status:** 📝 preparing · 📤 submitted · 💬 under review · 🔁 revising ·
  ✅ accepted · ❌ rejected. Record the date of every transition in `00-strategy.md`.
- **Citation audit verdict:** ✅ verified (source exists, DOI resolves, claim matches) ·
  ⚠️ claim drift (source exists but does not say what we say it says) · ❌ FAIL (cannot
  confirm it exists). **There is no "uncertain".**
- **Source tier:** peer-reviewed journal · conference · preprint · grey literature. Record the
  tier on every source. Never flatten them.
- **Grade sources against their own discipline's standard**, not a single cross-field pyramid —
  a qualitative study meeting its field's gold standard rates highly.
- **Revision roadmap status:** ⬜ open · 🔁 in progress · ✅ done · 🚫 declined (with reason).
- **Links are clickable** — cross-link strategy ↔ plan ↔ matrix ↔ audit ↔ venue folders **within
  the same paper folder only**. Never `../` into a sibling paper.
- **Convert relative dates to absolute** ("last month" → the actual date).
- **Never overwrite the author's prose.** Mark and propose; the voice is theirs.

## Workflows

Ordered by value. C and F are the ones that earn their keep.

### C. Citation integrity check

Run before **every** submission. Output: `citation-audit.md`
([template](templates/citation-audit.md)).

1. Extract every in-text citation from the manuscript and every entry from the reference list.
2. Diff the two — a reference cited but not listed, or listed but not cited, is a finding.
3. For each reference: WebFetch the DOI or a publisher/database URL. Confirm the **authors,
   year, title, venue and volume/pages all match**. A DOI that resolves to a different paper is
   ❌, not ✅.
4. For each in-text use: read what the source actually claims and compare it to our sentence.
   Different → ⚠️ claim drift. Record the supporting quote or page for the ✅ ones.
5. Sweep for **uncited assertions** — empirical or contested claims carrying no citation and
   not flagged as our own contribution.
6. Report. Every ❌ either gets a real replacement source or the claim comes out of the paper.

### F. Reviewer response

Two passes, with the author's decisions in between. Never draft the rebuttal in the same pass
that parses the comments.

1. Save the reviewer comments **verbatim** to `<venue>/reviews.md` before touching anything.
2. Parse into `revision-roadmap.md` ([template](templates/revision-roadmap.md)): one row per
   distinct request — **split bundled comments**, reviewers routinely put three asks in one
   paragraph. Classify type and severity; name the section each lands in.
3. Surface **conflicts between reviewers** explicitly and recommend a side with a reason.
4. Flag requests worth declining. Declining is legitimate; declining silently is not.
5. Stop. Get the author's calls on the majors and the declines.
6. Draft `response-to-reviewers.md` ([template](templates/response-to-reviewers.md)) — point by
   point, quoting each comment, stating the change and **where it now appears**.
7. Audit the rebuttal before sending: every comment answered, every claimed change actually
   present in the manuscript, tone civil throughout.

### A. Start a paper

1. Create `<paper-slug>/` per the folder convention.
2. Write `00-strategy.md` ([template](templates/00-strategy.md)): the argument for this paper,
   its contribution, and **target venues in tier order** with deadlines and fit notes.
3. Write `paper-plan-<slug>.md` ([template](templates/paper-plan.md)): research questions,
   contribution claim, section structure with a word budget, data and method, planned figures.
4. Do **not** start drafting prose. Run Workflow B first — the plan changes once the literature
   is actually verified.

### B. Literature pass

Output: `literature-matrix.md`, evidence cards, and a `lit-scan-<topic>.md` report.

1. **Write the search strategy table before searching** ([template](templates/literature-matrix.md)):
   databases, Boolean strings, date range, language, inclusion and exclusion criteria, date run.
   Searching first and documenting after produces an irreproducible scan.
2. **Check the construct exists.** Before assuming the user's term is established, search for it
   as a defined construct. If it is not in the literature as framed, that is the headline
   finding — say so plainly and early. It reframes the whole project and is worth more than a
   list of loosely-related papers.
3. WebSearch broadly, then **WebFetch every candidate** to verify it exists and capture the full
   citation. A search-result snippet is not verification.
4. Write an evidence card ([template](templates/evidence-card.md)) for each source that carries
   weight — separating **what it claims** from **what it actually shows**.
5. Fill the matrix: source × theme, with tier, method, sample, key finding and limitation.
6. Record **convergence and divergence** — where sources disagree, both sides appear, with a
   comparison of evidence quality.
7. Write the report ([template](templates/lit-scan-report.md)). The **Flagged and Unverified
   Sources** section is required and must appear even when empty — it is where Gray-zone-=-FAIL
   becomes visible to the reader.
8. Render to `.docx` if it is going to a supervisor or collaborator (see **Word deliverables**).

### D. Pre-submission review

Output: `review-report.md` ([template](templates/review-report.md)).

1. Read the manuscript in full first.
2. Review as five distinct personas, each writing independently — do not blend them:
   **methodologist** (design, analysis, threats to validity) · **domain expert** (novelty,
   whether the contribution is real) · **statistician / analyst** (do the numbers support the
   claims) · **writing and structure** · **ethics and integrity** (disclosure, data, consent).
3. Run the **devil's-advocate pass**: one pass whose only job is the strongest argument against
   the paper. If the answer is "the contribution is incremental", say it.
4. Write an editorial decision — accept / minor / major / reject — with the reasoning.
5. Turn the majors into a work list. Anything unfixable becomes an explicit limitation.

### E. Venue attempt

1. Create `<venue-slug>/`. Never edit a previous attempt's folder — each submission is a record.
2. Read the venue's **current** author guidelines from its site; do not rely on memory.
3. Fill `submission-checklist.md` ([template](templates/venue-checklist.md)) against those
   guidelines.
4. Convert the manuscript to the required format and citation style; anonymise if required —
   including **file metadata and self-citations**.
5. Draft `cover-letter.md`: the contribution in three sentences, the fit with this venue, and
   the declarations the venue asks for.
6. Update the status legend and date in `00-strategy.md`.

### G. AI-use disclosure

Fetch the venue's **actual published policy** with its URL and the date checked, then fill
[`templates/ai-disclosure.md`](templates/ai-disclosure.md). Be specific and bounded about what
tools did what — vague disclosure reads worse than none. Generic statements written from memory
are a failure mode; policies differ sharply between venues.

## Iron rules

1. **Gray zone = FAIL.** A reference that cannot be independently confirmed does not go in.
2. **No vibe citing** — never assemble a reference from remembered fragments of several papers.
3. **Every claim carries a citation**, or is explicitly flagged as the author's own contribution.
4. **Contradicting evidence is reported**, with a comparison of evidence quality.
5. **Every paper has an explicit limitations section.**
6. **Source tiers are never flattened** — peer-reviewed > preprint > grey literature, graded
   relative to the discipline's own standards.
7. **The search strategy is documented** — databases, Boolean strings, dates, in/out criteria.
8. **A devil's-advocate pass runs before submission** — one pass whose only job is to build the
   strongest case against the paper.

## Anti-patterns

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Marking an unverifiable reference "uncertain" | It survives into the submitted draft | Gray zone = FAIL |
| Citing the one supportive study | Cherry-picking; a reviewer will find the other three | Report the full landscape |
| Treating a blog post as a peer-reviewed source | Tier inflation | Apply the hierarchy strictly |
| Rewriting the author's prose wholesale | Loses their voice and their argument | Propose edits, keep the voice |
| Trusting a search-result snippet as a citation | Snippets misattribute authors and years | WebFetch and verify every one |
| Assuming the user's construct exists in the literature | Builds a paper on a term nobody uses | Verify the construct first (B2) |
| Searching first, documenting the strategy after | Irreproducible; a reviewer can ask | Write the strategy table first |

## Reading non-Markdown inputs (macOS-friendly)

- **.docx / .doc:** `textutil -convert txt -output out.txt "file.docx"`, or
  `pandoc "file.docx" -o out.md` to keep structure.
- **.pdf:** read directly; long PDFs in page ranges. Only write a *verified* evidence card
  after actually reading the PDF — mark abstract-only cards as such.
- **.tex:** read directly. `\cite{}` keys map to the `.bib` or `references-<slug>.md`.
- **.xlsx:** Python `openpyxl`, `load_workbook(path, data_only=True)`.

## Word and PDF deliverables

Anything leaving the repo — a supervisor, a collaborator, a venue that wants Word — is rendered
**from the Markdown**, never authored separately. The Markdown stays the source of truth; a
deliverable that has been hand-edited after export is a deliverable that will drift.

**Word** — for anything the recipient will comment on or track changes in.

```bash
# one artefact, styled (Calibri 11/1.15, navy headings, shaded table headers)
python3 scripts/md_to_docx.py <in.md> <out.docx>

# whole paper folder, in skill order, one .docx — the twin of the dossier PDF below
python3 scripts/md_to_docx.py --folder <paper> <paper>/<slug>-dossier.docx \
  --title "<Paper title>" --subtitle "<what this bundle is>"
```

Quick and unstyled, when the house style does not matter: `pandoc file.md -o file.docx`.

Folder mode shares `md_to_pdf.py`'s ordering and link-cleaning, so the `.docx` and the `.pdf`
carry the same sections in the same order — **ship both from the same run**, or they drift. It
adds a cover page and a Word **TOC field**: page numbers only exist once Word paginates, so the
contents populate on open (or on Update Field), not at export time.

**PDF** — for anything read rather than edited: a dossier for a supervisor, a scan report going
to a co-author, a fixed record of what was submitted.

```bash
# whole paper folder, in skill order, one PDF
python3 scripts/md_to_pdf.py <paper>/<slug>-dossier.pdf --folder <paper> \
  --title "<Paper title>" --subtitle "<what this bundle is>"

# or named files, in the order given
python3 scripts/md_to_pdf.py out.pdf a.md b.md c.md --title "…"
```

Requires `pandoc` (≥ 3.0) and `typst` — `brew install pandoc typst`. No LaTeX needed. The script
builds a cover page and contents, starts each source file on a new page, keeps long tables
breaking across pages with a repeating header, and **unlinks relative links** — a `.md` link that
resolves inside the repo is dead in a PDF that has left it.

**Regenerate every deliverable whenever the Markdown changes** — the `.docx` as well as the
`.pdf`. A stale dossier next to an updated folder is worse than no dossier: it is a confident,
wrong snapshot.

## Style

- Scannable: tables, short bullets, bold key terms. One idea per line.
- Decisive: state the finding, then the evidence. Do not bury a null result in hedging.
- Faithful: never invent findings, numbers, or sources to fill a thin section. An empty cell
  marked "not found" is a legitimate result.
- Say what the author must **do** next, at the end of every artefact.

See [`README.md`](README.md) for install and sharing.
