# England and Wales: conveyancing matter workbench v0.2.0

**Release status:** working **offline supervised beta**, not a certified legal opinion tool or deployed case-management integration. It preserves the existing 15-stage profile engine, 117-entry lender research directory, 98 indexed forms, deed-of-gift generator, legal practice guides and source-checking features in v0.1.12. The added Python workbench is standard-library based; reading PDF/DOCX requires optional `pypdf` / `python-docx` respectively.

**Critical:** this software cannot authenticate the identity of a signatory, establish a deed's valid execution, confirm legal marketability, act as a lawyer, certify lender title, advise a client without professional supervision, verify firm bank accounts, submit an eCoT, file at HMLR/Companies House, or transfer funds. It doesn't execute anything outside local user-selected files. Read the repo licence before use; live client work also requires firm security/AI approval.

## Features now available

| Area | Implemented v0.2.0 | Not implemented / human gate |
|---|---|---|
| Central matter record | JSON record, pseudonymous ID, audit hash-chain and controlled local edits | Multi-user access control, encryption, privileged DMS sync |
| Document discovery | PDF/DOCX/TXT/MD text, candidate facts and potential mortgage-offer condition lines with page/line and SHA-256 | OCR plan scale, signatures, diagram, genuine document verification |
| Comparison | Candidate-level title/party/company/loan/date mismatch and line diff | Full binary/layout/redline reconstruction; legal effect determination |
| Lenders | Directory lookups; requirements/waivers review; case-specific instructions gate | Live Part 2/offer download and accepted eCoT transmission |
| Security | First/second charge, multi-security and third-party advice missing-evidence flags | Legal effect of prior charge, ranking, restriction or consent |
| Auctions and dates | Original/extended completion records, notice trigger, configurable periods, provisional CoT notice; SDLT/LTT/MR01 and priority-date checks | Automatic interpretation of auction conditions, lender acceptance/cut-off and unknown holidays |
| Finances | Exact GBP decimal reconciliation, discrepancies and shortfalls | Ledger, cleared funds, verified bank details, authorisation |
| Leasehold and specialist | Applicability-driven missing-evidence tests for leasehold, BSA, tenancy, unregistered, probate/trust, new-build and commercial | Bespoke legal opinion and review of actual leases, grants, filed deeds and instruments |
| Documents | 12 reusable solicitor-style draft categories, source-linked issues, placeholders | Signing, sending, licensed third-party CoT/HMLR forms, law-firm branding |
| Registration | AP1/FR1, tax certificate, restrictions, fee, priority, deed/filing status preflight | Actual HMLR application/fee payment or acceptance |
| Post-completion | Application-vs-registration distinction, requisition draft and issue exports | HMLR case-status API, live requisition timer without source |
| Interface/exports | Accessible local HTML dashboard; Markdown/JSON and CSV/JSON handoff | Hosted dashboard, firm CMS Outlook/OneDrive/HMLR connectors |
| Source freshness | Dated official-source URLs and prior read-only source-watch integration | Automatic re-approval of laws or rechecking user-specific lender instructions |

## Setup

Install the plugin package in an approved environment following its pre-existing instructions, then install the Python package in your authorised workspace. Within its source folder:

```bash
python -m pip install -e '.[documents]'
conveyancing-workbench --help
```

If the script is unavailable, use `python -m conveyancing_skill.workbench` with `PYTHONPATH=src`. Do **not** run external network commands on confidential files. Keep the work area private, ideally encrypted at the firm infrastructure level; the plugin itself supplies no encryption or identity-management layer.

## End-to-end workflow

```bash
# 1. Create an empty pseudonymous matter; DO NOT use client name as file ID
conveyancing-workbench init /firm-private/matters/ANON-123.json \
  --matter-id ANON-123 --jurisdiction England --transaction-type auction_purchase

# 2. Register authorised documents. Everything extracted is UNVERIFIED.
conveyancing-workbench add-document /firm-private/matters/ANON-123.json \
  /firm-private/source/memorandum.pdf --id DOC-1 --type auction_memorandum
conveyancing-workbench add-document /firm-private/matters/ANON-123.json \
  /firm-private/source/loan-offer.pdf --id DOC-2 --type lender_offer

# 3. Record an observed fact at exact source location. Not lawyer approval.
conveyancing-workbench add-observation /firm-private/matters/ANON-123.json \
  --field title_number --value ABC123456 --document-id DOC-1 --locator 'page 2, panel 4'

# 4. Add transaction-specific requirements/financials/security via structured JSON
conveyancing-workbench update-data /firm-private/matters/ANON-123.json \
  --patch /firm-private/input/offer-and-completion.json

# 5. Review contradictory data, lender conditions, security, execution, money and registration
conveyancing-workbench review /firm-private/matters/ANON-123.json \
  --output /firm-private/output/review.json
conveyancing-workbench deadlines /firm-private/matters/ANON-123.json
conveyancing-workbench accounting /firm-private/matters/ANON-123.json
conveyancing-workbench security-map /firm-private/matters/ANON-123.json
conveyancing-workbench form-preflight /firm-private/matters/ANON-123.json
conveyancing-workbench post-completion /firm-private/matters/ANON-123.json --as-of 2026-11-27
conveyancing-workbench requisitions /firm-private/matters/ANON-123.json --as-of 2026-11-27

# 6. Compare revised lender paperwork text/Word/PDF
conveyancing-workbench compare original.pdf revised.pdf --output /firm-private/output/revision-diff.json

# 7. Draft (does NOT send) or prepare a screen-reader accessible review
conveyancing-workbench draft /firm-private/matters/ANON-123.json \
  --kind lender-report --output /firm-private/output/lender-report-draft.json
conveyancing-workbench report-md /firm-private/matters/ANON-123.json \
  --output /firm-private/output/review.md
conveyancing-workbench dashboard /firm-private/matters/ANON-123.json \
  --output /firm-private/output/review.html

# 8. Hand off open tasks MANUALLY, no integration is invoked
conveyancing-workbench handoff /firm-private/matters/ANON-123.json \
  --output /firm-private/output/tasks.csv

# 9. Verify audit integrity; do not treat a hash as lawyer approval
conveyancing-workbench audit /firm-private/matters/ANON-123.json
conveyancing-workbench validate /firm-private/matters/ANON-123.json
```

### Manual patch format

`update-data` accepts only `roles`, `requirements`, `securities`, `dates`, `financials`, `registration`, `execution`, `specialist`, `post_completion` and `lender`. It refuses to overwrite `review`, audit history and document records or to change any already marked `lawyer-approved` matter. All manual inputs remain unverified and must be independently reviewed. Offer-clause candidates are created only for document types `lender_offer`, `lender_instructions`, `facility_agreement` and `mortgage_offer`; they are not accepted conditions until a human checks the entire original and records an actual requirement with a matching `candidate_ref`. The model must still review the full offer, since keyword discovery cannot find every condition. Use `add-document` or `add-observation` for evidence record changes rather than writing source data without locators.

Example requirements/financial data:

```json
{
  "roles": ["buyer", "borrower", "lender"],
  "lender": {"name":"Rely Mortgages", "live_instructions_checked":false},
  "requirements": [{"id":"R-1","description":"Evidence of insurance","source_document_id":"DOC-2","source_locator":"offer page 4 condition 3","status":"outstanding","blocking":true,"evidence_refs":[]}],
  "securities": [{"id":"S-1","property_id":"P-1","title_number":"ABC123456","intended_rank":"first","charge_instrument_ref":"DOC-CHARGE"}],
  "dates": {"contractual_completion":"2026-11-20","agreed_extended_completion":"2026-11-27","target_completion":"2026-11-27","bank_holidays":[]},
  "financials": {"purchase_price":"100000.00","deposit_paid":"10000.00","seller_balance_stated":"90000.00","lender_net_advance":"65000.00","client_funds_confirmed":"32000.00","costs_and_disbursements":"2000.00","tax_and_filing":"5000.00"},
  "registration": {"application_type":"AP1","title_numbers":["ABC123456"],"tax_return_required":true,"fee_checked_against_live_scale":false,"priority_result_reviewed":false},
  "specialist": {"uk_company_or_llp_borrower":true,"leasehold":{"applicable":false},"tenancy":{"applicable":false}}
}
```

**Status facts:** lender `verified` should have source evidence, actual human reviewer/date. `waived_by_lender` needs a written lender decision reference and its date. The software flags missing proof but cannot validate the authenticity of such claims. Use a firm-controlled lawyer approval process, not an AI-produced approval.

## Draft types

`lender-report`, `seller-enquiries`, `client-update`, `auction-extension`, `completion-chaser`, `lender-cot-query`, `registration-requisition`, `security-consent`, `postcompletion-chaser`, `redemption-statement`, `funds-request`, `execution-clarification`.

Drafts use explicitly labelled blanks, never supplied or invented authorised signatures, and must be checked against originals. The existing separately implemented gift-deed generator remains the route for customised Deeds of Gift. For actual TR1/AP1/FR1/CoT and other protected forms, load official current source and authorised forms; don't substitute a generic original draft.

## Statutory example references, checked 20 November 2026

- HMRC SDLT: <https://www.gov.uk/guidance/check-if-you-need-to-send-a-stamp-duty-land-tax-return> (ordinary return 14 days from taxable effective date)
- WRA LTT: <https://www.legislation.gov.uk/anaw/2017/1/section/44> and <https://www.gov.wales/pay-land-transaction-tax> (30-day return and payment period from the day following the effective date)
- Companies House MR01: <https://www.gov.uk/guidance/register-a-charge-mortgage-for-a-limited-company> (21 days beginning the day after charge creation)
- HMLR official-search priority: <https://www.gov.uk/government/publications/official-searches-and-outline-applications/practice-guide-12-official-searches-and-outline-applications> (30 working days after search application received; check receipt and noon delivery advice)
- HMLR requisitions: <https://www.gov.uk/guidance/hm-land-registry-requisitions>
- HMLR PG50: <https://www.gov.uk/government/publications/requisition-and-cancellation-procedures/practice-guide-50-requisition-and-cancellation-procedures>
- SRA AI responsibility warning: <https://www.sra.org.uk/solicitors/guidance/misuse-ai/>

A statutory default is not a safe one-size-fits-all legal due date: determine transaction type, effective date, reliefs, exceptions and any transitional law at point of use. Contract notices have no universal period. For lender dates check live instructions, submission acceptance date and business-hour cut-offs. Without an explicit bank-holiday list working-day outputs are unresolved, not guessed.

## Data protection, ethics and troubleshooting

- Do not use source-control or generic logs as a live client database. Audit file hashes are *tamper-evident against accidental corruption*, not cryptographic signatures, reliable evidence of authority or encrypted storage.
- This plugin must be authorised by the firm and copyright owner for its actual use; the existing licence requires separate permission for commercial uses.
- If document parsing fails, check file type, encryption, size and readable text. Scans must be visually reviewed or handled through separately authorised OCR; do not treat blank extracted text as an empty form.
- If a lender does not appear, the directory is only a research aid; check current lender direct instructions, correct legal entity and mortgage product. Never import a related bank's form.
- Where no approved local runtime is available in ChatGPT, the skill can produce a supervised in-chat evidence table and drafts but **cannot claim it has run the CLI or persisted a case**.
- Do not publish sensitive report files; store outputs only inside the firm’s approved matter system. Users are responsible for completing and confirming all external actions.

See `docs/INTEGRATION_CONTROLS.md` and `docs/ACCESSIBILITY.md` for the next deployment controls.
