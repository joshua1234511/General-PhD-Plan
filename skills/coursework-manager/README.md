# Coursework Manager — a Claude Code skill

Turn messy student inputs — live class notes, uploaded PDFs, a schedule spreadsheet, an
instructor email — into a clean, linked, trackable Markdown coursework vault. Works for any
degree and any set of courses.

**What it does**
- 📝 Captures **class session notes** (fixes typos, structures them, adds *questions to ask in class*).
- 📥 **Files uploaded documents** (PDF/DOC/DOCX/XLSX) into the right course's folder.
- 📚 Writes **class-ready briefings** for readings — abstract + critical questions.
- 📊 Builds an **at-a-glance dashboard** — progress bars, a mermaid chart, and the full class schedule.
- ✅ Maintains **per-course assignment/term-project trackers** with a
  `Not started → Drafting → Submitted → Feedback → Reworking → Done` pipeline.

## Install (each classmate does this once)
1. Copy the whole `coursework-manager/` folder into your Claude Code skills directory:
   - **Per user (all your projects):** `~/.claude/skills/coursework-manager/`
   - **Per project (one repo):** `<repo>/.claude/skills/coursework-manager/`
2. Restart Claude Code (or start a new session). The skill auto-registers from its `SKILL.md`.

## Use it
Just ask in plain language — Claude will pick up the skill automatically. Examples:
- *"Capture my class notes: <paste>"*
- *"I dropped files in `uploads/` — file them into the right course."*
- *"Make briefing notes for this reading with questions to ask."*
- *"Build a coursework dashboard with progress bars and the schedule."*
- *"Set up a term-project tracker for my qualitative course."*

Or invoke explicitly: `/coursework-manager`.

## First-time setup for your vault
Create a `coursework/` folder and, per course, copy the templates from
[`templates/`](templates/): `course-README.md`, `notes.md`, `briefing-notes.md`,
`project-tracker.md`, plus one `dashboard.md` at the top. Then just talk to Claude as your
term goes on — it keeps them updated.

## Share
Zip the folder and send it, or commit it to a shared repo:
```
cd ~/.claude/skills && zip -r coursework-manager.zip coursework-manager
```
Classmates unzip into their own `~/.claude/skills/`.

## Privacy note
This skill only organises files you give it. It does not upload anything. Keep your vault in
a private repo (or a git-ignored folder) if your notes are sensitive.

---
*Made by a fellow scholar — improve it and pass it on.*
