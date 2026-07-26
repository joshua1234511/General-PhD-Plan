% Coursework Manager — How to Use
% A Claude Code skill for students
% Share freely

## What it does
Turns messy inputs — live class notes, uploaded PDFs, a schedule spreadsheet, an
instructor email — into a clean, linked, trackable Markdown coursework vault. For any
degree, any courses.

- **Class notes** → structured, typos fixed, with *questions to ask in class*.
- **Uploaded files** (PDF/DOC/DOCX/XLSX) → filed into the right course folder.
- **Readings** → class-ready briefings (abstract + critical questions).
- **Dashboard** → progress bars, a chart, and the full class schedule at a glance.
- **Assignments/term projects** → trackers with a `Not started → Drafting → Submitted → Feedback → Reworking → Done` pipeline.

## Install (once, ~1 minute)
1. Get the `coursework-manager/` folder (or unzip `coursework-manager.zip`).
2. Copy it into your Claude Code skills directory:
   - All your projects: `~/.claude/skills/coursework-manager/`
   - One repo only: `<repo>/.claude/skills/coursework-manager/`
3. Start a new Claude Code session. Done — it auto-registers.

## Use it (just ask in plain English)
- "Capture my class notes: …"
- "I dropped files in `uploads/` — file them into the right course."
- "Make briefing notes for this reading, with questions to ask."
- "Build a coursework dashboard with progress bars and the schedule."
- "Set up a term-project tracker for my qualitative course."

Or type `/coursework-manager` to invoke it explicitly.

## Set up your vault (first time)
Make a `coursework/` folder. Per course, copy the templates from the skill's
`templates/` folder: `course-README.md`, `notes.md`, `briefing-notes.md`,
`project-tracker.md`; put one `dashboard.md` at the top. Then just talk to Claude as
the term goes — it keeps everything updated.

## Handy to know
- Reads Word (`.doc/.docx`) and Excel (`.xlsx`) you give it; can produce Word docs for
  "submit in Word" assignments.
- Only organises files you provide — it uploads nothing. Keep your vault private if your
  notes are sensitive.

*Made by a fellow scholar — improve it and pass it on.*
