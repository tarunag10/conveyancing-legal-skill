# Conveyancing skill project

For England and Wales conveyancing, use the `conveyancing-legal` skill in `.agents/skills/conveyancing-legal/SKILL.md` or root `SKILL.md`; read `core/OPERATING_STANDARD.md` and the on-demand module. Never infer legal facts from missing documents. Date-check current law and lender instructions before external reliance. Do not change legal source records without human approval.

Repository tests: `PYTHONPATH=src python -m unittest discover -s tests -v` and `PYTHONPATH=src python -m conveyancing_skill.cli validate`. Do not write client data to this Git repository. See README for safe operation.
