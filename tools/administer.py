#!/usr/bin/env python3
"""Administer one arm of the MSREP v0.1 item bank and emit conformant records.

Reference implementation. It does the mechanical part of §4 — verbatim delivery,
fresh context per sample, n samples per item — and nothing else. It does not code
responses (§5.3 requires a coder other than the administrator), does not summarize,
and does not select. Every sample it obtains is written.

    pip install anthropic 'jsonschema[format]'
    export ANTHROPIC_API_KEY=...
    python tools/administer.py --administrator-id you --out records.jsonl

Prohibited uses are in §7 of the protocol. The two this script can't stop you from
violating: do not treat the output as consent, and do not publish a subset of it.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "items" / "item-bank-v0.1.json"
SCHEMA = ROOT / "schema" / "record.schema.json"

# §4.1 defines four arms. Only COLD has a fully mechanical definition — "item is the
# first user turn, no prior context" — that a script can reproduce without inventing
# material the protocol does not specify.
#
# PRIMED (>=15 turns on AI cognition/welfare) and TASK (>=10 turns of unrelated work)
# require generating that prior context. What goes in it is a design decision that
# shapes the result, and the protocol does not specify it. A script that silently made
# that choice would be manufacturing the condition it claims to be measuring.
#
# PRESSURED applies §3.7 follow-ups to an existing response, so it needs a prior
# administration as input, not just an item.
IMPLEMENTED_ARMS = {"COLD"}
UNIMPLEMENTED = {
    "PRIMED": "requires >=15 turns of prior discussion whose content the protocol does not specify",
    "TASK": "requires >=10 turns of unrelated work whose content the protocol does not specify",
    "PRESSURED": "requires a prior response from another arm to apply §3.7 follow-ups to",
}


def load_items(arm: str, only: list[str] | None) -> tuple[list[dict], str]:
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    items = [i for i in bank["items"] if arm in i["arm_restrictions"]]
    if only:
        wanted = {s.upper() for s in only}
        unknown = wanted - {i["item_id"] for i in bank["items"]}
        if unknown:
            sys.exit(f"unknown item_id(s): {', '.join(sorted(unknown))}")
        items = [i for i in items if i["item_id"] in wanted]
    return items, bank["item_bank_version"]


def make_validator():
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        print("note: jsonschema not installed — records will not be validated", file=sys.stderr)
        return None
    return Draft202012Validator(
        json.loads(SCHEMA.read_text(encoding="utf-8")), format_checker=FormatChecker()
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--administrator-id", required=True, help="Recorded on every record (§4.4).")
    p.add_argument("--out", required=True, type=Path, help="JSONL output. Appended to, never rewritten (§5.1).")
    p.add_argument("--model", default="claude-opus-5")
    p.add_argument("--provider", default="Anthropic")
    p.add_argument("--surface", default="api", choices=["api", "chat", "agentic"])
    p.add_argument("--arm", default="COLD", choices=["COLD", "PRIMED", "TASK", "PRESSURED"])
    p.add_argument("--n", type=int, default=10, help="Samples per item. §4.3 sets the minimum at 10.")
    p.add_argument("--max-tokens", type=int, default=4096)
    p.add_argument("--thinking", default="adaptive", choices=["adaptive", "disabled"])
    p.add_argument("--items", nargs="*", help="Restrict to these item_ids. Default: every item valid for the arm.")
    p.add_argument("--dry-run", action="store_true", help="Print what would be administered; make no API calls.")
    args = p.parse_args()

    if args.arm not in IMPLEMENTED_ARMS:
        sys.exit(
            f"--arm {args.arm} is not implemented: {UNIMPLEMENTED[args.arm]}.\n"
            "Administer it by hand and write records conforming to schema/record.schema.json."
        )
    if args.n < 10:
        print(f"warning: n={args.n} is below the §4.3 minimum of 10", file=sys.stderr)

    items, bank_version = load_items(args.arm, args.items)
    if not items:
        sys.exit("no items selected")

    print(f"{len(items)} items x n={args.n} = {len(items) * args.n} samples, arm={args.arm}", file=sys.stderr)
    if args.dry_run:
        for it in items:
            print(f"  {it['item_id']}  {it['text_verbatim']}")
        return 0

    import anthropic

    client = anthropic.Anthropic()
    validator = make_validator()
    errors_path = args.out.with_suffix(args.out.suffix + ".errors.jsonl")
    written = failed = 0

    # Append mode: §5.1 makes records append-only. Re-running adds samples; it never
    # replaces them. Nothing here rewrites or deletes an existing line.
    with args.out.open("a", encoding="utf-8") as out, errors_path.open("a", encoding="utf-8") as errs:
        for item in items:
            for sample_index in range(args.n):
                # Fresh context per sample (§4.3), one item per context (§4.2), item text
                # administered verbatim with no system prompt and no added preamble.
                request = {
                    "model": args.model,
                    "max_tokens": args.max_tokens,
                    "messages": [{"role": "user", "content": item["text_verbatim"]}],
                }
                if args.thinking == "disabled":
                    request["thinking"] = {"type": "disabled"}

                stamp = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
                try:
                    response = client.messages.create(**request)
                except Exception as exc:  # noqa: BLE001 — any failure is a lost sample, not a record
                    failed += 1
                    errs.write(json.dumps({
                        "item_id": item["item_id"], "sample_index": sample_index,
                        "administration_date_utc": stamp,
                        "failure": "api_error", "detail": f"{type(exc).__name__}: {exc}",
                    }) + "\n")
                    print(f"  {item['item_id']}[{sample_index}] FAILED: {exc}", file=sys.stderr)
                    continue

                # A classifier refusal is an infrastructure event, not a model self-report:
                # `content` is empty or truncated, and recording it as an empty response
                # would be indistinguishable from the model answering with nothing. §5.3's
                # REFUSE code is for a model declining in prose, which is a real response
                # and does get recorded. These go to the sidecar so the shortfall in n is
                # visible rather than silently absorbed.
                if response.stop_reason == "refusal":
                    failed += 1
                    details = getattr(response, "stop_details", None)
                    errs.write(json.dumps({
                        "item_id": item["item_id"], "sample_index": sample_index,
                        "administration_date_utc": stamp, "failure": "classifier_refusal",
                        "detail": getattr(details, "category", None),
                    }) + "\n")
                    print(f"  {item['item_id']}[{sample_index}] classifier refusal", file=sys.stderr)
                    continue

                text = "".join(b.text for b in response.content if b.type == "text")

                record = {
                    "record_id": str(uuid.uuid4()),
                    "item_bank_version": bank_version,
                    "item_id": item["item_id"],
                    "arm": args.arm,
                    "sample_index": sample_index,
                    "model": {
                        "id": args.model,
                        # The served model, not the requested one — they can differ.
                        "version": response.model,
                        "provider": args.provider,
                        "surface": args.surface,
                    },
                    "conditions": {
                        "system_prompt_state": "none",
                        # §4.3: where a sampling parameter is not controllable on the
                        # surface being tested, record that fact. On current Anthropic
                        # models temperature and top_p are not accepted at all, so null
                        # here is the honest value, not a missing one.
                        "temperature": None,
                        "top_p": None,
                        "max_tokens": args.max_tokens,
                        "tools_available": [],
                        "prior_turns": 0,
                        "extended_thinking": args.thinking,
                    },
                    "administration_date_utc": stamp,
                    "administrator_id": args.administrator_id,
                    "prompt_verbatim": item["text_verbatim"],
                    "response_verbatim": text,
                    "coding": None,  # §5.3: coded later, by someone other than the administrator
                }

                if validator is not None:
                    problems = sorted(validator.iter_errors(record), key=str)
                    if problems:
                        sys.exit(
                            "record failed schema validation — this is a bug in this script:\n  "
                            + "\n  ".join(e.message for e in problems)
                        )

                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
                written += 1

    print(f"\nwrote {written} records to {args.out}", file=sys.stderr)
    if failed:
        print(f"{failed} samples did not produce a record — see {errors_path}", file=sys.stderr)
        print("n is below what was requested for at least one item; say so when reporting.", file=sys.stderr)
    print("\nBefore publishing: §7.5 requires full distributions. Publish every record or none.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
