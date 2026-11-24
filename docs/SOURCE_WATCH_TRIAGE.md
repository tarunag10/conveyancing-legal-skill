# Public legal source watch: operations and approval controls

**Checked implementation:** 24 November 2026. This is an automated *technical* publication monitor; it is not an automated legal editor or a legal opinion.

## How the monitor works

1. Every Monday at **06:17 UTC** GitHub Actions runs `source-watch` on the default branch. GitHub schedules are best effort and can start late. `workflow_dispatch` enables manual runs. Relevant monitoring source changes pushed to `main` also trigger a check.
2. The monitor reads the allowlisted public URL records in `knowledge/legislation/source-index.json`. It prefers the GOV.UK public Content API and, where available, legislation.gov.uk XML. It excludes common site navigation and script noise from HTML fallbacks. It checks up to 60 monitored sources without uploading client data.
3. Each source is recorded as a baseline, unchanged, changed, an older raw-HTML baseline migrated to the new strategy, an incompatible source representation, or access/fetch failure.
4. A legitimate changed semantic fingerprint creates **one open GitHub review issue per source**, with evidence, original URL, comparison metadata and mandatory review steps. Source access restrictions (HTTP 401/403) generate a separate manual-access issue. Later observations update rather than create duplicates.
5. The `public-source-status` workflow artifact retains source observations, technical fingerprints, access failures and the review queue. New technical fingerprints move forward to avoid the same observation triggering endless alerts. **Changing a fingerprint is not approving a rule.**
6. No task edits legal rules, prescribes notice text, replaces forms, or updates a legal verification date automatically. A qualified professional must independently compare the primary authority, amendments, commencement, territorial application and actual document revisions and approve any proposed change.

## Historical noisy results (2–23 November 2026)

The first run established a raw-byte baseline; the next three runs flagged 44–46 broad HTML differences. These were not proven amendments. They remain historical alerts requiring triage. The new content-strategy migration marks prior raw hashes as `legacy_baseline_migrated`; it does **not** silently represent those historic alerts as resolved. Keep the historical review issue open until independently assessed.

## Blocked publisher pages

Law Society TA forms pages and UK Finance Handbook pages have returned HTTP 403. **Do not bypass technical restrictions, spoof credentials, or claim monitoring coverage for those sites.** The workflow records `access_restricted` and opens a distinct review issue. A practitioner must check the official publisher using permitted firm access and document the current version and findings. An inaccessible page is not a legal change or proof of unchanged law.

## Reviewer decision steps

For each open `Legal source review` issue:

- Identify a substantive, dated publisher change or record **no legal change** (site-only update).
- Establish current law, start date, transitional provisions, geographical extent, and any affected cases.
- Record direct authoritative evidence (official notice/document version), and review the current repository rule/form/template.
- Have a qualified solicitor approve a specific version-controlled change. Use a pull request with tests and record it in the source verification report, current `rules.json` / `source-index.json` and change log only to the extent justified.
- After the approved GitHub change, verify publication and explicitly sync with the ChatGPT plugin through the normal Plugin Creator update; a GitHub push alone does not update ChatGPT.
- Close the GitHub issue only after a reviewer records a decision. Do not silently close on a subsequent successful fingerprint scan.

## Distinguishing failure states

| Result | Meaning | Action |
|---|---|---|
| `first_baseline` | First usable publication fingerprint; no comparison | No legal conclusion |
| `legacy_baseline_migrated` | Previous v1 raw-byte hash not comparable to v2 structured hash | Keep historical alerts for review; establish v2 baseline |
| `unchanged` | Same technical publication fingerprint | No proof of legally current status |
| `change_detected_review_required` | Stable publication content differs | GitHub issue and qualified legal review |
| `representation_changed` | Structured API vs HTML fallback changed | Recheck source access; don't claim law changed |
| `access_restricted` | Publisher denies automated access | Manual check via approved access |
| `fetch_failed` | Failed request/timeout/other error | Retry or manually check; not proof unchanged |

Use GitHub Actions status for operational health; an ordinary change-detection event should not make the scheduled workflow fail. A failed workflow after these changes means actual operational troubleshooting is needed (for example missing GitHub permissions or a code error). GitHub issue creation requires `issues:write` for the workflow token.
