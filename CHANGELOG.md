# Changelog

All notable changes to Splitzy. Follows semantic versioning (major.minor.patch).
The PWA cache name is bumped on each release so updates reach installed apps.

## [1.3.5] — 4 Sep 2026
### Changed
- **Summary export simplified to two options everywhere: Image/Share + Text.** The **PDF**
  export was removed — on mobile it couldn't produce a real PDF (it fell back to a PNG, which
  was misleading), and on desktop the browser's own Print → *Save as PDF* covers that need.
  - On **desktop**, the first button is **Image** and downloads a PNG.
  - On **touch devices**, it becomes **Share** and opens the native OS share sheet
    (`navigator.share` with the PNG file) — save to Photos/Files, message it, etc.
  The label and icon adapt to the device (`@media (pointer: coarse)`); the underlying action is
  the same summary rendered to a PNG.
- PWA cache bumped to `splitzy-v1.3.5`.
### Fixed
- **Mobile summary export used to fail silently.** The old **Image** used an `<a download>` click
  that mobile browsers largely ignore (nothing saved), and the old **PDF** opened a new tab and
  called `print()`, which on mobile often did nothing and stranded the user with no way back.
  Both are resolved by the share-sheet approach above.
- Success toasts are now honest — they say **shared** / **downloaded** to match what actually happened.

## [1.3.4] — 4 Sep 2026
### Added
- **Raster PNG icons** (192 & 512, standard + maskable) alongside the existing SVGs, for
  wider install compatibility on platforms that don't rasterize SVG app icons. Generated
  from the SVG geometry by a dependency-free `icons/generate-icons.py` (Python standard
  library only). Referenced in `manifest.json` and precached by the service worker.
### Fixed
- Closes the PWA-readiness icon gap so the manifest's install/offline promise holds on more
  platforms. (Service-worker registration was already present since v1.3.0 — verified, no change.)
- **Accessibility (Lighthouse a11y 88 → 100 target):**
  - **Colour contrast** — darkened muted text and the brand-strong colour, and introduced an
    `--on-brand` token so all text/background pairs meet WCAG AA (4.5:1; 3:1 for the large
    result figure) in **both** light and dark themes. Verified every pair by computation.
  - **Landmark** — wrapped the app content in a `<main>` element (was missing a main landmark).
  - **ARIA list** — the bills container now only carries `role="list"` when it actually holds
    `listitem` children (the empty-state hint and inline-edit rows no longer violate the
    list/listitem parent-child requirement).
- **PWA meta** — added the standard `<meta name="mobile-web-app-capable" content="yes">`
  alongside the Apple-specific one (which stays for older iOS Safari). Clears a Chrome console
  deprecation warning; no behaviour change.
- **Touch usability** — on touch devices (`@media (pointer: coarse)`), small tap targets are
  enlarged to a comfortable minimum (edit/delete 44px, save/cancel & steppers 40px, theme/about
  42px) without changing the icon glyphs or the desktop layout; wider spacing between the
  per-bill edit/delete buttons; and `touch-action: manipulation` on controls to remove the tap
  delay and prevent double-tap zoom.
### Changed
- PWA cache bumped to `splitzy-v1.3.4` so the new icons reach installed apps.

## [1.3.3] — 28 Aug 2026
### Added
- In-app **About / Help** dialog (icon between the currency selector and theme toggle).
- **"Powered by Forjé"** note in the footer.
- **MIT LICENSE**, standalone **User Guide**, **README**, and this changelog.

## [1.3.2] — 28 Aug 2026
### Added
- Hidden **sample-data loader** (no visible UI): drag-and-drop a JSON file, `Ctrl+Shift+L`
  file picker, or `?sample=1` URL auto-load. Validated input, reversible via undo.
- `generate-data.ps1` + `sample-data.json` (6 bills, group of 5, INR).

## [1.3.1] — 28 Aug 2026
### Fixed
- Buttons not responding: an embedded closing `</style>`/`</head>`/`</body>`/`</html>` in the
  PDF export string broke script parsing. Tags are now built from fragments so none appear literally.

## [1.3.0] — 28 Aug 2026
### Changed
- Major UI redesign to a two-card layout ("Option C"): Bills (left) and Result (right),
  equal width/height, responsive.
- Bills shown as compact one-liners with **inline edit** and delete.
- Adding a bill now uses a small **dialog** opened from a top-right "+ Add" pill.
- **People** and **Tip** are directly editable fields with &minus;/+ steppers (tip default 5%, 1% steps).
- **Round-Off** is a toggle switch beside the centred result value.
- **Reset** and **Summary** are compact, centred pill buttons.
### Added
- **Summary** dialog with real **Image (PNG)**, **PDF (print)**, and **Text (clipboard)** export.
- **5-second Undo** on delete and reset.
- Currency selector default changed to **₹ INR** (persistent).
- Full tooltips and ARIA across controls.

## [1.2.1] — 28 Aug 2026
### Fixed
- Hotfix for an embedded `<script>` tag in the PDF export that stopped all JavaScript running.

## [1.2.0] — 28 Aug 2026
### Added
- Three-card side-by-side layout.
- Per-bill **dates** (defaulting to today).
- **Save as PNG / PDF** export (library-free).
### Fixed
- Currency toggle no longer wipes entered amounts (symbols update in place).
- Amounts can no longer be negative.

## [1.1.0] — 28 Aug 2026
### Changed
- Renamed **SplitEasy → Splitzy**.
- Two-column layout.
### Added
- Currency selector (£/$/₹/€ or none).
- **Multiple bills** with a consolidated split.
### Fixed
- Round-up-per-person toggle now works reliably.

## [1.0.0] — 28 Aug 2026
### Added
- Initial build (as "SplitEasy"): single bill, people stepper, tip presets, round-up,
  live per-person / tip / total, copy summary. Installable PWA, light/dark theme,
  offline caching, local-first.
