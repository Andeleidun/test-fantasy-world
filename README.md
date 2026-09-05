# Erde & Dverghamar

A minimal, accessible worldbuilding guide for Erde and Dverghamar. It contains geography, ecology, peoples, language, maps and relevant cosmology. Plot, character dossiers and private author notes are outside its scope.

The site has 21 public articles and reference pages, 13 existing atlas sheets, the Stavmark writing chart, a 571-record Korvar dictionary and 98 translated language examples. The public edition presents the setting in subject-based articles. Original working documents retain their detailed decision history separately. A light/dark toggle follows the device preference initially and remembers a reader’s choice when browser storage is available.

## Run locally

Use Node 24 or newer.

```sh
npm ci
npm run build
npm run preview
```

Open <http://localhost:4173/test-fantasy-world/>. The local server also supports the root path. Generated files are in `dist/` and are not committed.

## Deploy with GitHub Actions

In repository **Settings → Pages → Build and deployment → Source**, select **GitHub Actions**. The checked-in workflow is `.github/workflows/pages.yml`.

Every push to `main` builds, checks internal links, runs browser and accessibility checks, uploads only `dist/`, then deploys to the `github-pages` environment. Pull requests run the same checks without deploying. **Actions → Build and deploy world guide → Run workflow** can publish the current main branch after enabling Pages or retry a deployment.

The expected project URL is <https://andeleidun.github.io/test-fantasy-world/>. A successful deployment reports its actual URL in the workflow environment. If Pages has not been enabled yet, the build can succeed while the deployment step fails; select GitHub Actions as the source and rerun the workflow.

The workflow follows [GitHub’s custom Pages workflow guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). Actions are pinned to commit SHAs. Build permissions are read-only; Pages and OIDC write permissions are limited to the deployment job. No deployment secrets or third-party hosting account are required.

## Edit the lore

- Edit reader-facing Markdown in `content/public/`. Register articles in `content/public/catalog.json` with a unique ID, title, category, description, kind and Markdown filename. Each document has a title and uses relative `.md` article links, which the build translates to website routes.
- Categories are `worlds`, `peoples`, `cosmology`, `language` and `maps`. Keep existing IDs stable to preserve links.
- Edit `content/public/lexicon.json` for public vocabulary and `content/public/maps.json` for map captions. Preserve dictionary row order because row anchors are stable links.
- Public downloads live in `content/public/data/`. The build generates the Common dictionary from the public lexicon; update its source TSV copy and regional meanings when editing vocabulary. Tests check that the downloads match.
- Erde’s public identity and proposed names are documented in `docs/ERDE-NAMING-DIRECTION.md`. Earth correspondence and construction history stay authorial; proper-name proposals are selected before public use.
- `python scripts/editorial/prepare-erde-atlas.py` prepares the public Erde atlas variants from the retained original sheets. Legacy map URLs receive the public artwork during the build.
- Shared illustrations and application files live in `assets/`. The build copies only approved public article/data inputs and these assets into `dist/`.
- Original working Markdown, catalogs and data remain in `content/` and `public/data/`. They are not website inputs. This is an editorial split within a public repository, not an access-control boundary.
- `content/public/README.md` maps articles to working sources. `content/SOURCES.md` records import provenance. Changes to Drive documents do not automatically update this publication.
- The implementation plan and review record are in `docs/PUBLIC-EDITION-PLAN.md` and `docs/PUBLIC-EDITION-REVIEW.md`.

Raw HTML in Markdown is disabled. The build generates complete HTML pages, heading anchors, a local search index and relative links that work beneath the repository prefix. No framework, client-side router, remote fonts, analytics, external API or runtime account is required.

## Verify

```sh
npm test
npx playwright install --with-deps chromium
npm run test:e2e
```

Build checks cover internal links, section fragments, duplicate IDs, search destinations and the worldbuilding-only scope. Browser checks cover keyboard skip navigation, search and recovery from a failed request, dictionary filtering, no-JavaScript reading, horizontal overflow, theme persistence, system preferences, blocked storage, print appearance, search races, pagination, and automated WCAG A/AA checks in light and dark themes at 1440, 390 and 320 pixels. Automated checks do not replace a full manual accessibility audit or assistive-technology testing.

## Implementation

`scripts/build.mjs` renders Markdown at build time using Markdown-it. `assets/theme.js` applies saved appearance before styling; `assets/app.js` enhances the theme control, search and dictionary filtering. `assets/styles.css` contains the responsive layout, high-contrast focus styles, reduced-motion treatment and print styles. All articles and dictionary rows remain available with JavaScript disabled. Map captions explain the principal relationships and link to full-size SVG sheets.

Worldbuilding content and original illustrations retain their owner’s rights; no blanket open-source license is assigned. Third-party land geometry is credited in `content/SOURCES.md`.
