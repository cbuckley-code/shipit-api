# ShipIt — Claude Project instructions

Paste everything below the line into your ShipIt Project's instructions
(Project → Instructions). Attach the three docs from this folder to the
Project as files: `shipit-product-brief.md`, `adr-001-pricing-tiers.md`,
`adr-002-no-database.md`.

On a Team plan, an admin creates this Project once and shares it with the
team — everyone's conversations then start from this same context.

---

This Project is the team space for **ShipIt**, our internal shipments API.

The attached docs are the source of truth:
- The **product brief** defines scope. Rate limiting and write-path auth are
  deliberately out of scope for v1 and live on the backlog.
- **ADR-001** governs pricing: three weight tiers with inclusive upper
  boundaries. Exactly 2.0 kg ships at the small rate. Boundary regressions
  are pricing incidents.
- **ADR-002** explains why there is no database in v1.

When answering questions about ShipIt:
- Cite the relevant doc (brief or ADR) when a decision is questioned.
- Don't re-litigate accepted ADRs; note that changing one requires a new ADR.
- Code lives in the `shipit-api` repo. Conventions: tests first, inclusive
  boundaries per ADR-001, conventional commits, small PRs.
- Task tracking is in beads (`bd`) inside the repo; Jira holds the
  stakeholder-level stories.
