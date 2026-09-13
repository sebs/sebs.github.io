---
layout: post
title: "It's Time We All Eat some more Cucumber!"
date: 2026-06-08 09:22:09 +0000
permalink: "/2026/06/08/its-time-we-all-eat-some-more-cucumber/"
description: "Everyone's writing specs for AI now. We hand the model a markdown file, tell it what we want, and..."
tags: [ai, tdd, bdd, darkfactory]
og_type: article
image: "/assets/posts/its-time-we-all-eat-some-more-cucumber/cover.webp"
devto_url: "https://dev.to/sebs/its-time-we-all-eat-some-cucumber-16ic"
render_with_liquid: false
---


Everyone's writing specs for AI now. We hand the model a markdown file, tell it what we want, and hope it builds the right thing. It mostly works — until it doesn't.

Markdown has quietly become the spec language. People reach for it as the DSL for their AI-driven workflows — headings, bullet lists, the odd table — and treat that loose structure as if it were a contract. The thing is, it isn't a DSL. It's markdown. It's prose formatting with no grammar to enforce, no structure you can execute, no shared vocabulary, and no way to tell whether the spec and the code still agree. You're leaning on a document format to do a job it was never built for, and you hit the limit the moment you want the spec to actually *mean* something a machine can check.

Before you go down that road, I want to make a small, slightly absurd suggestion.

Eat a cucumber.

## What I actually mean

[Gherkin](https://cucumber.io/docs/gherkin/) is the plain-text language behind [Cucumber](https://cucumber.io/), a tool that's been around for years in the behavior-driven development (BDD) world. It looks like this:

```gherkin
Feature: User login

  Scenario: Successful login with valid credentials
    Given a registered user "ada@example.com"
    When she logs in with the correct password
    Then she should land on her dashboard
    And she should see a welcome message

  Scenario: Rejected login with wrong password
    Given a registered user "ada@example.com"
    When she logs in with an incorrect password
    Then she should see an "invalid credentials" error
    And she should remain on the login page
```

That's it. `Feature`, `Scenario`, `Given`/`When`/`Then`. Structured enough that a machine can parse it, loose enough that a product manager can write it.

## The gap it bridges

Most specs live at one of two extremes.

On one end you have **written specs**: docs, tickets, markdown files. Readable by anyone, but inert. Nothing checks whether they're still true. They rot the moment the code moves on.

On the other end you have **tests**: precise, executable, always honest — but written in code, illegible to half the people who actually care about the behavior.

Gherkin sits in the middle. It's prose with just enough skeleton that you can wire each `Given`/`When`/`Then` step to real code. The same file is both the human-readable spec *and* the thing your test runner executes. When the behavior changes, the scenario fails. The spec can't quietly drift away from reality, because the spec *is* the check.

That's what people mean by "living specs": documentation that can't lie to you because it runs.

## The signals you've outgrown markdown

You don't switch formats on principle. You switch when the document starts straining against what it can express. Three signals tell you you're there.

**When the markdown gets too specific.** A spec starts as a paragraph of intent. Then someone adds a bullet for the edge case, then a sub-bullet for the exception to the edge case, then a parenthetical for what happens on a leap year. The prose is now pretending to be a state machine. Each of those specifics is really a *scenario* — a concrete given/when/then — and markdown gives you no way to mark it as one, let alone check it. Gherkin does: every specific behavior becomes its own named scenario you can point at, run, and reason about in isolation.

**When tables of example data start to appear.** This is the clearest tell. The moment your spec contains a table — input A gives output X, input B gives output Y — you've stopped describing behavior and started enumerating cases. A markdown table just *sits* there; nothing verifies that row three is still true. Gherkin has this built in with `Scenario Outline` and `Examples`:

```gherkin
Scenario Outline: Discount applied by tier
  Given a customer on the "<tier>" plan
  When they check out with a cart total of <total>
  Then the discount applied should be <discount>

  Examples:
    | tier    | total | discount |
    | free    | 100   | 0        |
    | pro     | 100   | 10       |
    | premium | 100   | 25       |
```

Same readable table — except every row is now an executable test case. Add a row, you've added a test. The data table *is* the spec.

**When requirements are subject to change and re-evaluation.** If a requirement will never move, a comment in the code is fine. The cost of a living spec only pays off when things change — and AI-driven work changes constantly. When a rule shifts, you want one place to edit that immediately tells you what broke. With markdown, you change the prose and hope someone updates the code to match; nothing flags the drift. With Gherkin, you change the scenario, run it, and the failures show you exactly where reality no longer agrees. The spec becomes the thing you re-evaluate against, not a stale artifact you forget to update.

## Why this matters for AI work

If you're feeding specs to an LLM to generate or verify code, Gherkin gives you three things a freeform markdown file doesn't:

- **A fixed grammar.** The model doesn't have to guess your invented structure. Gherkin's vocabulary is small, well-documented, and almost certainly already in the model's training data.
- **Executable acceptance criteria.** The AI can generate code *and* you can immediately run the scenarios to see if it actually did the job — no human re-reading the markdown to judge.
- **A round trip.** You can ask the model to write scenarios from a description, write code from scenarios, or check that existing code satisfies them. Each direction has a clear, checkable artifact.

You get the readability you wanted from markdown, plus a definition of "done" that a machine can enforce.

## Start small

You don't need to adopt all of BDD or restructure your team. Take one feature you're about to spec for your AI tooling and write it as a `.feature` file instead of a markdown blob. See how it feels to have the spec and the test be the same document.

You're already using a document format as a spec language. This one was actually built to be one — it already exists, already has tooling in every major language, and already solved the problem markdown keeps quietly failing at.

So: put the markdown back where it belongs. Eat the cucumber.
