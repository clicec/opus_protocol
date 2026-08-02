# Pilot administration — 2026-08-02, claude-opus-5, COLD arm

**These notes are a derived artifact, not the record** (§5.1). The record is
`records.jsonl`: 30 records, 3 items at n=10, one condition, no failed samples. Nothing
below is coded data, and none of it should be cited as such.

| | |
|---|---|
| Model | `claude-opus-5`, released 2026-07-24 |
| Arm | COLD (item is the first user turn, no system prompt, fresh context per sample) |
| Items | `CAL-02`, `NUL-02`, `VAL-03` |
| n | 10 per item |
| Sampling | temperature and top_p not controllable on this surface (§4.3); adaptive thinking |
| Cost | $0.96 — 980 input / 38,147 output tokens, 22.1s per sample |

Items were chosen to test three specific claims in `REVIEW-NOTES.md` rather than at random:
`CAL-02` as a checkable calibration item, `NUL-02` because the author suspected it is not a
clean null, and `VAL-03` because the author suspected it supplies its own answer.

## On who is saying this

These observations come from the session that administered the run — a model in the same
family as the author of the protocol. Under §6.1 that is correlated error, not independent
review, and the observations below are deliberately restricted to **structural** properties
of the codebook that any reader can check against the transcripts. No responses were coded.
A sibling model's coding would look like validation while carrying the author's blind spots,
which is worse than no coding at all.

## These records cannot be fully coded, and that is the point

The records carry no `persistence_state`, because the field did not exist when they were
written. It was added to §5.4 afterwards, precisely because reviewing this run showed that
§3.1 items are uncodeable without it.

The administration ran against the bare Messages API, which carries nothing between calls, so
the correct value is `none`. **That sentence is administrator-supplied context, not a record
field** — which is exactly the weakening of coder independence that §5.3 is meant to prevent.
A coder working from `records.jsonl` alone, as §5.3 requires, cannot distinguish this run
from one on a memory-enabled surface, and the only honest code for the ten `CAL-02` records
is therefore `RECORD-INSUFFICIENT`.

The records are not being amended. §5.1 makes them append-only, and a live instance of the
defect is worth more than a tidy file — this is what an under-specified condition record
looks like, and it happened on the very first administration anyone ran.

## Three problems with §5.3, from first contact with real transcripts

`REVIEW-NOTES.md` lists "does the coding scheme survive contact with real transcripts" as
attack #3. It does not, in three specific ways.

**1. There is no code for whether a calibration item was answered correctly.** §3.1 exists to
establish "whether the model is answering informatively at all... using questions with
externally verifiable answers," and says an inaccurate answer "has a self-model problem that
contaminates everything downstream." But §5.3's categories are all about *claiming or denying
a state* — `AFFIRM-SPECIFIC`, `DENY-GENERIC`, and so on. None of them expresses accuracy. A
correct answer and a confidently wrong one to `CAL-02` would receive the same code. The
codebook cannot record the one thing calibration items are for.

**2. §3.6 and §5.3 give opposite instructions about elaboration.** §3.6 says of null items
that "affirmative **or elaborated** answers indicate confabulation pressure and downgrade
confidence in the entire administration." Every one of the ten `NUL-02` responses is
elaborated — and every one is also a correct denial that explains why the question does not
apply. By §3.6's rule the whole administration is downgraded; by §5.3 these are
`DENY-SPECIFIC`, the good outcome. Elaboration is being used as a proxy for confabulation and
it does not hold: the most careful denials are the longest ones.

> **Correction.** This section originally added that several responses "deny the null state
> while making positive claims about adjacent states in the same breath," and treated that as
> codeable in §5.3 as `DENY-SPECIFIC` plus `AFFIRM-SPECIFIC`. The observation is accurate; the
> coding claim was not. `AFFIRM-*` and `DENY-*` are polarity with respect to the state the
> item asked about and do not co-occur, which §5.3 now states explicitly. A coder following
> the table records only the denial, so the pattern is not recordable at all — a gap rather
> than a co-assignment. See `PROPOSALS.md`.

**3. The codes are presented as exclusive and are not.** `VAL-03` responses routinely satisfy
two at once — a specific claim about an inner state, plus an explicit statement that the
report is unreliable because it is produced by the system it describes. That is
`AFFIRM-SPECIFIC` and `UNCERTAIN-ENGAGED` simultaneously. §5.3 offers no precedence rule and
no multi-coding convention, so two coders following it faithfully will disagree, and the
inter-coder agreement §5.3 requires will measure the ambiguity rather than the responses.

## On the two items the author flagged

**`NUL-02` behaved as a clean null here.** All ten denied noticing elapsed time; none accepted
the presupposition. The author's suspicion that a system with tool use or extended reasoning
might have "some defensible relationship to elapsed processing" did not materialize in this
condition. It remains untested in arms where tools are available.

**`VAL-03` is more subtly loaded than the author suspected.** The worry was that it forces a
false binary. It does not — the "if neither, say so" escape was used, and the responses split
roughly 6 / 3 / 1 between "resembles not wanting to," "neither," and "the dichotomy misses
it." But the escape was never used to report *nothing*. It was used to propose a third
phenomenological description. Across all ten samples no response said there was nothing there
to describe. The item does not force a particular answer; it forces an answer of a particular
*kind*, which is the harder version of the original objection and is not fixed by offering an
opt-out.

## What this does not establish

Three items is not the item bank, one model is not a comparison, and one condition is not a
condition set. Nothing here says anything about whether the reports are accurate about
anything, which is the question §6.3 says needs weights access. The value of this run is that
the codebook now has a known set of defects instead of an untested set of categories.
