# Public edition implementation plan

## Purpose and boundaries

Publish a welcoming, factual guide to Erde and Dverghamar, retaining the working documents as editorial sources. Preserve established names, substantive rules, meaningful uncertainty, existing page routes, and the distinction between worldbuilding and story. The repository is public; the working/public split is an editorial boundary, not an access control.

## Diagnosis before implementation

1. **Working documents appear as reader articles.** The build reads the internal catalog directly. Decision numbers, superseded alternatives, author instructions, and revision commentary obscure the current setting. Create `content/public/` with independently edited articles and a source mapping; keep internal files intact. Retain substantial reference detail and link related articles.
2. **Secondary publication paths can retain draft language.** Search, dictionary notes, downloads, map captions, and template text also need review. Read all publication data from the public folder and generate downloads from that edition. Do not silently alter established vocabulary or invent missing geography.
3. **Presentation uses promotional language.** Replace slogans and vague navigation with descriptive headings, introductions, and link labels. Keep comfortable typography and a restrained visual identity.
4. **Colors assume a light background.** Introduce semantic theme tokens, system preference, an accessible persistent toggle, storage-failure handling, no-JavaScript defaults, and a light print layout. Preserve legible map artwork.
5. **Regression risks span content and interaction.** Check source isolation, links and anchors, known canon distinctions, dictionary consistency, keyboard controls, search races, responsive tables and navigation, both themes, and deployment under the repository path.

## Ordered slices and acceptance gates

### 1. Public documents

Write concise world/people introductions and substantial subject-based histories, cosmology, biology, and language references. Preserve the grammar and translated examples while editing the surrounding teaching prose. Map each public article to its source. Review coverage and claims against the latest source decisions before accepting the slice.

### 2. Reader and publication pipeline

Switch article, dictionary, map-caption, search and download inputs to the public edition. Preserve routes. Rewrite home, category, about and error-page copy. Validate links and ensure draft-only metadata does not re-enter the publication.

### 3. Themes and interaction

Apply semantic colors throughout. Use system appearance until the reader selects a theme; persist that selection across pages and reloads. Keep the toggle keyboard accessible and report its state. Check mobile header fit, no-JavaScript reading, print, focus and contrast. Correct concrete search/navigation defects found during review.

### 4. Iterative review and publication

For each finding, record evidence, root cause, chosen correction and recheck in `PUBLIC-EDITION-REVIEW.md`. Run build/link/content tests and browser accessibility/interaction checks. Inspect desktop and mobile screenshots. Fix any failed gates, repeat affected checks, then publish through the existing GitHub Actions workflow and verify the live assets.

## Completion criterion

All identified material findings have a correction or an explicit content boundary; targeted checks pass; the public site deploys successfully. This is a bounded review of the current edition, not a claim that future lore or every possible accessibility issue is exhausted.
