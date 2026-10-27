# Practical matter workflow

This workflow shows how to use the current CLI as a supervised evidence organiser. It does not provide legal sign-off or replace a firm's case-management system.

## 1. Establish authority and a safe workspace

- Obtain written permission for the intended use under `LICENSE`; paid client work needs separate written commercial permission.
- Use only a firm-approved workspace and AI platform for live matter information. Do not place live client data in this public repository, examples, Git history, issues, or CI logs.
- Create a pseudonymous matter ID. Keep the mapping to the client identity in the firm's case-management system.

## 2. Choose the scope and collect evidence

From an installed project environment, list profiles with `conveyancing workflow --list`, then inspect a relevant one, for example `conveyancing workflow registered-freehold-purchase`. The workflow's stages start outstanding; they are a checklist, not proof that work is done.

Copy `templates/matter-intake.template.json` into the private matter workspace. Record each document once in `documents` with a stable `document_id`, type, title/address where relevant, and a locator such as `official copy register, Charges Register, entry C2, page 3`. In issue records (`charges`, `restrictions`, `access`, and `lender_requirements`), use the same document ID and a precise page/clause locator. Record assertions as assertions; do not turn them into verified facts.

## 3. Record lender conditions separately

Use `templates/LENDER_CONDITION_CHECKLIST.md` to transcribe each condition from the actual live mortgage offer, applicable UK Finance Handbook provisions and any bespoke instructions. Record the source version/date and exact part/paragraph, the evidence required, trigger/deadline, owner, and status. Do not copy password-protected or licensed lender material into this repository. Keyword extraction with `conveyancing lender-checklist` is only a candidate finder and cannot show completeness or satisfy a condition.

## 4. Run the structured review

Save the completed JSON somewhere outside the repository, then run:

```bash
conveyancing validate
conveyancing review /private/approved/path/matter.json
```

The output identifies issues and blockers using the facts entered. When `evidence_document_id` and `evidence_locator` are supplied, the issue output points back to the document and location. Check those references against the original document. The CLI does not authenticate evidence, interpret plans, determine legal effect, or decide readiness.

## 5. Review, draft, and control actions

The conveyancer checks current primary law, commencement and transitional rules, actual forms, lender terms, and firm policy. Resolve or escalate each issue, record enquiries and responses in the firm's matter system, and use the original text templates only for drafts. A qualified conveyancer reviews all findings and drafts and remains responsible for title opinion, lender reporting, exchange/contract decisions, completion funds, filing, and external communications. This repository provides no automatic clearance or action authorisation.

## Practical limitations

- The intake template is not a secure matter database; it contains no encryption, access control, audit retention, or case-management integration.
- Document extraction is text-only unless a separately approved OCR workflow is supplied. It does not verify signatures, execution, plan scale, boundaries, or authenticity.
- The legal source registry is dated research, not assurance of current law at the matter's effective date.
- An empty issue list or blocker list does not certify title or establish readiness to exchange or complete.
