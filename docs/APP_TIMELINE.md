# App use and update timeline

**Repository/package update:** 28 October 2026  
**Current release:** 0.1.0 (`v0.1.0`)  
**Legal research baseline:** 27 October 2026

This is a sequence, not a promised number of days. The time each matter takes depends on its facts, documents, lender requirements and firm procedures.

## Timeline for using the app

| When | What to do | Check before moving on |
|---|---|---|
| Before first use | Read `LICENSE` and `docs/USE_PERMISSION.md`; obtain prior written permission. Install the complete ZIP and keep its folder structure intact. | Installation does not grant permission to use the contents. |
| After installation | Run `python -m conveyancing_skill.cli validate` (or `conveyancing validate` after installation). | A software pass checks package structure and rules; it is not legal verification or professional approval. |
| At matter opening | Use an approved private workspace outside the public repository. Select the relevant transaction profile and record each document with a stable ID and page/clause reference. | Do not add live client or confidential matter data to the public repository or unapproved AI tools. |
| During review | Use the workflow and CLI to organise evidence and surface unresolved issues. Compare extracted text with the original documents. | Treat all stages as outstanding until a conveyancer checks the actual evidence. |
| Before exchange, completion, tax filing or registration | Check current law, commencement and transitional provisions, current forms, lender instructions, tax/fee rules and firm policy for the matter's effective date. | Do not treat an empty blocker list or automated calculation as clearance to act. |
| At close and on later updates | Record decisions and evidence in the firm's matter system. Review source changes under `docs/MAINTENANCE.md`; have a qualified reviewer approve legal changes before treating them as current. | The app does not send correspondence, file applications, release funds or provide legal sign-off. |

For the detailed matter sequence, see [`PRACTICAL_MATTER_WORKFLOW.md`](PRACTICAL_MATTER_WORKFLOW.md).

## Update and future-use timeline

| Date | What it records |
|---|---|
| 27 October 2026 | Legal research reference date for the current source registry and rules. It is not an assurance that the material remains current after that date. |
| 28 October 2026 | Version 0.1.0 published as a downloadable GitHub release; installation and distribution guidance recorded. No new legal research baseline is claimed by the packaging update. |
| After 28 October 2026 | No automatic legal-content refresh is promised. Check primary sources at the point of use and follow the maintenance process when sources or rules change. |
| 2030 and later | The package has no general 2030 expiry date. It may remain usable as software, subject to host compatibility and permission. Its stored legal material must not be assumed current through 2030. Date-sensitive features may refuse calculations after their declared review-by date until their data is researched, refreshed and checked. |

The recorded update date tells users what they have downloaded. It is not a “law current as at” date for a later matter. See [`VALIDATION_AND_LIMITATIONS.md`](VALIDATION_AND_LIMITATIONS.md) and [`MAINTENANCE.md`](MAINTENANCE.md) before relying on the package.
