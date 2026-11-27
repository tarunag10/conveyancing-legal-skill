# Law Society TA form source verification

**Review date:** 27 November 2026  
**Sources:** Law Society transaction-form guidance (page dated 24 June 2026) and TA6 sixth-edition guidance (page dated 4 February 2026).  
**Scope:** Public guidance and repository catalogue/practice statements only. This is not legal approval and does not verify the content, currentness or licensing of form binaries.

## Alert disposition

GitHub issues [#7](https://github.com/tarunag10/conveyancing-legal-skill/issues/7) (`ls-ta`) and [#8](https://github.com/tarunag10/conveyancing-legal-skill/issues/8) (`ls-ta6`) recorded HTTP 403 on 24 November 2026. This review used the publicly indexed official pages, which exposed their text and stated publication dates. Direct page retrieval still returned HTTP 403 in this review session. The alerts establish a retrieval restriction, not a substantive source change. No issue comments were identified on 27 November. They remain open for human approval and issue handling. The next routine source-monitor run is scheduled for Monday 30 November 2026 at 06:17 UTC.

## Sources and confirmed points

1. [Law Society: Transaction (TA) forms](https://www.lawsociety.org.uk/topics/property/transaction-forms), dated 24 June 2026. The page says forms are used alongside the Conveyancing Protocol and must be used by CQS firms. For TA6, it specifies sixth edition for new transactions instructed on or after 30 March 2026. For TA7, it specifies fifth edition for new transactions instructed on or after that date; if using the Protocol, send TA6 and TA7 together for seller completion. For either form, an older edition can continue for a pre-30 March instruction only where it has already been used for that transaction. It also identifies TA8 as the new-home information form and says flat purchases use TA7 for seller questions and LPE1/LPE2 for landlord or managing-agent questions.
2. [Law Society: TA6 Property information form (6th edition)](https://www.lawsociety.org.uk/topics/property/ta6-6th-edition), dated 4 February 2026. The page confirms the CQS edition requirement and transition above. It says TA6 is designed for owner-occupier home sales and most standard residential transactions in England and Wales; it is **not intended for new-build purchases** and **may not be suitable for part-exchange transactions and auctions without some amendment**. It says the Conveyancing Protocol would be updated in 2026 to clarify sending explanatory notes with TA6; the page does not establish whether that update was finalised or its operative wording.

Accordingly, the edition pair and 30 March 2026 commencement date already in rule `r-law-society-ta6` are supported by the two public guidance pages. The governing source is CQS/Protocol guidance, not a universal statutory prescribed-form rule. For transition, the trigger is not simply “older matter”: the older TA6 or TA7 must already have been used on that transaction before the instruction cut-off.

## Repository comparison and corrections prepared

- `knowledge/legislation/rules.json`: retains the confirmed edition requirement, narrows it to applicable new CQS sale/purchase transactions, makes the old-form transition precise, and flags the TA6 new-build/auction scope issue. `legal_reviewer_approved` remains false.
- `knowledge/legislation/source-index.json`: records the 27 November public-guidance check and states that binaries were not inspected.
- `knowledge/forms/catalogue.json`: records the official TA6 guidance link and owner-occupier/new-build/part-exchange/auction limitations. TA6 and TA7 binary verification remain false; no proprietary form text is copied.
- `knowledge/practice/LEASEHOLD_AND_BUILDING_SAFETY.md`: replaces the generic transition phrase with the source's already-used condition and states evidence limits.
- `knowledge/practice/AUCTIONS.md`: adds a seller-side TA6 suitability gate and prevents inferring that an unmodified form is appropriate or that the buyer must complete TA6.
- `knowledge/practice/DEVELOPMENT_AND_SPECIAL.md`: states TA6 is not intended for new-build purchases and points to case-specific developer enquiries; TA8 may be suitable but is not treated as a substitute without review.
- `knowledge/forms/FIELD_GUIDES.md`, `knowledge/forms/PRIORITY_FORMS.md`, `knowledge/practice/MATTER_PACKS.md`, `knowledge/workflows/DOCUMENT_MATRIX.md` and `templates/SALE_PACK_REVIEW.md`: add the exact instruction-date transition, conditional TA7 leasehold scope, TA6 notes recommendation and transaction-specific suitability checks. The notes are not described as a mandatory step unless the operative Protocol confirms it.

## Discrepancies and evidence gaps

- Previous repository wording described only “limited older matter transitional use” and was less precise than the publisher's condition that an older edition had already been used for that transaction.
- The former TA6 catalogue purpose (“standard owner-occupier residential sale, not new build”) omitted the publisher's qualification on part-exchange and auctions without amendment.
- Current public pages support the edition labels and selected scope limitations. They do **not** establish that every question, explanatory note, provision or practice instruction is unchanged.
- The restricted licensed binaries were not obtained or examined. No binary checksum, edition comparison, question-level review or licence review was performed.
- The current/final status and wording of the Law Society's announced 2026 Conveyancing Protocol update were not verified. No claim is made that all CQS transactions, including every atypical or new-build matter, require use of TA6 in an unmodified form.
- No qualified solicitor approved the changes. Legal review and issue closure remain separate human decisions; the plugin release state is recorded separately from solicitor approval.

## Review handoff

A supervising solicitor should review the scope and wording, especially the meaning of “applicable” CQS transactions, use on new-build and auction sales, any permitted amendments and the current Protocol. Keep issues #7 and #8 open pending that review. Do not label form binaries or unexamined material verified.
