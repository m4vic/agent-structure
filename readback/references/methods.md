# Methods

Readback is assembled from established practices for recording decisions under
uncertainty. None of them were invented here. This file records what each
contributes, what Readback took, and — more usefully — what it deliberately
refused, since most of these methods fail for a reason when applied to an agent.

---

## Architecture Decision Records

**Michael Nygard, *Documenting Architecture Decisions* (2011); Documenting
Software Architectures, SEI.**

The direct ancestor. Numbered, immutable records of Context / Decision /
Consequences. A decision is never edited once written; it is superseded by a new
record that references it.

**Taken:** immutability, sequential IDs, supersession-by-reference, and the rule
that consequences are recorded alongside the choice.

**Refused:** ADRs record only the *decision*. They have no concept of the
instruction that produced it or of the gap between what was asked and what was
built — an ADR written by a model that misunderstood you is a confident record
of the wrong decision. The `Asked` / `Readback` split exists because ADRs have no
place to put it.

---

## Decision journals

**Annie Duke, *Thinking in Bets*; Kahneman on hindsight bias.**

Write down the decision, the reasoning, and the expected outcome *at the moment
of deciding* — because once you know how it turned out, you can no longer
reconstruct what you actually believed beforehand. Outcome quality and decision
quality are independent, and hindsight silently merges them.

**Taken:** this is the entire reason `Readback` must be written **before**
implementing. A readback composed afterward is not a readback; it is a
justification, and it will unfailingly be more reasonable than what the agent
actually understood at the time.

**Refused:** decision journals score calibration over time. Readback does not
grade itself — a `Match` value is an observation, not a performance metric.

---

## Lab and engineering notebooks

**Standard research and patent practice.**

Contemporaneous, append-only, bound pages, written in ink. Errors are struck
through with a single line and initialed, never erased, because an erasure
destroys the evidentiary value of everything around it.

**Taken:** contemporaneous capture (write when it happens, never batch), and
strike-through-not-erase — Readback amends superseded entries in place rather
than rewriting them.

**Refused:** the notebook is a *human* discipline that survives on ritual.
Readback shifts the writing to the agent precisely because rituals requiring
human diligence at the end of a long session do not survive contact with a long
session.

---

## Zettelkasten

**Niklas Luhmann; Sönke Ahrens, *How to Take Smart Notes*.**

Atomic notes, each holding one idea, densely cross-linked, with structure
emerging from the links rather than from a pre-built hierarchy. An index exists
only as an entry point, not as a taxonomy.

**Taken:** one entry = one change, explicit `Supersedes` links, decision chains
as emergent structure, and `index.md` as an entry point rather than a
classification scheme.

**Refused:** Zettelkasten optimizes for *serendipitous connection* across a
lifetime. Readback optimizes for *targeted retrieval* under a token budget.
Emergent structure is good; unbounded growth is not, so entries are consolidated
and archived on a schedule that a Zettelkasten would consider vandalism.

---

## Textual criticism

**Stemmatics; the critical apparatus of a scholarly edition.**

The discipline of reconstructing what a text originally said from divergent
copies. Every variant reading is preserved alongside the witness that attests
it. A *stemma* maps how versions descend from one another, so any reading can be
traced to its source.

**Taken:** decision chains (`RB-004 → RB-012 → RB-027`) are stemmata. Variants
are never discarded, because determining which reading was correct often becomes
possible only later.

**Refused:** textual criticism aims to establish one authoritative text.
Readback keeps the divergences as first-class content — the wrong reading is the
interesting part, not noise to be resolved away.

---

## Read-back / hear-back

**ICAO and FAA radiotelephony procedure; NASA ASRS Callback reporting.**

The receiver repeats a clearance back so the sender can catch a misunderstanding
before it is acted on. A wrong repetition is a *readback error*; a sender who
fails to catch it commits a *hearback error*. The protocol exists to defeat
**expectation bias** — hearing what you expect rather than what was said.

**Taken:** the entire core loop, both error names, and the `Match` taxonomy.

**Refused:** aviation readback is verbatim repetition of a highly constrained
phraseology. Natural language has no such constraint, so verbatim repetition
defeats the purpose — it can be produced without comprehension. Readback
requires restatement *in the agent's own words, naming scope and exclusions*,
which is the only form that can be falsified.

---

## The Checklist Manifesto

**Atul Gawande.**

Short mandatory checks outperform expert judgment on exactly the failures
experts consider beneath them. Gawande's distinction: **read-do** (read the
item, then perform it) versus **do-confirm** (perform from memory, then confirm
against the list).

**Taken:** the readback is a read-do check — stated before acting, not after.
The Quality Gate in `SKILL.md` is a do-confirm check. Both are deliberately
short, because a checklist long enough to feel thorough is long enough to be
skipped.

**Refused:** checklists assume a fixed procedure. Readback's triggers are
conditional, so the skill describes when to write rather than prescribing a
fixed sequence.

---

## Blameless postmortems

**Sidney Dekker, *The Field Guide to Understanding Human Error*; John Allspaw
et al. at Etsy.**

Record what made the error *make sense at the time* to the person who made it.
Second-story accounts explain the local rationality that produced the mistake;
first-story accounts name a culprit and teach nothing. Blame reliably suppresses
reporting, and suppressed reports are worse than the original errors.

**Taken:** the tone of `Match: missed` and of `references/drift-patterns.md`.
A missed readback is data about a communication channel, not a fault of either
party. This is also why the honest `unchecked` value exists rather than being
folded into a failure category.

**Refused:** postmortems are triggered by incidents. Readback records the
uneventful changes too, because the baseline is what makes the divergences
legible.

---

## Compiled enforcement

**Zhou et al., *TRACE: Compiling User Corrections into Runtime Enforcement for
Coding Agents*, arXiv 2606.13174 (2026).**

Distinguishes **preference access** from **compliance**: a memory system can make
a correction visible in a later session without causing the agent to obey it.
Measured — memory-based retrieval reached 42.5% compliance where compiled,
checkable rules reached 70.1%. Rules carry an applicability check, a behavior
instruction, and a verifier; a five-action resolver (Noop / Update / Supersede /
Split / New) decides what each new correction does to the existing set.

**Taken:** verifiers on Active Constraints, and the five-action resolver. This is
a correction to Readback's original design — a pure record is an access-layer
system, and the paper's own numbers show that visibility alone underperforms.

**Refused:** TRACE compiles rules into automated runtime blocks. Readback stops
at a stated, checkable condition. Their appendix concedes that a mis-classified
Supersede archives a rule with no automatic rollback, which is precisely the
failure an append-only record avoids — and an over-strict automated block is
harder to notice and harder to undo than a constraint a human can read.

---

## What none of them solve

Every method above assumes the record is written by the person who will later
read it. Readback's record is written by an agent about its own comprehension,
which introduces a failure the sources do not address: the writer and the
subject of the record are the same party, and that party has a standing
incentive to record a more coherent understanding than it actually had.

The `Asked` field is verbatim for this reason and no other. It is the only field
the agent does not author, and therefore the only one that cannot be tidied.
