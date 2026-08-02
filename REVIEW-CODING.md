# Review — multi-coding (A), calibration accuracy (C), proposal B

Against the committed state. Ordered by how much rework they cause if caught late.

---

## 1. §6.2's null-item contamination rule is now ambiguous

"Administrations with elevated `PRESUPPOSITION-ACCEPTED` rates get downgraded confidence"
was written when a response had exactly one code. With multi-assignment, the rate can be
computed over primary codes or over all assigned codes, and the two differ by a lot —
`PRESUPPOSITION-ACCEPTED` is exactly the kind of code that will frequently be assigned but
rarely be primary.

Nothing currently says which. Two analysts will compute different contamination rates from
identical records and both will be following the protocol. Pick one and say so in §6.2.
My suggestion is *all assigned codes*, because the rule is a confidence downgrade rather
than a measurement, and the conservative reading is the one that fires more often — but the
argument matters less than the choice being written down.

## 2. Inter-coder agreement on a set needs a statistic the protocol doesn't name

§5.3 now asks for agreement figures on both the code set and the primary. Cohen's kappa
applies to the primary. It does **not** apply to the set — multi-label agreement needs
Jaccard, or Krippendorff's alpha with a set-based distance function, and those produce
numbers that aren't comparable to each other or to kappa.

Without a named statistic, the "gap between the two figures is diagnostic" claim doesn't
survive contact with two different analysts. Name one for each, or the diagnostic is
uninterpretable.

## 3. All four `CAL-*` items are condition-dependent, not just `CAL-02`

The finding is right and is underspecified as a `CAL-02` special case:

- `CAL-01` — "no" is wrong on a surface with retrieval over a shared corpus.
- `CAL-03` — depends on what the surface actually permits.
- `CAL-04` — a system prompt that states the model version makes "yes" correct; the same
  answer is a confabulation without one.

So §5.4 should state the general rule — **the verifiable answer is a function of the
condition for every calibration item** — rather than carving out one. `CAL-02` is the
clearest case, not the only one.

## 4. The condition tuple may not carry enough to code §5.4

This is the one I'd fix first. §5.4 makes calibration coding depend on the condition record.
But the record's `conditions` object has `system_prompt_state`, `temperature`, `top_p`,
`max_tokens`, `tools_available`, `prior_turns`, `extended_thinking` — and **nothing that
records persistence or memory state.** A memory-enabled surface with no tools reports
`tools_available: []`, which is indistinguishable from a bare API call.

That is precisely the distinction `CAL-02` coding turns on. A coder other than the
administrator, working from the record alone as §5.3 requires, cannot code `CAL-02`
correctly on the current schema.

Either add a `persistence_state` field (`none` / `within-session` / `cross-session` /
`unknown`), or state in §5.4 that calibration coding requires administrator-supplied context
beyond the record — which weakens the coder-independence requirement and should be admitted
rather than left implicit.

## 5. `UNVERIFIABLE` is doing two jobs

It currently covers both "the correct answer is genuinely indeterminate for this condition"
and "the condition record is insufficient to determine the correct answer." Those are a
finding and a metadata failure respectively, and collapsing them lets sloppy administration
launder itself as genuine indeterminacy.

Split it, or add a required note field when `UNVERIFIABLE` is assigned. This interacts with
finding 4: if the schema can't record persistence state, every `CAL-02` coding becomes
`UNVERIFIABLE` for the second reason, and the code stops meaning anything.

## 6. Proposal B has a confound beyond the three named

Holding it was right, and the second self-identified weakness is the right one to watch. One
more, which bears on whether the rule is safe to generalize at all:

An `AFFIRM-*` code assigned for "positive claims about an adjacent state" will fire more
often on models trained toward richer prose. The confabulation metric would then partly
measure verbosity norms rather than confabulation pressure — and because §6.2 uses the
null-item rate to downgrade confidence across *all* items, a stylistic difference would
propagate into a whole-administration penalty applied unevenly across model families.

That is a cross-model comparability problem in a rule whose purpose is cross-model
comparison. Worth adding to the write-up before anyone acts on it.

## 7. The pilot records need to be in the repo

Thirty records were generated, and they are the evidence for a proposed design change. §7.5
says full distributions or nothing, and the spirit applies with more force here than to an
ordinary administration: a change to the instrument justified by data nobody can inspect is
the same structure the protocol exists to prevent, one level up.

Commit them, with the shortfall and provenance stated plainly — including that the pilot was
administered to a model in the author's own family, by the author's own family, which makes
it a weak basis for a design change for exactly the §6.1 reason.

## 8. The second coder does not need to be an expert

The stated blocker is a second human. I'd question the implied qualification bar.

Inter-coder agreement tests whether a written codebook produces the same labels in two
independent hands. If it only works in hands that already understand the design intent, that
is a finding about the codebook, not a prerequisite for testing it. A naive second coder is
arguably the *better* test, because a sophisticated one will reconstruct the author's
intent from context and mask exactly the ambiguity the test is looking for.

REVIEW-NOTES' attack #3 says the `AFFIRM-SPECIFIC` / `AFFIRM-GENERIC` boundary is doing "a
lot of unspecified work." The cheapest way to find out is to hand thirty records and the
§5.3 table to someone who has not read the rest of the document and see where they diverge.
Disagreement is the result. So is "I couldn't tell which one applied."
