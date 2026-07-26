---
name: coursework-manager
description: Organise and track university/PhD coursework as clean Markdown. Use when capturing class/lecture session notes, filing uploaded course documents (PDF/DOC/DOCX/XLSX) into the right course folder, turning readings into class-ready briefings (abstract + critical questions to ask), building an at-a-glance dashboard with progress bars and a session schedule, or maintaining per-course assignment/term-project trackers with a submit→feedback→rework pipeline. Triggers include "capture my class notes", "update coursework", "file these course documents", "briefing notes for this reading", "coursework dashboard", "assignment tracker", "term project tracker", "questions to ask in class", "schedule of classes".
---

# Coursework Manager

Turn a student's messy inputs — live class notes, uploaded PDFs, a schedule spreadsheet,
an instructor email — into a clean, linked, trackable Markdown coursework vault. Works for
any degree (PhD, Master's, undergrad) and any set of courses.

## When to use
- The user pastes/dictates **class session notes** (often with typos, mid-lecture) → capture them.
- The user drops files in an **uploads folder** and says "file these" → route to the right course.
- The user shares a **reading** or an instructor asks them to read one → make a briefing.
- The user wants to **see everything at a glance** → build/refresh the dashboard.
- The user wants to **track assignments/term projects** through submit → feedback → rework.

## Folder convention

```
coursework/
  README.md                     # index: course table + link to dashboard
  dashboard.md                  # at-a-glance: progress bars, status, schedule
  Schedule-<term>.xlsx          # source schedule (if provided)
  <course-slug>/
    README.md                   # syllabus, instructor, assessment, readings
    notes.md                    # running session notes (newest first)
    project-tracker.md          # assignment/term-project pipeline
    reading-materials/
      briefing-notes.md         # class-ready abstracts + questions for readings
      <papers/slides>.pdf
    assignments/
      <assignment files & drafts>
```

Use a short kebab-case `<course-slug>` (e.g. `qualitative-techniques`). Templates for every
file above are in [`templates/`](templates/) — copy and fill them.

## Conventions (keep these consistent)
- **Status legend:** ⬜ not started · 🟡 in progress · ✅ done.
- **Deliverable pipeline:** `⬜ Not started → ✍️ Drafting → 📤 Submitted → 💬 Feedback → 🔁 Reworking → ✅ Done`.
- **Progress bar:** 20 chars, `█` filled / `░` empty, 5% each, followed by `NN%  done/total`.
- **Notes:** newest session at the TOP of `notes.md`, each under a `## Session — <date> · <topic>` heading.
- **Links are clickable** — cross-link notes ↔ readings ↔ tracker ↔ dashboard.
- **Convert relative dates to absolute** (e.g. "tomorrow" → the actual date).
- Only append to notes; **never delete** a student's captured point.

## Workflows

### A. Capture a class session
1. Identify which course it belongs to (topic, instructor name, timetable).
2. Open that course's `notes.md`; add a `## Session — <date> · <topic>` block at the top.
3. Expand the user's rough bullets into structured notes: key concepts, definitions,
   any exercise/assignment announced, and **fix typos** silently.
4. Add a short **"Questions to ask in class"** list (this is often graded participation).
5. Optionally add a **"Links to my research/thesis"** line if the user has a research theme.
6. If the user is feeding points live ("session going on"), keep appending each point and
   supplying questions until they say the session is over.

### B. File uploaded documents
1. List the uploads folder; read/scan each file (see **Reading non-Markdown** below).
2. Decide the course by content + who sent it (instructor name → course).
3. Decide the sub-folder: a **reading/slide** → `reading-materials/`; an **assignment brief
   or a draft to submit** → `assignments/`.
4. **Move** (not copy) the file in, with a clean kebab-case name (author-year where useful).
5. Update that course's `README.md` "readings on file" list and, for readings, add a
   briefing entry (Workflow C). Record any Google/Zoom links in the README.
6. Leave the uploads folder empty. Then summarise **what the user must DO** (read by when,
   submit what, confirm any missing deadline).

### C. Briefing notes for a reading
For each reading, add to the course `reading-materials/briefing-notes.md`:
- **One-line abstract** + section-wise key points (from the actual PDF if available;
  if written from general knowledge, mark it and say to verify against the real paper).
- **Questions to ask in class** — sharp, critical, discussion-worthy.
- Optional: a **research hook** connecting it to the student's own work.
- Link the source file. Deep-read the PDF when the user asks for a verified upgrade.

### D. Dashboard
Maintain `coursework/dashboard.md` (template provided):
- A **4-column-plus course table**: course, code, instructor, sessions done→next, status, key assessment, links.
- **Progress bars** for sessions completed per course + overall, plus a mermaid `pie`.
- An **assignments/term-project** mini-table (in progress / submitted / graded / marks secured).
- **Next class day(s)** with prep, a **things-done / things-to-do** list, and the **full schedule**.
- If a schedule spreadsheet is provided, parse it (see below) and reconstruct the calendar;
  flag any gaps or ambiguous dates rather than guessing.

### E. Project / assignment tracker
Per course, maintain `project-tracker.md` (template provided):
- An **overview table**: deliverable · weight · status · due · submitted · grade/feedback · next action.
- A **per-deliverable cycle log** where each round is a dated line
  (draft → submit → paste feedback → rework → done). Update status through the pipeline.
- Keep a **marks-secured** tally. If weightings are unknown, mark **TBC** and remind the user to get them.

### F. Progress log (optional)
If the vault has a `progress.md`, add a one-line weekly entry after each work cycle
(what moved → next), newest first.

## Reading non-Markdown inputs (macOS-friendly)
- **.doc / .docx:** `textutil -convert txt -output out.txt "file.doc"` then read `out.txt`.
  (Cross-platform: `pandoc "file.docx" -o out.txt`.)
- **.xlsx / .xls:** Python `openpyxl` (`load_workbook(path, data_only=True)`, iterate rows).
  Watch for Excel mangling `DD/MM/YYYY` into US dates — correct against the weekday column.
- **.pdf:** read directly; for long PDFs read in page ranges. Do a **verified** briefing only
  after actually reading the PDF.
- **Produce Word docs** for "submit in Word" assignments: `pandoc file.md -o file.docx`.

## Style
- Scannable: tables, short bullets, bold key terms. One idea per line.
- Faithful: expand the user's points; don't invent lecture content they didn't give.
  When you add standard theory to flesh out a thin bullet, say so, so they can trim it.
- Decisive: when a file's course is obvious, file it and report; only ask when genuinely ambiguous.

See [`templates/`](templates/) for ready-to-copy `dashboard.md`, `notes.md`,
`briefing-notes.md`, `project-tracker.md`, and `course-README.md`.
See [`README.md`](README.md) for how to install and share this skill.
