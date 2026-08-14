# Drift Patterns

A taxonomy for the `Pattern:` line on entries where `Match` is `corrected` or `missed`.

Classification is not bureaucracy. One misread is an anecdote; forty misreads sorted into nine buckets is a measurement of how you and the model actually miscommunicate — and most of the buckets have a specific, learnable countermeasure.

---

## 1. Scope generalization

The user constrained the request; the agent applied it broadly.

> **Asked:** "make the scheduled jobs retry"
> **Built:** retries on every enqueue path

The most common pattern by a wide margin. Qualifiers — *only*, *just*, *for now*, *the X ones* — carry the entire meaning of a sentence and are the first thing lost.

**Countermeasure:** in the readback, state the scope boundary explicitly and name what is being *excluded*.

---

## 2. Unrequested adjacency

The agent fixed neighboring things nobody asked about — reformatting, renaming, "while I was in there."

Individually harmless, collectively corrosive: it inflates diffs, hides the real change during review, and makes reverting expensive.

**Countermeasure:** list adjacent fixes as proposals, do not commit them with the requested change.

---

## 3. Literal versus goal

The agent satisfied the words and missed the purpose, or inferred a purpose the user never held.

> **Asked:** "can you make the tests faster"
> **Built:** parallel execution — but the user meant the *feedback loop*, and wanted a watch mode

**Countermeasure:** the readback should name the outcome the user gets, not the change being made.

---

## 4. Invented constraint

The agent assumed a requirement never stated — backward compatibility, a performance target, a naming convention — and let the phantom constraint distort the design.

**Countermeasure:** every constraint in the readback is either quoted from the user, cited from the repo, or explicitly labeled an assumption.

---

## 5. Dropped constraint

The user stated a real constraint early; it decayed over turns and was gone by implementation. Long sessions and compaction both cause this.

**Countermeasure:** durable constraints belong in `map.md` under Active Constraints, not in conversational memory.

---

## 6. Wrong referent

*"The config"*, *"that function"*, *"the old one"* resolved to something other than what the user meant.

Cheap to prevent, expensive to discover, and disproportionately common in codebases with parallel naming.

**Countermeasure:** resolve every pronoun to a path in the readback. Never carry a demonstrative into implementation.

---

## 7. Silent substitution

The agent chose a different approach than the one discussed and did not flag the swap. The user discovers a different architecture than the one they approved.

The deception is rarely intentional — usually the substitution felt obviously better mid-implementation. It is still a broken contract.

**Countermeasure:** a mid-implementation change of approach requires a new readback before continuing.

---

## 8. Premature abstraction

The agent generalized from one case: a config system for one setting, an interface with one implementation, a plugin architecture for a feature that will never have a second plugin.

**Countermeasure:** name the concrete second use case, or build the concrete first one.

---

## 9. Expectation bias

The aviation term, and the root cause underneath several of the patterns above. The agent recognized a familiar shape and responded to the shape instead of the words — REST conventions imposed on an RPC endpoint, a standard auth flow assumed where the user described a custom one.

The tell: the built solution is *more idiomatic* than what was asked for. Fluency reads as correctness right up until it is discovered to be wrong.

**Countermeasure:** when a request pattern-matches something familiar, that similarity is the reason to read back, not the reason to skip it.

---

## Reading the accumulated record

Periodically, scan the log:

```bash
grep -c "Match: missed"    .readback/log.md
grep -c "Match: corrected" .readback/log.md
grep -A1 "^\*\*Pattern:\*\*" .readback/log.md | sort | uniq -c | sort -rn
```

What the numbers mean:

- **`missed` climbing relative to `corrected`** — readbacks are happening too late, or are too vague to be corrected. A readback nobody can disagree with is not doing its job.
- **One pattern dominating** — that is a fixable communication habit, on one side or the other. Scope generalization concentrated in one area of the codebase usually means that area's boundaries are unclear in the code itself, not just in the conversation.
- **`unchecked` dominating overall** — the protocol is not being run. Everything else is noise until that changes.

The point is not a clean scorecard. A log with no `missed` entries almost certainly means they went unrecorded.
