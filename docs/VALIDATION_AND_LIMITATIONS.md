# Validation, assurance level and outstanding legal work

**Initial research reference:** 27 October 2026. **Automated assurance:** implementation tests only, not practising solicitor approval. **Publication disposition:** working, tested core for review, not a production-certified advice engine.

## What 'verified' means in this repository

- `official_source_checked`: the publisher's publicly accessible relevant source page was reviewed at the recorded date. It does **not** mean every amendment, secondary regulation, exception or commencement was checked for all transactions.
- `checked_at_reference_date`: a specific legal proposition was supported by a page or provision at the reference date, but `legal_reviewer_approved: false` means no external solicitor has signed it off.
- `publisher_listing_checked_only`: the form or directory was observed at its publisher. The embedded form's **binary version, PDF layout, signature panel, e-signature validity and applicable fees remain unverified**.
- `edition_or_provenance_requires_verification`: even the edition requires separate provider verification. This is intentional, not a blank form.
- Historical versions and effective dates are not reliably reconstructible from an updated web page alone. Consult revised legislation *and* original commencement/transitional instruments before applying rules retrospectively.
- Tax rates are a time-limited illustration only; subsequent amendments can occur between source check and actual transaction effective date. The four basic residential tables were checked against current legislation and official guidance on 28 October 2026. A calculation date after the earlier of `last_verified_date` and `review_by` is refused; the present snapshot therefore permits dates through 28 October 2026 only. See [the tax rate verification record](TAX_RATE_VERIFICATION_2026-10-28.md). The selected standard or higher table does not determine statutory eligibility.

## Supported fully executable functions

- Read local catalogues and choose workflows, returning all 15 stages initially outstanding.
- Flag unproved historic mortgage release, unsatisfied restrictions, unverified highway status, reported document contradictions, open lender requirements and potentially applicable building-safety rules from **explicit JSON inputs**.
- Reconcile buyer-side completion inputs with `Decimal` accounting; always refuse automated funds release and maintain evidence/condition blockers unless humans attest to checks. Input is not live bank evidence.
- Calculate selected purely arithmetic due dates with explicit assumptions. No contractual notice analysis and no inferred holiday calendar.
- Calculate narrow illustrative residential SDLT/LTT band estimates with dated gates and complexity refusal.
- Extract selectable PDF/Word text with source paragraph/page pointers, identify candidate references, record empty scan pages, and warn that execution cannot be authenticated.
- Create editable **original** report Word documents, and replace explicit placeholders in a user-provided template while preserving unrelated runs and logging every change. Does not verify visual/layout fidelity or process tracked changes safely.
- Check reference integrity, duplicate IDs, mandatory fields and skill architecture; run automated fictional scenario tests.
- Network watcher, when explicitly enabled, checks **allowed public domains only** and stores byte hashes/HTTP metadata; does not determine legally material change or approve any new rule.

## Material limitations requiring solicitor/editorial review

1. **Individual prescribed forms:** most 98 listings do not yet have a verified binary download/version, complete clause/panel-by-panel guidance, execution matrix, fee, or accurate requisition statistics. The protected Law Society and CPSE forms are excluded from reproduction. Links usually lead to the official *landing page* or catalogue, not to a PDF download.
2. **Actual title evaluation:** OCR, plans, deeds, scales and boundary overlays cannot be reliably established by the text extractor. Structured JSON inputs need a careful human transcription and source citation. It cannot give an opinion on marketability or certify title.
3. **Lender obligations:** no stored lender-specific UK Finance Part 2 tables, lender password-protected material or commercial banking instructions. Each live lender agreement, COT and security demand must be separately read, sourced and checked.
4. **Completion:** no verified client account balance, lender drawdown, exchange authority, CLEARED same-day money, signed undertaking or legal authority for client transfer. Never treat `ready_to_send_funds: false` as a tool defect.
5. **Commercial/tax:** development transfers, TOGC, option to tax, special nonresident/corporate SDLT, linked consideration and Welsh LTT relief analysis require bespoke written tax assessment. Numeric estimates intentionally refuse complexity.
6. **Building safety:** English high-rise applicability, complex landlord/leaseholder certificates, remediation and mortgage acceptance require specialist document review. Wales rules and territorial application differ.
7. **Platform integrations:** local repository layout is implemented; actual installed Plugin / ChatGPT / Claude Desktop / Cursor / Gemini accounts were **not accessed or live-tested**. Do not claim publication or marketplace approval.
8. **No secure multi-tenant document repository:** no retention/access-control layer, encryption-at-rest, firm DMS integration or case-management API. Sensitive files must stay in a firm's approved environment; this repo contains fictional fixtures only.
9. **Monitoring:** GitHub Actions definitions exist but no schedule is active until separately installed/enabled in GitHub. Raw hashes may change for unrelated website layout updates. No automatic legal rule mutation.
10. **Regulatory review:** firm-specific SRA/CLC confidentiality, AML, data protection, client money and professional indemnity obligations are not delegated to the software.

## Acceptance steps before deployment on actual matters

- Obtain practising property solicitor sign-off on each referenced rule and commencement/transitional effect as of the effective transaction date.
- Verify and hash current official form files, check licensed rights and use a regression set of real (suitably anonymised) HMLR rejection examples.
- Validate each lender's live Handbook edition/instructions and signing/witnessing requirements, with a dual-control approval system.
- Security review of storage, document extraction and tool permissions, legal-privilege management and audit retention.
- Run a UAT pack on each supported host and record exact installed version, filesystem/network access, skill-discovery proof, test output and reviewer approval.
- Obtain a second reviewer for any calculation intended for commercial reliance and ensure current fee/tax tables are checked immediately before completion.
