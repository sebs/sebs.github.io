---
layout: post
title: "sudo 'schland just give me my data"
date: 2026-07-06 17:31:08 +0000
permalink: "/2026/07/06/sudo-schland-just-give-me-my-data/"
description: "There's an old xkcd. Guy says \"make me a sandwich.\" Gets refused. Says \"sudo make me a sandwich.\"..."
tags: [opendata, ai, darkfactory]
og_type: article
image: "/assets/posts/sudo-schland-just-give-me-my-data/cover.png"
devto_url: "https://dev.to/sebs/sudo-schland-just-give-me-my-data-4ga7"
render_with_liquid: false
---
There's an old xkcd. Guy says "make me a sandwich." Gets refused. Says "sudo make me a sandwich." Gets a sandwich.

I've been running the same play, except the sandwich is public data and the reluctant party is the Federal Republic of Germany. The result is [maschinenlesbar.org](https://github.com/maschinenlesbar-org): Many TypeScript CLIs, one per open API the German state runs, all on npm, all built the same way. `sudo bundesrepublik --json`, more or less. 25 is the current count. The plan is roughly a hundred.

## The joke in the name

"Maschinenlesbar" means machine-readable, and it's not a word I made up for branding. It appears *in German law*. The E-Government-Gesetz obliges federal agencies to publish their data in machine-readable formats. A country that still confirms things by fax has a statute demanding machine-readability.

And on paper, the agencies delivered. Live water levels for every federal waterway. The complete federal budget. Every registered lobbyist. Ambient gamma radiation from about 1,700 probes. Parliamentary proceedings going back decades. All behind REST endpoints, largely unauthenticated.

So far, so good. Now try to *connect* any of it.

## The moat

Here's the thesis, and it holds across every party and every legislative period: the core strategy of German open-data politics is the prevention of interoperability. The data is published — that box is checked. The data cannot be linked. That's the actual defense.

Smart people have spent years trying to get one uniform interface over the *kleine Anfragen* — the written parliamentary questions — across Germany's parliaments. Or the parliamentary documentation, sixteen states plus the Bundestag, in one format. LOL. There are X systems and every single one does things *slightly* differently. Federalism is a fine idea for distributing power; here it moonlights as a technique for making sure data never meets other data. Nobody had to forbid anything. No shared identifiers, no common schemas, a different timestamp format per API, one endpoint speaking clean JSON and the next speaking WFS — an OGC standard older than the iPhone — and the job is done.

And when passive fragmentation isn't enough, there's the active move: change a format, arbitrarily, and watch every downstream tool die. That trick has quietly killed civic-tech projects for two decades.

Because the dangerous thing was never a single dataset. A lobbyist list is a phone book. A budget is a spreadsheet. It's the *join* that produces accountability: this lobbyist, this committee, this budget line, this vote. Publish everything, link nothing, and you get transparency theater — technically open, practically opaque.

## 25 boring CLIs as a political act

Which is why aggressive uniformity is the entire design. Every CLI:

- installs the same way (`npm i -g <name>-cli`, or just `npx` it)
- emits JSON on stdout, errors on stderr, honest exit codes
- ships as a typed API client too, if you'd rather import than shell out

Uniformity on the outside is interoperability retrofitted in userland. The state won't build the joins — fine, `jq` and a pipe will.  

> "write programs that handle text streams, because that is a universal interface" 

Doug McIlroy's quote is fifty years old and turns out to double as civic infrastructure.

There's also a speed asymmetry worth naming. The state ships one half-baked portal per geological epoch. An open-source tool, once it's out there, does five to ten iterations in the same window — and how that pace is sustained across a hundred repos is its own story, which I'll get to at the end. Suffice it for now: I'm genuinely curious whether the old sabotage strategies still work. My bet is no.

## Anti-journalism, in the friendliest possible way

The other honest motivation, and I know how the word sounds: this is anti-journalism activism.

Not anti-truth. Anti-middleman. The project started because I wanted to understand politics better and noticed the way to do it was to stop reading coverage and start reading sources — because something is deeply off in the land of print and online.

If you've followed games journalism, you already know the mechanism. Embargo access, preview trips, review copies: cuddle with the subject of your reporting long enough and their viewpoints start seeping into the copy. Whoever wants access has to heel. Berlin political journalism runs the identical loop, just with ministries instead of publishers. Ask genuinely hard questions and you stop getting interview partners; stay harmless and you get the chancellor on your politics podcast — formats that have degraded into free airtime, retransmitting campaign promises without so much as a follow-up question.

The business model completes the picture, and it's beautifully inverted: the comment section — the part engineered to split people, because division is engagement — is free. The actual reporting sits behind the paywall. Outrage as the loss leader, information as the premium tier. Meanwhile the 90-page committee document that the 400-word article summarizes sits in a public API, timestamped and complete, read by approximately nobody.

Here's the sentence that will annoy everyone, so let me stand behind it: a language model reproduces mediocrity, at best. That happens to clear the bar for most of German political journalism. If your value-add over the primary source is a summary plus a framing, you are competing with `curl` piped into a tin can — and losing on price, speed, and blood pressure.

But replacement is the petty version of the goal. The real one is democratizing access. A normal citizen has neither the money to first train as a political scientist nor the decade for a traineeship just to work out what a law will actually do to them. The documents are public; the *literacy* was gatekept. An agent with these CLIs closes that gap — and sometimes the entire barrier is language: rewrite a committee report in plain German, or in another language altogether, and a document that was technically public becomes actually accessible. Plenty of people can consume politics straight from the source once someone removes the provocative framing that only ever served somebody else's revenue. I'm fairly certain I'm not the only one who wants that.

The manual version of this research already works and I've done it plenty: pull a member of parliament from the Bundestag's DIP system, enrich the picture at abgeordnetenwatch.de, then follow the person's pet topic down a FragDenStaat rabbit hole of freedom-of-information requests. Handwork, but it delivers — that route has genuinely surprised me more than once, and the surprises are the point. I go looking for my unknowns.

Handwork, though? Maybe not for long.

## The new Unix user has no hands

Agentic systems — the new machine god, as I've taken to calling it, with more patience than a trainee news desk and better organization than the people officially in charge of "Digitalisierung" — are terminal natives. Give an agent a tool that takes flags and returns JSON with a predictable schema and it uses it correctly on the first try; it has seen ten million CLIs in training. The shell *is* the integration layer. Every agent runtime on earth can execute a command; not every one speaks whatever protocol is fashionable this quarter. That's why it's CLI first, and why each repo ships agent skills alongside the binary — the CLI is the muscle, the skill is the manual.

Now hand an agent all 25 manuals and describe the DIP → abgeordnetenwatch → FragDenStaat workflow. It runs the whole rabbit hole in minutes, in parallel, with citations. And notice: entity matching across inconsistently named datasets — the state's main anti-interoperability defense — happens to be something language models are freakishly good at. The moat was designed for humans with browsers. It was not designed for this.

The traffic runs the other way too. These tin cans confabulate; producing plausible text is the whole job description, and a model will invent a river level or a committee vote without blinking. Feeding it primary data from calibrated government systems — a sensor bolted to a bridge, a document with an ID and a timestamp — is how you stop the machine from making things up. The APIs ground the model; the model joins the APIs. Fair trade.

How you combine thetools is, as far as I'm concerned, a secret between you and your computer.

## How does one even end up here

In a second repo sits a politics search engine that needs exactly this data for contextualization — a five-digit number of sources, collected since the RSS days. The engine has been through three eras that neatly mirror the last fifteen years of search itself: pure full-text before 2010, semantic search through 2020, and since 2025 both of those with a language model bolted on top. The CLIs are what that stack turned out to need: grounding. Fifteen-plus years of watching this ecosystem is where the interoperability thesis comes from; it's not a hot take, it's a scar.

## The boring parts, on purpose

Everything is AGPL. Every package ships an SBOM, because I've written enough about npm supply-chain attacks to refuse publishing anything opaque myself. Version numbers start at 0.0.x and mean it.

## The dark factory

Which leaves the question of how sixteen of these exist already and a hundred are plausible without me giving up sleep, food, or my remaining goodwill. The answer is the part of the project I find most instructive: the CLIs come out of a dark factory.

Manufacturing people know the term — lights-out production. FANUC has run plants in Japan where robots build robots for weeks at a stretch with the lights literally off, because nobody's in the building to need them. That, minus the sheet metal, is the production model here. There's a template repository that acts as the assembly line: project layout, flag conventions, test harness, CI, SBOM generation, npm publishing — the jigs and fixtures. A new government API enters at one end as raw material; agents read whatever passes for its documentation, probe the endpoints, generate the wrapper against the template, write the tests, write the agent skill, and a CLI comes out the other end, boxed and labeled like its fifteen siblings. When shared plumbing improves, the change propagates across every repo the same way — nobody hand-edits sixteen READMEs at 11 PM, because nobody hand-edits sixteen READMEs at all.

My job in this factory is not on the line. It's the job humans keep in every lights-out plant: I define the product, I set the tolerances, and I stand at the quality gate reading diffs before anything ships. Exception handling, in both senses.

Two consequences fall out of this, and they're the whole game. First, the marginal cost of wrapping one more government API is approaching the cost of caring about it — which is how "roughly a hundred" stops being bravado and becomes a backlog. Second, remember the state's favorite defense, the arbitrary format change? Against a hand-maintained scraper, lethal. Against a factory, it's a work order. The breakage lands in CI, an agent retools the line, I review the diff over coffee. The sabotage now costs the saboteur more than the target.

---

*The project lives at [github.com/maschinenlesbar-org](https://github.com/maschinenlesbar-org), with running commentary at [@maschinenlesbar.bsky.social](https://bsky.app/profile/maschinenlesbar.bsky.social). *
