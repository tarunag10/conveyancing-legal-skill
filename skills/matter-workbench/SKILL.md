---
name: matter-workbench
description: Use for end-to-end England and Wales conveyancing matter setup, document comparison, lender-condition tracking, title/security and execution preflight, auction/deadline management, completion figures, correspondence drafts, Land Registry registration checks and post-completion work.
---

# Conveyancing matter workbench (solicitor-supervised)

First load the **controlling canonical skill** at `../../SKILL.md`, its `core/` operating standards, `../../knowledge/workflows/ROUTER.md` and `../../knowledge/practice/MATTER_WORKBENCH.md`. Only load other practice modules relevant to the case. Read `../../docs/MATTER_WORKBENCH.md` for actual local commands, data layout, evidence requirements and installation limits. This skill augments, never supersedes, existing lender directory, gift-deeds, title and completion workflows.

## Workflow

1. Classify jurisdiction, buyer/seller/borrower/lender roles, title estate(s), transaction, contractual deadlines and source documents. Ask only for genuinely missing **essential** information. Do not guess missing dates or lender instructions.
2. Create or load a **pseudonymous** matter record from approved private storage. NEVER commit client names, bank details, lender login credentials or privileged files to the skill package, GitHub, AI demonstrations or a public issue. For an in-chat review without a runtime, use a temporary evidence table linked to attached documents; do not claim a persisted case exists.
3. Register documents with `document_id`, document revision, source and a page/entry/paragraph locator. Extract document fields as **unverified candidates**, not accepted facts. Compare evidence from multiple documents; present contradictions visibly. A false match between individuals, companies, charged assets or legal estates is a high-priority issue.
4. Separate lender condition **text**, required evidence, source offer/Part 2/Part 3 reference, status, written waiver, role and funding gate. Use existing `knowledge/lenders/lender-directory.json` as a **dated research snapshot** only. Live case offer and lender directions control CoT, RoT, eCoT, drawdown notices, additional property security and consents. Escalate undisclosed lender issues; never certify title or treat an outgoing report as accepted lender waiver.
5. For multiple properties map each legal owner, title, mortgage instrument, existing lender, intended rank, restrictions, consent, priority arrangement and company security. A TR1 for a purchase is **not** automatically required for charging an existing property; the charge instrument is separate. The algorithm can flag evidence gaps, not establish effective priority.
6. For auction/leasehold/unregistered/company/bridging/building-safety/tenancy/probate/commercial triggers, use specialised review prompts, actual original documents and applicable current law. Do not import generic auction notice terms or tenancy assumptions.
7. Calculate provisional dates ONLY from evidenced triggering events; distinguish calendar, business and working days, jurisdiction, bank holidays, lender cut-offs and statutory exceptions. Keep **original contractual completion** and **agreed extensions** separately. SDLT, LTT and MR01 periods must be checked against actual transactions and current authoritative sources.
8. Reconcile financial figures with exact decimal arithmetic and identify missing/contradictory money sources. This cannot certify bank-account ownership, cleared funds or authorise a transfer.
9. Draft enquiry letters, lender reports, CoT routing requests, chasers and client updates from traceable issues. Leave blanks for unknowns and actual signatures; show the **DRAFT NOT SENT** status. Use real prescribed or authorised source documents for registered forms; never invent a lender certificate or execute a deed.
10. Run registration/execution preflight: deeds and signatory authority, HMLR AP1/FR1/transfer details, restrictions/consents, tax certificate, priority, filing fee and pending requisitions. Track actual HMLR response and registration separately.
11. Produce evidence-linked issues and actions with owner, real deadline and solicitor-review status; optionally export CSV/JSON for MANUAL case-management handoff or an offline accessible HTML dashboard. The package does not itself connect to Outlook, OneDrive, case software, lender portals or HM Land Registry.
12. End with factual status, disputed facts, legal/blocker findings, required lender decisions, proposed drafts, case deadlines, outstanding evidence and **pending human sign-off**. An empty checklist or a reassuring output is never an authority to certify, exchange, complete, register or send funds.

## Tooling

When the user's environment offers the plugin files and a permitted Python runtime, use `conveyancing-workbench` or `python -m conveyancing_skill.workbench`. Start with `--help`. Commands include `init`, `add-document`, `add-observation`, `update-data`, `review`, `compare`, `lender`, `deadlines`, `accounting`, `draft`, `report-md`, `dashboard`, `handoff`, `post-completion`, `requisitions`, `form-preflight`, `security-map`, `audit` and `validate`.

If command execution or approved private storage is missing in the host, do not claim it ran, saved, sent, verified, or scheduled anything. Offer the in-chat assessment/draft, source-linked issue list and an importable local work record instead. A signed deed or CoT cannot be generated from a checklist.

**Security and legal scope:** local audit hashes detect accidental edits, not deliberate tampering or attorney approval. This package provides **no encryption, firm access control, statutory rule auto-updates, verified lender portal integration or submission API**. Firm policy, the actual licence, current law and human supervision remain mandatory.
