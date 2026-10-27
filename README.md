# England and Wales Conveyancing Legal Skill

**Release:** 0.1.0 (27 October 2026 research baseline) | **Audience:** qualified solicitors, licensed conveyancers and supervised legal support staff | **Status:** tested, usable foundation; **not** a certified autonomous legal practice system.

A portable, evidence-gated conveyancing knowledge and workflow package for the law of England and Wales, focused on purchase/borrower/lender work. A single canonical `SKILL.md` selects independently maintainable practice modules and rules. A Python CLI supplies deterministic quality gates and calculations. **Human legal verification and lender-specific sign-off remain mandatory.**

## What is included

- 15 stages for intake, CDD/AML, title, searches, enquiries, finance, reporting, exchange, completion, tax, registration and closing. **28 transaction profiles**, including commercial, auction, unregistered, bridging, corporate, transfers, shared ownership and development.
- 9 substantial practice modules and a registered/unregistered title risk-review protocol. An explicit risk scheme R0–R4 and evidence trace requirements.
- **98 indexed forms**, their official provider page or directory, verification status, general execution/filing considerations and specific first-priority panel guides. The binary versions and numerous individual form paragraphs remain **unverified**: no PDF/Word facsimiles are included.
- **51 authoritative source records** and **33 indexed legal rules** with a 27 October 2026 check baseline and explicit commissioning/commencement caveats. The source directory is **not** an assurance that all legislation is current at the later point of use.
- UK Finance Handbook checks, lender condition extractor workflow, conveyancing pre-completion/auction workflow and case-specific lender-reporting flags. Bank confirmations, actual Handbook Part 2 requirements and certificate sign-off cannot be automatically inferred.
- Python standard-library completion statement, deadline and restricted tax calculation functions; optional PDF/DOCX extraction and evidence-controlled DOCX changes with exact logs.
- GitHub Actions unit tests and a **proposed** weekly read-only source watch. Workflow jobs do not run until the user enables them in their GitHub repository. A source change always enters a human review queue.

## Prerequisites

- Python 3.10 or newer and `pip`. Git is needed to clone the repository; a ZIP download also works.
- The core CLI uses Python's standard library and needs no API keys or external services. Internet access is needed to install packages and only when you explicitly check current public sources.
- PDF/DOCX extraction requires the optional `documents` extra (`pypdf` and `python-docx`); install it with the command below.
- Use this as supervised support for qualified conveyancing practitioners. Check current law, lender instructions and firm requirements at the point of use.

## Quick start (Python 3.10+)

```bash
python -m venv .venv
source .venv/bin/activate                # Windows: .venv\Scripts\activate
python -m pip install -e '.[documents]' # omit [documents] if not processing PDFs/Word
conveyancing validate
python -m unittest discover -s tests -v
conveyancing forms TR1
conveyancing workflow registered-freehold-purchase
conveyancing workflow --list
conveyancing review tests/fixtures/historic-charge.json
conveyancing completion examples/completion-input.json
conveyancing deadline sdlt 2026-10-27
conveyancing tax-estimate --jurisdiction england --price 295000 --as-of 2026-10-27 --acknowledge-simple
conveyancing extract /path/to/lease.pdf --output evidence.json
conveyancing source-watch --limit 6               # dry-run, no HTTP calls
# To check published pages, explicitly opt in:
conveyancing source-watch --allow-network --limit 6 --output reports/source-watch.json
```

**Tax guardrail:** no relief, non-UK resident, linked transaction, mixed-use, special corporate rate, multiple dwellings, lease rent/NPV, lease premium complexities or anti-avoidance questions are calculated here. Dates after the stored verification date or snapshot review-by date **refuse** calculation. The rate snapshot has **review-by 3 November 2026**, meaning it must be researched again before later use.

**Priority-period guardrail:** for OS1/OS2 the program requires a separately verified list of public holidays. It must not treat statutory deadlines, notice-to-complete deadlines and lender conditions as interchangeable.

## Installation by AI platform

| Platform | How to enable the skill | Operating detail |
|---|---|---|
| **Claude Code** | Open this repository as the project, or copy/link `.claude/skills/conveyancing-legal` into your project. Refer to `CLAUDE.md`. | Claude follows project skill conventions; local CLI commands require filesystem/shell permissions. See [official documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). |
| **OpenAI Codex** | Open project root. Codex discovers `.agents/skills/conveyancing-legal/SKILL.md` and `AGENTS.md` in supported versions. | Allow local script execution only in a trusted workspace. [Official skills guide](https://developers.openai.com/codex/skills). |
| **ChatGPT Plugins** | In an eligible ChatGPT plugin-builder/workflow, upload or connect the repo containing `plugin.json` and `skills/`, according to the current builder flow. | Platform installation and packaging **have not been tested on a live ChatGPT account**. `plugin.json` is a candidate scaffold, not a registered/published plugin. Verify [plugins](https://developers.openai.com/plugins/build/plugins) and [skills](https://developers.openai.com/plugins/concepts/skills). |
| **ChatGPT Projects** | Create a Project, paste `adapters/chatgpt/PROJECT_INSTRUCTIONS.md` into its instructions, upload canonical `SKILL.md`, and only the needed reference files (or knowledge as supported). | Markdown instructions can guide analysis; local CLI cannot be assumed available. The Projects fallback is a manual installation, not an automatically linked repository. [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt). |
| **Cursor** | Open repo, enable project skill discovery from `.cursor/skills`/`.agents/skills` as supported; `.cursor/rules/conveyancing.mdc` also supplies short project rules. | Run CLI in integrated terminal. [Cursor skills](https://cursor.com/help/customization/skills). |
| **Gemini CLI** | Open repo: `.gemini/skills/conveyancing-legal/SKILL.md` and root `GEMINI.md` instruct project-scope skill usage. | Check agent settings and filesystem permissions. [Gemini skills](https://geminicli.com/docs/cli/skills/). |
| **Claude Desktop** | Where supported, install the folder as an Agent Skill via your Desktop application's current Skills UI; otherwise attach the canonical skill and relevant knowledge in a project. | Do not claim automatic access to a local CLI in ordinary chat. |
| **Other agents** | Supply `SKILL.md`, `core/`, the relevant `knowledge/practice/` module, `knowledge/legislation`, and selected workflows through project instructions or the host's skill-folder interface. | Host availability of networking, documents, tools and scheduled updates differs. |

The **authoritative skill is the root `SKILL.md`**. Platform `SKILL.md` files are shallow launchers, not separately maintained legal copies. Relative paths assume the whole repository is available to the agent. Standalone isolated skill-folder installation may require copying additional referenced files into the same accessible folder.

## Work on a matter

1. Create a client-authorised confidential workspace outside a public repository. Never add live client documents, IDs, bank statements, matter credentials, lender offers or privileged advice to Git, CI logs or third-party AI tools without approved firm policy.
2. Select one of 28 profiles: `conveyancing workflow --list`. Collect matter facts and documents; the default status for every stage is **outstanding**.
3. Extract uploaded material only when local policy permits; compare the actual scanned original, page, plan and seal with the text. OCR is not automatic.
4. Put structured facts (with original evidence refs) into JSON like `examples/matter-input.json`; run `conveyancing review ...` for a list of unresolved issues. An empty blocker list **never** equals clearance to exchange or complete.
5. Check up-to-date legislation, HMLR forms, HMRC/WRA tax guidance, firm policies, lender offer and the actual applicable UK Finance Part 1/2/3 (or bespoke) instructions. Raise and record enquiries.
6. Draft correspondence using the original templates at `templates/`, not the statutory form facsimiles. Convert original reports to editable Word with `conveyancing to-docx INPUT.md OUTPUT.docx` (requires `python-docx`). Use `fill-docx` **only** for named evidence-supported `{{PLACEHOLDER}}` values in an authorised template; see `examples/field-values.json`.
7. Supervised conveyancer checks changes, confirms no unresolved registration/completion blockers, then personally authorises any filing or communication through their approved tools. **The skill never executes those actions.**

## Repository layout

```text
SKILL.md                         Canonical agent instructions
core/                            Evidence protocol and source policy
knowledge/legislation/           Legislation/source registry and time-gated tax snapshots
knowledge/forms/                 Forms catalogue, status, panel guidance
knowledge/practice/              9 specialist substantive practice modules
knowledge/workflows/             15 stages and 28 transaction profiles
templates/                       Original, non-prescribed editable text drafts
src/conveyancing_skill/          Python CLI, extraction, output and source watcher
schemas/                         Structured matter and source schemas
adapters/                        ChatGPT Projects installation
.agents/, .claude/, .gemini/      Adapter launcher files
.cursor/, AGENTS.md, CLAUDE.md, GEMINI.md   Project host entrypoints
examples/                        Fictional example data
/tests/fixtures/                 Fictional positive and failure scenarios
.github/workflows/               CI + inactive-until-push source watch definition
docs/                            Legal verification, maintenance, inventory, reports
```

## Essential legal accuracy rules

- The title plan indicates **general boundaries**. A plan's appearance does not prove adopted-highway status, an easement or exact boundary location.
- An email asserting a mortgage was “vacated” **does not** itself show a registered or otherwise effective discharge. Identify the actual release or charge evidence, registered/unregistered treatment, and lender acceptability.
- Individual UK Finance lender requirements, bespoke bridging terms, guarantee protections and ILA wording must be sourced from the **actual lender instructions**. Independent advice must be genuinely independent and delivered under applicable professional rules.
- Sale contract date, statutory instrument commencement, late tax filing, accepted HMLR application, bank funds and legal completion are distinct events.
- The legal form's wording and prescribed execution must not be altered in the name of formatting. Protected TA, CPSE and LPE forms are reference-only unless a licence permits their use.

## Authority, change control and acceptance

Read `docs/SOURCE_VERIFICATION_REPORT.md`, `docs/VALIDATION_AND_LIMITATIONS.md`, `docs/MAINTENANCE.md`, `docs/FEATURE_INVENTORY.md`, and `CHANGELOG.md`. Legislation and regulatory rule changes are detected, researched for legal effect, manually approved and versioned as separate steps. The baseline source check date is **27 October 2026**; each matter needs its own point-of-use confirmation.

## Licence and confidentiality

No licence is granted automatically. Any use, including non-commercial use, requires prior written permission from the copyright holder; commercial use requires separate prior written permission. No proprietary Law Society forms, premium Handbook content, lender internal terms or third-party confidential legal pack is included or sublicensed. Official materials remain under their publisher's rights.

### Extract candidate lender conditions and compare documents

```bash
conveyancing lender-checklist /path/to/lender-instructions.pdf
conveyancing compare-documents /path/to/title-register.pdf /path/to/transfer.docx
```

These are deliberately **candidate** extractors, not exhaustive document readers: text-only pages and key phrases may be missed and every extracted sentence remains unverified until the solicitor checks the original. The lender-checklist command will never mark a requirement satisfied.
