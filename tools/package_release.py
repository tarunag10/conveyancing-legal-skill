#!/usr/bin/env python3
"""Build a source ZIP from a Git commit and verify it can be read and extracted."""

from __future__ import annotations

import argparse
import hashlib
import io
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="ZIP output path")
    parser.add_argument("--ref", default="HEAD", help="Git ref to package (default: HEAD)")
    parser.add_argument("--version", required=True, help="Package version, e.g. 0.1.0")
    args = parser.parse_args()

    commit = git("rev-parse", "--verify", f"{args.ref}^{{commit}}").decode().strip()
    prefix = f"conveyancing-legal-skill-v{args.version}/"
    archive = git("archive", "--format=zip", f"--prefix={prefix}", commit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(archive)

    with zipfile.ZipFile(io.BytesIO(archive)) as package:
        bad_member = package.testzip()
        if bad_member:
            raise RuntimeError(f"Corrupt ZIP member: {bad_member}")
        names = set(package.namelist())
        required = {
            f"{prefix}SKILL.md",
            f"{prefix}README.md",
            f"{prefix}LICENSE",
            f"{prefix}core/OPERATING_STANDARD.md",
            f"{prefix}src/conveyancing_skill/cli.py",
            f"{prefix}tests/test_engine.py",
            f"{prefix}adapters/chatgpt/PROJECT_INSTRUCTIONS.md",
            f"{prefix}.agents/skills/conveyancing-legal/SKILL.md",
            f"{prefix}.claude/skills/conveyancing-legal/SKILL.md",
            f"{prefix}.cursor/rules/conveyancing.mdc",
            f"{prefix}.gemini/skills/conveyancing-legal/SKILL.md",
        }
        missing = required - names
        if missing:
            raise RuntimeError(f"ZIP is missing required paths: {sorted(missing)}")
        with tempfile.TemporaryDirectory(prefix="conveyancing-release-") as temp_dir:
            package.extractall(temp_dir)
            extracted_root = Path(temp_dir) / prefix.rstrip("/")
            if not (extracted_root / "LICENSE").is_file():
                raise RuntimeError("ZIP extraction check failed")

    digest = hashlib.sha256(archive).hexdigest()
    checksum_path = args.output.with_suffix(args.output.suffix + ".sha256")
    checksum_path.write_text(f"{digest}  {args.output.name}\n", encoding="utf-8")
    print(f"Verified {args.output} ({len(archive)} bytes)")
    print(f"SHA-256: {digest}")
    print(f"Source commit: {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
