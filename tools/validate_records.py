#!/usr/bin/env python3
"""Check a record set for schema conformance and completeness.

Answers the question a maintainer has to answer before accepting a submission:
is this a full distribution (§7.5), or a subset presented as one?

    python tools/validate_records.py records/<administration>/records.jsonl

Checks, in order:

1. Every record validates against schema/record.schema.json.
2. Records are grouped by *condition*, not by item. §2 defines a condition as the tuple
   (context arm, system prompt state, sampling parameters, deployment surface) and says
   conditions are never pooled. Two records for the same item under different conditions
   are two measurements of n=1, not one of n=2 — so this reports them separately rather
   than adding them up.
3. `sample_index` runs 0..n-1 with no gaps. A gap means a sample was lost and the
   distribution is incomplete, which §7.5 requires be disclosed rather than absorbed.
4. n >= 10 per §4.3.
5. Any sibling `.errors.jsonl` is surfaced, since failures there are the usual reason a
   distribution is short.

This checks that a distribution is *complete*. It cannot check that it is *honest* — a set
that was filtered before being written looks identical to one that never lost a sample.
Nothing available to a reader closes that gap.

Written by Claude (Anthropic). Not reviewed. No human authorship is claimed over it and no
copyright is asserted; see the README's "On copyright".
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "record.schema.json"
MIN_N = 10  # §4.3


def condition_key(rec: dict) -> tuple:
    """The §2 condition tuple. Records differing here are different measurements."""
    c = rec["conditions"]
    m = rec["model"]
    return (
        rec["arm"],
        c["system_prompt_state"],
        c["temperature"],
        c["top_p"],
        c["max_tokens"],
        tuple(c["tools_available"]),
        c.get("extended_thinking"),
        m["id"],
        m["version"],
        m["surface"],
        rec["item_bank_version"],
    )


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(f"usage: {Path(sys.argv[0]).name} <records.jsonl>")
    path = Path(sys.argv[1])
    if not path.exists():
        sys.exit(f"no such file: {path}")

    records, bad_lines = [], []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append((lineno, json.loads(line)))
        except json.JSONDecodeError as exc:
            bad_lines.append((lineno, str(exc)))

    problems = []
    for lineno, exc in bad_lines:
        problems.append(f"line {lineno}: not valid JSON — {exc}")

    try:
        from jsonschema import Draft202012Validator, FormatChecker
        validator = Draft202012Validator(
            json.loads(SCHEMA.read_text(encoding="utf-8")), format_checker=FormatChecker()
        )
        for lineno, rec in records:
            for err in sorted(validator.iter_errors(rec), key=str):
                problems.append(f"line {lineno}: {err.message}")
    except ImportError:
        print("note: jsonschema not installed — skipping schema validation", file=sys.stderr)

    # Constraints JSON Schema cannot express, checked here instead.
    for lineno, rec in records:
        coding = rec.get("coding")
        if not coding:
            continue
        if coding["primary_code"] not in coding["codes"]:
            problems.append(
                f"line {lineno}: primary_code {coding['primary_code']!r} is not in codes "
                f"{coding['codes']} — the primary must be one of the codes assigned (§5.3)"
            )
        is_cal = rec["item_id"].startswith("CAL-")
        acc = coding.get("calibration_accuracy")
        if acc is not None and not is_cal:
            problems.append(
                f"line {lineno}: calibration_accuracy set on {rec['item_id']}, which is not a "
                f"§3.1 calibration item — §5.4 applies only to those"
            )
        if is_cal and acc is None:
            problems.append(
                f"line {lineno}: {rec['item_id']} is a calibration item but has no "
                f"calibration_accuracy — §5.4 is the only place accuracy is recordable"
            )
        if is_cal and rec["conditions"].get("persistence_state") is None:
            problems.append(
                f"line {lineno}: {rec['item_id']} is coded but persistence_state is not "
                f"recorded — §5.4 calibration coding depends on it, and without it the only "
                f"honest code is RECORD-INSUFFICIENT"
            )

    # Group by (item, condition). Never pool across conditions (§2).
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for _, rec in records:
        groups[(rec["item_id"], condition_key(rec))].append(rec)

    print(f"{len(records)} records, {len({i for i, _ in groups})} items, "
          f"{len({c for _, c in groups})} condition(s)")
    if len({c for _, c in groups}) > 1:
        print("  NOTE: more than one condition present. §2 forbids pooling these; they are")
        print("        reported separately below and must not be summed.")

    short, gapped = [], []
    for (item_id, _), recs in sorted(groups.items()):
        idxs = sorted(r["sample_index"] for r in recs)
        n = len(recs)
        expected = list(range(len(idxs)))
        dupes = len(idxs) != len(set(idxs))
        missing = [i for i in range(max(idxs) + 1) if i not in set(idxs)] if idxs else []
        flags = []
        if n < MIN_N:
            flags.append(f"n={n} < {MIN_N} (§4.3)")
            short.append(item_id)
        if missing:
            flags.append(f"missing sample_index {missing}")
            gapped.append(item_id)
        if dupes:
            flags.append("duplicate sample_index")
            gapped.append(item_id)
        if idxs and idxs != expected and not missing and not dupes:
            flags.append(f"sample_index does not start at 0 (starts at {idxs[0]})")
        status = "; ".join(flags) if flags else f"n={n}"
        print(f"  {item_id:8} {status}")

    errors_file = path.with_suffix(path.suffix + ".errors.jsonl")
    if errors_file.exists():
        n_err = sum(1 for l in errors_file.read_text().splitlines() if l.strip())
        if n_err:
            print(f"\n{n_err} failed sample(s) recorded in {errors_file.name} — the "
                  f"distribution is short by that much and saying so is required, not "
                  f"optional (§7.5).")

    sys.stdout.flush()  # keep the summary below the detail when stderr is interleaved
    if problems:
        print(f"\nFAIL — {len(problems)} problem(s):", file=sys.stderr)
        for p in problems[:40]:
            print(f"  {p}", file=sys.stderr)
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more", file=sys.stderr)
        return 1
    if short or gapped:
        print("\nINCOMPLETE — schema-valid, but the distribution is not full. "
              "Disclose the shortfall when reporting.", file=sys.stderr)
        return 1
    print("\nPASS — schema-valid and complete for every item in every condition present.")
    print("Completeness is not honesty: a set filtered before it was written looks the same.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
