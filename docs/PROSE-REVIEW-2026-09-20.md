# Public prose review, 20 September 2026

## Plan

Use the supplied Humanizer v3 skill to read and edit the complete public collection, its metadata, the reader interface and repository prose.

1. Compare the 44-file Drive inventory with the repository snapshot. Read all 37 Markdown files and identify repeated disclaimers, draft instructions, empty summaries and awkward prose.
2. Edit paragraphs in context. Keep the learned voices of the Gnome and Goblin naturalists. Preserve factual qualifications, legal notices, chronology, linguistic rules, examples, citations and link targets.
3. Replace catalog heading lists with summaries. Align titles with the articles. Edit atlas descriptions and site copy. Preserve routes, atlas codes, dictionary identities and existing section bookmarks.
4. Review repository documentation and archived prose without changing historical status, research results or source attribution.
5. Compare edited texts with the originals. Check language examples and structured records independently of prose. Read the changed passages again for voice and meaning.
6. Update existing Drive files in place, preserving their IDs. Make targeted edits to the native index. Fetch the results and record their modification times and checksums.
7. Build and test the site, inspect desktop and mobile pages, then publish through the existing GitHub Actions workflow. Verify the deployed result.

## Initial findings

The source inventory and modification times match the 18 September snapshot. Catalog descriptions concatenate headings instead of summarizing articles. Many articles repeat the same scope notice. The long Erde history retains draft labels and overlapping accounts of the same events. Some language example notes discuss editorial choices instead of explaining grammar. Erde's overview incorrectly says there is no public Goblin profile.

No new lore is needed for this edit. Technical records and historical source claims must retain their meaning.

## Changes

- Edited all 37 public Markdown files. Replaced draft labels, redundant conclusions and repeated scope notices with direct descriptions. Kept necessary uncertainty in the passages where it matters. Moved each article’s rights notice to its end.
- Rewrote all 37 catalog summaries and thirteen atlas descriptions. Catalog titles now match article titles, including the detailed Gnome reference. The reader no longer needs a separate Gnome display correction.
- Removed the homepage’s “Reading the setting” notice and the decorative arrows on article cards. Revised category introductions, About and search prompts.
- Replaced ten example annotations with grammar explanations and edited nineteen dictionary notes. Updated the matching Markdown, JSON and TSV representations together. Removed machine-style feature labels from the example article while preserving the tags in its data file.
- Corrected Erde’s outdated statement that no Goblin profile existed. Repaired the native index’s Goblin and Hamarkorar links, which both pointed to Gnomes.
- Edited repeated prose in the repository’s archived introductions and language guides. Added dated notes to distinguish this copy edit from the historical decisions. The same explanatory language notes were edited in the historical dictionary and example files; their 571 records and 98 examples retain their forms, meanings, translations and identifiers. Technical decision ledgers, measurements and past validation results retain their historical status.
- Updated the existing Drive files in place. No source IDs changed. The regional dictionary required no changes.

## Preservation and verification

All 37 articles retain their original Markdown link targets, reference tables and numeric values. A separate comparison confirmed that the 562 dictionary records retain their forms, meanings, parts, grammatical roles, domains and order. All 97 examples retain their sentences, translations, identifiers and grammar tags. The regional dictionary is unchanged.

All 43 raw source files were fetched after the edits and compared byte for byte with the repository. The native index was exported again. The 44-file manifest records the final source modification times, byte lengths and SHA-256 checksums.

All 43 native index links were checked, with two corrected. All 58 paragraph styles were preserved. Google Docs initially extended one link change into the adjacent Gnome link; readback caught it, the three adjacent links were separated and restored, and the full link/style comparison then passed.

The build retains all article routes, thirteen atlas codes and dictionary bookmarks. Eighteen previous section bookmarks resolve through aliases after heading edits.

- All nine build, source, link and data tests passed.
- All thirteen browser tests passed, including search, keyboard use, no-JavaScript reading, theme persistence and storage failure.
- The browser matrix checked fifteen routes at 1440, 390 and 320 pixels in both themes, with no page overflow or automated WCAG A/AA violations.
- Desktop home, mobile Korvar and desktop dark-history renders were inspected. Headings, tables, navigation and body text remained readable.
- Local browser checks used the existing temporary Chromium 153 installation with system fonts. Project dependencies and CI configuration were unchanged.

The prose was reread against the original passages after editing. Genuine technical contrasts, unresolved mechanisms and the naturalists’ disagreements were retained. This is an editorial pass; it does not certify the underlying scientific models.

Publication uses the existing GitHub Actions workflow. Its run records the final build, browser checks and Pages deployment.
