# Splitzy — Session Log

A local-first Bill Splitter with tip, built as an installable PWA (vanilla HTML/CSS/JS, no build step).

---

## Session 1 — 28 Aug 2026

### Goal
First build of a Simple-tier app to exercise the new build-mode workflow end to end. Started in **Default (Vibe)** mode.

### Build-standards flags (agreed up front)
- **Rigour:** Simple tier — tidy single-file app, readable and correct, no over-engineering, no test framework/build step.
- **Stack:** Vanilla HTML/CSS/JS. A framework would add a build step + Windows tooling for zero benefit on a single-page calculator. Matches the no-build / Live Server workflow.
- **Platform:** Installable PWA (Isaac's usual preference), responsive desktop-to-mobile, touch-friendly.
- **Monetization:** Not a candidate; utility tool. Nothing flagged.

### What we built (initial "SplitEasy")
- Single-page app: bill amount, people stepper (1–99), tip presets (0/5/10/15/20%) + custom %, round-up-per-person toggle, live per-person / tip / total, Reset + Copy-summary.
- PWA: `manifest.json`, `sw.js` (cache-first + navigation fallback), two SVG icons (standard + maskable), `serve.ps1` on port 8091.
- Design tokens, light/dark theming (`prefers-color-scheme` + persistent manual toggle), ~160ms motion with reduced-motion guard, ARIA labels / `aria-pressed` / `aria-live`, safe-area insets, local-first.

### Enhancements this session (renamed to "Splitzy", v1.1.0)
After Isaac's live check, five changes:
1. **Renamed** SplitEasy → **Splitzy** across title, manifest, SW cache, serve script, storage keys.
2. **Currency selector** in the header — No symbol (agnostic) / £ GBP / $ USD / ₹ INR / € EUR. Persists to `splitzy-currency` (default GBP). Applies to bill rows and all outputs.
3. **Fixed the round-up toggle.** Root cause: the visible `.track`/`.thumb` overlay could sit above the hidden checkbox, so clicks didn't always land. Fixed with explicit z-index layering (input z2, thumb z1, track z0) + `inset:0` on the input. Round-up now clearly changes the per-person figure and shows an explanatory note.
4. **Horizontal layout.** CSS grid: inputs (left) and results (right, sticky) side by side ≥760px; stacks to one column on mobile.
5. **Multiple bills.** `state.bills` = list of `{ desc, amount }` rows with add/remove (remove disabled at 1 row). Shows a bills subtotal; the consolidated total (subtotal + shared tip) is split across the shared people count. Copy-summary lists each bill.

### Key decisions
- **Consolidated split model:** one shared tip rate and one people count applied to the combined subtotal (simplest read of "consolidated split"). Per-bill tips / different people per bill were considered and deferred — would be a bigger data model.
- **Currency:** offered both requested options at once — an agnostic "No symbol" plus a symbol picker — rather than choosing one.
- **Cache bump** to `splitzy-v1.1.0` so the rename/enhancements reach any installed PWA.

### Files
```
Bill Splitter/
  index.html          single-page app (CSS + JS inline)
  manifest.json        PWA manifest (Splitzy)
  sw.js                service worker, cache splitzy-v1.1.0
  serve.ps1            local dev server on :8091
  icons/icon.svg, icons/icon-maskable.svg
  SESSION-LOG.md       this file
```

### Verification
- **By inspection:** all files present; manifest well-formed with paths matching real files; round-up math traced (e.g. 100 + 10% tip = 110 / 3 = 36.67 → £37.00 each, note "collects £111.00, £1.00 over"); currency wiring and multi-bill subtotal logic reviewed.
- **Not run here:** live browser/HTTP test — blocked by the known Windows shell quirk (terminal prepends a `cd` line; command exits 1 with no output). PowerShell JSON-parse check also hit this.
- **Isaac's manual check:** open via Live Server (or `serve.ps1` → http://localhost:8091/). Confirm: round-up toggles and changes per-person; currency switch updates all figures; add/remove bills updates the consolidated split; layout goes side-by-side on a wide window and stacks on mobile; theme persists across reload; SW registers (DevTools → Application).

### Known follow-ups / ideas
- Icons are SVG (standard + maskable), not the full PNG set — add PNGs later if wider install compatibility is wanted.
- Possible future: per-bill tip or per-bill people; remember last session's bills; export/share summary.

### Next session
- Fold Isaac's live-check results back in (any tweaks).
- Update `Ideas.md`: mark **Tip / Bill Splitter** as Built (Splitzy v1.1.0).
- Consider User Guide + About/Help if it graduates from a demo to a keeper.

---

## Session 2 — 28 Aug 2026 (v1.2.0)

### Goal
Second round of refinements after Isaac's live check of v1.1.0. Still **Default (Vibe)** mode, still vanilla / no-build / offline-first.

### Changes
1. **Three cards side by side.** Layout is now a responsive grid: three columns (Bills | Split settings | Result) ≥1020px; two columns 620–1019px with the Result card spanning full width beneath; single column on mobile. Max width widened to 1180px.
2. **Currency-toggle bug fixed + no negatives.**
   - *Bug:* switching currency mid-entry rebuilt every bill row from state, which re-stringified amounts and could wipe a mid-edit field. *Fix:* `setCurrency()` now calls `refreshCurrencySymbols()`, which updates only the currency symbol spans in place — entered values are left exactly as typed.
   - *Negatives blocked:* `parseNum()` clamps anything `< 0` to 0; a keydown guard blocks `-`, `+`, `e`, `E` on amount and tip inputs; `min="0"` set; a pasted negative is corrected on input.
3. **Per-bill date.** Each bill now has a date field defaulting to today (`todayISO()`), fully editable. Stored on `state.bills[i].date` and shown in the summary as dd/mm/yyyy. Bill rows became small cards: top row = description + remove, bottom row = amount + date.
4. **Save as PNG / PDF (library-free).**
   - *PNG:* renders the summary onto a `<canvas>` (device-pixel-ratio aware) and downloads `splitzy-summary-<date>.png`. No dependency.
   - *PDF:* opens a scoped, styled print window and auto-triggers the browser print dialog → Save as PDF. No dependency.
   - A shared `summaryLines()` feeds Copy, PNG and PDF (lists each bill with its date, subtotal, tip, total, people, each-pays).
   - Results actions are now a 4-button grid: Reset / Copy / Save PNG / Save PDF.

### Key decisions
- **Kept Splitzy library-free** to preserve pure offline + no-build. PNG via Canvas, PDF via native print. A true one-click `.pdf` (jsPDF) was consciously deferred; would mean caching a library into the SW. Flagged to Isaac; can revisit if he wants it.
- **Cache bumped** to `splitzy-v1.2.0` so updates reach installed PWAs.

### Verification
- **By inspection:** currency change no longer touches values (only symbol spans); negative guard covers typing, pasting and the number spinners; date defaults to today and flows into all three exports; PNG/PDF use only built-in browser APIs (offline-safe); responsive breakpoints reviewed.
- **Not run here:** live browser test (Windows shell quirk unchanged).
- **Isaac's manual check:** enter a couple of bills → switch currency (values must stay put, only the symbol changes) → try typing a negative amount (should be rejected) → edit a bill date → Save PNG (downloads an image) → Save PDF (print dialog opens; choose Save as PDF; pop-ups must be allowed) → check three cards sit side by side on a wide window and stack on mobile.

### Next session
- Fold in Isaac's live-check feedback.
- Decide on true one-click PDF (jsPDF) vs keeping the print route.
- Update `Ideas.md`: mark Tip / Bill Splitter as Built (Splitzy v1.2.0).

---

## Session 2b — 28 Aug 2026 (v1.2.1 — hotfix)

### Problem (reported by Isaac, with screenshot)
- No bill row showing; "Add another bill" and all buttons dead; raw JavaScript printed as text at the bottom of the page.

### Root cause
- The PDF export built its print window by concatenating a **literal `<script>…</script>` tag inside the parent page's own script block** (`"<script>window.onload=…<\/script>"`). That embedded opening tag broke script parsing, so the entire Splitzy script was treated as text and never executed — which is why nothing rendered and no buttons worked.

### Fix
- Removed the embedded script-tag string from `savePDF()`. The print is now triggered from the parent via `w.print()` on a short timeout after `w.document.close()`, so no literal `<script>` ever appears in the file.
- Verified there is now exactly one `<script>` open + one `</script>` close in the file, with none in between.
- Cache bumped to `splitzy-v1.2.1`.

### Verification
- By inspection: script block is well-formed; `renderBills()` runs at init (creates the first bill row); all button listeners wired. Fix directly addresses all three reported symptoms.
- Not run here: live browser test (Windows shell quirk). **Isaac to re-check:** a bill row shows on load; Add another bill works; Copy / Save PNG / Save PDF / Reset all work; no code text at the bottom. Hard-refresh to pick up `splitzy-v1.2.1`.

---

## Session 3 — 28 Aug 2026 (v1.3.0 — major UI redesign)

### Goal
Redesign the Splitzy UI from scratch based on iterative prototyping with Isaac. Moved from the original three-card layout to a confirmed **Option C (refined v3)** two-card layout, with significant interaction model changes.

### Prototype process
- Built 3 layout prototypes (A — Form/Receipt, B — Compact, C — Nested Split) in a single toggleable file.
- Isaac chose **Option C**, then iterated through 4 rounds of refinement:
  1. Shorter cards, one-liner bills with inline edit/delete, compact tip stepper (1% steps, default 5%), Summary dialog.
  2. Edit happens in-line on the row (not a separate area), People/Tip as directly editable number fields, Add via a dialog from a top-right "+" pill, Round-Off as a toggle switch beside the result.
  3. Undo toast for Delete and Reset (5 seconds), Round-Off pinned right with result centered, currency defaults to INR.
  4. Reset → compact "Reset" pill (centered), Save/Print Summary → "Summary" pill (same style), toast on export options, full tooltips + ARIA.
- Prototypes folder: `prototypes/prototype-c-refined.html` (kept for reference); the earlier `layouts.html` was deleted.

### What we built (v1.3.0)
Complete rewrite of `index.html`. All interactions are functional (not placeholder).

**Layout:**
- Two equal-width, equal-height cards side by side (CSS grid `1fr 1fr`), stacking on mobile (≤720px).
- Left = Bills card; Right = Result card.

**Bills card (left):**
- Card header with title + a compact **"+ Add" pill** (top-right) that opens a **dialog** for entering description / amount / date (DD/MM/YYYY, defaults to today).
- Each saved bill shows as a **compact one-liner** with description, date, amount, and inline pencil (edit) + trash (delete) icons on the right.
- **Inline edit:** clicking the pencil turns that row into editable fields in place (desc / amount / date), with ✓ save and ✕ cancel mini-buttons.
- **Delete** with 5-second **undo toast** (state snapshot, countdown, Undo button restores the removed bill to its exact position).
- Bills subtotal shown below.
- **Split Settings** nested sub-panel: People (left, `[−] [editable field] [+]`) and Tip (right, `[−] [editable field]% [+]`). Both accept direct typing. Default: 2 people, 5% tip, 1% steps.
- **Reset** as a compact centered pill button. Fires a 5-second undo toast that restores the complete prior state.

**Result card (right):**
- Large centred per-person amount with a **Round-Off toggle switch** ("Round-Off") pinned to the right of the same row (CSS grid 3-col: spacer | amount | toggle).
- Subtitle "each · N people".
- Breakdown: subtotal, tip amount, total with tip, each pays.
- **Summary** button (centered pill, same style as Reset) opens an **export dialog** with three options:
  - **Image (PNG):** renders summary to a canvas (device-pixel-ratio aware) and downloads `splitzy-summary.png`. Fires toast "Summary saved as image."
  - **PDF:** opens a styled print window and triggers `window.print()` for Save-as-PDF. Fires toast "Opening print — choose Save as PDF." No embedded `<script>` tag (the bug from v1.2.0 is gone; print is called from the parent via setTimeout).
  - **Text:** copies a plain-text summary to the clipboard. Fires toast "Summary copied as text."

**Other:**
- **Currency selector** in the header (No symbol / ₹ INR / £ GBP / $ USD / € EUR). Defaults to **₹ INR**, persists to `splitzy-currency` localStorage key. Changing it updates all displays without rebuilding bills (symbol swap in place via recalc).
- **Light/dark theme toggle** (persists to `splitzy-theme`, respects `prefers-color-scheme`).
- **Non-negative amounts:** keydown guard blocks `-`, `e`, `E`, `+` on the Add-dialog amount field; `parseAmt` clamps to 0.
- **DD/MM/YYYY** date format throughout (input, summary, exports).
- **Accessibility:** tooltips (`title`) and ARIA labels on all interactive controls; `aria-haspopup="dialog"` on buttons that open dialogs; `role="switch"` on Round-Off; `aria-live="polite"` on the result value and toast; decorative SVGs `aria-hidden`; `role="list"` / `role="listitem"` on the bills container. `prefers-reduced-motion` respected.
- **PWA:** service worker registered; cache `splitzy-v1.3.0`.
- Footer: "Works offline · Nothing leaves your device · v1.3.0".

### Key decisions
- **Add via dialog, edit inline** — two different mechanisms for a reason: adding is a deliberate action (dialog from a pill), editing an existing bill is quick (in-place on the row).
- **Tip default 5%, People default 2** — rounded to a practical everyday scenario.
- **Currency default INR** — per Isaac's request.
- **No library for exports** — PNG via Canvas API, PDF via native print, Text via Clipboard API. Keeps the app fully offline, no dependencies.
- **Reset and Summary matched** — both are compact self-sizing pill buttons, same secondary styling, centered in their respective cards.

### Files changed
```
Bill Splitter/
  index.html      — full rewrite (v1.3.0)
  sw.js           — cache bumped to splitzy-v1.3.0
  manifest.json   — unchanged (already correct)
  prototypes/prototype-c-refined.html — prototype kept for reference
```

### Verification
- **By inspection:** no embedded `<script>` tag in the JS (the v1.2.0 bug); no stray literals; script block is well-formed (one open, one close); all DOM IDs match between HTML and JS; `esc()` used on user content to prevent XSS in innerHTML; `parseAmt` clamps negatives; currency symbol updates go through `recalc()` not `renderBills()` so existing typed values are preserved. Round-up logic: `Math.ceil(each)` only when `roundUp && each > 0`.
- **Not run here:** live browser test (same Windows shell constraint). Isaac to do a full click-through.
- **Isaac's manual check:** open via Live Server → add a bill via the dialog → edit inline → delete (see undo toast + undo) → type into People/Tip fields → flip Round-Off → switch currency → try negatives → Summary → Image (downloads PNG) / Text (clipboard) / PDF (print dialog) → Reset (undo toast) → theme toggle → check responsive (narrow window stacks cards).

### Next session
- Isaac's live-check feedback on v1.3.0.
- If confirmed: flip `Ideas.md` from In Progress → Built (Splitzy v1.3.0).
- Possible follow-ups: full PNG icon set, User Guide, deployment.

---

## Session 3b — 28 Aug 2026 (v1.3.1 — hotfix)

### Problem (reported by Isaac)
- Buttons not working again in v1.3.0.

### Root cause
- The PDF export's `pw.document.write(...)` string contained literal closing tags — `</style>`, `</head>`, `</body>`, `</html>` — inside the main page's `<script>` block. While only `</script>` strictly terminates a script element, these embedded closing tags can confuse the HTML parser in some browsers and are the same class of hazard that broke v1.2.0. (Likely compounded by the old service worker serving a stale cached page — a hard refresh is needed.)

### Fix
- Rebuilt the PDF window HTML string with the closing tags split into fragments (`"<" + "/style>"`, `"<" + "/head>"`, etc.) so no literal closing tag appears in the source. Pulled the CSS into its own `css` variable for readability.
- Confirmed the only remaining literal closing tags inside `<script>` are `</td></tr>` (harmless — do not terminate a script) and the single legitimate `</script>` at the end.
- Cache bumped to `splitzy-v1.3.1`; footer shows v1.3.1.

### Verification
- By inspection: script block well-formed (one open, one close), no embedded page-structural closing tags, all handlers intact.
- **Isaac to re-check with a HARD REFRESH** (Ctrl+Shift+R) or unregister the service worker (DevTools → Application → Service Workers) so the stale cache is replaced by `splitzy-v1.3.1`. Then confirm all buttons work and no code text shows.

---

## Session 3c — 28 Aug 2026 (v1.3.2 — data loader)

### Goal
Add a WealthOrah-style sample data loader to Splitzy, but with the load control hidden from the UI (Isaac's request).

### What we built
- **`generate-data.ps1`** — WealthOrah-style PowerShell generator. Writes `sample-data.json` with 6 INR bills, a group of **5 people**, 10% tip, round-off off. Dates are relative to today (dd/MM/yyyy). Run: `powershell -ExecutionPolicy Bypass -File .\generate-data.ps1`.
- **`sample-data.json`** — created directly too so it exists immediately. Shape matches Splitzy state:
  `{ version, currency, people, tip, roundUp, bills:[{desc, amount, date}] }`.
- **Hidden import in `index.html`** — no visible button. Three ways to load:
  1. **Drag-and-drop** a JSON file anywhere on the window.
  2. **Ctrl+Shift+L** opens a hidden file picker.
  3. **`?sample=1`** in the URL auto-loads the bundled `sample-data.json` via fetch.
- `applyData()` **validates** input (filters bad bill entries, clamps negative amounts to 0, checks currency against the known list, coerces people/tip) and is **wrapped in the 5-second undo** so an accidental load is reversible (restores bills, people, tip, roundUp, currency).
- `sample-data.json` added to the service-worker ASSETS so `?sample=1` works offline.

### Notes / decisions
- Splitzy had **no JSON import** before this; the loader doubles as Splitzy's first import path (validated, non-destructive via undo) without adding save/export UI — kept minimal and hidden per request.
- Data-safety: import can't corrupt state silently (validation + undo), consistent with the family data-safety standard.
- Cache bumped to `splitzy-v1.3.2`; footer + JS VERSION now 1.3.2.

### Verification
- By inspection: `applyData` validation and undo wiring reviewed; sample JSON is well-formed and matches state shape; SW caches the sample file.
- **Isaac to check (hard-refresh first for the new SW):** open `index.html?sample=1` → 6 bills + 5 people load, undo toast appears; also try dragging `sample-data.json` onto the window and Ctrl+Shift+L. Re-run `generate-data.ps1` to regenerate with today's dates if wanted.

### Next session
- Confirm v1.3.2 + loader; if all good, flip `Ideas.md` to Built (Splitzy v1.3.2).
- Optional: deploy via Netlify power for a real hosted URL.

---

## Status update — 28 Aug 2026: Built

Isaac confirmed v1.3.2 (with the hidden data loader) works well. Per the backlog-sync
rule, `Ideas.md` flipped from **In Progress → Built (Splitzy v1.3.2)**.

Splitzy is now feature-complete for this cycle: two-card Option C layout, multi-bill with
inline edit + Add dialog, People/Tip steppers, Round-Off toggle, 5s undo, currency (INR
default), Image/PDF/Text export, hidden sample-data loader, light/dark theme, offline PWA.

### Possible future work (not committed)
- Deploy to a real hosted URL (Netlify power) and verify the installed PWA there.
- Full PNG icon set (currently SVG icons) — Bria-ai power could generate these.
- User Guide + About/Help, README, LICENSE (ask Isaac which license).

---

## Session 4 — 28 Aug 2026 (v1.3.3 — documentation)

### Goal
Finish Splitzy's documentation & delivery per the build standards.

### What we added
- **LICENSE** — MIT (Copyright (c) 2026 Isaac A. Gera). Isaac chose MIT.
- **In-app About/Help** — a "?" icon button in the header, placed between the currency selector
  and the theme toggle. Opens an About dialog with a quick-help list and a link to the full
  user guide. (Matches the existing dialog styling; keyboard/ARIA friendly.)
- **"Powered by Forjé"** — centred note added below the "Works offline…" footer line.
- **`Splitzy-UserGuide.html`** — standalone styled guide (Splitzy tokens, light/dark), covering
  bills, edit/delete, people & tip, round-off, currency, result, summary export, reset/undo,
  theme, install/offline, and the hidden sample loader. Includes a note clarifying Splitzy is an
  even-split tool (not a who-owes-whom settler).
- **`README.md`** — repo-facing: features, running, deployment, sample-data, file structure, tech notes, license.
- **`CHANGELOG.md`** — full history v1.0.0 → v1.3.3 (semver).

### Housekeeping
- Version bumped to **1.3.3** (footer, JS VERSION const, guide, README, changelog).
- SW cache → `splitzy-v1.3.3`; added `Splitzy-UserGuide.html` to cached ASSETS (offline-available).

### Verification
- By inspection: About dialog open/close wired; footer note present; guide/README/changelog cross-reference the right version; cache bumped.
- **Isaac to check (hard-refresh):** About "?" opens the dialog and its "Full user guide" link opens `Splitzy-UserGuide.html`; footer shows "Powered by Forjé"; guide renders in light/dark.

### Status
- Splitzy remains **Built (Splitzy v1.3.3)** — documentation complete. `Ideas.md` version tag can be updated to v1.3.3 on next sync.

### Deferred (future)
- Deploy via Netlify for a real hosted URL.
- Full PNG icon set (currently SVG) — Bria-ai power could generate.
- Separate **group expense settler** app (who-owes-whom + minimised transfers) — agreed as a distinct new build.

---

## Housekeeping — 30 Aug 2026: Folder relocation

Moved the project folder from `Projects/Bill Splitter/` into `Projects/finance-apps/Bill Splitter/`
so it sits alongside WealthOrah under the finance-apps grouping. Pure local filesystem move —
verified the full tree (all files + `icons/` and `prototypes/`) copied before the original was
removed. No `.git` in the folder, so no repo impact; Splitzy is a self-contained PWA with relative
paths, so the app runs unchanged from the new location. No code or version change; still
**Built (Splitzy v1.3.3)**.

---

## Session 5 — 4 Sep 2026 (v1.3.4 — PWA icon gap + offline verification)

### Goal
Close the gaps from a PWA-readiness audit of Splitzy. **Bug Fix** mode.

### Audit findings vs reality (diagnosis first)
The audit summary was partly **stale**. Checked against the actual files before changing anything:
- **"Add SW registration to index.html"** — *already present* (index.html, in the IIFE:
  `if ("serviceWorker" in navigator) { window.addEventListener("load", … register("./sw.js") …) }`).
  Been there since v1.3.0 per this log. **No change needed** — the "Works offline" claim was
  already backed by real registration + precaching.
- **Raster PNG icons (optional / should-fix)** — *genuine gap*. Only SVG icons existed. **Fixed.**
- Because a real asset change shipped (icons), the version + cache bump **is** warranted here
  (unlike a bump for a no-op fix).

### What we did
1. **Generated raster PNG icons** — 192 & 512, standard + maskable (`icons/icon-192.png`,
   `icon-512.png`, `icon-maskable-192.png`, `icon-maskable-512.png`).
   - **Tooling constraint:** pip/PyPI is unreachable on this machine (corporate TLS interception —
     `CERTIFICATE_VERIFY_FAILED`), so Pillow/cairosvg couldn't be installed. Did **not** disable SSL
     verification (work-network security).
   - **Solution:** `icons/generate-icons.py` — a **pure Python standard-library** generator (zlib +
     struct write the PNG; geometry redrawn from the SVG: gradient rounded-rect / full-bleed maskable,
     white receipt with zig-zag bottom, three lines; 3× supersampled for anti-aliasing). No
     dependencies, no network. Kept in the repo like `generate-data.ps1`. Re-run:
     `python icons/generate-icons.py`.
   - All four visually verified against the SVG source — faithful match.
2. **manifest.json** — added the 4 PNGs alongside the 2 SVGs (6 icons total), with explicit
   `sizes`/`type`/`purpose`. Validated as parseable JSON; all six icon files confirmed present.
3. **sw.js** — added the 4 PNGs to `ASSETS` (precached/offline) and bumped `CACHE_NAME` to
   `splitzy-v1.3.4`.
4. **Version bump to 1.3.4** — `VERSION` const, footer, and About-dialog meta in `index.html`
   (no stray 1.3.3 left); `CHANGELOG.md` entry added; `README.md` version + file-structure line updated.

### Verification
- **By inspection / automated:** manifest JSON parses and every icon `src` resolves on disk;
  version string consistent across index.html/README/CHANGELOG; SW asset list matches real files;
  SW registration confirmed present in source.
- **Not run here:** live browser/offline test — the known Windows shell quirk makes an in-agent
  HTTP/browser test unreliable. **Isaac to confirm manually** (steps below).

### Isaac's manual check (serve + offline — validates the "Works offline" claim)
1. Serve over HTTP (not file://):
   `powershell -ExecutionPolicy Bypass -File .\serve.ps1`  → open http://localhost:8091/
2. **Hard-refresh** (Ctrl+Shift+R) so the new `splitzy-v1.3.4` SW installs (or DevTools →
   Application → Service Workers → Unregister, then reload).
3. DevTools → Application → Service Workers: confirm `sw.js` is **activated**.
4. DevTools → Application → Manifest: confirm 6 icons listed, no icon warnings.
5. DevTools → Network → tick **Offline**, then hard-refresh: the app should still load.
6. While still offline, open http://localhost:8091/Splitzy-UserGuide.html — the precached
   guide should load too.
7. (Optional) Install the PWA and confirm the app icon renders crisply.

### Status
- Ships as **v1.3.4**. On Isaac's successful offline check, `Ideas.md` version tag → **Built (Splitzy v1.3.4)**.

### Deferred (unchanged)
- Deploy via Netlify for a real hosted URL (verify installed PWA there).
- Separate group-expense settler app (who-owes-whom).

---

## Session 6 — 4 Sep 2026 (v1.3.4 cont. — Lighthouse accessibility 88 → 100)

### Goal
Lift the Lighthouse **Accessibility** score from **88 to 100** before publishing to GitHub.
Performance / Best Practices / SEO were already 100. **Bug Fix** mode. Folded into v1.3.4
(not yet shipped externally, so no new version bump — this is pre-release polish).

### The three flagged audits (from Isaac's Lighthouse PDF) and fixes
1. **CONTRAST — "Background and foreground colors do not have a sufficient contrast ratio."**
   Root cause: several tokens failed WCAG AA. Measured (before): muted `#64748b` on
   `--surface-2` = 4.34; white on `--brand #0ea5e9` = 2.77; brand-strong `#0284c7` text = 4.10;
   dark theme white on `#38bdf8` = 2.14.
   Fix (tokens): light `--text-muted` → `#556275`, light `--brand-strong` → `#036aa0`,
   dark `--text-muted` → `#a7b6cf`, dark `--brand-strong` → `#38bdf8`; added a new `--on-brand`
   token (`#fff` light / `#0b1220` dark) and pointed all brand-filled *text-bearing* controls
   (Add pill, primary dialog button, inline-edit save, toast Undo) at `--brand-strong` bg +
   `--on-brand` text. Updated all four theme blocks (`:root`, `prefers-color-scheme: dark`, and
   both `html[data-theme=...]` overrides). **Verified by computation**: all 28 text/background
   pairs now pass AA in both themes (lowest 5.48 normal / 5.88 large in light; ≥7.66 in dark).
2. **BEST PRACTICES — "Document does not have a main landmark."**
   Fix: the `.layout` container is now a `<main>` element (closing `</div>` → `</main>`).
3. **ARIA — "Elements with an ARIA [role] that require children to contain a specific [role]
   are missing … required children."**
   Root cause: `#bills` had a permanent `role="list"`, but its child was a non-`listitem`
   `.empty-hint` when empty (and inline-edit rows were also role-less).
   Fix: removed the static `role="list"`; `renderBills()` now sets `role="list"` only when
   bills exist and removes it when empty; the inline-edit row gets `role="listitem"` so every
   direct child of the list is a listitem.

### Verification
- **Contrast:** computed WCAG ratios for every pair in both themes — all pass (script was
  temporary, removed after).
- **Landmark / ARIA:** by inspection of the emitted DOM (one `<main>`; list role present only
  with listitem children).
- **Not re-run here:** the live Lighthouse pass — Isaac to re-run in Chrome DevTools to confirm
  Accessibility = 100. (Report was captured in dark theme; fixes cover both themes.)
- No behavioural/logic changes — purely tokens + semantics.

### Note on the Lighthouse "Performance" diagnostics
The report also *suggested* (not scored, Performance was already 100): minify CSS/JS, optimise
DOM size. Deliberately **not** doing these — Splitzy is intentionally a single no-build file;
minifying would add a build step against the app's design. Noted, not actioned.

### Status
- Still **v1.3.4**. Accessibility fixes complete and verified by computation; awaiting Isaac's
  live Lighthouse re-run, then on to publishing to GitHub.

---

## Session 7 — 4 Sep 2026 (v1.3.4 cont. — mobile/tablet tap-target polish + git init)

### Goal
Before publishing to GitHub, tighten Splitzy for mobile/tablet touch use, and prepare the
local git repo. Still folded into v1.3.4 (pre-release polish, no new version bump).

### Responsive review (findings)
Read the CSS: the app was already responsive by design — correct viewport meta with
`viewport-fit=cover`, `env(safe-area-inset-*)` padding for notched phones, two-card layout
collapsing to one column at ≤720px, a ≤420px breakpoint simplifying the inline-edit row, and
dialogs capped at `max-width: 90vw`. Main gap: some tap targets were below the 44px touch
minimum (edit/delete icon buttons 26px; inline-edit save/cancel 28px).

### Change (CSS-only, touch-scoped)
- Added `@media (pointer: coarse)` rules: icon-btn → 44px min hit area, inline-edit minis &
  steppers → 40px, theme/about → 42px, add-pill padding bumped, dialog-close/undo min-height 40px,
  and `.bl-actions` gap widened to 8px. Icon glyphs and the desktop (pointer: fine) layout are
  unchanged — only the clickable area grows on touch.
- Added `touch-action: manipulation` to interactive controls (removes ~300ms tap delay, blocks
  double-tap zoom on buttons).
- No behavioural/JS changes; Lighthouse desktop scores unaffected (touch rules don't apply to the
  desktop emulation).

### Git (local, done from Kiro)
- `git init -b main`; added `.gitignore` (OS/editor cruft + `_*` scratch files); staged all 20
  app files; first commit **820c6d9** "Initial commit: Splitzy v1.3.4 (bill splitter PWA)".
- `gh` (GitHub CLI) could not be installed — winget source is broken on this corporate network
  (`0x8a15000f`), and the MSI needs admin. **Plan:** publish via **GitHub Desktop** (bundles git,
  handles auth) → then enable GitHub Pages (Settings → Pages → main / root).

### Verification
- Tap-target CSS reviewed by inspection; style block confirmed balanced. Live device check is
  Isaac's (checklist provided). Contrast/a11y from Session 6 unchanged.

### Pending
- Isaac: publish via GitHub Desktop (personal account, repo name TBD, public for Pages), enable
  Pages, then confirm on the live HTTPS URL + a real phone.
- After live confirmation: add a "Live demo" link to README, sync `Ideas.md` if the version tag
  needs it, and note the final URL here.

---

## Session 8 — 4 Sep 2026 (Published to GitHub + GitHub Pages)

### What happened
- Isaac published the repo via **GitHub Desktop** to his personal account.
  - Repo: **`Bill-Splitter`** (public) — https://github.com/isaacgera/Bill-Splitter
  - Live (GitHub Pages): **https://isaacgera.github.io/Bill-Splitter/**
- GitHub Pages enabled from `main` / root.

### Live verification (done from Kiro via web fetch)
- `/` → serves the real Splitzy app HTML (header, Bills, Split Settings, Result, breakdown all present).
- `/manifest.json` → loads, all 6 icons listed (2 SVG + 4 PNG).
- `/sw.js` → served with `application/javascript` content-type (reachable; not a 404).
- Relative paths resolve correctly under the `/Bill-Splitter/` subpath — no broken links from the subdirectory.

### Docs synced
- `README.md`: added **Live demo** link at top; Deployment section updated with the real Pages URL + setup steps.
- (Version stays **1.3.4** — publishing isn't a code change.)

### Still to do (Isaac)
- Run the **mobile checklist** on the live URL from a real phone (install, offline via airplane mode,
  tap targets, exports, light/dark). Confirm the Chrome `mobile-web-app-capable` warning is gone.
- These README doc edits are committed locally — **sync once more in GitHub Desktop** to push them.

### Status
- **Built (Splitzy v1.3.4)** — now publicly live as an installable PWA on GitHub Pages.

---

## Session 9 — 4 Sep 2026 (v1.3.5 — mobile summary export fix)

### Problem (reported by Isaac, testing the live PWA on his phone)
1. **Image** export: tapping Summary → Image gave no indication where (or whether) the image saved.
2. **PDF** export: opened a new tab showing the summary with **no way back** to the app.

### Root cause
- **Image**: used a programmatic `<a download>` click. Mobile browsers (esp. iOS Safari) largely
  ignore the `download` attribute, so nothing visibly saved — yet the toast still said "saved".
- **PDF**: `window.open("", "_blank")` + `print()`. On mobile `print()` frequently doesn't fire,
  leaving the user stranded in an orphan tab with no back navigation.

### Fix (export logic reworked; no UI restructure)
- Added helpers: `canShareFiles(file)` (feature-detects `navigator.canShare({files:[...]})`),
  `renderSummaryCanvas()` (extracted the canvas drawing), `downloadBlob()`, and `summaryPrintHTML()`.
- **Image**: canvas → `toBlob` → if file-share supported, open the **OS share sheet** via
  `navigator.share({files})`; else fall back to a Blob **download**. Toast now reflects the real
  outcome (shared vs downloaded); `AbortError` (user cancelled the sheet) is silent.
- **PDF**: on mobile (file-share available) shares the summary **as a PNG** (phones print-to-PDF
  poorly, and this removes the orphan-tab dead end); on desktop prints via a **hidden same-page
  iframe** (auto-cleaned via `onafterprint` / matchMedia, with a safety-net timeout) — **no new
  tab**, so the app is never left behind.
- Web Share API pattern verified against MDN/web.dev; file-share support is good on Android Chrome
  and modern iOS Safari, with graceful fallback where it isn't. (Content rephrased for compliance.)

### Release chores (per build standards — this is a shipped app, real behaviour change)
- Version → **1.3.5** across index.html (VERSION const, footer, About), user guide (pill + footer),
  README. SW cache → `splitzy-v1.3.5`. CHANGELOG v1.3.5 entry added.

### Verification
- **By inspection:** handlers re-read and balanced; exactly one each of `</script></style></head></body>`
  in correct positions (no embedded closing tags — kept the fragment-split technique). A naive
  brace-balance script flagged false positives on JS regex literals **identically** for the current
  and the previously-shipped file, so no new imbalance was introduced.
- **Not run here:** live device test. **Isaac to check on phone + desktop** (checklist provided):
  mobile Summary → Image and → PDF should both open the **share sheet** (save to Photos/Files etc.),
  and never strand you in a tab; desktop Image still downloads a PNG, desktop PDF opens the print
  dialog **without** a new tab and returns cleanly.

### Status
- **v1.3.5** ready locally (4 commits from v1.3.4 already pending push + this). Needs Isaac's device
  test, then push via GitHub Desktop; Pages will update automatically. `Ideas.md` tag → v1.3.5 after confirm.

---

## Session 10 — 4 Sep 2026 (v1.3.5 refinement — export simplified to two options)

### Context
After the Session 9 mobile-export fix, Isaac tested on his phone: the **PDF** button now produced
a **.png** (the mobile fallback), which is misleading — a PDF button shouldn't hand back an image.
Discussed options; Isaac chose to **drop PDF entirely** and go to **two buttons everywhere**.

### Final design (v1.3.5)
- Export dialog now has exactly **two options on every device**:
  - **Image / Share** — one adaptive button. Desktop: label **Image**, downloads a PNG.
    Touch (`@media (pointer: coarse)`): label **Share**, opens the OS share sheet with the PNG.
    Label + icon swap via CSS; the action (render summary → PNG) is identical underneath.
  - **Text** — copies a plain-text summary to the clipboard.
- **PDF removed completely**: the `#expPdf` button, its click handler, and the `summaryPrintHTML()`
  helper + hidden-iframe print code are all gone. Desktop users who want a PDF use the browser's
  own Print → Save as PDF (noted in the user guide).
- `.dialog-options` grid is now 2 columns everywhere (was 3).

### Why
Honest UI over clever UI: a "PDF" button that yields a PNG on mobile is a lie. Most phone users
want to share/save the summary anyway. Removing PDF also deletes the most fragile export code
(the print string that caused the v1.2.0/v1.3.1 button-breakage bugs historically) — net simpler
and safer, and keeps Splitzy library-free.

### Docs synced
- CHANGELOG v1.3.5 rewritten to describe the two-option design (Changed + Fixed).
- User guide: summary section + ToC updated (Image/Share/Text; PDF note points to browser print).
- README (feature line + tech note) and in-app About dialog updated.
- Version stays **1.3.5** (not pushed live yet); SW cache already `splitzy-v1.3.5`.

### Verification
- By inspection: `expPdf`/`summaryPrintHTML` fully removed (grep clean — no dangling `$("expPdf")`
  that would throw); `expImg` + `expTxt` handlers intact; exactly one each of the structural closing
  tags in the right places (the risky print HTML string is gone).
- **Isaac to device-test** (checklist provided): dialog shows two buttons; desktop Image downloads
  a PNG; mobile Share opens the share sheet; Text copies; no PDF anywhere; no orphan tab.

### Status
- **v1.3.5** ready locally. After Isaac's device test → push via GitHub Desktop; then Ideas.md tag → v1.3.5.
