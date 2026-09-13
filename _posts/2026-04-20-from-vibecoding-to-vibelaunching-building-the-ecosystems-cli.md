---
layout: post
title: "From Vibecoding to Vibelaunching: Building the ecosystems-cli"
date: 2026-04-20 18:58:07 +0000
permalink: "/2026/04/20/from-vibecoding-to-vibelaunching-building-the-ecosystems-cli/"
description: "12 months ago I set a goal: ship a production-ready CLI for the ecosyste.ms API, in Python. Some..."
tags: [vibecoding, python, programming, ai]
og_type: article
image: "/assets/posts/from-vibecoding-to-vibelaunching-building-the-ecosystems-cli/cover.png"
devto_url: "https://dev.to/sebs/from-vibecoding-to-vibelaunching-building-the-ecosystems-cli-nje"
render_with_liquid: false
---

12 months ago I set a goal: ship a production-ready [CLI](https://github.com/ecosyste-ms/ecosyste_ms_cli) for the ecosyste.ms API, in Python. Some commits later, ecosystems-cli is about to land on PyPI. A deliberate attempt to take LLM-assisted development seriously on something larger than a toy.

## Why bother

I follow the AI critics and agree there are real risks in LLM-supported development. But criticism grounded only in theory is thin. I wanted more than the same twenty one-trick-pony demos that cycle through LinkedIn every week. So I picked a language I don't work in daily (Python) to reproduce the quintessential vibecoding condition — a little out of my depth — and built something I'd actually use, because we were using ecosyste.ms at work.

## The setup isn't traditional anymore

The project is developed with Claude Code, but the "setup" has drifted a long way from what that phrase usually implies. My baseline expectation is now, that a coding LLM can follow the Zen of Python and write real tests. From the initially used 'instruction heavy mode', something interesting happens: **over time, the code turns into spec via the unit tests.** The tests pin behaviour; the code becomes the executable description of that behaviour; and the next change — refactor, rewrite, port — starts from a spec that's already true. These days: no skills, no Claude.md, etc. Plain: open a session and tell the clanker what to do. 

The practical payoff is replayability. I can blow up a module, regenerate it, and the test suite tells me whether I'm back where I was. On larger projects, that's a qualitatively different experience than any setup I've used before.

## What actually took 10 months

> Work work (Peons, Warcraft II)

- **API client approach.** Started with an OpenAPI-generated client, abandoned it for a custom implementation, then migrated to a mature third-party library once I understood the domain well enough to evaluate one.
- **Release pipeline.** The unglamorous CI/CD grind is where some of the time went.
- **17 endpoints + MCP integration.** Wrapping each endpoint is concrete, bounded work. MCP added another layer.
- **Python as a second language.** Syntax is the easy part; idioms, tooling conventions, and ecosystem norms take longer. Early decisions got revisited as my understanding deepened.
- **Continuous refactoring.** Fighting unnecessary abstraction is constant. Several designs got simplified once they failed to earn their keep. 

### OpenCollective changed the trajectory

When ecosyste.ms adopted the CLI officially and started funding it via OpenCollective, the project stopped being a side experiment and started being worth finishing properly. It's not keep-the-lights-on money, but it's a meaningful signal — and it bought the time for the boring, essential work: test coverage, documentation, dependency management, a reliable release pipeline. That's the real line between prototype and production.

### Takeaways

1. **Be willing to throw out early architecture.** The generated client → custom → library arc wasn't waste; each step taught the next.
2. **Infrastructure is not optional.** A serious chunk of any real project is CI/CD, tests, and release plumbing.
3. **Refactoring is continuous.** Especially with an LLM in the loop — it happily generates abstractions that don't earn their keep unless you push back.
4. **Tests are the spec.** This is the unlock. If your test suite describes behaviour well, the code underneath becomes replaceable. That's what makes LLM-assisted development work at scale instead of collapsing into spaghetti.
5. **Funding enables quality.** The non-feature work that separates a tool from a toy doesn't happen on evenings and weekends indefinitely.Thanks to [ecosyste.ms](https://ecosyste.ms)  
6. **Some problems are 'LLM hard'**: Parameter parsing in such a large app with nuanced differences in underlying API structure - Mission impossible. 


The result is a CLI that's functional, maintainable, and ready to be used by people who aren't me. To end up in a 'Instructionless mode' is quite surprising, but surely a result of python leaning to a minimalism that is to be found in 'The Zen of Python'.
