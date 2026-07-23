#!/usr/bin/env python3
"""Validate the minimum structure of an evidence-backed repository audit."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = (
    "executive summary",
    "scope",
    "findings",
    "execution roadmap",
    "verification",
)
STATUSES = ("CONFIRMED", "REFUTED", "UNVERIFIED", "NOT CHECKED")
SEVERITIES = ("P0", "P1", "P2")


def validate_text(text: str) -> list[str]:
    """Return human-readable contract violations."""
    errors: list[str] = []
    headings = {
        match.group(1).strip().lower()
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    }

    for section in REQUIRED_SECTIONS:
        if not any(section in heading for heading in headings):
            errors.append(f"missing section: {section}")

    if not re.search(r"\b(?:P0|P1|P2)\b", text):
        errors.append("missing severity label: P0, P1, or P2")

    if not re.search(r"\b(?:CONFIRMED|REFUTED|UNVERIFIED|NOT CHECKED)\b", text):
        errors.append("missing evidence status")

    if not re.search(r"\b[A-Z][A-Z0-9]*-\d+\b", text):
        errors.append("missing stable finding ID such as DATA-1")

    evidence_patterns = (
        r"\b(?:File|Evidence|Source|Command|Receipt):\s+\S+",
        r"https://github\.com/\S+",
        r"`[^`\n]+:\d+(?:-\d+)?`",
    )
    if not any(re.search(pattern, text, re.IGNORECASE) for pattern in evidence_patterns):
        errors.append("missing exact evidence locator")

    return errors


def run_self_test() -> int:
    """Exercise both passing and failing validation paths."""
    good = """# Audit
## Executive summary
## Scope
## Findings
### DATA-1
Severity: P1
Status: CONFIRMED
Evidence: `src/store.py:42`
## Execution roadmap
## Verification
"""
    bad = "# Notes\nLooks fine.\n"
    if validate_text(good):
        print("self-test failed: valid fixture was rejected", file=sys.stderr)
        return 1
    if not validate_text(bad):
        print("self-test failed: invalid fixture was accepted", file=sys.stderr)
        return 1
    print("self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit", nargs="?", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if args.audit is None:
        parser.error("audit path is required unless --self-test is used")

    try:
        text = args.audit.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"unable to read {args.audit}: {exc}", file=sys.stderr)
        return 2

    errors = validate_text(text)
    result = {
        "path": str(args.audit),
        "valid": not errors,
        "errors": errors,
    }
    if args.as_json:
        print(json.dumps(result, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    else:
        print(f"valid audit: {args.audit}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
