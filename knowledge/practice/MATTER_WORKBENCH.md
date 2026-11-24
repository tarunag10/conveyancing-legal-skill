# Evidence-led conveyancing matter workbench

**Load when:** user requests end-to-end matter processing, automated matter facts, document version comparison, lender condition tracker, security/charge map, deed execution checks, auction/extension monitoring, registration preflight, deadline calendar, post-completion progress or legal correspondence based on uploaded records.

Use the controlling `core/OPERATING_STANDARD.md` and `core/EVIDENCE_AND_RISK.md`. For legal details, load the relevant specific module. This is a supplemental practice/workflow layer, not a duplicate source of legal rules.

## Evidence hierarchy and anti-invention rules

- **Machine-observed candidate:** extracted from a document, not verified. It must retain document ID and page/paragraph locator. Never call it approved or confirmed.
- **Documented:** reviewed original/source material, still subject to legal interpretation.
- **Corroborated:** independent authoritative evidence matches the matter, scope and date. Distinguish it from verbal assertions or matching OCR.
- **Lawyer-approved:** requires actual competent reviewer, decision, source and approval date. An AI cannot impersonate the reviewer or supply an approval.
- **Lender-waived:** only after genuine lender written response tied to the exact requirement. A report, sent email or draft is not a waiver.

## Critical distinctions

- Do not merge multiple legal titles, transfer and mortgage deeds, additional security properties or companies because a street address/surname looks similar.
- Check original deed/official plan visually; text extraction cannot prove signature, attestation, scales, boundaries or colours.
- UK Finance applies only where incorporated or applicable, and lender Part 2/3 and offer-specific requirements remain mandatory. Bridging/commercial borrowers may have bespoke solicitor instructions.
- The date engine uses the actual SDLT/LTT taxable effective date and the proper MR01 company charge creation date; neither automatically equals exchange or completion in every case. Application protection, requisition deadlines, lender notice and contractual interest are fact-dependent.
- Registry preflight is an **error-spotting aid**. Review HM Land Registry practice guides, prescribed current forms and all supporting originals. Avoid assuming AP1 is appropriate for first registration or every lease transaction.
- Any instruction to send files, ask a lender for funds, request registration or give an undertaking is an external professional action requiring specific authority, appropriate connected tool and firm review.

## Controls

Treat every case file as privileged and firm-controlled. Use local ephemeral/external approved matter storage, pseudonymous identifiers and separate access controls. Do not sync sensitive content to public source control. No live service is enabled by the static offline dashboard or CSV handoff. For updated guidance, use the existing source-policy change-control steps before promoting changed propositions or lender routes to `verified`.

See `../../docs/MATTER_WORKBENCH.md` for end-to-end CLI, statuses, example and validation instructions.
