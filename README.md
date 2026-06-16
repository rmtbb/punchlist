# 📋 Punchlist

**A beautiful, themeable lens over a plain markdown checklist — that writes your answers _straight back into the file_.**

One self-contained `index.html`. No build. No server. No dependencies. No account. No tracking. Double-click it and go.

> The markdown is the source of truth. Punchlist is just a really nice way to live inside it.

---

## 😤 The problem (you've felt this)

You're working with a coding agent — Claude Code, Cursor, whatever's hot this week. It's cranking. And then it stops and hits you with **the wall of questions**:

> "Should I close these 6 tickets? Which database for the cache? Want me to delete the old migration? Here are 9 findings, which do you want fixed? Also pick a name for the service. Also—"

Now you're stuck. Chat is a **terrible** surface for this:

- 🌀 Answer in prose and your replies get tangled — "yes to 1 and 3, no to 4, skip 2, do 5 later."
- ⏳ You can't think about #7 for an hour without blocking the whole thread.
- 🧠 The agent loses the thread, you lose the thread, everyone loses the thread.
- 📜 Two messages later you're scrolling up going "wait, what was item 4 again?"

A batch of decisions isn't a conversation. **It's a list.** It wants to be a document you chew on at your own pace — tick a box here, type a note there, leave the hard one blank till after lunch — and then hand back, answered.

So: make it a list. A markdown file. The agent writes the questions, **you** fill in the answers inline, and the agent reads them back and acts. Clean contract. The file is the API between you and your robot.

The only problem with raw markdown is that staring at forty `➡️ YOU:` lines in a text editor is... bleak.

**That's Punchlist.** It turns that file into a gorgeous, interactive, themeable UI — and every checkbox you tick and every answer you type **autosaves right back into the same `.md`**. The agent never has to leave the file. Neither do you.

---

## ✨ What you get

- 🎯 **Answer at your own pace.** Work top to bottom, tick boxes, type answers, click an `Options:` chip to drop it into the field. Leave the hard ones blank. Come back later.
- 💾 **Write-back to the actual file.** In Chrome / Edge / Arc, every edit autosaves to the same `.md` via the [File System Access API](https://developer.mozilla.org/en-US/docs/Web/API/File_System_Access_API). The agent reads the identical file back. No copy-paste, no export dance.
- 🩹 **Surgical, never destructive.** It rewrites *only* the answer lines and checkbox markers it owns, by line number. Your prose, headings, tables, and formatting are never re-serialized or touched.
- 🎨 **Themeable to the teeth.** Presets, custom colors, any Google Font by name, your own logo or wordmark — all stored in your browser, never written into the markdown.
- 📁 **Folder mode.** Point it at a folder once; it auto-opens the **newest** `_punchlist-*.md` every time, with a dropdown to switch days. One click to today's list.
- ✏️ **Edit anything.** Pencil any block to edit its raw markdown, `＋` to drop a note anywhere, `🗑` to delete one. It's your file.
- 🪶 **Zero everything.** One HTML file, ~50KB, no build step, no server, no npm install, works offline. Your data never leaves your machine.

---

## 🚀 Quickstart

```bash
git clone https://github.com/rmtbb/punchlist.git
cd punchlist
open index.html        # macOS — or just double-click it
```

1. Click **Open a file** and pick any markdown checklist (try `examples/sample-punchlist.md`).
2. Type into the answer fields, tick boxes — it autosaves back to the file (Chromium browsers).
3. That's it. There is no step 3.

> 🧭 **Write-back needs a Chromium-based browser** (Chrome, Edge, Arc, Brave). Safari/Firefox can still load + edit, but **Save** downloads an updated copy instead of writing in place.

---

## 📝 The format (it's just markdown)

Punchlist reads plain markdown plus a couple of featherweight conventions:

| You write | You get |
|---|---|
| `# Title` | the document title |
| `## 🔴 Section` | a collapsible section (the leading emoji sets the accent color) |
| `### Item` | an item card |
| `➡️ YOU:` | an editable answer field — **the thing that writes back** |
| `- [ ] task` / `- [x] done` | a checkbox (writes back) |
| `- Options: ` `` `lock it` `` ` / ` `` `hold` `` | clickable chips that fill the answer |
| tables, **bold**, `code`, [links], ~~strike~~, `[[wikilinks]]` | rendered |

A tiny example:

```markdown
# Punchlist — Launch

## 🔴 Needs you now

### 1. Lock the launch date
Marketing wants the 14th; eng prefers the 21st. No wrong answer — just lock it.
- Options: `the 14th` / `the 21st` / `one more day`

➡️ YOU:

### 2. Release checklist
- [ ] Cut the release branch
- [x] Update the changelog
- [ ] Smoke-test staging

➡️ YOU:
```

Open that in Punchlist and it becomes a clickable, themeable, self-saving control panel. Edit it in plain Obsidian on your phone and it's... still just a markdown file. Mix surfaces freely — the format is identical everywhere.

---

## 🤖 Built for the human-in-the-loop

Punchlist was born working alongside agentic coding tools, where the agent regularly needs a batch of decisions from a human without stalling the whole session. The pattern is dead simple and tool-agnostic:

1. **The agent writes a punchlist** — every open question as a `➡️ YOU:` line or checkbox.
2. **You work it in Punchlist** at your own pace; answers autosave into the `.md`.
3. **The agent reads the same file back** and actions everything you answered, leaving blanks alone.
4. **Repeat.** It's re-entrant — answer a few more, hand it back, keep going.

It pairs naturally with a [Claude Code](https://www.anthropic.com/claude-code) skill that generates the daily `_punchlist-YYYY-MM-DD.md` and pops this app open — but nothing here is tied to any one agent or vendor. Any tool (or human) that can write a markdown file can drive it. It's equally happy as a plain personal to-do list with no robot in sight.

---

## 🎨 Theming

Everything visual is a theme, stored in `localStorage` — it never touches your markdown. Open the 🎨 panel to:

- pick a **preset** (Aurora / Midnight / Paper) or go fully Custom,
- upload **any logo** or set a wordmark,
- set **any colors** — accent, background, surface, text, the answer + done colors, borders,
- set **any fonts** — type any Google Font family name and it loads on the fly,
- **export / import** a theme as JSON to share or reuse.

The bundled default is **Aurora**, an indigo/violet dark palette. Make it yours in about thirty seconds.

---

## ⌨️ Good to know

- **`⌘S` / `Ctrl+S`** — save now.
- **Top bar** — live completion ring (answered + checked / total), per-section counts, and connection state.
- **Filters** — show *unanswered only*, *open checkboxes only*, or search items by text.
- **Privacy** — there is no backend. Nothing is uploaded. Your files stay on your disk, full stop.

---

## 🛠️ How it works under the hood

- The whole app is one `index.html` (HTML + CSS + vanilla JS, no framework).
- Markdown is parsed into lines; each interactive control remembers its **line number**.
- Typing into an answer edits that one line in place. Add / edit / delete operations splice the markdown and re-render, recomputing every line map — your scroll position and collapsed sections survive.
- Writes go through the File System Access API to the file handle you granted; it's remembered across sessions so reopening is one click.

No magic, no lock-in. Worst case, close the tab and your markdown is exactly where you left it.

---

## 🗺️ Roadmap-ish ideas (not built)

- A hosted version (it's static — any static host works).
- Drag-to-reorder items.
- More presets, because why not.

PRs and ideas welcome.

---

## 📄 License

[MIT](LICENSE) © Remote BB. Do whatever you want with it.

---

<sub>Made because answering a robot's twenty questions in a chat box is a special kind of pain. 📋</sub>
