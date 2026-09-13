---
layout: post
title: "From Cardboard to Code"
date: 2026-04-10 22:43:15 +0000
permalink: "/2026/04/10/from-cardboard-to-code/"
description: "RuleForge, a suite of Claude Code slash commands, turns a board game rulebook PDF into a developer bundle with GDD, user stories and architecture diagrams."
tags: [ai-assisted-development, game-development, developer-tooling]
og_type: article
image: "/assets/posts/from-cardboard-to-code/og.jpg"
devto_url: "https://dev.to/sebs/from-cardboard-to-code-29d5"
render_with_liquid: false
---


> The design challenge isn't understanding board games. It's turning prose rules into structures a software team can actually act on.

There are thousands of board games. Most of them contain fascinating design work: carefully balanced economies, elegant interaction models, loop structures refined over years of playtesting. Almost none of them exist as digital games. The barrier is real work — translating a 40-page rulebook into a game design document, a feature backlog, an architecture diagram, user stories — before a single line of code is written.

[RuleForge](https://github.com/sebs/ruleforge) automates that translation. You hand it a PDF. It hands you a developer bundle.

---

## What it actually does

At its core, RuleForge is a suite of Claude Code slash commands stored in a `.claude/commands/` directory. Each command is a focused AI workflow targeting one specific phase of the board-game-to-digital-game translation process. They can be run individually, or chained together through the main `/ruleforge` pipeline command.

The full pipeline runs 16 stages and produces a self-contained output directory scoped to the game — something like `output/catan/` or `output/terraforming-mars/` — filled with structured files ready for a development team.

---

## The pipeline, step by step

**1. `/complexity-estimate` — Quick pre-flight scan**
Before committing to the full pipeline, get a fast complexity estimate. How long is the rulebook? How many mechanics? Is this a 20-minute job or a 2-hour one?

**2. `/ruleforge` — Full pipeline, PDF to developer bundle**
The main event. Extracts rules, identifies mechanics, generates the game loop diagram, writes the GDD, builds the feature list, creates user stories, outputs architecture diagrams. Resumable if interrupted.

**3. `/card-database` + `/economy-flow` — Domain-specific extraction**
Card-heavy games need their component databases structured. Economy-driven games need their resource flows mapped — sources, sinks, conversions. These commands go deeper on those specific concerns.

**4. `/accessibility-audit` — Check for digital barriers**
Audits the extracted design across five accessibility dimensions: visual, motor, cognitive, hearing, and communication. Digital ports are an opportunity to do better than the physical original.

**5. `/realtime-forge` — Translate to interactive game design**
The big leap. Takes the RuleForge output and translates it into a real-time or interactive digital game design — covering analysis, a revised GDD, architecture, balance sheets, asset specifications, and prototype prompts. Seven waves, roughly 30 output files.

**6. `/dev-bundle` — Validate and package**
Validates all output files including Mermaid diagram syntax, checks for completeness, and packages everything into a clean bundle ready to hand off.

---

## The full command library

### Extraction & Analysis

| Command | What it does |
|---|---|
| `/extract-rules` | Parse and summarize the rules from a PDF. The raw input layer. |
| `/identify-mechanics` | Classify game mechanics across 25 standard types — Worker Placement, Deck Building, Area Control, Engine Building, and so on. |
| `/game-loop` | Generate a Mermaid diagram of atomic, primary, secondary, and tertiary game loops. |
| `/validate-loop` | Check the game loop for structural soundness and state reachability. Catches design dead ends. |
| `/adaptation-gap` | Report on how much work a digital port actually requires — No Change / Simple Adaptation / Redesign. |
| `/flag-ambiguities` | Surface rules that are unclear, contradictory, or likely to cause bugs when implemented. |
| `/confidence-score` | Self-assessment of extraction quality. Useful for knowing when to do a manual review. |

### Design & Documentation

| Command | What it does |
|---|---|
| `/generate-gdd` | Full Game Design Document. Chunked automatically for complex games. |
| `/balance-sheet` | Extract balance parameters with digital annotations and sensitivity analysis. |
| `/feature-list` | Prioritized feature list output as both CSV and Markdown, with a dependency diagram. |
| `/user-stories` | User stories with granularity selector and acceptance criteria. Outputs to Stories.csv. |
| `/onboarding-design` | Tutorial and onboarding flow design — how a new player learns the game digitally. |
| `/interaction-model` | Component interaction model — how game entities relate to and affect each other. |

### Architecture & Prototyping

| Command | What it does |
|---|---|
| `/architecture-diagram` | System architecture in Mermaid. Supports Unity, Godot, Phaser, Web, or generic targets. |
| `/prototype-prompts` | AI prototyping prompts for Rosebud, v0, Bolt, Lovable, or generic tooling. |
| `/economy-flow` | Resource economy diagram — where resources come from, where they go, and how they convert. |
| `/card-database` | Extracts individual card, tile, or component data into a structured database. |

### Standalone Utilities

| Command | What it does |
|---|---|
| `/game-mixer` | Blend mechanics from two or more games into hybrid designs, with iteration support. |
| `/decompose-idea` | Break down a game idea using a 7-category ludemic framework. |
| `/ludeme-generator` | Generate a Ludii game description file (.lud) from a concept. |
| `/game-fitness` | Analyze a game concept across 6 fitness dimensions. |
| `/playtest-design` | Design an automated playtesting plan with fitness functions. |
| `/procedural-generator` | Design procedural generation systems using the Watson et al. (2008) workflow. |
| `/game-comparison` | Side-by-side comparison of two RuleForge extractions. |
| `/pdf-to-markdown` | Convert any PDF to clean, well-structured Markdown. Useful as a standalone tool. |

---

## The output structure

Every skill writes into a game-scoped directory under `output/`. The game slug is derived automatically from the title in the rulebook. A `.context.json` metadata file lets downstream commands pick up where upstream ones left off — that's what makes the pipeline resumable.

A typical output for something like Terraforming Mars would contain a GDD, a feature CSV, a user stories CSV, Mermaid files for the game loop and architecture, a balance sheet, an onboarding flow design, and prototype prompts ready to paste into your AI prototyping tool of choice.

---

## The solo dungeon bash

The repository also ships a `solo-dungeon-bash/` directory — a worked example of the pipeline in action on a solo dungeon-crawl game. It's useful both as a reference output and as a test case to understand what the extraction quality actually looks like on a real game with real rules.

---

## Why slash commands, not a CLI tool?

This is a deliberate choice. Claude Code's slash command system makes each step conversational and inspectable. You can run `/identify-mechanics`, read the output, decide the model missed a nuance, correct it manually, and then continue with `/game-loop`. That feedback loop would be much harder to preserve in a fully automated CLI pipeline.

It also means the tool is essentially zero-setup. Clone the repo, point Claude Code at the directory, and the commands are available. No build step, no package install, no configuration.

---

## Get started

The project is on GitHub at [github.com/sebs/ruleforge](https://github.com/sebs/ruleforge). Clone it, drop a rulebook PDF next to it, and start with `/complexity-estimate path/to/your-game.pdf`.

The design is intentionally modular — you don't have to run the full pipeline. If you just need a GDD from a rulebook, run `/generate-gdd`. If you want to compare two games, run `/game-comparison`. Each command is independently useful.

Board games are some of the most densely designed interactive systems humans have made. RuleForge is a bet that those designs are worth bringing into software — and that AI can do a lot of the translation work.
