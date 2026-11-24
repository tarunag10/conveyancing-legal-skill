---
name: legal-source-watch
description: Use when checking, fixing, interpreting, or responding to scheduled England and Wales legal source monitoring, GitHub source-watch runs, publication changes, form revisions, outdated legislative guidance, or review queue issues.
---

# Legal source monitoring: qualified-review workflow

**First read** `../../docs/SOURCE_WATCH_TRIAGE.md`, `../../docs/SOURCE_ACCESS_EXCEPTIONS.md`, `../../core/SOURCE_POLICY.md`, and relevant source-index, rule records and actual run evidence. In GitHub also inspect `.github/workflows/source-watch.yml`, `src/conveyancing_skill/source_watch.py` and `tools/legal_source_review.py`.

The workflow detects **technical changes to primary-source publications**, not legal change or legal approval. Its source categories include GOV.UK Content API, legislation.gov.uk XML and stable accessible publisher content. Do not treat a content hash difference as a changed statute, regulator rule, lending instruction, or prescribed form. Do not treat HTTP 403 as successful verification.

## When user asks about alerts, legal updates or the schedule

1. Verify the **actual GitHub Actions run history**, runtime, technical status, logs, artifacts and distinct source observations. A valid weekly schedule alone does not prove a scan took place. Scheduled runs may be delayed or dropped.
2. Read the actual source-watch JSON report for source IDs, access failures, baseline migration, representation switch, changed content and the separate legal-review queue. Distinguish scan status from review/approval status.
3. For each substantive candidate, independently fetch the official publication/change history, pinpoint the section/form edition, verify jurisdiction, effective commencement and transitional position, identify affected module(s) and provide documentary evidence.
4. Record manual solicitor approval, versioned tested changes, source verification metadata and an issue resolution. Only then update laws/forms/reference material. Approval cannot be inferred from a job succeeding.
5. GitHub issues are deduplicated per source ID and issue kind. Do not create 46 new issues merely because a legacy raw HTML hash changed. Historical alerts need a human-reviewed triage record.
6. Verify ChatGPT plugin release separately after GitHub changes. GitHub push never automatically edits the installed plugin. Never push client data, unpublished instructions, signed declarations, lender credentials or legal case papers into a public repository.
7. Report exact state: *scheduled*, *ran*, *source fetched*, *candidate change*, *review pending*, *approved*, *rule/template updated*, and *plugin published* are distinct milestones.

**Manual access:** For Law Society and UK Finance pages returning 403, obtain approved access or current official updates by other authorised publisher means. No scraping bypasses or unlicensed forms.

**Safety:** No automatic legal approval, execution of deeds, filings, lender certification, publishing to a shared audience or financial transactions.
