# Erde, Dverghamar & Merenval

A guide to the landscapes, peoples, languages, ordinary magic and beliefs of Erde, Dverghamar, Merenval and its living companion.

The reader brings the current public collection into five complete, illustrated guides. Each contains its related histories and references, with links to chapters and individual sections.

| Guide | Read online | Read in the repository |
| --- | --- | --- |
| Erde | [World guide](https://andeleidun.github.io/test-fantasy-world/erde.html) | [Erde](guides/erde.md) |
| Dverghamar | [World guide](https://andeleidun.github.io/test-fantasy-world/dverghamar.html) | [Dverghamar](guides/dverghamar.md) |
| Merenval and its companion | [World guide](https://andeleidun.github.io/test-fantasy-world/merenval.html) | [Merenval](guides/merenval.md) |
| Magic and belief | [World guide](https://andeleidun.github.io/test-fantasy-world/magic.html) | [Magic and belief](guides/magic.md) |
| Korvar, including the dictionary | [World guide](https://andeleidun.github.io/test-fantasy-world/korvar.html) | [Korvar](guides/korvar.md) |

The edition retains 36 source subjects, all 562 dictionary records and 97 translated examples. Seven vector maps cover the thirteen existing atlas subjects and Merenval's paired landscapes. Six illustrations and the Stavmark chart appear beside their subjects and are embedded in the corresponding source documents. The full source collection was reviewed and synchronized on 20 September 2026; Dorrenath's two public sources and illustration received a targeted revision on 23 September 2026.

## Run locally

Use Node 24 or newer.

```sh
npm ci
npm run build
npm run preview
```

Open <http://localhost:4173/test-fantasy-world/>. The local server also supports the root path. The site build is written to `dist/`. The five complete Markdown guides are also generated into `guides/` and committed for repository readers.

## Current sources and synchronization

The public Drive collection supplies the site's source text. Before synchronization, check it against the author's latest accepted decisions: a recent file timestamp alone does not establish current canon. Update the public sources where eligible decisions supersede them. `content/public/` then preserves those source bytes, plus a readable text export of the native index. `content/public-sync.json` maps all 44 files to source IDs, modification times, byte lengths and SHA-256 checksums.

`content/reader/guides.json` defines the five guides and their chapter order. `scripts/reader-edition.mjs` maps source sections and old URLs into this structure; `scripts/build.mjs` renders the website and the complete Markdown guides. Every source has a recorded destination in `content/reader/coverage.json`.

- Assign new public subjects to a guide in the reader configuration. Keep the source article ID stable for old links.
- Record editorial replacements and merged summaries in `content/reader/edits.json`, with a destination and reason. The source snapshot remains unchanged by reader composition.
- `content/reader/figures.json` supplies image descriptions, captions, placements and atlas-code coverage. Only its reviewed images and the reader's application assets are deployed. `scripts/draw-reader-maps.py` regenerates the seven vector plates.
- Illustration prompts and generation method are recorded in `content/reader/illustration-prompts.json`. The web images are stored in `assets/illustrations/`.
- After editing figure metadata, run `node scripts/sync-source-figures.mjs`, review the resulting public Markdown, and synchronize those source files. The reader recognizes these embedded blocks and renders each figure once at its configured location.
- Maintain the exact six source datasets/indexes. TSVs live in `content/public/data/`; JSON files live directly in `content/public/`.
- `content/dictionary-anchors.json` preserves old numeric bookmarks for surviving words. Stable lexical anchors identify dictionary records. Removed entries never redirect to a different word.
- Old article routes provide fragment-aware forwarding and ordinary links for readers without JavaScript. Search indexes the composed text and points directly into the five guides.
- Apply the Humanizer editorial rules to new reader prose and captions. Preserve naturalist voices, grammatical examples and genuine uncertainty.

The [Dorrenath regional update](docs/DORRENATH-REGION-UPDATE-2026-09-23.md) records the latest targeted correction. The earlier [canon review and artwork plan](docs/CANON-REVIEW-2026-09-20.md), [synchronization record](docs/PUBLIC-SYNC-2026-09-18.md), [prose review](docs/PROSE-REVIEW-2026-09-20.md), and [consolidation record](docs/GUIDE-CONSOLIDATION-2026-09-20.md) retain their dated results.

## Historical research

Twenty-seven obsolete articles directly in `content/` now point to the current guides and to their previous versions in Git history, where their source credits remain. The unused article catalog agrees with the current public catalog. Original lexical ordering, older map data and artwork, and prior scientific/editorial records remain dated research history used by old bookmarks or research scripts. They are not copied into the website. The older Level 3 register is a historical research record; import coverage does not certify a fresh real-world source audit.

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
