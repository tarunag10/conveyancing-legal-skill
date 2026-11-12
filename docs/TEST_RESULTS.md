# Current release validation: 0.1.6

9 November 2026: 58 unittest methods passed, including the existing 48 tests with newly supplied synthetic inputs and 10 regression tests. Registry validation passed: 98 forms, 51 sources, 33 rules, 28 profiles, 15 stages. Reference-bundle wheel build and isolated installation validation passed. These checks do not validate legal propositions, current lender instructions, prescribed form binaries, rendered Word layout or fresh-host behaviour. No new formal accessibility certification is claimed.

The original installed 0.1.5 package failed with 2 test failures and 19 errors due to absent adapter/example/fixture files. The older report below is preserved as historical build information and was not reproducible from that installed package.

# Build and validation record

**Research baseline and validation date:** 27 October 2026.

## What was executed

- `python -m compileall -q src tests tools`: passed.
- `python -m pip install -e . --no-build-isolation --no-deps -q`: passed in the build environment.
- `conveyancing validate`: `status: PASS`, 0 errors; **one explicit scope warning** that rule opinions, signed originals, per-lender requirements and downloadable form versions are not certified by automated validation.
- `python -m unittest discover -s tests -v`: **48 tests passed**, covering fictional transaction scenarios, negative safety tests and actual CLI entry points.
- `conveyancing source-watch --limit 3 --output ...`: passed in no-network mode. Live source monitoring was **not activated**, and no background monitoring was configured.
- `conveyancing forms MR01`: returns the official Companies House charge registration entry.
- `conveyancing to-docx examples/fictional-historic-charge-report.md examples/fictional-historic-charge-report.docx`: passed; both rendered pages were manually inspected for layout.
- `python /home/oai/skills/docx/scripts/a11y_audit.py examples/fictional-historic-charge-report.docx`: completed with 0 high, 0 medium and 0 low findings.

## Scope of evidence

Tests exercise code behaviour and fictional fixtures, not the truth of original matter documents, their lawful execution, live HMLR acceptance, the state of legal commencement, source publisher availability after the baseline date, current lender-specific instructions, or actual installation in each supported AI host.

The Word example is a **fictional original report**, not an official prescribed form. No file in this project contains client funds, confidential client files, or authenticated lender certificates.

## Prerequisites for operational adoption

Before live client use, verify individual form binaries and revisions, supervise current legal research, check the applicable lender instructions, perform firm security assessment, and undertake user acceptance testing with the exact host application and its enabled tools. See `docs/VALIDATION_AND_LIMITATIONS.md` and `docs/FEATURE_INVENTORY.md`.

