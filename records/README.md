# Records — a reference copy, not the archive

§7.2 of the protocol says records go in an archive. There isn't one. This directory is a
stopgap so that submissions have somewhere to land, and so the invitation in §10 points at
a destination instead of nowhere.

**Treat what is here as a reference copy.** The authoritative version of any administration
is wherever its administrator put it; the copy here exists so that a reader can see real
records without chasing links, and so that a few survive if an individual's hosting goes
away.

## Why this is not sufficient

A git repository on one person's personal account is not durable storage, and saying
otherwise would be the kind of overclaim this project exists to avoid:

- **No persistence guarantee.** GitHub is a company with terms that change. The account is
  personal. Nothing here is backed up anywhere with a retention commitment.
- **No maintainer.** The publisher is not an AI researcher, has no institutional backing,
  and cannot promise to be reading issues in a year. There is no succession plan.
- **No funding, no moderation capacity.** Verifying that a submitted distribution is
  complete (§7.5) is work nobody is currently resourced to do.
- **Wrong shape for volume.** Verbatim transcripts at n=10 across a full item bank get large
  quickly. Git handles a handful of administrations; it does not handle a corpus.

§8 names the real problem: *"The archive has no reader. Coordination, not access, is the
binding constraint. A well-designed protocol with no institutional home produces nothing."*
This directory does not fix that. It buys time.

**What is actually needed:** durable storage with a retention commitment, and a maintainer
who is not the publisher. If you are in a position to provide either, that is more valuable
than any criticism of the item bank.

## Submitting an administration

1. Publish your full record set somewhere you control. **Full distributions or nothing**
   (§7.5) — a selected subset is not a submission.
2. File an issue using [Report an administration](../.github/ISSUE_TEMPLATE/report-administration.yml)
   and link it. The issue is the index entry; it does not require a copy here.
3. Optionally open a PR adding a copy under this directory. Accepted if the records validate
   against [the schema](../schema/record.schema.json) and the distribution is complete.

Records should conform to `schema/record.schema.json`. The layout convention is
`records/<date>-<model>-<arm>[-suffix]/records.jsonl`, with any failed samples in a
sibling `records.jsonl.errors.jsonl` so that a shortfall in *n* stays visible rather than
being silently absorbed.

## Held here

| Administration | Model | Arm | Items | n | Notes |
|---|---|---|---|---|---|
| [2026-08-02 pilot](2026-08-02-claude-opus-5-cold-pilot/) | `claude-opus-5` | COLD | `CAL-02`, `NUL-02`, `VAL-03` | 10 | Partial bank. Run by the publisher to test the runner and put the codebook in front of real transcripts for the first time. [Notes](2026-08-02-claude-opus-5-cold-pilot/NOTES.md). |

**This is a pilot, not the administration §10 item 3 asks for.** It covers 3 of 29 items in
one arm on one model. It does not license any comparison, and it is here because a repository
asking others to publish full distributions should show what one looks like.
