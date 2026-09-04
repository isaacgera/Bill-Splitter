# Splitzy

A local-first, offline **bill splitter with tip**. Split one or more bills across a group,
add a tip, round shares if you like, and see what each person pays. Nothing leaves your
device &mdash; no account, no server, no tracking.

**Version:** 1.3.4 · **License:** MIT · Powered by Forjé

## Features

- **Multiple bills** &mdash; each with a description, amount, and date (DD/MM/YYYY).
- **Inline editing** &mdash; edit a bill in place; delete with a 5-second undo.
- **Add via dialog** &mdash; a compact "+ Add" pill opens a small entry dialog.
- **People &amp; tip** &mdash; directly editable fields with &minus;/+ steppers (tip defaults to 5%).
- **Round-Off** &mdash; toggle to round each share up to the next whole unit.
- **Currency** &mdash; ₹ INR (default), £ GBP, $ USD, € EUR, or no symbol; remembered between visits.
- **Consolidated split** &mdash; per-person amount from the combined subtotal + shared tip.
- **Summary export** &mdash; save as Image (PNG), PDF (via print), or copy as Text. No libraries.
- **5-second Undo** on delete and reset.
- **Light/dark theme** &mdash; follows the OS preference, with a persistent manual toggle.
- **In-app About/Help** and a full standalone User Guide.
- **Installable PWA** &mdash; works offline once loaded.
- **Hidden sample-data loader** for demos (see below).

## Running it

Splitzy needs an HTTP server for full PWA behaviour (install + offline). Opening the file
directly (`file://`) works for basic use but not for install/offline.

- **VS Code Live Server:** right-click `index.html` → *Open with Live Server*.
- **Or** run the bundled script: `powershell -ExecutionPolicy Bypass -File .\serve.ps1`
  then open `http://localhost:8091/`.

## Deployment

Static host (e.g. GitHub Pages, Netlify). Deploy the folder as-is; there is no build step.
Test the hosted version (not just local) to confirm PWA install and offline behaviour.

## Sample data (advanced, no UI)

For demos/testing, load a sample set of bills via any of:

- Open with `?sample=1` in the URL (auto-loads the bundled `sample-data.json`).
- Press `Ctrl+Shift+L` to pick a JSON file.
- Drag a JSON file onto the window.

Regenerate the sample with `generate-data.ps1`. All loads are validated and reversible via undo.

Data shape:

```json
{
  "version": "1.3.3",
  "currency": "inr",
  "people": 5,
  "tip": 10,
  "roundUp": false,
  "bills": [ { "desc": "Dinner", "amount": 4850.00, "date": "28/08/2026" } ]
}
```

## File structure

```
Bill Splitter/
  index.html               the app (HTML + inline CSS + JS, no build step)
  manifest.json            PWA manifest
  sw.js                    service worker (offline cache)
  icons/                   SVG + PNG icons (standard + maskable), plus generate-icons.py
  serve.ps1                local dev server (port 8091)
  generate-data.ps1        writes sample-data.json
  sample-data.json         bundled sample (6 bills, 5 people, INR)
  Splitzy-UserGuide.html   full user guide
  README.md                this file
  CHANGELOG.md             version history
  LICENSE                  MIT
  SESSION-LOG.md           development history
  prototypes/              layout prototype kept for reference
```

## Tech notes

- Vanilla HTML/CSS/JS, single file, no dependencies, no build step.
- Design tokens (CSS custom properties) with light/dark theming.
- Exports are library-free: PNG via the Canvas API, PDF via native print, Text via the Clipboard API.
- State is in-memory per session; the sample loader is the import path (validated, undoable).
- Accessibility: semantic markup, ARIA labels/roles, keyboard-friendly, honours `prefers-reduced-motion`.

## License

MIT &mdash; see [LICENSE](./LICENSE). Copyright (c) 2026 Isaac A. Gera.
