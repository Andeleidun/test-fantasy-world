# Public edition review

## Scope

Reviewed the publication pipeline, all 21 public articles, dictionary and downloadable data, map captions, shared templates, themes, search, navigation, responsive reading, tests and deployment workflow. The original working sources and original illustrations remain intact. This edition contains approximately 21,400 words of articles, 571 lexical records, 98 translated examples and 13 atlas sheets.

The review follows `PUBLIC-EDITION-PLAN.md`. Each correction below was made after identifying the issue and its cause, followed by a focused recheck. Quantitatively unresolved worldbuilding remains explicitly provisional rather than being silently completed for publication.

## Round 1: publication and editorial structure

| Finding and root cause | Correction | Re-evaluation |
| --- | --- | --- |
| Working ledgers were rendered directly, mixing decisions, old alternatives and author instructions with current lore. | Added a separate public catalog and subject-based articles under `content/public/`; mapped each to its working source. | Public articles and search are checked for decision-history leakage. Original article routes remain available. |
| Familiar magic was buried in a long historical ledger and could disappear during condensation. | Added a dedicated familiar/shapeshifting article covering mutuality, separate minds, learned forms, repair, equipment and gestation. | Checked against the later decisions, including permanent mastery and the limits of native-magic retention. |
| Home and utility pages used promotional or vague copy. | Replaced the slogan with the world names; used direct headings, subject navigation and explanatory introductions. | Reviewed the home, category, about, search and error-page text. |
| Dictionary notes, downloads and map captions were separate routes for draft text to remain public. | Added public copies of vocabulary, aligned regional data, examples and map captions. The build uses these inputs and generates the Common TSV from the public lexicon. | Meanings agree between the displayed dictionary and downloads; word forms, grammatical roles and row order remain unchanged. |
| Grammar pages referred to unavailable generators, chapter numbers and implementation contracts. | Replaced those references with article links and reader-facing explanations while preserving substantive grammar, regional rules and all examples. | Reviewed the grammar and regional tables against their source edition; source and generated links resolve. |

## Round 2: accuracy and completeness of the edited documents

| Finding and root cause | Correction | Re-evaluation |
| --- | --- | --- |
| Condensing the water inventory to “total water” incorrectly included unresolved deep-mantle reservoirs. | Restored “exchangeable surface and near-surface water,” with included reservoirs and the separate mantle boundary. | Compared to the planetary bulk-properties source; overview and reference now agree. |
| A short statement about hostile hemispheres could imply cold alone excludes every large Earth-like animal. | Explained the combined limits of cold, darkness, food, heat and desiccation, distinguishing broad self-sustaining populations from supplied or sheltered animals. | Checked against the source climate interpretation. |
| Summarizing withdrawal could confuse ending a structural contribution with leaving an afterlife home. | Explicitly distinguished structural withdrawal, continued ordinary residence and voluntary departure. | Compared to the later domain-residence decision. |
| Brief afterlife treatment obscured the different sources of power and limits of restoration. | Restored permanent versus pooled power, surviving self-pattern requirements, consent of self-aware fragments and the need for a surviving trace to recover an exact memory. | Checked against the later restoration and power-persistence decisions. |
| Short biology introductions lost useful established adaptations and engineering ranges. | Added heat/cold/altitude traits, retained vision, deep-massif origins, conditional deep residence, mine/expedition limits and shallow rail cover. | Checked against the latest species and settlement sections; candidate traits remain candidates. |
| A simplified food-web account could overstate cultivation capacity or portray every flood as beneficial. | Restored photon-area limits, organic feedstock accounting, grow-light costs and damaging flood outcomes. | Reviewed energy flow from producers to fungi and consumers; no closed deep-city ecosystem is implied. |
| Standalone public Markdown lacked document titles and used website-only relative links. | Added titles, source-document links, direct map links and a source Common TSV. The renderer translates Markdown paths to Pages routes. | Every local public-document link and generated internal link resolves. |

## Round 3: interface and accessibility

| Finding and root cause | Correction | Re-evaluation |
| --- | --- | --- |
| The app assumed light colors throughout its components. | Added semantic colors, a pre-paint saved preference, system fallback, a keyboard-operable pressed-state toggle, guarded storage access and light print styling. | Tested system changes, persistence across navigation/reload, explicit preference overriding the system, blocked storage, no-JavaScript dark reading and print. |
| The first dark-theme pass found pale text on the retained light Erde card. | Added theme-aware card foreground/background tokens. | Dark contrast checks passed after correction. |
| The card correction also exposed a mobile heading rule overriding the Dverghamar card’s foreground. | Kept the responsive heading rule limited to typography. | Repeated the complete 12-test browser suite; all passed. |
| Navigation marked a category hub as the current page on an article or dictionary page. | Distinguished the current section from an exact current-page link. | Inspected generated navigation and checked accessible page structure. |
| Pending search requests could render stale results during the input debounce. | Invalidate the sequence and clear previous results immediately on input. | Delayed-request test confirms the old query does not return results for the new query. |
| Search repeatedly normalized the same large text and could display Markdown link syntax. | Cache normalized fields once per index load; extract searchable text from Markdown inline tokens. | Search, recovery and pagination checks pass; results use reader text. |
| Every map reserved the same image aspect ratio despite differing SVG dimensions. | Read each SVG viewBox to set the correct image dimensions. | Build succeeds for all 13 sheets; original artwork remains legible on its own light canvas. |

## Verification

- Four build test groups pass: generated links/anchors/IDs, worldbuilding-only scope and search destinations, public-source ownership and standalone links, and dictionary/download consistency.
- Twelve browser tests pass, including automated WCAG A/AA checks on six representative page types in both themes at 1440, 390 and 320 pixels. All tested layouts avoid horizontal page overflow.
- Keyboard checks cover skip navigation, theme activation and focus after pagination. Tests also cover failed-search recovery, stale requests, filtering and no-JavaScript reading.
- Desktop light/dark home pages, the dark grammar reader and a full mobile article were visually inspected for hierarchy, legibility, spacing and navigation.
- The local browser download endpoint timed out; local checks used Chromium 149 from a temporary browser package. The repository dependency set was not changed. GitHub Actions uses its normal Playwright Chromium installation and runs the checked-in suite before deployment.
- Existing working Markdown/data and original map artwork remain unchanged. Only the public edition, app, tests and maintenance documentation are updated.

## Publication and remaining boundaries

The existing GitHub Actions workflow builds and tests the public edition before uploading `dist/` and deploying to Pages. This review record is committed with the implementation; the exact deployed commit and execution result are recorded in GitHub’s workflow history.

No identified material issue remains open within this publication pass. The planetary climate, water budget, early atmospheric retention, biological productivity and reproductive measurements still require the modeling already identified in the source project. Regional names with no assigned community remain unassigned. Those are visible setting boundaries, not publication defects.

Automated accessibility checks and visual inspection do not constitute exhaustive assistive-technology testing. The editorial split does not make the working files private: they remain in the public repository. Future source changes require deliberate public-edition updates.
