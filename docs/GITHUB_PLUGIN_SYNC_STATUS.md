# ChatGPT Plugin to GitHub Sync Status (24 November 2026)

This repository update compares the user's original GitHub repository with the **EW Conveyancing Legal** ChatGPT plugin v0.4.2, release `pluginrel_6b0609ffca1c819184f0b5fbfc8eedff`. The ChatGPT plugin is the primary source for the new conveyancing skills and notices. GitHub-only CI, community, setup and examples files are preserved rather than deleted.

## Transferred into the proposed GitHub commit

- 187 plugin source files (Markdown, JSON, Python and plugin configuration), including new skills for LTA 1954 notices, property searches, commercial leasehold notices, enforcement and residential notices.
- 58 byte-verified neutral DOCX files covering prescribed-form preparation worksheets, Schedule 1/2/3/4 notices and declarations, search request/review sheets, leasehold notices, enforcement forms and residential forms. The source-to-export base64 decoding was independently checked against SHA-256 digests for each file.
- The plugin manifest and the compatible .codex-plugin metadata, set to v0.4.2.

## Outstanding binary master templates (7 files)

The ChatGPT Plugin Creator read interface does not return binary file contents, and a full byte-for-byte archive could not be materialised in this session. These **seven master DOCX files remain in the ChatGPT plugin but are not included in this GitHub sync**:

1. `skills/commercial-lease-drafting/assets/COMMERCIAL_LEASE_MASTER.docx`
2. `skills/commercial-lease-drafting/assets/RENT_DEPOSIT_DEED_MASTER.docx`
3. `skills/commercial-lease-drafting/assets/STATUTORY_DECLARATION_1954_MASTER.docx`
4. `templates/COMMERCIAL_LEASE_MASTER.docx`
5. `templates/DEED_OF_GIFT_TEMPLATE.docx`
6. `templates/RENT_DEPOSIT_DEED_MASTER.docx`
7. `templates/STATUTORY_DECLARATION_1954_MASTER.docx`

These should be copied from a verified full export of the plugin, retaining the original binary bytes and screening them for confidential client information, before this PR is merged. **The commercial-lease master regression tests will fail until the files are added.** Do not replace the missing documents with dummy or incomplete drafts.

## Safety and status

The plugin’s prescribed-form preparation worksheets are **not substitutes for official statutory forms** and must not be served as statutory notices. Current rules, individual facts and service deadlines require verification at point of use. This update does not certify any legal instrument.

This is a source synchronisation candidate, not a completed identical mirror or a completed legal matter.
