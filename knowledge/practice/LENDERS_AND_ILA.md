# Lender compliance, bridging finance, corporate borrowers, guarantees and ILA

**Load when:** mortgage, remortgage, buy-to-let, lender-only instruction, bridging, debenture, all-monies charges, director guarantee, ILA, lender certificate or report on title.

## Handbook / instruction source gate

The UK Finance Mortgage Lenders' Handbook is voluntary. For a participating **residential** lender, identify the England and Wales Part 1, that lender's current Part 2 and, where acting for the lender but not borrower and incorporated, Part 3. The official platform was replaced in June 2026. Confirm lender name, corporate group, exact instruction version/date, offer, special conditions, updates, separate reporting process and solicitor panel status **on this matter**. Commercial and bridging lenders may use bespoke requirements; do not backfill with a guessed handbook term.

## Lender-specific Certificates of Title and Reports on Title (added 20 November 2026)

**When the question is about which CoT/RoT form to obtain, where to download it, how to submit it, panel case access, the lender's completion/drawdown notice or who to contact:** read `knowledge/lenders/README.md`, look up the exact lender/brand in `knowledge/lenders/lender-directory.json`, and use `templates/LENDER_COT_ROUTING_AND_SUBMISSION_CHECKLIST.md` for the matter. The specialist `skills/lender-certificates/SKILL.md` supplies the output format. The directory is a **dated, non-exhaustive public-source snapshot** and does not override mortgage offer conditions, current UK Finance Part 2, Part 3, or a lender's bespoke instructions. A live lender case is authoritative over a public lender document listing.

Return the **exact lender and product**, appropriate RoT/CoT/eCoT, form source URL, case portal and accepted submission method **only where verified**, timing and unit, contact(s) by purpose, source and checked date, relevant matter/representation exceptions, and unresolved access/conditions. Distinguish confirmed delivery instructions from an LMS document/panel listing. If only the document or portal is public, label the submission route **UNVERIFIED** and give a lender enquiry route, never assert an eCoT exists on a case. A static lender-branded CoT is not an editable free-form generic certificate. Do not reproduce Law Society or proprietary forms without permission. Never sign/certify/send or trigger release of funds without appropriate qualified human instruction and tools.

Important brand distinctions: Rely ≠ Kent Reliance even where related; Barclays Bank UK residential ≠ Barclays Business/Commercial; HSBC UK ≠ HSBC Private Bank ≠ first direct; NatWest residential ≠ NatWest Group commercial; Halifax ≠ Lloyds; Molo / ColCap and Monmouthshire MBS-prefix forms require product/entity checking. Together's lender-solicitor **Report on Title** may be prepared by lender's appointed solicitor after a separate borrower-solicitor title pack, whereas residential eCoT is often submitted by jointly acting solicitor; establish each retainer and facility instruction. Additional security may involve multiple charges and lender approvals, but **does not automatically entail two TR1s or two CoTs**. Record separate charged properties, existing charges and consents and follow lender's precise certification requirements.

## Requirement extraction schema

For each requirement record: `id`, `source_file`, `page_or_clause`, `exact_or_short_paraphrase`, `lender`, `role`, `legal_or_contractual`, `deadline`, `supporting_evidence`, `responsible_party`, `status` (`outstanding`, `evidence_received`, `verified`, `waived_by_lender`, `not_applicable`), `blocking` and `reportability`. Only the actual lender or instructed conveyancer may authorise waiver.

## Priority risk checklist

- **Title:** correct borrower and charged estate, title restrictions and consents, class of title, third-party interests, property access, adopted roads, restrictive covenants and indemnity insurer/lender acceptance.
- **Security:** charge ranking, prior mortgages/all-monies/further advances, redemption arrangements, DS1/e-DS1, additional lender/debenture, deed of priority/consent/waiver, HMLR registration. Check Companies House MR01 clock for charge created by UK company/LLP where applicable.
- **Property:** purchase or refinancing value/use, tenancies and occupiers, HMO/licensing, buildings insurance policy sum/interests/inception, warranties/EWS1/BSA documentation (if triggered), searches and environmental risk.
- **Borrower:** company existence, directors' powers, articles/constitution, board approvals, beneficial owners, gift or deposit chain, AML/sanctions, insolvency/undervalue risks, corporate support, guarantees and ability to service debt.
- **Finance:** drawdown notice period, condition precedent, retainers and dual representation rules, interest accrual, arrangement fees, exit date, lender report/Certificate of Title approval, whether funds cleared and allocated.

## Independent legal advice (ILA) and personal guarantees

First establish WHO the solicitor represents and what the lender requires: guarantor, director, company, borrower, or combinations. Check conflict and independence, interpreter/accessibility needs, capacity, conflict-free advice environment and scope of retainer. Do not use another party's solicitor as guarantor's independent adviser if independence is compromised.

Explain the facility amount and obligations, nature of primary debt vs guarantee vs **indemnity**, whether capped or all-monies, continuing security, joint/several liability, demand triggers, notice/waiver clauses, lender's freedom to vary facility, repayment on default, right of recourse, risk to personal assets and possible insolvency. Work from actual agreement and identify exact clause numbers, NEVER generic unverified clauses. Independently ask whether advice understood and freely accepted, not from borrower assurances. Ask for relevant financial information and urge financial/tax advice where necessary. Document advice dates, method, identification, exact contract version, witness presence and client questions.

Use lender-approved certificate wording without unapproved changes. Prepare an ILA attendance note and certificate **only after actual advice and witnessed signature have taken place**, signed by authorised adviser. AI cannot attest that advice was given or signature witnessed. Do not pre-date or pre-certify; keep letterhead editable if provided.

## Lender reports and sign-off

If an adverse issue might require reporting, produce a careful neutral draft specifying matter, title, lender instruction clause, evidenced problem, probable implication, cure proposals and **request for lender consent/waiver**. Do not assert lender approval because solicitor sent a report. Mark Completion Blocker until required written decision/condition evidence is on file.

**Borrower vs lender:** client commercial preferences do not override lender conflict/disclosure duties. Separate reports to client and lender by instructions and confidentiality boundaries; if unable to reconcile duties escalate before exchange or drawdown.

## Integrated workbench check (added v0.2.0)

For a live lender-funded matter, read `knowledge/practice/MATTER_WORKBENCH.md` to link each condition, actual source file + page, security parcel, expected rank, outstanding consent, human reviewer, real lender decision and drawdown cut-off to the case-specific record. The offline workbench can use the dated directory for research, but **cannot log into LMS, submit CoT/RoT, request funds or confirm lender receipt**. A second-charge or third-party-security property requires its own charge instrument and evidence; do not conflate it with a purchase TR1.
