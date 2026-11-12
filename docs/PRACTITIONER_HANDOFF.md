# Practitioner handoff and host acceptance

Use an approved private matter workspace and the permission process in `docs/USE_PERMISSION.md`. The CLI emits working records; it does not persist a matter or certify evidence. Keep decisions in the firm's case-management system.

## Matter issue register

Copy the following into the approved matter system. Give every issue a stable ID and link it to the stage and evidence locator. A blank field means unknown, not complete.

| Issue ID / stage | Fact or assertion and document ID/page | Risk / uncertainty | Owner and next action | Deadline and source | Client/lender report and decision | Resolution evidence / reviewer |
|---|---|---|---|---|---|---|
| | | | | | | |

For lender conditions, record the lender, actual offer and instruction source/version/paragraph, trigger, evidence, report, response and reviewer. Record missing instructions as **not supplied**. A waiver requires evidence from the authorised lender; do not assume silence is approval. Do not copy licensed lender material into a public repository.

## Source change review

The source watcher produces technical change candidates. Changed hashes stay at the prior baseline until a human reviews the source and deliberately updates the baseline. A fetch failure is distinct from a detected change. Persist the output artifact or an issue in the approved review system, including source URL, old/new hash, detection time, affected material, reviewer and disposition. Review amendments, territorial extent, commencement and transitional provisions using authoritative sources. No hash change approves a rule. The 9 November 2026 GitHub source-watch run 42654526654 detected a content change; its artifact requires review. A hash difference alone does not establish a legal change.

## Fresh-host acceptance record

Record host and version, plugin release/commit, date and reviewer. In an approved test environment use fictional data to verify: plugin discovery; access to root skill and linked modules; document upload and page/paragraph citations; workflow output; source access; and behaviour when browsing, filesystem or a tool is unavailable. Record actual results and limitations, and do not claim a pass until the host has been tested. A bundled CLI is not proof that a host can execute it.

## Document handling

Maintain a document inventory with ID, received version, source, pages present, pages extracted, unreadable/scan pages and locator. Present conflicting extracts side by side with document/page references. Escalate boundaries, plans, execution, signatures and authenticity for human inspection. OCR or text extraction is not evidence of authenticity.

## Illustrative matter checks

- Historic charge: identify the entry and any claimed release, cite source and request proof of discharge. Correspondence alone does not establish release.
- Leasehold: list lease and management evidence received and missing; record any proposed client/lender referral and the reviewer's decision.
- Lender condition: record actual instruction and source, evidence and response; a blank field remains outstanding.
- Conflicting pack: cite each document and locator, explain the discrepancy and record an enquiry rather than silently choosing a version.

These prompts are illustrative, not legal sign-off. Check current primary sources and lender requirements for the matter.

## Optional local OCR and plan review

Use `conveyancing extract /approved/path/scan.pdf --ocr --output /approved/path/ocr.json` only in a firm-approved local environment. Requires Tesseract, Poppler's `pdftoppm`, Pillow and pypdf. It creates temporary raster images locally, restricts input/page sizes and deletes its temporary directory; review originals and firm retention policy. OCR is unverified and does not interpret plans or verify execution. Use `templates/PLAN_REVIEW.md` for human visual plan review. See `docs/CASE_SYSTEM_HANDOFF.md` for local action export.
