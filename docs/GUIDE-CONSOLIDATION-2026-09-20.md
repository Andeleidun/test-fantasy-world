# Guide consolidation and illustrations

## Plan recorded before implementation

Baseline: `eb4433cd22aa15e3586076693d38b5f62e1f8e35`.

The reader currently distributes 36 subject articles across six category pages, a home page and a separate dictionary. Many articles are only a few paragraphs long. Readers must follow several links to connect a world's landscape, inhabitants and history. Thirteen atlas entries have no displayed maps. The only published reference image is the Stavmark chart.

The new edition will have five comprehensive guides:

| Guide | Contents |
| --- | --- |
| Erde | Geography, maps, ancestry, regional histories and institutions, Goblins, and the Thal departure |
| Dverghamar | Day and night, landscape and water, mountain settlements, wildlife, Hamarkorar, Thals and Jotun |
| Merenval | Both inhabited worlds, landscapes, Elven traditions, Gnomes and living houses, Orcs |
| Magic and belief | Everyday magic, practitioners, enchanted objects, familiars, spiritual practice, Otherworld accounts and religious boundaries |
| Korvar | Sounds, grammar, material vocabulary, regional languages, writing, all examples and the complete dictionary |

The home page will introduce the setting and its skies. About will hold source information, map conventions and downloads. Search will link directly to sections in the five guides. The main navigation will lead straight to these guides; there will be no category-hub step. Each guide will have a compact chapter contents list and detailed section links. All substantive text remains expanded and readable without JavaScript.

## Editorial and source handling

The synchronized public collection remains the source authority. Composition will happen in a separate, explicit reader configuration. Every source article and section will have a recorded destination. Remove repeated rights paragraphs and navigation-only lists from the composed pages, put rights information in the shared footer, and revise obsolete statements about missing illustrations. Merge overlapping introductory material where the detailed account carries the same facts. Preserve the naturalist voices, grammatical data, examples and uncertainties.

Apply the supplied Humanizer v3 skill to new introductions, transitions, captions and edited passages. Review whole paragraphs and preserve supported claims. Keep older source snapshots and research records available as repository history.

## Images and maps

Retain the current Stavmark reference. Existing research atlas sheets include superseded continental geometry, numerical habitat envelopes and engineering assumptions absent from the public collection. They require revision before use in this reader.

Create source-grounded vector plates for Erde's regional geography, landscape and ancestry; Dverghamar's light, habitats, water and settlement; and Merenval's paired landscapes. Associate every E1–E5 and D1–D8 subject with an inline figure. Maps will distinguish schematic relationships from surveyed positions. Do not invent shorelines, regional coordinates, settled political borders, biological measurements or physical model results.

Use the built-in image generation tool for contextual landscape illustrations. Show an Erde river landscape, Dverghamar's inhabited twilight country, Merenval's maritime landscape and a Gnome living house. Depictions will be captioned as illustrations; unspecified appearances will not become natural-history claims. Store final image assets in this repository and document their prompts.

## Implementation and verification

1. Record complete source-to-guide and old-fragment-to-new-fragment mappings. Build the five pages, inline dictionary and images. Rewrite internal links to their final destinations. Retain old URLs as compatibility pages, with fragment-aware automatic forwarding and useful no-JavaScript links.
2. Replace the persistent category sidebar with a compact header and guide navigation. Keep page contents available on desktop and mobile. Support narrow screens, light/dark themes, print, keyboard navigation and full-size figure viewing.
3. Test source coverage, all old fragments, current links, dictionary identities, all 97 examples, asset coverage and source snapshot checksums. Update obsolete tests that required text-only atlases and category hubs.
4. Run the build and interaction/accessibility suite, inspect representative pages and every new illustration/map, and fix concrete defects. Check the upstream branch for concurrent changes before publication.
5. Publish through the existing GitHub Pages workflow. Confirm successful deployment and compare live guides and assets with the reviewed build.

## Results

The reader now contains five complete guides, with 30 chapters in total. The home page introduces the worlds and skies; About contains source information, map conventions and downloads. Search points to sections in the complete guides. The persistent category sidebar and category-hub browsing step are removed.

`guides/` contains the same five accounts as Markdown for repository readers and download. Their images appear inline. Korvar includes the complete dictionary and all translated examples. `content/reader/coverage.json` records 336 source destinations, including 16 merged summaries or navigation sections. The 44-file synchronized source snapshot remains byte-for-byte unchanged.

### Visuals

- Four new illustrations: Erde river country, Dverghamar twilight settlement, Merenval coast and a Gnome living house. The built-in image generator produced the artwork; exact prompts are retained in `content/reader/illustration-prompts.json`. Final web assets are in `assets/illustrations/`.
- Seven new vector diagrams cover all thirteen atlas subjects and the Merenval pair. Their captions and full-size links appear on the relevant guide pages. `scripts/draw-reader-maps.py` reproduces the diagrams from the documented qualitative relationships.
- The existing Stavmark chart appears within the writing chapter. No current reader figure is left only in a separate gallery or atlas index.
- Historical research maps remain in the repository. Their numerical envelopes, proposed geography and engineering assumptions are not introduced into the current public accounts.

### Verification

- Ten build/content tests pass: exact source snapshot checksums, coverage, local routes and fragments, figure coverage, public-data consistency, dictionary identity, complete Markdown links and all 97 translated examples.
- Fifteen browser tests pass. The accessibility matrix checks all eight reader/utility pages at 1440, 390 and 320 pixels in light and dark themes, with no page overflow or automated WCAG A/AA violations.
- Browser interaction checks cover search failure/recovery and stale requests, dictionary filtering, keyboard navigation, theme persistence and blocked storage, mobile chapter selection, old fragments and reading without JavaScript.
- A separate comparison against the preceding build checked 1,447 old content bookmarks, including dictionary records. Every one resolves to retained content or its documented merged section.
- Inspected all four generated illustrations, all seven maps and representative desktop/mobile/light/dark page renders. Corrected two crowded map labels, the coastal-route diagram's endpoint, and mobile scroll spacing beneath the sticky contents control. Image QA waits for decoding before capture.
- The five Markdown guides contain no broken local image, document or fragment links. Utility and data links use the published site address so the same files work in GitHub and in downloads.
- Source scientific and historical uncertainties remain as described in the public collection. This publication pass does not validate the older planetary models or select new continental geometry.

Publication uses the existing build, research-validation, browser-test and Pages-deployment workflow. The deployed commit and workflow result are recorded in GitHub history.
