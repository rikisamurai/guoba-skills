#!/usr/bin/env python3
"""Grade quick-commit eval results against the typed assertions in evals.json.

Usage:
    python3 grade.py [--evals evals.json] [--results-dir baseline-results]

Each result file is `<results-dir>/<eval-name>.json` and follows the
`result_schema` documented in evals.json. The grader prints per-eval and
overall pass/fail, plus a "should" score for nuance. Exit code is 0 when all
`must` assertions pass across all evals, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent


@dataclass
class CheckResult:
    status: str  # "pass" | "fail" | "manual"
    detail: str = ""


def _get_field(result: dict, field: str) -> Any:
    if field not in result:
        raise KeyError(f"result is missing field '{field}'")
    return result[field]


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(str(v) for v in value)
    return json.dumps(value, ensure_ascii=False)


def run_check(check: dict, result: dict) -> CheckResult:
    ctype = check["type"]

    if ctype == "qualitative":
        return CheckResult("manual", "human review required")

    if ctype == "regex_match":
        haystack = _stringify(_get_field(result, check["field"]))
        if re.search(check["pattern"], haystack):
            return CheckResult("pass")
        return CheckResult("fail", f"pattern not found in {check['field']!r}")

    if ctype == "regex_not_match":
        haystack = _stringify(_get_field(result, check["field"]))
        if re.search(check["pattern"], haystack):
            snippet = re.search(check["pattern"], haystack).group(0)
            return CheckResult("fail", f"unwanted pattern matched: {snippet!r}")
        return CheckResult("pass")

    if ctype == "equals":
        actual = _get_field(result, check["field"])
        if actual == check["value"]:
            return CheckResult("pass")
        return CheckResult("fail", f"expected {check['value']!r}, got {actual!r}")

    if ctype == "array_equals":
        actual = _get_field(result, check["field"])
        if not isinstance(actual, list):
            return CheckResult("fail", f"{check['field']} is not a list: {actual!r}")
        if sorted(actual) == sorted(check["value"]):
            return CheckResult("pass")
        return CheckResult("fail", f"expected set {sorted(check['value'])!r}, got {sorted(actual)!r}")

    if ctype == "array_excludes":
        actual = _get_field(result, check["field"])
        if not isinstance(actual, list):
            return CheckResult("fail", f"{check['field']} is not a list")
        bad = [v for v in check["values"] if v in actual]
        if bad:
            return CheckResult("fail", f"forbidden elements present: {bad!r}")
        return CheckResult("pass")

    if ctype == "array_includes_all":
        actual = _get_field(result, check["field"])
        if not isinstance(actual, list):
            return CheckResult("fail", f"{check['field']} is not a list")
        missing = [v for v in check["values"] if v not in actual]
        if missing:
            return CheckResult("fail", f"missing elements: {missing!r}")
        return CheckResult("pass")

    if ctype == "subject_length_le":
        message = _stringify(_get_field(result, "commit_message"))
        subject = message.split("\n", 1)[0]
        if len(subject) <= check["max"]:
            return CheckResult("pass", f"subject is {len(subject)} chars")
        return CheckResult("fail", f"subject is {len(subject)} chars, max {check['max']}")

    return CheckResult("fail", f"unknown check type: {ctype}")


def grade_eval(eval_def: dict, result: dict) -> dict:
    rows = []
    for assertion in eval_def["assertions"]:
        outcome = run_check(assertion["check"], result)
        rows.append({
            "id": assertion["id"],
            "weight": assertion["weight"],
            "human": assertion["human"],
            "status": outcome.status,
            "detail": outcome.detail,
        })

    must_total = sum(1 for r in rows if r["weight"] == "must" and r["status"] != "manual")
    must_passed = sum(1 for r in rows if r["weight"] == "must" and r["status"] == "pass")
    should_total = sum(1 for r in rows if r["weight"] == "should" and r["status"] != "manual")
    should_passed = sum(1 for r in rows if r["weight"] == "should" and r["status"] == "pass")
    manual_count = sum(1 for r in rows if r["status"] == "manual")

    return {
        "name": eval_def["name"],
        "rows": rows,
        "must_passed": must_passed,
        "must_total": must_total,
        "should_passed": should_passed,
        "should_total": should_total,
        "manual_count": manual_count,
        "passed": must_passed == must_total,
    }


def fmt_status(status: str) -> str:
    return {"pass": "PASS", "fail": "FAIL", "manual": "MANUAL"}[status]


def print_eval(report: dict) -> None:
    print(f"\n[{report['name']}]")
    for row in report["rows"]:
        line = f"  {fmt_status(row['status']):6} ({row['weight']:5}) {row['id']:40} {row['human']}"
        print(line)
        if row["detail"] and row["status"] == "fail":
            print(f"           {row['detail']}")
    must_score = f"{report['must_passed']}/{report['must_total']}"
    should_score = f"{report['should_passed']}/{report['should_total']}"
    verdict = "PASS" if report["passed"] else "FAIL"
    print(f"  --- {verdict}  must={must_score}  should={should_score}  manual={report['manual_count']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evals", type=Path, default=HERE / "evals.json")
    parser.add_argument("--results-dir", type=Path, default=HERE / "baseline-results")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of text")
    args = parser.parse_args()

    evals_doc = json.loads(args.evals.read_text(encoding="utf-8"))
    reports = []
    missing = []

    for eval_def in evals_doc["evals"]:
        result_path = args.results_dir / f"{eval_def['name']}.json"
        if not result_path.is_file():
            missing.append(str(result_path))
            continue
        result = json.loads(result_path.read_text(encoding="utf-8"))
        reports.append(grade_eval(eval_def, result))

    total_must = sum(r["must_total"] for r in reports)
    passed_must = sum(r["must_passed"] for r in reports)
    total_should = sum(r["should_total"] for r in reports)
    passed_should = sum(r["should_passed"] for r in reports)
    total_manual = sum(r["manual_count"] for r in reports)
    all_passed = all(r["passed"] for r in reports) and not missing

    if args.json:
        print(json.dumps({
            "passed": all_passed,
            "missing_results": missing,
            "summary": {
                "must": {"passed": passed_must, "total": total_must},
                "should": {"passed": passed_should, "total": total_should},
                "manual": total_manual,
            },
            "evals": reports,
        }, indent=2, ensure_ascii=False))
    else:
        for report in reports:
            print_eval(report)
        print()
        print("=" * 60)
        if missing:
            print("MISSING result files:")
            for path in missing:
                print(f"  - {path}")
        print(f"OVERALL: {'PASS' if all_passed else 'FAIL'}")
        print(f"  must:   {passed_must}/{total_must}")
        print(f"  should: {passed_should}/{total_should}")
        print(f"  manual: {total_manual}  (qualitative — review by hand)")

    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
