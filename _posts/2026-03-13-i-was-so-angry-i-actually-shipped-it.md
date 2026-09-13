---
layout: post
title: "I Was So Angry, I Actually Shipped It"
date: 2026-03-13 22:31:40 +0000
permalink: "/2026/03/13/i-was-so-angry-i-actually-shipped-it/"
description: "Introducing rewelo, a CLI and MCP server for relative-weight backlogs: priority from benefit, penalty, estimate and risk, stored in DuckDB with history."
tags: [developer-tooling, agile-practices, ai-assisted-development]
og_type: article
image: "/assets/posts/i-was-so-angry-i-actually-shipped-it/og.jpg"
devto_url: "https://dev.to/sebs/i-was-so-angry-i-actually-shipped-it-2m19"
render_with_liquid: false
---
A while ago I wrote about how I was fed up enough with project management tools to build my own. No URL. No code. Just a rant and some screenshots of a half-baked UI.

Several people in the comments called it a tease. They weren't wrong.

So here's the follow-up nobody .... erm ... at least three people did ask for.

## The UI Didn't Happen

Let me be upfront: I didn't build the fancy web UI I was implicitly promising. I started down that road a couple of times, got bored fighting CSS and component state, and asked myself the honest question — *who is this actually for?*

Me. It's for me.

And I live in the terminal.

So I threw out the frontend entirely and built a CLI instead. No regrets.

## Meet rewelo

**rewelo** — Relative Weight Backlogs for the CLI and MCP.

It does exactly what I said I wanted: it prioritizes work using four dimensions instead of the fictional psychic measurement known as story points.

Every ticket gets scored on:

- **Benefit** — value gained by doing the thing
- **Penalty** — cost of *not* doing the thing
- **Estimate** — how much work it actually is
- **Risk** — how uncertain or gnarly the implementation is

From those four numbers, priority calculates itself:

```plaintext
Value    = Benefit + Penalty
Cost     = Estimate + Risk
Priority = Value / Cost
```

Higher priority = better return on investment. It's not rocket science. It's just math that most tools refuse to let you do.

## DuckDB Was The Right Call

One of the decisions I'm most happy about: no server.

I spent zero hours configuring a database daemon, zero hours fighting connection pools, and zero hours explaining to myself why postgres was running at 3am. The whole thing runs on DuckDB — an embedded analytical database that lives in a single file.

This meant I could focus on the actual problem instead of infrastructure theater. Turns out a project management tool for one person doesn't need a distributed SQL cluster.

Who knew.

## Tags Instead of Fixed Fields

The state machine I wanted to build kept getting complicated. So I simplified it down to a tag system.

Every ticket gets tags in `prefix:value` format: `state:backlog`, `state:wip`, `state:done`, `feature:checkout`, `team:platform`. Whatever you need. The system doesn't care — it just tracks every assignment and removal in an audit log.

The beautiful side effect: since every `state:` tag change is recorded with a timestamp, cycle time and lead time fall out of the data for free. No extra instrumentation. No dashboards you have to manually update. Just the log.

## Revision History Because I've Been Burned

Every change to a ticket creates a snapshot of what it looked like before. Not just the scores — the tags too.

This means you can reconstruct the exact state of your backlog at any point in time. Remember that estimation session three weeks ago? You can see the numbers from before the panic re-estimation happened. This turned out to be more useful than I expected. Past me was making different tradeoffs than present me, and it's actually worth knowing when that changed and why.

## The MCP Part Is The Interesting Part

Here's where it gets weird in a good way.

The CLI doubles as an MCP server over stdio. Which means Claude — or any AI assistant that speaks MCP — can manage your backlog directly. Create tickets, assign tags, run priority calculations, generate reports. All from a conversation.

![Claude's MCP summary: 104 rewelo tickets created from 18 Gherkin feature files, with story counts per game system](/assets/posts/i-was-so-angry-i-actually-shipped-it/j7e5lti6ti1xyzxv764l.png)

I wrote in the original post that I wanted to bind agent integration to workflows, to have some control over machine-made changes. This is the answer to that. The MCP tools are the workflow. The AI calls them explicitly and the audit log catches everything it touches. Nothing happens silently.

In claudes own words

> I extracted all 18 Gherkin feature files from your features/ directory and converted each "Rule" block into a rewelo ticket — 104 stories total — with acceptance criteria derived from the scenarios, Fibonacci scores for benefit/penalty/estimate/risk, and system tags. I created the golden-season project in rewelo from scratch, set up 21 tags (3 part tags for B2G/NLS/24H and 18 system tags), and assigned every ticket its corresponding system:* tag. The backlog is now fully populated and prioritised, ready for sprint planning or further refinement like assigning part:* tags to map stories to the three-part implementation roadmap.


## A Word on Scope Creep Not Happening

I am genuinely proud of what I did *not* build.

No user accounts. No sharing. No real-time collaboration. No mobile app. No integrations with Slack, GitHub, Linear, Jira, or anything that would require me to maintain OAuth tokens at 2am.

This tool is for one person — me — and it does that job well. The moment I start building for an imaginary team of five, I stop building for myself and start building a worse version of tools that already exist.

I've read enough HN threads to know how that ends.

## It Exists. You Can Download It.

Here it is: [github.com/sebs/rewelo](https://github.com/sebs/rewelo).

---

*Sometimes the best tool is the one that you actually finish.*
