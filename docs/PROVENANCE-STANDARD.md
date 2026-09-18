# Level 3 provenance standard

> The policy remains useful; the repository Level 3 manifest records the 14 September research snapshot. Current public import coverage is independently recorded in `content/public-sync.json`. It does not prove a new Level 3 evidence audit.

Level 3 provenance is required for every identifiable, deliberate and materially significant real-world source used by the project. It records what a source informed, how it was used, what it supports, and where fiction or uncertainty begins. It does not claim to recover unconscious influence, common fantasy vocabulary or coincidental resemblance.

The canonical authorial policy and Otherworld register are in [Drive document 41](https://docs.google.com/document/d/1jjVMwY809mFxfuB0mswFlCXEeFO-RUQBECcT9ByZgU0/edit). The repository manifest in [`content/provenance.json`](../content/provenance.json) indexes the distributed Level 3 records and maps every public article to at least one covered domain. The longer [`content/SOURCES.md`](../content/SOURCES.md) file retains synchronization history and source-specific scientific notes.

## Required fields

Each materially used source must preserve:

- Source identity, including the responsible creator or institution, title, edition or translation where relevant, and a stable locator.
- Source class, such as primary text, collector or translator, institutional scholarship, peer-reviewed research, educational synthesis, dataset, software or popular synthesis.
- The exact project claim, mechanism, motif, name, practice, design constraint, map or asset it informed.
- Its relationship to the project: evidence, strong inference, contextual reconstruction, adaptation, linguistic derivation, visual reference, comparative influence or general analogy.
- A support boundary that states what remains fictional, inferred, provisional or unresolved.
- The current decision authority and any relevant supersession.
- Rights status and cultural status when either affects use.
- Publication status: authorial only, eligible for public summary or already represented publicly.
- Confidence or uncertainty when interpretation, translation or evidence quality requires it.

Original setting premises use `fictional-premise` instead of borrowing external authority. Candidate research uses `candidate` and does not count as adopted-source debt until a setting decision uses it.

## Source order

Current decision ledgers outrank older sketches. An explicit correction or approved retcon outranks recency. Older material remains historical provenance or in-setting cultural mythology when the current authority does not establish it as literal history.

The registers closest to each claim retain the details:

| Domain | Primary Level 3 record |
| --- | --- |
| Source hierarchy and publication boundaries | `content/SOURCES.md` and Drive document 00 |
| Erde history and lineages | Drive documents 20, 24 and 33; geographic trial records under `docs/` |
| Dverghamar science and natural history | Drive documents 35 through 38 and `docs/DVERGHAMAR-SCIENTIFIC-REVIEW.md` |
| Merenval, its companion and System A | Current Merenval authority, Drive document 00 and the historical multistar comparison |
| Otherworld cosmology | Drive document 34 |
| Magic | Drive document 40 |
| Otherworld mythology, dragons and ecological analogues | Drive document 41 |
| Dverghamar language | Language source package and the working language files |
| Maps and datasets | Atlas source bundles, map methods and data credits |

## Public boundary

Level 3 is authorial traceability. Public articles can summarize records marked eligible, but they do not publish hidden mechanics, private reasoning, story material, rejected decisions or unresolved research as settled lore. Level 4 will be generated from these records rather than maintained as a separate factual authority.

## Completion rule

A current domain is complete when every adopted or materially used source has the required fields in its closest register, the manifest points to that register, and each published article maps to a covered domain. Future research queues, rejected options and unadopted candidates remain recorded but do not prevent closure.
