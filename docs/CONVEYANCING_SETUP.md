# Conveyancing setup: from instruction to closure

This is an England and Wales working pack for a supervised solicitor or licensed conveyancer. Before use, obtain the written permission described in `LICENSE` and `docs/USE_PERMISSION.md`; commercial use needs separate permission. Select an approved private workspace for matter data. This repository is public; never commit client records, lender instructions, identification, banking data or privileged advice.

## Start here

1. Record the pseudonymous matter reference, role, jurisdiction, property and tenure in `templates/SETUP_INTAKE.md`. Confirm the actual client, authority, conflicts and the firm's onboarding arrangements in approved systems.
2. Select the profile with `conveyancing workflow --list` and `conveyancing workflow <profile-id>`. Save the generated 15-stage work record only in approved private storage. Review applicability; a stage or requirement starts outstanding and is not completed by generating a checklist.
3. Create the document inventory from `templates/DOCUMENT_REGISTER.md` and use `knowledge/workflows/DOCUMENT_MATRIX.md` to identify evidence. Assign a stable ID and exact page, paragraph, entry or clause to each finding. Use `templates/ISSUE_REGISTER.md`, `templates/ENQUIRY_TRACKER.md` and `templates/KEY_DATES_AND_ACTIONS.md` for outstanding work.
4. Choose the applicable pack below. Obtain actual forms from their publisher and observe licence conditions. Proprietary forms are not reproduced here.

| Matter | Working records and modules |
|---|---|
| Buyer / seller, freehold | `templates/PURCHASE_PACK_REVIEW.md`, `templates/SALE_PACK_REVIEW.md`, `templates/PLAN_REVIEW.md`, `knowledge/practice/TITLE_REGISTERED.md` |
| Leasehold / managed estate | `templates/LEASE_MANAGEMENT_REVIEW.md`, `knowledge/practice/LEASEHOLD_AND_BUILDING_SAFETY.md`; check actual lease, variations, landlord and management evidence |
| Auction | `templates/AUCTION_PACK_MATRIX.md`, `templates/AUCTION_RISK_REPORT.md`, `knowledge/practice/AUCTIONS.md` |
| Remortgage / bridging / guarantee | `templates/FACILITY_REVIEW.md`, `templates/LENDER_CONDITION_CHECKLIST.md`, `knowledge/practice/LENDERS_AND_ILA.md` |
| Gift, declaration or evidence statement | `templates/EVIDENCE_GIFT_LOAN_REVIEW.md`, `templates/DECLARATION_FACT_SCHEDULE.md`, `knowledge/practice/EVIDENCE_GIFTS_AND_LOANS.md` |
| Unregistered / first registration | `knowledge/practice/TITLE_UNREGISTERED.md`, `templates/REGISTRATION_PROGRESS.md` |
| New build, shared ownership, probate, trust, commercial or development | applicable profile plus `knowledge/practice/DEVELOPMENT_AND_SPECIAL.md` or `knowledge/practice/COMMERCIAL_AND_TAX.md`; seek specialist input as appropriate |

## Evidence, reporting and decisions

Check every title entry, plan, deed and search against the original. Record discrepancies, missing attachments and requests; a text extract is not signature or plan verification. Optional `conveyancing extract <file> --ocr --output <private-file>` runs local OCR when its dependencies are available, but OCR is unverified and must be compared with the original. For lender work use the actual offer and current instructions; record each condition, source, evidence, report and actual response in `templates/LENDER_CONDITION_CHECKLIST.md`. Draft reports and correspondence using `templates/CLIENT_UPDATE_DRAFT.md`, `templates/CLIENT_TITLE_REPORT.md`, `templates/REPORT_ON_TITLE.md` and `templates/TITLE_ENQUIRIES.md` as appropriate.

Review legal sources, territorial extent, commencement, transitional rules, forms and the lender's actual requirements at point of use. Use `templates/TAX_REVIEW_RECORD.md` for a human tax review. The narrow calculator gives illustrative bands only and does not decide relief, surcharge eligibility, historical treatment or liability. Date metadata alone does not stop an illustration; unknown applicability and current-source confirmation remain explicit.

## Exchange, completion and registration

Use `templates/COMPLETION_CHECKLIST.md`, `templates/KEY_DATES_AND_ACTIONS.md` and the actual contract and lender requirements to organise evidence. The conveyancer records instructions and decisions; the tool does not authenticate signatures, certify title, exchange, file or release funds. After completion record the application, priority information, evidence, requisitions, actual deadlines and outcome in `templates/REGISTRATION_PROGRESS.md`. Record client/lender reporting, undertakings, notices and residual actions through closure. See [HMLR requisition guidance](https://www.gov.uk/guidance/hm-land-registry-requisitions) and [execution of deeds guidance](https://www.gov.uk/government/publications/execution-of-deeds) for current procedures.

## Practical boundaries

The pack supports common scenarios and is not exhaustive. It is not a secure case-management system, a complete forms library, automatic legal verification, a bank feed or an independent professional opinion. Check scans, plan colours and boundaries, authenticity, signatures and execution in the originals. Do not invent facts, confirmations, signatures, dates or executed legal instruments. A qualified reviewer decides the action appropriate to the actual matter.
