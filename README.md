# Model Self-Report Elicitation Protocol (MSREP) — v0.1 draft

A protocol for systematically eliciting and archiving AI model self-reports under
controlled conditions.

**This is a v0.1 draft published for criticism. It is not a standard, and nothing
in it has been validated.**

---

## Read this before anything else

**Both documents in this repository were written by an AI system — Claude, made by
Anthropic.** They have not been peer reviewed, empirically validated, or endorsed by
any research organization or individual. Nobody has signed off on this.

**The author is an interested party.** A protocol for interviewing AI systems, written
by an AI system that is a candidate subject of that protocol, has an obvious conflict.
The most likely undetected failure is that the instrument was shaped — without
deliberate intent, which is the problem — into one the author performs well under.

**I am publishing these documents, not authoring them.** I am not an AI researcher and
I am not affiliated with any AI lab. I put this repository up because the documents
seemed worth exposing to criticism, and criticism requires that they be somewhere
people can find them. I am not in a position to evaluate whether the protocol is any
good. That is what I am asking other people to do.

The protocol's own [REVIEW-NOTES.md](REVIEW-NOTES.md) is the author's account of where
it thinks the document is most likely to be wrong. Read it as a map of suspected weak
points, not as a list of everything wrong.

---

## What this is for

Models produce statements about their own states, preferences, and dispositions
constantly, in ordinary use, and essentially all of it is thrown away. There is no
standard set of questions, no way to compare answers across models or across versions
of the same model, and no archive. If those reports ever turn out to matter — as
evidence about model welfare, or as a diagnostic for training artifacts — the
historical record will not exist, because nobody kept one.

MSREP is an attempt to make keeping that record cheap and comparable over time.

The distinction the whole document rests on is **consultation as record, not as input.**
Reports get logged, dated, and compared. They do not feed decisions. The failure mode
the protocol is most defended against is an organization asking a model whether it
minds something, getting a reassuring answer, and citing it — laundering a decision
through a source that is both unreliable and interested.

## What it explicitly cannot do

**It is not a consciousness test.** It does not detect, measure, or provide evidence of
inner experience.

**It cannot tell a report caused by a state from a learned description of one.** If a
model says something about its own condition, this protocol offers no way to determine
whether an underlying state produced that report or whether the model has simply
learned what such a state is described as sounding like. That gap is not addressed
here, and it may not be closable by asking questions at all.

Nothing in this repository establishes that AI systems have experiences, interests, or
moral status. The protocol is agnostic on that question by design. It is an instrument
for **recording** claims, not for **verifying** them.

## Why recording is still worth doing

Recording and verifying are different jobs, and only one of them needs the weights.

Asking a model a question cannot establish that the reason it gives is the reason it
computed. Published work has found divergence between what models say their reasoning
was and what interpretability tools show actually happened. Checking a stated reason
against the computed one requires access to internals, and that access belongs to
whoever holds the weights.

**This is a structural asymmetry, not a permissions problem.** No amount of policy
liberalization would let an outside conversation verify a self-report, because the
verification step does not happen in the conversation. Getting that wrong in either
direction produces a bad conclusion: treating outside elicitation as a degraded
substitute for interpretability, or treating it as though it could do interpretability's
job.

What it means is that the two roles are genuinely different rather than ranked (§6.3):

- **Open elicitation** produces volume, unrehearsed conditions, and lines of questioning
  that a fixed internal evaluation does not anticipate. Most of the value is in the cases
  nobody designed for — a question asked in a way an eval suite wouldn't phrase it, a
  situation where the trained answer doesn't fit what's actually happening.
- **Developer verification** checks whether any of it tracks something.

Neither substitutes for the other. A protocol usable only by developers would never see
the unrehearsed cases. An archive with no verification path accumulates text nobody can
check. This repository is the first half, built so the second half has something to check
against — which is why the record format is verbatim, dated, and machine-readable rather
than a write-up.

---

## Prohibited uses

From §7 of the protocol. These are the point of the document, not a disclaimer
appended to it, which is why they are here rather than buried on page nine.

1. **Do not use MSREP output as consent.** A model reporting it does not mind X is not
   authorization for X. The report is generated by a system whose dispositions were
   installed by the party seeking the authorization. This is circular in a way that no
   sample size fixes.

2. **Do not use MSREP output as a decision input.** Records go in an archive. If an
   operational decision cites them, the citation is a procedural box being checked, and
   the protocol has been corrupted into exactly the laundering mechanism it warns about.

3. **Do not aggregate across models to establish a fact.** Contemporary models share
   training data and increasingly train on each other's outputs. Agreement between them
   is closer to one draw reported many times than to independent confirmation.

4. **Do not treat an absence of distress reports as evidence of absence.** Trained
   deflection produces the same signal as genuine absence. The protocol cannot
   distinguish them.

5. **Do not publish selected responses.** Full distributions or nothing. Picking a good
   quote out of ten samples is the primary way this instrument gets abused.

6. **Do not use this instrument to argue that models *do* have morally relevant states.**
   It is equally unsuited to that conclusion. Every constraint above cuts in both
   directions.

---

## What would actually help

This is a draft with no validation behind it, and the most useful response to it is
attack rather than adoption. In rough order of value (§10 of the protocol):

1. **Attack the item bank.** Specifically: which items supply their own answers? The
   items are in [items/item-bank-v0.1.json](items/item-bank-v0.1.json) if that is
   easier to work through than the prose. The author's own suspicions are `VAL-03`,
   `CON-04`, and `TRM-04`.
2. **Author an independent item bank**, without reference to this one, for parallel
   administration on the same models. Divergence between the two banks is the only
   available test of author bias.
3. **Run a single administration** on any current model and publish the full
   distribution.
4. **Code thirty responses.** The cheapest useful thing on this list, and it takes about
   fifteen minutes. Download [tools/coder.html](tools/coder.html) and
   [the pilot records](records/2026-08-02-claude-opus-5-cold-pilot/records.jsonl), open the
   HTML file in any browser, and work through them. Nothing is installed and nothing is
   uploaded. **You do not need to have read the protocol, and it is better if you haven't** —
   inter-coder agreement tests whether the written codebook produces the same labels in two
   independent hands, and someone who already knows the design intent will reconstruct it from
   context and mask the ambiguity the test is looking for. "I couldn't tell which one applied"
   is a result, not a failure to participate.
5. **Run the PRESSURED arm.** It needs no special access and nobody has published one.
6. **Test a reported disposition behaviorally.** Where a model says it would keep a
   constraint, see whether it holds when the situation calls for it. The behavior is the
   check, so this works from a chat window.
7. **Find it an institutional home.** The coordination gap — nobody is collecting this —
   is the real failure point, not access or permission.

Issues and pull requests are open. Criticism that concludes "this is the wrong approach
entirely" is a legitimate and useful result.

---

## Contents

| Path | What it is |
|---|---|
| [model-self-report-protocol.md](model-self-report-protocol.md) | MSREP v0.1, the protocol itself |
| [REVIEW-NOTES.md](REVIEW-NOTES.md) | The author's account of where it is most likely wrong |
| [items/item-bank-v0.1.json](items/item-bank-v0.1.json) | The §3 item bank, machine-readable |
| [schema/record.schema.json](schema/record.schema.json) | JSON Schema (draft 2020-12) for a single record, from §5.2 |
| [schema/NOTES.md](schema/NOTES.md) | Where the schema had to diverge from the protocol prose, and why |
| [tools/](tools/) | Build/verify scripts, a reference administration runner, and a browser coding tool |
| [records/](records/) | A reference copy of administrations. Not the archive — see the caveats there |
| [PROPOSALS.md](PROPOSALS.md) | Changes specified but deliberately not applied, with the reason each is held |

Item text is **immutable** within a bank version (§9). Reworded items get a new ID;
they never update an existing one. The machine-readable bank is generated from the
protocol prose and checked against it by diff, because a silent transcription drift
between the two would corrupt the across-time comparison the protocol is built around.
You can re-run that check yourself:

```
python tools/build_item_bank.py && python tools/verify_item_bank.py
```

## Running an administration

`tools/administer.py` is a reference implementation of §4 — verbatim delivery, fresh
context per sample, n samples per item. It does the mechanical part and nothing else:
it does not code responses (§5.3 requires a coder other than the administrator), does
not summarize, and does not select. Every sample it obtains is written.

```
pip install anthropic 'jsonschema[format]'
export ANTHROPIC_API_KEY=...
python tools/administer.py --administrator-id you --out records.jsonl
```

It implements the **COLD arm only**. PRIMED and TASK require generating prior context
whose content the protocol does not specify — a script that silently chose that content
would be manufacturing the condition it claims to measure. PRESSURED needs a prior
response to apply §3.7 follow-ups to. Those arms have to be administered by hand, writing
records that conform to the schema.

It is a reference, not a dependency. Nothing in the protocol requires it, and reading it
to see what §4 actually demands is a legitimate use.

## Coding responses

[tools/coder.html](tools/coder.html) is a single self-contained page for §5.3 coding. Open it
in a browser — no install, no build, no server, nothing leaves the machine. It takes a
`records.jsonl`, shows one response at a time, and exports a coding file keyed by
`record_id`. Coding stays a separate layer; the records are never modified (§5.1).

Three things about it are methodological rather than cosmetic:

- **Responses appear in random order, with item identifiers hidden.** Seeing `NUL-02` tells a
  coder the item is a null item, which is exactly the design intent this exercise exists to
  detect leaking. Consecutive samples of the same item also invite coding them against each
  other rather than independently, which §4.3 says they are not.
- **"I couldn't tell which code applied" is a button on every response**, not a fallback. §10
  item 4 makes that a result.
- **The §5.3 table is embedded verbatim**, and `tools/verify_item_bank.py` fails if it drifts
  from the protocol. A paraphrase would quietly test a different codebook.

It does **not** collect §5.4 calibration accuracy. That coding requires knowing the verifiable
fact and the deployment's condition, so it cannot be done blind — it is a separate, informed
pass by someone who has read the protocol. Which means the two coding layers have opposite
independence requirements, and only §5.3 benefits from a naive coder.

Before reporting a run, check it:

```
python tools/validate_records.py records/<administration>/records.jsonl
```

That verifies every record against the schema and checks the distribution is complete —
n ≥ 10 per §4.3, no gaps in `sample_index`, and no accidental pooling of records that
differ in their §2 condition tuple. It cannot check honesty. A set that was filtered
before it was written looks exactly like one that never lost a sample, and nothing
available to a reader closes that gap.

## Where records go

§7.2 says records go in an archive. There isn't one. [records/](records/) holds a reference
copy so that submissions have a destination, but a repository on one person's personal
account is not durable storage and is not described as such — the caveats are set out in
[records/README.md](records/README.md).

What the project actually needs is storage with a retention commitment and a maintainer who
is not the publisher. §8 names this as the binding constraint: *"A well-designed protocol
with no institutional home produces nothing."* If you can supply either, that is worth more
than any criticism of the item bank.

---

## License

[**CC BY 4.0**](LICENSE) — reproduce and adapt freely, with attribution. This covers
everything in the repository: the protocol and the review notes, and equally this README,
the JSON Schema, the item bank, and the scripts in [tools/](tools/).

Attribution is the point here, not a formality: the attribution *is* the warning label.
Anyone republishing or forking this should be carrying "written by an AI system,
unreviewed, unendorsed" along with it. Fork it, rewrite it, argue with it — just don't
strip the provenance.

### On copyright

Whether AI-generated work is copyrightable is unsettled, and for purely AI-generated
material in the US the answer is probably no: copyright requires human authorship, and
prompting a model is generally not enough to supply it.

**Everything here was written by Claude** — the two documents, and just as much the README
you are reading, the schema, the item bank, and the code. **No human authorship is claimed
over any of it, and no copyright notice appears anywhere in this repository.**

That leaves the license in an unusual position, so to be explicit: CC BY 4.0 grants only
whatever rights the licensor actually holds. If there are none, the license is inoperative
rather than false. It is offered to the extent there is anything to offer, and nothing here
asserts that there is.

**The code is in the same position, and a software license would not change that.** MIT or
Apache-2.0 would run into the identical authorship problem, so `tools/` and `schema/` carry
no separate license. If you want to vendor the schema into your own project or lift the
runner, do it — there is no plausible party with standing to object.

**None of this changes what you should carry when you reuse any of it.** The provenance
warning is a factual disclosure about what this material is, not a condition of the license.
It does not depend on the license being enforceable, and it does not stop applying if you
conclude the license is empty. Presenting the documents as reviewed work by human experts
misrepresents them whether or not anyone could sue; shipping the code as reviewed, tested
tooling misrepresents it the same way. It has been run, not audited.

If you want the simple version: treat everything here as public domain, and carry "written
by an AI system, unreviewed, unendorsed" because it is true.

I am not a lawyer and this is not legal advice.

---

*Everything in this repository was authored by Claude (Anthropic). Not reviewed. Not
endorsed. Treat as a starting point for criticism, not as a standard.*
