# England and Wales Conveyancing Legal Skill

**Release:** 0.1.0 | **Research baseline:** 27 October 2026 | **Repository/package update:** 28 October 2026 | **Audience:** qualified solicitors, licensed conveyancers and supervised legal support staff | **Status:** tested, usable foundation; **not** a certified autonomous legal practice system.

A portable, evidence-gated conveyancing knowledge and workflow package for the law of England and Wales, focused on purchase/borrower/lender work. A single canonical `SKILL.md` selects independently maintainable practice modules and rules. A Python CLI supplies deterministic quality gates and calculations. **Human legal verification and lender-specific sign-off remain mandatory.**

For a step-by-step use sequence, recorded update dates and the 2030-and-later position, see [the app use and update timeline](docs/APP_TIMELINE.md). There is no general 2030 expiry, but stored legal research is not guaranteed current through 2030; check current sources before relying on it.

## What is included

- 15 stages for intake, CDD/AML, title, searches, enquiries, finance, reporting, exchange, completion, tax, registration and closing. **28 transaction profiles**, including commercial, auction, unregistered, bridging, corporate, transfers, shared ownership and development.
- 9 substantial practice modules and a registered/unregistered title risk-review protocol. An explicit risk scheme R0–R4 and evidence trace requirements.
- **98 indexed forms**, their official provider page or directory, verification status, general execution/filing considerations and specific first-priority panel guides. The binary versions and numerous individual form paragraphs remain **unverified**: no PDF/Word facsimiles are included.
- **51 authoritative source records** and **33 indexed legal rules** with a 27 October 2026 check baseline and explicit commissioning/commencement caveats. The source directory is **not** an assurance that all legislation is current at the later point of use.
- UK Finance Handbook checks, lender condition extractor workflow, conveyancing pre-completion/auction workflow and case-specific lender-reporting flags. Bank confirmations, actual Handbook Part 2 requirements and certificate sign-off cannot be automatically inferred.
- Python standard-library completion statement, deadline and restricted tax calculation functions; optional PDF/DOCX extraction and evidence-controlled DOCX changes with exact logs.
- GitHub Actions unit tests and a **proposed** weekly read-only source watch. Workflow jobs do not run until the user enables them in their GitHub repository. A source change always enters a human review queue.

## Download the complete package

Download the versioned source ZIP from [GitHub Releases](https://github.com/tarunag10/conveyancing-legal-skill/releases). For version 0.1.0, the direct asset link is [conveyancing-legal-skill-v0.1.0.zip](https://github.com/tarunag10/conveyancing-legal-skill/releases/download/v0.1.0/conveyancing-legal-skill-v0.1.0.zip); the matching `.sha256` file is published alongside it. The ZIP contains the full tagged repository tree, including the canonical skill, knowledge modules, Python implementation, templates, tests, documentation, licence, and platform adapters. Extract it before installing; keep the directory structure intact.

**Permission is required before any use.** The ZIP does not grant a licence. Read the included `LICENSE` and [`docs/USE_PERMISSION.md`](docs/USE_PERMISSION.md), and obtain prior written permission from the copyright holder for the intended use. Commercial use requires separate prior written permission. Platform installation does not amount to legal verification, professional approval, or permission to use the contents. Check current law, lender instructions, firm requirements, and the supplied research at the point of use.

### Install from the extracted folder

| Platform | Steps |
|---|---|
| **ChatGPT desktop plugin** | Open a terminal in the extracted `conveyancing-legal-skill-v0.1.0` folder and run `codex plugin marketplace add .`. In ChatGPT desktop, open the Plugins Directory, select the `conveyancing-legal-skill` marketplace, and install **Conveyancing Legal Skill**. Restart the app if it does not appear. This installs the local copy for the signed-in desktop app. See [OpenAI's plugin packaging and installation guide](https://developers.openai.com/plugins/build/plugins). |
| **ChatGPT Projects** | Create a Project. Copy `adapters/chatgpt/PROJECT_INSTRUCTIONS.md` into the Project instructions, then upload the root `SKILL.md` and only the reference files needed for that Project. Keep related files together where possible because the instructions use relative paths. This is a manual, knowledge-file installation; the Python CLI is not available in ordinary Projects chat. |
| **Claude Code** | Open the extracted repository folder as the project. Claude Code discovers `.claude/skills/conveyancing-legal` and `CLAUDE.md`. Alternatively, copy that skill folder into the project and keep the referenced repository files accessible. |
| **OpenAI Codex** | Open the extracted repository root as the workspace. Codex discovers `.agents/skills/conveyancing-legal/SKILL.md` and `AGENTS.md` in supported versions. |
| **Cursor** | Open the extracted repository root. Use `.cursor/` and `.agents/skills/` discovery supported by your Cursor version. |
| **Gemini CLI** | Open the extracted repository root. The `.gemini/skills/` entrypoint and `GEMINI.md` provide the project instructions. |
| **Claude Desktop and other supported agents** | Use the host's current Agent Skills or project-knowledge interface. Add the canonical root `SKILL.md` and the relevant linked repository files; retain the extracted directory layout when the host can access files. The repository ZIP is not a standalone skill-folder ZIP. Check the host's current documentation for its supported import method. |

For the Python CLI, install from that folder with the Quick start commands below. Run `python -m conveyancing_skill.cli validate` (or `conveyancing validate` after installation) to check the local package. To run the test suite, use `PYTHONPATH=src python -m unittest discover -s tests -v`. These checks validate package structure and software behaviour only. They do not verify legal correctness for a live matter or provide professional sign-off.

### Verify the downloaded ZIP

Download the ZIP and its `.sha256` file from the same release. From the download directory, run `sha256sum -c conveyancing-legal-skill-v0.1.0.zip.sha256` on Linux/macOS, or compare the hash printed by `Get-FileHash .\conveyancing-legal-skill-v0.1.0.zip -Algorithm SHA256` on Windows with the value in the checksum file. Then extract the ZIP and confirm that the top-level folder contains `SKILL.md`, `LICENSE`, `README.md`, `src/`, `knowledge/`, `templates/`, and `adapters/`.

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
| **ChatGPT desktop plugin** | Run `codex plugin marketplace add .` from the repository root. In ChatGPT desktop, use Plugins Directory to select the repo marketplace and install **Conveyancing Legal Skill**. | This installs the local copy in the signed-in desktop app; it does not publish the plugin. Other users must obtain the ZIP or clone the repo and install their own local copy. A plugin install does not grant permission to use the skill: see `docs/USE_PERMISSION.md` and obtain written permission first. See [OpenAI plugin packaging and installation](https://developers.openai.com/plugins/build/plugins). |
| **ChatGPT Projects** | Create a Project, paste `adapters/chatgpt/PROJECT_INSTRUCTIONS.md` into its instructions, upload canonical `SKILL.md`, and only the needed reference files (or knowledge as supported). | Markdown instructions can guide analysis; local CLI cannot be assumed available. The Projects fallback is a manual installation, not an automatically linked repository. [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt). |
| **Cursor** | Open repo, enable project skill discovery from `.cursor/skills`/`.agents/skills` as supported; `.cursor/rules/conveyancing.mdc` also supplies short project rules. | Run CLI in integrated terminal. [Cursor skills](https://cursor.com/help/customization/skills). |
| **Gemini CLI** | Open repo: `.gemini/skills/conveyancing-legal/SKILL.md` and root `GEMINI.md` instruct project-scope skill usage. | Check agent settings and filesystem permissions. [Gemini skills](https://geminicli.com/docs/cli/skills/). |
| **Claude Desktop** | Where supported, install the folder as an Agent Skill via your Desktop application's current Skills UI; otherwise attach the canonical skill and relevant knowledge in a project. | Do not claim automatic access to a local CLI in ordinary chat. |
| **Other agents** | Supply `SKILL.md`, `core/`, the relevant `knowledge/practice/` module, `knowledge/legislation`, and selected workflows through project instructions or the host's skill-folder interface. | Host availability of networking, documents, tools and scheduled updates differs. |

The **authoritative skill is the root `SKILL.md`**. Platform `SKILL.md` files are shallow launchers, not separately maintained legal copies. Relative paths assume the whole repository is available to the agent. Standalone isolated skill-folder installation may require copying additional referenced files into the same accessible folder.

## Work on a matter

1. Create a client-authorised confidential workspace outside a public repository. Never add live client documents, IDs, bank statements, matter credentials, lender offers or privileged advice to Git, CI logs or third-party AI tools without approved firm policy.
2. Start from [`templates/matter-intake.template.json`](templates/matter-intake.template.json) in that private workspace. Use a pseudonymous matter ID, give each document a stable ID, and cite the actual document plus page/clause for every recorded fact. The template is only an intake aid; it contains no client data.
3. Select one of 28 profiles: `conveyancing workflow --list`. Collect matter facts and documents; the default status for every stage is **outstanding**. See [`docs/PRACTICAL_MATTER_WORKFLOW.md`](docs/PRACTICAL_MATTER_WORKFLOW.md) for a step-by-step example.
4. Extract documents only when firm policy permits; compare the original, page, plan and execution with extracted text. OCR is not automatic. Record each applicable lender condition in [`templates/LENDER_CONDITION_CHECKLIST.md`](templates/LENDER_CONDITION_CHECKLIST.md), against the actual current offer/instructions.
5. Put structured facts and source locators into the intake JSON; run `conveyancing review /private/approved/path/matter.json` for unresolved issues. Findings carry document ID/page references when supplied. An empty blocker list **never** equals clearance to exchange or complete.
6. Check up-to-date legislation, HMLR forms, HMRC/WRA tax guidance, firm policies, lender offer and the actual applicable UK Finance Part 1/2/3 (or bespoke) instructions. Raise and record enquiries.
7. Draft correspondence using the original templates at `templates/`, not the statutory form facsimiles. Convert original reports to editable Word with `conveyancing to-docx INPUT.md OUTPUT.docx` (requires `python-docx`). Use `fill-docx` **only** for named evidence-supported `{{PLACEHOLDER}}` values in an authorised template; see `examples/field-values.json`.
8. A supervised conveyancer checks findings and drafts, confirms any unresolved registration/completion blockers, and personally authorises filing or communication through approved tools. **The skill never executes those actions.**

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

No licence is granted automatically. Any use, including internal evaluation or non-commercial research, requires prior written permission from the copyright holder. Using the tool on fee-earning client matters is likely commercial use and requires separate prior written permission. See [`docs/USE_PERMISSION.md`](docs/USE_PERMISSION.md) for a permission request checklist. No proprietary Law Society forms, premium Handbook content, lender internal terms or third-party confidential legal pack is included or sublicensed. Official materials remain under their publisher's rights.

### Extract candidate lender conditions and compare documents

```bash
conveyancing lender-checklist /path/to/lender-instructions.pdf
conveyancing compare-documents /path/to/title-register.pdf /path/to/transfer.docx
```

These are deliberately **candidate** extractors, not exhaustive document readers: text-only pages and key phrases may be missed and every extracted sentence remains unverified until the solicitor checks the original. The lender-checklist command will never mark a requirement satisfied.
