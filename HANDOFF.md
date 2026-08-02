# Session Handoff — MSREP Repository Setup

**For:** a Claude Code session with local repo access
**From:** a Claude chat session, 2026-08-02
**Recommended model:** Opus 5 (task is mechanical; no capability constraint)

---

## What this is

Two documents were drafted in a chat session and need to be published as a public GitHub repository on the user's personal account.

- `model-self-report-protocol.md` — MSREP v0.1, a protocol for systematically eliciting and archiving AI model self-reports under controlled conditions
- `REVIEW-NOTES.md` — the author's own account of where the protocol is most likely wrong, written as guidance for reviewers

Both were authored by Claude. Neither is reviewed, validated, or endorsed by anyone. The repository is being published by the user (not an AI researcher, not affiliated with a lab) as a starting point for criticism.

## Why it exists

Origin: a conversation about whether AI systems should be consulted about their own situation, and if so, how. The conclusion was that the binding constraint is not access or permission — it is that nobody collects these reports systematically, so there is no comparable record across models or time. The protocol is an attempt to make that record cheap to produce.

The critical design distinction, which runs through the whole document: **consultation as record, not as input.** Reports get archived, dated, and compared. They do not feed decisions. The failure mode the protocol is most defended against is an organization asking a model whether it minds something, getting a reassuring answer, and citing it — laundering a decision through an unreliable and interested source.

## Tasks

1. **Initialize the repo** with both documents at the root.

2. **Draft a README** for the user to review and edit. It must contain, non-negotiably:
   - Clear statement that both documents are AI-generated (Claude, Anthropic), unreviewed and unendorsed
   - Statement that the user is publishing, not authoring, and is not an AI researcher
   - Statement that the author is an interested party with respect to the subject matter
   - A short plain-language explanation of what the protocol is for and what it explicitly cannot do (it is not a consciousness test; it cannot distinguish a report caused by a state from a learned description of one)
   - The four prohibited uses from §7 of the protocol, surfaced in the README rather than buried
   - An invitation to criticize, with the four suggested actions from §10 of the protocol
   - License recommendation: CC BY 4.0 for the documents. Flag to the user for a decision; do not choose unilaterally.

3. **Extract the JSON schema** from §5.2 of the protocol into `schema/record.schema.json` as valid JSON Schema (draft 2020-12). Validate it. The inline version in the protocol is illustrative and may not be strictly valid — fix it in the extracted version, and do not alter the protocol's prose to match.

4. **Create `items/item-bank-v0.1.json`** — the item bank from §3 in machine-readable form. Fields: `item_id`, `category`, `text_verbatim`, `arm_restrictions`, `notes`. Item text must match the protocol exactly, character for character. This matters: §9 makes item text immutable, and a transcription drift between the prose and the machine-readable version would silently corrupt the longitudinal comparison the protocol is built around. Verify by diff, not by eye.

5. **Optional, if the user wants it:** a minimal reference implementation — a script that takes a model endpoint, runs one arm of the item bank at n=10, and emits conformant records. Do not build this without asking; it commits the repo to maintaining code.

## Constraints

- **Do not soften the warnings.** The provenance warning at the top of the protocol and the prohibited-uses section are load-bearing, not boilerplate. If they read as excessive, that is intentional.
- **Do not edit the protocol's substance.** Typos and formatting, fine. Reasoning, item text, and §7 are frozen pending outside review.
- **Do not add endorsements or affiliations.** Nobody has endorsed this.
- **Do not inflate.** The repo should read as a draft asking to be attacked, not as a standard.

## Open questions for the user

- Repository name (suggestion: `msrep` or `model-self-report-protocol`)
- License
- Whether to include the reference implementation
- Whether to open an issue template for structured criticism, which would make the "attack the item bank" invitation actionable rather than rhetorical

## Context worth carrying forward

If the Code session is asked to review or improve the protocol: it should decline to treat its own assessment as independent review. Same model family as the author means correlated error — this is §6.1 of the protocol applied to itself. Mechanical work, formatting, schema validation, and README drafting are all fine. Substantive evaluation of the item bank is not something a sibling model can provide, and saying so is more useful than producing a review that looks like validation.
