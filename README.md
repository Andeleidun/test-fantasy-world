# Erde & Dverghamar

A minimal, accessible worldbuilding guide for Erde and Dverghamar. It contains geography, ecology, peoples, language, maps and relevant cosmology. Plot, character dossiers and private author notes are outside its scope.

The site has 20 articles and reference pages, 13 existing atlas sheets, the Stavmark writing chart, a 571-record Korvar dictionary and 98 translated language examples. The home page and topic indexes provide a shorter route through the longer decision ledgers.

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

- Edit article Markdown in `content/`. Register new articles in `content/catalog.json` with a unique ID, title, category, description, kind and Markdown filename.
- Categories are `worlds`, `peoples`, `cosmology`, `language` and `maps`.
- Edit `content/lexicon.json` for dictionary records and `content/maps.json` for atlas captions and text explanations.
- Keep the downloadable TSV reference data in `public/data/` consistent with vocabulary changes.
- Place public assets in `assets/` or `public/`. Only approved public material belongs here.
- Source provenance and publication boundaries are in `content/SOURCES.md`. This is a publication snapshot, not an automatic Drive sync. Explicit current decisions take precedence over older working proposals.

Raw HTML in Markdown is disabled. The build generates complete HTML pages, heading anchors, a local search index and relative links that work beneath the repository prefix. No framework, client-side router, remote fonts, analytics, external API or runtime account is required.

## Verify

```sh
npm test
npx playwright install --with-deps chromium
npm run test:e2e
```

Build checks cover internal links, section fragments, duplicate IDs, search destinations and the worldbuilding-only scope. Browser checks cover keyboard skip navigation, search and recovery from a failed request, dictionary filtering, no-JavaScript reading, horizontal overflow, and automated WCAG A/AA checks at 1440, 390 and 320 pixels. Automated checks do not replace a full manual accessibility audit or assistive-technology testing.

## Implementation

`scripts/build.mjs` renders Markdown at build time using Markdown-it. `assets/app.js` progressively enhances search and dictionary filtering. `assets/styles.css` contains the responsive layout, high-contrast focus styles, reduced-motion treatment and print styles. All articles and dictionary rows remain available with JavaScript disabled. Map captions explain the principal relationships and link to full-size SVG sheets.

Worldbuilding content and original illustrations retain their owner’s rights; no blanket open-source license is assigned. Third-party land geometry is credited in `content/SOURCES.md`.
