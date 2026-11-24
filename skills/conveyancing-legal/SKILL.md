---
name: conveyancing-legal
description: Evidence-gated conveyancing for qualified practitioners in England and Wales. Use for title, auctions, lender security, unregistered land, commercial leasing, completion statements, Land Registry forms, legal drafting, commercial leases (including LTA 1954 contracting out) and registration. Do not self-certify, sign, file or send funds.
---

# Conveyancing legal skill launcher

**Canonical, controlling instructions:** open `../../SKILL.md` (repository root `SKILL.md`), then its `core/` operating files. For all current law and lender rules check direct authoritative sources at point of use.

**Progressive disclosure:** read `knowledge/workflows/ROUTER.md`, then *only* the relevant `knowledge/practice/*.md`, form catalogue entry, actual matter source documents and applicable rule records. Every stage initially remains outstanding; no automatic funds release, legal sign-off or filing.

**LTA 1954 commercial-letting trigger:** For any instruction to **contract out** of sections 24-28, issue the landlord's warning notice, prepare a simple or statutory declaration, check 14-day timing, or draft/review a lease expressly excluding security of tenure, open `skills/lt1954-contracting-out/SKILL.md`, `knowledge/practice/LTA1954_CONTRACTING_OUT.md` and the blank Word templates indexed by `templates/lta1954/TEMPLATE_INDEX.md`. Use this workflow on a new commercial lease when its heads of terms call for contracting out. Do not assume a generic lease is excluded or confuse a new tenancy with the separate surrender procedure.

**Commercial lease and connected deeds:** for a lease drafted from Heads of Terms and an existing lease, load `skills/commercial-lease-drafting/SKILL.md`, `docs/COMMERCIAL_LEASE_DRAFTING.md` and appropriate complete DOCX masters in `templates/`. Preserve all substantive precedent clauses and schedules unless actual instructions/law require otherwise; never deliver a TOC that lists absent clauses, omit a schedule accidentally, invent parties or amounts, or put bracketed instruction placeholders inside the legal instruments. Unknown particulars must be blank write-in lines; unresolved legal choices go in a separate report. The deed set must be rendered and checked page by page before it is described as ready for solicitor review.

**Business tenancy renewal, protected termination and information notices:** use `skills/business-tenancy-notices/SKILL.md`, `knowledge/practice/BUSINESS_TENANCY_NOTICES.md`, and current official 2004 Regulations SI 2004/1005 Forms 1-17. The bundled Word Forms 1–17 are **preparation worksheets only**, never notices for service. Route surrender under 2003 Order Schedule 3/4 separately from new-grant contracting out Schedule 1/2.

**Searches, leasehold notices, enforcement and residential notices:** Load respectively `skills/conveyancing-searches/SKILL.md`, `skills/leasehold-notices/SKILL.md`, `skills/lease-enforcement-notices/SKILL.md`, or `skills/residential-tenancy-notices/SKILL.md` where the request relates to HMLR or other searches, notices of transfer/charge and landlord consents, lease breaks/section 146/notice to complete, or post-1-May-2026 England residential notices. Original official or licensed statutory forms take priority; use worksheets for source evidence and drafting preflight, not as imitation prescribed notices. Distinguish England from Wales and private from social sector.

**Lender CoT/RoT questions:** consult `knowledge/lenders/README.md` and `knowledge/lenders/lender-directory.json` after `knowledge/practice/LENDERS_AND_ILA.md`; the separate `skills/lender-certificates/SKILL.md` gives the lender-specific lookup workflow. The research directory is dated, non-exhaustive and never a substitute for live lender instruction, panel/case verification or solicitor approval. Use the official lender form/portal, not a guessed generic CoT.

For a 15-stage workflow, return a stage record for every applicable stage with status, expected deliverables, evidence references, findings, open actions (owner and actual deadline when known), conditional-task applicability/rationale, client instructions, lender reports/decisions, and human reviewer/decision. Apply each stage's review prompts and escalation triggers. Leave unknown fields empty and keep unsupported work outstanding or pending. Link findings to document IDs and page/clause locators. Never infer completion, approval, or satisfaction from a blank field.

If the root is not available (for example a standalone installed folder), tell the user the skill is incompletely installed and ask that the whole repository or an accessible copy of canonical core and modules be connected. Do not replace unavailable legal modules with remembered rules.
