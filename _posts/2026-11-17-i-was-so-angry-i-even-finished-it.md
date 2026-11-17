---
layout: post
title: "I Was So Angry, I Even Finished It"
date: 2026-11-17 20:00:00 +0000
permalink: "/2026/11/17/i-was-so-angry-i-even-finished-it/"
description: "Eighteen months after the rant, rewelo is finished: what survived of the original plan, why DuckDB went, 237 bugs in a week, and a tool that checks its own estimates."
tags: [developer-tooling, agile-practices, ai-assisted-development]
og_type: article
series: "I was so angry I built my own"
render_with_liquid: false
---
Eighteen months ago I wrote [a rant](/2025/05/28/i-was-so-angry-i-built-my-own/) about project management tools and promised to build my own. In March I [shipped something](/2026/03/13/i-was-so-angry-i-actually-shipped-it/) and called it done. It wasn't done. Now it is: [rewelo](https://github.com/sebs/rewelo) is at 0.10.0, installs with `npm install -g rewelo`, has a [website](https://sebs.github.io/rewelo/), is listed in the MCP Registry, and I have stopped wanting things from it. That last one is my definition of finished for a tool I build for myself.

So time to hold the original rant against what exists. Rants age badly, lets see how bad.

## The ledger

The four dimensions survived without a scratch. Value became Benefit, Effort became Estimate, Penalty and Risk stayed what they were. Priority is still `(B + P) / (E + R)`. That part never moved once since the first sketch, which tells me the idea was the good part and everything around it was negotiable.

Markdown stories did not survive. A story in rewelo is a row in a SQLite file: title, description, four numbers, tags. The editor from the screenshots in the first post died with the rest of the UI. I don't miss it, mostly an agent writes the descriptions now and I read them.

ADRs and post-mortems as first class citizens: no. rewelo has six ADRs, but they are markdown files in `adr/`, in the repo, next to the code they talk about. Which is where I put them at every client anyway. Building a second home for them inside a backlog tool was the "personal tool" trying to become a platform. Post-mortems I never even started.

DORA metrics: not built. rewelo has no idea what a deployment is and it will stay that way. The pipeline knows that better than a backlog ever will.

Kanban metrics: built, and more than I wrote back then. Every `state:` tag change sits in an audit log, so `rw report flow` gives throughput per week, cycle and lead time as 50th/85th/95th percentiles (averages lie as soon as one ticket takes a month) and flags the work in progress that's already older than the 85th percentile. The dashboard draws a cumulative flow diagram. There are no WIP limits. A flag on the ticket that is getting old does more for me than a number on a column header.

And then there was this sentence:

> I don't want to cheap out and get a bunch of things ironed out before integrating some 3rd party agentic api.

I never integrated one. I turned it around: rewelo is an MCP server and the agent comes to the tool. More on that below.

## "DuckDB was the right call" lasted six months

In March I wrote, in a header, that DuckDB was the right call. [ADR-005](https://github.com/sebs/rewelo/blob/main/adr/005-sqlite.md) disagrees. The `duckdb` npm package is a native module and for Node 26 there was no prebuilt binary, so npm fell back to compiling DuckDB from C++ source on my machine (it failed). Its build toolchain was also behind every single finding `npm audit` reported. And the columnar analytical engine I was so pleased about was aggregating a few hundred tickets.

Node ships `node:sqlite` since 24. So that's what it is now, and the runtime dependencies are down to three: the MCP SDK, commander and zod. Installs are boring now, which is the compliment.

ADR-003, the DuckDB one, is still in the repo, marked "Superseded by ADR-005". That is the part of "documentation as a first class citizen" I actually believe in. Not that the decisions were right, but that you can see when they stopped being right, and why.

## September

Between March and July not much happened. Then September had 436 commits, 328 of them starting with `fix`.

What happened was exploratory testing. Rounds time-boxed to 30 minutes, each with three areas under test (the database layer, the CLI and import/export, the MCP server against its own docs, and so on), every finding written down with a severity, fixed on a branch, one commit per finding. Rounds three to nine found 237 bugs. [Agents did the exploring, I wrote the charters and read every finding before it got fixed.] The findings files are in the repo if you want to see what a "shipped" tool looks like from the inside: a rate limiter that locks the server out when the system clock steps backwards, emoji flags cut in half by truncation, backups that restore once but not a second time.

None of these would have hurt me as the only user. All of them would have hurt the first person that isn't me. That's the difference between shipped in March and finished now. The test suite is at roughly 860 tests, about as many lines of tests as of code.

## The agent comes to the tool

The MCP part was the interesting part in March and it still is, but it grew up a bit. What changed how I work:

- `apply_changes` takes a whole plan (create, re-score, tag, relate, delete) and applies all of it in one transaction or none of it. With `dryRun` it only shows what the ranking would look like afterwards. An agent grooming a backlog makes dozens of calls, and a failure halfway used to leave me with a half-groomed backlog. Now I review one plan instead of approving forty tool calls.
- When the client can show forms, `ticket_create` asks me for the scores the model left out, with a drop-down of Fibonacci values, instead of defaulting them quietly. Scoring is the one thing I don't delegate. The model writes a fine ticket, but my opinion is the whole point of benefit and penalty.
- The workflows from my consulting toolbox (intake interview, sprint planning against a capacity, standup digest, slicing a big ticket, what-if, retro on estimate accuracy) are Claude Code skills in the repo and get served as MCP prompts. In Claude Code that's `/mcp__rewelo__plan-sprint Acme 30`.
- The dashboard renders as an MCP App in hosts that support it and stays live while I change things from the CLI in another terminal.

That is roughly what I meant with "binding agent integration to workflows" back then. The agent can do a lot, but it does it through a small set of tools that log everything they touch, and the decisions that are mine stay mine.

## It now argues with its own premise

This is my favourite part and I did not plan it.

Half of the cost in the priority formula is the estimate. So the ranking is exactly as good as the estimates are. `rw report estimates` takes the done tickets, takes the estimate each one had when work started (not the one it got re-estimated to afterwards, a bit of cheating every team does) and checks with [Spearman's rank correlation](https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient) whether the bigger estimates actually took longer. From 0.6 it says "well", from 0.3 "somewhat", below that "not at all".

And `rw report forecast` doesn't look at estimates in the first place. It replays the actual throughput as a Monte Carlo simulation, 10,000 runs, and gives you the dates at 50, 85 and 95%.

So the tool I built out of anger about story points ships a forecast that ignores estimates and a report that tells you whether yours are worth anything. I'm fine with that. Relative weight never claimed estimates are right, only that the trade-off should be visible. If the data says the estimate column is noise, `rw config weights` lets me lean on benefit and penalty instead. [On my own backlog the correlation came out at ...]

Finished, for me, means no accounts, no sync, no web UI apart from a static HTML dashboard, and a README that still says "experimental software" and will keep saying it. One user, done.

p.s. The anger was gone after about three weeks. What got it over the line was a findings file with 37 lines in it and a time-box.
