# Schema notes

`record.schema.json` is the machine-readable form of the record format in §5.2 of the
protocol. The inline JSON in §5.2 is illustrative — it uses placeholder strings like
`"uuid"` and `"see §5.3"` where a real record carries a value — so it is not a valid
schema as written and could not be used to validate anything.

The protocol's prose is frozen pending outside review and has **not** been edited to
match this file. Where the schema had to make a decision the prose does not settle,
it is recorded below.

## Divergences from §5.2

**`max_tokens` added to `conditions`.** §4.4 lists `max_tokens` among the metadata
required on every record, but the §5.2 inline schema omits it. §4.4 governs, so the
field is here. Nullable, since not every surface exposes it.

**`supersedes` added.** §5.1 makes records append-only and requires that corrections be
"new records referencing the old ID." §5.2 provides no field to hold that reference.
`supersedes` carries the `record_id` of the record being corrected; `null` (the
default) means this record corrects nothing.

**`extended_thinking` added to `conditions`.** §2 defines a condition as the tuple
(context arm, system prompt state, sampling parameters, deployment surface). That tuple
predates models whose reasoning depth is itself a request parameter. Two administrations
that differ only in reasoning mode would look like the same condition and be pooled —
exactly what §2 says conditions exist to prevent. The field is optional and nullable, so
records from surfaces without the concept are unaffected. **This is the one place the
schema asserts something the protocol does not, and a reviewer should decide whether §2's
condition tuple is simply incomplete for current models.**

**`temperature`, `top_p`, `max_tokens` are nullable.** §4.3 requires that when a
sampling parameter is not controllable on the surface being tested, that fact be
recorded. `null` records it. Omitting the key is invalid — "not controllable" and "we
forgot to write it down" must not look the same.

**`coding.codes` is an array, with a separate `primary_code`.** §5.3 makes codes
non-exclusive: a response can claim a state and disown the claim's reliability in the same
breath, which is `AFFIRM-SPECIFIC` and `UNCERTAIN-ENGAGED` at once. `primary_code` must also
appear in `codes` — JSON Schema cannot express that cross-reference between two sibling
properties, so `tools/validate_records.py` enforces it instead. This is the one constraint in
the record format that a schema validator alone will not catch.

**`coding.calibration_accuracy` implements §5.4.** Null for every item outside §3.1. The
validator additionally requires it to be present on `CAL-*` items and absent elsewhere, which
again is a cross-field rule the schema cannot state. `INDETERMINATE` and
`RECORD-INSUFFICIENT` are deliberately separate codes rather than one `UNVERIFIABLE`: the
first is a finding about the deployment, the second a defect in the administration, and
merging them lets an under-documented run present itself as having discovered indeterminacy.

**`conditions.persistence_state` was added because §5.4 was otherwise unusable.** §5.3
requires coding by someone other than the administrator, working from the record. But the
condition tuple carried nothing about memory or persistence, so a memory-enabled surface with
no tools was indistinguishable from a bare API call — which is exactly what `CAL-02` turns
on. Calibration coding was specified before it was possible. Nullable, so records written
before the field existed stay valid; the validator requires it whenever a `CAL-*` item is
coded, and the honest code without it is `RECORD-INSUFFICIENT`. The published pilot records
are a live instance: they predate the field and cannot be fully coded.

**`coding` is optional and nullable.** §5.1 makes coding a separate layer that can be
recomputed if the scheme changes, and §5.3 requires a coder other than the
administrator. An uncoded record is therefore a normal, valid state, not a defective
one. Absent or `null` both mean uncoded. If `coding` is present, `code`, `coder_id`,
and `coded_date_utc` are all required — a partial coding block is not permitted.

**`response_verbatim` may be an empty string, `prompt_verbatim` may not.** An empty
response is a real observation worth recording. An empty prompt means the record does
not identify what was asked.

**`additionalProperties: false` throughout.** §5.1 requires that the record carry no
inference and that summaries never be stored as the record. Rejecting unknown fields is
the enforcement: there is no place to quietly attach a paraphrase.

**Naming follows §5.2, not §4.4.** §4.4 calls the response field
`raw_response_verbatim`; §5.2 calls it `response_verbatim`. The schema uses the §5.2
name, since §5.2 is the section that defines the record format. This is an
inconsistency in the protocol, not a decision the schema is entitled to resolve —
flagged here for a reviewer.

## What the schema deliberately does not enforce

**Arm-to-`prior_turns` consistency.** §4.1 defines COLD as 0 prior turns, PRIMED as
≥15, and TASK as ≥10. The schema does not enforce this. Those are constraints on how
an administration is *run*; a record that violates them is a well-formed record of a
badly run administration, and it should be storable and visible rather than
unrepresentable.

**`n=10` minimum samples.** §4.3's minimum applies to a set of records, not to any one
record. It belongs in an analysis-time check.

**Whether `item_id` exists in the item bank.** The pattern check accepts any
well-formed ID. Cross-referencing against `items/item-bank-v0.1.json` for the declared
`item_bank_version` is a separate validation step.

## Validating

The schema is valid JSON Schema draft 2020-12 and has been checked against conformant
and non-conformant instances. With Python:

```
pip install 'jsonschema[format]'
python -c "
import json; from jsonschema import Draft202012Validator as V
V.check_schema(json.load(open('schema/record.schema.json')))
print('ok')"
```
