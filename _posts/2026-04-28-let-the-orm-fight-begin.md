---
layout: post
title: "Let the ORM fight begin!"
date: 2026-04-28 17:23:24 +0000
permalink: "/2026/04/28/let-the-orm-fight-begin/"
description: "The orm-fight experiment builds the same bookkeeping app with seven TypeScript ORMs and tracks updates, CVEs and SBOM dependency drift for a year."
tags: [supply-chain-security, web-development, tech-strategy]
og_type: article
image: "/assets/posts/let-the-orm-fight-begin/og.jpg"
devto_url: "https://dev.to/sebs/let-the-orm-fight-begin-392e"
render_with_liquid: false
---
Every few months, a new round of "which TypeScript ORM should we use?" breaks out — on team chats, on Hacker News, in conference hallways. The arguments rhyme: Prisma is too heavy, Drizzle is too new, TypeORM is too legacy, Sequelize is too JavaScript-y. The evidence cited is usually a benchmark from 2022, a vibes-based blog post, or a single bug someone hit on a Tuesday.

Got tired of it as well? We're running an experiment!

## The setup

[`github.com/orm-fight`](https://github.com/orm-fight/) is a public GitHub organization where we've started spinning up one project per major TypeScript ORM. Same domain, same test suite, same CI/CD pipeline, same Dependabot configuration. The only thing that changes between projects is the ORM itself.

The application we're building is a **double-entry bookkeeping** system. We picked it deliberately: it's a domain with real transactional constraints (debits must equal credits), genuine relationships between tables (accounts, ledgers, entries, postings), and invariants that any ORM worth its npm download has to help you express and enforce. 

Each project has:

- A **test suite** built on the Node.js built-in test runner (no Jest, no Vitest — we want to keep the dependency footprint honest).
- A **CI pipeline** that builds `main`, runs tests, and pushes artifacts.
- **Dependabot** turned on, so every project receives the same upgrade pressure.
- An **SBOM** generated and stored as a build artifact, so we can track dependency drift over time.

## What we want to know

Once these projects have been running for a while — we're aiming for a runtime of about a year — we'll have data on questions that usually get answered with anecdotes:

- **How do the implementations actually differ?** It will be interesting to see how the syntax sugar from framework to framework differs - or not. 
- **How often do updates land?** Which ORMs ship steadily, which go quiet, which break things in minor releases.
- **How many CVEs are reported over time?** And — more interestingly — how does that propagate to *transitive* dependencies? An ORM is rarely a single package; it's a tree.
- **How does the dependency graph evolve?** This is what the SBOMs are for. We want to see the supply chain shape, not just the top-level `package.json`.

## Why we're doing this

Two reasons.

The first is straightforward: we want **long-term, evidence-based knowledge** to ground future ORM discussions. To replace "I read somewhere that..." with "here's the data we collected over the last 12 months." Being equally allergic to hype and bullshit bingo: Maybe its time for some a experiment to see what stands out, whats boring (aka ready for prod) and whats surprisingly broken.  

The second reason is **supply chain security**. An ORM is one of the most consequential dependencies in a typical Node.js backend. It pulls in database drivers, query builders, connection pools, validation libraries, sometimes a whole code-generation pipeline. The security posture of your app is, in large part, the security posture of your ORM and everything downstream of it. Tracking SBOMs over time, against real CVE data, is a useful thing to *practice* — and one of the side effects of this project is that we'll get good at extracting and researching build artifacts.

We also just want to **write about it as it happens**. One year is a long time in JavaScript-land. Things will break. Things will improve. Some maintainers will burn out. Some projects will surprise us. That story is worth telling in real time. 

## The contestants

Here are the TypeScript SQL ORMs (and ORM-adjacent tools) we're starting with:

- **Prisma** — Schema-first with codegen, excellent type safety, migrations built-in. The most popular option, and the one most teams default to.
- **Drizzle ORM** — Lightweight, SQL-like query builder, zero runtime overhead, edge-friendly. The newcomer that has eaten a lot of Prisma's mindshare in the last two years.
- **TypeORM** — Decorator-based, supports both Active Record and Data Mapper patterns. Mature, widely deployed, and starting to feel its age.
- **MikroORM** — Data Mapper, Unit of Work, Identity Map. If you've worked with Doctrine or Hibernate, you'll feel at home immediately.
- **Kysely** — Strictly speaking, a type-safe SQL query builder rather than a full ORM. Included because a lot of teams reach for it instead of an ORM, and we want that comparison on the table.
- **Sequelize** — JS-first with TypeScript types added later. Still very common in legacy codebases.
- **Objection.js** — Built on Knex, less TS-native but still in production use in a lot of places.

We may add or drop candidates as we go. If a project is clearly abandoned by month three, it goes. If something interesting shows up, it gets a slot.

## Follow along

Everything is public from day one — the code, the CI configuration, the SBOMs, the Dependabot history. You can find the organization at:

**[https://github.com/orm-fight/](https://github.com/orm-fight/)**

I'll be writing here periodically with what we're seeing — early surprises, build breakages, CVE patterns, dependency tree changes, and whatever else turns up that we didn't expect.

The fight isn't really *between* the ORMs. It's between the way we currently choose tools — vibes, recency bias, the loudest voice in the team meeting — and a slower, more boring, more useful alternative: actually watching them over time - create a conclusion from data.

Let the ORM fight begin.
