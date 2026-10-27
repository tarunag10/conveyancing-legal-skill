# Contributing to the Conveyancing Legal Skill

The project provides professional support tooling, not unattended legal advice. New features are useful only if they preserve an evidence audit and distinguish legal requirements, lender conditions, guidance and recommended practice.

## Making a change

1. Open a GitHub issue describing the document/rule/form, the authoritative source, effective date, territorial extent and affected workflows.
2. Attach or link relevant authoritative material. Never commit privileged matter files or copyright-restricted form content.
3. For a substantive change, add a legal reviewer sign-off field and tests including a negative or counterexample case.
4. Run `python -m unittest discover -s tests -v` and `conveyancing validate` from an installed editable checkout.
5. Update `knowledge/legislation/source-index.json` or `rules.json`, `docs/SOURCE_VERIFICATION_REPORT.md`, the relevant workflow, `CHANGELOG.md` and the review-by date for fiscal schedules if appropriate.
6. Request independent professional legal approval and a separate technical/code review before release. Avoid silently overwriting previously recorded historical propositions.

`tools/seed_sources_forms.py` and `tools/seed_workflows.py` generate the **initial** curated reference datasets. Re-running them will overwrite the corresponding JSON registries: do so only on a controlled branch with a reviewed diff. Do not run the seeding scripts on real matter files.

## Proposed private GitHub workflow

Create a **private** repository, review its public licensing and client-data policy, then import the files. Only the repository owner can give permission to push or deploy. To upload manually after review:

```bash
git remote add origin git@github.com:YOUR_ORGANISATION/YOUR_PRIVATE_REPO.git
git push -u origin main
```

No remote has been configured by the supplied package.
