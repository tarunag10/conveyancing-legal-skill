# Feature inventory and deployment status

| Feature | Implemented | Verified / readiness |
|---|---|---|
| Canonical portable skill instructions | Yes | Filesystem review; live platform import not tested |
| Claude Code, Codex, Cursor, Gemini CLI folder adapters | Yes | Installed directories and short launchers; host discovery not tested |
| ChatGPT Projects fallback | Yes | Copy-ready instructions; manual upload required |
| ChatGPT Plugin package | Candidate only | Current schema-dependent importer compatibility not live-tested |
| 15 end-to-end conveyancing stages | Yes | Stage definitions include tasks, conditional tasks, responsibilities, evidence, dependencies and unproven default status |
| 28 matter-specific profiles | Yes | Detailed variation tasks; workflow approval remains manual |
| Registered/unregistered title, deeds, charges, access | Yes (reference and risk triage) | No automatic title opinion or visually verified plan interpretation |
| Auction, buy-to-let, bridging, corporate borrowers, ILA | Yes (reference and checklist) | No lender-specific Part 2 content, approved security package or lawyer certification |
| Leasehold, building safety, commercial, VAT/TOGC | Yes (reference) | Specialist provisions require matter-specific review |
| Forms library (98 entries) | Yes (index) | Zero original form binary revisions independently hash-validated; individual panel coverage selective |
| Dated source registry (51) | Yes | Source pages checked 27 Oct 2026; 33 rule records await legal sign-off |
| Buyer-side completion money reconciliation | Yes, executable | Input-only; actual client account/lender evidence not confirmed |
| Narrow basic residential SDLT/LTT calculator | Yes, executable | Time-gated illustrative bands; complex cases refused |
| Selected statutory days / OS priority date | Yes, executable | Holiday list required; contractual notice analysis manual |
| PDF/Word evidence text extraction | Yes, optional dependencies | Text only; OCR/visual signature or plan checks not provided |
| Editable original Word and replacement change logs | Yes, optional dependency | Only literal same-run placeholders; no protected form mutation or guaranteed preservation of layout |
| Content change watcher | Yes, opt-in | Domain allowlist and SHA256; no actual law effect determination |
| GitHub Actions CI / periodic watch definitions | Yes | Not remotely activated or scheduled until GitHub repository installed |
| Test scenarios | Yes | Fictional stress tests in `tests/fixtures` with Python unit tests |
| Full DMS, access control, authenticated user actions | No | Integrate only after firm security design and approval |
| Automatic exchange, payment, filing and third-party communications | Intentionally no | Requires explicit professional authorisation plus tool permissions |

### Most important gaps before a true production deployment

1. Form binary validation and precise per-form panel, execution and version details; licensed form source access.
2. Exhaustive legal sign-off for operative, transitional and jurisdictional status; live lender conditions.
3. Adversarial document parsing and OCR validation, scanned plans and boundary interpretation.
4. Independent legal and QA review, platform-by-platform acceptance, secure file storage and live CI deployment.
