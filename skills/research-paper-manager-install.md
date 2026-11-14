% Research Paper Manager — Install Instructions
% Hand this whole file to an AI assistant and it will do the install
% Share freely

**Human: you do not need to read this file.** Open your AI assistant, attach or paste this
file, and say: *"Install this skill for me."* Then skip to
**research-paper-manager-how-to.md** and start using it.

Everything below is addressed to the assistant.

---

## Instructions for the AI assistant

You are installing a Claude Code skill called **research-paper-manager** for a research
student. It is a folder of Markdown instructions plus templates and two Python scripts —
there is nothing to compile and no network access required.

### What you are given

This file sits inside a `skills/` folder. Next to it is the skill itself:

```
skills/
  research-paper-manager/          ← the skill
    SKILL.md                       ← the instructions; this is the source of truth
    README.md                      ← what it does, for humans
    templates/                     ← 11 Markdown templates it fills in
    scripts/md_to_docx.py          ← Markdown → styled Word
    scripts/md_to_pdf.py           ← Markdown → single-file PDF
  research-paper-manager.zip       ← the same folder, zipped
  research-paper-manager-how-to.md ← the user-facing guide
  research-paper-manager-install.md ← this file
```

All paths in this file are **relative to the `skills/` folder that contains it**. Resolve
them against wherever the user actually put it; do not assume any absolute path.

### Step 1 — work out which tool you are

Pick the matching section below. If you cannot run shell commands or write files, use the
**ChatGPT** section, which needs neither.

| Tool | Reads/writes files? | Runs commands? | Result |
|------|:--:|:--:|:--:|
| **Claude Code** | ✅ | ✅ | ✅ native skill |
| **Cursor** | ✅ | ✅ (Agent) | ✅ via a Rule |
| **GitHub Copilot** (VS Code) | ✅ | ✅ (Agent mode) | ✅ via custom instructions / prompt file |
| **ChatGPT** (web) | ❌ | ❌ | ⚠️ generates content; the user saves it |

The Word and PDF steps need file and terminal access. Cursor and Copilot in agent mode
have it. ChatGPT does not — it still does every writing and checking workflow.

### Step 2 — install

#### Claude Code

Copy the skill folder into the user's skills directory. Ask which scope they want; default
to user-wide if they have no preference.

```bash
# user-wide — available in every project
mkdir -p ~/.claude/skills
cp -R research-paper-manager ~/.claude/skills/research-paper-manager

# or project-only — available in one repo
mkdir -p <repo>/.claude/skills
cp -R research-paper-manager <repo>/.claude/skills/research-paper-manager
```

If only the zip is present, `unzip research-paper-manager.zip` first.

Then verify, and tell the user what you found:

```bash
test -f ~/.claude/skills/research-paper-manager/SKILL.md && echo "SKILL.md present"
ls ~/.claude/skills/research-paper-manager/templates | wc -l    # expect 11
head -3 ~/.claude/skills/research-paper-manager/SKILL.md        # expect: --- / name: / description:
```

Tell the user to **start a new session** — skills are registered at session start, so it
will not appear in the one they are currently in.

Do **not** copy the folder onto a path that is already a symlink; that writes through the
link and produces a nested `research-paper-manager/research-paper-manager/`. Check with
`test -L` first and remove the link if so.

#### Cursor

Cursor uses **Rules**, not skills.

1. Create `.cursor/rules/research-paper-manager.mdc` in the user's project.
2. Put this header at the top, then paste the **entire body of `SKILL.md`** (everything
   after its closing `---`) beneath it:

   ```
   ---
   description: Manage an academic paper from plan to submission to reviewer response —
     literature scan, citation audit, pre-submission peer review, venue submission,
     reviewer response, AI-use disclosure.
   alwaysApply: false
   ---
   ```

   `alwaysApply: false` means Cursor loads it when relevant; the user can also invoke it
   by typing `@research-paper-manager`.
3. Copy the `templates/` folder into the project, e.g. `research/_templates/`.
4. Copy `scripts/` too if the user wants Word or PDF output.
5. Tell them to use the **Agent** (⌘I), which can read, write and run commands.

User-wide alternative: Cursor Settings → Rules → add it as a User Rule.

#### GitHub Copilot (VS Code)

1. **On-demand (recommended):** create `.github/prompts/research-paper-manager.prompt.md`
   and paste the `SKILL.md` body. The user runs it from Chat with
   `/research-paper-manager`.
2. **Always-on alternative:** paste the same body into `.github/copilot-instructions.md`.
   Copilot Chat then applies it automatically in that repo.
3. Copy `templates/` and `scripts/` into the repo.
4. Tell them to use **Agent mode** for the full workflow; Ask and Edit modes still produce
   the writing and checking output.

#### ChatGPT

No file access, so set it up as a content generator. Either:

- **Custom GPT** (needs a paid plan): Explore GPTs → Create. Paste the `SKILL.md` body into
  **Instructions**, upload the 11 `templates/` files as **Knowledge**, name it "Research
  Paper Manager", and share the link with classmates.
- **Project or plain chat:** create a ChatGPT **Project**, add the `SKILL.md` body as the
  project instructions, upload the templates. Or just paste `SKILL.md` at the top of a new
  chat.

Workflow to explain: the user pastes a manuscript or a reference list, gets back an audit,
a review, a roadmap or a draft, and saves it into their own files. Uploaded PDFs can be
read; files on their machine cannot be touched.

### Step 3 — optional dependencies

Only needed for Word and PDF output. Everything else works without them.

```bash
# macOS
brew install pandoc typst
# Debian / Ubuntu
sudo apt install pandoc          # then install typst from https://typst.app
```

`md_to_docx.py` needs `pandoc`. `md_to_pdf.py` needs `pandoc` and `typst`. If the user does
not want Word or PDF, skip this entirely and say so rather than installing silently.

### Step 4 — confirm and hand over

Report back, in plain language: where you installed it, whether the 11 templates are
present, whether pandoc and typst are available, and that they must start a new session.

Then point them at **research-paper-manager-how-to.md** and give them one thing to try:

> *"check my citations in <their manuscript file>"*

### What you must not do

- Do not rewrite `SKILL.md` to suit your own tool. Its rules — especially *gray zone =
  FAIL* and the ban on vibe citing — are the point of the skill. Reformat the wrapper,
  never the rules.
- Do not install anything beyond pandoc and typst, and only with the user's agreement.
- Do not put the user's paper drafts, data or unpublished work anywhere outside their own
  project folder.

*Made by a fellow scholar — improve it and pass it on.*
