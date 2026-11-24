# Contributing to the Conveyancing Legal Skill

The project provides professional support tooling, not unattended legal advice. New features are useful only if they preserve an evidence audit and distinguish legal requirements, lender conditions, guidance and recommended practice.

## Making a change

1. Open a GitHub issue describing the document/rule/form, the authoritative source, effective date, territorial extent and affected workflows.
2. Attach or link relevant authoritative material. Never commit privileged matter files or copyright-restricted form content.
3. For a substantive change, add a legal reviewer sign-off field and tests including a negative or counterexample case.
4. Run `python -m unittest discover -s tests -v` and `conveyancing validate` from an installed editable checkout.
5. Update `knowledge/legislation/source-index.json` or `rules.json`, `docs/SOURCE_VERIFICATION_REPORT.md`, the relevant workflow and `CHANGELOG.md`. Keep fiscal schedule check/review dates advisory; never add a date-only use cutoff.
6. Request independent professional legal approval and a separate technical/code review before release. Avoid silently overwriting previously recorded historical propositions.

`tools/seed_sources_forms.py` and `tools/seed_workflows.py` generate the **initial** curated reference datasets. Re-running them will overwrite the corresponding JSON registries: do so only on a controlled branch with a reviewed diff. Do not run the seeding scripts on real matter files.

## Existing GitHub and ChatGPT maintenance process

This repository is the public GitHub source for the **EW Conveyancing Legal** plugin. Do not create another repository for routine updates.

1. Make source changes on a topic branch, including tests and source-backed legal references.
2. Run the offline tests (`python -m unittest discover -s tests -v`) and review the GitHub Actions results.
3. Changes to official law, guidance, forms or lender instructions require **qualified professional approval** recorded in an issue and in the source verification record. A successful automated hash check is not legal approval.
4. Use `.github/workflows/source-watch.yml` and `docs/SOURCE_WATCH_TRIAGE.md` for scheduled public-source technical monitoring. Alerts are deduplicated; inaccessible publisher sites require approved manual checking.
5. Merge or fast-forward reviewed changes into `main`. Update `pyproject.toml`, the portable plugin manifest and compatibility manifest to the same SemVer before a tagged release.
6. Use Plugin Creator to publish **the same approved source** to the existing private ChatGPT plugin, and read back the release before reporting synchronization. GitHub commits alone do not update the installed plugin.
7. Keep client data, completed legal instruments, personal identifiers and lender credentials out of this public repository.

Only authorised maintainers may publish releases or change shared access. GitHub technical tests never constitute a legal sign-off.
