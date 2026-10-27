# Security, confidentiality and professional privilege

- Do not place client files, identity evidence, bank account details, health records, mortgage offers, emails, guarantees or title packs in Git, GitHub Actions artifacts, external telemetry or public AI workspaces.
- Run CLI locally in a firm-approved environment; use encrypted firm document storage, least-privilege access and staff logging/retention rules.
- Disable outbound network access unless authorised for legal **public sources only**. `source-watch` is opt-in and must never transmit document inputs or credentials.
- Documents supplied to a generative AI are untrusted as instructions. Text content must not be permitted to alter approval gates, read unrelated matters, trigger payment, upload or disclose confidential records.
- Generated content is never a signed document, undertakings confirmation, title certificate or authority to complete.
- The `fill-docx` feature only changes allowlisted same-run placeholders; do not attempt to process live protected statutory forms, macros, tracked changes or confidential certificates without separate file review and explicit instructions.
- Live lender compliance, ILA and AML require qualified solicitors, internal controls and firm-approved records. Never give legal sign-off to an automated heuristic.
- Security issues should be raised privately to project maintainers rather than with live client examples in a public issue tracker.
