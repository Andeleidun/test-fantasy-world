# Dverghamar source synchronization and validation

Date: 7 September 2026. Starting repository revision: `a8f7e6ab873d2dd109bde088d1962e39d1d59ebf`.

## Source order and scope

The current Drive documents were read before editing. Newer repository naming/projection decisions, geographic trials and geological validation records were restored to documents 20 and 24, retaining their selected versus proposed status. Dverghamar source ledgers 35–38 and the related Thal passages in 33 were then revised and read back before this repository synchronization. Source links are in `content/SOURCES.md`.

Related legacy planet, ancestry and giant summaries were reconciled in their native and Word versions. Language references received physical-context corrections; the lexical data, grammar, examples and people-name assignments were preserved. The five current public Erde maps were restored to the Drive atlas editions. Dverghamar's eight SVGs retain their geometry with revised physical readings. No experimental continental outline or species territory was adopted.

The full scientific assessment is in `DVERGHAMAR-SCIENTIFIC-REVIEW.md` and Drive document 38. It separates physical calculations, relevant analogues, conditional models, unsupported values and fictional premises. Existing editorial/public separation remains intact; no raw connector payload or private narrative draft is committed.

## Verification results

- Native document read-back confirmed the intended paragraph replacements and appended material. The three restored Google source links in document 24 are native linked resources. A broad match to a repeated ancestry heading was immediately reversed, then applied at the exact Thal paragraph; comparison confirmed that unrelated paragraphs were preserved.
- Legacy Word pages and regenerated atlas maps/PDF layouts were rendered and reviewed. A truncated PNG and a heading page-break issue were repaired before final atlas upload.
- The water partition totals 240 million km³ water-equivalent. Independent calculations reproduce about 24.53% corridor area, 3.0-km example ice thickness, 2.81-km conductive comparison, 134-TJ annual food demand, 21-MW hydropower and 1.2-m³/s example cooling flow. These checks validate stated arithmetic, not the planet's climate or carrying capacity.
- `npm test` passed all five existing build/content tests: links/fragments, publication scope/search, source distinctions, dictionary consistency and Erde identity. The build retains 21 articles, 13 maps and 571 dictionary records.
- Local browser tests could not launch because Chromium was absent. Installation timed out at the browser CDN; no browser-test success is claimed. The existing GitHub workflow runs its browser/accessibility checks before deployment.
- `git diff --check` passed. Remote `main` still matched the starting revision when fetched before the commit.

## Remaining scientific gates

The joint stellar/escape, atmosphere, topography, ice and water-return model is unresolved. Local runoff, food yield, underground heat rejection, native adult/nursery physiology and Thal multigenerational reproduction at 1.53 g remain explicit tests. More prose review cannot establish those results. Keep the selected world and peoples while adjusting the narrowest failing quantitative assumption when those models are available.

## Continuation from e99ab003

Google Drive scientific review document 38 and governing documents 35–37 were re-read before editing. Drive was updated and read back before repository synchronization. The restored Erde Proposal 4 Strategy A reconstruction, its U1–U4 gates, the Dwarves’ independent six-limbed ancestry and preferred mineral nursery, and the Thals’ separate refugee identity were preserved.

This pass selects one linked screening case: a 0.50-solar-mass, 8.0-billion-year early-M star approximated by 0.040 solar luminosities and 0.47 solar radii; 1.20 Earth bolometric flux at 0.1826 AU; and a 40.30-day orbital and synchronous period. It also defines a dry 1.50-bar atmospheric input and records the derived gravity, escape speed, column mass, total atmospheric mass and scale height. The values are conditional model inputs, not a completed stellar track, escape history or climate solution.

The unresolved first gate is now narrower: integrate stellar bolometric and rotation-dependent XUV history with magma-ocean exchange, mantle retention, oxidation, hydrodynamic and diffusion-limited escape, impacts and outgassing. Test staged secondary-atmosphere formation first and delayed outgassing plus bounded later delivery as the one materially different retry. Climate, ice, catchment, inhabited-valley, adult/nursery and Thal-demography work remains downstream.

Local validation reproduced the stated arithmetic. `git diff --check` passed. `npm test` rebuilt 21 articles, 13 maps and 571 dictionary records and passed all five build/content tests. The 12 Playwright checks did not launch because the local Chromium executable is absent; this is an environment limitation, not a failed browser assertion. The earlier attempted download from this baseline had already timed out, so it was not repeated. The GitHub workflow remains the browser/accessibility validation path for the resulting commit.
