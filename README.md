# Erde, Dverghamar & Merenval

An accessible guide to the landscapes, peoples, languages, ordinary magic and beliefs of Erde, Dverghamar, Merenval and its living companion.

The current edition was synchronized from the [Public — Cultural Knowledge folder](https://drive.google.com/drive/folders/126BrWsD3GZ-Qg2oGTjxX3lN_Tp642AXt) on 18 September 2026. It contains **36 subject articles, a collection index, thirteen atlas subjects, 562 dictionary entries and 97 translated examples**. The atlas currently supplies text guides; older map artwork is outside this edition. The Stavmark writing chart remains consistent with the current writing guide.

## Run locally

Use Node 24 or newer.

```sh
npm ci
npm run build
npm run preview
```

Open <http://localhost:4173/test-fantasy-world/>. The local server also supports the root path. Generated files are in `dist/` and are not committed.

## Current sources and synchronization

The live public Drive collection governs publication eligibility. `content/public/` contains its unchanged Markdown and data, plus a readable text export of the native index. `content/public-sync.json` maps all 44 files to source IDs, modification times, byte lengths and SHA-256 checksums. The import does not introduce additional authorial lore.

The build resolves links between known public Drive files to local articles and downloads. Article H1 headings govern displayed titles when a catalog label lags a document revision. The detailed Gnome article has older catalog metadata; its current title and a content-based summary are used for display, as recorded in the sync manifest. Downloaded source catalogs retain the original wording.

- Categories: `worlds`, `peoples`, `cosmology`, `language`, `maps` and `reference`.
- Keep article IDs stable. New articles require catalog entries; every category needs navigation and a category page.
- Maintain the exact six source datasets/indexes. TSVs live in `content/public/data/`; JSON files live directly in `content/public/`. Tests compare dictionary meanings, forms and row counts across formats.
- `content/dictionary-anchors.json` preserves old numeric bookmarks for surviving words. Deterministic lexical anchors are used for new links. Removed entries do not redirect to a different word.
- `scripts/public-edition.mjs` defines link resolution, related reading and the explicit asset allowlist. New illustrations require review before inclusion.
- Public knowledge is bounded natural history, ordinary practitioner experience and attributed cultural accounts. Earlier public inclusion does not make technical or authorial material eligible today.
- Plans and results for this update are recorded in [the synchronization record](docs/PUBLIC-SYNC-2026-09-18.md).

## Historical research

Files directly in `content/` other than the current sync and anchor manifests, older `public/data/`, map artwork in `assets/maps/`, and prior scientific/editorial records under `docs/` are retained research history. They are not current public source authority and are not copied into the website. Their credits and evidence distinctions remain intact. The older Level 3 register is a historical research record; import coverage does not certify a fresh real-world source audit.

This repository is public. An editorial directory boundary does not restrict access, and this synchronization does not erase previously committed material from Git history. See [source notes](content/SOURCES.md) for the historical record and current boundary.

## Verify

```sh
npm test
npx playwright install --with-deps chromium
npm run test:e2e
```

Checks cover exact source checksums and folder coverage, local links and fragments, navigation, search destinations, publication assets, atlas anchors, dictionary identity and downloads. Browser tests cover search, keyboard access, no-JavaScript reading, themes, storage failure, narrow layouts and automated WCAG A/AA checks. Automated checks do not constitute a full manual accessibility audit.

## Deployment

The existing GitHub Actions workflow builds, tests and deploys `dist/` on pushes to `main`. Pull requests run checks without deployment. Pages must use **GitHub Actions** as its source. Historical geography reconstruction checks remain in the workflow independently of the public edition.

The project URL is <https://andeleidun.github.io/test-fantasy-world/>. A successful workflow reports its deployment URL. No external runtime service, account, analytics, font or API is required by the reader.

## Rights

All original project IP remains the author’s. Public documentation grants no license or right to reuse this work. Existing third-party credits remain with their research records; no blanket open-source license is assigned.
