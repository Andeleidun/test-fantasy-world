# Canon review and revised world illustrations

20 September 2026. Plan recorded before content edits and image generation.

## Why another review was needed

The preceding import checked the repository against the public Drive files. Those files still contained older decisions. Exact file parity did not establish that the lore was current. This review compares public statements with later accepted decisions as well as the topic records.

The author's instruction in this review establishes the Thal migration at **40,000 years before the present**, overriding older five-thousand-year accounts. The later Thal and Dorrenath investigations contain both accepted developments and unselected proposals; only accepted, publicly eligible material belongs in the guide.

## Changes to make

| Subject | Correction |
| --- | --- |
| Thal migration | Use about 40,000 years ago in prose, catalog, captions and the ancestry diagram. Describe the fleeing people, animals and plants and their changed arrival without inventing a cause or disclosing the underlying magical explanation. |
| Erde chronology | The Thal departure precedes the histories' five-thousand-year snapshot. Retain that separate snapshot and the date of early experimental shapeshifting. |
| Dorrenath | Replace the short city-scale description with the accepted 25-kilometre tree, inhabited spaces, responsive host, Great Mother tradition and practical obligations of residence. Leave exact crown width, location and proposed habitats unsettled. |
| Elven life and travel | Include practical developments of the four traditions, stable bodily identity and gradual childhood learning. State that passage between worlds remains rare. A dependable local route does not guarantee an onward interworld journey. |
| Jotun | Do not present a provisional size range as settled anatomy. Preserve imposing cold-adapted bodies and varied societies. |
| Enchanted machinery | Distinguish sensitive electrical equipment from more robust simple machinery. |
| Gnome account | Put the previously restored bodily-tissue and centuries-of-house-growth details in the public source itself. |
| Atlas and entry pages | Replace statements that revised illustrations are unavailable. Put the five complete guides first. |
| Duplicate repository articles | Replace obsolete article copies with links to the current guides and their immutable historical versions. Keep scientific research records recognizable as dated research. |

## Artwork briefs

| World or subject | Landscape and composition | Light and materials |
| --- | --- | --- |
| Erde | Retain the cultivated river basin, boats and inhabited banks. | Daylight, varied greens, earth and timber. |
| Dverghamar | Replace the pastoral valley with a close, weighty rock escarpment, excavated homes, water-driven industry and limited planted benches. | Fixed low light, deep shadow, weathered stone, metal and wet rock. No green alpine postcard. |
| Merenval | Replace the river-valley composition with a water-level maritime scene: flooded forest, branching roots, inhabited boats and open channels. | Humid green canopy, blue-green water, diffuse light and living construction. |
| Merenval's companion | Add a broad continental plateau scene, steep pillars and crystal-bearing masonry. | Open air, mineral colors and pale dry interiors. Cavern mouths connect to a separate ecology below. |
| Dorrenath | Add a landscape-scale living tree with a broad crown, clouds far below upper branches and forest at its feet for scale. | Living bark and foliage. No precise site, crown diameter, mapped city plan or unselected anatomy implied. |

These are scene illustrations, not surveys. Surface details and building designs remain artistic interpretations. Do not manufacture a fixed planetary color palette, a new species or named settlement to differentiate the images.

## Source coverage

The audit uses the current charter and knowledge register; topic records 33–37, 40, 42, 44–48; the September 18 correction record; and the later Thal and Elves/Dorrenath investigations. The September 19 atmosphere/location proposals and September 20 Erde simulation results were checked for status. Their unselected geography, climate and evolutionary scenarios are not promoted into canon. Current language references and all six datasets are checked together.

The public knowledge boundary still applies. Observable life and landscapes, comparative natural history, attributed traditions and ordinary practitioner experience can be described. Technical mechanisms, detailed ancestry models and hidden cosmology stay outside this edition.

## Verification and publication

1. Review every public subject and the reader's captions against its topic source and later accepted decisions.
2. Update the existing public Drive files in place, read them back, and refresh their checksums and modification times.
3. Regenerate the maps and five Markdown/HTML guides. Scan current prose, metadata, search output and SVG text for the superseded date and associated assumptions.
4. Check the new pictures individually and together. Confirm placement, alt text, image loading and distinct visual character on desktop and mobile.
5. Run content, link, bookmark, dictionary and browser/accessibility checks. Keep regression checks for the corrected chronology and source boundary.
6. Publish the reviewed tree, confirm the Pages workflow and compare the deployed pages and changed assets with the local build.

## Results

The content and artwork changes above are complete. Eighteen public Drive files were updated in place and read back as raw bytes; all eighteen exactly match the repository copies. The fresh folder listing contains the same 44 source IDs, with modification times matching the refreshed manifest.

The public sources and five guides now contain 14 figures: seven maps, six scene illustrations and the Stavmark chart. Four illustrations were generated in this review: two replacements and two additions. Their prompts are recorded in `content/reader/illustration-prompts.json`; the final WebP assets are in `assets/illustrations/`. The remaining two scene illustrations were retained after comparison.

Twenty-seven obsolete article copies now point to the current guides and immutable historical versions. The unused article catalog agrees with the current one. Dated scientific research remains identifiable as research; Thal-related assessments carry a correction notice rather than silently changing the assumptions of past analyses.

| Review group | Result |
| --- | --- |
| Erde and Thals | Corrected the migration date and event order; retained the separate five-thousand-year regional and shapeshifting chronology. Added the publicly describable migration developments. |
| Merenval and Elves | Incorporated the later Dorrenath and practical Elven developments. Qualified interworld travel as rare. Location proposals, exact crown width and hidden mechanisms were excluded. |
| Dverghamar and its native peoples | Retained the independent native ancestry, four arms, five species and deep-massif subspecies. Corrected the provisional status of Jotun height. |
| Gnomes, Goblins and Orcs | Retained their distinct accounts and public natural-history limits. Moved the two Gnome details previously supplied only by reader composition into the source. No newly selected Goblin or Orc revision was found. |
| Magic, spiritual practice and Otherworld accounts | Refined the electrical-equipment distinction and Dorrenath's attributed Great Mother tradition. Preserved the limits of practitioner testimony and human accounts. |
| Language | Retained selected forms, all 562 dictionary entries and 97 examples. Embedded the existing writing chart in its source. |
| Atlas and data | Removed obsolete artwork notices, updated all thirteen atlas records with their reviewed images, and corrected the ancestry diagram. |
| Prose | Applied the Humanizer rules to the rewritten accounts, captions, entry pages and replacement article notices. Preserved the longer naturalist accounts and language examples. |

All 12 content/build tests and all 15 browser tests passed. They cover source checksums, complete source destinations, internal links, legacy routes, dictionary identity, map coverage, single image placement, corrected chronology, search, keyboard use, no-JavaScript reading and automated WCAG A/AA checks. Browser checks covered light and dark themes at 1440, 390 and 320 pixels.

Rendered review confirmed that all four new pictures and the revised ancestry diagram load with their captions, without horizontal overflow. The changed map has no text outside its canvas. Desktop, mobile and dark-theme screenshots were inspected. The deployed tree is built and checked by the repository's existing Pages workflow; final live-file verification follows publication.
