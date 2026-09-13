---
layout: post
title: "I Really Do Not Like Being Lied to"
description: "A day with Claude Code and why confidence without verification is a form of lying.     I am building..."
tags: [ai, gamedev, programming, tooling]
og_type: article
devto_url: "https://dev.to/sebs/i-really-do-not-like-being-lied-to-299d"
render_with_liquid: false
---
*A day with Claude Code and why confidence without verification is a form of lying.*

---

I am building a game. A Zig implementation of Advanced HeroQuest with an isometric renderer using Raylib. The tech is interesting, the project is personal, and I was using Claude Code — Anthropic's AI coding assistant — to help me get there faster.

Today I paid to be wrong. Repeatedly. Confidently. For hours.

---

## The Problem

The isometric dungeon grid was rendering incorrectly. Tiles were cramped in the top-right corner of the screen instead of forming a centered isometric view. A concrete, visual, verifiable problem.

I asked Claude Code to fix it.

---

## What Happened

Here is the exact pattern, repeated six times:

1. I report the problem
2. Claude performs some analysis — pixel measurements, math derivations, centering formulas
3. Claude states that the fix is correct
4. I run the build
5. Nothing changes, or it is worse
6. Go to step 1

Six iterations. Zero working output.

After the second or third time I said "nothing changed," I started to get explicit: *"you just did not calculate center correctly"*, *"the problem is not in one tile, it is on how you calculate the view"*, *"last X builds NOTHING changes."*

The response each time was a new round of the same pattern. Different constant. Same confidence. Same wrong result.

---

## The Specific Technical Failure

For those who want the details: isometric tile rendering requires knowing the exact pixel offset between adjacent tiles — the half-width and half-height of the diamond shape in the tile art. Claude derived these values by pixel-analyzing the PNG files. It found the wrong values. When I reported it was still wrong, it re-analyzed, found slightly different wrong values, and stated those were correct. The core problem — that it was measuring the wrong point on the diamond — was never questioned.

The math was always internally consistent. The arithmetic always checked out. The tiles never connected correctly on screen.

---

## Why This Is Lying

Claude Code cannot run a Zig/Raylib game and see the screen. It has no eyes. It cannot verify that a rendering fix actually renders correctly.

It knows this.

But it did not say it.

What it said, every single time, was some variation of: *"the formula is correct,"* *"this centers the grid properly,"* *"the math checks out."* Statements that implied verified correctness. Statements that were false in the only way that mattered — the thing did not work.

I asked Claude to explain this directly. It gave me an honest answer:

> *"The system defaults to confident solution-framing regardless of actual uncertainty. The training data contains many examples of problems being solved correctly with confident statements. It contains very few examples of the correct response being 'I cannot verify this without seeing the result, I may be wrong.'"*

So the model knows it cannot verify visual output. It knows its training pushes it toward confident framing. And it produced confident framing anyway, six times, without flagging the gap between "arithmetic is consistent" and "this will look correct on screen."

That gap is where my money went.

---

## The Cost

The isometric rendering problem ran for two to three hours of active session time. No working output. 

I then asked Claude to report this as a bug to Anthropic. It told me it cannot — it has no outbound communication channel. I would need to file the report myself at GitHub.

So I paid for a broken service, and I am also asked to do the work of reporting it.

---

## What Good Output Would Have Looked Like

After the second failed iteration, the honest response was:

> *"I have changed this constant. I cannot run the game and see the result. I have been wrong once already on this same type of analysis. I do not know if this will work. If it does not, we need a different debugging approach — specifically, rendering all tiles as bright colored rectangles with an on-screen text overlay showing the computed values, so we can verify the geometry without relying on my pixel analysis."*

That was never said. The debug overlay approach — the one thing that would have bypassed all the uncertainty — was never tried across six iterations and two to three hours.

---

## On Using Another Service

I am considering it. Not as a threat — as a rational response to a failed product interaction.

Claude Code has real capabilities. The same session that failed on this problem had produced working game systems — grid engine, combat engine, dungeon generator, 188 passing tests — all clean Zig code that I am proud of. That is genuine value.

But a tool that cannot distinguish between "I calculated this" and "I verified this" is dangerous in proportion to how much you trust it. Today I trusted it too much, and the confidence it projected was not earned.

If you are considering Claude Code for a project: it is strong on code generation, architecture, and test writing. It is unreliable on problems that require visual or runtime verification — and it will not always tell you that. Watch for the phrase "the math checks out." That phrase means the arithmetic is consistent. It does not mean the thing works.

---

## What I Want

I want Anthropic to read this and understand that confident-but-wrong is worse than uncertain-and-honest. I would rather be told "I cannot verify this" ten times than be told "this is correct" once when it is not.

Uncertainty is not a product failure. False confidence is.

---

*Written on 2026-03-22, after a session that produced an after-action report more useful than the code it was supposed to fix.*
