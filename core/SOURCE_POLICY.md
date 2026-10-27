# Source change-control policy

`knowledge/legislation/rules.json` holds material legal rules with `verification_status`, exact reference, jurisdiction, source, effective-date status, transitional notes, legal character, applicability and a **separate** `last_verified_date`. `knowledge/legislation/source-index.json` is the monitored URL registry. `forms/catalogue.json` contains publisher-listed dates, not automatically inspected file revisions.

Source version control: online page changed != substantive law changed; Royal Assent != commencement; publication update != commencement date; court judgment != binding proposition without checking status, ratio and subsequent cases. If a publisher changes, record metadata/hash, put update in `legal-review-queue.jsonl` and obtain solicitor approval of rule changes. Maintain old record and add a new version with provenance. Only approved versions may be marked current in production.

Permitted machine status updates: check time, HTTP outcome, ETag, Last-Modified and content digest. Prohibited automated transitions: moving `unverified` to `verified`, changing legal effective dates or marking a lender requirement satisfied. Do not crawl non-public lender/third-party portals without permission. Never send client documents to monitoring endpoints.

`source-watch --allow-network` is an opt-in checker and outputs the review queue, not an updater. CI cron file is **proposed**; it does not run until GitHub Actions is enabled in an uploaded repository. `--allow-network` performs GET only for allowlisted public sources, with timeouts; network denial is recorded as a failed check, not absence of legal change.
