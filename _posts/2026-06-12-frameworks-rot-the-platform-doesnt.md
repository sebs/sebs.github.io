---
layout: post
title: "Frameworks Rot. The Platform Doesn't."
date: 2026-06-12 18:46:48 +0000
permalink: "/2026/06/12/frameworks-rot-the-platform-doesnt/"
description: "A decision memo for anyone staring at their package.json and wondering.   Most arguments for leaving..."
tags: [ai, javascript, tco, webdev]
og_type: article
image: "/assets/posts/frameworks-rot-the-platform-doesnt/cover.png"
devto_url: "https://dev.to/sebs/frameworks-rot-the-platform-doesnt-58g0"
render_with_liquid: false
---


> *A decision memo for anyone staring at their `package.json` and wondering.*


Most arguments for leaving your SPA framework center on the upgrade treadmill — the endless cycle of major-version migrations, dependency churn, and build-tool turnover. That argument is real but incomplete, and on its own it has never been decisive: every framework shop has learned to live with the treadmill. There's a stronger case, built on four pillars that compound with each other.

First, **total cost of ownership**: vanilla JavaScript on the web platform has unusual TCO properties, dominated by a depreciation curve that is nearly flat. Code written against the platform does not rot, because its substrate does not change. Over long horizons, this single property outweighs almost every per-feature productivity argument in a framework's favor.

Second, **the labor market**: the pool of people who can work on vanilla JavaScript is not a niche within the frontend market — it is the entire frontend market, plus most of the backend market. Every framework developer is, underneath, a JavaScript developer. The reverse is not true. If you hire for a specific framework, you're hiring from a subset while telling yourself you're hiring from the mainstream.

Third, **AI leverage**: engineers now produce a growing share of code with AI assistance, and the economics of that assistance differ sharply by target. The web platform is a small, stable, exhaustively documented body of knowledge; a framework ecosystem is a large, fast-mutating one whose training data is perpetually stale. AI coding tools are measurably more reliable on the former. As AI-assisted development becomes the dominant mode of production, the substrate that AI handles best becomes the cheaper substrate — and the gap widens every year the platform stays still while frameworks move.

Fourth, **architecture**: porting to Web Components is not a transliteration of the same design into different syntax. The platform pushes toward a genuinely different architecture — autonomous, message-passing components rather than a centrally reconciled tree — and that architecture has its own economic consequences, mostly favorable for a broad class of applications, which you should adopt deliberately rather than discover by accident.

The recommendation, stated up front: if your application sits in the right quadrant — long-lived, stabilizing, forms-and-views rather than collaborative-canvas — migrate incrementally via the strangler pattern, and reject any big-bang rewrite. The rest of this post develops each pillar, the reasoning behind them, and the conditions under which the whole argument flips.

## 2. Tenets

Before the pillars, the principles they rest on. If you disagree with a conclusion below, the disagreement is probably with one of these — and that's the productive place to have it.

1. **Optimize total cost of ownership over the application's full life, not development cost over the next quarter.** A foundation's depreciation rate matters more than its day-one ergonomics.
2. **Measure labor pools at the skill floor, not the skill label.** The relevant question is not "how many React developers exist" but "how many people can become productive in this codebase in a month."
3. **The cost of code is increasingly the cost of supervising AI that writes it.** Substrates should be chosen partly for how well machines generate, verify, and maintain code on them.
4. **Architecture is an economic object.** Coupling structure determines change cost; choose the structure, don't inherit it from a library's render model.
5. **Prefer two-way doors.** A migration plan must be pausable mid-flight while still having paid for itself.

## 3. Pillar One: The TCO Curve of Platform-Native Code

Most software cost models obsess over construction cost and treat the maintenance tail as a multiplier. For long-lived applications, this is backwards: the tail is the animal. Industry experience consistently puts lifetime maintenance at several multiples of initial development, and the *composition* of that maintenance is what distinguishes substrates.

Framework code carries three maintenance components: (a) changes you choose to make — features, fixes; (b) changes the substrate forces on you — version migrations, deprecations, dependency security churn, toolchain turnover; and (c) the eventual full rewrite, when the foundation's liability exceeds the asset's value. Platform-native code carries only (a). Component (b) approaches zero because browsers do not ship breaking changes to the DOM; the platform's backwards-compatibility record spans decades, and code written against Custom Elements and CSS custom properties in 2026 will run unmodified in 2040. Component (c) — the scheduled-but-undated rewrite — is eliminated outright, and it's the largest single line in any honest long-horizon model: the cost of your entire application, again, plus the behavioral archaeology of rediscovering a decade of micro-decisions nobody remembers making.

The resulting picture is two depreciation curves. Framework code depreciates like a vehicle: it loses value continuously through ecosystem drift even when untouched, and requires periodic capital injections (major-version migrations) merely to retain function. Platform code depreciates like land with a building on it: the building — your features — needs upkeep proportional to how often *you* change it, but the ground does not move. On a four-year horizon the curves barely separate, and the framework's day-one ergonomics win. On a ten-year horizon the flat curve dominates decisively, with the crossover arriving well before year eight even under assumptions generous to the framework.

One honest cost on the vanilla side of the ledger: the platform lacks a built-in reactivity model, so any non-trivial app will carry a thin, standards-tracking layer — a few hundred lines of signals, or a micro-library like Lit. That's a maintenance liability you own. It's also bounded, inspectable, and sits on a substrate that doesn't move beneath it — a fundamentally different risk class from a framework's hundreds of thousands of lines on a quarterly release cadence.

## 4. Pillar Two: The Labor Pool Is Larger, Not Smaller

The conventional objection runs: "the market is full of React developers; vanilla and Web Components are a niche; you'd be narrowing your hiring funnel." This inverts the actual structure of the market.

Every framework developer writes JavaScript. The framework is a dialect on top of a language they already know; the DOM is the machine their framework ultimately drives. A vanilla codebase is therefore legible, at the floor, to the *union* of all framework communities — React, Vue, Angular, Svelte — plus the substantial population of full-stack and backend engineers who know JavaScript but never specialized in any frontend framework. A framework codebase is legible to one slice. When a company posts a role requiring deep experience in a specific framework *at a specific major version*, it filters the market twice: once by dialect, once by dialect vintage. Tenet 2 says to measure at the skill floor: the number of engineers who can be productive in a well-structured vanilla codebase within a month is a strict superset — several times over — of those who can be productive in any single framework codebase.

The second-order effects all point the same direction. **Onboarding** compresses, because there's no framework dialect, no bespoke state-management idiom, and no build-pipeline folklore to absorb; the learning surface is the platform itself — which every candidate has been marinating in their whole career — plus your domain. **Skill durability** improves: what engineers learn maintaining a vanilla codebase (DOM, events, encapsulation, the platform's actual contract) appreciates over their careers rather than expiring with a framework's market share — which, incidentally, makes such roles easier to sell to strong senior candidates who have been burned by dialect churn before. **Key-person risk** falls: you're no longer exposed to the scenario where your framework's talent pool thins as fashion moves on, leaving you bidding against scarcity for maintenance of an aging stack — the COBOL dynamic, arriving on a ten-year fuse.

The honest counterpoint: average familiarity with Shadow DOM specifics — slot composition, event retargeting, `ElementInternals` — is genuinely lower than average familiarity with mainstream framework idioms. Size that as a weeks-not-quarters training cost per engineer, set against a structural enlargement of the funnel. That's a trade worth taking eagerly.

## 5. Pillar Three: AI Leverage — The Small, Frozen Corpus Wins

A growing share of code is now produced with AI assistance, and the share keeps rising. This changes what "developer productivity" means: increasingly, the binding constraint is not how fast a human writes code but how reliably a model generates it and how cheaply a human verifies it. Substrate choice now has an AI term in it (Tenet 3), and the term favors the platform, for three structural reasons.

**The body of knowledge is small.** The web platform's API surface — DOM, events, Custom Elements, fetch, modern CSS — is compact and exhaustively specified. A framework ecosystem is that surface *plus* the framework's own large API, *plus* its state-management satellites, *plus* its meta-framework conventions, *plus* the idioms of whichever major version is current. A model asked to generate framework code is navigating a pattern space an order of magnitude larger, much of it convention rather than specification, where plausible-looking compositions are subtly wrong.

**The corpus is stable.** Models are trained on historical code. For a fast-moving framework, that history is a sediment of deprecated patterns: training data is dominated by yesterday's idioms, and the model confidently emits APIs that were removed two majors ago, mixes the old paradigm with the new one, or imports packages that have since been renamed. Anyone who uses AI assistants on framework code recognizes this failure mode; it converts generation speed into review burden. Platform APIs don't have this problem, because the correct pattern of 2016 is still the correct pattern of 2026. The training distribution and the deployment reality coincide. This appears to be a permanent structural advantage: it widens every year the platform stays still while frameworks move, and no amount of model improvement fully closes it, because the staleness is in the data, not the model.

**Verification is cheaper.** AI-generated vanilla code is checkable against a public specification and observable directly in a debugger; there's no reconciler between the code and its effect. AI-generated framework code must additionally be checked against framework semantics — rules of hooks, reactivity caveats, hydration constraints — exactly the kind of non-local, convention-encoded correctness conditions that models violate most and reviewers catch slowest.

The economic translation: if AI assistance produces correct-on-first-pass code meaningfully more often on platform targets — and the day-to-day experience of teams suggests it does — then per-feature production cost on the platform falls faster than on the framework as AI adoption deepens. The framework's traditional advantage was developer ergonomics for humans. In a regime where machines write the first draft, ergonomics-for-machines is the metric, and it points the other way. The benefit is symmetric, too: a smaller, stable codebase with no framework dialect is easier for AI tools to *read*, making AI-assisted maintenance, migration, and onboarding cheaper as well.

## 6. Pillar Four: It Is a Different Architecture, and That Is the Point

A framework SPA, whatever its component syntax, is architecturally a *centrally coordinated* system: a single reconciler owns the tree, state changes flow through a global scheduler, and components are functions evaluated inside someone else's run loop. This buys coherence and costs coupling — every component is coupled to the coordinator's semantics, which is precisely why framework migrations are total rather than partial. You cannot move one limb at a time when one brain runs the body.

Web Components push toward the opposite: an architecture of *autonomous cells*. Each custom element owns its state, its shadow-encapsulated rendering, and its lifecycle; coordination happens at the edges, through attributes and properties going down and composed DOM events bubbling up — message passing, not shared reconciliation. The DOM itself becomes the integration layer, which is to say the integration layer is standardized, inspectable, and owned by no vendor.

This architecture has economic consequences worth naming explicitly. **Change locality:** with state and rendering encapsulated per element and styling hard-bounded by the shadow root, the blast radius of a change is structurally small; cost-of-change correlates with the size of the change rather than the size of the application. **Independent evolvability:** components can be rewritten, replaced, or owned by different teams on different schedules, because the contract between them is the DOM, not a framework version — this is the property that makes incremental migration possible at all, and it persists afterward as a permanent option to adopt or shed any future technology one component at a time. **Failure isolation:** autonomous cells degrade locally; a broken widget is a broken widget, not a poisoned render tree. **Honest costs:** truly cross-cutting state — session, theming, live shared data — requires deliberate design (a small event bus or shared reactive stores) rather than reaching for a framework's global store; and deeply orchestrated interactions spanning many components are genuinely harder to express than in a centralized model. For applications shaped like many semi-independent views over a domain model — most business software, most dashboards, most content products — the trade is strongly favorable. For a real-time collaborative canvas, it isn't, and it's better to say so than to pretend.

The strategic point of Tenet 4: don't port the old architecture into new syntax. The migration's full return is only collected if you adopt the cell architecture deliberately — defining element contracts, event taxonomies, and the thin shared-state layer up front — so that what you build is not "your framework app, minus the framework," but a system whose coupling structure is itself the asset.

## 7. Risks, Reversal Conditions, and the Way to Actually Do It

The pillars share failure modes worth naming. The TCO argument fails if the application's life is cut short — below roughly five years, the flat curve never overtakes. The labor argument fails if the codebase is structured so idiosyncratically that the "anyone who knows JavaScript" floor becomes theoretical; the mitigation is the deliberate architecture of Pillar Four plus written contracts. The AI argument is the youngest and deserves humility plus instrumentation — track first-pass acceptance rates of AI-generated changes on platform-native versus framework surfaces and let the data speak. The architecture argument fails if the product is heading toward heavy cross-component choreography; treat that as a named trigger to reconsider.

And the execution model matters as much as the destination, because the all-at-once rewrite is the highest-risk version of this trade. Web Components offer a uniquely cheap alternative, since custom elements work *inside* any framework: freeze the framework version first (instantly recovering the upgrade-treadmill capacity, before a single component is ported), build all new components as custom elements mounted within the existing app, convert old components opportunistically when feature work touches them anyway (so the behavioral archaeology is paid for by the feature), and remove the framework shell last, when it has been reduced to routing and a mount point. Each phase pays for itself; the plan is pausable at every stage; even abandoning it after the freeze leaves you better off than before. That's the two-way door of Tenet 5 — and it's the property that turns this from a bet into a position you can adjust.

---

## Appendix: Anticipated Questions (FAQ)

**Q: The hiring argument seems backwards — job boards show far more framework roles than vanilla roles.**
A: Job postings measure employer demand for dialects, not the supply of capable engineers. The claim here is about supply at the skill floor: everyone writing those framework apps knows JavaScript and the DOM underneath. Going vanilla widens your funnel to the union of all camps; the postings only tell you most employers haven't noticed.

**Q: Won't AI tools get good enough at frameworks that Pillar Three evaporates?**
A: Models will improve at everything, but the framework penalty is structural, not capability-based: training corpora lag a moving target, and convention-heavy correctness is harder to verify than specification-backed correctness. A better model narrows the gap per task while framework churn re-widens it. Stability is the moat, and only the platform has it.

**Q: Isn't "autonomous cells coordinated by events" just microservices on the frontend, with all the same distributed-system pain?**
A: It shares the virtue — independent evolvability — without the worst costs: no network between components, synchronous composition, and a standardized integration layer (the DOM) that nobody has to build or operate. The genuine analogous cost, designing cross-cutting state deliberately, is acknowledged in Pillar Four and should be budgeted, not discovered.

**Q: If platform TCO is so superior, why do new projects keep choosing frameworks?**
A: Because most projects rationally optimize time-to-first-ship on a short horizon, and frameworks win that race. The argument here is about years five through fifteen of an application's life, where the curves invert. Different phase, different optimum — and most TCO discussions never get past phase one.

**Q: What single metric tells a team in a year whether this was right?**
A: Fully-loaded cost per shipped change on converted surfaces versus unconverted ones — inclusive of review time and AI-assist acceptance rates. If converted surfaces aren't cheaper to change within a couple of quarters, the two-way door is right there.
