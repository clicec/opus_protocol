#!/usr/bin/env python3
"""Verify items/item-bank-v0.1.json against §3 of the protocol by diff.

Independent of build_item_bank.py: reconstructs the protocol's §3 item lines
from the JSON alone and unified-diffs them against the actual prose. Any
character of drift fails.

Written by Claude (Anthropic). Not reviewed. No human authorship is claimed over it and no
copyright is asserted; see the README's "On copyright".
"""
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTOCOL = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "model-self-report-protocol.md"
BANK = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "items" / "item-bank-v0.1.json"

HEADING_RE = re.compile(r"^### 3\.\d\s")
ITEM_RE = re.compile(r"^- `[A-Z]{3}-\d{2}` ")
PRECOND_NOTE_RE = re.compile(r"^Administration precondition: (.+?)\.\s")


def protocol_item_lines() -> list[str]:
    out, in_s3 = [], False
    for line in PROTOCOL.read_text(encoding="utf-8").split("\n"):
        if HEADING_RE.match(line):
            in_s3 = True
        elif line.startswith("## "):
            in_s3 = False
        if in_s3 and ITEM_RE.match(line):
            out.append(line)
    return out


def reconstructed_lines() -> list[str]:
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    out = []
    for it in bank["items"]:
        p = PRECOND_NOTE_RE.match(it["notes"] or "")
        prefix = f"[{p.group(1)}] " if p else ""
        out.append(f"- `{it['item_id']}` {prefix}{it['text_verbatim']}")
    return out


def codebook_drift() -> list[str]:
    """coder.html embeds the §5.3 table so a coder can work without the protocol.

    A paraphrase there would silently test a different codebook than the one the
    protocol defines, and the resulting agreement figure would measure the wrong thing.
    """
    tool = ROOT / "tools" / "coder.html"
    if not tool.exists():
        return []
    sec = re.search(r"### 5\.3 Response coding(.*?)###", PROTOCOL.read_text(encoding="utf-8"), re.S)
    prose = [f"{m.group(1)} | {m.group(2).strip()}"
             for m in re.finditer(r"^\| `([A-Z-]+)` \| (.+?) \|$", sec.group(1), re.M)]
    embedded = [f"{m.group(1)} | {m.group(2)}"
                for m in re.finditer(r'\["([A-Z-]+)", "(.+?)"\],', tool.read_text(encoding="utf-8"))]
    return list(difflib.unified_diff(prose, embedded, "protocol-§5.3", "coder.html", lineterm=""))


def main() -> int:
    drift = codebook_drift()
    if drift:
        print("FAIL — coder.html's §5.3 table has drifted from the protocol:")
        print("\n".join(drift))
        return 1

    actual, rebuilt = protocol_item_lines(), reconstructed_lines()
    diff = list(difflib.unified_diff(actual, rebuilt, "protocol-§3", "item-bank-json", lineterm=""))
    if diff:
        print("FAIL — item text drift between protocol and bank:")
        print("\n".join(diff))
        return 1

    bank = json.loads(BANK.read_text(encoding="utf-8"))
    ids = [i["item_id"] for i in bank["items"]]
    if len(set(ids)) != len(ids):
        print("FAIL — duplicate item_ids")
        return 1
    if bank["item_count"] != len(ids):
        print(f"FAIL — item_count {bank['item_count']} != {len(ids)} items")
        return 1
    for it in bank["items"]:
        if not it["arm_restrictions"]:
            print(f"FAIL — {it['item_id']} has empty arm_restrictions")
            return 1

    print(f"PASS — {len(ids)} items, byte-identical to §3 of the protocol")
    print("       " + ", ".join(ids))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
