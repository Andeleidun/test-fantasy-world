# Public documentation synchronization: 18 September 2026

## Plan established before implementation

Baseline: `e4c2cca396b9de75f5272bb4ce0b9ef9daa51695` on `main`.
Authority: [Public — Cultural Knowledge](https://drive.google.com/drive/folders/126BrWsD3GZ-Qg2oGTjxX3lN_Tp642AXt), inventoried live on 18 September 2026.

The folder contains 44 files: 37 Markdown documents (36 subject articles and the collection README), six datasets/indexes, and one native document index. All 43 stored text files were retrieved completely and checked against Drive byte sizes. The native index is a readable text export; its native storage size is not a text-export size. The source snapshot supersedes the earlier Library summary and the 14 September repository publication.

## Diagnosis and constraints

- Current public knowledge covers observable life, bounded natural history, attributed traditions and ordinary practitioner experience. Previously public technical models are no longer eligible for publication merely because they were once included.
- The old build requires SVG stems; the new atlas index contains thirteen text subjects and no approved artwork. Copying the entire assets directory would continue publishing excluded sheets even if no page linked them.
- The new catalog adds a `reference` category and the collection README. Without a category page, its articles would have broken return links and incomplete navigation.
- The language edition has 562 lexical records and 97 examples. Removing entries shifts row-number links; legacy dictionary anchors must continue identifying the same surviving entry.
- The detailed Gnome article was revised after its catalog title. Its H1 is the display authority, and the display summary follows the current article; the source catalog remains an exact snapshot.
- Existing working documents, scientific trials and provenance registers are historical research, not the current public edition. Preserve them and their credits without presenting them as current source authority. This task does not rewrite repository history or conduct a new scientific/provenance audit.

## Ordered implementation and acceptance gates

1. Import every public Markdown/data file into `content/public/`; place TSVs in `data/` and the native text index in `PUBLIC-INDEX.txt`. Record source IDs, URLs, modification times, byte lengths and SHA-256 hashes in `content/public-sync.json`. Keep source wording and data byte-for-byte; localize links at build time.
2. Update the renderer, navigation, search categories, home/about copy and downloads to the current public boundary. Render atlas text with stable E1–E5/D1–D8 anchors. Copy an explicit reviewed asset list only. Keep the existing Stavmark chart only after checking it against the current writing guide. Add related-reading navigation without altering source prose.
3. Keep all existing article routes. Preserve old numeric dictionary anchors for surviving records and supply deterministic lexical anchors. Do not redirect an omitted word to a different word. Expose all six public data/index downloads.
4. Update source documentation and distinguish prior editorial/research records from the current publication. Retain Level 3 research history without claiming that an import checksum verifies its real-world evidence.
5. Replace obsolete assertions with source parity, coverage, category, link, anchor, data-integrity and publication-boundary checks. Run build/unit tests, browser interactions, no-JavaScript reading and the existing responsive/light/dark accessibility matrix. Inspect representative renders. Fix concrete failures and repeat the affected checks.
6. Recheck live source metadata and repository HEAD for concurrent changes. Push the reviewed commit without force, use the existing GitHub Pages workflow, and inspect its result. Report an incomplete deployment separately from a successful repository update.

## Coverage and publication boundaries

The machine-readable source map covers every live folder file. The website consumes only `content/public/`, `content/public-sync.json` for link resolution, the dictionary anchor map, and explicitly reviewed reader assets. Historical source documents, geographic trials, raw older language data, provenance internals and unrevised atlas sheets are excluded from `dist/`.

Current source documents may legitimately describe observable Gnome cultivation and spiritual practices. Their presence does not authorize importing additional hidden mechanisms from authorial research. No new lore, named mythology, planetary model or reconstruction is selected by this sync.

## Validation results

- Imported all 44 source files. All 43 stored Markdown/data files matched their reported Drive byte sizes; the native index is explicitly labeled a text export. SHA-256 checks cover every imported file.
- Built 37 catalog pages (36 subject articles and the collection index), six category pages, thirteen text atlas subjects and 562 dictionary records. All six source datasets/indexes and the native index are downloadable.
- Preserved all prior article routes and numeric dictionary anchors for surviving entries. Omitted entries cannot point to a different word. E1–E5 and D1–D8 atlas fragments resolve to the current text.
- Confirmed every catalog article is reachable from its category and search. Known public Drive links resolve locally. The newer Gnome H1 and a current content summary replace stale catalog metadata only in display.
- Confirmed the deployment contains exactly the five reviewed reader assets; no older atlas SVG, technical source, provenance register or research output is copied into `dist/`.
- `npm test`: all nine tests passed, covering complete source parity, links/fragments, publication boundaries, catalog coverage, data consistency, dictionary identity and retained substantive distinctions.
- Browser suite: all thirteen tests passed. The six light/dark and width combinations (1440, 390, 320 px) checked fifteen routes each for overflow and automated WCAG A/AA violations. Search, retries, keyboard navigation, no-JavaScript reading, themes, storage failure, pagination, new references and atlas links also passed.
- Inspected desktop Gnome and mobile atlas renders. Text, navigation and table-of-contents controls are readable and aligned. No layout change was needed.
- Local test environment: the standard Playwright Chromium download timed out. A temporary Chromium 153.0.8010.0 package with system fonts ran the suite; its package, launch configuration and screenshots are outside version control. Project dependencies and the standard CI browser configuration are unchanged. A failed initial fallback run was traced to missing font configuration, then rerun successfully with system fonts.
- Fresh public-folder inventory still contained the same 44 IDs and modification times. The remote branch remained at the planned baseline before publication.
- `git diff --check` passed. Public snapshot paths disable Git line-ending normalization so checksums survive checkout; source-provided whitespace remains intact.

## Remaining limits

The source catalog and native index retain the older Gnome label because imports are exact. The reader displays the current article title and summary. Source parity verifies the import, not scientific truth or a new Level 3 research audit. Existing research and past Git history remain publicly accessible as historical material. The live atlas has text guides until revised artwork is supplied.

The existing GitHub Actions workflow is the final deployment gate. Its result and the deployed commit can be checked in the repository Actions history.
