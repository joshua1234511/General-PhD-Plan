% Coursework Manager — Install on Cursor, GitHub Copilot & ChatGPT
% Same instructions, different packaging per tool
% Share freely

The skill is just **instructions + templates** (in `SKILL.md` and `templates/`). Any AI
assistant can use them — you only change *where you paste them*. The source of truth is
`coursework-manager/SKILL.md`; copy its body wherever a tool asks for "instructions/rules".

## What transfers (and what doesn't)
| Tool | Reads/writes your files? | Runs commands (move files, pandoc)? | Full skill works? |
|------|:--:|:--:|:--:|
| **Claude Code** | ✅ | ✅ | ✅ native (`SKILL.md`) |
| **Cursor** | ✅ | ✅ (Agent) | ✅ via a Rule |
| **GitHub Copilot** (VS Code) | ✅ | ✅ (Agent mode) | ✅ via custom instructions / prompt file |
| **ChatGPT** (web) | ❌ local files | ❌ | ⚠️ Generates the content; you paste inputs & save outputs |

> The **filing/dashboard/pandoc** steps need file + terminal access. Cursor and Copilot
> (agent mode) have it, so the whole workflow runs. ChatGPT can't touch your computer — it
> still writes great notes/briefings/trackers as text for you to copy into files.

---

## Cursor
Cursor uses **Rules** instead of skills.
1. In your project, create `.cursor/rules/coursework-manager.mdc`.
2. Paste the **body of `SKILL.md`** into it, with this header on top:
   ```
   ---
   description: Organise & track university coursework — class notes, filing course
     files, reading briefings, dashboard, assignment trackers.
   alwaysApply: false
   ---
   ```
   (`alwaysApply: false` = Cursor pulls it in when relevant; you can also invoke it by
   typing `@coursework-manager` in chat.)
3. Copy the `templates/` folder into your project (e.g. `coursework/_templates/`).
4. Use the **Agent** (⌘I) and ask in plain English — it can read/write files and run the
   `pandoc`/`textutil` commands, so the full workflow works.
   *(User-wide alternative: Cursor Settings → Rules → add it as a User Rule.)*

## GitHub Copilot (VS Code)
Copilot uses **custom instructions** and **prompt files**.
1. **Always-on:** create `.github/copilot-instructions.md` and paste the `SKILL.md` body.
   Copilot Chat applies it automatically in that repo.
2. **On-demand (recommended):** create `.github/prompts/coursework-manager.prompt.md`,
   paste the `SKILL.md` body, then run it from Chat with `/coursework-manager`.
3. Copy the `templates/` folder into the repo.
4. Use **Copilot Chat in Agent mode** (it can edit files and run terminal commands) for the
   full workflow; Ask/Edit mode still generates the notes/briefings.

## ChatGPT
No file access, so use it as a **content generator**. Two good setups:
- **Custom GPT** (needs ChatGPT Plus): *Explore GPTs → Create*. Paste the `SKILL.md` body
  into **Instructions**, upload the five `templates/` files as **Knowledge**, name it
  "Coursework Manager", and share the link with classmates.
- **Project** (or plain chat): create a ChatGPT **Project**, add the `SKILL.md` body as the
  project instructions and upload the templates. Or simply paste `SKILL.md` at the top of a
  new chat.
- **Workflow:** paste your class notes / a reading's text → it returns structured notes,
  briefings, or a tracker (use **Canvas** for long docs) → you copy the output into your
  own files. Upload a PDF and it can read it; it just can't move files on your machine.

---

## Keep one source of truth
Edit `coursework-manager/SKILL.md`, then re-paste it into each tool when you change it. The
`templates/` files are identical everywhere.

*Made by a fellow scholar — improve it and pass it on.*
