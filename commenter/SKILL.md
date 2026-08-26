---
name: commenter
description: Add or improve useful code comments by explaining abstractions, contracts, constraints, intent, and non-obvious design decisions; supports beginner, intermediate, and advanced detail levels.
metadata:
  short-description: Add meaningful comments to code
---

# Commenter

Add comments that preserve information a reader cannot easily derive from the code. The goal is to make the system's structure and behavior understandable without narrating every line.

## Detail levels

Use the level supplied by the user:

- **Beginner:** use plain language; explain component responsibility, important terms, inputs, outputs, side effects, lifecycle, and likely edge cases.
- **Intermediate:** the default. Provide moderately detailed interface and field documentation, contracts, invariants, important failure behavior, non-obvious implementation reasoning, and meaningful dependency notes.
- **Advanced:** be concise. Comment abstractions, contracts, invariants, hazards, tradeoffs, and reasons that an experienced maintainer cannot infer directly.

If no level is supplied, use **intermediate-detailed**. If the user says "for future me," use intermediate-detailed behavior with extra attention to assumptions, edge cases, and maintenance hazards.

## Comment types

Choose the type that matches the information being documented:

1. **Interface comment:** immediately before a module, class, data structure, function, or method. Explain its abstraction, responsibilities, arguments, return value, side effects, exceptions, caller requirements, and important guarantees.
2. **Data-structure member comment:** beside a field, property, or constant. Explain meaning, units, valid values, nullability, ownership, lifecycle, and relationships that are not obvious from the declaration.
3. **Implementation comment:** inside a function or method. Explain why an algorithm, ordering, workaround, optimization, or edge-case branch is necessary. Do not translate individual statements into English.
4. **Cross-module comment:** document a dependency or design decision crossing module, package, service, or layer boundaries. State the shared rule and identify the other locations that must change together. Use a central design note when the explanation is too large or has no natural code location.
5. **Contract comment:** document preconditions, postconditions, invariants, error behavior, thread-safety, security expectations, or lifecycle guarantees relied on by callers.
6. **Design-decision comment:** record a non-obvious rationale, constraint, tradeoff, compatibility requirement, or intentional limitation.

## Workflow

1. Inspect the language, documentation convention, project conventions, existing comments, and the requested scope.
2. Understand the code before commenting. Identify public interfaces, important data structures, abstractions, boundaries, invariants, side effects, and non-obvious behavior.
3. Prefer improving names or structure when that makes the behavior genuinely obvious; do not use comments to excuse confusing code.
4. Add comments at a higher or different level of abstraction than the nearby code. Explain intent, "why," contracts, constraints, and risks.
5. Preserve the repository's comment and documentation format, including Javadoc, Doxygen, Go doc, docstrings, or local conventions.
6. Review each new or changed comment for accuracy, repetition, ambiguity, and future staleness. Update or remove nearby comments that conflict with the implementation when they are within scope.
7. Report what was documented, the selected detail level, and important areas intentionally left uncommented.

## Quality rules

- Do not comment every line or repeat names, types, operators, or obvious control flow.
- A comment should add intent, abstraction, constraint, invariant, rationale, side effect, failure behavior, or boundary knowledge.
- Write for a developer seeing the code for the first time, not only for the original author.
- Keep comments synchronized with behavior; never preserve a comment that is no longer true.
- Avoid speculative claims, vague phrases, and comments that promise behavior the code does not guarantee.
- For cross-module behavior, make the relationship discoverable with a concise pointer to the authoritative design note or related declaration.
- Match detail to the requested level, but do not omit safety-critical, correctness-critical, or public API information.

## Verification

Before finishing, inspect the diff or changed files and verify that:

- comments are attached to the correct declarations or code paths;
- documented behavior matches the implementation;
- public contracts, important fields, and non-obvious boundaries are covered;
- comments do not merely restate the code;
- the repository's formatting and documentation conventions remain valid.

If the code cannot be fully understood or verified, state the uncertainty instead of inventing documentation.
