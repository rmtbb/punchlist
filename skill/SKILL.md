---
name: punchlist
description: Present a batch of mixed feedback items as an interactive markdown punchlist the user works through — in the companion Punchlist app (a stylized, themeable viewer that writes answers back to the file) or any markdown editor — then read their inline answers back and action them. Use when you have MANY items or HETEROGENEOUS response types (yes/no, free-text notes, "you-run-this", FYI/parked) that the user will chew on at their own pace. Trigger word "/punchlist", or any ask like "make me a punchlist / worklist / checklist I can run through". Do NOT use for 4-or-fewer crisp synchronous decisions you need answered this turn — that is what the native AskUserQuestion tool is for.
trigger: /punchlist
---

# /punchlist — interactive markdown feedback list

A single markdown file the user works down top-to-bottom — answering each item inline — then says "check the punchlist" so you read their answers back and action them. Re-entrant: they fill some, you action, they fill more.

The markdown file is always the source of truth. The user can work it in two surfaces, and you write the **same format** either way:

- **The Punchlist app** (preferred) — a stylized, themeable single-file viewer that renders the punchlist and **writes answers + checkboxes straight back into the `.md`**. This is the companion tool to this skill; see "Open it" below.
- **Any markdown editor** — the file is plain markdown, so editing it by hand works exactly the same. This is the fallback when the app isn't available or the user prefers their editor.

## When to use this vs. AskUserQuestion

| Situation | Tool |
|---|---|
| ≤4 crisp, mutually-exclusive choices you need answered **this turn** to proceed | **AskUserQuestion** (native) |
| Many items, OR mixed response types (yes/no + free-text + "you run this" + FYI), OR the user wants to work async at their own pace, OR the set will evolve over several passes | **punchlist** |

If it's a quick synchronous fork, use AskUserQuestion. If it's a batch of feedback to chew on at leisure, use punchlist.

## Trigger behavior (proactive-but-ask)

- **Explicit:** the user typed `/punchlist` (or "make me a punchlist/worklist/checklist"). Build it.
- **Proactive:** when you're about to present a batch that fits the punchlist profile above, **offer first** — "Want this as a punchlist you can work through?" — and only build on their yes. Don't silently turn prose summaries into files.

## Where to put the file

Put the punchlist where the user's editor and the app can both reach it — a dedicated punchlists folder, the current project directory, or (if the user keeps notes in an Obsidian-style vault) the vault root. Name it `_punchlist-YYYY-MM-DD.md` (the underscore sorts it with other working files; add a short slug if there may be more than one a day). Get today's date from the session context, not by guessing.

## Open it

### Preferred: the Punchlist app

The app is a single self-contained `index.html` from this repo. It parses the punchlist, renders a themeable interactive view, and autosaves the user's answers + checkboxes back into the `.md` via the File System Access API. **Write-back needs a Chromium browser** (Chrome / Edge / Arc) — Safari/Firefox can load + edit but only download a copy.

Open it in a Chromium browser (point `PUNCHLIST_APP` at your clone, or edit the default path):

```bash
APP="${PUNCHLIST_APP:-$HOME/punchlist/index.html}"
if [ -f "$APP" ]; then
  opened=""
  for B in "Google Chrome" "Arc" "Microsoft Edge" "Brave Browser"; do
    if open -Ra "$B" >/dev/null 2>&1; then open -a "$B" "$APP"; opened=1; break; fi
  done
  [ -z "$opened" ] && open "$APP"   # default browser; note Safari can't write back
fi
```

(On Linux, swap the `open -a` lines for `google-chrome "$APP"` / `xdg-open "$APP"`.)

**How the app reaches today's file** (tell the user the first time): the app has a **folder mode** — they click **"Open a folder"** once and pick the folder where you write these. After that it auto-opens the **newest** `_punchlist-*.md` (today's) every launch, with a dropdown to switch days. Because the app autosaves into the file, when they say "check the punchlist" you just **Read the same `.md`** — their answers are already there.

### Fallback: a markdown editor

If the app isn't present, or the user prefers their editor, open the file by **absolute path**:

```bash
open "/absolute/path/to/_punchlist-YYYY-MM-DD.md"     # macOS; use xdg-open on Linux
```

For Obsidian specifically you can use `obsidian://open?path=<url-encoded-absolute-path>`. Either way the format is identical, so the user can mix surfaces freely (app on the laptop, editor on the phone).

## File format

Group items by what they need. Skip empty groups. Each actionable item gets a line or two of context, an optional `Options:` hint, and a `➡️ YOU:` line the user types on. FYI/done items need no input line.

```markdown
# Punchlist — YYYY-MM-DD

Work top to bottom. Type your answer on each `➡️ YOU:` line (yes / no / a choice / free notes), or tick the box. Save, then tell me "check the punchlist" and I'll action everything you've answered and leave blanks alone.

---

## ✅ Already done (FYI, no action)
- [x] **<thing>** — <one line on what happened>

## 🟡 Needs your call
### 1. <Item> — <ref if any>
<1-2 lines of context so the answer is obvious without leaving the file.>
- Options: `optionA` / `optionB` / `hold`

➡️ YOU:

### 2. <Item>
...
➡️ YOU:

## 🔵 You run this one (I can't)
### N. <Item>
<commands or steps in a fenced block>

➡️ YOU (done? / error?):

---

## Rules I'm holding to
- I won't take any notifying or irreversible action (send, post, resolve, delete) until you've answered it here AND, where the harness requires it, re-confirmed in chat (see note below).
- Anything you mark, I action. Anything blank, I leave alone.
```

Keep per-item context tight — the user should never have to leave the file to know what they're answering.

## The interaction loop

1. Build the file, open it (the app if present, else their editor), and tell the user it's open — fill the `➡️ YOU:` lines and tick the boxes, then say "check the punchlist." In the app, answers autosave as they type; in an editor they just save normally.
2. On "check the punchlist" (also accept "check the list / worklist", "k check", etc.): **Read the file** (the single source of truth, regardless of surface), parse each `➡️ YOU:` line and checkbox.
3. Action every answered item. For each, annotate the file **inline** under the item with its outcome so the file stays the source of truth:
   - `**→ DONE:** <what happened>`
   - `**→ BLOCKED:** <why / what's needed>` and mark the header `⏳`
   - `**→ HELD:** <why>` for deliberate no-ops
   Mark resolved item headers with `✅`/`⏳` so progress is visible at a glance.
4. Leave blank items untouched.
5. Report a compact table of what you did and what's still open, and invite the next pass.
6. The file is re-entrant — the user may fill more and call "check the punchlist" again. Keep going until everything's resolved.
7. When everything's resolved, offer to delete or archive the punchlist file so it doesn't linger.

## Permission gotcha (important)

The harness's permission classifier can't read the punchlist file's contents when it evaluates a tool call. So an answer like "close it" written in the file is **not** sufficient authorization for a *notifying or irreversible* action (resolving a ticket, sending a message, deleting data) — the classifier may block it because it can't verify the approval. When that happens:
- Don't fight it. Surface it: tell the user the action is blocked and ask them to confirm **in chat** (e.g. "say 'close #244'"), which the classifier can see.
- Annotate that item `**→ BLOCKED ON YOUR APPROVAL:**` in the file with exactly what to say.
- Read-only and local actions (file edits, local git, file ops) generally go through fine.

## Cleanup

A punchlist is a transient working surface for one feedback round, not a permanent tracker. When items graduate into ongoing work, move them into the project's real task tracker and let the punchlist be archived or deleted.
