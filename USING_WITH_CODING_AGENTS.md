# Using this repository with a coding agent

Repository: https://github.com/tarunag10/conveyancing-legal-skill

## Before you start

This is a research and supervised-workflow project for England and Wales conveyancing. It is not legal advice, a substitute for a qualified practitioner, or a source of guaranteed current law. Check the current law, lender instructions and firm requirements for each matter.

The repository is public only if its owner makes it public; visibility does not grant permission to use, copy, adapt or run its contents. The `LICENSE` requires prior written permission for all use. Obtain and follow that permission before asking an agent to work with the repository. Do not include live client, identity, financial, privileged or confidential matter data.

## Give a coding agent access

1. Open a coding-agent workspace that can access GitHub repositories, then paste the repository link and the task prompt below.
2. If the agent cannot open GitHub links, clone the repository or download its ZIP, then open the extracted repository folder in the agent.
3. Ask the agent to read `LICENSE`, `README.md`, `AGENTS.md`, `SKILL.md`, and any relevant files before changing anything.
4. Keep any work on a separate branch or local copy. Review the diff before using or sharing changes.

## Copy-paste task prompt

```text
Work in the repository at https://github.com/tarunag10/conveyancing-legal-skill.

I have the written permission required by LICENSE for this task. Its scope is:
[quote or describe the permission and any limits; if you do not have permission, stop and tell me]

First inspect LICENSE, README.md, AGENTS.md, SKILL.md and the relevant modules. Then complete this task:
[describe the coding or documentation task]

Follow repository instructions. Keep the change focused, explain what you changed, and report any checks you ran and their results. Do not put real client or confidential matter data in this repository. Do not treat stored legal research as current without checking authoritative sources at the point of use. Do not make legal decisions, contact third parties, file documents, exchange contracts, or move funds.
```

## Current technical requirements

- Python 3.10 or newer and `pip`; use Git to clone, or download the repository as a ZIP.
- The core CLI uses Python's standard library. PDF and DOCX extraction needs the optional `documents` extra described in `README.md`.
- Internet access is needed to install packages and to check current public sources when explicitly requested. The core CLI does not need API keys.

See `README.md` for installation, commands, limitations and supported agent entrypoints.
