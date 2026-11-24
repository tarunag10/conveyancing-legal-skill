# Transaction router

Load the profile in `knowledge/workflows/profiles.json` matching the matter type, combined with the mandatory stage engine in `stages.json`. The CLI can render the combined workflow. Do not infer that a stage passed because it appears in a checklist.

| Trigger | Read |
|---|---|
| Full matter review, evidence record, document comparison, lender-condition tracking, security mapping, deadlines, completion accounting, preflight or dashboard | `knowledge/practice/MATTER_WORKBENCH.md`, `skills/matter-workbench/SKILL.md`, `docs/MATTER_WORKBENCH.md` |
| Buyer/seller pack, lease/management pack, auction or facility review | `knowledge/practice/MATTER_PACKS.md` |
| **Draft or amend a new commercial lease, rent deposit deed, or LTA 1954 contracting-out notice/declaration from Heads of Terms and a supplied precedent; produce complete editable DOCX documents and a correct contents/schedules map** | **`skills/commercial-lease-drafting/SKILL.md`, `docs/COMMERCIAL_LEASE_DRAFTING.md`, `knowledge/practice/COMMERCIAL_AND_TAX.md`, and the appropriate complete `templates/*_MASTER.docx` only after reading actual matter documents** |
| Register, charges, right of way, title plans, defects | `knowledge/practice/TITLE_REGISTERED.md` |
| Epitome, root, Land Charges, old mortgage, FR1 | `knowledge/practice/TITLE_UNREGISTERED.md` |
| Auction legal pack, special conditions, notice to complete | `knowledge/practice/AUCTIONS.md` |
| UK Finance / lender letter, company borrower, guarantee, ILA | `knowledge/practice/LENDERS_AND_ILA.md` |
| Lender Certificate of Title, eCoT, Report on Title, lender conveyancer contacts, LMS/Lender Exchange/Smoove or funding notice | `knowledge/practice/LENDERS_AND_ILA.md` + `knowledge/lenders/README.md` + `knowledge/lenders/lender-directory.json` + `templates/LENDER_COT_ROUTING_AND_SUBMISSION_CHECKLIST.md` |
| Leaseholds, LPE1, management pack, BSA, enfranchisement | `knowledge/practice/LEASEHOLD_AND_BUILDING_SAFETY.md` |
| VAT, option to tax, SDLT/LTT, commercial tenure | `knowledge/practice/COMMERCIAL_AND_TAX.md` |
| **Landlord and Tenant Act 1954 contracting out**: new business lease/underlease/agreement for lease with excluded security of tenure; s38A warning notice, simple declaration, statutory declaration, 14-day deadline, contracting-out lease clause or preflight | **`skills/lt1954-contracting-out/SKILL.md` + `knowledge/practice/LTA1954_CONTRACTING_OUT.md` + `templates/lta1954/TEMPLATE_INDEX.md`**; for a full commercial lease also `knowledge/practice/COMMERCIAL_AND_TAX.md` and `skills/commercial-lease-drafting/SKILL.md` |
| **Landlord and Tenant Act 1954 protected renewal or ending**: section 25 notice, section 26 request, section 27 tenant notice, section 29A/29B proceedings or deadline extension, section 40 information request; 2004 SI Forms 1–17 | `skills/business-tenancy-notices/SKILL.md`, `knowledge/practice/BUSINESS_TENANCY_NOTICES.md`, `templates/notices/business/OFFICIAL_FORMS_1_TO_17.json`, live SI 2004/1005 and GOV.UK guidance |
| **Agreement to surrender a protected business tenancy under 2003 Order**: Schedule 3 warning and Schedule 4 declaration | `skills/business-tenancy-notices/SKILL.md`, `templates/lta1954/SURRENDER_WORKFLOW.md`, the separate Schedule 3/4 templates; NEVER reuse the grant Schedule 1 notice |
| **Conveyancing search request/result/adverse review**: OS1, OS2, OS3, SIM, OC1, OC2, K15/K16, LLC1, CON29/CON29O, environment, water/drainage, highways | `skills/conveyancing-searches/SKILL.md`, `knowledge/practice/SEARCHES_AND_RESULTS.md`, `templates/searches/SEARCH_ROUTING_CATALOGUE.json` and the official provider's current forms |
| **Leasehold notices and consents**: notice of transfer or charge, landlord or managing-agent requests, licence to assign/alter, certificate of compliance | `skills/leasehold-notices/SKILL.md`, `knowledge/practice/LEASEHOLD_NOTICE_DRAFTING.md`, `templates/notices/leasehold/` |
| **Commercial contractual or statutory termination and enforcement**: section 27, section 29B extension, break, rent review, notice to complete, section 146 forfeiture | `skills/lease-enforcement-notices/SKILL.md`, `knowledge/practice/LEASE_ENFORCEMENT_NOTICES.md`, `templates/notices/enforcement/`; section 146 is a preflight worksheet only |
| **Residential England tenancy notices**: post-1-May-2026 private-sector official Form 3A possession, Form 4A rent increase, LTA 1987 sections 47 and 48 | `skills/residential-tenancy-notices/SKILL.md`, `knowledge/practice/RESIDENTIAL_NOTICE_ROUTING.md`, `templates/notices/residential/READ_ME_FIRST.md`; choose England/Wales, private/social, transitional before drafting |
| Completion funds, undertakings, redemption, notices | `knowledge/practice/COMPLETION.md` |
| Rejected/late company charge, s859F application | `knowledge/practice/COMPANY_CHARGE_REMEDIES.md` |
| Declarations, statements of truth, gifts, family or bridging loans | `knowledge/practice/EVIDENCE_GIFTS_AND_LOANS.md` |
| Form AP1/FR1/TR1/TP1, company charge filings | `knowledge/practice/REGISTRATION.md` |
| New build, shared ownership, overseas owner, probate, trusts | `knowledge/practice/DEVELOPMENT_AND_SPECIAL.md` |

The generic stages apply to **every** matter, but can be marked not applicable only with recorded rationale and legal review. For a lender-only matter, check third-party borrower solicitor instructions and the UK Finance Part 3 if incorporated into that lender's instructions.

For document applicability use `knowledge/workflows/DOCUMENT_MATRIX.md`; for matter evidence, decisions and registration tracking use `templates/MATTER_REVIEW_RECORD.md`. For prescribed form triage use `knowledge/forms/PRIORITY_FORMS.md` and the live official source. For source review use `templates/SOURCE_REVIEW_RECORD.md`.

**Important:** The Schedule 1 / Schedule 2 contracting-out procedure applies to a proposed **grant**. An **agreement to surrender** an existing business tenancy uses the separate Schedule 3 / Schedule 4 procedure and must not receive the grant notice by mistake. A new lease's contracting-out clause is no substitute for completing its notice and declaration before the tenant is bound. Forms 1–17 of SI 2004/1005 are for protected business tenancy notices, not new-grant contracting-out, and the bundled preparation worksheets are never substitutes for prescribed forms.
