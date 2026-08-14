Plan the feature: $ARGUMENTS

You are planning, not implementing. Do not write or modify application code.

1. Read `docs/shipit-product-brief.md` and every ADR in `docs/` first.
   If the feature appears in the brief's out-of-scope list, note that this
   plan is the act of pulling it into scope.
2. Write the plan to `docs/plans/<feature-slug>-plan.md` using the template
   at `docs/templates/feature-plan.md`.
3. The plan must include:
   - Problem and why now (cite the brief)
   - Scope: in / out for this iteration
   - Design sketch (respect accepted ADRs; if one must change, say which
     and note that it requires a new ADR — do not re-litigate silently)
   - Task breakdown: each task sized for one focused session, with its own
     definition of done (symptom + location + scope + done discipline)
   - Test plan, including boundary cases per ADR-001's convention
   - Risks and open questions for the humans
4. End by listing which tasks are independent (parallelizable) and which
   block others — this breakdown becomes tracker issues later.
