# Legal change monitoring and release controls

**Owner:** property practice legal-editor; **technical owner:** source/CI maintainer; **approver:** designated qualified conveyancer. Source checks are NOT legal approvals.

## Sources and cadence

- Daily/manual when an active matter requires it: official legislation, actual lender instructions, HMLR prescribed form/current application guide, tax rates and rules.
- Suggested scheduled watch: weekly official source pages for legislation, HMLR collections, HMRC/WRA, SRA, UK Finance, Companies House, building safety and forms. Website hashes detect possible alterations but cannot alone establish a legal change.
- Following a Budget or announced reform: targeted monitoring with documented commencement dates, transitional rules, territorial application and statutory instruments.
- Subscriptions to official notifications and a human legal-news review are recommended. No monitoring is assumed active until configured.

## Four-stage promotion gate

1. **Detect:** run `conveyancing source-watch --allow-network --output audit.json`. Save the old/new URL, retrieval date and ETag/hash; log in a legal-change issue. Pages may change for cosmetic reasons.
2. **Research and interpret:** inspect actual amended provision, commencement and saving law, geographic scope, HMLR practice guide wording, authority hierarchy and affected workflows/forms/calculators. Record when law came into force, not merely publication/Royal Assent. Mark as `awaiting_legal_review`.
3. **Approve:** legal reviewer confirms binding/guidance/lender/contractual status, effective and transitional dates, cross-references, test cases, rate schedules, application to in-flight matters and copyright. Record reviewer name, date, source and materiality in PR; **do not automatically write to canonical rules**.
4. **Publish:** bump package version and `CHANGELOG.md`, record superseded historical entries without destroying them, run Python tests and cross-platform smoke tests, and make a signed, peer-reviewed release. Notify users of breaking changes.

## Special change types

- Land Registry form edits: download genuinely official current form, record filename, published date, SHA256, guidance and whether old editions accepted; do not redistribute restricted binaries.
- SDLT/LTT: confirm actual effective date, chargeable consideration, special rates and user jurisdiction. Snapshot must be dated with expiry/review-by and tests recalculated against government examples. No implicit rate rollover.
- UK Finance Handbook: record lender name, handbook platform/edition and relevant Part 1/2/3 section reference and date. Lender-specific terms are **not** republished here unless licensing permits.
- Cases/judgments: establish official citation, court, precedential status, pending appeal, geographical scope and relevance before adding to rules; do not invent holdings.
- Leasehold reforms: distinguish provisions enacted, commenced, scheduled, repealed or stayed; carry transitional cases separately.

## GitHub Actions

- `.github/workflows/checks.yml`: proposed CI; runs on push / PR **only after it exists in the remote repository**.
- `.github/workflows/source-watch.yml`: proposed weekly check with `workflow_dispatch`; reports informational output/artifacts and flags changes; cannot merge anything or approve legal changes.
- Keep the watcher read-only. Never give it client materials or repository write tokens.
- Browser/network access to primary-source sites must comply with publisher terms and reasonable request limits. For blocks, manual verification is the correct fallback.

## Incident response

If a source is found stale or a calculator wrong, mark the rule `suspended`, disable the affected feature, add a failing regression case, investigate all released decisions depending on it, have solicitor review impact on active matters and release a corrected version with dated note. Never silently replace the old legal position.

## Persistent technical snapshot in GitHub Actions

The proposed `source-watch.yml` restores the latest cached public URL SHA256 fingerprints, compares them against current publisher pages, emits a complete JSON artifact and fails the job if changed page contents require legal review. It saves the next **technical** fingerprints after a successful or changed run; this is never approval or silent rewriting of legal propositions. On a first run the baseline is `{}` and no comparison is possible until the following run. Failures to fetch retain the previous fingerprint. Cache expiration or eviction can reset detection continuity, so review the artifact and retain audit records in approved storage. CI alert delivery depends on the GitHub account's Actions notification configuration; nothing has been enabled remotely.
