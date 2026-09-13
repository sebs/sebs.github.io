---
layout: post
title: "From Idea to Implementation-Ready: A Six-Phase Pipeline with Rewelo"
date: 2026-03-17 19:13:14 +0000
permalink: "/2026/03/17/from-idea-to-implementation-ready-a-six-phase-pipeline-with-rewelo/"
description: "A six-phase pipeline from vision to a ready backlog: specs, Gherkin scenarios, ADRs, rewelo scoring of 113 tickets and an AI-run Four Amigos review."
tags: [agile-practices, ai-assisted-development, testing-and-quality]
og_type: article
image: "/assets/posts/from-idea-to-implementation-ready-a-six-phase-pipeline-with-rewelo/og.jpg"
devto_url: "https://dev.to/sebs/from-idea-to-implementation-ready-a-six-phase-pipeline-with-rewelo-42lp"
render_with_liquid: false
---
Most projects start with a vague idea and a Jira board. The gap between "we should build X" and "here is a fully specified, dependency-ordered, priority-scored backlog ready for sprint planning" is usually traversed through a series of meetings, half-written requirements documents, and optimistic estimates scribbled on sticky notes.

This post documents a different approach: a six-phase pipeline in which each phase produces structured, machine-readable artifacts that feed directly into the next. The backbone is [Rewelo](https://github.com/sebs/rewelo) — a CLI and MCP server for relative-weight backlog prioritization built on DuckDB — which transforms the back half of the process from intuition-based ticket-sorting into a transparent, reproducible calculation.

> The question is not "how do we decide what to build first?" but "how do we make the decision auditable, reversible, and legible to every stakeholder?"

The result, across a real product build: 113 scored and tagged tickets, 124 dependency relations organized into five dependency layers, and a backlog that can be re-ranked in seconds when priorities shift.

| Metric | Count |
|---|---|
| Gherkin feature files | 16 |
| BDD scenarios | ~160 |
| Scored tickets | 113 |
| Dependency relations | 124 |

---

## The Pipeline

The process is structured into six sequential phases, each with a defined entry condition, a set of artifacts it produces, and a quality gate before the output is accepted downstream. Two phases have explicit iteration loops; three feedback paths run from the final review back into earlier phases.

### Phase 1 — Vision & Concept

**Lock the problem space before touching architecture.**

The phase begins with four documents: `concept.md` (what and why), `elements.mmd` (a Mermaid diagram of the major domain entities), `estimates.md` (rough sizing and constraints), and `trlc-cheatsheet.md` (a quick-reference for the requirements language used throughout). Before anything moves forward, the four documents undergo a cross-consistency review — checking that the entity model matches the concept, that estimates are grounded in scope, and that the requirements language is applied uniformly.

*Artifacts:* `concept.md` · `elements.mmd` · `estimates.md` · `trlc-cheatsheet.md` · cross-consistency review

### Phase 2 — Architecture & Specifications

**Define how the system actually works, then find the gaps.**

With the vision locked, `architecture.md` documents the major components, their data flows, and any specialized concerns (in this project, a CRDT-to-Git synchronization layer). A gap analysis follows — specifically looking for what is needed to ship a first version versus what is aspirational. Only what passes that bar makes it into the three specification documents: `artifact_schemas.md`, `api_contract.md`, and `operational.md`, which together define the technical surface area that will be tested and implemented.

*Artifacts:* `architecture.md` · gap analysis → v1 · `artifact_schemas.md` · `api_contract.md` · `operational.md`

### Phase 3 — Behavioral Specifications

**Sixteen feature files. ~160 scenarios. One explicit loop.**

This is where requirements become falsifiable. Gherkin scenarios are written for every feature identified in Phase 2 — Given, When, Then triples that can drive automated tests and that make edge-case thinking explicit. A best-practices review is applied to the full scenario set: are scenarios atomic? Are they written from the user's perspective? Do they avoid implementation detail? If the answer to any of these is "no", the feature files are reworked. Only when the scenario set passes the gate does the process continue.

This is the most iterative phase, and deliberately so — fixing an ambiguous scenario at this stage costs minutes; finding the same ambiguity during implementation costs days.

*Artifacts:* 16 feature files · ~160 scenarios · best-practices review · explicit rework loop

### Phase 4 — Decisions & Quality Gates

**Capture the choices so future team members can understand them.**

Three Architecture Decision Records are authored at this stage: one mapping the technology stack to the problem constraints, one capturing the rationale for the BDD approach, and one documenting the Rewelo integration decision itself. The Definition of Ready and Definition of Done are written here as well — these become the acceptance criteria applied in Phase 6. Finally, reusable templates for User Stories and ADRs are finalized, ensuring that new tickets and decisions added later follow a consistent structure.

*Artifacts:* ADR: tech mapping · ADR: BDD rationale · ADR: Rewelo · Definition of Ready · Definition of Done · Story and ADR templates

### Phase 5 — Backlog

**113 tickets. Scored, tagged, and dependency-ordered.**

Every story derived from the BDD scenarios and architecture documents is entered into Rewelo and scored across four dimensions: Benefit, Penalty, Estimate, and Risk. Tags group tickets by feature, team, and state. Ticket relations — `blocks`, `depends-on`, `relates-to` — are declared explicitly, yielding 124 relations that sort the backlog into five logical dependency layers. The top of the backlog is not a product manager's gut feel; it is the output of a priority formula.

*Artifacts:* 113 tickets · B/P/E/R scores · 124 relations · 5 dependency layers

### Phase 6 — Four Amigos Review

**Four perspectives, one approval gate, three feedback paths.**

The Four Amigos — Product Owner, Developer, QA Engineer, and UX Designer — each review the backlog through their own lens, informed by AI-simulated personas. The PO checks value propositions and acceptance criteria. The Developer flags architecture misalignment and re-scores Estimate and Risk. QA surfaces edge cases and cross-feature risks. The UX designer reviews interaction states, cognitive load, and missing flows. The gate is a four-way approval. If it doesn't pass, three feedback loops are available: back to requirements (for conceptual gaps), back to the feature files (for BDD issues), or back to ticket refinement (for scope or scoring problems).

*Personas:* Product Owner · Developer · QA Engineer · UX Designer · three feedback loops

---

## Rewelo at the Center

The pipeline would be useful without Rewelo — structured documents and BDD scenarios alone are a meaningful step up from most engineering processes. But the backlog phase is where the approach goes from "disciplined" to "genuinely different."

[Rewelo](https://github.com/sebs/rewelo) is a CLI and MCP server for relative-weight backlog prioritization. It stores tickets in an embedded DuckDB database — no server required — and calculates a priority score at runtime based on four dimensions, normalized across the full backlog or any tagged subset.

Each ticket receives four scores on the Fibonacci scale (1, 2, 3, 5, 8, 13, 21):

| Dimension | Measures |
|---|---|
| **B** — Benefit | Value delivered by implementing this story |
| **P** — Penalty | Cost of *not* implementing — the downside of deferral |
| **E** — Estimate | Resources required for implementation |
| **R** — Risk | Uncertainty or complexity in the implementation |

At runtime, Rewelo calculates:

```plaintext
# Value vs Cost, normalized across the backlog
Value    = Benefit + Penalty
Cost     = Estimate + Risk
Priority = Value / Cost
```

Higher priority means better return on investment. The scores are normalized relative to the whole backlog — or any subset filtered by tag — so re-ranking is instantaneous when new tickets are added or when the team changes their weighting preferences. `rw calc priority` is a single command away.

This matters in the Four Amigos phase specifically. When a Developer argues that a ticket's Estimate score is too optimistic, or a QA engineer surfaces a hidden dependency that increases Risk, the scores are updated and the backlog re-sorts itself. The discussion produces data, not just minutes.

### Tag-driven organization

Rewelo uses a flexible `prefix:value` tag system rather than fixed fields. In this project, tags covered state (`state:backlog`, `state:wip`, `state:done`), feature grouping (`feature:auth`, `feature:checkout`), and team (`team:platform`). Because every tag assignment is logged in an audit trail, the tag history also yields lead time and cycle time data from `state:` transitions — a useful side effect.

### Dependency ordering

The 124 relation declarations (`blocks`, `depends-on`, `relates-to`) produce a directed graph of the backlog. Rewelo uses this to expose a five-layer topological ordering: the tickets in layer one have no upstream dependencies and can be started immediately; each subsequent layer becomes unblocked as the previous one completes. This is far more actionable than a flat, priority-sorted list.

---

## The Four Amigos Review in Detail

The Four Amigos is a well-established agile practice: before any story reaches a sprint, it should be reviewed by representatives of the four key perspectives. What makes this pipeline's implementation unusual is that the review is run against AI-simulated personas — each grounded in the artifact set produced by the earlier phases — before involving the human team. This surfaces structural problems in the backlog without consuming sprint planning time.

**Product Owner** reviews value propositions, acceptance criteria, and Benefit/Penalty scores. Asks: does this story deliver the outcome described in the concept? Is the acceptance criteria in the feature file comprehensive? Would a user recognize this as solving their problem?

**Developer** reviews architecture fit, implementation plausibility, and Estimate/Risk scores. Asks: is this story implementable given the architecture defined in Phase 2? Are the E and R scores realistic? Are there hidden technical dependencies not captured in the relation graph?

**QA Engineer** reviews edge cases and cross-feature risks. Asks: are the Gherkin scenarios sufficient to catch regressions? Are there error states or boundary conditions missing from the feature files? Do any of these stories interact in ways that could produce surprising failures?

**UX Designer** reviews interaction states, transitions, and cognitive load. Asks: are all the states this feature can be in represented in the acceptance criteria? Is the described flow consistent with how users actually think about the task? Where might a user get confused?

The gate is a four-way approval. If any persona finds a material gap, one of three feedback paths is taken:

**↩ Refine requirements.** Conceptual gaps or value misalignments send the work back to Phase 1's cross-consistency review — the deepest and most expensive loop.

**↩ Rework feature files.** Missing scenarios, incomplete edge cases, or poorly specified acceptance criteria send individual feature files back to Phase 3 for revision.

**↩ Refine stories.** Mis-scored tickets, missing dependencies, or scope problems are addressed directly in the Rewelo backlog — the shallowest and most common loop.

The three loops are tiered by cost: story refinement is cheap (minutes), BDD rework is moderate (hours), requirements revision is expensive (days). The earlier a problem is found, the cheaper it is to fix — which is the central argument for front-loading structure in the first place.

---

## What the Output Looks Like

When the Four Amigos gate passes, the output is a Rewelo project containing 113 tickets that have been scored by all four personas, organized into five dependency layers, and validated against 160 behavioral scenarios. The implementation team can:

- Run `rw calc priority` to get an instant priority ranking
- Run `rw report dashboard` to generate an HTML dashboard showing backlog health, score distribution, and tag breakdowns
- Export to CSV or JSON for integration with any downstream tool
- Start a sprint immediately from layer one, knowing every ticket in that layer is dependency-free and has passed four distinct review perspectives

What the team cannot do is argue about what to build next without data. That is, perhaps, the most useful property of the whole pipeline.

## Running Rewelo as an MCP Server

One of Rewelo's less obvious capabilities is its MCP server mode. Run `rw serve` (or deploy the Docker container and configure Claude to point to it), and the AI assistant can manage the entire backlog — creating tickets, updating scores, assigning tags, running calculations — through natural language. This is how the Four Amigos review phase was implemented: each persona is a system prompt, the Rewelo MCP server provides the backlog as context, and the review runs as a structured conversation.

The configuration is straightforward. Rewelo's `.mcp.json` file in the repository shows the exact setup. Because the data lives in a named Docker volume, the database persists across container restarts and the full audit trail — every score change, every tag transition — is preserved.

---

## Conclusion

The pipeline described here is not light-weight. Six structured phases, 16 feature files, 113 tickets, three ADRs, and a four-persona review process is a meaningful investment before any implementation begins. The argument for making that investment is simple: the cost of ambiguity grows exponentially the later it is found. A missing acceptance criterion discovered during sprint planning costs a conversation. The same gap found during code review costs a rewrite. Found in production, it costs users.

Rewelo sits at the center of this because the backlog is where ambiguity historically hides most effectively — in vague story descriptions, in optimistic estimates, in priorities that change with whoever spoke last at the planning meeting. Replacing that with a transparent scoring formula, a dependency graph, and a full revision history is not bureaucracy. It is engineering applied to the product development process itself.

The repository is at [github.com/sebs/rewelo](https://github.com/sebs/rewelo). It is experimental software, as the README notes — but the ideas it implements are not.
